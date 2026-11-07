"""
Prediction and inference API routes.
"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image
import io
from app.dependencies import get_predictor
from app.schemas import PredictResponse
from src.utils.logger import get_logger

logger = get_logger("api_predict")
router = APIRouter(prefix="/api/v1", tags=["Inference"])

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp"
}
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB


@router.post("/predict", response_model=PredictResponse)
def predict_disease(
    file: UploadFile = File(..., description="Leaf image file (JPEG, PNG, WebP)"),
    top_k: int = Form(3, description="Number of top candidate predictions to return"),
    predictor = Depends(get_predictor)
):
    """
    Analyzes an uploaded leaf image and returns:
    - Top predicted disease / condition
    - Probability confidence score
    - Top-K alternative predictions
    - Agricultural treatment advisory (organic & chemical)
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{file.content_type}'. Allowed types: {list(ALLOWED_CONTENT_TYPES)}"
        )

    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image size exceeds the maximum limit of {MAX_FILE_SIZE // (1024 * 1024)} MB."
        )

    try:
        # Validate image integrity
        image = Image.open(io.BytesIO(content))
        image.verify()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupt or invalid image file: {str(e)}"
        )

    if not predictor:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Predictor engine is not initialized."
        )

    try:
        result = predictor.predict(content, top_k=top_k)
        return result
    except Exception as e:
        logger.error(f"Inference error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing prediction: {str(e)}"
        )
