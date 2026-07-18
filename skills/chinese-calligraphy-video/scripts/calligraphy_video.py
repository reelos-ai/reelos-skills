#!/usr/bin/env python3
"""中国诗词书法视频 Skill 的统一命令行入口。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent
COMMANDS = {
    "init": "init_project.py",
    "design-audit": "audit_design.py",
    "validate": "validate_project.py",
    "contact": "make_contact_sheet.py",
    "render": "compose_video.py",
    "inspect": "inspect_output.py",
    "self-test": "self_test.py",
}


HELP = """中国诗词书法视频统一 CLI

用法:
  calligraphy_video.py init --project-dir DIR --line TEXT [--line TEXT ...]
  calligraphy_video.py design-audit --manifest DESIGN_MANIFEST.json
  calligraphy_video.py validate --config CONFIG
  calligraphy_video.py preview --config CONFIG --output PREVIEW.png
  calligraphy_video.py contact --config CONFIG --output CONTACT.png
  calligraphy_video.py render --config CONFIG --output VIDEO.mp4
  calligraphy_video.py inspect --input VIDEO.mp4 [--config CONFIG]
  calligraphy_video.py self-test
"""


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"}:
        print(HELP)
        return 0
    command = sys.argv[1]
    forwarded = sys.argv[2:]
    if command == "preview":
        if "--output" not in forwarded:
            print("preview 必须提供 --output PREVIEW.png", file=sys.stderr)
            return 2
        output_index = forwarded.index("--output")
        forwarded[output_index] = "--preview"
        script = "compose_video.py"
    elif command in COMMANDS:
        script = COMMANDS[command]
    else:
        print(f"未知命令: {command}\n\n{HELP}", file=sys.stderr)
        return 2
    result = subprocess.run([sys.executable, str(SCRIPTS / script), *forwarded], check=False)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
