#!/usr/bin/env python3
"""Render reading notes Markdown into a polished standalone HTML page."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"“([^”]+)”", r'<span class="quote">“\1”</span>', escaped)
    return escaped


def slugify(text: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.lower()).strip("-") or "section"


def collect_headings(markdown: str) -> list[tuple[str, str]]:
    headings: list[tuple[str, str]] = []
    seen: dict[str, int] = {}
    for match in re.finditer(r"^##\s+(.+)$", markdown, flags=re.MULTILINE):
        title = match.group(1).strip()
        base = slugify(title)
        count = seen.get(base, 0)
        seen[base] = count + 1
        section_id = base if count == 0 else f"{base}-{count + 1}"
        headings.append((section_id, title))
    return headings


def section_list_class(section_id: str) -> str:
    for keyword, class_name in (
        ("阅读目标", "concept-cards"),
        ("知识资产", "concept-cards"),
        ("全书地图", "concept-cards"),
        ("章节精读", "concept-cards"),
        ("全书复盘", "concept-cards"),
        ("九宫格", "grid-nine"),
        ("方法论", "method-cards"),
        ("迁移", "transfer-grid"),
        ("已知领域", "transfer-grid"),
        ("单概念", "concept-cards"),
        ("提问链", "concept-cards"),
        ("关键词", "concept-cards"),
        ("金句", "concept-cards"),
        ("费曼", "concept-cards"),
        ("观点卡", "concept-cards"),
        ("写作外化", "concept-cards"),
        ("体系化", "concept-cards"),
        ("反馈", "action-loop"),
        ("行动闭环", "action-loop"),
        ("复盘", "review-log"),
        ("教学输出", "teaching-pack"),
        ("33", "knowledge-cards"),
        ("知识卡片", "knowledge-cards"),
    ):
        if keyword in section_id:
            return class_name
    return ""


def render_blocks(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    in_ul = False
    in_ol = False
    pending_q = ""
    heading_iter = iter(collect_headings(markdown))
    current_list_class = ""

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            if pending_q:
                out.append(f"<div class=\"card qcard\">{pending_q}</div>")
                pending_q = ""
            close_lists()
            continue

        if stripped.startswith("# "):
            close_lists()
            out.append(f"<h1>{inline_markup(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            close_lists()
            section_id, _ = next(heading_iter)
            current_list_class = section_list_class(section_id)
            out.append(f"<h2 id=\"{section_id}\">{inline_markup(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            close_lists()
            out.append(f"<h3>{inline_markup(stripped[4:])}</h3>")
        elif re.match(r"^\d+\. ", stripped):
            if pending_q:
                out.append(f"<div class=\"card qcard\">{pending_q}</div>")
                pending_q = ""
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            item_text = re.sub(r"^\d+\. ", "", stripped)
            out.append(f"<li>{inline_markup(item_text)}</li>")
        elif stripped.startswith("- Q: "):
            close_lists()
            if pending_q:
                out.append(f"<div class=\"card qcard\">{pending_q}</div>")
            pending_q = f"<p class=\"question\">{inline_markup(stripped[5:])}</p>"
        elif stripped.startswith("A: ") or stripped.startswith("A："):
            answer = stripped[2:].strip(" :：")
            if pending_q:
                pending_q += f"<p class=\"answer\">{inline_markup(answer)}</p>"
            else:
                out.append(f"<p>{inline_markup(stripped)}</p>")
        elif stripped.startswith("- "):
            if pending_q:
                out.append(f"<div class=\"card qcard\">{pending_q}</div>")
                pending_q = ""
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                class_attr = f' class="{current_list_class}"' if current_list_class else ""
                out.append(f"<ul{class_attr}>")
                in_ul = True
            out.append(f"<li>{inline_markup(stripped[2:])}</li>")
        else:
            if pending_q:
                out.append(f"<div class=\"card qcard\">{pending_q}</div>")
                pending_q = ""
            close_lists()
            meta_match = re.match(r"^(作者|来源|页数|估算词数):\s*(.*)$", stripped)
            if meta_match:
                out.append(
                    f"<p class=\"meta\"><span>{inline_markup(meta_match.group(1))}</span>{inline_markup(meta_match.group(2))}</p>"
                )
            else:
                out.append(f"<p>{inline_markup(stripped)}</p>")

    if pending_q:
        out.append(f"<div class=\"card qcard\">{pending_q}</div>")
    close_lists()
    return "\n".join(out)


def build_html(markdown: str, title: str) -> str:
    body = render_blocks(markdown)
    toc_links = "\n".join(
        f'      <a href="#{section_id}">{inline_markup(text)}</a>'
        for section_id, text in collect_headings(markdown)[:14]
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --paper: #fbfaf6;
      --ink: #1f2320;
      --muted: #667067;
      --line: #ded8ca;
      --accent: #b7402a;
      --accent-dark: #6f2a20;
      --sage: #dbe5d4;
      --card: #fffef9;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        linear-gradient(90deg, rgba(183,64,42,.08) 1px, transparent 1px),
        linear-gradient(180deg, rgba(31,35,32,.05) 1px, transparent 1px),
        var(--paper);
      background-size: 72px 72px;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
      line-height: 1.78;
    }}
    .shell {{
      display: grid;
      grid-template-columns: minmax(220px, 300px) minmax(0, 860px);
      gap: 48px;
      width: min(1180px, calc(100% - 48px));
      margin: 0 auto;
      padding: 48px 0 72px;
    }}
    aside {{
      position: sticky;
      top: 24px;
      align-self: start;
      border-left: 4px solid var(--accent);
      padding: 18px 0 18px 20px;
      color: var(--muted);
    }}
    aside .kicker {{
      color: var(--accent-dark);
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
      font-size: 12px;
    }}
    aside a {{
      display: block;
      margin: 10px 0;
      color: var(--muted);
      text-decoration: none;
      font-size: 14px;
    }}
    article {{
      background: rgba(255,254,249,.86);
      border: 1px solid var(--line);
      box-shadow: 0 28px 80px rgba(56, 48, 37, .12);
      padding: clamp(26px, 5vw, 64px);
    }}
    h1, h2, h3 {{
      font-family: Georgia, "Songti SC", "Noto Serif CJK SC", serif;
      line-height: 1.2;
      letter-spacing: 0;
    }}
    h1 {{
      margin: 0 0 22px;
      font-size: clamp(34px, 6vw, 72px);
      max-width: 12ch;
    }}
    h2 {{
      margin: 58px 0 18px;
      padding-top: 18px;
      border-top: 1px solid var(--line);
      font-size: clamp(24px, 3vw, 36px);
    }}
    h3 {{
      margin: 34px 0 12px;
      color: var(--accent-dark);
      font-size: 22px;
    }}
    p {{ margin: 16px 0; font-size: 17px; }}
    .meta {{
      display: inline-flex;
      gap: 10px;
      margin: 4px 12px 4px 0;
      padding: 6px 10px;
      border: 1px solid var(--line);
      background: var(--sage);
      font-size: 14px;
    }}
    .meta span {{ font-weight: 700; color: var(--accent-dark); }}
    ul, ol {{ padding-left: 1.35rem; }}
    li {{ margin: 9px 0; }}
    code {{
      padding: 2px 6px;
      border: 1px solid var(--line);
      background: #f3efe6;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: .92em;
    }}
    .quote {{ color: var(--accent-dark); font-weight: 600; }}
    .card {{
      margin: 14px 0;
      padding: 16px 18px;
      border: 1px solid var(--line);
      background: #fff;
    }}
    .question {{
      margin: 0 0 6px;
      font-weight: 700;
      color: var(--accent-dark);
    }}
    .answer {{ margin: 0; color: var(--ink); }}
    .grid-nine {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      padding: 0;
      list-style: none;
    }}
    .grid-nine li,
    .concept-cards li,
    .method-cards li,
    .transfer-grid li,
    .action-loop li,
    .review-log li,
    .teaching-pack li,
    .knowledge-cards li {{
      margin: 0 0 12px;
      padding: 14px 16px;
      border: 1px solid var(--line);
      background: #fff;
      list-style: none;
    }}
    .method-cards,
    .concept-cards,
    .transfer-grid,
    .action-loop,
    .review-log,
    .teaching-pack,
    .knowledge-cards {{
      padding: 0;
    }}
    .method-cards li::first-line,
    .concept-cards li::first-line,
    .transfer-grid li::first-line,
    .action-loop li::first-line,
    .teaching-pack li::first-line {{
      font-weight: 700;
      color: var(--accent-dark);
    }}
    article > h2:nth-of-type(1) + p {{
      font-size: 20px;
      line-height: 1.8;
    }}
    @media (max-width: 860px) {{
      .shell {{ display: block; width: min(100% - 28px, 760px); padding: 18px 0 42px; }}
      aside {{ position: static; margin-bottom: 18px; background: rgba(255,254,249,.78); }}
      article {{ padding: 24px 18px; }}
      h1 {{ max-width: 100%; }}
      .grid-nine {{ grid-template-columns: 1fr; }}
    }}
    @media print {{
      body {{ background: #fff; }}
      .shell {{ display: block; width: 100%; padding: 0; }}
      aside {{ display: none; }}
      article {{ border: 0; box-shadow: none; padding: 0; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <aside>
      <div class="kicker">Reading Notes</div>
{toc_links}
    </aside>
    <article>
{body}
    </article>
  </div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render reading notes Markdown as standalone HTML.")
    parser.add_argument("markdown", type=Path, help="Input Markdown file")
    parser.add_argument("--out", type=Path, help="Output HTML file")
    args = parser.parse_args()

    markdown = args.markdown.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", markdown, flags=re.MULTILINE)
    title = title_match.group(1) if title_match else "Reading Notes"
    out = args.out or args.markdown.with_suffix(".html")
    out.write_text(build_html(markdown, title), encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
