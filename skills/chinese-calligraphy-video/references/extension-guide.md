# 扩展开发指南

## 稳定边界

- 配置文件是项目与 Skill 的接口，当前 `schema_version` 为 1。
- 书法前景必须是 RGBA；背景可为 RGB/RGBA；路径相对配置文件解析。
- 图像生成与 TTS 是可替换的上游，合成器不依赖具体供应商。
- 渲染输出由 ffmpeg 负责，编码参数位于 `encoding`。

## 添加显影策略

1. 在 `compose_video.py` 中实现新的 mask 函数。
2. 在 `reveal_mask()` 分派新名称。
3. 在 `validate_project.py` 的 `REVEAL_STYLES` 注册名称。
4. 在 `configuration.md` 记录语义与适用场景。
5. 在 `self_test.py` 增加至少一个镜头覆盖该策略。

显影策略只接收透明母版、文本和 0–1 progress；不要把供应商或项目路径耦合进 mask。

## 替换图像生成方式

保持输出契约即可：每句一张 RGBA PNG、文字准确、透明四角、有效区域足够宽。默认仍应优先使用 Codex 内置 GPT Image；只有用户明确选择其他生成路径时才替换。

## 接入 TTS

每个供应商最终只需落地一个可被 ffmpeg 读取的分句音频文件。把 provider、voice ID、情绪与语速记录在项目清单中，但不要写入密钥。时间轴只依赖每句 `audio` 和 `tts_lead_seconds`。

## 新增配置字段

- 新字段优先可选并提供旧行为默认值。
- 破坏性修改必须提升 `schema_version`，同时在加载器中明确迁移或拒绝。
- 在模板、配置参考、校验器和自测中同步覆盖。

## 回归门槛

```bash
"$PYTHON_BIN" scripts/calligraphy_video.py self-test
"$PYTHON_BIN" scripts/calligraphy_video.py validate --config <existing-config>
"$PYTHON_BIN" scripts/calligraphy_video.py render --config <existing-config> --output <test.mp4>
"$PYTHON_BIN" scripts/calligraphy_video.py inspect --input <test.mp4> --config <existing-config>
```

同时检查旧项目配置兼容、新配置扩展字段、三种显影策略、音频边界、contact sheet 和最终编码。
