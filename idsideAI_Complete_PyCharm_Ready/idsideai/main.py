from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .routers import decision_models, telemetry
app = FastAPI(title="idsideAI — Decision Layer")
templates = Jinja2Templates(directory="idsideai/ui/templates")
app.mount("/static", StaticFiles(directory="idsideai/ui/static"), name="static")
app.include_router(decision_models.router)
app.include_router(telemetry.router)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
