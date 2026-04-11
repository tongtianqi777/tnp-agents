# xjqq-download-agent — Book Title Recognition Agent

A minimal LangChain agent that identifies a book's title from a cover image using OpenAI's vision model (`gpt-4o`).

## How it works

1. Accepts a local absolute path to a book cover image as input.
2. Encodes the image as base64 and sends it to `gpt-4o` via the OpenAI vision API.
3. Returns **only** the recognized book title (Chinese, English, or both).

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."   # replace with your actual key
```

## Usage

### CLI

```bash
python book-title-detection-agent.py /absolute/path/to/book_cover.jpg
```

Output (stdout):

```
深度学习
```

### Programmatic

```python
from book-title-detection-agent import recognize_book_title

title = recognize_book_title("/absolute/path/to/book_cover.jpg")
print(title)   # e.g. "Deep Learning"
```

## Prompts

| Role   | Content |
|--------|---------|
| System | *"You are a book title recognition assistant. When given an image of a book, extract and return ONLY the book title. The title may be in Chinese, English, or both. Do not include any explanation, punctuation, or additional text — output the title and nothing else."* |
| Human  | `[image]` + *"What is the title of this book?"* |

## Model

`gpt-4o` — OpenAI's multimodal model with vision support, best suited for OCR and text recognition in images across multiple languages.

## File structure

```
xjqq-download-agent/
├── book-title-detection-agent.py  # agent implementation
├── requirements.txt  # Python dependencies
└── README.md         # this file
```
