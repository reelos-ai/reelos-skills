#!/usr/bin/env python3
"""把透明书法母版、背景和分句音频合成为逐字显影视频。"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


FONT_CANDIDATES = (
    Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"),
)


@dataclass(frozen=True)
class Scene:
    text: str
    asset: Image.Image
    start: float
    build_end: float
    hold_end: float
    reveal_style: str
    x_offset: int
    y_offset: int
    line_scale: float
    tts_lead: float


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def ease_out_cubic(value: float) -> float:
    value = clamp(value)
    return 1.0 - (1.0 - value) ** 3


def rgba(value: list[int] | tuple[int, ...], default_alpha: int) -> tuple[int, int, int, int]:
    color = tuple(int(part) for part in value)
    if len(color) == 3:
        color += (default_alpha,)
    if len(color) != 4:
        raise ValueError(f"颜色必须是 RGB 或 RGBA: {value}")
    return color


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if path.exists():
            return ImageFont.truetype(str(path), size, index=0)
    return ImageFont.load_default()


def prepare_background(path: Path, width: int, height: int) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"缺少背景素材: {path}")
    image = Image.open(path).convert("RGBA")
    scale = max(width / image.width, height / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    image = image.resize(size, Image.Resampling.LANCZOS)
    left = max(0, (image.width - width) // 2)
    top = max(0, (image.height - height) // 2)
    return image.crop((left, top, left + width, top + height))


def prepare_line(path: Path, max_width: int, max_height: int) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"缺少书法素材: {path}")
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"素材完全透明: {path}")
    image = image.crop(bbox)
    scale = min(max_width / image.width, max_height / image.height, 1.0)
    if scale < 1.0:
        size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
        image = image.resize(size, Image.Resampling.LANCZOS)
    return image


def load_config(path: Path) -> tuple[dict, Path]:
    config_path = path.resolve()
    base = config_path.parent
    config = json.loads(config_path.read_text(encoding="utf-8"))
    missing = {"width", "height", "fps", "lines"}.difference(config)
    if missing:
        raise ValueError(f"配置缺少字段: {', '.join(sorted(missing))}")
    if not config["lines"]:
        raise ValueError("配置至少需要一句文本")
    background_asset = config.get("background_asset")
    if background_asset:
        config["_background_image"] = prepare_background(
            base / background_asset, int(config["width"]), int(config["height"])
        )
    return config, base


def build_scenes(config: dict, base: Path) -> tuple[list[Scene], float]:
    cursor = float(config.get("intro_seconds", 0.5))
    default_build = float(config.get("line_build_seconds", 1.6))
    default_hold = float(config.get("line_hold_seconds", 2.3))
    default_gap = float(config.get("gap_seconds", 0.35))
    default_lead = float(config.get("tts_lead_seconds", 0.3))
    default_reveal = str(config.get("reveal_style", "character-wipe"))
    max_width = int(config.get("max_line_width", config["width"] * 0.88))
    max_height = int(config.get("max_line_height", config["height"] * 0.6))
    scenes: list[Scene] = []
    last_gap = default_gap
    for line in config["lines"]:
        line_max_width = int(line.get("max_width", max_width))
        line_max_height = int(line.get("max_height", max_height))
        asset = prepare_line(base / line["asset"], line_max_width, line_max_height)
        build_seconds = float(line.get("build_seconds", default_build))
        hold_seconds = float(line.get("hold_seconds", default_hold))
        gap_seconds = float(line.get("gap_seconds", default_gap))
        build_end = cursor + build_seconds
        hold_end = build_end + hold_seconds
        scenes.append(Scene(
            text=line["text"],
            asset=asset,
            start=cursor,
            build_end=build_end,
            hold_end=hold_end,
            reveal_style=str(line.get("reveal_style", default_reveal)),
            x_offset=int(line.get("x_offset", 0)),
            y_offset=int(line.get("y_offset", 0)),
            line_scale=float(line.get("scale", 1.0)),
            tts_lead=float(line.get("tts_lead_seconds", default_lead)),
        ))
        cursor = hold_end + gap_seconds
        last_gap = gap_seconds
    total = cursor - last_gap + float(config.get("outro_seconds", 1.0))
    return scenes, total


def line_wipe_mask(asset: Image.Image, progress: float) -> Image.Image:
    width, height = asset.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    frontier = width * ease_out_cubic(progress)
    step = max(4, height // 64)
    boundary = []
    for y in range(0, height + step, step):
        jitter = 12 * math.sin(y * 0.047) + 5 * math.sin(y * 0.131)
        boundary.append((round(frontier + jitter), min(y, height)))
    draw.polygon([(0, 0), *boundary, (0, height)], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(1.15))


def reveal_mask(asset: Image.Image, text: str, progress: float, style: str) -> Image.Image:
    width, height = asset.size
    if style == "fade":
        return Image.new("L", (width, height), round(255 * ease_out_cubic(progress)))
    if style == "line-wipe":
        return line_wipe_mask(asset, progress)
    if style != "character-wipe":
        raise ValueError(f"不支持的 reveal_style: {style}")
    count = max(1, len(text))
    stagger = 0.62 / count
    duration = 1.0 - stagger * (count - 1)
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    step = max(4, height // 64)
    for index in range(count):
        local = ease_out_cubic((progress - index * stagger) / max(duration, 0.001))
        if local <= 0:
            continue
        left = round(index * width / count)
        right = round((index + 1) * width / count)
        frontier = left + (right - left) * local
        boundary = []
        for y in range(0, height + step, step):
            jitter = 10 * math.sin(y * 0.047 + index * 1.9)
            jitter += 5 * math.sin(y * 0.131 + index * 0.7)
            boundary.append((round(frontier + jitter), min(y, height)))
        draw.polygon([(left, 0), *boundary, (left, height)], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(1.15))


def apply_reveal(asset: Image.Image, text: str, progress: float, style: str) -> Image.Image:
    result = asset.copy()
    result.putalpha(ImageChops.multiply(asset.getchannel("A"), reveal_mask(asset, text, progress, style)))
    return result


def draw_labels(frame: Image.Image, config: dict) -> None:
    draw = ImageDraw.Draw(frame)
    width, height = frame.size
    info_font = load_font(max(22, height // 38))
    badge_font = load_font(max(20, height // 45))
    info_color = rgba(config.get("info_color", [150, 22, 40, 235]), 235)
    badge_color = rgba(config.get("badge_color", [190, 180, 230, 230]), 230)
    info = f'{config.get("title", "")} {config.get("author", "")}'.strip()
    if info:
        box = draw.textbbox((0, 0), info, font=info_font)
        draw.text((width - (box[2] - box[0]) - 58, height - 74), info, font=info_font, fill=info_color)
    badge = config.get("badge", "")
    if badge:
        box = draw.textbbox((0, 0), badge, font=badge_font)
        badge_box = (48, height - 92, 76 + box[2], height - 42)
        draw.rounded_rectangle(badge_box, radius=5, outline=badge_color, width=1)
        draw.text((61, height - 82), badge, font=badge_font, fill=badge_color)


def render_frame(t: float, config: dict, scenes: list[Scene]) -> Image.Image:
    width, height = int(config["width"]), int(config["height"])
    if "_background_image" in config:
        frame = config["_background_image"].copy()
    else:
        background = tuple(config.get("background", [0, 0, 0]))
        frame = Image.new("RGBA", (width, height), background + (255,))
    background_dim = clamp(float(config.get("background_dim", 0.0)))
    if background_dim > 0:
        frame.alpha_composite(Image.new("RGBA", frame.size, (0, 0, 0, round(255 * background_dim))))
    active = next((scene for scene in scenes if scene.start <= t <= scene.hold_end), None)
    if active:
        duration = active.build_end - active.start
        progress = clamp((t - active.start) / max(duration, 0.001))
        revealed = apply_reveal(active.asset, active.text, progress, active.reveal_style)
        scale = active.line_scale * (0.975 + 0.025 * ease_out_cubic(progress))
        if scale < 0.999:
            size = (max(1, round(revealed.width * scale)), max(1, round(revealed.height * scale)))
            revealed = revealed.resize(size, Image.Resampling.LANCZOS)
        elif scale > 1.001:
            size = (max(1, round(revealed.width * scale)), max(1, round(revealed.height * scale)))
            revealed = revealed.resize(size, Image.Resampling.LANCZOS)
        x = (width - revealed.width) // 2 + active.x_offset
        y = (height - revealed.height) // 2 - round(height * 0.025) + active.y_offset
        frame.alpha_composite(revealed, (x, y))
    draw_labels(frame, config)
    return frame.convert("RGB")


def mix_audio(config: dict, base: Path, scenes: list[Scene], duration: float, video: Path, output: Path) -> None:
    command = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video)]
    filters: list[str] = []
    labels: list[str] = []
    encoding = config.get("encoding", {})
    audio_index = 1
    for scene, line in zip(scenes, config["lines"]):
        audio = line.get("audio")
        if not audio:
            continue
        path = base / audio
        if not path.exists():
            raise FileNotFoundError(f"缺少 TTS 音频: {path}")
        command.extend(["-i", str(path)])
        delay = max(0, round((scene.start + scene.tts_lead) * 1000))
        label = f"a{audio_index}"
        filters.append(f"[{audio_index}:a]adelay={delay}:all=1[{label}]")
        labels.append(f"[{label}]")
        audio_index += 1
    filters.append(
        f'{"".join(labels)}amix=inputs={len(labels)}:duration=longest:normalize=0,'
        f"volume=0.95,apad=pad_dur={duration:.3f}[aout]"
    )
    command.extend([
        "-filter_complex", ";".join(filters), "-map", "0:v:0", "-map", "[aout]",
        "-c:v", "copy", "-c:a", str(encoding.get("audio_codec", "aac")),
        "-b:a", str(encoding.get("audio_bitrate", "192k")),
        "-ar", str(encoding.get("audio_sample_rate", 48000)),
        "-t", f"{duration:.3f}", "-movflags", "+faststart", str(output),
    ])
    subprocess.run(command, check=True)


def encode(config: dict, base: Path, scenes: list[Scene], duration: float, output: Path) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("未找到 ffmpeg")
    width, height, fps = int(config["width"]), int(config["height"]), int(config["fps"])
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    has_audio = any(line.get("audio") for line in config["lines"])
    encoding = config.get("encoding", {})
    silent = output.with_name(f"{output.stem}.silent.tmp{output.suffix}") if has_audio else output
    command = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}", "-r", str(fps), "-i", "pipe:0",
        "-c:v", str(encoding.get("video_codec", "libx264")),
        "-preset", str(encoding.get("preset", "medium")),
        "-crf", str(encoding.get("crf", 18)),
        "-pix_fmt", str(encoding.get("pixel_format", "yuv420p")),
        "-movflags", "+faststart", str(silent),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    total_frames = math.ceil(duration * fps)
    try:
        for index in range(total_frames):
            process.stdin.write(render_frame(index / fps, config, scenes).tobytes())
            if (index + 1) % fps == 0:
                print(f"已渲染 {index + 1}/{total_frames} 帧")
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("ffmpeg 视频编码失败")
    if has_audio:
        mix_audio(config, base, scenes, duration, silent, output)
        silent.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="合成中国诗词书法视频")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("output.mp4"))
    parser.add_argument("--preview", type=Path, help="仅输出第一句显影中段预览")
    args = parser.parse_args()
    config, base = load_config(args.config)
    scenes, duration = build_scenes(config, base)
    if args.preview:
        t = scenes[0].start + (scenes[0].build_end - scenes[0].start) * 0.58
        preview = render_frame(t, config, scenes)
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        preview.save(args.preview)
        print(f"预览图已保存: {args.preview.resolve()}")
        return
    encode(config, base, scenes, duration, args.output)
    print(f"视频已保存: {args.output.resolve()}")


if __name__ == "__main__":
    main()
