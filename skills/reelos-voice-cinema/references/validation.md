# Validation

Use this reference before claiming a video task is complete.

## Required Checks

Run:

```bash
npm run check
```

Export stills and visually inspect:

- title readability
- subtitle readability
- no overlap between title, caption, keywords, and diagrams
- no text clipped by safe areas
- visual lane matches the user request
- material clips are not blank or badly cropped
- final frame is complete

Render:

```bash
npm run render:slug
```

If Chromium cannot launch because of macOS sandbox permissions, rerun the render with escalated permission.

Validate output:

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=codec_type,codec_name,width,height,r_frame_rate \
  -of json out/slug.mp4
```

Expected:

- video stream exists
- audio stream exists unless intentionally silent
- fps is `30/1`
- dimensions match composition
- duration matches timing

## Final Response Must Include

- MP4 path with local video markdown if appropriate
- TTS scene count
- whether timing came from real audio
- output duration and dimensions
- key changed files
- verification commands and results
