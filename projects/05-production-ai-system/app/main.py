import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import predict
from app.core.config import settings
from app.core.exceptions import AppException
from app.monitoring.logger import setup_logging

logger = setup_logging(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("Starting up... version=%s", settings.VERSION)
    # TODO: Initialize model manager, load AI models
    # model_manager = ModelManager()
    # await model_manager.load_models()
    # app.state.model_manager = model_manager
    yield
    logger.info("Shutting down...")
    # TODO: Cleanup resources
    # await model_manager.unload_models()


app = FastAPI(
    title="Production AI System",
    description="Production-grade AI inference service with monitoring and fallbacks",
    version=settings.VERSION,
    lifespan=lifespan,
)

# --- Middleware ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    """Add request timing headers."""
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID for tracing."""
    import uuid

    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# --- Exception handlers ---


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error("Application error: %s (code=%s)", exc.message, exc.error_code)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )


# --- Routes ---

app.include_router(predict.router, prefix="/api")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }
