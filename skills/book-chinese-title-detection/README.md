# book-chinese-title-detection-skill

An agent skill that detects book titles from a cover image, returning the Chinese portion of any bilingual titles.

## What it does

Given a local image path, the skill:

1. Passes the image to `gpt-4o` via OpenAI's vision API.
2. Extracts all visible book titles.
3. For bilingual (English + Chinese) titles, returns only the Chinese part.
4. Returns Chinese-only or English-only titles as-is.
5. Strips punctuation marks (`!`, `！`, `?`, `？`) from all output.

## Trigger phrase

> "detect the Chinese titles of the books from this image"

## Skill workflow

1. **Ask for image path** — prompts the user for an absolute path to the book cover image.
2. **Run the script** — executes:
   ```bash
   python3 scripts/book-chinese-title-detection-agent.py "<image_path>"
   ```
3. **Return results** — prints one title per line to stdout.

## Setup

```bash
pip install langchain-openai langchain-core pillow pillow-heif
export OPENAI_API_KEY="sk-..."
```

## Supported image formats

JPEG, PNG, WebP, GIF, HEIC/HEIF

## File structure

```
book-chinese-title-detection-skill/
├── SKILL.md                                  # skill definition for Claude Code
├── scripts/
│   └── book-chinese-title-detection-agent.py # vision agent implementation
└── README.md                                 # this file
```

## Example output

```
深度学习
机器学习实战
Python编程
```
