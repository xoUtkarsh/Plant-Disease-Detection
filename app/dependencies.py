"""
Dependency injection and predictor lifecycle manager.
Eliminates circular imports and ensures singleton predictor availability.
"""

from pathlib import Path
from typing import Optional
import yaml
from src.inference.predictor import PlantDiseasePredictor
from src.utils.logger import get_logger

logger = get_logger("dependencies")

_predictor_instance: Optional[PlantDiseasePredictor] = None


def get_predictor() -> PlantDiseasePredictor:
    """
    Returns the singleton PlantDiseasePredictor instance.
    Initializes lazily if not already present.
    """
    global _predictor_instance
    if _predictor_instance is None:
        logger.info("Initializing singleton predictor instance...")
        config_path = Path("configs/api_config.yaml")
        cfg = {}
        if config_path.exists():
            with open(config_path, "r") as f:
                cfg = yaml.safe_load(f)

        inf_cfg = cfg.get("inference", {})
        model_path = inf_cfg.get("model_path", "models/plant_disease_model.pth")
        onnx_path = inf_cfg.get("onnx_path", "models/plant_disease_model.onnx")
        device = inf_cfg.get("device", "cpu")

        _predictor_instance = PlantDiseasePredictor(
            model_path=model_path,
            onnx_path=onnx_path,
            device=device
        )
    return _predictor_instance


def set_predictor(predictor: PlantDiseasePredictor) -> None:
    """
    Overrides the predictor instance (useful for testing or custom configs).
    """
    global _predictor_instance
    _predictor_instance = predictor
