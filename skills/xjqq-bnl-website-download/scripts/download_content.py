#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

API_URL = "https://p.lovereadingbooks.com/api/v1/content?_format=json"
DEFAULT_OUTPUT_DIR = Path("/Users/tnpbot/.openclaw/workspace/downloads")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve and download a LoveReadingBooks content file"
    )
    parser.add_argument("--content-url", help="Full content page URL, e.g. https://piyopen.lovereadingbooks.com/content/879?...")
    parser.add_argument("--content-id", help="Numeric content id from a /content/<id> page")
    parser.add_argument("--title", help="Title to search for if the content id is not known")
    parser.add_argument("--output", help="Exact output file path")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for downloaded files when --output is not set")
    parser.add_argument("--json", action="store_true", help="Emit final result as JSON")
    args = parser.parse_args()

    if not any([args.content_url, args.content_id, args.title]):
        parser.error("pass at least one of --content-url, --content-id, or --title")
    return args


def parse_content_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    parsed = urllib.parse.urlparse(url)
    segments = [segment for segment in parsed.path.split("/") if segment]
    content_id = None
    title = None

    if len(segments) >= 2 and segments[0] == "content":
        content_id = segments[1]

    query = urllib.parse.parse_qs(parsed.query)
    for key in ("title", "keyword"):
        values = query.get(key)
        if values and values[0].strip():
            title = values[0].strip()
            break

    return content_id, title


def fetch_json(url: str) -> object:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "OpenClaw LoveReadingBooks downloader",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def build_query_url(content_id: Optional[str], title: Optional[str]) -> str:
    params: Dict[str, str] = {}
    if content_id:
        params["id"] = content_id
    if title:
        params["title"] = title
    return f"{API_URL}&{urllib.parse.urlencode(params)}" if params else API_URL


def choose_entry(entries: List[dict], requested_title: Optional[str]) -> dict:
    if not entries:
        raise SystemExit("No matching content entries returned by the API")

    if requested_title:
        exact = [entry for entry in entries if entry.get("title") == requested_title]
        if len(exact) == 1:
            return exact[0]
        if len(exact) > 1:
            raise SystemExit(
                "Multiple exact title matches returned. Re-run with --content-id or a specific --output path."
            )

    if len(entries) > 1:
        titles = ", ".join(sorted({entry.get('title', '<untitled>') for entry in entries}))
        raise SystemExit(f"Multiple matches returned: {titles}. Re-run with --content-id.")

    return entries[0]


def pick_download_url(entry: dict) -> str:
    for key in ("fileUrl", "url3"):
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise SystemExit("Entry does not contain fileUrl or url3")


def infer_output_path(download_url: str, output: Optional[str], output_dir: str) -> Path:
    if output:
        return Path(output).expanduser().resolve()

    filename = Path(urllib.parse.urlparse(download_url).path).name or "download.bin"
    target_dir = Path(output_dir).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename


def download_file(download_url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(download_url, headers={"User-Agent": "OpenClaw LoveReadingBooks downloader"})
    with urllib.request.urlopen(req, timeout=120) as response, open(destination, "wb") as fh:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            fh.write(chunk)


def main() -> int:
    args = parse_args()

    content_id = args.content_id
    title = args.title

    if args.content_url:
        parsed_id, parsed_title = parse_content_url(args.content_url)
        content_id = content_id or parsed_id
        title = title or parsed_title

    query_url = build_query_url(content_id, title)
    entries = fetch_json(query_url)
    if not isinstance(entries, list):
        raise SystemExit("Unexpected API response shape")

    entry = choose_entry(entries, title)
    download_url = pick_download_url(entry)
    output_path = infer_output_path(download_url, args.output, args.output_dir)
    download_file(download_url, output_path)
    size_bytes = output_path.stat().st_size

    result = {
        "contentId": entry.get("id"),
        "nid": entry.get("nid"),
        "title": entry.get("title"),
        "downloadUrl": download_url,
        "path": str(output_path),
        "sizeBytes": size_bytes,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Downloaded {result['title']} -> {result['path']}")
        print(f"URL: {result['downloadUrl']}")
        print(f"Size: {result['sizeBytes']} bytes")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
