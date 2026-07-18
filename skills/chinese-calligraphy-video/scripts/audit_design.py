#!/usr/bin/env python3
"""审计书法视频的内容分析、创意方向、评分与配色对比度。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


WEIGHTS = {
    "content_fit": 25,
    "cultural_coherence": 15,
    "calligraphy_legibility": 15,
    "palette_light": 15,
    "composition_space": 10,
    "motion_rhythm": 10,
    "audio_fit": 10,
}
CRITICAL = {"content_fit", "cultural_coherence", "calligraphy_legibility"}
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def require_text(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"缺少有效文本: {label}")


def require_object(value: object, label: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{label} 必须是对象")
        return {}
    return value


def relative_luminance(color: str) -> float:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    high, low = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def score_direction(direction: dict, critical_minimum: float, errors: list[str]) -> float:
    scores = require_object(direction.get("scores"), "direction.scores", errors)
    total = 0.0
    for key, weight in WEIGHTS.items():
        value = scores.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 1 <= value <= 5:
            errors.append(f"scores.{key} 必须在 1 到 5 之间")
            continue
        if key in CRITICAL and value < critical_minimum:
            errors.append(f"关键项 scores.{key}={value} 低于门槛 {critical_minimum}")
        total += float(value) / 5 * weight
    return total


def audit(manifest: dict) -> tuple[list[str], float, dict]:
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("schema_version 必须为 1")
    source = require_object(manifest.get("source"), "source", errors)
    require_text(source.get("title"), "source.title", errors)
    require_text(source.get("author"), "source.author", errors)
    lines = source.get("lines")
    if not isinstance(lines, list) or not lines or any(not isinstance(line, str) or not line.strip() for line in lines):
        errors.append("source.lines 必须是非空文本数组")
    if source.get("text_integrity") not in {"confirmed", "user-provided"}:
        errors.append("source.text_integrity 必须为 confirmed 或 user-provided")

    analysis = require_object(manifest.get("content_analysis"), "content_analysis", errors)
    for field in ("genre", "theme", "time_space", "rhythm", "cultural_logic"):
        require_text(analysis.get(field), f"content_analysis.{field}", errors)
    for field in ("imagery", "emotional_arc", "light_material", "evidence"):
        value = analysis.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"content_analysis.{field} 必须是非空数组")
    for index, item in enumerate(analysis.get("evidence", []) if isinstance(analysis.get("evidence"), list) else [], start=1):
        if not isinstance(item, dict) or item.get("confidence") not in {"observed", "provided", "inferred"}:
            errors.append(f"content_analysis.evidence[{index}] 的 confidence 无效")

    directions = manifest.get("directions")
    if not isinstance(directions, list) or not 2 <= len(directions) <= 3:
        errors.append("directions 必须包含 2 到 3 个候选方向")
        directions = []
    direction_map = {item.get("id"): item for item in directions if isinstance(item, dict) and item.get("id")}
    selection = require_object(manifest.get("selection"), "selection", errors)
    selected_id = selection.get("selected_direction_id")
    selected = direction_map.get(selected_id, {})
    if not selected:
        errors.append("selection.selected_direction_id 未指向有效方向")
    minimum_score = selection.get("minimum_score", 80)
    critical_minimum = selection.get("critical_minimum", 3)
    if not isinstance(minimum_score, (int, float)) or not 0 <= minimum_score <= 100:
        errors.append("selection.minimum_score 必须在 0 到 100 之间")
        minimum_score = 80
    if not isinstance(critical_minimum, (int, float)) or not 1 <= critical_minimum <= 5:
        errors.append("selection.critical_minimum 必须在 1 到 5 之间")
        critical_minimum = 3
    require_text(selection.get("reason"), "selection.reason", errors)

    selected_score = 0.0
    ids: set[str] = set()
    for index, direction in enumerate(directions, start=1):
        if not isinstance(direction, dict):
            errors.append(f"directions[{index}] 必须是对象")
            continue
        direction_id = direction.get("id")
        require_text(direction_id, f"directions[{index}].id", errors)
        if direction_id in ids:
            errors.append(f"方向 id 重复: {direction_id}")
        ids.add(direction_id)
        for field in ("name", "taste_thesis", "dominant_aesthetic"):
            require_text(direction.get(field), f"directions[{index}].{field}", errors)
        signals = direction.get("supporting_signals")
        if not isinstance(signals, list) or len(signals) > 2:
            errors.append(f"directions[{index}].supporting_signals 最多两个")
        for section, fields in {
            "typography": ("calligraphy_style", "title_font", "metadata_font", "hierarchy", "legibility_rule"),
            "composition": ("focal_point", "negative_space", "shot_progression"),
            "material_imagery": ("background", "texture", "lighting"),
            "motion": ("reveal", "tempo", "transition", "restraint"),
            "audio": ("voice", "emotion", "speed", "pause_logic"),
        }.items():
            data = require_object(direction.get(section), f"directions[{index}].{section}", errors)
            for field in fields:
                require_text(data.get(field), f"directions[{index}].{section}.{field}", errors)
        anti_patterns = direction.get("anti_patterns")
        if not isinstance(anti_patterns, list) or len(anti_patterns) < 2:
            errors.append(f"directions[{index}].anti_patterns 至少两个")
        direction_errors: list[str] = []
        direction_score = score_direction(direction, float(critical_minimum), direction_errors)
        errors.extend(f"directions[{index}].{message}" for message in direction_errors)
        if direction_id == selected_id:
            selected_score = direction_score

    if selected:
        palette = require_object(selected.get("palette"), "selected.palette", errors)
        for field in ("canvas", "primary_ink", "secondary_ink"):
            value = palette.get(field)
            if not isinstance(value, str) or not HEX.fullmatch(value):
                errors.append(f"selected.palette.{field} 必须是六位 HEX")
        for field in ("primary_role", "secondary_role"):
            require_text(palette.get(field), f"selected.palette.{field}", errors)
        if all(isinstance(palette.get(field), str) and HEX.fullmatch(palette[field]) for field in ("canvas", "primary_ink", "secondary_ink")):
            primary_ratio = contrast(palette["canvas"], palette["primary_ink"])
            secondary_ratio = contrast(palette["canvas"], palette["secondary_ink"])
            if primary_ratio < 4.5:
                errors.append(f"主笔与画布对比度 {primary_ratio:.2f}:1，低于 4.5:1")
            if secondary_ratio < 3.0:
                errors.append(f"辅笔与画布对比度 {secondary_ratio:.2f}:1，低于 3.0:1")
    if selected_score < float(minimum_score):
        errors.append(f"入选方向得分 {selected_score:.1f}/100，低于门槛 {float(minimum_score):.1f}")

    handoff = require_object(manifest.get("implementation_handoff"), "implementation_handoff", errors)
    for field in ("background_prompt", "calligraphy_prompt", "tts_direction"):
        require_text(handoff.get(field), f"implementation_handoff.{field}", errors)
    if not isinstance(handoff.get("verification"), list) or not handoff.get("verification"):
        errors.append("implementation_handoff.verification 必须是非空数组")
    return errors, selected_score, selected


def main() -> int:
    parser = argparse.ArgumentParser(description="审计内容审美与创意方向")
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"设计清单读取失败: {exc}")
        return 1
    errors, score, selected = audit(manifest)
    if errors:
        print("设计审计未通过:")
        for error in errors:
            print(f"- {error}")
        return 1
    palette = selected["palette"]
    print(f"✓ 入选方向: {selected['name']} ({score:.1f}/100)")
    print(f"✓ 主笔对比度: {contrast(palette['canvas'], palette['primary_ink']):.2f}:1")
    print(f"✓ 辅笔对比度: {contrast(palette['canvas'], palette['secondary_ink']):.2f}:1")
    print("设计闸门通过，可以进入 GPT Image 与 TTS 制作。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
