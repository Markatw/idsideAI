from typing import Annotated
"""
Sprint 21.9 — Learning API (protocol v2)
- POST /api/learning/feedback {event_id, feedback_type, notes} -> log feedback
- GET  /api/learning/{event_id} -> list feedback entries
"""

from fastapi import APIRouter, Body

from app.utils.learning import get_feedback, log_feedback

router = APIRouter(prefix="/api/learning", tags=["learning"])


@router.post("/feedback")
def feedback(
    event_id: Annotated[str, Body(..., embed=True),
    feedback_type: Annotated[str, Body(..., embed=True),
    notes: Annotated[str, Body(default="", embed=True),
):
    return log_feedback(event_id, feedback_type, notes)


@router.get("/{event_id}")
def list_feedback(event_id: str):
    return {"event_id": event_id, "feedback": get_feedback(event_id)}


@router.get("/all")
def all_feedback(limit: int = 100):
    from app.utils.learning import list_all_feedback

    return {"feedback": list_all_feedback(limit)}


@router.post("/tags")
def tag_update(event_id: str, tags: Annotated[list[str], Body(default=[])):
    from app.utils.learning import add_feedback_tags

    return add_feedback_tags(event_id, tags)


@router.get("/stats")
def stats(limit: int = 1000):
    from app.utils.learning import summarize_feedback

    return summarize_feedback(limit)


@router.post("/export")
def export_all(limit: Annotated[int, Body(1000, embed=True)):
    from app.utils.learning import export_feedback_csv

    return {"csv": export_feedback_csv(limit)}
