#!/usr/bin/env bash
set -euo pipefail

audio_file="${1:?Usage: detect-pauses.sh <audio-file> [noise-db] [min-duration]}"
noise_db="${2:--38dB}"
min_duration="${3:-0.18}"

ffmpeg -hide_banner -i "$audio_file" \
  -af "silencedetect=noise=${noise_db}:d=${min_duration}" \
  -f null - 2>&1 |
  awk '
    /silence_start:/ {
      for (i = 1; i <= NF; i++) if ($i == "silence_start:") start = $(i + 1)
    }
    /silence_end:/ {
      for (i = 1; i <= NF; i++) {
        if ($i == "silence_end:") finish = $(i + 1)
        if ($i == "silence_duration:") duration = $(i + 1)
      }
      printf "%.6f,%.6f,%.6f\n", start, finish, duration
    }
  '
