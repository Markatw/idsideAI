from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List, Optional

NodeType = Literal[
    "Decision", "Option", "Evidence", "Risk", "Constraint", "Outcome", "Metric", "Task"
]
EdgeType = Literal[
    "considers",
    "supported_by",
    "contradicted_by",
    "chosen",
    "constrained_by",
    "incurs",
    "leads_to",
    "measured_by",
    "depends_on",
]


class Node(BaseModel):
    id: str
    type: NodeType
    title: str
    x: Optional[int] = None
    y: Optional[int] = None
    w: Optional[int] = None
    h: Optional[int] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class Edge(BaseModel):
    id: str
    type: EdgeType
    source: str
    target: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class SubgraphResponse(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


class Snapshot(BaseModel):
    id: str
    at: str


class DiffChange(BaseModel):
    id: str
    field: Optional[str] = None
    from_value: Optional[str] = None
    to_value: Optional[str] = None


class DiffResponse(BaseModel):
    nodes_added: List[Node] = Field(default_factory=list)
    nodes_removed: List[str] = Field(default_factory=list)
    edges_added: List[Edge] = Field(default_factory=list)
    edges_removed: List[str] = Field(default_factory=list)
    props_changed: List[DiffChange] = Field(default_factory=list)
