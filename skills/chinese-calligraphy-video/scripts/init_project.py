#!/usr/bin/env python3
"""初始化可移植的中国诗词书法视频项目结构。"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "video_config.example.json"
REQUIREMENTS = SKILL_DIR / "assets" / "requirements.txt"
DESIGN_TEMPLATE = SKILL_DIR / "assets" / "design_manifest.example.json"


def create_project(
    target: Path,
    *,
    title: str,
    author: str,
    lines: list[str],
    variant: str,
    width: int,
    height: int,
    fps: int,
    silent: bool,
) -> list[Path]:
    target = target.resolve()
    if width < 128 or height < 128 or fps < 1:
        raise ValueError("width/height 至少为 128，fps 至少为 1")
    if not variant or any(part in variant for part in ("/", "\\", "..")):
        raise ValueError("variant 必须是单一安全目录名")
    if not lines or any(not line.strip() for line in lines):
        raise ValueError("至少提供一句非空文本")

    config_path = target / "video_config.json"
    requirements_path = target / "requirements.txt"
    design_path = target / "design_manifest.json"
    if config_path.exists():
        raise FileExistsError(f"配置已存在，不会覆盖: {config_path}")

    directories = (
        target / "assets" / "backgrounds",
        target / "assets" / "lines" / variant / "source",
        target / "assets" / "audio",
        target / "previews",
        target / "outputs",
    )
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    config = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    config.update({
        "schema_version": 1,
        "variant": variant,
        "width": width,
        "height": height,
        "fps": fps,
        "title": title,
        "author": author,
    })
    config["lines"] = []
    for index, text in enumerate(lines, start=1):
        item = {
            "text": text,
            "asset": f"assets/lines/{variant}/line_{index:02d}.png",
        }
        if not silent:
            item["audio"] = f"assets/audio/line_{index:02d}.mp3"
        config["lines"].append(item)

    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    created = [config_path, *directories]
    if not requirements_path.exists():
        shutil.copy2(REQUIREMENTS, requirements_path)
        created.append(requirements_path)
    if not design_path.exists():
        design = json.loads(DESIGN_TEMPLATE.read_text(encoding="utf-8"))
        design["source"].update({"title": title, "author": author, "lines": lines})
        design_path.write_text(json.dumps(design, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created.append(design_path)
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="初始化中国诗词书法视频项目")
    parser.add_argument("--project-dir", type=Path, required=True)
    parser.add_argument("--title", default="《诗名》")
    parser.add_argument("--author", default="朝代 · 作者")
    parser.add_argument("--line", action="append", dest="lines", required=True, help="可重复传入")
    parser.add_argument("--variant", default="default")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--silent", action="store_true", help="不预配置分句音频路径")
    args = parser.parse_args()
    created = create_project(
        args.project_dir,
        title=args.title,
        author=args.author,
        lines=args.lines,
        variant=args.variant,
        width=args.width,
        height=args.height,
        fps=args.fps,
        silent=args.silent,
    )
    print("项目已初始化:")
    for path in created:
        print(f"- {path}")


if __name__ == "__main__":
    main()
