from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routes.graphs_export import router as graphs_router
from app.routes.providers import router as providers_router
from app.routes.workspaces import router as workspaces_router

def build_app() -> FastAPI:
    app = FastAPI(title="idsideAI", version="1.0-green")
    # Basic CORS (relaxed for dev; tighten in prod as needed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(graphs_router)
    app.include_router(providers_router)
    app.include_router(workspaces_router)
    return app

app = build_app()
