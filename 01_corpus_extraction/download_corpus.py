#!/usr/bin/env python3
"""Download PDFs listed in links.txt into a corpus folder."""

from __future__ import annotations

import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import unquote, urlparse

DEFAULT_LINKS = Path(__file__).resolve().parent / "links.txt"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "corpus"
USER_AGENT = "Mozilla/5.0 (compatible; corpus-downloader/1.0)"
MAX_WORKERS = 2
MAX_RETRIES = 4
RETRY_DELAY = 2.0


def load_links(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def filename_from_url(url: str) -> str:
    name = Path(unquote(urlparse(url).path)).name
    return name or "document.pdf"


def download_pdf(url: str, output_dir: Path) -> tuple[str, str | None]:
    dest = output_dir / filename_from_url(url)
    if dest.exists() and dest.stat().st_size > 0:
        return url, None

    last_error = "unknown error"
    for attempt in range(MAX_RETRIES):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
        except urllib.error.URLError as exc:
            last_error = str(exc.reason if hasattr(exc, "reason") else exc)
            if attempt + 1 < MAX_RETRIES:
                time.sleep(RETRY_DELAY * (attempt + 1))
            continue

        if not data.startswith(b"%PDF"):
            return url, "response is not a PDF"

        dest.write_bytes(data)
        return url, None

    return url, last_error


def main() -> None:
    links_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LINKS
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT

    links = load_links(links_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    skipped = 0
    downloaded = 0
    failed: list[tuple[str, str]] = []

    pending = []
    for url in links:
        dest = output_dir / filename_from_url(url)
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            print(f"skip  {dest.name}")
        else:
            pending.append(url)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_pdf, url, output_dir): url for url in pending}
        for future in as_completed(futures):
            url = futures[future]
            _, error = future.result()
            name = filename_from_url(url)
            if error:
                failed.append((url, error))
                print(f"fail  {name}: {error}")
            else:
                downloaded += 1
                print(f"ok    {name}")

    print(
        f"\nDone: {downloaded} downloaded, {skipped} skipped, "
        f"{len(failed)} failed (total {len(links)})"
    )
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
