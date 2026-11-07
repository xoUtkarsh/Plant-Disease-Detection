"""
Model Architecture Definitions.
Supports MobileNetV3-Large, ResNet50, EfficientNet-B0, and a Custom CNN.
"""

from typing import Optional
import torch
import torch.nn as nn
from torchvision import models
from src.constants import NUM_CLASSES
from src.utils.logger import get_logger

logger = get_logger("architecture")


class CustomLightweightCNN(nn.Module):
    """
    Lightweight standalone CNN architecture for leaf classification.
    Runs fast even on minimal CPU resources without external pretrained weights.
    """
    def __init__(self, num_classes: int = NUM_CLASSES, dropout_rate: float = 0.3):
        super().__init__()
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 4
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Dropout(p=dropout_rate),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_rate),
            nn.Linear(128, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.classifier(x)
        return x


def build_model(
    backbone: str = "mobilenet_v3_large",
    num_classes: int = NUM_CLASSES,
    pretrained: bool = True,
    dropout_rate: float = 0.3
) -> nn.Module:
    """
    Factory function to build model architectures.
    """
    backbone = backbone.lower()
    logger.info(f"Building model with backbone '{backbone}' (pretrained={pretrained}, classes={num_classes})")

    if backbone == "mobilenet_v3_large":
        weights = models.MobileNet_V3_Large_Weights.DEFAULT if pretrained else None
        model = models.mobilenet_v3_large(weights=weights)
        in_features = model.classifier[0].in_features
        model.classifier = nn.Sequential(
            nn.Linear(in_features, 1024),
            nn.Hardswish(inplace=True),
            nn.Dropout(p=dropout_rate, inplace=True),
            nn.Linear(1024, num_classes)
        )
        return model

    elif backbone == "resnet50":
        weights = models.ResNet50_Weights.DEFAULT if pretrained else None
        model = models.resnet50(weights=weights)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(p=dropout_rate),
            nn.Linear(in_features, num_classes)
        )
        return model

    elif backbone == "efficientnet_b0":
        weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        model = models.efficientnet_b0(weights=weights)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=dropout_rate, inplace=True),
            nn.Linear(in_features, num_classes)
        )
        return model

    elif backbone == "custom_cnn":
        return CustomLightweightCNN(num_classes=num_classes, dropout_rate=dropout_rate)

    else:
        raise ValueError(
            f"Unsupported backbone '{backbone}'. Supported: mobilenet_v3_large, resnet50, efficientnet_b0, custom_cnn"
        )
