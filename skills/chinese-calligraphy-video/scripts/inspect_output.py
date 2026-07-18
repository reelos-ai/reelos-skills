#!/usr/bin/env python3
"""用 ffprobe 检查成片流信息，并可与项目配置比对。"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


VIDEO_CODEC_NAMES = {"libx264": "h264", "libx265": "hevc"}


def expected_duration(config: dict) -> float:
    total = float(config.get("intro_seconds", 0.5))
    default_build = float(config.get("line_build_seconds", 1.6))
    default_hold = float(config.get("line_hold_seconds", 2.3))
    default_gap = float(config.get("gap_seconds", 0.35))
    last_gap = default_gap
    for line in config.get("lines", []):
        total += float(line.get("build_seconds", default_build))
        total += float(line.get("hold_seconds", default_hold))
        last_gap = float(line.get("gap_seconds", default_gap))
        total += last_gap
    return total - last_gap + float(config.get("outro_seconds", 1.0))


def probe(path: Path) -> dict:
    if shutil.which("ffprobe") is None:
        raise RuntimeError("未找到 ffprobe")
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_name,codec_type,width,height,pix_fmt,r_frame_rate,sample_rate,channels",
        "-show_entries", "format=duration,size", "-of", "json", str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe 失败")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="检查中国诗词书法视频成片")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()
    video_path = args.input.resolve()
    if not video_path.exists():
        print(f"成片不存在: {video_path}")
        return 1
    data = probe(video_path)
    streams = data.get("streams", [])
    video = next((item for item in streams if item.get("codec_type") == "video"), None)
    audio = next((item for item in streams if item.get("codec_type") == "audio"), None)
    errors: list[str] = []
    if not video:
        errors.append("缺少视频流")
    if args.config:
        config = json.loads(args.config.resolve().read_text(encoding="utf-8"))
        encoding = config.get("encoding", {})
        if video:
            if int(video.get("width", 0)) != int(config["width"]) or int(video.get("height", 0)) != int(config["height"]):
                errors.append("成片分辨率与配置不一致")
            rate = float(Fraction(video.get("r_frame_rate", "0/1")))
            if abs(rate - float(config["fps"])) > 0.01:
                errors.append("成片帧率与配置不一致")
            expected_pixel_format = str(config.get("encoding", {}).get("pixel_format", "yuv420p"))
            if video.get("pix_fmt") != expected_pixel_format:
                errors.append(f"像素格式不一致: {video.get('pix_fmt')} != {expected_pixel_format}")
            configured_codec = str(encoding.get("video_codec", "libx264"))
            expected_codec = VIDEO_CODEC_NAMES.get(configured_codec, configured_codec)
            if video.get("codec_name") != expected_codec:
                errors.append(f"视频编码不一致: {video.get('codec_name')} != {expected_codec}")
        expects_audio = any(line.get("audio") for line in config.get("lines", []))
        if expects_audio and not audio:
            errors.append("配置包含音频，但成片缺少音频流")
        if not expects_audio and audio:
            errors.append("配置为无声，但成片包含音频流")
        if expects_audio and audio:
            expected_audio_codec = str(encoding.get("audio_codec", "aac"))
            if audio.get("codec_name") != expected_audio_codec:
                errors.append(f"音频编码不一致: {audio.get('codec_name')} != {expected_audio_codec}")
            expected_sample_rate = int(encoding.get("audio_sample_rate", 48000))
            if int(audio.get("sample_rate", 0)) != expected_sample_rate:
                errors.append(f"音频采样率不一致: {audio.get('sample_rate')} != {expected_sample_rate}")
        actual_duration = float(data.get("format", {}).get("duration", 0))
        target_duration = expected_duration(config)
        tolerance = 1 / max(1, int(config["fps"])) + 0.02
        if abs(actual_duration - target_duration) > tolerance:
            errors.append(f"成片时长与配置不一致: {actual_duration:.3f}s != {target_duration:.3f}s")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    if errors:
        print("\n成片检查失败:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\n成片检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
