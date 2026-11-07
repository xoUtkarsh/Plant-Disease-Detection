"""
Plant Disease Detection Constants and Mappings.
Covers the 38 classes from the PlantVillage dataset across 14 crops.
"""

from typing import Dict, List, Tuple

# Exact 38 classes index-mapped
CLASS_NAMES: List[str] = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

CLASS_TO_INDEX: Dict[str, int] = {name: idx for idx, name in enumerate(CLASS_NAMES)}
INDEX_TO_CLASS: Dict[int, str] = {idx: name for idx, name in enumerate(CLASS_NAMES)}

NUM_CLASSES: int = len(CLASS_NAMES)  # 38

# Standard Normalization (ImageNet)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
DEFAULT_IMAGE_SIZE = (224, 224)


def parse_class_name(class_name: str) -> Tuple[str, str, bool]:
    """
    Parses a raw class name (e.g. 'Tomato___Early_blight') into human readable elements:
    Returns (crop_name, condition_name, is_healthy).
    """
    if "___" in class_name:
        crop_part, condition_part = class_name.split("___", 1)
    else:
        crop_part, condition_part = class_name, "Unknown"

    crop = crop_part.replace("_", " ").replace("(", "").replace(")", "").strip()
    condition = condition_part.replace("_", " ").strip()
    is_healthy = "healthy" in condition_part.lower()

    return crop, condition, is_healthy
