---
name: record-tnp-life-moment
description: Record an interesting life moment for the TNP household into Apple Notes. Trigger when the user's message begins with "record life moment".
---

# Record TNP Life Moment

Append a new life moment entry to the Apple Notes note **"TNP Life Moments"** in the **"Notes"** folder.

## Step 1 — Extract the Life Moment

Read the user's message carefully. The life moment description may be in English, Chinese, or a mix of both.

Preserve the meaning and wording as closely as possible. Do not paraphrase, summarize, or alter the content. Add line breaks only where they improve readability (e.g., between distinct sentences or clauses).

## Step 2 — Format the Entry

Format the entry as:

```
<MM/DD/YYYY>
<Life moment description>
```

Use today's date for the date line.

Example:

```
04/27/2026
Today Seth scored his first goal in the soccer game. The whole family was there cheering for him. 太棒了！
```

## Step 3 — Prepend to the Note via AppleScript

Run the following AppleScript via `osascript` to prepend the new entry at the top of the note. Replace `DATE_LINE` and `MOMENT_TEXT` with the actual formatted values.

```bash
osascript <<'APPLESCRIPT'
tell application "Notes"
    set targetFolder to folder "Notes"
    set targetNote to note "TNP Life Moments" of targetFolder

    set newEntry to "DATE_LINE" & linefeed & "MOMENT_TEXT"
    set existingBody to plaintext of targetNote

    set updatedBody to newEntry & linefeed & linefeed & existingBody
    set body of targetNote to updatedBody
end tell
APPLESCRIPT
```

### Important notes on the AppleScript

- The note name is **"TNP Life Moments"** and the folder name is **"Notes"**.
- `plaintext` reads the current note body as plain text; `body` sets it.
- Prepend `newEntry` followed by two line feeds before the existing body so entries are separated by a blank line.

### Handling quotes in the text

If the life moment description contains single or double quotes, use a Python helper to invoke the AppleScript to avoid shell escaping issues:

```bash
python3 -c "
import subprocess

date_line = 'MM/DD/YYYY'
moment_text = '''MOMENT_TEXT_HERE'''

script = f'''
tell application \"Notes\"
    set targetFolder to folder \"Notes\"
    set targetNote to note \"TNP Life Moments\" of targetFolder
    set newEntry to \"{date_line}\" & linefeed & \"{moment_text}\"
    set existingBody to plaintext of targetNote
    set updatedBody to newEntry & linefeed & linefeed & existingBody
    set body of targetNote to updatedBody
end tell
'''
subprocess.run(['osascript', '-e', script], check=True)
print('Life moment recorded.')
"
```

Use the Python approach whenever the text contains quotes or special characters.

## Step 4 — Confirm to the User

After the script runs successfully, confirm:

> Life moment recorded in "TNP Life Moments".
