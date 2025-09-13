# IDSIDEAI FRONTEND HEADER BEGIN
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta, timezone
import os, logging

# Safe placeholders if not defined below
try:
    router  # type: ignore # noqa: F821
except NameError:
    router = APIRouter(prefix="", tags=["frontend"])
try:
    templates  # type: ignore # noqa: F821
except NameError:
    templates = Jinja2Templates(directory=os.getenv("TEMPLATES_DIR", "templates"))
# IDSIDEAI FRONTEND HEADER END

def _navbar(request: Request) -> str:
    return ""

def _footer(request: Request) -> str:
    return ""

