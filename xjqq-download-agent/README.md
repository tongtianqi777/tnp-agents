# xjqq-download-agent — Book Title Recognition Agent

A minimal LangChain agent that identifies book titles from a cover image using OpenAI's vision model (`gpt-4o`). Supports multiple books in a single image and extracts the Chinese portion of bilingual titles.

## How it works

1. Accepts a local absolute path to a book cover image as input.
2. Encodes the image as base64 and sends it to `gpt-4o` via the OpenAI vision API.
3. Detects **all visible book titles** in the image.
4. For each title: if it contains both an English part and a Chinese translation, returns **only the Chinese part**. Otherwise returns the title as-is.
5. Strips any exclamation marks (`!`, `！`) and question marks (`?`, `？`) from the output.

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."   # replace with your actual key
```

## Usage

### CLI

```bash
python book-chinese-title-detection-agent.py /absolute/path/to/book_cover.jpg
```

Output (stdout, one title per line):

```
深度学习
机器学习实战
```

### Programmatic

```python
from book_chinese_title_detection_agent import recognize_book_titles

titles = recognize_book_titles("/absolute/path/to/book_cover.jpg")
for title in titles:
    print(title)
```

## Prompts

| Role   | Content |
|--------|---------|
| System | *"You are a book title recognition assistant. When given an image that may contain one or more books, extract the title of every visible book. For each title: if it contains both an English part and a Chinese translation, output ONLY the Chinese part. If the title is Chinese-only, output it as-is. If the title is English-only (no Chinese translation present), output the English title as-is. Output one title per line with no numbering, explanations, or extra text."* |
| Human  | `[image]` + *"List the titles of all books visible in this image."* |

## Model

`gpt-4o` — OpenAI's multimodal model with vision support, best suited for OCR and text recognition in images across multiple languages.

## File structure

```
xjqq-download-agent/
├── book-chinese-title-detection-agent.py  # agent implementation
├── book-chinese-title-detection-skill.md  # skill description
├── requirements.txt  # Python dependencies
└── README.md         # this file
```
