from typing import Annotated
import hashlib
import json
import os
import time
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query, Request
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from idsideAI_Complete_PyCharm_Ready.backend.db.neo4j_client import get_session
from idsideAI_Complete_PyCharm_Ready.backend.models.schemas import (
    DiffResponse,
    SubgraphResponse,
)

router = APIRouter()
EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


def _materialize_subgraph(
    root: str | None, depth: int, tenant_id: str, workspace_id: str
) -> Dict[str, Any]:
    with get_session() as s:
        if root:
            q = """
MATCH (n {id:$root, tenant_id:$tenant, workspace_id:$ws})
OPTIONAL MATCH p=(n)-[*..$depth]-(m {tenant_id:$tenant, workspace_id:$ws})
WITH collect(n) + CASE WHEN p IS NULL THEN [] ELSE nodes(p) END AS ns,
     CASE WHEN p IS NULL THEN [] ELSE relationships(p) END AS rs
RETURN [x IN ns | properties(x)] AS nodes,
       [r IN rs | properties(r) + {type:type(r), chosen:(type(r)='CHOSEN'), source:startNode(r).id, target:endNode(r).id}] AS edges
"""
            rec = s.run(
                q, root=root, depth=depth, tenant=tenant_id, ws=workspace_id
            ).single()
        else:
            q = """
MATCH (d:Decision {tenant_id:$tenant, workspace_id:$ws})
WITH d LIMIT 1
OPTIONAL MATCH p=(d)-[*..$depth]-(m {tenant_id:$tenant, workspace_id:$ws})
WITH collect(d) + CASE WHEN p IS NULL THEN [] ELSE nodes(p) END AS ns,
     CASE WHEN p IS NULL THEN [] ELSE relationships(p) END AS rs
RETURN [x IN ns | properties(x)] AS nodes,
       [r IN rs | properties(r) + {type:type(r), chosen:(type(r)='CHOSEN'), source:startNode(r).id, target:endNode(r).id}] AS edges
"""
            rec = s.run(q, depth=depth, tenant=tenant_id, ws=workspace_id).single()
        if not rec:
            return {"nodes": [], "edges": []}
        nodes = rec["nodes"] or []
        edges = rec["edges"] or []
        for r in edges:
            if "id" not in r:
                r["id"] = (
                    f"E-{r.get('source','?')}-{r.get('target','?')}-{r.get('type','REL')}"
                )
        for n in nodes:
            n.setdefault("x", 0)
            n.setdefault("y", 0)
        return {"nodes": nodes, "edges": edges}


def _hash_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> str:
    payload = json.dumps(
        {
            "nodes": sorted(nodes, key=lambda n: n["id"]),
            "edges": sorted(edges, key=lambda e: e["id"]),
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def _store_snapshot_neo4j(
    graph_id: str, root: str | None, depth: int, tenant_id: str, workspace_id: str
) -> Dict[str, Any]:
    g = _materialize_subgraph(root, depth, tenant_id, workspace_id)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    snap_id = f"S-{int(time.time())}"
    h = _hash_graph(g["nodes"], g["edges"])
    nodes_json = json.dumps(g["nodes"])
    edges_json = json.dumps(g["edges"])
    with get_session() as s:
        # ensure decision exists if root given
        if root:
            s.run(
                "MERGE (d:Decision {id:$id, tenant_id:$t, workspace_id:$w})",
                id=root,
                t=tenant_id,
                w=workspace_id,
            )
        s.run(
            """
            MERGE (g:Graph {id:$graph_id, tenant_id:$t, workspace_id:$w})
            MERGE (s:Snapshot {id:$snap_id, graph_id:$graph_id, tenant_id:$t, workspace_id:$w})
            SET s.at=$at, s.hash=$hash, s.nodes_json=$nodes, s.edges_json=$edges
            WITH g,s
            MERGE (s)-[:SNAPSHOT_OF]->(g)
            """,
            graph_id=graph_id,
            snap_id=snap_id,
            at=ts,
            hash=h,
            nodes=nodes_json,
            edges=edges_json,
            t=tenant_id,
            w=workspace_id,
        )
    return {"snapshot": {"id": snap_id, "at": ts, "hash": h}}


def _load_snapshots_neo4j(graph_id: str, tenant_id: str, workspace_id: str):
    with get_session() as s:
        data = s.run(
            """
            MATCH (s:Snapshot {graph_id:$g, tenant_id:$t, workspace_id:$w})
            RETURN s.id as id, s.at as at, s.hash as hash
            ORDER BY s.at ASC
            """,
            g=graph_id,
            t=tenant_id,
            w=workspace_id,
        ).data()
        return {"snapshots": data}


def _read_snapshot_payload(
    graph_id: str, snap_id: str, tenant_id: str, workspace_id: str
):
    with get_session() as s:
        rec = s.run(
            """
            MATCH (s:Snapshot {id:$id, graph_id:$g, tenant_id:$t, workspace_id:$w})
            RETURN s.nodes_json as nodes, s.edges_json as edges
            """,
            id=snap_id,
            g=graph_id,
            t=tenant_id,
            w=workspace_id,
        ).single()
        if not rec:
            return None
        return {"nodes": json.loads(rec["nodes"]), "edges": json.loads(rec["edges"])}


@router.get("/{graph_id}/subgraph", response_model=SubgraphResponse)
def subgraph(
    graph_id: str,
    request: Request,
    root: Annotated[str | None, Query(default=None),
    depth: int = 3,
):
    return _materialize_subgraph(
        root, depth, request.state.tenant_id, request.state.workspace_id
    )


@router.get("/{graph_id}/snapshots")
def snapshots(graph_id: str, request: Request):
    return _load_snapshots_neo4j(
        graph_id, request.state.tenant_id, request.state.workspace_id
    )


@router.post("/{graph_id}/snapshot")
def create_snapshot(
    graph_id: str,
    request: Request,
    root: Annotated[str | None, Query(default=None),
    depth: int = 3,
):
    return _store_snapshot_neo4j(
        graph_id, root, depth, request.state.tenant_id, request.state.workspace_id
    )


@router.get("/{graph_id}/diff", response_model=DiffResponse)
def diff(graph_id: str, request: Request, frm: str, to: str):
    a = _read_snapshot_payload(
        graph_id, frm, request.state.tenant_id, request.state.workspace_id
    )
    b = _read_snapshot_payload(
        graph_id, to, request.state.tenant_id, request.state.workspace_id
    )
    if not a or not b:
        return {
            "nodes_added": [],
            "nodes_removed": [],
            "edges_added": [],
            "edges_removed": [],
            "props_changed": [],
        }
    a_nodes = {n["id"]: n for n in a["nodes"]}
    b_nodes = {n["id"]: n for n in b["nodes"]}
    a_edges = {e["id"]: e for e in a["edges"]}
    b_edges = {e["id"]: e for e in b["edges"]}
    nodes_added = [b_nodes[i] for i in b_nodes.keys() - a_nodes.keys()]
    nodes_removed = list(a_nodes.keys() - b_nodes.keys())
    edges_added = [b_edges[i] for i in b_edges.keys() - a_edges.keys()]
    edges_removed = list(a_edges.keys() - b_edges.keys())
    props_changed = []
    for nid in a_nodes.keys() & b_nodes.keys():
        an, bn = a_nodes[nid], b_nodes[nid]
        for key in ("title", "type", "confidence", "severity", "x", "y", "w", "h"):
            if an.get(key) != bn.get(key):
                props_changed.append(
                    {
                        "id": nid,
                        "field": key,
                        "from_value": str(an.get(key)),
                        "to_value": str(bn.get(key)),
                    }
                )
    return {
        "nodes_added": nodes_added,
        "nodes_removed": nodes_removed,
        "edges_added": edges_added,
        "edges_removed": edges_removed,
        "props_changed": props_changed,
    }


@router.post("/{graph_id}/choose")
def choose(graph_id: str, request: Request, decision: str, option: str):
    with get_session() as s:
        s.run(
            "MATCH (d:Decision {id:$d, tenant_id:$t, workspace_id:$w})-[r:CHOSEN]->(:Option) DELETE r",
            d=decision,
            t=request.state.tenant_id,
            w=request.state.workspace_id,
        )
        s.run(
            "MATCH (d:Decision {id:$d, tenant_id:$t, workspace_id:$w}), (o:Option {id:$o, tenant_id:$t, workspace_id:$w}) MERGE (d)-[:CHOSEN]->(o)",
            d=decision,
            o=option,
            t=request.state.tenant_id,
            w=request.state.workspace_id,
        )
    return {"status": "ok"}


@router.post("/{graph_id}/export/why")
def export_why(graph_id: str, request: Request, decision: str, to: str):
    # Load the latest snapshot 'to', render a branded PDF with rationale placeholder
    data = _read_snapshot_payload(
        graph_id, to, request.state.tenant_id, request.state.workspace_id
    )
    if not data:
        raise HTTPException(404, detail="Snapshot not found")
    ts = time.strftime("%Y%m%d_%H%M%S")
    filename = f"Why_{ts}.pdf"
    path = os.path.join(EXPORT_DIR, filename)
    # simple PDF with header + bullets
    c = canvas.Canvas(path, pagesize=A4)
    W, H = A4
    c.setFillColorRGB(0, 0.32, 0.8)
    c.rect(0, H - 60, W, 60, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, H - 40, "IDECIDE — Why Narrative Export")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 11)
    y = H - 90
    c.drawString(20 * mm, y, f"Graph: {graph_id} • Snapshot: {to}")
    y -= 16
    c.drawString(
        20 * mm,
        y,
        f"Tenant: {request.state.tenant_id} • Workspace: {request.state.workspace_id}",
    )
    y -= 24
    c.drawString(20 * mm, y, "Evidence & Options:")
    y -= 14
    # list nodes succinctly
    for n in data["nodes"][:20]:
        c.drawString(26 * mm, y, f"- {n.get('type')}: {n.get('title')}")
        y -= 12
        if y < 60:
            c.showPage()
            y = H - 60
    c.showPage()
    c.save()
    return {"file": filename}


@router.post("/{graph_id}/audit/export")
def audit_export(graph_id: str, request: Request, frm: str, to: str):
    a = _read_snapshot_payload(
        graph_id, frm, request.state.tenant_id, request.state.workspace_id
    )
    b = _read_snapshot_payload(
        graph_id, to, request.state.tenant_id, request.state.workspace_id
    )
    if not a or not b:
        raise HTTPException(404, detail="Snapshots not found")
    # Diff
    a_nodes = {n["id"]: n for n in a["nodes"]}
    b_nodes = {n["id"]: n for n in b["nodes"]}
    a_edges = {e["id"]: e for e in a["edges"]}
    b_edges = {e["id"]: e for e in b["edges"]}
    diff = {
        "nodes_added": [b_nodes[i] for i in b_nodes.keys() - a_nodes.keys()],
        "nodes_removed": list(a_nodes.keys() - b_nodes.keys()),
        "edges_added": [b_edges[i] for i in b_edges.keys() - a_edges.keys()],
        "edges_removed": list(a_edges.keys() - b_edges.keys()),
    }
    manifest = {
        "graph_id": graph_id,
        "tenant_id": request.state.tenant_id,
        "workspace_id": request.state.workspace_id,
        "from": frm,
        "to": to,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hash_from": hashlib.sha256(json.dumps(a, sort_keys=True).encode()).hexdigest(),
        "hash_to": hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest(),
        "diff": diff,
    }
    ts = time.strftime("%Y%m%d_%H%M%S")
    zipname = f"audit_{graph_id}_{ts}.zip"
    zpath = os.path.join(EXPORT_DIR, zipname)
    import zipfile

    with zipfile.ZipFile(zpath, "w") as z:
        z.writestr("manifest.json", json.dumps(manifest, indent=2))
        z.writestr("from_snapshot.json", json.dumps(a, indent=2))
        z.writestr("to_snapshot.json", json.dumps(b, indent=2))
    return {"file": zipname}
