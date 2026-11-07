"""
Dataset Ingestion and Verification Module.
Downloads and extracts the PlantVillage dataset from Kaggle or validates local copies.
"""

import os
import shutil
import zipfile
from pathlib import Path
from typing import Optional
from src.utils.logger import get_logger

logger = get_logger("data_download")


def setup_kaggle_credentials(kaggle_json_path: Optional[str] = None) -> bool:
    """
    Ensures kaggle.json is present in the standard user location (~/.kaggle/kaggle.json).
    """
    home = Path.home()
    target_kaggle_dir = home / ".kaggle"
    target_kaggle_file = target_kaggle_dir / "kaggle.json"

    if target_kaggle_file.exists():
        logger.info(f"Kaggle credentials already present at: {target_kaggle_file}")
        return True

    source_path = None
    if kaggle_json_path and os.path.exists(kaggle_json_path):
        source_path = Path(kaggle_json_path)
    elif os.path.exists("kaggle.json"):
        source_path = Path("kaggle.json")

    if source_path:
        target_kaggle_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, target_kaggle_file)
        try:
            os.chmod(target_kaggle_file, 0o600)
        except Exception:
            pass
        logger.info(f"Copied Kaggle credentials to: {target_kaggle_file}")
        return True

    logger.warning("No kaggle.json found. Direct Kaggle API download may not function.")
    return False


def download_dataset(
    dataset_name: str = "vipoooool/new-plant-diseases-dataset",
    output_dir: str = "data/raw",
    kaggle_json_path: Optional[str] = None
) -> Path:
    """
    Downloads and extracts the PlantVillage dataset using the Kaggle API.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Check if already extracted
    train_dir = out_path / "New Plant Diseases Dataset(Augmented)" / "train"
    alt_train_dir = out_path / "train"
    if train_dir.exists() or alt_train_dir.exists():
        logger.info(f"Dataset already appears to be present in {output_dir}")
        return out_path

    setup_kaggle_credentials(kaggle_json_path)

    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        logger.info(f"Downloading dataset '{dataset_name}' to '{output_dir}'...")
        api.dataset_download_files(dataset_name, path=str(out_path), unzip=True)
        logger.info("Dataset downloaded and extracted successfully.")
    except Exception as e:
        logger.error(f"Failed to automatically download dataset via Kaggle API: {e}")
        logger.info(
            "Manual step: Download 'vipoooool/new-plant-diseases-dataset' from Kaggle "
            f"and extract its contents into: {out_path.resolve()}"
        )

    return out_path


def verify_dataset(data_dir: str) -> bool:
    """
    Verifies that the dataset folder structure contains expected directories.
    """
    base = Path(data_dir)
    if not base.exists():
        logger.error(f"Directory {data_dir} does not exist.")
        return False

    subdirs = [d.name for d in base.iterdir() if d.is_dir()]
    logger.info(f"Found directories in {data_dir}: {subdirs}")
    return len(subdirs) > 0


if __name__ == "__main__":
    download_dataset()
