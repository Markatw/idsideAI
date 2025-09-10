# PyCharm Setup Instructions for IDECIDE AI

## Quick Setup (Recommended)

1. **Open Project in PyCharm**
   - File → Open → Select the `idsideAI_PyCharm_Ready` folder
   - Click "Trust Project" when prompted

2. **Configure Python Interpreter**
   - PyCharm should automatically detect the `venv` folder
   - If not: File → Settings → Project → Python Interpreter
   - Click gear icon → Add → Existing Environment
   - Select `venv/bin/python` (or `venv/Scripts/python.exe` on Windows)

3. **Install Dependencies**
   - PyCharm will show a notification about requirements.txt
   - Click "Install requirements" in the notification
   - Or manually: Terminal → `pip install -r requirements.txt`

4. **Run the Application**
   - Right-click `run.py` → Run 'run'
   - Or click the green play button next to `if __name__ == "__main__":`
   - Application will start at http://127.0.0.1:8000

## Alternative Setup (If Virtual Environment Doesn't Exist)

1. **Create Virtual Environment**
   - Terminal in PyCharm: `python -m venv venv`
   - Or use PyCharm: File → Settings → Project → Python Interpreter → Add → New Environment

2. **Activate and Install**
   - Terminal: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
   - Install: `pip install -r requirements.txt`

3. **Run Setup**
   - `python setup.py` (optional - creates database and .env file)
   - `python run.py` (starts the application)

## PyCharm Run Configurations

### For run.py
- **Name**: IDECIDE AI Server
- **Script path**: `/path/to/idsideAI_PyCharm_Ready/run.py`
- **Python interpreter**: Project interpreter (venv)
- **Working directory**: `/path/to/idsideAI_PyCharm_Ready`

### For setup.py
- **Name**: IDECIDE AI Setup
- **Script path**: `/path/to/idsideAI_PyCharm_Ready/setup.py`
- **Python interpreter**: Project interpreter (venv)
- **Working directory**: `/path/to/idsideAI_PyCharm_Ready`

## Debugging

1. **Set Breakpoints**
   - Click in the left margin next to line numbers
   - Breakpoints work in all Python files

2. **Debug Mode**
   - Right-click `run.py` → Debug 'run'
   - Or use the debug button (bug icon) in the toolbar

3. **Environment Variables**
   - Edit `.env` file for configuration
   - Or set in Run Configuration → Environment Variables

## Common Issues

### "Module not found" errors
- Ensure virtual environment is activated
- Check Python interpreter is set to `venv/bin/python`
- Reinstall requirements: `pip install -r requirements.txt`

### Port already in use
- Change port in `run.py`: `port=8001` instead of `port=8000`
- Or kill existing process: `lsof -ti:8000 | xargs kill`

### Database issues
- Delete `idsideai.db` file
- Run `python setup.py` again

## Development Tips

### Code Navigation
- **Ctrl+Click** (Cmd+Click on Mac) to jump to definitions
- **Ctrl+B** to go to declaration
- **Ctrl+Shift+F** for global search

### Code Formatting
- **Ctrl+Alt+L** to format code
- Configure: Settings → Editor → Code Style → Python

### Version Control
- PyCharm has built-in Git support
- VCS → Enable Version Control Integration

### Database Inspection
- View → Tool Windows → Database
- Add SQLite datasource pointing to `idsideai.db`

## Project Structure in PyCharm

```
idsideAI_PyCharm_Ready/
├── venv/                    # Virtual environment (auto-created)
├── idsideai/               # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database setup
│   ├── models.py          # SQLAlchemy models
│   ├── routers/           # API endpoints
│   ├── services/          # Business logic
│   └── ui/               # Frontend templates/static files
├── examples/              # Example decision models
├── requirements.txt       # Python dependencies
├── run.py                # Application runner
├── setup.py              # Database setup script
├── .env                  # Environment variables (auto-created)
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
└── README.md            # Documentation
```

## Next Steps

1. **Explore the Code**
   - Start with `idsideai/main.py` to understand the FastAPI structure
   - Look at `idsideai/models.py` for data models
   - Check `idsideai/routers/` for API endpoints

2. **Test the API**
   - Visit http://127.0.0.1:8000/docs for interactive API documentation
   - Use the web interface at http://127.0.0.1:8000

3. **Add Features**
   - Create new routers in `idsideai/routers/`
   - Add business logic in `idsideai/services/`
   - Update models in `idsideai/models.py`

Happy coding! 🚀

