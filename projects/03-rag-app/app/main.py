from fastapi import FastAPI

from app.api.routes import rag
from app.core.config import settings

app = FastAPI(
    title="RAG Application",
    description="Retrieval-Augmented Generation API",
    version="0.1.0",
)

app.include_router(rag.router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}
