#!/usr/bin/env python3
"""校验书法视频配置、透明母版、背景和分句音频。"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


REVEAL_STYLES = {"character-wipe", "line-wipe", "fade"}


def validate_rgba(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"缺少书法素材: {path}"]
    with Image.open(path) as image:
        if image.mode != "RGBA":
            return [f"{path}: 必须是 RGBA，当前为 {image.mode}"]
        alpha = image.getchannel("A")
        low, high = alpha.getextrema()
        if low != 0:
            errors.append(f"{path}: 没有透明背景")
        if high == 0:
            errors.append(f"{path}: 图像完全透明")
        corners = ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1))
        if any(alpha.getpixel(point) != 0 for point in corners):
            errors.append(f"{path}: 至少一个角落不透明")
        bbox = alpha.getbbox()
        if bbox is None or bbox[2] - bbox[0] < image.width * 0.3:
            errors.append(f"{path}: 有效书法区域过小")
    return errors


def audio_duration(path: Path) -> float | None:
    if shutil.which("ffprobe") is None:
        return None
    command = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return -1
    try:
        return float(result.stdout.strip())
    except ValueError:
        return -1


def main() -> int:
    parser = argparse.ArgumentParser(description="校验中国诗词书法视频项目")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config_path = args.config.resolve()
    base = config_path.parent
    errors: list[str] = []
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"配置读取失败: {exc}")
        return 1

    schema_version = config.get("schema_version", 1)
    if schema_version != 1:
        errors.append(f"不支持的 schema_version: {schema_version}")
    for field in ("width", "height", "fps", "lines"):
        if field not in config:
            errors.append(f"配置缺少字段: {field}")
    if errors:
        for error in errors:
            print(f"✗ {error}")
        return 1
    if not isinstance(config["lines"], list) or not config["lines"]:
        print("✗ lines 必须是非空数组")
        return 1
    if int(config["width"]) < 128 or int(config["height"]) < 128:
        errors.append("width/height 至少为 128")
    if int(config["fps"]) < 1:
        errors.append("fps 至少为 1")

    background = config.get("background_asset")
    if background and not (base / background).exists():
        errors.append(f"缺少背景素材: {base / background}")

    default_build = float(config.get("line_build_seconds", 1.6))
    default_hold = float(config.get("line_hold_seconds", 2.3))
    default_gap = float(config.get("gap_seconds", 0.35))
    default_lead = float(config.get("tts_lead_seconds", 0.3))
    default_reveal = str(config.get("reveal_style", "character-wipe"))
    if default_reveal not in REVEAL_STYLES:
        errors.append(f"不支持的 reveal_style: {default_reveal}")
    background_dim = float(config.get("background_dim", 0.0))
    if not 0 <= background_dim <= 1:
        errors.append("background_dim 必须在 0 到 1 之间")
    encoding = config.get("encoding", {})
    if not isinstance(encoding, dict):
        errors.append("encoding 必须是对象")
        encoding = {}
    crf = int(encoding.get("crf", 18))
    if not 0 <= crf <= 63:
        errors.append("encoding.crf 必须在 0 到 63 之间")
    audio_sample_rate = int(encoding.get("audio_sample_rate", 48000))
    if audio_sample_rate < 8000:
        errors.append("encoding.audio_sample_rate 不能低于 8000")

    for index, line in enumerate(config["lines"], start=1):
        text = line.get("text", "")
        asset = line.get("asset")
        if not text:
            errors.append(f"第 {index} 句缺少 text")
        if not asset:
            errors.append(f"第 {index} 句缺少 asset")
        else:
            errors.extend(validate_rgba(base / asset))
        build = float(line.get("build_seconds", default_build))
        hold = float(line.get("hold_seconds", default_hold))
        gap = float(line.get("gap_seconds", default_gap))
        lead = float(line.get("tts_lead_seconds", default_lead))
        scale = float(line.get("scale", 1.0))
        reveal = str(line.get("reveal_style", default_reveal))
        if build <= 0 or hold < 0 or gap < 0 or lead < 0:
            errors.append(f"第 {index} 句时间参数无效")
        if not 0.1 <= scale <= 2.0:
            errors.append(f"第 {index} 句 scale 必须在 0.1 到 2.0 之间")
        if int(line.get("max_width", config.get("max_line_width", config["width"]))) < 1:
            errors.append(f"第 {index} 句 max_width 必须大于 0")
        if int(line.get("max_height", config.get("max_line_height", config["height"]))) < 1:
            errors.append(f"第 {index} 句 max_height 必须大于 0")
        if reveal not in REVEAL_STYLES:
            errors.append(f"第 {index} 句不支持的 reveal_style: {reveal}")
        audio = line.get("audio")
        if audio:
            audio_path = base / audio
            if not audio_path.exists():
                errors.append(f"缺少音频: {audio_path}")
            else:
                duration = audio_duration(audio_path)
                if duration == -1:
                    errors.append(f"音频无法解析: {audio_path}")
                elif duration is not None:
                    print(f"✓ 第 {index} 句音频 {duration:.2f}s: {audio_path.name}")
                    outro = float(config.get("outro_seconds", 1.0))
                    tail = outro if index == len(config["lines"]) else gap
                    available = build + hold + tail - lead
                    if duration > available:
                        errors.append(
                            f"第 {index} 句音频 {duration:.2f}s 超出镜头可用时间 {available:.2f}s"
                        )
        if asset and (base / asset).exists():
            print(f"✓ 第 {index} 句书法: {text}")

    if shutil.which("ffmpeg") is None:
        errors.append("系统未安装 ffmpeg")
    if shutil.which("ffprobe") is None:
        errors.append("系统未安装 ffprobe")
    if errors:
        print("\n校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\n项目结构与素材校验通过。仍需人工逐字检查书法内容。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
