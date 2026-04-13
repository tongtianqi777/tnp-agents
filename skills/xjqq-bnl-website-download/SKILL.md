---
name: xjqq-bnl-website-download
description: Download bnl files from https://piyopen.lovereadingbooks.com/category/cid/42, which is a page for XJQQ book bnl files. Use this skill when the user wants to download a `.bnl` file for a book from XJQQ website.
---

# XJQQ Bnl website download

Use this skill when the user wants to download a `.bnl` file for a book from XJQQ website. A book title (typically in Chinese) needs to be provided by the user.

## Workflow

1. Open the page https://piyopen.lovereadingbooks.com/category/cid/42 with Firecrawl browser tools.
2. Use Firecrawl interact prompts to:
   - click the top-right search box
   - type the requested book title
   - click the matching result, often labeled `bnl格式 <title>`
   - open the item detail page
3. Once the browser is on a content page like `/content/879?...`, resolve and download the file with `scripts/download_content.py`. The download link is often labeled with `下载bnl格式`.
4. Save to `/Users/tnpbot/.openclaw/workspace/downloads/xjqq/` by default unless the user asked for a different path.
5. Name the downloaded file in the format of `<title>-<original-file-name-without-extension>.bnl`.
6. If the .bnl file cannot be found for a given book title, let the user know.


## Preferred command

Run the helper script instead of manually reverse-engineering the file URL every time.

```bash
python3 /Users/tnpbot/.openclaw/workspace/skills/xjqq-bnl-website-download/scripts/download_content.py \
  --content-url "https://piyopen.lovereadingbooks.com/content/879?from=search&nid=4650&keyword=%E4%B8%89%E4%B8%AA%E7%81%AB%E8%BD%A6%E5%A4%B4"
```

Useful variants:

```bash
# If you already know the content id
python3 /Users/tnpbot/.openclaw/workspace/skills/xjqq-bnl-website-download/scripts/download_content.py --content-id 879

# If you only know the title
python3 /Users/tnpbot/.openclaw/workspace/skills/xjqq-bnl-website-download/scripts/download_content.py --title "三个火车头"

# If you want structured output
python3 /Users/tnpbot/.openclaw/workspace/skills/xjqq-bnl-website-download/scripts/download_content.py \
  --content-id 879 --json
```

## What the helper script does

The script queries the LoveReadingBooks content API at `https://p.lovereadingbooks.com/api/v1/content?_format=json`, prefers `fileUrl`, falls back to `url3`, then downloads the resolved file locally.

## Operating rules

- Prefer Firecrawl browser steps when the user explicitly asks to browse, click, search, or visually inspect the page.
- If the browser is already on the correct content page, skip extra clicks and run the script directly.
- If the title search returns multiple matches, do not guess. Show the options or ask the user which one to download.
- Keep downloads inside the workspace unless the user asks for a different location.
- After downloading, verify the saved file exists and report the exact path.

## Troubleshooting

- If Firecrawl can click the badge but does not expose the final file URL, use the current content-page URL with `download_content.py`.
- If the title alone is ambiguous, extract the numeric content id from `/content/<id>` and rerun with `--content-id`.
- If the page looks hydrated but HTML fetches are empty, rely on Firecrawl interact plus the API-backed helper script rather than raw page scraping.
