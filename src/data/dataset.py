"""
Dataset and DataLoader Module.
Handles image loading, augmentations, and PyTorch DataLoader creation.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
from src.constants import IMAGENET_MEAN, IMAGENET_STD, DEFAULT_IMAGE_SIZE
from src.utils.logger import get_logger

logger = get_logger("dataset")


def get_transforms(
    image_size: Tuple[int, int] = DEFAULT_IMAGE_SIZE,
    is_training: bool = True
) -> transforms.Compose:
    """
    Builds torchvision transforms for training or evaluation.
    """
    if is_training:
        return transforms.Compose([
            transforms.Resize(image_size),
            transforms.RandomResizedCrop(image_size[0], scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])
    else:
        return transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size[0]),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])


def build_data_loaders(
    train_dir: str,
    val_dir: Optional[str] = None,
    batch_size: int = 32,
    image_size: Tuple[int, int] = DEFAULT_IMAGE_SIZE,
    num_workers: int = 2
) -> Tuple[DataLoader, Optional[DataLoader], Dict[str, int]]:
    """
    Creates training and validation PyTorch DataLoaders using ImageFolder.
    """
    train_path = Path(train_dir)
    if not train_path.exists():
        raise FileNotFoundError(f"Train directory not found: {train_path}")

    train_transform = get_transforms(image_size=image_size, is_training=True)
    train_dataset = datasets.ImageFolder(root=str(train_path), transform=train_transform)
    class_to_idx = train_dataset.class_to_idx

    logger.info(f"Loaded {len(train_dataset)} training images across {len(class_to_idx)} classes.")

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )

    val_loader = None
    if val_dir and Path(val_dir).exists():
        val_transform = get_transforms(image_size=image_size, is_training=False)
        val_dataset = datasets.ImageFolder(root=str(val_dir), transform=val_transform)
        logger.info(f"Loaded {len(val_dataset)} validation images.")
        val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=torch.cuda.is_available()
        )

    return train_loader, val_loader, class_to_idx
