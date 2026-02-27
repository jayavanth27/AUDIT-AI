"""Entry point for the FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import auth, engagements, upload, summary

app = FastAPI(title="AI Audit Evidence Review Assistant")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(engagements.router, prefix="/engagements", tags=["engagements"])
app.include_router(upload.router, prefix="/engagements", tags=["documents"])
app.include_router(summary.router, prefix="/engagements", tags=["summaries"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
