"""Remove the copy of the title that `p2 ingest` leaves at the top of each own-corpus document's body.

Usage, from the repo root, after every `p2 ingest` of the arXiv abstracts:
    uv run python scripts/strip_repeated_titles.py
    uv run p2 ingest --report

fetch_arxiv.py writes each raw file as `# title`, a blank line, the abstract. Ingest keeps that heading as
the document's title line and also keeps the title text as the first line of the body, so every title was
in the document twice, which counts its words twice for bm25 and pulls the dense vectors toward the title.
This drops that first body line when it is the title (or, for a long title that ingest cut short in the
heading, starts with it), and leaves every other document alone, so running it twice changes nothing.
"""

from __future__ import annotations

from pathlib import Path

DOCS = Path("corpora/own/docs")


def main() -> None:
    changed = 0
    for path in sorted(DOCS.glob("*.md")):
        lines = path.read_text(encoding="utf-8").split("\n")
        if len(lines) < 4 or not lines[0].startswith("# ") or lines[1] != "":
            continue
        title = lines[0][2:].strip()
        first = lines[2].strip()
        if title and (first == title or first.startswith(title)):
            rest = lines[3:]
            if rest and rest[0] == "":
                rest = rest[1:]
            path.write_text("\n".join(lines[:2] + rest), encoding="utf-8", newline="\n")
            changed += 1
    print(f"removed a repeated title from {changed} document(s) in {DOCS}")


if __name__ == "__main__":
    main()
