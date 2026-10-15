"""Fetch arXiv stat.AP abstracts whose paper carries a CC0, CC BY or CC BY-SA license.

Usage, from the repo root:
    uv run python scripts/fetch_arxiv.py --from 20250101 --until 20251231 --limit 600 --out ../p2-raw/arxiv

It lists papers in stat.AP through the arXiv search API (oldest first, submitted between the two dates),
keeps those whose primary category is stat.AP, reads each one's license from its abstract page on
export.arxiv.org, and writes one `<arxiv id>.md` per paper with a license p2 allows
(`# title`, a blank line, the abstract) into a folder named after the license, so `p2 ingest`
can run once per license. It stops after --limit papers.
arXiv asks for no more than one request every three seconds; the script pauses ten between requests,
and waits 15 minutes or more when arXiv answers 406, 429 or 503.
A file already on disk is not fetched again, so a stopped run can be restarted with the same command.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = "https://export.arxiv.org/api/query"
ABS = "https://export.arxiv.org/abs/{id}"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
CATEGORY = "stat.AP"
PAGE = 100
PAUSE_SECONDS = 10.0  # arXiv's floor is 3; at 3 it throttled us after about 50 requests
USER_AGENT = "p2-rag-system course project (fetch_arxiv.py)"

# The license URL arXiv shows on the abstract page, mapped to p2's license vocabulary; anything else is skipped.
LICENSES = {
    "creativecommons.org/publicdomain/zero/1.0": "cc0-1.0",
    "creativecommons.org/licenses/by/4.0": "cc-by-4.0",
    "creativecommons.org/licenses/by/3.0": "cc-by-3.0",
    "creativecommons.org/licenses/by-sa/4.0": "cc-by-sa-4.0",
}
LICENSE_LINK = re.compile(r'href="https?://((?:creativecommons\.org|arxiv\.org)/[^"]*licen[cs]es?/[^"]*|creativecommons\.org/publicdomain/[^"]*)"')


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            # 406, 429 and 503 are arXiv saying "slow down": wait 15 minutes, then 30, then 45
            wait = 900 * (attempt + 1) if err.code in (406, 429, 503) else 30
            print(f"  {err}; retrying in {wait}s", file=sys.stderr, flush=True)
            time.sleep(wait)
        except (TimeoutError, urllib.error.URLError) as err:
            wait = 30 * (attempt + 1)
            print(f"  {err}; retrying in {wait}s", file=sys.stderr, flush=True)
            time.sleep(wait)
    raise RuntimeError(f"gave up on {url}")


def clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def license_of(arxiv_id: str) -> str:
    """The license link on the paper's abstract page, without scheme or trailing slash, or '' if none."""
    html = fetch(ABS.format(id=arxiv_id)).decode("utf-8", "replace")
    for m in LICENSE_LINK.finditer(html):
        link = m.group(1).rstrip("/")
        if "info.arxiv.org" not in link:
            return link
    return ""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--from", dest="start", required=True, help="first submission date, YYYYMMDD")
    ap.add_argument("--until", required=True, help="last submission date, YYYYMMDD")
    ap.add_argument("--limit", type=int, default=600, help="stop after this many papers are kept")
    ap.add_argument("--out", required=True, help="folder for the raw files, outside the repo")
    args = ap.parse_args()

    out = Path(args.out)
    on_disk = {p.stem for p in out.glob("*/*.md")}
    kept = len(on_disk)
    # papers already found to have a license p2 does not allow, so a resumed run does not ask again
    skip_file = out / "skipped.tsv"
    known_skips = {line.split("\t")[0] for line in skip_file.read_text(encoding="utf-8").splitlines()} if skip_file.exists() else set()
    looked = 0
    skipped: dict[str, int] = {}
    query = f"cat:{CATEGORY} AND submittedDate:[{args.start}0000 TO {args.until}2359]"
    offset = 0
    while kept < args.limit:
        params = {"search_query": query, "start": offset, "max_results": PAGE, "sortBy": "submittedDate", "sortOrder": "ascending"}
        root = ET.fromstring(fetch(API + "?" + urllib.parse.urlencode(params)))
        time.sleep(PAUSE_SECONDS)
        entries = root.findall("a:entry", NS)
        if not entries:
            break
        for entry in entries:
            if kept >= args.limit:
                break
            primary = entry.find("arxiv:primary_category", NS)
            if primary is None or primary.get("term") != CATEGORY:
                continue
            arxiv_id = re.sub(r"v\d+$", "", clean(entry.findtext("a:id", "", NS)).rsplit("/abs/", 1)[-1])
            if arxiv_id in on_disk or arxiv_id in known_skips:
                continue
            looked += 1
            link = license_of(arxiv_id)
            time.sleep(PAUSE_SECONDS)
            lic = LICENSES.get(link)
            if lic is None:
                skipped[link or "(no license shown)"] = skipped.get(link or "(no license shown)", 0) + 1
                out.mkdir(parents=True, exist_ok=True)
                with skip_file.open("a", encoding="utf-8", newline="\n") as f:
                    f.write(f"{arxiv_id}\t{link or '(no license shown)'}\n")
                continue
            title = clean(entry.findtext("a:title", "", NS))
            abstract = clean(entry.findtext("a:summary", "", NS))
            folder = out / lic
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"{arxiv_id}.md").write_text(f"# {title}\n\n{abstract}\n", encoding="utf-8", newline="\n")
            kept += 1
        offset += PAGE
        print(f"listed {offset}, license checked {looked}, kept {kept} of {args.limit}", file=sys.stderr, flush=True)

    print(f"kept {kept} {CATEGORY} abstracts under {out}")
    for link, n in sorted(skipped.items(), key=lambda kv: -kv[1]):
        print(f"  skipped {n}: {link}")


if __name__ == "__main__":
    main()
