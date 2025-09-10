from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./idsideai.db")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    azure_openai_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_key: str | None = os.getenv("AZURE_OPENAI_KEY")
    allow_fake_provider: bool = os.getenv("ALLOW_FAKE_PROVIDER", "true").lower() == "true"
settings = Settings()
