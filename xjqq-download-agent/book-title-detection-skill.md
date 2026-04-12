# 
1. When the user sends an image and asks "detect the title of the book in this image":
2. Run my script: `python3 book-title-detection-agent.py "{{BookImagePath}}"`


---
name: book-title-detection-skill
version: 1.0.0
description: |
  This skill allows you to detect the title of a book from an image.
  Use this when the user asks "detect the title of the book in this image".
author: TNP
---

# Book Title Detection Skill

This skill allows you to detect the title of a book from an image.

Use this when the user asks "detect the title of the book in this image".

## Workflows

### 1. Ask for Book Image Path
Asks for the book image path, and use it to populate the {{BookImagePath}} placeholder in the next step.

### 2. Run the script
Run my script: `python3 book-title-detection-agent.py "{{BookImagePath}}"`
