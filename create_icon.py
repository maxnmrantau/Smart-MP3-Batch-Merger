"""
create_icon.py
Generates a sleek, high-resolution app icon (PNG & ICO) with a gradient audio wave & music note.
"""

import os
from PIL import Image, ImageDraw

def create_app_icons():
    size = (256, 256)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded dark background rectangle
    # Gradient-like background
    draw.rounded_rectangle([(12, 12), (244, 244)], radius=54, fill=(14, 20, 32, 255), outline=(0, 242, 254, 180), width=6)

    # Draw neon cyan and purple glowing concentric audio arcs / wave lines
    draw.arc([(40, 40), (216, 216)], start=140, end=400, fill=(0, 242, 254, 255), width=8)
    draw.arc([(60, 60), (196, 196)], start=140, end=400, fill=(168, 85, 247, 255), width=7)

    # Draw modern musical note symbol in center
    # Note head 1 (left)
    draw.ellipse([(76, 150), (116, 186)], fill=(0, 242, 254, 255))
    # Note head 2 (right)
    draw.ellipse([(140, 134), (180, 170)], fill=(79, 172, 254, 255))

    # Note stems
    draw.rectangle([(108, 80), (116, 168)], fill=(0, 242, 254, 255))
    draw.rectangle([(172, 64), (180, 152)], fill=(79, 172, 254, 255))

    # Note top beam (slant)
    draw.polygon([(108, 80), (180, 64), (180, 80), (108, 96)], fill=(0, 242, 254, 255))

    # Save to multiple formats
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, "static")
    os.makedirs(static_dir, exist_ok=True)

    png_path = os.path.join(static_dir, "icon.png")
    ico_path = os.path.join(base_dir, "app_icon.ico")
    static_ico_path = os.path.join(static_dir, "favicon.ico")

    img.save(png_path, format="PNG")
    img.save(ico_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    img.save(static_ico_path, format="ICO", sizes=[(64, 64), (32, 32), (16, 16)])

    print("[OK] Icons created:")
    print(f"  - {png_path}")
    print(f"  - {ico_path}")
    print(f"  - {static_ico_path}")

if __name__ == "__main__":
    create_app_icons()
