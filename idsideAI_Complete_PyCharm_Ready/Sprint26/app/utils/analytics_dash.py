"""
Analytics dashboard utilities (Sprint 23.8, protocol v2)
"""
from app.utils.perf import cap_events
import collections

def summarize(events: list[dict], limit: int = 1000) -> dict:
    events = cap_events(events or [], max_items=limit)
    total = len(events)
    providers = collections.Counter([e.get("provider","") for e in events if e.get("provider")])
    feedback = collections.Counter([e.get("feedback_type","") for e in events if e.get("feedback_type")])
    return {
        "total": total,
        "unique_providers": len(providers),
        "providers": dict(providers.most_common(10)),
        "feedback_types": dict(feedback)
    }

def seed_dashboard(events: list[dict], limit: int = 1000) -> dict:
    events = cap_events(events or [], max_items=limit)
    providers = collections.Counter([e.get("provider","") for e in events if e.get("provider")])
    feedback = collections.Counter([e.get("feedback_type","") for e in events if e.get("feedback_type")])
    charts = {
        "bar_providers": [{"provider": p, "count": c} for p,c in providers.most_common(10)],
        "pie_feedback": [{"type": t, "count": c} for t,c in feedback.items()]
    }
    return {"charts": charts, "total_events": len(events)}
