"""
Disease Catalog and Agricultural Reference routes.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from src.constants import CLASS_NAMES, parse_class_name
from src.inference.disease_catalog import get_disease_details, DISEASE_KNOWLEDGE_BASE
from app.schemas import DiseaseListItem, DiseaseListResponse

router = APIRouter(prefix="/api/v1", tags=["Knowledge Base"])


@router.get("/diseases", response_model=DiseaseListResponse)
def list_diseases(
    crop: Optional[str] = Query(None, description="Filter diseases by crop name (e.g., Tomato, Apple)"),
    severity: Optional[str] = Query(None, description="Filter by severity (None, Low, Moderate, High, Critical)")
):
    """
    Returns the comprehensive catalog of all 38 supported plant diseases and healthy crop states.
    """
    crops_set = set()
    items: List[DiseaseListItem] = []

    for class_name in CLASS_NAMES:
        info = get_disease_details(class_name)
        crop_name = info["crop"]
        crops_set.add(crop_name)

        if crop and crop.lower() not in crop_name.lower():
            continue
        if severity and severity.lower() != info["severity"].lower():
            continue

        items.append(
            DiseaseListItem(
                class_name=class_name,
                crop=crop_name,
                condition=info["condition"],
                disease_name=info["disease_name"],
                scientific_name=info["scientific_name"],
                severity=info["severity"],
                is_healthy=info["is_healthy"]
            )
        )

    return DiseaseListResponse(
        total=len(items),
        crops=sorted(list(crops_set)),
        diseases=items
    )


@router.get("/diseases/{class_name}")
def get_disease(class_name: str):
    """
    Retrieves full symptoms, description, and treatment advisory for a specific disease class.
    """
    if class_name not in CLASS_NAMES and class_name not in DISEASE_KNOWLEDGE_BASE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class '{class_name}' not found in the agricultural knowledge base."
        )

    return get_disease_details(class_name)
