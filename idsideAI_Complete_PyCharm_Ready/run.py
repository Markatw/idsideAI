#!/usr/bin/env python3
"""
IDECIDE AI Application Runner
Automatically sets up the database and starts the application.
"""

import asyncio
import os
import sys
import uvicorn
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def ensure_database():
    """Ensure database is set up before starting the application."""
    try:
        from idsideai.database import engine, Base
        from idsideai.models import DecisionModel, ExecutionLog
        
        # Create tables if they don't exist
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database ready!")
        
    except Exception as e:
        print(f"⚠️  Database setup warning: {e}")
        print("Continuing anyway - database will be created on first request.")

def create_env_if_missing():
    """Create .env file if it doesn't exist."""
    env_path = Path(".env")
    if not env_path.exists():
        print("📝 Creating .env file with default settings...")
        with open(env_path, "w") as f:
            f.write("""# IDECIDE AI Configuration
DATABASE_URL=sqlite+aiosqlite:///./idsideai.db
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
AZURE_OPENAI_KEY=your_azure_key_here
ALLOW_FAKE_PROVIDER=true
""")
        print("✅ .env file created!")

def main():
    """Main application runner."""
    print("🚀 Starting IDECIDE AI...")
    
    # Create .env file if missing
    create_env_if_missing()
    
    # Setup database
    asyncio.run(ensure_database())
    
    print("🌐 Starting web server...")
    print("📱 Open http://127.0.0.1:8000 in your browser")
    print("🛑 Press Ctrl+C to stop")
    
    # Start the application
    uvicorn.run(
        "idsideai.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
