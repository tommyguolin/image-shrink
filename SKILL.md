---
name: image-shrink
description: >
  Compress images before AI vision analysis to reduce token consumption by ~80%.
  MUST be used before every image analysis task — do NOT feed original full-resolution
  images directly to vision models. Workflow: compress first → analyze compressed →
  if details are unclear, fall back to original. Triggers on: analyzing screenshots,
  photos, UI captures, documents, diagrams, or any image with AI vision. Requires
  Python 3.6+ (Pillow auto-installed).
---

# Image Shrink — Mandatory Image Compression for AI Vision

## ⚠️ Mandatory Workflow (follow EVERY time)

When analyzing images with AI vision, you MUST follow this exact sequence:

```
Step 1: Compress all images
    python3 scripts/image-shrink.py <input> <output_dir> [max_size]

Step 2: Analyze compressed images
    Use the compressed files in <output_dir> for vision analysis.

Step 3: Check result quality
    - If text is readable and details are clear → DONE ✅
    - If small text is blurry or details are missing → go to Step 4

Step 4: Fallback (only if Step 2 failed)
    Re-run with larger size:
    python3 scripts/image-shrink.py <input> <output_dir> 1200
    If still unclear, use original images directly.

Step 5: Clean up
    rm -rf <output_dir>
```

## Quick Start

```bash
# Compress a single image
python3 scripts/image-shrink.py /tmp/screenshot.png

# Compress all images in a directory
python3 scripts/image-shrink.py /tmp/images /tmp/images_small

# Preserve more detail (for text-heavy images)
python3 scripts/image-shrink.py /tmp/images /tmp/images_small 1200
```

## Sizing Guide

| Max Size | Use Case | Savings |
|----------|----------|---------|
| 600 | Rough layout, large text only | ~85% |
| **800** | **Default — UI screenshots, general use** | **~80%** |
| 1000 | Medium-detail images | ~75% |
| 1200 | Small text, detailed diagrams | ~65% |
| 1600 | Fine print, technical drawings | ~40% |

## What It Does

- Resizes images so longest edge ≤ MAX_SIZE (keeps aspect ratio)
- Converts all output to JPEG (handles RGBA/transparent backgrounds)
- Small images already at target size: JPEG copied as-is, others converted
- Supports: PNG, JPEG, GIF, BMP, TIFF, WebP

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `IMAGE_SHRINK_MAX_SIZE` | 800 | Max pixels on longest edge |
| `IMAGE_SHRINK_QUALITY` | 85 | JPEG quality 1-100 |

## Requirements

- Python 3.6+ (pre-installed on nearly all systems)
- Pillow (auto-installed on first run)
