#!/usr/bin/env python3
"""Render reading-notes Markdown into a polished, standalone HTML report.

The output is fully self-contained (no external CDN, system fonts only),
responsive, print-friendly, and adapts to light/dark color schemes. It adds a
book-identity hero with a stat dashboard, a scroll-spy table of contents, a
reading-progress bar, and section-aware card layouts.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

META_KEYS = ("作者", "来源", "页数", "估算词数", "阅读模式", "Author", "Source", "Pages", "Estimated words", "Reading mode")

# Friendly labels + icons for the hero stat dashboard.
META_DISPLAY = {
    "作者": ("✍️", "作者"),
    "Author": ("✍️", "Author"),
    "页数": ("📄", "页数"),
    "Pages": ("📄", "Pages"),
    "估算词数": ("📝", "估算词数"),
    "Estimated words": ("📝", "Words"),
    "阅读模式": ("⚙️", "阅读模式"),
    "Reading mode": ("⚙️", "Mode"),
}

MODE_LABELS = {
    "baopo": "爆破模式 · 深度精读",
    "suidan": "碎弹模式 · 快速速读",
    "hedan": "核弹模式 · 跨书对读",
}

# (keyword in heading, icon, hue, layout). First match wins, so order specific → generic.
# layout: "grid" = nine-grid tiles, "cards" = card grid, "list" = clean bullets.
SECTION_THEMES: list[tuple[str, str, int, str]] = [
    ("一页速读", "📖", 205, "list"),
    ("One-Page", "📖", 205, "list"),
    ("阅读目标", "🎯", 8, "cards"),
    ("知识资产转换", "🧰", 28, "cards"),
    ("知识资产", "🧰", 28, "cards"),
    ("生平年表", "🕰️", 35, "timeline"),
    ("年表", "🕰️", 35, "timeline"),
    ("时间线", "🕰️", 35, "timeline"),
    ("生平", "🕰️", 35, "timeline"),
    ("Timeline", "🕰️", 35, "timeline"),
    ("核心结论", "🎯", 8, "list"),
    ("一句话", "🎯", 8, "list"),
    # Upgrade sections (read-mode gate / falsification / spaced reuse).
    ("选读法门", "🧭", 158, "list"),
    ("读法", "🧭", 158, "list"),
    ("模型证伪", "🔬", 2, "cards"),
    ("证伪", "🔬", 2, "cards"),
    ("反例", "🔬", 2, "cards"),
    ("间隔复盘", "📅", 152, "cards"),
    ("复用调度", "🔁", 152, "cards"),
    ("跨书", "🔗", 205, "cards"),
    ("反事实", "💡", 45, "list"),
    ("核心主张", "📌", 8, "list"),
    ("Candidate Thesis", "📌", 8, "list"),
    ("候选核心问题", "❓", 268, "cards"),
    ("Candidate Questions", "❓", 268, "cards"),
    ("单概念", "🧩", 286, "cards"),
    ("提问链", "❓", 268, "cards"),
    ("读前三问", "❓", 268, "cards"),
    ("结构骨架", "🧱", 158, "list"),
    ("Structure", "🧱", 158, "list"),
    ("全书地图", "🗺️", 158, "list"),
    ("章节地图", "🗺️", 158, "list"),
    ("Chapter Map", "🗺️", 158, "list"),
    ("章节要点", "📑", 205, "cards"),
    ("Chapter Takeaways", "📑", 205, "cards"),
    ("章节精读", "🔬", 205, "cards"),
    ("作者的核心机制", "⚙️", 205, "list"),
    ("ARISE", "🛠️", 152, "list"),
    ("方法", "🛠️", 152, "cards"),
    ("高频术语", "🔑", 38, "cards"),
    ("关键词", "🔑", 38, "cards"),
    ("Term Signals", "🔑", 38, "cards"),
    ("金句", "✨", 45, "cards"),
    ("费曼", "🧠", 286, "cards"),
    ("观点卡", "🗂️", 205, "cards"),
    ("写作外化", "✍️", 205, "cards"),
    ("体系化", "🕸️", 158, "cards"),
    ("反常识", "💡", 45, "cards"),
    ("九宫格", "🔲", 286, "grid"),
    ("Nine-Grid", "🔲", 286, "grid"),
    ("已知领域", "🔗", 205, "cards"),
    ("迁移", "🔗", 205, "cards"),
    ("读后行动", "🔁", 152, "cards"),
    ("行动闭环", "🔁", 152, "cards"),
    ("Action Loop", "🔁", 152, "cards"),
    ("7 天复盘", "📅", 152, "cards"),
    ("全书复盘", "🧭", 205, "cards"),
    ("复盘", "📅", 152, "cards"),
    ("教学", "🎓", 268, "cards"),
    ("知识卡片", "🗂️", 286, "cards"),
    ("33", "🗂️", 286, "cards"),
    ("复习卡片", "🃏", 8, "cards"),
    ("Review Cards", "🃏", 8, "cards"),
    ("适用边界", "🚧", 8, "list"),
    ("阅读计划", "🗓️", 205, "list"),
    ("Reading Plan", "🗓️", 205, "list"),
    ("脚本", "📝", 205, "list"),
    ("Personal Script", "📝", 205, "list"),
    ("应用建议", "🧭", 152, "list"),
    ("肯定句", "💡", 45, "list"),
    ("今天就能做", "🚀", 8, "list"),
]


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"“([^”]+)”", r'<span class="quote">“\1”</span>', escaped)
    return escaped


def slugify(text: str) -> str:
    return re.sub(r"[^\w一-鿿]+", "-", text.lower()).strip("-") or "section"


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


def section_theme(title: str) -> tuple[str, int, str]:
    for keyword, icon, hue, layout in SECTION_THEMES:
        if keyword in title:
            return icon, hue, layout
    return "📘", 205, "list"


def split_lead(text: str) -> tuple[str, str]:
    """Split a card line into a bold lead and body when it reads as 'Lead: body'."""
    match = re.match(r"^([^:：]{1,28})[:：]\s*(.+)$", text)
    if match and not re.search(r"[。！？.!?]", match.group(1)):
        return match.group(1).strip(), match.group(2).strip()
    return "", text


def split_timeline(text: str) -> tuple[str, str]:
    """Split 'time — event' / 'time: event' into (time, event)."""
    match = re.match(r"^([^—:：]{1,32}?)\s*[—:：]\s*(.+)$", text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "", text


def render_card_item(text: str, layout: str) -> str:
    if layout == "timeline":
        time, event = split_timeline(text)
        if time:
            return (
                f'<li class="tl"><span class="tl-dot"></span>'
                f'<span class="tl-time">{inline_markup(time)}</span>'
                f'<span class="tl-event">{inline_markup(event)}</span></li>'
            )
        return f'<li class="tl"><span class="tl-dot"></span><span class="tl-event">{inline_markup(text)}</span></li>'
    if layout == "grid":
        lead, body = split_lead(text)
        if lead:
            return (
                f'<li class="tile"><span class="tile-key">{inline_markup(lead)}</span>'
                f'<span class="tile-val">{inline_markup(body)}</span></li>'
            )
        return f'<li class="tile"><span class="tile-val">{inline_markup(text)}</span></li>'
    lead, body = split_lead(text)
    if lead:
        return (
            f'<li class="card"><span class="lead">{inline_markup(lead)}</span>'
            f'<span class="body">{inline_markup(body)}</span></li>'
        )
    return f'<li class="card"><span class="body">{inline_markup(text)}</span></li>'


def render_qcard(question: str, answer: str) -> str:
    a = (
        f'<p class="answer"><span class="badge a">A</span>{inline_markup(answer)}</p>'
        if answer
        else ""
    )
    return (
        f'<div class="qa"><p class="question"><span class="badge q">Q</span>'
        f"{inline_markup(question)}</p>{a}</div>"
    )


def render_section_body(body_lines: list[str], layout: str) -> str:
    out: list[str] = []
    in_ul = False
    in_ol = False
    in_fence = False
    fence_lang = ""
    fence_buf: list[str] = []
    pending_q = ""
    pending_a = ""

    list_open_tag = (
        '<ul class="grid9">' if layout == "grid"
        else '<ul class="cardgrid">' if layout == "cards"
        else '<ul class="timeline">' if layout == "timeline"
        else "<ul>"
    )

    def flush_q() -> None:
        nonlocal pending_q, pending_a
        if pending_q:
            out.append(render_qcard(pending_q, pending_a))
            pending_q = ""
            pending_a = ""

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    i = 0
    while i < len(body_lines):
        raw = body_lines[i]
        stripped = raw.strip()

        # Fenced code / passthrough blocks.
        fence = re.match(r"^```+\s*([\w-]*)\s*$", stripped)
        if fence and not in_fence:
            flush_q()
            close_lists()
            in_fence = True
            fence_lang = fence.group(1).lower()
            fence_buf = []
            i += 1
            continue
        if in_fence:
            if re.match(r"^```+\s*$", stripped):
                content = "\n".join(fence_buf)
                if fence_lang in ("svg", "html", "raw"):
                    out.append(f'<div class="embed">{content}</div>')
                else:
                    out.append(f"<pre><code>{html.escape(content)}</code></pre>")
                in_fence = False
            else:
                fence_buf.append(raw)
            i += 1
            continue

        if not stripped:
            flush_q()
            close_lists()
            i += 1
            continue

        # Raw inline HTML block (e.g. an SVG mental-model diagram).
        if stripped.startswith("<") and re.match(r"^<(svg|figure|table|div|img|p|span)\b", stripped, re.IGNORECASE):
            flush_q()
            close_lists()
            block = [raw]
            close_tag = re.match(r"^<(\w+)", stripped)
            if close_tag:
                end = f"</{close_tag.group(1)}>"
                while end not in raw and i + 1 < len(body_lines):
                    i += 1
                    raw = body_lines[i]
                    block.append(raw)
            out.append(f'<div class="embed">{chr(10).join(block)}</div>')
            i += 1
            continue

        # GFM table block.
        if stripped.startswith("|") and stripped.endswith("|") and i + 1 < len(body_lines) \
                and re.match(r"^\|[\s:\-|]+\|$", body_lines[i + 1].strip()):
            flush_q()
            close_lists()
            rows: list[str] = []
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # skip header + separator
            while i < len(body_lines) and body_lines[i].strip().startswith("|"):
                cells = [c.strip() for c in body_lines[i].strip().strip("|").split("|")]
                rows.append(
                    "<tr>" + "".join(f"<td>{inline_markup(c)}</td>" for c in cells) + "</tr>"
                )
                i += 1
            thead = "<tr>" + "".join(f"<th>{inline_markup(c)}</th>" for c in header) + "</tr>"
            out.append(
                f'<div class="tablewrap"><table><thead>{thead}</thead>'
                f"<tbody>{''.join(rows)}</tbody></table></div>"
            )
            continue

        # Blockquote → callout (supports > [!tip]/[!note]/[!warn] kind tags).
        if stripped.startswith(">"):
            flush_q()
            close_lists()
            quote_lines: list[str] = []
            kind = "note"
            while i < len(body_lines) and body_lines[i].strip().startswith(">"):
                content = body_lines[i].strip()[1:].strip()
                tag = re.match(r"^\[!(\w+)\]\s*(.*)$", content)
                if tag:
                    kind = tag.group(1).lower()
                    if tag.group(2):
                        quote_lines.append(tag.group(2))
                elif content:
                    quote_lines.append(content)
                i += 1
            inner = " ".join(inline_markup(line) for line in quote_lines)
            out.append(f'<blockquote class="callout {kind}">{inner}</blockquote>')
            continue

        if stripped.startswith("### "):
            flush_q()
            close_lists()
            out.append(f"<h3>{inline_markup(stripped[4:])}</h3>")
        elif re.match(r"^\d+\.\s", stripped):
            flush_q()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            item_text = re.sub(r"^\d+\.\s", "", stripped)
            out.append(f"<li>{inline_markup(item_text)}</li>")
        elif stripped.startswith("- Q: ") or stripped.startswith("- Q："):
            flush_q()
            close_lists()
            pending_q = stripped[5:].strip()
        elif (stripped.startswith("A: ") or stripped.startswith("A：")) and pending_q:
            pending_a = stripped[2:].strip(" :：")
        elif stripped.startswith("- "):
            flush_q()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append(list_open_tag)
                in_ul = True
            if layout in ("cards", "grid", "timeline"):
                out.append(render_card_item(stripped[2:], layout))
            else:
                out.append(f"<li>{inline_markup(stripped[2:])}</li>")
        else:
            flush_q()
            close_lists()
            out.append(f"<p>{inline_markup(stripped)}</p>")
        i += 1

    flush_q()
    close_lists()
    return "\n".join(out)


def parse_document(markdown: str) -> tuple[str, list[tuple[str, str]], str]:
    """Return (title, meta_pairs, body_markdown_after_meta)."""
    lines = markdown.splitlines()
    title = "Reading Notes"
    meta: list[tuple[str, str]] = []
    body_start = 0

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# ") and title == "Reading Notes":
            title = stripped[2:].strip()
            body_start = idx + 1
            continue
        if not stripped:
            continue
        m = re.match(rf"^({'|'.join(META_KEYS)})\s*[:：]\s*(.*)$", stripped)
        if m and not stripped.startswith("#"):
            meta.append((m.group(1), m.group(2).strip().strip("`")))
            body_start = idx + 1
            continue
        if stripped.startswith("## "):
            body_start = idx
            break
        # Any other content line before the first section: stop scanning meta.
        if title != "Reading Notes":
            body_start = idx
            break

    body = "\n".join(lines[body_start:])
    return title, meta, body


def build_hero(title: str, meta: list[tuple[str, str]]) -> str:
    meta_map = {k: v for k, v in meta}
    source = meta_map.get("来源") or meta_map.get("Source")
    chips: list[str] = []
    for key, value in meta:
        if key in ("来源", "Source") or not value:
            continue
        icon, label = META_DISPLAY.get(key, ("•", key))
        display = value
        if key in ("阅读模式", "Reading mode"):
            display = MODE_LABELS.get(value, value)
        chips.append(
            f'<div class="stat"><span class="stat-ic">{icon}</span>'
            f'<span class="stat-body"><span class="stat-label">{html.escape(label)}</span>'
            f'<span class="stat-value">{html.escape(display)}</span></span></div>'
        )
    chips_html = "\n        ".join(chips)
    source_html = (
        f'<p class="source"><span>来源</span><code>{html.escape(source)}</code></p>'
        if source
        else ""
    )
    return f"""    <header class="hero">
      <p class="eyebrow">📚 读书加速 · 阅读笔记报告</p>
      <h1>{inline_markup(title)}</h1>
      {source_html}
      <div class="stats">
        {chips_html}
      </div>
    </header>"""


def build_sections(body: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Return (sections_html, toc[(id, icon, title)])."""
    id_iter = iter(collect_headings(body))

    lines = body.splitlines()
    sections_html: list[str] = []
    toc: list[tuple[str, str, str]] = []
    index = 0

    # Group lines into sections delimited by '## '.
    current_title = ""
    current_id = ""
    current_icon = ""
    current_hue = 205
    current_layout = "list"
    buffer: list[str] = []

    def flush_section() -> None:
        nonlocal buffer
        if not current_title:
            buffer = []
            return
        body_html = render_section_body(buffer, current_layout)
        sections_html.append(
            f'    <section id="{current_id}" class="block" style="--c: hsl({current_hue} 64% 45%);">\n'
            f'      <div class="block-head"><span class="block-ic">{current_icon}</span>'
            f'<span class="block-no">{index:02d}</span>'
            f'<h2>{inline_markup(current_title)}</h2></div>\n'
            f'      <div class="block-body">\n{body_html}\n      </div>\n'
            f"    </section>"
        )
        buffer = []

    for line in lines:
        if line.strip().startswith("## "):
            flush_section()
            index += 1
            section_id, title = next(id_iter)
            current_title = title
            current_id = section_id
            current_icon, current_hue, current_layout = section_theme(title)
            toc.append((section_id, current_icon, title))
        elif line.strip().startswith("# "):
            continue
        else:
            buffer.append(line)
    flush_section()

    return "\n".join(sections_html), toc


def build_html(markdown: str, title: str) -> str:
    parsed_title, meta, body = parse_document(markdown)
    if parsed_title and parsed_title != "Reading Notes":
        title = parsed_title
    hero = build_hero(title, meta)
    sections_html, toc = build_sections(body)
    toc_links = "\n".join(
        f'        <a href="#{section_id}" data-target="{section_id}">'
        f'<span class="toc-ic">{icon}</span><span class="toc-no">{i + 1:02d}</span>'
        f'<span class="toc-tx">{inline_markup(text)}</span></a>'
        for i, (section_id, icon, text) in enumerate(toc)
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --paper: #f7f4ec;
      --paper-2: #efe9dc;
      --ink: #211d16;
      --muted: #6c6253;
      --soft: #8c8273;
      --line: #e4ddcd;
      --card: #fffdf7;
      --accent: #c0492f;
      --accent-ink: #8a3120;
      --ok: #2f7d6b;
      --shadow: 0 18px 48px rgba(63, 52, 36, .12);
      --radius: 14px;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --paper: #14120d;
        --paper-2: #1a1711;
        --ink: #ece5d7;
        --muted: #a89e8d;
        --soft: #877d6c;
        --line: #2e2920;
        --card: #1d1a13;
        --accent: #e68363;
        --accent-ink: #f0a78d;
        --ok: #5cae9a;
        --shadow: 0 18px 48px rgba(0, 0, 0, .5);
      }}
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background:
        radial-gradient(120% 90% at 100% 0%, color-mix(in srgb, var(--accent) 7%, transparent), transparent 55%),
        linear-gradient(180deg, var(--paper) 0%, var(--paper-2) 100%);
      background-attachment: fixed;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
      line-height: 1.78;
      font-size: 16px;
      -webkit-font-smoothing: antialiased;
    }}
    #progress {{
      position: fixed; top: 0; left: 0; height: 3px; width: 0;
      background: linear-gradient(90deg, var(--accent), var(--ok));
      z-index: 50; transition: width .12s ease-out;
    }}
    .shell {{
      display: grid;
      grid-template-columns: minmax(210px, 264px) minmax(0, 820px);
      gap: 44px;
      width: min(1160px, calc(100% - 44px));
      margin: 0 auto;
      padding: 40px 0 80px;
    }}
    /* Sidebar */
    aside {{ position: sticky; top: 22px; align-self: start; max-height: calc(100vh - 44px); overflow-y: auto; }}
    aside .kicker {{
      font-size: 11px; font-weight: 800; letter-spacing: .16em; text-transform: uppercase;
      color: var(--accent-ink); margin: 6px 0 14px; padding-left: 10px;
    }}
    aside nav {{ display: flex; flex-direction: column; gap: 2px; }}
    aside a {{
      display: grid; grid-template-columns: 22px 26px 1fr; align-items: center; gap: 6px;
      padding: 7px 10px; border-radius: 9px; text-decoration: none; color: var(--muted);
      font-size: 13.5px; border-left: 2px solid transparent; transition: background .15s, color .15s;
    }}
    aside a .toc-no {{ font-variant-numeric: tabular-nums; font-size: 11px; color: var(--soft); }}
    aside a .toc-ic {{ font-size: 14px; }}
    aside a:hover {{ background: color-mix(in srgb, var(--accent) 9%, transparent); color: var(--ink); }}
    aside a.active {{
      background: color-mix(in srgb, var(--accent) 13%, transparent);
      color: var(--accent-ink); font-weight: 700; border-left-color: var(--accent);
    }}
    /* Main */
    main {{ min-width: 0; }}
    .hero {{
      background: var(--card); border: 1px solid var(--line); border-radius: var(--radius);
      box-shadow: var(--shadow); padding: clamp(26px, 4.5vw, 46px); position: relative; overflow: hidden;
    }}
    .hero::before {{
      content: ""; position: absolute; inset: 0 0 auto 0; height: 5px;
      background: linear-gradient(90deg, var(--accent), var(--ok));
    }}
    .eyebrow {{ margin: 6px 0 14px; font-size: 12.5px; font-weight: 700; letter-spacing: .04em; color: var(--accent-ink); }}
    .hero h1 {{
      margin: 0; font-family: Georgia, "Songti SC", "Noto Serif CJK SC", serif;
      font-size: clamp(30px, 5.2vw, 56px); line-height: 1.12; letter-spacing: -.01em;
    }}
    .source {{ margin: 16px 0 0; display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--soft); }}
    .source span {{ font-weight: 700; }}
    .source code {{ background: var(--paper-2); border: 1px solid var(--line); border-radius: 6px; padding: 2px 8px; word-break: break-all; }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }}
    .stat {{
      display: flex; align-items: center; gap: 11px; padding: 11px 15px; min-width: 132px;
      background: var(--paper); border: 1px solid var(--line); border-radius: 11px;
    }}
    .stat-ic {{ font-size: 19px; }}
    .stat-body {{ display: flex; flex-direction: column; line-height: 1.3; }}
    .stat-label {{ font-size: 11px; color: var(--soft); letter-spacing: .04em; }}
    .stat-value {{ font-size: 16px; font-weight: 700; }}
    /* Sections */
    .block {{ margin-top: 30px; }}
    .block-head {{ display: flex; align-items: center; gap: 12px; margin-bottom: 4px; }}
    .block-ic {{
      flex: none; width: 38px; height: 38px; display: grid; place-items: center; font-size: 19px;
      border-radius: 11px; background: color-mix(in srgb, var(--c) 15%, var(--card));
      border: 1px solid color-mix(in srgb, var(--c) 35%, var(--line));
    }}
    .block-no {{ font-variant-numeric: tabular-nums; font-weight: 800; font-size: 13px; color: var(--c); }}
    .block-head h2 {{
      margin: 0; font-family: Georgia, "Songti SC", "Noto Serif CJK SC", serif;
      font-size: clamp(20px, 2.6vw, 27px); line-height: 1.25; flex: 1;
    }}
    .block-body {{
      background: var(--card); border: 1px solid var(--line); border-radius: var(--radius);
      box-shadow: var(--shadow); padding: clamp(18px, 3vw, 28px); border-top: 3px solid var(--c);
    }}
    .block-body > :first-child {{ margin-top: 0; }}
    .block-body > :last-child {{ margin-bottom: 0; }}
    h3 {{ margin: 24px 0 10px; font-size: 17px; color: var(--accent-ink); }}
    p {{ margin: 13px 0; }}
    a {{ color: var(--accent-ink); }}
    code {{
      padding: 1px 6px; border: 1px solid var(--line); border-radius: 5px; background: var(--paper-2);
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .9em;
    }}
    pre {{ background: var(--paper-2); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; overflow-x: auto; }}
    pre code {{ border: 0; padding: 0; background: none; }}
    .quote {{ color: var(--accent-ink); font-weight: 600; }}
    strong {{ color: var(--ink); }}
    .embed {{ margin: 16px 0; text-align: center; }}
    .embed svg {{ max-width: 100%; height: auto; }}
    /* Plain lists */
    .block-body ul:not(.cardgrid):not(.grid9):not(.timeline) {{ list-style: none; padding-left: 0; margin: 12px 0; }}
    .block-body ul:not(.cardgrid):not(.grid9):not(.timeline) > li {{ position: relative; padding-left: 22px; margin: 9px 0; }}
    .block-body ul:not(.cardgrid):not(.grid9):not(.timeline) > li::before {{
      content: ""; position: absolute; left: 4px; top: 11px; width: 7px; height: 7px;
      border-radius: 2px; background: var(--c);
    }}
    ol {{ padding-left: 1.3rem; margin: 12px 0; }}
    ol li {{ margin: 8px 0; }}
    ol li::marker {{ color: var(--c); font-weight: 700; }}
    /* Card grids */
    .cardgrid {{ list-style: none; padding: 0; margin: 14px 0; display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }}
    .card {{
      display: flex; flex-direction: column; gap: 4px; padding: 14px 16px;
      background: var(--paper); border: 1px solid var(--line); border-radius: 11px;
      border-left: 3px solid var(--c); transition: transform .14s ease, box-shadow .14s ease, border-color .14s;
    }}
    .card:hover {{ transform: translateY(-2px); box-shadow: var(--shadow); border-left-color: var(--accent); }}
    .card .lead {{ font-weight: 800; color: var(--c); font-size: 14.5px; letter-spacing: .01em; }}
    .card .body {{ font-size: 14.5px; color: var(--ink); }}
    /* Nine-grid */
    .grid9 {{ list-style: none; padding: 0; margin: 14px 0; display: grid; gap: 10px; grid-template-columns: repeat(3, 1fr); }}
    .tile {{
      display: flex; flex-direction: column; gap: 6px; padding: 15px; min-height: 92px;
      background: linear-gradient(160deg, color-mix(in srgb, var(--c) 9%, var(--card)), var(--card));
      border: 1px solid color-mix(in srgb, var(--c) 24%, var(--line)); border-radius: 12px;
    }}
    .tile-key {{
      font-size: 10.5px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: var(--c);
    }}
    .tile-val {{ font-size: 14px; font-weight: 600; line-height: 1.5; }}
    /* Q&A */
    .qa {{
      padding: 15px 17px; margin: 12px 0; background: var(--paper); border: 1px solid var(--line);
      border-radius: 12px; border-left: 3px solid var(--c);
    }}
    .qa .question {{ margin: 0; font-weight: 700; display: flex; gap: 9px; align-items: baseline; }}
    .qa .answer {{ margin: 9px 0 0; color: var(--muted); display: flex; gap: 9px; align-items: baseline; }}
    .badge {{
      flex: none; width: 20px; height: 20px; display: inline-grid; place-items: center; border-radius: 6px;
      font-size: 11px; font-weight: 800; color: #fff;
    }}
    .badge.q {{ background: var(--c); }}
    .badge.a {{ background: var(--ok); }}
    /* Callout / pull-quote */
    .callout {{
      margin: 16px 0; padding: 15px 18px 15px 20px; border-radius: 12px;
      background: color-mix(in srgb, var(--c) 8%, var(--card));
      border: 1px solid color-mix(in srgb, var(--c) 22%, var(--line));
      border-left: 4px solid var(--c); font-size: 15.5px; color: var(--ink); line-height: 1.8;
    }}
    .callout.tip {{ --c: var(--ok); }}
    .callout.warn {{ --c: #c98a1e; }}
    .callout.key, .callout.quote {{
      font-family: Georgia, "Songti SC", "Noto Serif CJK SC", serif; font-size: 18px; font-style: italic;
    }}
    /* Timeline */
    .timeline {{ list-style: none; margin: 16px 0 6px; padding: 0 0 0 6px; position: relative; }}
    .timeline::before {{ content: ""; position: absolute; left: 11px; top: 6px; bottom: 6px; width: 2px; background: color-mix(in srgb, var(--c) 35%, var(--line)); }}
    .tl {{ position: relative; display: grid; grid-template-columns: 92px 1fr; gap: 14px; padding: 8px 0 8px 26px; align-items: baseline; }}
    .tl-dot {{ position: absolute; left: 5px; top: 14px; width: 13px; height: 13px; border-radius: 50%; background: var(--card); border: 3px solid var(--c); }}
    .tl-time {{ font-variant-numeric: tabular-nums; font-weight: 800; color: var(--c); font-size: 14px; }}
    .tl-event {{ font-size: 15px; }}
    /* Tables */
    .tablewrap {{ overflow-x: auto; margin: 16px 0; border: 1px solid var(--line); border-radius: 12px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 14.5px; }}
    thead th {{
      background: color-mix(in srgb, var(--c) 12%, var(--card)); color: var(--accent-ink);
      text-align: left; font-weight: 700; padding: 11px 14px; border-bottom: 2px solid color-mix(in srgb, var(--c) 30%, var(--line));
    }}
    tbody td {{ padding: 10px 14px; border-bottom: 1px solid var(--line); vertical-align: top; }}
    tbody tr:last-child td {{ border-bottom: 0; }}
    tbody tr:nth-child(even) {{ background: color-mix(in srgb, var(--c) 4%, transparent); }}
    footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--line); color: var(--soft); font-size: 12.5px; text-align: center; }}
    @media (max-width: 880px) {{
      .shell {{ display: block; width: min(100% - 26px, 760px); padding: 16px 0 48px; }}
      aside {{ position: static; max-height: none; margin-bottom: 18px; }}
      aside nav {{ flex-direction: row; flex-wrap: wrap; }}
      aside a {{ grid-template-columns: auto auto; }}
      aside a .toc-tx {{ display: none; }}
      .grid9 {{ grid-template-columns: 1fr; }}
      .tl {{ grid-template-columns: 72px 1fr; gap: 10px; }}
    }}
    @media print {{
      body {{ background: #fff; color: #000; }}
      #progress, aside {{ display: none; }}
      .shell {{ display: block; width: 100%; padding: 0; }}
      .hero, .block-body, .card, .tile, .qa {{ box-shadow: none; }}
      .block {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <div id="progress"></div>
  <div class="shell">
    <aside>
      <div class="kicker">目录 · Contents</div>
      <nav>
{toc_links}
      </nav>
    </aside>
    <main>
{hero}
{sections_html}
      <footer>本报告由 PDF Book Accelerator 自动生成 · 离线可读 · 支持打印与深浅色模式</footer>
    </main>
  </div>
  <script>
    (function () {{
      var bar = document.getElementById('progress');
      var links = Array.prototype.slice.call(document.querySelectorAll('aside a'));
      var map = {{}};
      links.forEach(function (a) {{ map[a.getAttribute('data-target')] = a; }});
      function onScroll() {{
        var h = document.documentElement;
        var max = h.scrollHeight - h.clientHeight;
        bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
      }}
      document.addEventListener('scroll', onScroll, {{ passive: true }});
      onScroll();
      if ('IntersectionObserver' in window) {{
        var obs = new IntersectionObserver(function (entries) {{
          entries.forEach(function (e) {{
            if (e.isIntersecting) {{
              links.forEach(function (a) {{ a.classList.remove('active'); }});
              var a = map[e.target.id];
              if (a) a.classList.add('active');
            }}
          }});
        }}, {{ rootMargin: '-12% 0px -75% 0px', threshold: 0 }});
        document.querySelectorAll('section.block').forEach(function (s) {{ obs.observe(s); }});
      }}
    }})();
  </script>
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
