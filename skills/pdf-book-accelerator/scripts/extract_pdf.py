#!/usr/bin/env python3
"""Extract text and simple structure signals from a PDF ebook."""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path

import pdfplumber

logging.getLogger("pdfminer").setLevel(logging.ERROR)

CHAPTER_PATTERNS = [
    re.compile(r"^\s*(chapter|chap\.?)\s+\d+\s*[:.-]\s*(.+)?$", re.IGNORECASE),
    re.compile(r"^\s*(第[一二三四五六七八九十百千万0-9]+[章节篇部])\s*(.+)?$"),
    re.compile(r"^\s*\d{1,2}\s+[A-Z][A-Za-z0-9 ,:;'\-]{6,}$"),
]
CHAPTER_NUMBER = re.compile(r"\bchapter\s+(\d+)\b", re.IGNORECASE)


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def likely_heading(line: str) -> bool:
    line = line.strip()
    if not line or len(line) > 120:
        return False
    return any(pattern.match(line) for pattern in CHAPTER_PATTERNS)


def merge_wrapped_lines(lines: list[str]) -> list[str]:
    merged: list[str] = []
    for raw_line in lines:
        line = re.sub(r"\s+", " ", raw_line).strip()
        if not line:
            continue
        if merged and not re.match(r"^(chapter|back matter|takeaways|further reading|references|acknowledgments|about|colophon)\b", line, re.IGNORECASE):
            merged[-1] = f"{merged[-1]} {line}"
        else:
            merged.append(line)
    return merged


def extract_toc_titles(page_texts: dict[int, str]) -> dict[int, str]:
    toc_titles: dict[int, str] = {}
    for page in range(1, min(12, len(page_texts)) + 1):
        text = page_texts.get(page, "")
        if "Contents" not in text:
            continue
        after_contents = text.split("Contents", 1)[1]
        before_back = after_contents.split("Back matter", 1)[0]
        for line in merge_wrapped_lines(before_back.splitlines()):
            match = re.match(r"^Chapter\s+(\d+)\s*:\s*(.+)$", line, flags=re.IGNORECASE)
            if match:
                toc_titles[int(match.group(1))] = f"Chapter {match.group(1)}: {match.group(2).strip()}"
        if toc_titles:
            break
    return toc_titles


def extract(pdf_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = out_dir / "pages"
    pages_dir.mkdir(exist_ok=True)

    page_records = []
    headings = []
    page_texts: dict[int, str] = {}
    all_text_parts = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            raw_text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            text = normalize_text(raw_text)
            page_texts[index] = text
            page_file = pages_dir / f"page-{index:04d}.txt"
            page_file.write_text(text + "\n", encoding="utf-8")

            for line in text.splitlines()[:40]:
                if likely_heading(line):
                    headings.append({"page": index, "text": line.strip()})

            all_text_parts.append(f"\n\n--- page {index} ---\n\n{text}")
            page_records.append(
                {
                    "page": index,
                    "chars": len(text),
                    "words_estimate": len(re.findall(r"\w+", text)),
                    "text_file": str(page_file),
                }
            )

    full_text = normalize_text("".join(all_text_parts))
    (out_dir / "full-text.txt").write_text(full_text + "\n", encoding="utf-8")

    metadata = {
        "source": str(pdf_path),
        "pages": len(page_records),
        "total_chars": sum(page["chars"] for page in page_records),
        "total_words_estimate": sum(page["words_estimate"] for page in page_records),
        "low_text_warning": sum(page["chars"] for page in page_records) < max(1000, len(page_records) * 80),
        "candidate_headings": headings[:200],
        "pages_detail": page_records,
    }
    toc_titles = extract_toc_titles(page_texts)
    chapter_starts = []
    seen_titles = set()
    for heading in headings:
        title = re.sub(r"\s+", " ", heading["text"]).strip()
        if heading["page"] <= 7:
            continue
        number_match = CHAPTER_NUMBER.search(title)
        if number_match:
            title = toc_titles.get(int(number_match.group(1)), title)
        if title in seen_titles:
            continue
        seen_titles.add(title)
        chapter_starts.append({"page": heading["page"], "title": title})
    metadata["toc_titles"] = toc_titles
    metadata["chapter_starts"] = chapter_starts
    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "chapters.json").write_text(
        json.dumps(chapter_starts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from a PDF ebook.")
    parser.add_argument("pdf", type=Path, help="Path to the PDF file")
    parser.add_argument("--out", type=Path, default=Path("book-extract"), help="Output directory")
    parser.add_argument("--verbose", action="store_true", help="Print full metadata including page details")
    args = parser.parse_args()

    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")

    metadata = extract(args.pdf, args.out)
    if args.verbose:
        print(json.dumps(metadata, ensure_ascii=False, indent=2))
    else:
        summary = {
            "source": metadata["source"],
            "pages": metadata["pages"],
            "total_chars": metadata["total_chars"],
            "total_words_estimate": metadata["total_words_estimate"],
            "low_text_warning": metadata["low_text_warning"],
            "chapter_starts": metadata["chapter_starts"],
            "out": str(args.out),
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
