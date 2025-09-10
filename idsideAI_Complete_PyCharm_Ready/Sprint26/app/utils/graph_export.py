from typing import Dict, Any, List
import math
import html as html_mod

def _coerce_graph(graph: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(graph, dict):
        return {"nodes": [], "edges": []}
    return {
        "nodes": list(graph.get("nodes", []) or []),
        "edges": list(graph.get("edges", []) or []),
    }

def export_graphml(graph: Dict[str, Any]) -> str:
    g = _coerce_graph(graph)
    out: List[str] = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"')
    out.append('         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    out.append('         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">')
    out.append('  <graph id="G" edgedefault="directed">')
    for n in g.get("nodes", []):
        out.append(f'    <node id="{html_mod.escape(str(n.get("id")))}"/>')
    for i, e in enumerate(g.get("edges", [])):
        s = html_mod.escape(str(e.get("source")))
        t = html_mod.escape(str(e.get("target")))
        out.append(f'    <edge id="e{i}" source="{s}" target="{t}"/>')
    out.append('  </graph>')
    out.append('</graphml>')
    return "\n".join(out)

def export_svg(graph: Dict[str, Any], width: int = 640, height: int = 480) -> str:
    g = _coerce_graph(graph)
    nodes = g.get("nodes", [])
    edges = g.get("edges", [])
    N = max(1, len(nodes))
    R = min(width, height) // 3
    cx, cy = width // 2, height // 2
    coords = []
    for i in range(N):
        angle = (2*math.pi*i)/N
        x = int(cx + R*math.cos(angle))
        y = int(cy + R*math.sin(angle))
        coords.append((x,y))
    pos = {}
    for i, node in enumerate(nodes):
        nid = str(node.get("id"))
        pos[nid] = coords[i]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    out.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')
    for e in edges:
        s = pos.get(str(e.get("source")))
        t = pos.get(str(e.get("target")))
        if s and t:
            out.append(f'<line x1="{s[0]}" y1="{s[1]}" x2="{t[0]}" y2="{t[1]}" stroke="black" stroke-width="1"/>')
    for nid, (x,y) in pos.items():
        out.append(f'<circle cx="{x}" cy="{y}" r="12" fill="lightgray" stroke="black" stroke-width="1"/>')
        out.append(f'<text x="{x}" y="{y+4}" font-size="10" text-anchor="middle" fill="black">{html_mod.escape(nid)}</text>')
    out.append('</svg>')
    return "\n".join(out)
