# image-shrink

A universal **AI coding agent skill** that compresses images before vision analysis, saving ~80% token costs with minimal quality loss.

Works with **Claude Code**, **Cursor**, **Codex (OpenAI)**, **Open Code**, **Windsurf**, **Cline**, and any AI agent that reads instructions from markdown files.

<!-- 
Keywords: AI coding agent skill, image compression for AI vision, reduce token cost, Claude Code skill, Cursor rule, Codex instruction, save API tokens, vision model optimization, compress images before AI analysis, AI agent plugin, LLM token savings
-->

## Why

Vision models charge by the pixel. A 4000×3000 screenshot and its 800px compressed version extract the same information, but the smaller one costs ~80% fewer tokens. This skill ensures every image is compressed before being sent to the model.

## Setup

### Claude Code

Copy `SKILL.md` and `scripts/` into your project root.

### Cursor

Copy the content of `SKILL.md` into `.cursor/rules/image-shrink.mdc`.

### Codex / Open Code / Other Agents

Copy `SKILL.md` content into your agent's instruction file (e.g. `AGENTS.md`, `instructions.md`).

### Manual (Any Agent)

Add this to your agent instructions:

```markdown
Before analyzing any image with vision, run:
  python3 scripts/image-shrink.py <image_path>
Then analyze the compressed output. If details are unclear, re-run with size 1200.
```

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

## License

MIT
