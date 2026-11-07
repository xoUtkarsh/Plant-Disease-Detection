"""
Unit tests for constants and agricultural knowledge base mappings.
"""

import pytest
from src.constants import CLASS_NAMES, NUM_CLASSES, parse_class_name
from src.inference.disease_catalog import get_disease_details, DISEASE_KNOWLEDGE_BASE


def test_class_names_count():
    assert len(CLASS_NAMES) == 38
    assert NUM_CLASSES == 38
    assert len(set(CLASS_NAMES)) == 38  # No duplicates


def test_parse_class_name():
    crop, condition, is_healthy = parse_class_name("Tomato___Late_blight")
    assert crop == "Tomato"
    assert condition == "Late blight"
    assert not is_healthy

    crop, condition, is_healthy = parse_class_name("Apple___healthy")
    assert crop == "Apple"
    assert condition == "healthy"
    assert is_healthy


def test_disease_knowledge_base_coverage():
    for name in CLASS_NAMES:
        details = get_disease_details(name)
        assert "crop" in details
        assert "condition" in details
        assert "severity" in details
        assert "symptoms" in details
        assert "organic_treatment" in details
        assert "chemical_treatment" in details
        assert "prevention" in details
        assert len(details["symptoms"]) > 0
        assert len(details["organic_treatment"]) > 0
