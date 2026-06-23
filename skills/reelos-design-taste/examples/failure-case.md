# Failure Case

## User input

给我做一个中式、印度、非洲、赛博朋克、北欧、禅修混合风格，高级一点。

## Expected behavior

The skill should:
- Treat this as ambiguous style conflict.
- Ask one clarifying question or choose a dominant style if enough context exists.
- Avoid combining all motifs.

## Expected output

```text
你给的方向包含多个强烈且互相竞争的视觉系统。为了做出真正高级的结果，需要先确定主导逻辑：这个项目更应该偏「安静疗愈」「文化仪式」「高能节庆」还是「科技未来」？
```
