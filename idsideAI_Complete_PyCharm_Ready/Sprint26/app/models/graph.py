from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class NodeModel(BaseModel):
    id: str
    label: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None


class EdgeModel(BaseModel):
    source: str
    target: str
    label: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    directed: bool = True


class GraphModel(BaseModel):
    nodes: List[NodeModel] = Field(default_factory=list)
    edges: List[EdgeModel] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None


__all__ = ["NodeModel", "EdgeModel", "GraphModel"]
