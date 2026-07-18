# 配置说明

## 设计清单

`design_manifest.json` 是上游创意 SSOT。开始素材校验、预览、TTS 或渲染前先运行 `design-audit`。视频配置可以用可选字段 `design_manifest` 记录其相对路径；渲染器忽略该字段，制作人员和编排流程用它追溯已批准的方向。

设计清单结构与 100 分门槛见 `content-aesthetics.md`。视频配置只保留合成器需要的具体渲染值，不重复维护配色理由和创意判断。

## 顶层字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `schema_version` | 整数 | 当前为 `1`；缺省按 1 兼容旧配置 |
| `variant` | 字符串 | 素材版本名，例如 `scheme08-cursive` |
| `design_manifest` | 路径 | 可选，指向已通过审计的设计清单 |
| `width`, `height` | 整数 | 输出分辨率 |
| `fps` | 整数 | 输出帧率，推荐 24 |
| `reveal_style` | 字符串 | `character-wipe`、`line-wipe` 或 `fade` |
| `background_dim` | 0–1 浮点 | 背景压暗比例，提升书法可读性 |
| `background` | RGB 数组 | 无背景图时的纯色背景 |
| `background_asset` | 路径 | 可选，等比覆盖并居中裁切 |
| `title`, `author` | 字符串 | 右下角信息 |
| `badge` | 字符串 | 左下角题签，默认“愿君全屏静赏” |
| `info_color`, `badge_color` | RGB/RGBA | 题签颜色 |
| `line_build_seconds` | 浮点 | 每句逐字显影时长 |
| `line_hold_seconds` | 浮点 | 每句完整停留时长 |
| `gap_seconds` | 浮点 | 句间空场 |
| `intro_seconds`, `outro_seconds` | 浮点 | 首尾留白 |
| `tts_lead_seconds` | 浮点 | TTS 相对镜头开始的延迟 |
| `max_line_width`, `max_line_height` | 整数 | 书法母版最大显示范围 |
| `lines` | 数组 | 每句文本、透明图与可选音频 |
| `encoding` | 对象 | ffmpeg 视频/音频编码参数 |

## 每句字段

```json
{
  "text": "空山不见人",
  "asset": "assets/lines/default/line_01.png",
  "audio": "assets/audio/line_01.mp3"
}
```

每句可覆盖全局参数：

```json
{
  "text": "空山不见人",
  "asset": "assets/lines/default/line_01.png",
  "audio": "assets/audio/line_01.mp3",
  "build_seconds": 1.8,
  "hold_seconds": 2.6,
  "gap_seconds": 0.4,
  "tts_lead_seconds": 0.25,
  "reveal_style": "character-wipe",
  "x_offset": 0,
  "y_offset": -24,
  "scale": 1.05,
  "max_width": 1760,
  "max_height": 680
}
```

`character-wipe` 按字符区域依次显影；`line-wipe` 对整行做连续扫写；`fade` 适合尾场或完整诗文。三者都不等同于真实笔顺。

所有路径相对于配置文件所在目录解析。删除 `audio` 即可输出无声版本。

## 编码字段

```json
{
  "encoding": {
    "video_codec": "libx264",
    "preset": "medium",
    "crf": 18,
    "pixel_format": "yuv420p",
    "audio_codec": "aac",
    "audio_bitrate": "192k",
    "audio_sample_rate": 48000
  }
}
```

发布到常见社交平台时保持 `libx264`、`yuv420p` 与 AAC。只有确认目标播放器支持时才更换编码器或像素格式。

## 推荐节奏

- 4–5 字：显影 1.5–1.8 秒，停留 2.2–2.8 秒。
- 6–7 字：显影 1.8–2.2 秒，停留 2.5–3.0 秒。
- 句间空场：0.3–0.5 秒。
- TTS 延迟：镜头开始后 0.2–0.4 秒。

题签与播放器时间是不同图层。除非用户明确要求，不要把播放器的 `00:00` 时间显示烙进视频。

## 常见诗名输入

用户只提供诗名时，先展示拟采用的完整版本并确认，再开始生图。古诗存在异文、繁简体与标点差异，不能仅凭标题直接进入图像生成。
