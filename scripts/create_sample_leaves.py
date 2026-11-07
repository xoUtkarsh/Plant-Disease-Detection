"""
Generates synthetic leaf images with visual disease patterns
for immediate offline testing and UI demonstration.
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def generate_sample_leaf(kind: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 300, 300
    img = Image.new("RGB", (width, height), (245, 245, 240))
    draw = ImageDraw.Draw(img)

    # Base leaf contour
    leaf_color = (46, 125, 50) if kind != "rust" else (70, 110, 40)
    leaf_points = [
        (150, 30),
        (220, 100),
        (250, 180),
        (210, 250),
        (150, 270),
        (90, 250),
        (50, 180),
        (80, 100)
    ]
    draw.polygon(leaf_points, fill=leaf_color, outline=(27, 94, 32))

    # Central Vein
    draw.line([(150, 30), (150, 270)], fill=(76, 175, 80), width=3)
    # Side Veins
    for y in range(80, 240, 30):
        draw.line([(150, y), (200, y - 20)], fill=(76, 175, 80), width=2)
        draw.line([(150, y), (100, y - 20)], fill=(76, 175, 80), width=2)

    # Specific disease manifestations
    if kind == "early_blight":
        # Concentric brown rings (target board spots)
        for cx, cy in [(120, 130), (180, 160), (140, 200)]:
            for r in [22, 16, 10, 4]:
                color = (93, 64, 55) if r % 8 == 0 else (141, 110, 99)
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
            # Yellow chlorotic halo
            draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=(255, 235, 59), width=3)

    elif kind == "powdery_mildew":
        # White talc-like patches
        for cx, cy in [(130, 110), (170, 150), (120, 190), (190, 210)]:
            for _ in range(30):
                ox = cx + np.random.randint(-18, 18)
                oy = cy + np.random.randint(-18, 18)
                draw.point((ox, oy), fill=(240, 240, 240))

    elif kind == "rust":
        # Orange/brown rust pustules
        for cx, cy in [(120, 120), (170, 110), (130, 170), (175, 180), (150, 220)]:
            draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(230, 81, 0), outline=(191, 54, 12))

    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.save(str(output_path), quality=95)
    print(f"Created sample leaf: {output_path}")


def main():
    samples_dir = Path("data/sample_images")
    generate_sample_leaf("healthy", samples_dir / "sample_healthy_leaf.jpg")
    generate_sample_leaf("early_blight", samples_dir / "sample_early_blight.jpg")
    generate_sample_leaf("powdery_mildew", samples_dir / "sample_powdery_mildew.jpg")
    generate_sample_leaf("rust", samples_dir / "sample_rust_leaf.jpg")


if __name__ == "__main__":
    main()
