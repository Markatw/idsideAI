from typing import Literal, Dict, Any
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import PlainTextResponse
from app.utils.graph_export import export_graphml, export_svg

router = APIRouter(prefix="/api/graphs", tags=["graphs"])

@router.post("/export", response_class=PlainTextResponse)
def export_graph(
    fmt: Literal["graphml", "svg", "png"] = Body(..., embed=True),
    graph: Dict[str, Any] = Body(..., embed=True)
) -> str:
    fmt = (fmt or "svg").lower()
    if fmt == "graphml":
        return export_graphml(graph)
    if fmt == "svg":
        return export_svg(graph)
    if fmt == "png":
        raise HTTPException(status_code=501, detail="PNG export not implemented. Use 'svg' or 'graphml'.")
    raise HTTPException(status_code=400, detail="Unsupported format. Use 'graphml' or 'svg'.")
