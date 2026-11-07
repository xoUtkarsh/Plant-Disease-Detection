"""
Model Serialization and ONNX Export Module.
Converts PyTorch checkpoints into optimized ONNX graphs for low-latency web inference.
"""

import argparse
from pathlib import Path
import numpy as np
import torch
from src.constants import NUM_CLASSES
from src.models.architecture import build_model
from src.utils.logger import get_logger

logger = get_logger("model_export")


def export_to_onnx(
    model_path: str = "models/plant_disease_model.pth",
    output_onnx_path: str = "models/plant_disease_model.onnx",
    backbone: str = "mobilenet_v3_large",
    opset_version: int = 17,
    image_size: int = 224
) -> Path:
    """
    Exports a trained PyTorch model to ONNX.
    """
    out_file = Path(output_onnx_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Initialize model
    model = build_model(backbone=backbone, num_classes=NUM_CLASSES, pretrained=False)

    if Path(model_path).exists():
        checkpoint = torch.load(model_path, map_location="cpu")
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            model.load_state_dict(checkpoint["model_state_dict"])
            logger.info("Loaded state_dict from training checkpoint.")
        else:
            model.load_state_dict(checkpoint)
            logger.info("Loaded state_dict from raw weights.")
    else:
        logger.warning(f"Weights file {model_path} not found. Exporting base architecture for deployment scaffolding.")

    model.eval()

    dummy_input = torch.randn(1, 3, image_size, image_size, requires_grad=False)

    logger.info(f"Exporting to ONNX format at {output_onnx_path} (opset {opset_version})...")
    torch.onnx.export(
        model,
        dummy_input,
        str(out_file),
        export_params=True,
        opset_version=opset_version,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "output": {0: "batch_size"}
        }
    )

    logger.info("Verifying exported ONNX model...")
    try:
        import onnx
        onnx_model = onnx.load(str(out_file))
        onnx.checker.check_model(onnx_model)
        logger.info("ONNX model validated successfully!")
    except Exception as e:
        logger.warning(f"Could not verify ONNX model with onnx package: {e}")

    return out_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export PyTorch model to ONNX")
    parser.add_argument("--model", default="models/plant_disease_model.pth")
    parser.add_argument("--output", default="models/plant_disease_model.onnx")
    parser.add_argument("--backbone", default="mobilenet_v3_large")
    args = parser.parse_args()
    export_to_onnx(args.model, args.output, args.backbone)
