"""
Model Training Pipeline.
Executes training loops, metric logging, checkpointing, and early stopping.
"""

import argparse
import os
from pathlib import Path
from typing import Dict, Any
import torch
import torch.nn as nn
from torch.optim import AdamW, SGD
from torch.optim.lr_scheduler import CosineAnnealingLR
import yaml
from tqdm import tqdm

from src.constants import NUM_CLASSES
from src.data.dataset import build_data_loaders
from src.models.architecture import build_model
from src.utils.logger import get_logger

logger = get_logger("train_pipeline")


def train_one_epoch(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device
) -> Dict[str, float]:
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    pbar = tqdm(loader, desc="Training", leave=False)
    for images, labels in pbar:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)
        _, preds = torch.max(outputs, 1)
        correct += torch.sum(preds == labels).item()
        total += labels.size(0)

        pbar.set_postfix(loss=loss.item(), acc=(correct / total))

    epoch_loss = total_loss / max(1, total)
    epoch_acc = correct / max(1, total)
    return {"loss": epoch_loss, "accuracy": epoch_acc}


def validate(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    device: torch.device
) -> Dict[str, float]:
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in tqdm(loader, desc="Validation", leave=False):
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            total_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels).item()
            total += labels.size(0)

    val_loss = total_loss / max(1, total)
    val_acc = correct / max(1, total)
    return {"loss": val_loss, "accuracy": val_acc}


def run_training(config_path: str = "configs/train_config.yaml") -> None:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    # Build DataLoaders
    data_cfg = config.get("data", {})
    train_dir = data_cfg.get("processed_dir", "data/processed") + "/train"
    val_dir = data_cfg.get("processed_dir", "data/processed") + "/val"

    if not Path(train_dir).exists():
        logger.warning(f"Training dir {train_dir} does not exist. Checking raw dir...")
        train_dir = data_cfg.get("raw_dir", "data/raw")

    train_loader, val_loader, class_to_idx = build_data_loaders(
        train_dir=train_dir,
        val_dir=val_dir if Path(val_dir).exists() else None,
        batch_size=data_cfg.get("batch_size", 32),
        image_size=tuple(data_cfg.get("image_size", [224, 224])),
        num_workers=data_cfg.get("num_workers", 2)
    )

    # Build Model
    model_cfg = config.get("model", {})
    model = build_model(
        backbone=model_cfg.get("backbone", "mobilenet_v3_large"),
        num_classes=model_cfg.get("num_classes", NUM_CLASSES),
        pretrained=model_cfg.get("pretrained", True),
        dropout_rate=model_cfg.get("dropout_rate", 0.3)
    ).to(device)

    # Optimizer & Scheduler
    train_cfg = config.get("training", {})
    epochs = train_cfg.get("epochs", 20)
    lr = train_cfg.get("learning_rate", 0.0003)
    weight_decay = train_cfg.get("weight_decay", 0.0001)

    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs)

    # Output directory
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    best_weights_path = models_dir / "plant_disease_model.pth"

    best_val_loss = float("inf")
    patience = train_cfg.get("early_stopping", {}).get("patience", 5)
    patience_counter = 0

    logger.info(f"Starting training for {epochs} epochs...")
    for epoch in range(1, epochs + 1):
        train_metrics = train_one_epoch(model, train_loader, criterion, optimizer, device)
        scheduler.step()

        log_msg = f"Epoch {epoch:02d}/{epochs:02d} - Train Loss: {train_metrics['loss']:.4f} - Train Acc: {train_metrics['accuracy']:.4f}"

        if val_loader:
            val_metrics = validate(model, val_loader, criterion, device)
            log_msg += f" - Val Loss: {val_metrics['loss']:.4f} - Val Acc: {val_metrics['accuracy']:.4f}"

            if val_metrics["loss"] < best_val_loss:
                best_val_loss = val_metrics["loss"]
                patience_counter = 0
                torch.save({
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "class_to_idx": class_to_idx,
                    "val_loss": val_metrics["loss"],
                    "val_acc": val_metrics["accuracy"],
                    "backbone": model_cfg.get("backbone", "mobilenet_v3_large")
                }, best_weights_path)
                logger.info(f"-> Saved new best model checkpoint to {best_weights_path}")
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    logger.info(f"Early stopping triggered at epoch {epoch}")
                    break
        else:
            # If no validation set provided, save each epoch
            torch.save(model.state_dict(), best_weights_path)

        logger.info(log_msg)

    logger.info("Training pipeline finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Plant Disease Detection Model")
    parser.add_argument("--config", default="configs/train_config.yaml", help="Path to config file")
    args = parser.parse_args()
    run_training(args.config)
