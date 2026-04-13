---
name: book-chinese-title-detection
version: 1.0.0
description: |
  This skill allows you to detect all the Chinese titles of the books from an image.
  Use this when the user asks "detect the Chinese titles of the books from this image".
author: TNP
---

# Book Chinese Title Detection

This skill allows you to detect the titles of the books from an image.

Use this when the user asks "detect the Chinese titles of the books from this image".

## Workflows

### 1. Ask for Book Image Path
Asks for the book image path, and use it to populate the {{BookImagePath}} placeholder in the next step.

### 2. Run the script
Run my script: `python3 {baseDir}/scripts/detect.py "{{BookImagePath}}"`
