---
name: record-tnp-life-moment
description: Record an interesting life moment for the TNP household into Apple Notes. Trigger when the user's message begins with "record life moment".
---

# Record TNP Life Moment

Append a new life moment entry to the Apple Notes note **"TNP Life Moments"** in the **"Notes"** folder.

## Step 1 — Extract the Life Moment

Read the user's message carefully. The life moment description may be in English, Chinese, or a mix of both.

Preserve the meaning and wording as closely as possible. Do not paraphrase, summarize, or alter the content. Add line breaks only where they improve readability (e.g., between distinct sentences or clauses).

**Date:** If the user explicitly states a date (e.g., "yesterday", "last Saturday", "April 20", "2026-04-20"), use that date. Otherwise default to today's date. Always convert to `MM/DD/YYYY` format.

**Sender:** Identify who sent the message. Jake is the primary user. If the message came from Telegram account `@zoeyhu`, the sender is Zoey. Use the first name only.

## Step 2 — Format the Entry

The date line must be **bold**. The sender's name goes on the next line in *italics*. Then a blank line, then the life moment description.

Example (rendered):

> **04/27/2026**
> *Jake*
>
> Today Seth scored his first goal in the soccer game. The whole family was there cheering for him. 太棒了！

In HTML (used when writing to Apple Notes):

```html
<div><b>MM/DD/YYYY</b></div><div><i>Sender Name</i></div><div><br></div><div>Life moment description</div><div><br></div>
```

Use the date and sender from Step 1.

## Step 3 — Insert into the Note via Python + AppleScript

Write the following script to `/tmp/record_moment.py`, substituting the actual `DATE_LINE`, `SENDER_NAME`, and `MOMENT_TEXT` values:

```python
import subprocess, html, os

DATE_LINE = "MM/DD/YYYY"
SENDER_NAME = "Sender Name"
MOMENT_TEXT = "MOMENT_TEXT_HERE"

# Read the current note body as HTML
get_script = """
tell application "Notes"
    set targetNote to note "TNP Life Moments" of folder "Notes"
    return body of targetNote
end tell
"""
result = subprocess.run(["osascript", "-e", get_script], capture_output=True, text=True, check=True)
current_html = result.stdout.strip()

# Build the new entry HTML (bold date, italic sender, blank line, description, trailing blank line)
new_entry = (
    f"<div><b>{html.escape(DATE_LINE)}</b></div>"
    f"<div><i>{html.escape(SENDER_NAME)}</i></div>"
    f"<div><br></div>"
    f"<div>{html.escape(MOMENT_TEXT)}</div>"
    f"<div><br></div>"
)

# Insert after the first </div> (which closes the note title line "TNP Life Moments")
insert_pos = current_html.find("</div>") + len("</div>")
updated_html = current_html[:insert_pos] + new_entry + current_html[insert_pos:]

# Write the updated HTML to a temp file so AppleScript can read it safely
# (avoids embedding HTML directly in AppleScript strings, which breaks on quotes/special chars)
import os
html_tmp = "/tmp/note_content.html"
with open(html_tmp, "w", encoding="utf-8") as f:
    f.write(updated_html)

set_script = f"""
tell application "Notes"
    set targetNote to note "TNP Life Moments" of folder "Notes"
    set htmlContent to read POSIX file "{html_tmp}" as «class utf8»
    set body of targetNote to htmlContent
end tell
"""
subprocess.run(["osascript", "-e", set_script], check=True)
os.remove(html_tmp)
print("Life moment recorded.")
```

Run it:

```bash
python3 /tmp/record_moment.py
```

### Important notes

- The note title "TNP Life Moments" lives in the first `<div>` of the body HTML. Inserting after the first `</div>` places the new entry directly below the title.
- `html.escape()` safely handles quotes and special characters in the date and text.
- `repr()` in Python produces a properly quoted AppleScript string literal for the HTML payload.

## Step 4 — Confirm to the User

After the script runs successfully, confirm:

> Life moment recorded in "TNP Life Moments".
