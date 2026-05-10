# image-shrink

Compress images before feeding them to AI vision models — reduce token consumption by ~80% with minimal quality loss.

Built as a **Claude Code skill** that automatically activates before any image analysis task.

## Why

Vision models charge by the pixel. A 4000×3000 screenshot costs ~80% more tokens than an 800px compressed version, yet the AI extracts the same information. This script shrinks images to an optimal size before analysis.

## Usage

```bash
# Single image (output goes to <input_dir>_small/)
python3 scripts/image-shrink.py screenshot.png

# Directory of images with custom output path
python3 scripts/image-shrink.py ./images ./output

# Preserve more detail (for text-heavy images)
python3 scripts/image-shrink.py screenshot.png ./output 1200
```

### As a Claude Code Skill

Add this repo as a dependency in your Claude Code project. The skill (defined in `SKILL.md`) will automatically compress images before any vision analysis.

**Mandatory workflow:**

1. Compress → 2. Analyze compressed → 3. If unclear, re-compress at larger size → 4. Clean up

## Sizing Guide

| Max Size | Use Case | Savings |
|----------|----------|---------|
| 600 | Rough layout, large text only | ~85% |
| **800** | **Default — UI screenshots, general use** | **~80%** |
| 1000 | Medium-detail images | ~75% |
| 1200 | Small text, detailed diagrams | ~65% |
| 1600 | Fine print, technical drawings | ~40% |

## What It Does

- Resizes images so longest edge ≤ MAX_SIZE (preserves aspect ratio)
- Converts all output to JPEG (handles RGBA/transparent backgrounds)
- Already-small JPEGs are copied as-is to avoid re-encoding
- Supports: PNG, JPEG, GIF, BMP, TIFF, WebP

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `IMAGE_SHRINK_MAX_SIZE` | 800 | Max pixels on longest edge |
| `IMAGE_SHRINK_QUALITY` | 85 | JPEG quality 1-100 |

## Requirements

- Python 3.6+
- Pillow (auto-installed on first run)

## License

MIT
