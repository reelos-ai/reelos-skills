#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def media_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a TTS-synced promo timeline")
    parser.add_argument("timeline", type=Path)
    parser.add_argument("--audio", type=Path)
    args = parser.parse_args()

    data = json.loads(args.timeline.read_text(encoding="utf-8"))
    fps = float(data.get("fps", 0))
    shots = data.get("shots", [])
    expected = float(data.get("audio_duration", 0))
    errors = 0

    if fps <= 0:
        fail("fps must be greater than zero")
        errors += 1
        fps = 30.0
    tolerance = 1.0 / fps

    if not shots:
        fail("shots must not be empty")
        return 1

    if args.audio:
        actual = media_duration(args.audio)
        if expected and abs(actual - expected) > tolerance:
            fail(f"audio_duration {expected:.3f}s differs from media {actual:.3f}s")
            errors += 1
        expected = actual

    previous_end = 0.0
    hard_cut_times = []
    for index, shot in enumerate(shots):
        label = shot.get("id", f"shot-{index + 1}")
        try:
            start = float(shot["start"])
            end = float(shot["end"])
        except (KeyError, TypeError, ValueError):
            fail(f"{label} needs numeric start and end")
            errors += 1
            continue

        if end <= start:
            fail(f"{label} has non-positive duration")
            errors += 1
        if abs(start - previous_end) > tolerance:
            fail(f"{label} boundary gap/overlap is {start - previous_end:+.3f}s")
            errors += 1
        if end - start < 0.7:
            fail(f"{label} is shorter than the 0.7s comfort floor")
            errors += 1
        if index:
            hard_cut_times.append(start)
        previous_end = end

        anchor_tolerance = shot.get("tolerance")
        if anchor_tolerance is not None and float(anchor_tolerance) < 0:
            fail(f"{label} has a negative anchor tolerance")
            errors += 1

    if expected and abs(previous_end - expected) > tolerance:
        fail(f"timeline ends at {previous_end:.3f}s; audio ends at {expected:.3f}s")
        errors += 1

    for start in hard_cut_times:
        cuts = sum(1 for value in hard_cut_times if start <= value < start + 2.0)
        if cuts > 3:
            fail(f"more than three cuts occur between {start:.3f}s and {start + 2:.3f}s")
            errors += 1
            break

    if errors:
        print(f"Timeline validation failed with {errors} error(s).", file=sys.stderr)
        return 1

    print(
        f"Timeline OK: {len(shots)} shots, {previous_end:.3f}s, "
        f"{fps:g} fps, tolerance {tolerance:.4f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
