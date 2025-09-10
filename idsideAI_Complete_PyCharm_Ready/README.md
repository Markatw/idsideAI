# IDECIDE AI - PyCharm Ready

This is a clean, PyCharm-ready version of the IDECIDE AI application that runs seamlessly without manual database setup or bash commands.

## Quick Start

### Option 1: Automatic Setup (Recommended)
1. Open this folder in PyCharm
2. Run `python setup.py` - this will automatically:
   - Create the database
   - Set up default configuration
   - Initialize all required tables
3. Run `python run.py` to start the application
4. Open http://127.0.0.1:8000 in your browser

### Option 2: Direct Run
1. Open this folder in PyCharm
2. Run `python run.py` directly
3. The application will auto-create the database on first run
4. Open http://127.0.0.1:8000 in your browser

## PyCharm Configuration

### Setting up the Python Interpreter
1. Open PyCharm
2. Go to File → Settings → Project → Python Interpreter
3. Click the gear icon → Add
4. Choose "Virtualenv Environment" → New environment
5. Set the location to `./venv` in your project directory
6. Click OK

### Installing Dependencies
PyCharm will automatically detect the `requirements.txt` file and prompt you to install dependencies. Alternatively:
1. Open the terminal in PyCharm (View → Tool Windows → Terminal)
2. Run: `pip install -r requirements.txt`

### Running the Application
1. Right-click on `run.py` in the Project Explorer
2. Select "Run 'run'"
3. Or use the green play button in the top toolbar

## Configuration

The application uses a `.env` file for configuration. The setup script creates one automatically with default values:

```
DATABASE_URL=sqlite+aiosqlite:///./idsideai.db
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
AZURE_OPENAI_KEY=your_azure_key_here
ALLOW_FAKE_PROVIDER=true
```

### API Keys (Optional)
- The application works without API keys using a fake provider for testing
- To use real AI providers, update the `.env` file with your actual API keys
- Supported providers: OpenAI, Anthropic, Azure OpenAI

## Project Structure

```
idsideAI_PyCharm_Ready/
├── idsideai/                 # Main application package
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   └── ui/                  # Frontend templates and static files
├── examples/                # Example decision models
├── requirements.txt         # Python dependencies
├── run.py                  # Application entry point
├── setup.py                # Automatic setup script
└── README.md               # This file
```

## Features

- **Intent-to-Command Translation**: Natural language to structured AI commands
- **Multi-Provider Orchestration**: Automatically selects the best AI for each task
- **Decision Graphs**: Visual, auditable workflows
- **Web UI**: Clean, modern interface
- **API**: RESTful API for programmatic access

## Development

### Adding New Features
1. Models: Add to `idsideai/models.py`
2. API Endpoints: Add to `idsideai/routers/`
3. Business Logic: Add to `idsideai/services/`
4. Frontend: Modify `idsideai/ui/templates/` and `idsideai/ui/static/`

### Database Changes
If you modify the models, run:
```python
python -c "
import asyncio
from idsideai.database import engine, Base
async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
asyncio.run(recreate())
"
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `run.py` from 8000 to another port
2. **Database locked**: Delete `idsideai.db` and run `python setup.py` again
3. **Module not found**: Ensure you're running from the project root directory

### Getting Help
- Check the logs in the PyCharm console
- Ensure all dependencies are installed
- Verify the Python interpreter is set correctly

## Production Deployment

For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Setting up proper environment variables
- Using a production ASGI server like Gunicorn
- Implementing proper logging and monitoring

---

**IDECIDE AI** - The Intent-to-Command Orchestration Platform

