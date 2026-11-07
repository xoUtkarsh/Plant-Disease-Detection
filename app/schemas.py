"""
Pydantic Schemas for Request & Response Validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    model_type: str = Field(..., example="pytorch")
    total_classes: int = Field(..., example=38)
    device: str = Field(..., example="cpu")
    version: str = Field(..., example="1.0.0")


class PredictionItem(BaseModel):
    class_index: int
    class_name: str
    crop: str
    condition: str
    is_healthy: bool
    confidence: float
    confidence_percentage: str
    severity: str


class AdvisoryInfo(BaseModel):
    class_name: str
    crop: str
    condition: str
    is_healthy: bool
    disease_name: str
    scientific_name: str
    severity: str
    description: str
    symptoms: List[str]
    organic_treatment: List[str]
    chemical_treatment: List[str]
    prevention: List[str]


class PredictResponse(BaseModel):
    status: str
    model_type: str
    prediction: PredictionItem
    top_predictions: List[PredictionItem]
    advisory: AdvisoryInfo


class DiseaseListItem(BaseModel):
    class_name: str
    crop: str
    condition: str
    disease_name: str
    scientific_name: str
    severity: str
    is_healthy: bool


class DiseaseListResponse(BaseModel):
    total: int
    crops: List[str]
    diseases: List[DiseaseListItem]
