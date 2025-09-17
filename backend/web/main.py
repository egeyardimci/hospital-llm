from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.common.paths import REACT_BUILD_PATH
from backend.common.constants import ALLOWED_CORS_ORIGINS
from backend.ai.vectordb.main import GLOBAL_VECTOR_DB
from backend.common.constants import *
from backend.web.routes import chat, vectordb, results, tests, system_prompts, qa_batches
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
app.include_router(qa_batches.router, prefix="/batches", tags=["batches"])
