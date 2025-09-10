from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.dsl import parse_sdl, DecisionModelSpec
from ..services.engine import run_model
router = APIRouter(prefix="/decision-models", tags=["decision-models"])
class RunRequest(BaseModel):
    sdl_text: str
    inputs: dict = {}
@router.post("/run")
async def run_decision_model(req: RunRequest):
    try:
        spec: DecisionModelSpec = parse_sdl(req.sdl_text)
    except Exception as e:
        raise HTTPException(400, f"SDL parse error: {e}")
    result = await run_model(spec, req.inputs)
    return result
