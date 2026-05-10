# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code skill that compresses images before AI vision analysis to reduce token consumption. The skill definition lives in `SKILL.md` (frontmatter metadata + usage docs), and the implementation is a single script at `scripts/image-shrink.py`.

## Running

```bash
# Single image (output goes to <input_dir>_small/)
python3 scripts/image-shrink.py /path/to/image.png

# Directory of images, custom output dir, custom max size
python3 scripts/image-shrink.py /path/to/images /path/to/output 800
```

No build step, no test suite, no linting. Python 3.6+ with Pillow (auto-installed on first run).

## Architecture

Single-file design — everything is in `scripts/image-shrink.py`:

- `ensure_pillow()` — auto-installs Pillow if missing
- `process_image()` — handles one image: resize, RGBA→RGB conversion, JPEG output
- `main()` — CLI entry point, dispatches file vs directory input

Output is always JPEG. RGBA/P/LA modes get a white background composited. Images already smaller than `max_size` are copied (JPEG) or converted without resizing.

## Environment Variables

- `IMAGE_SHRINK_MAX_SIZE` — max pixels on longest edge (default 800)
- `IMAGE_SHRINK_QUALITY` — JPEG quality 1-100 (default 85)

## Skill Integration

`SKILL.md` frontmatter defines the trigger: this skill activates before any AI vision task. The mandatory workflow is compress → analyze compressed → fallback to original if details lost.
