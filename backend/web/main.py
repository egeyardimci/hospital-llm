from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from backend.common.paths import REACT_BUILD_PATH
from backend.common.constants import ALLOWED_CORS_ORIGINS
from backend.ai.vectordb.main import GLOBAL_VECTOR_DB
from backend.common.constants import *
from backend.web.routes import chat, vectordb, results, tests, system_prompts, qa_batches, config, runs
from backend.web.routes import qa

app = FastAPI(title="Hospital LLM API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(vectordb.router, prefix="/vectordb", tags=["vectordb"])
app.include_router(results.router, prefix="/results", tags=["results"])
app.include_router(tests.router, prefix="/tests", tags=["tests"])
app.include_router(qa.router, prefix="/qa", tags=["qa"])
app.include_router(system_prompts.router, prefix="/system-prompts", tags=["system-prompts"])
app.include_router(qa_batches.router, prefix="/qa-batches", tags=["batches"])
app.include_router(config.router, prefix="/config", tags=["config"])
app.include_router(runs.router, prefix="/runs", tags=["runs"])

# Serve frontend static files
frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    # Mount static files (assets like JS, CSS)
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    # Serve index.html for root
    @app.get("/", response_class=FileResponse)
    async def serve_root():
        return FileResponse(str(frontend_dist / "index.html"))

    # Serve SPA - return index.html for unmatched routes (for client-side routing)
    @app.get("/{full_path:path}", response_class=FileResponse)
    async def serve_spa(full_path: str):
        # Check if it's an API route (should not serve index.html)
        if full_path.startswith(("chat/", "vectordb/", "results/", "tests/", "qa/", "qa-batches/", "system-prompts/", "config/", "runs/", "docs", "redoc", "openapi.json")):
            return None

        # If file exists in dist, serve it
        file_path = frontend_dist / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))

        # Otherwise serve index.html for SPA routing
        return FileResponse(str(frontend_dist / "index.html"))
