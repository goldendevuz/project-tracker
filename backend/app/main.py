from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .infrastructure.db import create_tables
from .presentation.routes import router

app = FastAPI(
    title="Project Timeline API",
    description="DDD-based project timeline tracker with admin panel",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Serve static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    await create_tables()


@app.get("/")
async def root():
    """Serve main page"""
    return FileResponse(os.path.join(frontend_path, "index.html"))


@app.get("/admin")
async def admin():
    """Serve admin panel"""
    return FileResponse(os.path.join(frontend_path, "admin.html"))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}
