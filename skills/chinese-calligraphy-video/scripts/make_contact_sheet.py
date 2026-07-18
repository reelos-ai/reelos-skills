#!/usr/bin/env python3
"""从配置直接渲染每句完整停留帧并生成联系表。"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw

from compose_video import build_scenes, load_config, load_font, render_frame


def main() -> None:
    parser = argparse.ArgumentParser(description="生成每句完整停留帧联系表")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--thumb-width", type=int, default=960)
    args = parser.parse_args()
    if args.columns < 1 or args.thumb_width < 320:
        raise ValueError("columns 至少为 1，thumb-width 至少为 320")

    config, base = load_config(args.config)
    scenes, _ = build_scenes(config, base)
    source_width, source_height = int(config["width"]), int(config["height"])
    thumb_height = round(args.thumb_width * source_height / source_width)
    label_height = 42
    rows = math.ceil(len(scenes) / args.columns)
    sheet = Image.new("RGB", (args.columns * args.thumb_width, rows * (thumb_height + label_height)), (18, 18, 18))
    draw = ImageDraw.Draw(sheet)
    font = load_font(24)

    for index, scene in enumerate(scenes):
        t = scene.build_end + (scene.hold_end - scene.build_end) * 0.5
        frame = render_frame(t, config, scenes).resize((args.thumb_width, thumb_height), Image.Resampling.LANCZOS)
        column, row = index % args.columns, index // args.columns
        x, y = column * args.thumb_width, row * (thumb_height + label_height)
        sheet.paste(frame, (x, y))
        draw.text((x + 14, y + thumb_height + 12), f"{index + 1:02d}  {scene.text}", fill=(230, 230, 230), font=font)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"联系表已保存: {args.output.resolve()}")


if __name__ == "__main__":
    main()
