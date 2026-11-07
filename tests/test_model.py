"""
Unit tests for model architecture forward pass and tensor shapes.
"""

import pytest
import torch
from src.constants import NUM_CLASSES
from src.models.architecture import CustomLightweightCNN, build_model


def test_custom_lightweight_cnn_forward():
    model = CustomLightweightCNN(num_classes=NUM_CLASSES)
    model.eval()

    dummy_input = torch.randn(2, 3, 224, 224)
    with torch.no_grad():
        output = model(dummy_input)

    assert output.shape == (2, NUM_CLASSES)


def test_build_model_mobilenet_no_pretrained():
    model = build_model(backbone="mobilenet_v3_large", num_classes=NUM_CLASSES, pretrained=False)
    model.eval()

    dummy_input = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        output = model(dummy_input)

    assert output.shape == (1, NUM_CLASSES)
