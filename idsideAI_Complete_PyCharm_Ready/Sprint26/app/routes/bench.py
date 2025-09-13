from typing import Annotated
"""
Sprint 21.8 — Benchmark API (protocol v2)
- POST /api/bench/run { scenarios: [{name, delay_ms}] } -> runs simple synthetic benchmarks
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Body

from app.utils.bench import run_bench

router = APIRouter(prefix="/api/bench", tags=["bench"])


@router.post("/run")
def run(scenarios: Annotated[List[Dict[str, Any]], Body(..., embed=True)):
    return run_bench(scenarios)


@router.post("/compare")
def compare(payload: dict):
    scenarios = payload.get("scenarios", [])
    providers = payload.get("providers", [])
    from app.utils.bench import compare_providers

    return {"comparisons": compare_providers(scenarios, providers)}


@router.post("/compare/export")
def compare_export(results: list[dict]):
    from app.utils.bench import export_comparisons_csv

    return {"csv": export_comparisons_csv(results)}
