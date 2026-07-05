# Component reference

Copy-paste source, validated against a real 7-section report (Q2 硅谷 AI 产业观察). Don't
re-derive the CSS from scratch — start from this and only change content/colors per the
rules in SKILL.md.

## `<head>` boilerplate

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Noto+Sans+SC:wght@300;400;500;700;900&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

## Full CSS

```css
:root{
  --bg:#f5f0e8;
  --paper:#eef3fa;
  --panel:#ffffff;
  --ink:#182648;
  --muted:#57647a;
  --dim:#8794a8;
  --cyan:#1e6fd9;
  --cyan-bright:#1e6fd9;
  --cyan-glow:#60a5fa;
  --indigo:#e35a2b;
  --risk:#9c2f34;
  --border:rgba(24,38,72,.10);
  --on-dark:#eef3fa;
  --on-dark-muted:#93a3c0;
}
*{box-sizing:border-box; margin:0; padding:0;}
body{
  background:var(--bg); display:flex; justify-content:center;
  padding:40px 20px 80px; font-family:'Noto Sans SC', sans-serif; min-height:100vh;
}
::selection{ background:var(--cyan); color:#ffffff; }

.controls{ position:fixed; top:24px; right:24px; z-index:100; display:flex; flex-direction:column; gap:8px; }
.ctrl-btn{
  background:var(--paper); border:1px solid var(--cyan); color:var(--cyan-bright);
  font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:.05em;
  padding:8px 14px; cursor:pointer; transition:all .2s ease; white-space:nowrap;
}
.ctrl-btn:hover{ background:var(--cyan); color:#ffffff; }

.poster{
  position:relative; width:100%; max-width:760px; background:var(--paper); color:var(--ink);
  box-shadow:0 40px 100px rgba(24,38,72,.22), 0 0 0 1px rgba(30,111,217,.14); overflow:hidden;
}
.poster::before{
  content:''; position:absolute; inset:0; pointer-events:none; z-index:10; opacity:.6;
  background-image:
    linear-gradient(rgba(30,111,217,.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(30,111,217,.05) 1px, transparent 1px);
  background-size:28px 28px;
}

.topbar{ display:flex; justify-content:space-between; align-items:center; padding:18px 44px; border-bottom:1px solid var(--border); position:relative; z-index:2; }
.tag-chip{ background:var(--cyan); color:#ffffff; font-family:'JetBrains Mono', monospace; font-weight:700; font-size:10px; letter-spacing:.08em; padding:5px 12px; }
.topbar .meta{ font-family:'JetBrains Mono', monospace; font-size:10px; letter-spacing:.04em; color:var(--muted); text-align:right; line-height:1.6; }

.hero{ position:relative; padding:54px 44px 36px; overflow:hidden; z-index:2; }
.hero-watermark{
  position:absolute; top:-40px; right:-10px; font-family:'Playfair Display', serif; font-weight:900;
  font-size:190px; color:transparent; -webkit-text-stroke:1px rgba(20,28,38,.07); z-index:0; user-select:none;
}
.hero-eyebrow{ display:flex; align-items:center; gap:10px; font-family:'JetBrains Mono', monospace; font-size:11px; letter-spacing:.12em; color:var(--cyan-bright); margin-bottom:18px; position:relative; z-index:1; }
.hero-eyebrow::after{ content:''; flex:1; height:1px; background:var(--cyan); opacity:.35; }
.hero h1{ font-family:'Noto Sans SC', sans-serif; font-weight:900; font-size:32px; line-height:1.5; letter-spacing:-.01em; position:relative; z-index:1; }
.hero h1 em{ font-style:normal; color:var(--indigo); border-bottom:3px solid rgba(227,90,43,.3); }
.hero p.sub{ margin-top:20px; font-size:14.5px; font-weight:300; color:var(--muted); line-height:1.95; max-width:600px; position:relative; z-index:1; }

.takeaways{ margin:28px 0 0; border:1px solid var(--border); background:var(--panel); padding:22px 24px; position:relative; z-index:1; border-left:3px solid var(--cyan); }
.takeaways .tk-label{ font-family:'JetBrains Mono', monospace; font-size:9.5px; letter-spacing:.12em; color:var(--cyan-bright); margin-bottom:12px; }
.takeaways p{ font-size:15px; line-height:1.9; font-weight:700; color:var(--ink); margin:0; }

.divider{ height:1px; background:var(--border); margin:0 44px; position:relative; }
.divider::after{ content:'◆'; position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); background:var(--paper); padding:0 12px; font-size:8px; color:var(--cyan); }

.section{ padding:34px 44px 6px; position:relative; z-index:2; border-top:1px solid var(--border); }
.section:first-of-type{ border-top:none; }
.section-label{ font-family:'JetBrains Mono', monospace; font-weight:700; font-size:12px; letter-spacing:.1em; color:var(--cyan-bright); margin-bottom:14px; display:flex; align-items:center; gap:8px; }
.section-label::before{ content:''; width:18px; height:2px; background:var(--cyan); }
.section h2.stitle{ font-family:'Noto Sans SC', sans-serif; font-weight:900; font-size:27px; line-height:1.45; margin-bottom:20px; color:var(--ink); letter-spacing:-.01em; }

p{ font-size:14.5px; line-height:1.95; color:#333f4c; margin-bottom:20px; font-weight:300; }
strong.c{ color:var(--cyan-bright); font-weight:700; }
strong.i{ color:var(--indigo); font-weight:700; }

.pullquote{
  border-left:2px solid var(--cyan); padding:4px 0 4px 18px; margin:0 0 24px;
  font-size:14.5px; line-height:1.9; color:var(--ink); font-weight:700;
}

/* numbered reasons */
.reason{ display:flex; gap:16px; margin-bottom:20px; }
.reason .rn{ flex-shrink:0; width:34px; height:34px; border:1px solid var(--cyan); color:var(--cyan-bright); font-family:'JetBrains Mono', monospace; font-size:13px; display:flex; align-items:center; justify-content:center; }
.reason .rc h4{ font-size:14.5px; font-weight:700; color:var(--ink); margin-bottom:6px; }
.reason .rc p{ margin-bottom:0; }

/* company / entity profile, alternating accent */
.company{ margin-bottom:26px; padding-bottom:22px; border-bottom:1px solid var(--border); }
.company:last-child{ border-bottom:none; margin-bottom:0; padding-bottom:0; }
.company h3{ display:flex; align-items:center; gap:9px; font-size:15.5px; font-weight:700; color:var(--ink); margin-bottom:12px; }
.company h3::before{ content:''; width:8px; height:8px; background:var(--cyan); flex-shrink:0; }
.company.alt h3::before{ background:var(--indigo); }
.company.alt .pullquote{ border-left-color:var(--indigo); }

/* triad-ish structured list (2-3 short parallel lines) */
.triad{ border-left:2px solid var(--cyan); padding:2px 0 2px 18px; margin:0 0 24px; }
.triad p{ margin-bottom:6px; }
.triad p:last-child{ margin-bottom:0; }

/* charts: horizontal comparison bars */
.chart-box{ margin:0 0 26px; }
.chart-title{ font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:.05em; color:var(--muted); margin-bottom:16px; }
.cc-row{ margin-bottom:20px; }
.cc-row:last-child{ margin-bottom:0; }
.cc-head{ display:flex; justify-content:space-between; align-items:baseline; font-size:12px; color:var(--muted); margin-bottom:8px; gap:12px; }
.cc-head .cc-name{ color:var(--ink); font-weight:700; font-size:13px; }
.cc-head .cc-val{ font-family:'JetBrains Mono', monospace; font-weight:700; color:var(--ink); font-size:14px; flex-shrink:0; }
.cc-track{ height:22px; background:rgba(20,28,38,.06); position:relative; }
.cc-fill{ height:100%; border-radius:0 4px 4px 0; }
.chart-caption{ font-size:11.5px; color:var(--dim); line-height:1.85; margin-top:6px; }

/* stat tiles */
.stat-grid{ display:grid; grid-template-columns:repeat(2, 1fr); gap:0; border-top:1px solid var(--border); border-left:1px solid var(--border); margin-bottom:26px; }
.stat-tile{ position:relative; padding:18px 18px 16px; border-right:1px solid var(--border); border-bottom:1px solid var(--border); border-top:3px solid transparent; background:var(--panel); }
.stat-tile .st-label{ display:flex; align-items:center; gap:6px; font-family:'JetBrains Mono', monospace; font-size:9px; letter-spacing:.06em; color:var(--muted); margin-bottom:10px; }
.stat-tile .st-label .dot{ width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.stat-tile .st-value{ font-family:'JetBrains Mono', monospace; font-weight:700; font-size:30px; color:var(--ink); line-height:1; margin-bottom:8px; }
.stat-tile .st-cap{ font-size:11px; color:var(--muted); line-height:1.7; font-weight:300; }

/* card grid — e.g. 3-layer framework */
.grid{ display:grid; grid-template-columns:repeat(3, 1fr); gap:0; border-top:1px solid var(--border); border-left:1px solid var(--border); margin-bottom:20px; }
.card{ position:relative; padding:18px 16px; border-right:1px solid var(--border); border-bottom:1px solid var(--border); overflow:hidden; background:var(--panel); }
.card-num{ position:absolute; top:4px; right:8px; font-family:'JetBrains Mono', monospace; font-weight:700; font-size:28px; color:var(--cyan); opacity:.12; }
.card-label{ font-family:'JetBrains Mono', monospace; font-size:9px; letter-spacing:.08em; color:var(--cyan-bright); margin-bottom:8px; }
.card h3{ font-size:13.5px; font-weight:700; margin-bottom:6px; line-height:1.5; color:var(--ink); }
.card p{ font-size:11.5px; color:var(--muted); line-height:1.75; font-weight:300; margin-bottom:0; }

.alert-bar{ background:var(--risk); color:#fff; padding:16px 20px; display:flex; gap:16px; align-items:flex-start; margin-bottom:26px; }
.alert-bar .al-label{ font-family:'JetBrains Mono', monospace; font-weight:700; font-size:10px; letter-spacing:.1em; flex-shrink:0; padding-top:2px; }
.alert-bar .al-msg{ font-size:13px; line-height:1.85; }

/* the ONE dark inverted block — closing manifesto line */
.quote{
  position:relative; background:#0d1420; color:var(--on-dark); padding:44px 44px; z-index:2;
  border-top:1px solid var(--border); border-bottom:1px solid var(--border);
  box-shadow:inset 0 0 60px rgba(34,211,238,.06);
}
.quote-text{ position:relative; font-size:16.5px; font-weight:700; line-height:1.95; max-width:600px; color:var(--on-dark); }
.quote-text strong{ color:var(--cyan-glow); }
.quote-final{ margin-top:22px; font-family:'JetBrains Mono', monospace; font-size:13px; color:var(--cyan-glow); line-height:1.9; }
.attribution{ margin-top:20px; display:flex; align-items:center; gap:10px; font-family:'JetBrains Mono', monospace; font-size:11px; letter-spacing:.05em; color:var(--on-dark-muted); }
.attribution::before{ content:''; width:24px; height:1px; background:var(--cyan-glow); }

.footer{ padding:22px 44px; border-top:1px solid var(--border); position:relative; z-index:2; }
.footer .disc{ font-family:'JetBrains Mono', monospace; font-size:9px; color:var(--dim); line-height:1.9; letter-spacing:.02em; }
.footer .fmeta{ margin-top:10px; display:flex; justify-content:space-between; font-family:'JetBrains Mono', monospace; font-size:9px; color:var(--muted); letter-spacing:.04em; }

@media print{ .controls{ display:none !important; } .poster{ box-shadow:none; max-width:100%; } }

@media (max-width:640px){
  .hero h1{ font-size:25px; }
  .stat-grid, .grid{ grid-template-columns:1fr; }
  .topbar, .hero, .section, .quote, .footer{ padding-left:22px; padding-right:22px; }
}
```

## HTML skeleton

```html
<div class="controls">
  <button class="ctrl-btn" onclick="exportPNG()">↓ 导出 PNG</button>
  <button class="ctrl-btn" onclick="window.print()">⎙ 打印 / PDF</button>
</div>

<div class="poster" id="poster">

  <div class="topbar">
    <span class="tag-chip">RESEARCH NOTE · 分类标签</span>
    <span class="meta">品牌名（发布方)<br>期号 · 年份</span>
  </div>

  <div class="hero">
    <div class="hero-watermark">Q2</div>
    <div class="hero-eyebrow">品牌名（发布方)</div>
    <h1>主标题前半句<br>关键论点 <em>用橙红点睛的短语</em></h1>
    <p class="sub">2-3 句话的导语，交代这篇报告在讲什么、为什么现在重要。</p>

    <div class="takeaways">
      <div class="tk-label">TL;DR · 一句话概括</div>
      <p>全文最锋利的一句合成判断，<strong class="c">关键短语加粗高亮</strong>。</p>
    </div>
  </div>

  <div class="divider"></div>

  <!-- repeat .section per chapter; see snippets below for what goes inside -->

  <div class="quote">
    <p class="quote-text">收尾金句，<strong>关键词</strong>用 cyan-glow 高亮。</p>
    <p class="quote-text" style="margin-top:16px; font-weight:400; font-size:14px; color:var(--on-dark-muted);">补充的一两句收束。</p>
    <div class="quote-final">mono 字体的核心信号总结句。</div>
    <div class="attribution">写在最后</div>
  </div>

  <div class="footer">
    <div class="disc">数据来源与免责声明，说明口径差异、不构成投资建议等。</div>
    <div class="fmeta">
      <span>品牌名（发布方)</span>
      <span>期号 · 年份</span>
    </div>
  </div>

</div>
```

## Section-content snippets

Section wrapper (repeat per chapter):

```html
<div class="section">
  <div class="section-label">01 · 关键词</div>
  <h2 class="stitle">这一章的核心论点，写成一句完整判断，不要只写话题词</h2>
  <p>正文段落…</p>
  <div class="pullquote">这一段的"一句话判断"，只在源材料本身有明确判断句时才拉出来。</div>
</div>
```

Numbered reasons ("为什么是这几个原因"):

```html
<div class="reason">
  <div class="rn">01</div>
  <div class="rc"><h4>原因标题</h4><p>展开说明…</p></div>
</div>
```

Company/entity profile, alternate `.company` and `.company.alt` in source order:

```html
<div class="company">
  <h3>实体名 · 一句话定位</h3>
  <p>正文分析…</p>
  <div class="pullquote">这家的"一句话判断"。</div>
</div>
<div class="company alt">
  <h3>下一个实体 · 一句话定位</h3>
  <p>正文分析…</p>
  <div class="pullquote">一句话判断，边框自动跟随 .alt 变成橙红。</div>
</div>
```

Structured triad (2–3 short parallel clauses, e.g. who-owns-what):

```html
<div class="triad">
  <p><strong class="c">A</strong>负责……；</p>
  <p><strong class="c">B</strong> 负责……；</p>
  <p><strong class="c">C</strong>负责……。</p>
</div>
```

Horizontal comparison chart (2–3 entities, one metric — width% is entity value ÷ max value × 100):

```html
<div class="chart-box">
  <div class="chart-title">图表标题，注明单位和口径说明</div>
  <div class="cc-row">
    <div class="cc-head"><span class="cc-name">实体 A · 补充说明</span><span class="cc-val">数值</span></div>
    <div class="cc-track"><div class="cc-fill" style="width:100%; background:var(--cyan);"></div></div>
  </div>
  <div class="cc-row">
    <div class="cc-head"><span class="cc-name">实体 B · 补充说明</span><span class="cc-val">数值</span></div>
    <div class="cc-track"><div class="cc-fill" style="width:63%; background:var(--indigo);"></div></div>
  </div>
  <div class="chart-caption">口径差异说明——覆盖范围、统计方法不同的地方必须写出来。</div>
</div>
```

Stat tile grid (2 or 3 columns — set `grid-template-columns` on `.stat-grid` inline or add a modifier class):

```html
<div class="stat-grid">
  <div class="stat-tile" style="border-top-color:var(--cyan);">
    <div class="st-label"><span class="dot" style="background:var(--cyan);"></span>指标名</div>
    <div class="st-value">+63%</div>
    <div class="st-cap">数据来源和上下文说明。</div>
  </div>
  <div class="stat-tile" style="border-top-color:var(--indigo);">
    <div class="st-label"><span class="dot" style="background:var(--indigo);"></span>另一个指标</div>
    <div class="st-value">5×</div>
    <div class="st-cap">数据来源和上下文说明。</div>
  </div>
</div>
```

3-layer framework card grid:

```html
<div class="grid">
  <div class="card">
    <div class="card-num">01</div>
    <div class="card-label">LAYER NAME</div>
    <h3>层级标题</h3>
    <p>这一层包含什么。</p>
  </div>
  <!-- repeat for each layer -->
</div>
```

Risk/caveat callout:

```html
<div class="alert-bar">
  <div class="al-label">RISK</div>
  <div class="al-msg">风险点列举，用顿号分隔，末尾一句总括。</div>
</div>
```

## Export script

```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script>
  function exportPNG(){
    const poster = document.getElementById('poster');
    const btn = document.querySelectorAll('.ctrl-btn')[0];
    const originalLabel = btn.textContent;
    btn.textContent = '⋯ 生成中';
    html2canvas(poster, { backgroundColor: '#eef3fa', scale: 2, useCORS: true }).then(canvas => {
      const link = document.createElement('a');
      link.download = '报告文件名.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
      btn.textContent = originalLabel;
    }).catch(() => { btn.textContent = originalLabel; });
  }
</script>
```

`backgroundColor` in the html2canvas call must match `--paper`'s hex — if you change the
palette, update this too, or exported PNGs will get a white background seam where the
card's translucent bits show through.
