import json
import os
import pathlib
import sqlite3
import time

_DB = os.environ.get("GRAPH_DB_PATH", "data/graphs.db")


def _conn():
    pathlib.Path(_DB).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(_DB)
    con.execute(
        "CREATE TABLE IF NOT EXISTS graphs (id TEXT PRIMARY KEY, graph_json TEXT NOT NULL, updated_at INTEGER NOT NULL)"
    )
    return con


def save_graph(gid: str, graph_model):
    js = json.dumps(graph_model.dict(), separators=(",", ":"))
    with _conn() as c:
        c.execute(
            "REPLACE INTO graphs(id,graph_json,updated_at) VALUES (?,?,?)",
            (gid, js, int(time.time())),
        )


def load_graph(gid: str):
    with _conn() as c:
        row = c.execute("SELECT graph_json FROM graphs WHERE id=?", (gid,)).fetchone()
        return json.loads(row[0]) if row else None


def list_graph_ids():
    with _conn() as c:
        return [r[0] for r in c.execute("SELECT id FROM graphs").fetchall()]


def delete_graph(gid: str):
    with _conn() as c:
        c.execute("DELETE FROM graphs WHERE id=?", (gid,))
