# image-shrink

A universal **AI coding agent skill** that compresses images before vision analysis, saving ~80% token costs with minimal quality loss.

Works with **Claude Code**, **Cursor**, **Codex (OpenAI)**, **Open Code**, and any AI agent that reads instructions from markdown files. More agents coming soon.

<!--
Keywords: AI coding agent skill, image compression for AI vision, reduce token cost, Claude Code skill, Cursor rule, Codex instruction, save API tokens, vision model optimization, compress images before AI analysis, AI agent plugin, LLM token savings
-->

## Why

Vision models charge by the pixel. A 4000×3000 screenshot and its 800px compressed version extract the same information, but the smaller one costs ~80% fewer tokens. This skill ensures every image is compressed before being sent to the model.

## Setup

Include `SKILL.md` and `scripts/` in your project, then add the skill content to your agent's instruction file. The exact file varies by agent (e.g. `CLAUDE.md` for Claude Code, `.cursor/rules/` for Cursor, `AGENTS.md` for Codex, etc.).

## Workflow

```
1. Compress all images
       python scripts/image-shrink.py <input> [output_dir] [max_size]

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

## License

MIT
