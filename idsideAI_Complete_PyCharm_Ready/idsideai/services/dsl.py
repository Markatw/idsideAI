from typing import Any, Dict, List, Literal, Optional

import yaml
from pydantic import BaseModel, Field


class Step(BaseModel):
    id: str
    type: Literal["prompt", "tool", "decision"]
    model: Optional[str] = None
    prompt: Optional[str] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    next: Optional[str] = None


class DecisionModelSpec(BaseModel):
    name: str
    description: str = ""
    steps: List[Step]


def parse_sdl(text: str) -> DecisionModelSpec:
    try:
        data = yaml.safe_load(text)
        return DecisionModelSpec(**data)
    except Exception as e:
        raise ValueError(f"SDL parse error: {e}")
