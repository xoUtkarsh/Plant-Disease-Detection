"""
Model Evaluation and Metrics Module.
Calculates Top-1 accuracy, Precision, Recall, F1-score, and Confusion Matrix.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any
import numpy as np
import torch
import yaml
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tqdm import tqdm

from src.constants import CLASS_NAMES, NUM_CLASSES
from src.data.dataset import build_data_loaders
from src.models.architecture import build_model
from src.utils.logger import get_logger

logger = get_logger("evaluation")


def evaluate_model(
    model: torch.nn.Module,
    data_loader: torch.utils.data.DataLoader,
    device: torch.device
) -> Dict[str, Any]:
    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for images, targets in tqdm(data_loader, desc="Evaluating"):
            images = images.to(device)
            outputs = model(images)
            preds = torch.argmax(outputs, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_targets.extend(targets.numpy())

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)

    acc = accuracy_score(all_targets, all_preds)
    report = classification_report(
        all_targets,
        all_preds,
        target_names=CLASS_NAMES[:len(set(all_targets).union(set(all_preds)))],
        output_dict=True,
        zero_division=0
    )
    cm = confusion_matrix(all_targets, all_preds).tolist()

    logger.info(f"Evaluation Accuracy: {acc * 100:.2f}%")
    return {
        "accuracy": float(acc),
        "classification_report": report,
        "confusion_matrix": cm
    }


def run_evaluation(
    model_path: str = "models/plant_disease_model.pth",
    config_path: str = "configs/train_config.yaml",
    output_metrics_path: str = "models/evaluation_metrics.json"
) -> None:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load Model
    model_cfg = config.get("model", {})
    model = build_model(
        backbone=model_cfg.get("backbone", "mobilenet_v3_large"),
        num_classes=NUM_CLASSES,
        pretrained=False
    )

    checkpoint = torch.load(model_path, map_location=device)
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)

    model.to(device)

    # Build Test Loader
    data_cfg = config.get("data", {})
    test_dir = data_cfg.get("processed_dir", "data/processed") + "/test"
    if not Path(test_dir).exists():
        test_dir = data_cfg.get("processed_dir", "data/processed") + "/val"

    _, test_loader, _ = build_data_loaders(
        train_dir=test_dir,
        batch_size=data_cfg.get("batch_size", 32),
        image_size=tuple(data_cfg.get("image_size", [224, 224])),
        num_workers=2
    )

    metrics = evaluate_model(model, test_loader, device)

    Path(output_metrics_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Saved evaluation metrics to {output_metrics_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Plant Disease Detection Model")
    parser.add_argument("--model", default="models/plant_disease_model.pth")
    parser.add_argument("--config", default="configs/train_config.yaml")
    args = parser.parse_args()
    run_evaluation(args.model, args.config)
