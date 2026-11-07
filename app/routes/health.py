"""
Health check and system telemetry routes.
"""

from fastapi import APIRouter, Depends
from src.constants import NUM_CLASSES
from app.dependencies import get_predictor
from app.schemas import HealthResponse

router = APIRouter(tags=["Health & System"])


@router.get("/health", response_model=HealthResponse)
def health_check(predictor = Depends(get_predictor)):
    """
    Returns the operational health status and inference engine state.
    """
    model_type = predictor.model_type if predictor else "uninitialized"
    device_name = str(predictor.device) if predictor else "unknown"

    return HealthResponse(
        status="healthy",
        model_type=model_type,
        total_classes=NUM_CLASSES,
        device=device_name,
        version="1.0.0"
    )


@router.get("/api/v1/info")
def system_info(predictor = Depends(get_predictor)):
    """
    Provides API and system capabilities metadata.
    """
    return {
        "service": "Plant Disease Detection API",
        "version": "1.0.0",
        "supported_crops": 14,
        "supported_conditions": NUM_CLASSES,
        "inference_engine": predictor.model_type if predictor else "uninitialized",
        "documentation": "/docs"
    }
