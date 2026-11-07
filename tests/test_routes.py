"""
Unit tests for API route handlers and schemas.
"""

import io
import pytest
from fastapi import HTTPException
from PIL import Image
from starlette.datastructures import UploadFile
from app.routes.health import health_check, system_info
from app.routes.catalog import list_diseases, get_disease
from app.routes.predict import predict_disease
from app.dependencies import get_predictor


def test_health_check_handler():
    predictor = get_predictor()
    res = health_check(predictor=predictor)
    assert res.status == "healthy"
    assert res.total_classes == 38
    assert res.model_type == "pytorch"


def test_system_info_handler():
    predictor = get_predictor()
    res = system_info(predictor=predictor)
    assert res["service"] == "Plant Disease Detection API"
    assert res["supported_crops"] == 14
    assert res["supported_conditions"] == 38


def test_list_diseases_catalog():
    res = list_diseases(crop=None, severity=None)
    assert res.total == 38
    assert len(res.crops) == 14

    # Filter by crop
    res_apple = list_diseases(crop="Apple", severity=None)
    assert res_apple.total == 4
    for d in res_apple.diseases:
        assert d.crop == "Apple"


def test_get_disease_details():
    d = get_disease("Tomato___Early_blight")
    assert d["disease_name"] == "Tomato Early Blight"
    assert d["scientific_name"] == "Alternaria solani"
    assert d["crop"] == "Tomato"
    assert "symptoms" in d
    assert "organic_treatment" in d
    assert "chemical_treatment" in d


def test_predict_disease_handler_success():
    predictor = get_predictor()
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    upload_file = UploadFile(filename="test.jpg", file=buf, headers={"content-type": "image/jpeg"})
    res = predict_disease(file=upload_file, top_k=3, predictor=predictor)

    assert res["status"] == "success"
    assert "prediction" in res
    assert "advisory" in res
    assert len(res["top_predictions"]) == 3
    assert res["prediction"]["confidence"] > 0


def test_predict_disease_invalid_content_type():
    predictor = get_predictor()
    buf = io.BytesIO(b"dummy text")
    upload_file = UploadFile(filename="test.txt", file=buf, headers={"content-type": "text/plain"})
    
    with pytest.raises(HTTPException) as excinfo:
        predict_disease(file=upload_file, top_k=3, predictor=predictor)
    assert excinfo.value.status_code == 415


def test_predict_disease_corrupt_image():
    predictor = get_predictor()
    buf = io.BytesIO(b"not a valid image")
    upload_file = UploadFile(filename="corrupt.jpg", file=buf, headers={"content-type": "image/jpeg"})
    
    with pytest.raises(HTTPException) as excinfo:
        predict_disease(file=upload_file, top_k=3, predictor=predictor)
    assert excinfo.value.status_code == 400
