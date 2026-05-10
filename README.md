# image-shrink

A **Claude Code skill** that compresses images before AI vision analysis, saving ~80% token consumption with minimal quality loss.

## Why

Vision models charge by the pixel. A 4000×3000 screenshot and its 800px compressed version extract the same information, but the smaller one costs ~80% fewer tokens. This skill ensures every image is compressed before being sent to the model.

## Install

Copy `SKILL.md` and `scripts/` into your Claude Code project. The skill will automatically activate before any vision analysis task.

## Workflow

```
1. Compress all images
       python3 scripts/image-shrink.py <input> [output_dir] [max_size]

2. Analyze compressed images with vision model

3. If details are unclear → re-compress at larger size (1200)

4. Clean up: rm -rf <output_dir>
```

## Token Savings

| Max Size | Use Case | Token Savings |
|----------|----------|---------------|
| 600 | Rough layout, large text | ~85% |
| **800** | **Default — UI screenshots** | **~80%** |
| 1200 | Small text, diagrams | ~65% |

## Requirements

- Python 3.6+
- Pillow (auto-installed on first run)
