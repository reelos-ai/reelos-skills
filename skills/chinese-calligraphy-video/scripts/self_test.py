#!/usr/bin/env python3
"""在临时目录执行初始化、校验、三种显影、混音、编码与成片检查。"""

from __future__ import annotations

import json
import copy
import math
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

from PIL import Image, ImageDraw


SCRIPTS = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS.parent


def run(script: str, *args: str) -> None:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run([sys.executable, str(SCRIPTS / script), *args], check=True, env=environment)


def make_audio(path: Path, frequency: float) -> None:
    sample_rate = 16000
    duration = 0.18
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        frames = bytearray()
        for index in range(round(sample_rate * duration)):
            value = round(5000 * math.sin(2 * math.pi * frequency * index / sample_rate))
            frames.extend(int(value).to_bytes(2, "little", signed=True))
        handle.writeframes(bytes(frames))


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="calligraphy-video-self-test-") as raw:
        root = Path(raw)
        line_dir = root / "assets" / "lines" / "self-test"
        audio_dir = root / "assets" / "audio"
        background_dir = root / "assets" / "backgrounds"
        preview_dir = root / "previews"
        for directory in (line_dir, audio_dir, background_dir, preview_dir):
            directory.mkdir(parents=True, exist_ok=True)

        background = Image.new("RGB", (320, 180), (12, 18, 24))
        ImageDraw.Draw(background).rectangle((0, 145, 320, 180), fill=(30, 65, 58))
        background.save(background_dir / "background.png")
        colors = ((210, 195, 235, 255), (70, 130, 120, 255), (180, 210, 225, 255))
        for index, color in enumerate(colors, start=1):
            line = Image.new("RGBA", (260, 90), (0, 0, 0, 0))
            draw = ImageDraw.Draw(line)
            draw.rounded_rectangle((20, 18, 240, 72), radius=12, fill=color)
            draw.ellipse((220, 8, 248, 36), fill=color)
            line.save(line_dir / f"line_{index:02d}.png")
            make_audio(audio_dir / f"line_{index:02d}.wav", 220 + index * 55)

        config = {
            "schema_version": 1,
            "variant": "self-test",
            "width": 320,
            "height": 180,
            "fps": 6,
            "background_asset": "assets/backgrounds/background.png",
            "background_dim": 0.1,
            "title": "《自测》",
            "author": "Skill",
            "badge": "愿君全屏静赏",
            "line_build_seconds": 0.25,
            "line_hold_seconds": 0.3,
            "gap_seconds": 0.1,
            "intro_seconds": 0.1,
            "outro_seconds": 0.2,
            "tts_lead_seconds": 0.05,
            "max_line_width": 260,
            "max_line_height": 90,
            "encoding": {"preset": "ultrafast", "crf": 28},
            "lines": [
                {"text": "一", "asset": "assets/lines/self-test/line_01.png", "audio": "assets/audio/line_01.wav", "reveal_style": "character-wipe"},
                {"text": "二", "asset": "assets/lines/self-test/line_02.png", "audio": "assets/audio/line_02.wav", "reveal_style": "line-wipe", "x_offset": 4},
                {"text": "三", "asset": "assets/lines/self-test/line_03.png", "audio": "assets/audio/line_03.wav", "reveal_style": "fade", "scale": 0.9},
            ],
        }
        config_path = root / "video_config.json"
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest = json.loads((SKILL_DIR / "assets" / "design_manifest.example.json").read_text(encoding="utf-8"))
        second_direction = copy.deepcopy(manifest["directions"][0])
        second_direction.update({
            "id": "direction-c",
            "name": "静墨留白",
            "taste_thesis": "用更静的墨色留白测试候选方向的完整性",
            "dominant_aesthetic": "墨色极简",
            "supporting_signals": ["纸本肌理"],
        })
        manifest["directions"].append(second_direction)
        manifest_path = root / "design_manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        output = root / "outputs" / "self-test.mp4"
        run("audit_design.py", "--manifest", str(manifest_path))
        run("validate_project.py", "--config", str(config_path))
        run("compose_video.py", "--config", str(config_path), "--preview", str(preview_dir / "preview.png"))
        run("make_contact_sheet.py", "--config", str(config_path), "--output", str(preview_dir / "contact.png"), "--thumb-width", "320")
        run("compose_video.py", "--config", str(config_path), "--output", str(output))
        run("inspect_output.py", "--input", str(output), "--config", str(config_path))
        print("Skill 全链路自测通过。")


if __name__ == "__main__":
    main()
