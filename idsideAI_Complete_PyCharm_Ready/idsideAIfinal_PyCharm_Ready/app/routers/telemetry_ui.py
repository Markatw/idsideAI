from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter(prefix="/telemetry", tags=["telemetry-ui"])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
async def telemetry_page(request: Request):
    return templates.TemplateResponse("telemetry.html", {"request": request})
