#!/usr/bin/env python3
"""
image-shrink.py - Compress images to reduce AI vision model token consumption.

Usage:
    python3 image-shrink.py <input_dir_or_file> [output_dir] [max_size]

Examples:
    python3 image-shrink.py /tmp/screenshot.png
    python3 image-shrink.py /tmp/images /tmp/out 800
    python3 image-shrink.py /tmp/images /tmp/out 1200

Environment variables:
    IMAGE_SHRINK_MAX_SIZE    Max pixels on longest edge (default: 800)
    IMAGE_SHRINK_QUALITY     JPEG quality 1-100 (default: 85)
"""

import os
import sys
import shutil

def ensure_pillow():
    """Auto-install Pillow if missing."""
    try:
        from PIL import Image
        return Image
    except ImportError:
        print("[INFO] Installing Pillow (image processing library)...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
        from PIL import Image
        print("[INFO] Pillow installed successfully.")
        return Image

def process_image(Image, src, output_dir, max_size, quality):
    """Process a single image file. Returns (status, message)."""
    filename = os.path.basename(src)
    name = os.path.splitext(filename)[0]
    dest = os.path.join(output_dir, f"{name}.jpg")

    try:
        img = Image.open(src)
    except Exception:
        return "error", f"[错误] 无法读取: {filename}"

    width, height = img.size
    max_edge = max(width, height)

    # Convert RGBA/P to RGB for JPEG saving
    if img.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        if img.mode == "LA":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")

    if max_edge <= max_size:
        lower_ext = os.path.splitext(filename)[1].lower()
        if lower_ext in (".jpg", ".jpeg"):
            # Already small JPEG — copy directly to avoid re-encoding
            shutil.copy2(src, dest)
            return "skip", f"[跳过] {filename} ({width}x{height}) 已是小尺寸JPEG，直接复制"
        else:
            img.save(dest, "JPEG", quality=quality)
            return "convert", f"[转换] {filename} ({width}x{height}) → {name}.jpg (尺寸不变)"
    else:
        # Resize proportionally so longest edge = max_size
        ratio = max_size / max_edge
        new_w = int(width * ratio)
        new_h = int(height * ratio)
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        img_resized.save(dest, "JPEG", quality=quality)

        orig_size = os.path.getsize(src)
        new_size = os.path.getsize(dest)
        pct = 100 - (new_size * 100 // orig_size)
        return "shrink", f"[缩小] {filename} ({width}x{height} → {new_w}x{new_h}) 体积减少{pct}%"


SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".webp"}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ""
    max_size = int(sys.argv[3]) if len(sys.argv) > 3 else int(os.environ.get("IMAGE_SHRINK_MAX_SIZE", "800"))
    quality = int(os.environ.get("IMAGE_SHRINK_QUALITY", "85"))

    # Determine input files
    if os.path.isfile(input_path):
        input_dir = os.path.dirname(input_path)
        files = [input_path]
    elif os.path.isdir(input_path):
        input_dir = input_path
        files = [
            os.path.join(input_dir, f)
            for f in sorted(os.listdir(input_dir))
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS
        ]
    else:
        print(f"[ERROR] 路径不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    if not output_dir:
        output_dir = input_dir + "_small"

    os.makedirs(output_dir, exist_ok=True)

    Image = ensure_pillow()

    total = len(files)
    success = 0
    skipped = 0
    errors = 0

    for src in files:
        status, msg = process_image(Image, src, output_dir, max_size, quality)
        print(msg)
        if status == "error":
            errors += 1
        elif status == "skip":
            skipped += 1
        else:
            success += 1

    print()
    print("===============================")
    parts = [f"成功 {success}/{total}"]
    if skipped:
        parts.append(f"跳过 {skipped}")
    if errors:
        parts.append(f"错误 {errors}")
    print(f"处理完成: {', '.join(parts)}")
    print(f"输出目录: {output_dir}")
    print("===============================")


if __name__ == "__main__":
    main()
