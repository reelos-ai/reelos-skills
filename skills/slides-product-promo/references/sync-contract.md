# Audio–visual sync contract

## Timeline requirements

- Start the first scene at 0.
- End the final scene at the measured audio duration within one video frame.
- Keep scenes contiguous; allow no gap or overlap larger than one frame.
- Store start and end times as seconds with millisecond precision.
- Map each scene to an exact spoken phrase or intentional silence.

## Anchor tolerances

- Product name reveal: ±0.20 s
- Large keyword or feature label: ±0.25 s
- Domain typing start: ±0.20 s from “打开”, “访问”, or the spoken domain
- Domain completion: before the spoken domain ends or within +0.25 s
- Disclaimer visual start: ±0.35 s
- Ordinary scene boundary: ±0.40 s

## Timestamp sources

Use word timestamps from transcription when available. Otherwise:

1. Detect pauses with `scripts/detect-pauses.sh`.
2. Listen around each candidate boundary.
3. Align to the beginning of the meaningful word, not the middle of silence.
4. Save the final reviewed values in `timeline.json`.

## Timeline fields

Each shot needs:

- `id`
- `start`, `end`
- `phrase`
- `slide`
- `visual`
- `motion.type`, `motion.amount`
- optional `anchor`, `tolerance`

The root needs `fps`, `audio`, `audio_duration`, and `shots`.
