from typing import Any

from fastapi import APIRouter, HTTPException

from app.ai.model_manager import ModelManager
from app.ai.pipeline import AIPipeline
from app.core.config import settings
from app.core.exceptions import AppException
from app.monitoring.logger import setup_logging
from app.monitoring.metrics import MetricsCollector
from app.schemas.common import ErrorDetail, StandardResponse

logger = setup_logging(__name__)

router = APIRouter()

# --- Shared components (in production, use FastAPI Depends) ---

_model_manager = ModelManager()
_metrics = MetricsCollector()
_pipeline = AIPipeline(
    model_manager=_model_manager,
    metrics=_metrics,
)


@router.post("/predict", response_model=StandardResponse)
async def predict(input_data: dict[str, Any]):
    """Run inference on input data.

    Request body:
        {
            "text": "Your input text here",
            "model": "gpt-4"  // optional, defaults to configured model
        }

    Response:
        {
            "success": true,
            "data": {
                "prediction": {...},
                "model": "gpt-4",
                "latency_ms": 123.4
            }
        }
    """
    try:
        model_name = input_data.pop("model", None)
        result = await _pipeline.predict(input_data, model_name=model_name)
        return StandardResponse(success=True, data=result)
    except AppException as e:
        return StandardResponse(
            success=False,
            error=ErrorDetail(code=e.error_code, message=e.message, details=e.details),
        )
    except Exception as e:
        logger.exception(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/health")
async def health():
    """Health check with model status."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "models_loaded": _model_manager.list_models(),
    }


@router.get("/metrics")
async def metrics():
    """Return collected metrics."""
    return {
        "summary": _metrics.get_summary(),
        "by_model": _metrics.get_model_metrics(),
    }
