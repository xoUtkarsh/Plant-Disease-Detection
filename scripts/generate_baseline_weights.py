"""
Generates initialized baseline weights for PyTorch and ONNX
so the system is immediately fully operational out-of-the-box offline.
"""

from pathlib import Path
import torch
from src.constants import NUM_CLASSES
from src.models.architecture import build_model
from src.models.export import export_to_onnx


def main():
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    pth_path = models_dir / "plant_disease_model.pth"
    onnx_path = models_dir / "plant_disease_model.onnx"

    print("Building MobileNetV3-Large baseline model...")
    model = build_model(
        backbone="mobilenet_v3_large",
        num_classes=NUM_CLASSES,
        pretrained=False
    )
    model.eval()

    print(f"Saving checkpoint to {pth_path}...")
    torch.save({
        "epoch": 0,
        "model_state_dict": model.state_dict(),
        "num_classes": NUM_CLASSES,
        "backbone": "mobilenet_v3_large"
    }, str(pth_path))

    print(f"Exporting to ONNX at {onnx_path}...")
    export_to_onnx(
        model_path=str(pth_path),
        output_onnx_path=str(onnx_path),
        backbone="mobilenet_v3_large"
    )
    print("Baseline models generated successfully.")


if __name__ == "__main__":
    main()
