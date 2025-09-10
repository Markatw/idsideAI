from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class ApiCredential(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = None
    provider: str  # e.g., "openai","anthropic","gemini","mistral","groq","cohere"
    api_key: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DecisionModelShare(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    decision_model_id: int
    shared_with_email: str
    role: str = "viewer"  # viewer|editor|owner
    created_at: datetime = Field(default_factory=datetime.utcnow)