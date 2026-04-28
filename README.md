# tnp-agents

A collection of Claude Code skills and agents for the TNP household.

## Repository Structure

```
tnp-agents/
├── skills/                          # OpenClaw skills for Claude Code
│   ├── book-chinese-title-detection/   # Detect Chinese book titles from an image
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── detect.py
│   ├── seth-volunteering-hours-logging/  # Submit Seth's school volunteer hours to Google Form
│   │   └── SKILL.md
│   ├── tnp-life-moments/               # Record TNP household life moments into Apple Notes
│   │   └── SKILL.md
│   ├── xjqq-bnl-website-download/      # Download .bnl files from the XJQQ book website
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── download_content.py
│   └── xjqq-picture-to-bnl/           # Download .bnl files for all XJQQ books in a picture
│       └── SKILL.md
└── xjqq-download-agent/             # LangChain agent for downloading XJQQ book files
    ├── prompts.md
    └── requirements.txt
```

## Skills

| Skill | Trigger | Description |
|---|---|---|
| `book-chinese-title-detection` | User provides a book shelf image | Detects Chinese titles of books from an image |
| `seth-volunteering-hours-logging` | "log volunteer hours", "record volunteering", "submit hours for Seth" | Submits Seth's school volunteer hours to the school Google Form |
| `record-tnp-life-moment` | "record life moment ..." | Records a life moment into the Apple Notes note "TNP Life Moments" |
| `xjqq-bnl-website-download` | User wants to download a `.bnl` file for an XJQQ book | Downloads `.bnl` files from the XJQQ book website |
| `xjqq-picture-to-bnl` | User wants to download `.bnl` files for all XJQQ books in a picture | Combines image recognition and `.bnl` downloading for a full book shelf picture |