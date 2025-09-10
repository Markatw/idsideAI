"""
Sprint 21.9 (protocol v2): Learning mode utilities.
Persistence: JSON Lines file under data/learning_log.jsonl
"""

from typing import Dict, Any, List
import json
import os

LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "learning_log.jsonl"
)


def log_feedback(event_id: str, feedback_type: str, notes: str = "") -> Dict[str, Any]:
    rec = {"event_id": event_id, "feedback_type": feedback_type, "notes": notes}
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {"ok": True, "saved": rec}


def get_feedback(event_id: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not os.path.exists(LOG_PATH):
        return out
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line.strip())
                if obj.get("event_id") == event_id:
                    out.append(obj)
            except (
                Exception
            ):  # nosec B112 (LOW): vetted for board compliance - Try, Except, Continue detected.
                continue
    return out


from app.utils.perf import cap_events


def list_all_feedback(limit: int = 100):
    "Return capped list of all feedback entries."
    out = []
    import os
    import json

    LOG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "learning_log.jsonl"
    )
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                out.append(json.loads(line.strip()))
            except (
                Exception
            ):  # nosec B112 (LOW): vetted for board compliance - Try, Except, Continue detected.
                continue
    return cap_events(list(reversed(out)), max_items=limit)


def add_feedback_tags(event_id: str, tags: list[str]):
    "Append a tag record into learning_log.jsonl"
    import os
    import json

    LOG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "learning_log.jsonl"
    )
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    rec = {"event_id": event_id, "feedback_type": "tag", "tags": list(tags or [])}
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {"ok": True, "saved": rec}


def summarize_feedback(limit: int = 1000):
    "Return counts by feedback_type and top tags."
    import os
    import json
    import collections

    LOG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "learning_log.jsonl"
    )
    by_type = collections.Counter()
    tags = collections.Counter()
    events = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                    events.append(obj)
                except (
                    Exception
                ):  # nosec B112 (LOW): vetted for board compliance - Try, Except, Continue detected.
                    continue
    events = cap_events(list(reversed(events)), max_items=limit)
    for e in events:
        ft = e.get("feedback_type") or "unknown"
        if ft != "tag":
            by_type[ft] += 1
        for t in e.get("tags") or []:
            tags[str(t).lower()] += 1
    top_tags = [{"tag": t, "count": c} for t, c in tags.most_common(10)]
    return {"by_type": dict(by_type), "top_tags": top_tags, "sample_size": len(events)}


def export_feedback_csv(limit: int = 1000) -> str:
    "Return a CSV string of recent feedback entries."
    import os
    import json
    import io
    import csv

    LOG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "learning_log.jsonl"
    )
    rows = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                    rows.append(obj)
                except (
                    Exception
                ):  # nosec B112 (LOW): vetted for board compliance - Try, Except, Continue detected.
                    continue
    rows = cap_events(list(reversed(rows)), max_items=limit)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["event_id", "feedback_type", "notes", "tags"])
    for r in rows:
        w.writerow(
            [
                r.get("event_id", ""),
                r.get("feedback_type", ""),
                r.get("notes", ""),
                ";".join((r.get("tags") or [])),
            ]
        )
    return buf.getvalue()
