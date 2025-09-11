#!/usr/bin/env python3
"""
IDECIDE AI Setup Script
Automatically sets up the database and initializes the application.
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from idsideai.database import Base, engine


async def setup_database():
    """Create all database tables."""
    print("Setting up database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database setup complete!")


def create_env_file():
    """Create a .env file with default settings if it doesn't exist."""
    env_path = Path(".env")
    if not env_path.exists():
        print("Creating .env file with default settings...")
        with open(env_path, "w") as f:
            f.write(
                """# IDECIDE AI Configuration
DATABASE_URL=sqlite+aiosqlite:///./idsideai.db
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
AZURE_OPENAI_KEY=your_azure_key_here
ALLOW_FAKE_PROVIDER=true
"""
            )
        print(".env file created! Please update with your API keys if needed.")
    else:
        print(".env file already exists.")


def main():
    """Main setup function."""
    print("🚀 Setting up IDECIDE AI...")

    # Create .env file
    create_env_file()

    # Setup database
    asyncio.run(setup_database())

    print("✅ Setup complete!")
    print("\nTo run the application:")
    print("1. Update .env file with your API keys (optional)")
    print("2. Run: python run.py")
    print("3. Open http://127.0.0.1:8000 in your browser")


if __name__ == "__main__":
    main()
