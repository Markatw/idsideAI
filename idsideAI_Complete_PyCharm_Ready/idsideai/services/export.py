import csv
import json
from typing import List, Dict, Any
from pathlib import Path


def export_json(path: str, payload: Dict[str, Any]):
    Path(path).write_text(json.dumps(payload, indent=2))


def export_csv(path: str, rows: List[Dict[str, Any]]):
    if not rows:
        Path(path).write_text("")
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
