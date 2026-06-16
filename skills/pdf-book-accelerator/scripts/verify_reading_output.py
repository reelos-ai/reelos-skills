#!/usr/bin/env python3
"""Verify generated reading-note Markdown and HTML artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


PLACEHOLDERS = (
    "TODO",
    "待补",
    "未检测到明确",
    "定义 / 边界 / 应用场景",
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.add(str(attr["id"]))
        href = attr.get("href")
        if href and href.startswith("#"):
            self.hrefs.append(href[1:])


def count_section_items(markdown: str, heading_pattern: str) -> int:
    match = re.search(rf"^##\s+{heading_pattern}\s*$", markdown, flags=re.MULTILINE)
    if not match:
        return 0
    next_heading = re.search(r"^##\s+", markdown[match.end():], flags=re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(markdown)
    section = markdown[match.end():end]
    return len(re.findall(r"^- ", section, flags=re.MULTILINE))


def verify(workdir: Path, md_name: str, html_name: str) -> dict[str, object]:
    md_path = workdir / md_name
    html_path = workdir / html_name
    failures: list[str] = []
    warnings: list[str] = []

    if not md_path.exists():
        failures.append(f"missing markdown: {md_path}")
        markdown = ""
    else:
        markdown = md_path.read_text(encoding="utf-8")

    if not html_path.exists():
        failures.append(f"missing html: {html_path}")
        rendered = ""
    else:
        rendered = html_path.read_text(encoding="utf-8")

    if rendered and not re.search(r"<!doctype html>.*<html", rendered, flags=re.IGNORECASE | re.DOTALL):
        failures.append("html is not a standalone document")

    for token in PLACEHOLDERS:
        if token in markdown or token in rendered:
            failures.append(f"placeholder leaked: {token}")

    parser = LinkParser()
    if rendered:
        parser.feed(rendered)
        broken = sorted(href for href in parser.hrefs if href not in parser.ids)
        if broken:
            failures.append(f"broken anchors: {', '.join(broken[:8])}")
        if "https://fonts.googleapis.com" in rendered or "cdnjs.cloudflare.com" in rendered:
            failures.append("html depends on external CDN resources")

    q_count = len(re.findall(r"^- Q[:：]\s+", markdown, flags=re.MULTILINE))
    if q_count < 5:
        failures.append(f"review card count too low: {q_count}")

    nine_grid_count = count_section_items(markdown, "九宫格提取|Nine-Grid Extraction")
    if nine_grid_count and nine_grid_count != 9:
        failures.append(f"nine-grid item count is {nine_grid_count}, expected 9")

    if "爆破" in markdown or "baopo" in markdown:
        card_count = count_section_items(markdown, "33 张知识卡片框架")
        if card_count and card_count < 33:
            failures.append(f"33-card framework has only {card_count} items")

    method_section_count = count_section_items(markdown, "方法论卡片")
    if method_section_count and ("边界" not in markdown or "应用" not in markdown):
        failures.append("method cards must include boundary and application")

    if "读后行动闭环" in markdown and not all(token in markdown for token in ("行动目标", "最小行动", "迭代信号")):
        failures.append("action loop lacks goal, MVP, or iteration signal")

    # Chinese deep reports (marked by 复习卡片) must include the upgrade sections:
    # a read-mode gate, a falsification pass, and a spaced-reuse schedule.
    if "复习卡片" in markdown:
        if "证伪" not in markdown and "反例" not in markdown:
            failures.append("missing falsification section (模型证伪/反例)")
        if "复用调度" not in markdown and "间隔复盘" not in markdown:
            failures.append("missing reuse-schedule section (复用调度/间隔复盘)")

    metadata_path = workdir / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("low_text_warning") and "OCR" not in rendered and "提取" not in rendered:
            failures.append("low text warning is not reflected in html")
    else:
        warnings.append("metadata.json not found")

    return {
        "ok": not failures,
        "failures": failures,
        "warnings": warnings,
        "markdown": str(md_path),
        "html": str(html_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify generated reading-note artifacts.")
    parser.add_argument("workdir", type=Path)
    parser.add_argument("--md", default="reading-notes.zh-CN.md")
    parser.add_argument("--html", default="reading-notes.zh-CN.html")
    args = parser.parse_args()

    result = verify(args.workdir, args.md, args.html)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
