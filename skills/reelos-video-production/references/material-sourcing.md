# 主题素材检索与叠加

## 什么时候启用

主题素材层是可选增强，不是默认装饰。满足下面任一条件时才启用：

- 用户明确要求找素材、加背景视频、加主题图片、加真实纹理或参考免费素材站。
- 内容高度抽象，需要真实世界资料把观众带入现场，例如道、佛、禅修、历史、人文、自然、城市、工厂、AI 工程空间。
- 当前画面只有文字、图形或色块，关键帧显得空、泛、模板感重。
- 封面、开头、章节转场、结尾金句需要更强氛围，但正文讲解仍要保持清晰。

不启用的情况：

- 画面已经有足够信息密度，加入素材会干扰阅读。
- 投研报告、备忘录、黑板教学等风格本身需要干净、理性、低干扰。
- 没有可授权来源、无法记录许可，或 API key 缺失且没有合适本地素材。
- 素材只能作为“好看背景”，不能增强主题理解。

## 检索决策

1. 先写 3-6 个关键词：中文主题词 + 英文搜索词。例如 `道家 山雾 taoism mountain mist ancient temple`。
2. 再判断素材类型：视频优先用于慢背景和转场；图片优先用于纹理、文物、法相、古籍和局部叠加。
3. 再按画幅筛选：横屏视频优先匹配 1920x1080；竖屏项目优先匹配 1080x1920。
4. 再按时长筛选：素材片段必须长于目标分镜，或能无感循环。
5. 最后按视觉一致性筛选：色彩、明暗和主题必须能融入当前色板。

## API 来源

### Pexels

- API：`https://api.pexels.com/videos/search`
- 鉴权：Header `Authorization: <PEXELS_API_KEY>`
- 常用参数：`query`、`per_page`、`orientation`
- 适合：自然、建筑、人物氛围、空间、抽象光影。
- 筛选：优先找目标分辨率完全匹配的视频文件；不匹配时谨慎降级。

参考调用：

```text
GET https://api.pexels.com/videos/search?query=mountain%20mist&per_page=20&orientation=landscape
Authorization: <PEXELS_API_KEY>
```

### Pixabay

- API：`https://pixabay.com/api/videos/`
- 鉴权：URL 参数 `key=<PIXABAY_API_KEY>`
- 常用参数：`q`、`video_type=all`、`per_page`
- 适合：自然、插画感视频、纹理、抽象视频。
- 筛选：返回 `hits`，每条素材有不同清晰度版本；优先选宽度满足目标尺寸的视频。

参考调用：

```text
GET https://pixabay.com/api/videos/?q=temple%20mist&video_type=all&per_page=50&key=<PIXABAY_API_KEY>
```

### Coverr

- API：`https://api.coverr.co/videos`
- 鉴权：Header `Authorization: Bearer <COVERR_API_KEY>`
- 常用参数：`query`、`page_size`、`urls=true`、`sort=popular`
- 适合：横屏背景、商业空间、城市、自然、生活方式镜头。
- 筛选：以横屏素材为主，不强过滤比例；后续用视频处理逻辑 resize、crop 或 letterbox。

参考调用：

```text
GET https://api.coverr.co/videos?query=abstract%20technology&page_size=20&urls=true&sort=popular
Authorization: Bearer <COVERR_API_KEY>
```

## 下载与验证

- 下载路径建议：`public/materials/{slug}/`。
- 文件命名：`{provider}-{topic}-{shortHash}.mp4` 或 `{provider}-{topic}-{shortHash}.jpg`。
- 下载前用原始 URL 去掉 query 后做 hash，避免重复下载。
- 下载后必须用 `ffprobe` 验证视频能读出 duration、width、height、fps。
- 验证失败必须删除文件并换素材。
- 不要把临时缓存路径直接写进 Remotion；只引用项目内可提交或可复现的素材路径。

## 二次设计规则

外部素材不能直接铺满当背景。必须做二次设计：

- 裁切局部，而不是展示完整素材。
- 降低饱和度和对比度，统一到当前色板。
- 用 `opacity`、`mixBlendMode`、渐变遮罩或噪声层压低存在感。
- 文化类可叠加纸纹、颗粒、暗角、光扫；科技类可叠加日志、节点、状态灯。
- 背景透明度通常 8%-22%，文化氛围可到 30%，但不得影响文字可读性。

## 许可记录

每个被使用的素材都要在对应视觉设计卡中记录：

```text
素材名称：
来源网站：
API/页面 URL：
作者/上传者：
许可类型：
下载日期：
本地路径：
用途：
处理方式：
```

## 参考实现

可参考 MoneyPrinterTurbo 的素材检索思路，但不要直接耦合它的代码：

- Pexels：`/Users/netseek/Documents/MoneyPrint/MoneyPrinterTurbo/app/services/material.py`
- Pixabay：同文件 `search_videos_pixabay`
- Coverr：同文件 `search_videos_coverr`

可吸收的工程策略：

- 多 API key 时轮询使用。
- 请求设置超时。
- 按 duration 过滤。
- Pexels 优先分辨率完全匹配。
- Pixabay 从多清晰度版本里选择满足目标宽度的文件。
- Coverr 横屏优先，比例适配交给后续视频处理。
- 下载后验证音视频文件有效性，无效则删除。
