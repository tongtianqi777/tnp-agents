"""
Book Title Recognition Agent

A LangChain agent that takes a local image path as input,
uses OpenAI's vision model to recognize the book title,
and returns the title text only.
"""

import base64
import io
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = (
    "You are a book title recognition assistant. "
    "When given an image of a book, extract and return ONLY the book title. "
    "The title may be in Chinese, English, or both. "
    "Do not include any explanation, punctuation, or additional text — "
    "output the title and nothing else."
)

# OpenAI vision tiles images into 512×512 chunks for cost calculation.
# 1024px on the longest side is sufficient to read any book title while
# keeping the tile count (and therefore token cost) minimal.
MAX_LONG_SIDE = 1024


def _load_and_resize(image_path: Path) -> str:
    """
    Open an image (including HEIC), scale it down so the longest side is at
    most MAX_LONG_SIDE, and return a base64-encoded JPEG string.
    """
    from PIL import Image as PILImage

    suffix = image_path.suffix.lower().lstrip(".")
    if suffix in ("heic", "heif"):
        try:
            from pillow_heif import register_heif_opener
        except ImportError as e:
            raise ImportError(
                "pillow-heif is required for HEIC images: pip install pillow-heif"
            ) from e
        register_heif_opener()

    img = PILImage.open(image_path)

    # Convert to RGB so JPEG encoding always works (HEIC/PNG may have alpha).
    img = img.convert("RGB")

    # Scale down only if needed; never upscale.
    w, h = img.size
    long_side = max(w, h)
    if long_side > MAX_LONG_SIDE:
        scale = MAX_LONG_SIDE / long_side
        img = img.resize((int(w * scale), int(h * scale)), PILImage.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def recognize_book_title(image_path: str) -> str:
    """
    Recognize the title of a book from a local image.

    Args:
        image_path: Absolute path to the book cover image
                    (JPEG, PNG, WebP, GIF, HEIC/HEIF supported).

    Returns:
        The recognized book title as a plain string.
    """
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image_data = _load_and_resize(path)

    llm = ChatOpenAI(
        model="gpt-4o",
        max_tokens=256,
        # api_key is read from the OPENAI_API_KEY environment variable by default
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}",
                        "detail": "high",
                    },
                },
                {
                    "type": "text",
                    "text": "What is the title of this book?",
                },
            ]
        ),
    ]

    response = llm.invoke(messages)
    return response.content.strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python agent.py <absolute_path_to_book_image>")
        sys.exit(1)

    title = recognize_book_title(sys.argv[1])
    print(title)
