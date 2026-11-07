"""
Inference Predictor Engine.
Provides unified prediction inference using PyTorch or ONNX Runtime,
with image preprocessing, top-K probability extraction, and agricultural advisory enrichment.
"""

import io
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import numpy as np
from PIL import Image
import torch
from torchvision import transforms

from src.constants import (
    CLASS_NAMES,
    DEFAULT_IMAGE_SIZE,
    IMAGENET_MEAN,
    IMAGENET_STD,
    NUM_CLASSES,
)
from src.inference.disease_catalog import get_disease_details
from src.models.architecture import build_model
from src.utils.logger import get_logger

logger = get_logger("predictor")


class PlantDiseasePredictor:
    """
    High-performance predictor engine supporting PyTorch and ONNX runtimes.
    """

    def __init__(
        self,
        model_path: Optional[str] = "models/plant_disease_model.pth",
        onnx_path: Optional[str] = "models/plant_disease_model.onnx",
        prefer_onnx: bool = False,
        backbone: str = "mobilenet_v3_large",
        image_size: tuple = DEFAULT_IMAGE_SIZE,
        device: Optional[str] = None
    ):
        self.image_size = image_size
        self.backbone = backbone
        self.device = torch.device(
            device or ("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.model_type = "mock"
        self.torch_model = None
        self.onnx_session = None

        # Standard inference transform
        self.transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.CenterCrop(self.image_size[0]),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])

        # 1. Attempt loading ONNX if preferred or available
        if prefer_onnx and onnx_path and Path(onnx_path).exists():
            try:
                import onnxruntime as ort
                self.onnx_session = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
                self.model_type = "onnx"
                logger.info(f"Loaded ONNX model from {onnx_path}")
                return
            except Exception as e:
                logger.warning(f"Failed to load ONNX runtime model: {e}")

        # 2. Attempt loading PyTorch model
        if model_path and Path(model_path).exists():
            try:
                self.torch_model = build_model(
                    backbone=self.backbone,
                    num_classes=NUM_CLASSES,
                    pretrained=False
                )
                checkpoint = torch.load(model_path, map_location=self.device)
                if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                    self.torch_model.load_state_dict(checkpoint["model_state_dict"])
                else:
                    self.torch_model.load_state_dict(checkpoint)
                self.torch_model.to(self.device)
                self.torch_model.eval()
                self.model_type = "pytorch"
                logger.info(f"Loaded PyTorch model from {model_path} on {self.device}")
                return
            except Exception as e:
                logger.warning(f"Failed to load PyTorch weights: {e}")

        # 3. Fallback to initialized MobileNetV3 (offline, no external network download)
        try:
            logger.info("Initializing MobileNetV3 backbone as inference baseline...")
            self.torch_model = build_model(
                backbone=self.backbone,
                num_classes=NUM_CLASSES,
                pretrained=False
            ).to(self.device)
            self.torch_model.eval()
            self.model_type = "pytorch_baseline"
            logger.info("Initialized baseline PyTorch model.")
        except Exception as e:
            logger.warning(f"Using mock inference engine fallback: {e}")
            self.model_type = "mock"

    def preprocess_image(self, image_input: Union[str, Path, bytes, Image.Image]) -> torch.Tensor:
        """
        Converts diverse image inputs into a normalized PyTorch tensor [1, 3, H, W].
        """
        if isinstance(image_input, (str, Path)):
            image = Image.open(str(image_input)).convert("RGB")
        elif isinstance(image_input, bytes):
            image = Image.open(io.BytesIO(image_input)).convert("RGB")
        elif isinstance(image_input, Image.Image):
            image = image_input.convert("RGB")
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")

        tensor = self.transform(image).unsqueeze(0)  # [1, 3, H, W]
        return tensor

    def predict(
        self,
        image_input: Union[str, Path, bytes, Image.Image],
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Executes prediction on the input leaf image, returning enriched diagnostic information.
        """
        top_k = max(1, min(top_k, NUM_CLASSES))

        if self.model_type == "onnx" and self.onnx_session:
            tensor = self.preprocess_image(image_input).numpy()
            ort_inputs = {self.onnx_session.get_inputs()[0].name: tensor}
            ort_outs = self.onnx_session.run(None, ort_inputs)
            logits = ort_outs[0][0]
            # Softmax
            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / np.sum(exp_logits)
            top_indices = np.argsort(probs)[::-1][:top_k]
            top_probs = probs[top_indices]

        elif self.model_type.startswith("pytorch") and self.torch_model:
            tensor = self.preprocess_image(image_input).to(self.device)
            with torch.no_grad():
                logits = self.torch_model(tensor)
                probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
            top_indices = np.argsort(probs)[::-1][:top_k]
            top_probs = probs[top_indices]

        else:
            # Deterministic mock based on image properties
            if isinstance(image_input, bytes):
                img = Image.open(io.BytesIO(image_input)).convert("RGB")
            elif isinstance(image_input, Image.Image):
                img = image_input
            else:
                img = Image.open(str(image_input)).convert("RGB")

            # Simple hash-based class selection for deterministic mock
            img_hash = sum(img.getpixel((0, 0))) % NUM_CLASSES
            probs = np.full(NUM_CLASSES, 0.005)
            probs[img_hash] = 0.82
            probs[(img_hash + 1) % NUM_CLASSES] = 0.10
            probs[(img_hash + 2) % NUM_CLASSES] = 0.05
            top_indices = np.argsort(probs)[::-1][:top_k]
            top_probs = probs[top_indices]

        # Structure Top-K predictions
        predictions: List[Dict[str, Any]] = []
        for idx, prob in zip(top_indices, top_probs):
            class_name = CLASS_NAMES[idx]
            info = get_disease_details(class_name)
            predictions.append({
                "class_index": int(idx),
                "class_name": class_name,
                "crop": info["crop"],
                "condition": info["condition"],
                "is_healthy": info["is_healthy"],
                "confidence": float(round(float(prob), 4)),
                "confidence_percentage": f"{float(prob) * 100:.2f}%",
                "severity": info["severity"]
            })

        top_prediction = predictions[0]
        advisory_info = get_disease_details(top_prediction["class_name"])

        return {
            "model_type": self.model_type,
            "prediction": top_prediction,
            "top_predictions": predictions,
            "advisory": advisory_info,
            "status": "success"
        }
