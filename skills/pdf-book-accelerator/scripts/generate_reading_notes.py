#!/usr/bin/env python3
"""Generate a Markdown reading-notes scaffold from extracted PDF text."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PAGE_MARKER = re.compile(r"^--- page (\d+) ---$", re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> object:
    return json.loads(read_text(path))


def page_slice(full_text: str, start_page: int, end_page: int | None = None) -> str:
    markers = list(PAGE_MARKER.finditer(full_text))
    start_idx = None
    end_idx = len(full_text)
    for i, match in enumerate(markers):
        page = int(match.group(1))
        if page == start_page:
            start_idx = match.end()
        if end_page is not None and page == end_page:
            end_idx = match.start()
            break
        if end_page is None and start_idx is not None and i + 1 < len(markers):
            end_idx = markers[i + 1].start()
            break
    if start_idx is None:
        return ""
    return full_text[start_idx:end_idx].strip()


def heading_positions(full_text: str, heading: str) -> list[re.Match[str]]:
    pattern = re.compile(rf"^{re.escape(heading)}$", re.MULTILINE)
    return list(pattern.finditer(full_text))


def section_between(full_text: str, heading: str, next_heading: str | None = None, occurrence: str = "last") -> str:
    matches = heading_positions(full_text, heading)
    if not matches:
        return ""
    match = matches[0] if occurrence == "first" else matches[-1]
    start = match.end()
    end = len(full_text)
    if next_heading:
        next_matches = [m for m in heading_positions(full_text, next_heading) if m.start() > start]
        if next_matches:
            end = next_matches[0].start()
    return full_text[start:end].strip()


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip(" -")


def content_lines(section: str) -> list[str]:
    lines = []
    for raw_line in section.splitlines():
        if PAGE_MARKER.match(raw_line.strip()):
            continue
        line = clean_line(raw_line)
        if re.fullmatch(r"page \d+", line, flags=re.IGNORECASE):
            continue
        if line:
            lines.append(line)
    return lines


def detect_identity(full_text: str, metadata: dict) -> tuple[str, str]:
    first_pages = "\n".join(page_slice(full_text, p) for p in range(2, 7))
    lines = [clean_line(line) for line in first_pages.splitlines() if clean_line(line)]
    title = metadata.get("source", "Book")
    author = ""
    for i, line in enumerate(lines):
        if line.lower().startswith("by ") and i > 0:
            author = line[3:].strip()
            title = lines[i - 1]
            if i >= 2 and len(lines[i - 2]) < 90 and not lines[i - 2].lower().startswith("contents"):
                title = f"{lines[i - 2]}: {title}"
            break
    return str(title), author


def extract_takeaways(full_text: str) -> list[str]:
    section = section_between(full_text, "Takeaways", "The ARISE cheatsheet")
    lines = content_lines(section)
    merged: list[str] = []
    current = ""
    for line in lines:
        if re.match(r"^(Prologue\.|\d{1,2}\.)", line):
            if current:
                merged.append(current)
            current = line
        elif current:
            current = f"{current} {line}"
    if current:
        merged.append(current)
    return merged


def extract_arise(full_text: str) -> str:
    section = section_between(full_text, "The ARISE cheatsheet", "Further reading")
    if not section:
        return ""
    lines = content_lines(section)
    keep = []
    for line in lines:
        keep.append(line)
        if len(" ".join(keep)) > 1800:
            break
    return "\n".join(keep)


def markdown_escape(text: str) -> str:
    return text.replace("\n", " ").strip()


def append_book_header(lines: list[str], title: str, author: str, metadata: dict, mode: str = "baopo") -> None:
    lines.append(f"# {markdown_escape(title)}")
    if author:
        lines.append(f"\n作者: {markdown_escape(author)}")
    lines.append(f"\n来源: `{metadata.get('source', '')}`")
    lines.append(f"\n页数: {metadata.get('pages', '')}")
    lines.append(f"\n估算词数: {metadata.get('total_words_estimate', '')}")
    lines.append(f"\n阅读模式: {mode}")


def append_chapter_map(lines: list[str], chapters: object) -> None:
    lines.append("\n## 章节地图")
    if isinstance(chapters, list):
        for item in chapters:
            lines.append(f"- p. {item.get('page')}: {item.get('title')}")


def is_half_second_book(title: str, chapters: object) -> bool:
    if "The Half Second" in title:
        return True
    if not isinstance(chapters, list):
        return False
    joined = " ".join(str(item.get("title", "")) for item in chapters)
    signals = [
        "The half-second tells the truth",
        "The frequency counter",
        "The shape of a workable script",
        "Repeat past the protest",
    ]
    return sum(signal in joined for signal in signals) >= 2


def build_half_second_notes_zh(metadata: dict, chapters: object, title: str, author: str, mode: str = "baopo") -> str:
    lines: list[str] = []
    append_book_header(lines, title, author, metadata, mode)

    lines.append("\n## 开卷导读")
    lines.append("\n*——一个想改掉旧习惯的人，如何在「半秒」里改写第一反应*")
    lines.append("\n### 我读它，为了解决什么问题？")
    lines.append("\n为什么明明知道更好的选择，临场还是自动做出旧反应。它要解决的是「知道却做不到」——不靠事后意志力硬压，而是在刺激后的半秒里，让新动作先于旧反应启动。")
    lines.append("\n### 有没有一个核心模型？")
    lines.append("\n一句话核心：第一反应是事前写入的，不是现场选择的。母框架是 ARISE 脚本：刺激 → 旧反应启动 → 熟悉性计数器强化 → 新动作脚本重复 → 默认反应被改写。先写一个短、具体、可观察的动作脚本，重复到熟悉，让它接管半秒。")
    lines.append("\n### 读完之后我能做什么？")
    lines.append("- 改习惯：选一个旧反应，写「当 X 时，我做 Y，因为 Z」并重复 7 天。")
    lines.append("- 控冲动：在争吵、消费、投资波动前，用脚本插入一个可观察的小动作。")
    lines.append("- 待抗拒：把「觉得蠢」当成新脚本碰到旧身份的正常信号，而非失败。")
    lines.append("- 做维护：环境持续写入，定期重复以防旧反应回潮。")

    lines.append("\n## 阅读目标与知识资产")
    lines.append("- 默认目标: 快速理解 + 提炼可用方法 + 输出内容素材。")
    lines.append("- 可选目标: 快速了解、深度学习、写作/内容输出、产品/创业参考、管理/组织学习、投资/商业分析、个人行动。")
    lines.append("- 最终资产: 一页纸读书卡、完整 HTML 笔记、文章选题、团队分享大纲、行动实验。")

    lines.append("\n## 一页速读")
    lines.append("\n这本书不是在讲“如何更努力地改变自己”，而是在讲一个更小、更早、更难被察觉的位置: 刺激出现后的半秒。作者认为，很多决定并不是我们想清楚后做出的，而是在理性解释赶到之前，身体已经给出了第一反应。")
    lines.append("\n全书最有用的部分是一个行为脚本方法: 选一句短到能反复说、具体到身体能执行、真实到自己不会反感的话，让它通过重复逐渐变成默认反应。它不是正能量口号，也不是“我很棒”式肯定句。它的目标不是让你感觉良好，而是让你在旧反应出现前，已经有了新的动作。")
    lines.append("\n最值得深读的是序言、Ch1-Ch7、Ch11-Ch13、Takeaways 和 ARISE cheatsheet。Ch14-Ch17 是应用场景，涉及金钱、自我攻击、亲密关系和建设性习惯。参考文献很长，除非你要追证据，否则可以先跳过。")

    lines.append("\n## 核心主张")
    lines.append("\n第一反应不是靠事后意志力修正的，而是靠事前重复写入的。真正的改变发生在刺激出现后的半秒内: 旧反应还没完全启动，新脚本已经可以接管。")

    lines.append("\n## 单概念书判断")
    lines.append("- 类型: 单概念反复展开型。作者不是在堆很多新理论，而是在把“第一反应可以被写入，也可以被改写”这件事换场景讲透。")
    lines.append("- 一件事: 为什么明明知道更好的选择，临场还是会自动做旧反应？")
    lines.append("- 一个概念: 半秒第一反应窗口。")
    lines.append("- 一个模型: 刺激 -> 旧反应启动 -> 熟悉性计数器强化 -> 动作脚本重复 -> 默认反应改写。")
    lines.append("- 高效读法: 精读概念定义、机制链和 2-3 个最相关场景；对同质化案例只做一句话记录。")

    lines.append("\n## 提问链")
    lines.append("> [!tip] 用法：问题决定读哪里。每个问题都链到具体章节，答完会逼出下一个更尖的问题，从而驱动取舍，而不是平均读完每一页。")
    questions = [
        "读前·真问题: 我现在最想改掉的旧第一反应是什么？这是全书要为我解决的起点。",
        "第1问 → Ch1-Ch2: 作者如何解释“我知道但做不到”？→ 答：意志力来得太晚。→ 逼出：那真正能改写的位置在哪？",
        "第2问 → Ch1「半秒」: 改变发生在什么时间窗口？→ 答：刺激后、理性赶到前的半秒。→ 逼出：靠什么把新反应写进这半秒？",
        "第3问 → Ch6-Ch7「脚本/ARISE」: 一个能进半秒的脚本长什么样？→ 答：短、具体、可观察的动作。→ 逼出：哪些章只是换场景重复，可略读？",
        "第4问 → Ch11-Ch13: 安装时的抗拒和维护怎么处理？→ 答：觉得蠢是正常，靠重复到熟悉并维护。→ 逼出：我能写出哪一句“当 X 时我做 Y，因为 Z”？",
        "读后·收摄: 7 天后我用什么信号判断它真的有用？",
    ]
    lines.extend(f"- {item}" for item in questions)

    lines.append("\n## 关键词地图")
    keyword_map = [
        "核心词: half-second, first reaction, frequency counter, script, identity hub。",
        "支撑词: System 1, System 2, familiarity, repetition, maintenance。",
        "行动词: identify, write, repeat, test, maintain。",
        "边界词: trauma, addiction, acute mental state, technical skill, preference override。",
        "迁移词: 刺激、反应、选择空间、默认值、脚本化动作。",
    ]
    lines.extend(f"- {item}" for item in keyword_map)

    lines.append("\n## 金句与可转述句")
    lines.append("\n这里优先使用可转述句，不堆原文摘抄。金句的作用不是收藏，而是压缩模型，方便讲给别人和指导行动。")
    golden_lines = [
        "可转述句: 旧反应不是现场选择出来的，而是过去被重复写入的。",
        "可转述句: 意志力的问题不是不够强，而是经常来得太晚。",
        "可转述句: 半秒里装不下宏大目标，只装得下一个小动作。",
        "可转述句: 先别急着相信新脚本，先把它重复到熟悉。",
        "可转述句: 学习如果没有改变第一反应，还只是解释能力变强。",
        "使用场景: 讲给别人听、写海报标题、设计 7 天行动实验。",
        "误用边界: 不要把这些句子当万能肯定句，也不要用它替代专业治疗或复杂决策。",
    ]
    lines.extend(f"- {item}" for item in golden_lines)

    lines.append("\n## 费曼讲解卡")
    feynman_cards = [
        "讲给小孩: 大脑像输入法，常打的字会先跳出来。旧反应也是这样。想改变，就要提前练一个新词，让它以后先跳出来。",
        "讲给同事: 这本书把行为改变的位置从事后反思前移到第一反应窗口。它主张用短脚本和重复训练，改写临场默认动作。",
        "讲给自己: 别再问“我为什么这么差”，改问“哪个触发线索一出现，我要先做哪个小动作”。",
        "一句公式: 当 X 出现时，我先做 Y，因为 Z。",
        "检验标准: 如果不能写出 X 和 Y，就说明还停留在道理层，没有进入行动层。",
    ]
    lines.extend(f"- {item}" for item in feynman_cards)

    append_chapter_map(lines, chapters)

    lines.append("\n## 作者的核心机制")
    lines.append("\n作者把人的反应分成两个时间层:")
    lines.append("\n- 半秒内: 第一反应已经启动，身体先动，语言和解释随后赶到。")
    lines.append("- 半秒后: 理性开始解释、辩护、压制、后悔，很多时候已经晚了。")
    lines.append("\n所以，作者认为“靠意志力改行为”常常失败，不是因为人太弱，而是因为意志力介入的窗口太晚。旧反应已经开跑了，理性才开始追。")
    lines.append("\n书里反复出现的机制是 `frequency counter`，可以理解为“熟悉性计数器”。它不太关心一句话是不是真的，而是关心它出现过多少次。广告、政治口号、童年评价、平台信息流都在利用这个机制。作者的主张是: 既然别人一直在写入我们的第一反应，我们也可以有意识地写入自己选择的反应。")
    lines.append("\n这也是全书最值得带走的一点: 改变不是从“我想通了”开始，而是从“我让新的反应变熟了”开始。")

    lines.append("\n## 反常识洞见")
    counterintuitive = [
        "意志力不是弱，而是来得太晚。它常常在旧反应已经启动后才介入。",
        "让一句话重复到熟悉，比让自己一次性相信它更重要。",
        "脚本越宏大越没用，越小、越具体、越能被身体执行，越可能进入半秒。",
        "刚开始觉得蠢不是失败，而是新脚本正在碰到旧身份。",
        "学习如果没有改变第一反应，还只是解释能力变强，不是行为真的变了。",
    ]
    lines.extend(f"- {item}" for item in counterintuitive)

    lines.append("\n## 章节要点")
    chapter_notes = [
        "序言: 作者用戒烟经历引出全书。真正起作用的不是一次壮烈决定，而是一句短脚本经过大量重复后，改变了“我是吸烟者”这个默认身份。",
        "Ch1: 半秒揭示真实状态。人真正会做什么，常常不是看他事后怎么解释，而是看刺激出现后的第一反应。",
        "Ch2: 意志力不是弱工具，而是错工具。它试图在旧反应已经启动后接管现场。",
        "Ch3: 第一反应默认不是自己写的。广告、平台、他人的语言和早年经验，都在写入我们的默认反应。",
        "Ch4: 熟悉感会伪装成正确感。系统一更常问“我见过这个吗”，而不是“这是真的吗”。",
        "Ch5: 身份是枢纽。改一个身份级默认值，往往比逐个压制动作更省力。",
        "Ch6: 脚本必须写动作，不写心情。“我保持冷静”不可执行，“我先停三秒再回答”才可执行。",
        "Ch7: ARISE 是脚本设计框架。Action 是必需的，Identity、Situation、Reason、Emotion 是可选维度。",
        "Ch8: 这套方法不是普通肯定句。普通肯定句容易被理性审查和驳回，脚本要绕开争辩，进入重复和熟悉。",
        "Ch9: 声音、语法人称和语言会影响安装。你用谁的声音说、用第几人称说、用哪种语言说，都会改变抵抗程度。",
        "Ch10: 真实情绪会加速安装，表演出来的情绪会失败。关键是诚实，不是戏剧化。",
        "Ch11: 初期觉得蠢是正常的。抗拒感不是失败信号，反而说明新脚本正在碰到旧默认值。",
        "Ch12: 不必枚举所有情境。身份级脚本可以在任何想起来的地方重复，计数比地点更重要。",
        "Ch13: 安装后还要维护。环境每天都在继续写入，所以维护不是附加动作，而是常规保养。",
        "Ch14: 金钱行为也是第一反应问题。很多理财差异不在知识，而在面对价格、波动、账单时的默认动作。",
        "Ch15: 最伤人的第一反应常常是自我攻击。童年装进来的声音，可以用同一机制慢慢改写。",
        "Ch16: 冲突和亲密关系由很多小半秒组成。真正破坏关系的，经常不是大事件，而是一次次自动防御、冷处理和反击。",
        "Ch17: 打断坏反应比建设新反应容易。前者是拦截，后者是搭系统，需要更多脚本和更长维护。",
        "Ch18: 如果学习没有改变第一反应，它还没有完成。知道不等于会做，能进入反应才算学到。",
        "Ch19: 结尾很硬: 键盘就在桌上，坐下，或者不坐下。方法最后必须落到行动。",
    ]
    lines.extend(f"- {note}" for note in chapter_notes)

    lines.append("\n## ARISE 方法")
    lines.append("\nARISE 是写脚本的框架。不要把它理解成五个都必须填的表格。真正必须有的只有 Action，其他维度是为了让脚本更稳。")
    lines.append("\n### 1. Action: 动作")
    lines.append("\n先写身体能执行的动作。判断标准很简单: 外人能不能看见你做了什么？")
    lines.append("\n好例子:\n\n- 我先停三秒再回复。\n- 我看到价格大幅波动后，一整天不操作。\n- 我打开账单后立刻看第一项。")
    lines.append("\n坏例子:\n\n- 我不焦虑。\n- 我保持理性。\n- 我成为更好的人。")
    lines.append("\n这些不是动作，是愿望。")
    lines.append("\n### 2. Scope: 范围")
    lines.append("\n脚本可以是普遍的，也可以是情境化的。普遍脚本适合诚实地覆盖一整类反应，比如“我不抽烟”。情境脚本适合特定触发点，比如“当账单到来，我在一分钟内打开它”。判断问题: 这个动作真的适用于所有相关场景吗？如果不是，就写成具体情境。")
    lines.append("\n### 3. Identity: 身份")
    lines.append("\n身份通常不必明写。动作本身会携带身份。“我不抽烟”已经在安装非吸烟者身份。“我按周做决定，不按分钟做决定”已经在安装长期主义者身份。不要急着写“我是一个……的人”。如果动作足够清楚，身份会从动作里长出来。")
    lines.append("\n### 4. Situation: 情境")
    lines.append("\n情境要具体、会重复、能在旧反应启动前被识别。好情境包括“当她用那种语气说话时”“当价格波动超过 5% 时”“当账单邮件出现时”。弱情境包括“当我压力很大时”“当我有空时”“当我想改变时”。太模糊的情境通常来得太晚。")
    lines.append("\n### 5. Reason: 理由")
    lines.append("\n理由不是用来感动别人，而是让自己在第 1000 次重复时仍然点头。好理由要短、真、能长期站得住。一个脚本，一个理由。比如面对投资波动，“因为同一个数字明天看起来会不一样”比“因为投资需要耐心”更有力。")
    lines.append("\n### 6. Emotion: 情绪")
    lines.append("\n情绪不是一个固定槽位，而是增强安装的燃料。它可以在词语里、理由里、记忆里，也可以在说这句话的语气里。但情绪必须是真的。假装愤怒、假装坚定、假装乐观，都会把注意力拉回理性审查。")

    lines.append("\n## 方法论卡片")
    method_cards = [
        ("识别旧反应", "找出你在什么刺激后自动做什么。", "反应必须具体，不能写成“我状态不好”。", "适合处理反复发生的关系、金钱、写作和自我评价场景。"),
        ("定位半秒线索", "找到旧反应启动前最早能识别的外部或身体线索。", "如果线索太抽象，比如“压力大”，通常已经太晚。", "用于把模糊问题压缩成可拦截入口。"),
        ("写动作脚本", "用现在时写一个身体能执行的新动作。", "不要写情绪目标，比如“我很冷静”。", "适合把价值观变成第一动作。"),
        ("重复到熟悉", "不追求立刻相信，只追求重复次数和熟悉感。", "觉得蠢不是停止信号。", "适合任何新身份还没站稳的阶段。"),
        ("维护默认值", "脚本稳定后仍偶尔重复，抵抗环境重新写入。", "旧反应偶尔冒头不是失败，是维护信号。", "适合长期习惯、关系模式和投资纪律。"),
    ]
    for title_, definition, boundary, scenario in method_cards:
        lines.append(f"- {title_}: {definition} 边界: {boundary} 应用: {scenario}")

    lines.append("\n## 九宫格提取")
    grid_items = [
        ("书名", "The Half Second"),
        ("问题", "如何改写刺激出现后的第一反应？"),
        ("阿哈", "改变不是从想通开始，而是从让新反应变熟开始。"),
        ("概念", "half-second / frequency counter / script / identity hub"),
        ("核心", "用可执行脚本重复写入默认反应。"),
        ("案例", "戒烟、投资波动、账单回避、关系防御、自我攻击。"),
        ("书单延伸", "习惯、认知心理学、行为设计、主题阅读。"),
        ("感悟", "半秒里装不下宏大叙事，只装得下一个动作。"),
        ("接下来做", "选一个旧反应，写一个动作脚本，测试 7 天。"),
    ]
    for key, value in grid_items:
        lines.append(f"- {key}: {value}")

    lines.append("\n## 读后行动闭环")
    action_loop = [
        "读前三问: 我为何读？我要解决什么具体问题？读完打算做什么？",
        "读后回答: 这本书解决的是第一反应改写问题；核心工具是可执行脚本；下一步是测试一个脚本。",
        "行动目标: 选一个高频旧反应，在 7 天内用新动作替换。",
        "现实差距: 旧反应通常启动太快，靠事后反省来不及。",
        "最小行动 MVP: 写一句“当 X 时，我做 Y，因为 Z”，每天重复并记录抗拒。",
        "迭代信号: 抗拒从别扭变成烦躁，再变成普通；旧反应偶尔冒头时做维护重复。",
    ]
    for item in action_loop:
        lines.append(f"- {item}")

    if mode == "baopo":
        lines.append("\n## 33 张知识卡片框架")
        card_groups = [
            ("概念卡 x10", ["half-second", "first reaction", "frequency counter", "script", "identity hub", "System 1", "System 2", "universal script", "situated script", "maintenance"]),
            ("框架卡 x6", ["ARISE", "半秒时间层", "身份-情境-动作", "安装-抗拒-熟悉", "坏反应拦截", "好反应建设"]),
            ("问题卡 x5", ["我要改哪个旧反应？", "最早线索是什么？", "动作是否可观察？", "理由是否真实？", "何时需要维护？"]),
            ("案例卡 x5", ["戒烟", "投资波动", "账单回避", "亲密关系防御", "自我攻击"]),
            ("行动卡 x5", ["写旧反应", "找触发线索", "写动作脚本", "重复 7 天", "记录维护信号"]),
            ("总结构卡 x2", ["本书机制总图", "个人反应改写流程"]),
        ]
        for group, items in card_groups:
            lines.append(f"\n### {group}")
            for item in items:
                if item == "half-second":
                    lines.append("- half-second: 刺激出现后、理性解释赶到前的第一反应窗口。边界: 它不是万能控制点，强创伤或化学依赖需要专业支持。应用: 争吵、冲动消费、拖延启动前的拦截。")
                elif item == "first reaction":
                    lines.append("- first reaction: 未经充分思考就自动启动的身体、语言或注意力反应。边界: 不能把所有选择都归因于第一反应。应用: 找到真正需要改写的旧默认动作。")
                elif item == "frequency counter":
                    lines.append("- frequency counter: 大脑把高频出现误判为更熟悉、更自然的机制。边界: 熟悉不等于真实。应用: 用重复让新脚本逐渐变成默认反应。")
                elif item == "script":
                    lines.append("- script: 一句短、具体、可执行的反应指令。边界: 不是情绪口号或人格宣言。应用: 写成“当 X 时，我做 Y，因为 Z”。")
                elif item == "identity hub":
                    lines.append("- identity hub: 身份级默认值会影响一串具体行为。边界: 身份不能脱离动作空喊。应用: 用一个动作安装“我就是这样做的人”。")
                elif item == "System 1":
                    lines.append("- System 1: 快速、自动、依赖熟悉感的反应系统。边界: 快不代表错。应用: 把好动作训练到无需临场思考。")
                elif item == "System 2":
                    lines.append("- System 2: 慢速、解释、审查和计划的理性系统。边界: 它经常晚于旧反应。应用: 在事前设计脚本，而不是事后责备自己。")
                elif item == "universal script":
                    lines.append("- universal script: 适用于一整类场景的普遍脚本。边界: 如果场景差异太大，会变成空泛口号。应用: 戒烟、停止自我攻击等明确边界行为。")
                elif item == "situated script":
                    lines.append("- situated script: 由具体触发情境启动的脚本。边界: 情境不能太模糊。应用: “当账单邮件出现时，我一分钟内打开”。")
                elif item == "maintenance":
                    lines.append("- maintenance: 新反应稳定后仍需定期重复和校准。边界: 维护不是重新失败。应用: 环境压力变大或旧反应回潮时恢复练习。")
                elif item == "ARISE":
                    lines.append("- ARISE: 用 Action、Reason、Identity、Situation、Emotion 设计脚本的框架。边界: 必填只有 Action。应用: 把模糊目标压缩成可执行新动作。")
                elif item == "半秒时间层":
                    lines.append("- 半秒时间层: 把行为分成旧反应启动前后两个窗口。边界: 不是精确神经时间测量。应用: 判断该事前训练还是事后复盘。")
                elif item == "身份-情境-动作":
                    lines.append("- 身份-情境-动作: 用身份稳定方向，用情境识别入口，用动作完成替换。边界: 三者缺一会降低可执行性。应用: 写关系沟通或投资纪律脚本。")
                elif item == "安装-抗拒-熟悉":
                    lines.append("- 安装-抗拒-熟悉: 新脚本从别扭到普通的过程。边界: 强烈痛苦不应硬扛。应用: 判断练习是否进入正常阻力区。")
                elif item == "坏反应拦截":
                    lines.append("- 坏反应拦截: 在旧动作启动前插入一个更小的新动作。边界: 只能先拦截一个高频场景。应用: 防止争吵升级、避免追涨杀跌。")
                elif item == "好反应建设":
                    lines.append("- 好反应建设: 为长期目标建立默认启动动作。边界: 比拦截坏反应更慢。应用: 写作、运动、学习的启动脚本。")
                elif item.startswith("我要") or item.endswith("？"):
                    lines.append(f"- {item}: 用来检验脚本是否具体、真实、可执行。边界: 不能停留在反思，要逼出一个动作。应用: 写脚本前逐题回答。")
                elif item in {"戒烟", "投资波动", "账单回避", "亲密关系防御", "自我攻击"}:
                    lines.append(f"- {item}: 书中或可迁移的第一反应场景。边界: 严重成瘾、创伤或财务危机需要专业方案。应用: 把场景拆成触发线索、旧反应、新动作。")
                elif item in {"写旧反应", "找触发线索", "写动作脚本", "重复 7 天", "记录维护信号"}:
                    lines.append(f"- {item}: 反应改写流程中的一个动作。边界: 不要同时处理多个旧反应。应用: 作为 7 天实验的每日检查项。")
                elif item == "本书机制总图":
                    lines.append("- 本书机制总图: 环境写入熟悉感，熟悉感推动第一反应，脚本通过重复改写默认值。边界: 这是实践模型，不是完整心理学理论。应用: 解释为什么事前练习比事后自责更有效。")
                else:
                    lines.append("- 个人反应改写流程: 旧反应 -> 触发线索 -> 新动作脚本 -> 重复安装 -> 维护复盘。边界: 不替代医疗、法律或高风险决策支持。应用: 把读书收获转成一周实验。")

    lines.append("\n## 已知领域连接")
    transfer_links = [
        "写作: 类似“开头仪式”。可迁移原则是先设计启动动作，而不是等灵感。边界是脚本不能替代素材积累。",
        "投资: 类似“交易纪律”。可迁移原则是在波动前预写动作。边界是脚本不能替代风险管理和仓位规则。",
        "亲密关系: 类似“暂停-澄清”。可迁移原则是把防御反应换成可观察动作。边界是暴力、操控或严重伤害不能靠脚本解决。",
        "学习: 类似“提取练习”。可迁移原则是重复让新反应变熟。边界是机械重复不能替代理解和反馈。",
        "产品使用: 类似“默认选项设计”。可迁移原则是环境会写入反应。边界是不要用它操控他人。 ",
    ]
    lines.extend(f"- {item}" for item in transfer_links)

    lines.append("\n## 跨场景迁移矩阵")
    migration = [
        "争吵回复: 触发=看到刺耳消息；旧反应=立即反击；新动作=停三秒问一个澄清问题；失败边界=对方持续攻击时退出对话；验证信号=争吵升级次数下降。",
        "拖延启动: 触发=打开任务文档；旧反应=切到别的页面；新动作=只写第一行标题；失败边界=任务目标不清需先拆需求；验证信号=启动时间缩短。",
        "冲动消费: 触发=看到限时折扣；旧反应=立刻下单；新动作=加入清单 24 小时后再看；失败边界=刚需物品不适用；验证信号=后悔购买减少。",
        "投资波动: 触发=价格大幅下跌；旧反应=频繁刷新或卖出；新动作=关闭行情并看仓位规则；失败边界=基本面重大变化需重新评估；验证信号=非计划交易减少。",
        "自我攻击: 触发=犯错；旧反应=骂自己；新动作=写下一条可修正动作；失败边界=持续绝望需寻求专业支持；验证信号=恢复行动速度变快。",
    ]
    lines.extend(f"- {item}" for item in migration)

    lines.append("\n## 7 天复盘日志")
    review_items = [
        "第 1 天: 记录触发线索、重复次数、抗拒等级 1-5、旧反应是否发生、明天调整。",
        "第 2 天: 检查脚本是否太长，必要时压缩到一口气能说完。",
        "第 3 天: 检查动作是否可观察，删掉情绪词和人格宣言。",
        "第 4 天: 检查理由是否真实，换掉让自己反感的漂亮话。",
        "第 5 天: 观察抗拒是否从别扭变成普通烦躁。",
        "第 6 天: 在一个真实触发场景中执行一次，不追求完美。",
        "第 7 天: 判断保留、修改或停止；依据是旧反应次数、启动速度和恢复速度。",
    ]
    lines.extend(f"- {item}" for item in review_items)

    lines.append("\n## 教学输出包")
    teaching_pack = [
        "60 秒讲法: 人的很多行为不是想清楚后才发生，而是在刺激后的半秒里已经启动。要改变，不是等事后用意志力压制，而是在事前写一个短动作脚本，重复到它变熟。",
        "类比 1: 像快捷键，不是每次重新找菜单，而是先把常用动作绑定好。",
        "类比 2: 像输入法联想，出现次数多的词会更容易跳出来。",
        "类比 3: 像默认路线，走得越多越自动，但仍然可以重新铺一条路。",
        "5 个问题: 旧反应是什么？最早线索是什么？新动作是什么？理由是否真实？7 天后看什么信号？",
        "1 个练习: 写一句“当 X 时，我做 Y，因为 Z”，今天重复 20 次，明天在真实场景试一次。",
        "常见误解: 这不是肯定句，不是让你假装积极，也不是用一句话解决所有心理问题。",
    ]
    lines.extend(f"- {item}" for item in teaching_pack)

    lines.append("\n## 为什么它不同于肯定句、NLP 或鸡汤")
    lines.append("\n普通肯定句常常写状态，比如“我很自信”“我很富足”“我值得成功”。问题是，这些句子很容易被脑内另一个声音反驳: 你没有啊，你凭什么啊，你又失败了。")
    lines.append("\n这本书的脚本方法不跟这个声音辩论。它把目标缩小到一个动作，让系统一可以执行，让熟悉性计数器可以累计。它的重点不是“相信自己”，而是“重复一个具体动作身份，直到它变熟”。这是更朴素，也更难偷懒的方法。")

    lines.append("\n## 适用边界")
    lines.append("\n适合:\n\n- 戒掉或打断一个具体坏反应。\n- 改写金钱、冲突、自我评价里的自动动作。\n- 把已经认可的价值变成第一反应。\n- 给学习、写作、运动等行为补一个启动脚本。")
    lines.append("\n不适合单独使用:\n\n- 严重创伤、复杂 PTSD、解离反应。\n- 酒精、阿片、苯二氮卓类等化学依赖。\n- 躁狂、精神病性症状、重度抑郁等急性精神状态。\n- 技术动作本身，比如小提琴、竞技体育、复杂手艺。\n- 会压过真实偏好的身份脚本。")

    lines.append("\n## 今天就能做的第一个实验")
    lines.append("\n只选一个旧反应。不要贪多。")
    lines.append("\n1. 写下旧反应: 我在什么刺激后，总是自动做什么？")
    lines.append("2. 找到半秒位置: 旧反应启动前，最早能识别的线索是什么？")
    lines.append("3. 写一个动作: 身体能做，外人能看见，半秒内能开始。")
    lines.append("4. 写成脚本: 用现在时，短到一口气能说完。")
    lines.append("5. 重复 7 天: 不追求感觉神圣，只追求次数和熟悉。")
    lines.append("6. 记录抗拒: 觉得蠢、假、别扭时，不急着改。先看它会不会变成轻微烦躁，再变成普通。")
    lines.append("\n模板:\n\n- 旧反应: 当我看到消息语气不对，我立刻防御。\n- 新动作: 我先停三秒，再问一个澄清问题。\n- 脚本: 当我想反击时，我停三秒，问一句具体问题。\n- 理由: 因为关系比赢这一句重要。")

    lines.append("\n## 选读法门")
    lines.append("- 判断: 本书属压缩型单概念书，适合“一件事、一个模型、一组脚本”的快读法，不必逐章平均用力。")
    lines.append("- 压缩读法: 精读机制章与 2-3 个最相关场景，同质化案例只做一句话记录。")
    lines.append("- 保真提醒: 唯一需要慢读的是“半秒窗口”与“熟悉性计数器”这两个机制定义，别把它读成励志口号。")

    lines.append("\n## 模型证伪与反例")
    lines.append("- 模型解释不了的点: 强创伤、化学依赖、急性精神状态下，“写脚本+重复”无法独立改写第一反应。")
    lines.append("- 我可能读错的地方: 容易把脚本当成更高级的肯定句，从而忽略“动作可观察”这一硬约束。")
    lines.append("- 作者会反对我的地方: 作者会反对把它用于压过真实偏好、或替代专业治疗与复杂决策。")
    lines.append("- 预测检验: 给一个书里没写的新触发场景，你能否预测作者会要求先写哪个可观察动作？")

    lines.append("\n## 复用调度")
    lines.append("- 间隔复盘: 7 天看脚本是否进入熟悉、30 天看旧反应频率、90 天看是否需要维护重写。")
    lines.append("- 撞旧模型: 把“半秒脚本”与你已知的习惯回路、刺激-反应模型对照，看边界差异。")
    lines.append("- 跨书连接: 与习惯养成、认知行为、行为设计类书对读，避免把单一机制当万能解。")
    lines.append("- 调用触发: 选定一个高频旧反应，下次它出现时主动调用本书脚本执行一次。")

    lines.append("\n## 复习卡片")
    cards = [
        ("这本书说的 half-second 是什么？", "刺激出现后、理性解释赶到前，第一反应已经启动的窗口。"),
        ("为什么意志力经常失败？", "因为它通常在旧反应已经开始后才介入，只能追赶，不能提前改写。"),
        ("什么是 frequency counter？", "熟悉性计数器。它把“出现得多”误当作“更真、更自然、更像我”。"),
        ("一个好脚本必须先写什么？", "Action，也就是具体动作。没有动作，脚本就只是愿望。"),
        ("为什么“我很冷静”不是好脚本？", "它是情绪目标，不是可执行动作。半秒内身体不知道该做什么。"),
        ("什么时候用普遍脚本？", "当动作诚实地适用于整个场景类别时，比如“我不抽烟”。"),
        ("什么时候用情境脚本？", "当动作只在某个具体线索出现时才有意义，比如“当账单来了，我一分钟内打开”。"),
        ("为什么刚开始觉得蠢不是坏事？", "因为新脚本正在撞上旧默认值。抗拒感说明它不是无关噪音。"),
        ("维护为什么重要？", "环境每天都在继续写入反应。安装完成后，偶尔重复是保养，不是失败。"),
        ("学习什么时候才算完成？", "当它能改变第一反应，而不只是让你事后解释得更漂亮。"),
    ]
    for question, answer in cards:
        lines.append(f"- Q: {question}\n  A: {answer}")

    lines.append("\n## 阅读计划")
    lines.append("\n- 30 分钟: 读序言、章节地图、Takeaways 和 ARISE cheatsheet。目标是判断这本书能不能立刻帮你改一个反应。")
    lines.append("- 2 小时: 深读 Ch1-Ch7、Ch11-Ch13。目标是掌握机制、脚本格式、重复方式和维护方式。")
    lines.append("- 完整阅读: 全书通读后，只选一个个人脚本，连续测试 7 天。不要同时做三个。")

    lines.append("\n## 我的脚本草稿")
    lines.append("\n- 旧的第一反应:")
    lines.append("- 最早触发线索:")
    lines.append("- 新动作:")
    lines.append("- 脚本句子:")
    lines.append("- 是否普遍适用:")
    lines.append("- 如果不是，具体情境:")
    lines.append("- 理由:")
    lines.append("- 可投入的真实情绪:")
    lines.append("- 7 天重复方式:")
    lines.append("- 维护信号:")

    lines.append("\n## 我的应用建议")
    lines.append("\n这本书最容易被误用成“再找一句更厉害的话”。不要这样用。")
    lines.append("\n真正要做的是把一个旧反应拆到很小，然后写一个很朴素的新动作。朴素到你觉得“不就这？”通常才对。半秒里装不下宏大叙事，只装得下一个动作。")
    lines.append("\n我会从关系、金钱、写作这三类里选一个开始。优先选已经反复伤害你的场景，而不是最宏大的目标。脚本不是人生宣言，是反应补丁。")

    return "\n".join(lines).rstrip() + "\n"


def top_terms(full_text: str, limit: int = 12) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z-]{3,}|[\u4e00-\u9fff]{2,}", full_text)
    stop = {
        "this", "that", "with", "from", "have", "will", "book", "chapter", "there", "their",
        "about", "which", "when", "what", "would", "could", "should", "into", "your",
    }
    counts: dict[str, int] = {}
    for word in words:
        key = word.lower()
        if key in stop or key.isdigit():
            continue
        counts[key] = counts.get(key, 0) + 1
    return [word for word, _ in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:limit]]


def evidence_quality(metadata: dict, chapters: object, full_text: str) -> str:
    word_count = int(metadata.get("total_words_estimate") or 0)
    chapter_count = len(chapters) if isinstance(chapters, list) else 0
    if word_count < 2000:
        return "low"
    if word_count < 12000 or chapter_count < 3:
        return "medium"
    return "high"


def build_generic_notes_zh(metadata: dict, chapters: object, full_text: str, title: str, author: str, mode: str) -> str:
    lines: list[str] = []
    quality = evidence_quality(metadata, chapters, full_text)
    terms = top_terms(full_text)
    append_book_header(lines, title, author, metadata, mode)

    lines.append("\n## 开卷导读")
    lines.append("\n*——先用三个问题锁定你和这本书的关系，再开始读*")
    lines.append("\n### 我读它，为了解决什么问题？")
    lines.append("\n用一句话写下你要这本书帮你解决的具体问题；它决定你精读哪些章、跳过哪些章。")
    lines.append("\n### 有没有一个核心模型？")
    lines.append("\n读完后用「输入 → 机制 → 输出 → 可干预点」把全书压成一个模型；如果压不出，说明还没抓住骨架。")
    lines.append("\n### 读完之后我能做什么？")
    lines.append("\n把模型落成一份能力清单：在什么场景、遇到什么触发、你会改用什么新做法，并设计一个 7 天验证。")

    lines.append("\n## 一页速读")
    lines.append(f"\n评测结论: 当前提取质量为 {quality}。这份笔记先提供问题驱动的阅读支架，核心判断只基于目录、标题、章节边界和高频术语；需要深读后再固化最终结论。")
    lines.append("\n继续策略: 如果这本书能回答你的一个具体问题，继续读；如果只能提供零散背景，保留速读卡即可；如果目录和正文都无法支撑判断，先做 OCR 或换更清晰版本。")

    lines.append("\n## 核心主张")
    lines.append("\n候选书核: 先不要编造最终主张。请用后续精读验证作者到底在解决什么问题、反对什么旧观点、给出什么可执行路径。")

    lines.append("\n## 读前三问与读后回答")
    lines.append("- 我为何读这本书: 为一个具体问题寻找可验证的原则、框架或行动方法。")
    lines.append("- 我要解决什么问题: 从目录和关键词中锁定 3-5 个候选问题，精读时逐个回答。")
    lines.append("- 读完打算做什么: 产出一页海报、完整 HTML 笔记、一个最小行动实验。")
    lines.append("- 读后回答: 当前为初筛版本，完成精读后补成“问题 -> 作者答案 -> 我的行动”。")

    append_chapter_map(lines, chapters)

    lines.append("\n## 结构骨架")
    if isinstance(chapters, list) and chapters:
        for item in chapters[:18]:
            lines.append(f"- p. {item.get('page')}: {item.get('title')} -> 判断它是在提出问题、定义概念、论证原则、给出案例，还是指导行动。")
    else:
        lines.append("- 未识别到可靠目录。先根据标题、段落标题和高频术语人工建立章节骨架。")

    lines.append("\n## 候选核心问题")
    candidate_questions = [
        "作者认为读者最需要解决的核心问题是什么？",
        "作者反对的主流看法或低效做法是什么？",
        "全书最重要的 3 个概念分别解决什么问题？",
        "哪些章节是原则，哪些章节只是例子或背景？",
        "读完后最小可执行动作是什么？",
    ]
    lines.extend(f"- {item}" for item in candidate_questions)

    lines.append("\n## 全书地图")
    lines.append("- 一句话讲什么: 先根据标题、目录和高频术语给出候选判断，精读后再修正。")
    lines.append("- 作者想解决什么问题: 从序言、结论和章节标题中定位。")
    lines.append("- 目标读者: 根据案例、术语难度和行动建议推断。")
    lines.append("- 章节关系: 判断是线性论证、并列工具、案例展开，还是单概念反复展开。")
    lines.append("- 精读优先级: 优先读定义概念、搭建模型、给出方法和关键案例的章节。")
    lines.append("- 略读原则: 背景故事、重复劝说、同质化案例、参考文献先略读。")

    lines.append("\n## 单概念书检测")
    lines.append("- 检测问题: 这本书是否主要围绕一个核心概念换不同场景展开？")
    lines.append("- 判断方法: 看高频关键词是否集中，后半章节是否多为案例和重复劝说。")
    lines.append("- 处理策略: 如果是，就先压缩成“一件事、一个概念、一个模型”，再选 2-3 个代表场景深读。")
    lines.append("- 跳读原则: 同质化案例只记一句话，不做逐章平均总结。")

    lines.append("\n## 提问链")
    lines.append("> [!tip] 用法：问题决定读哪里。每个问题都链到具体章节，答完会逼出下一个更尖的问题，从而驱动取舍，而不是平均读完每一页。")
    generic_questions = [
        "读前·真问题: 我为什么需要这本书，它要解决我的哪个具体问题？这是后续提问的起点。",
        "第1问 → 序言/结论: 作者真正要解决的断点是什么？→ 逼出下一问：他靠一个概念，还是多个独立主题来解决它？",
        "第2问 → 目录/章节标题: 哪些章节在定义概念，哪些只是案例或背景？→ 逼出：核心概念到底怎么定义、边界在哪？",
        "第3问 → 概念章: 这个核心概念的机制是什么（输入→机制→输出→干预点）？→ 逼出：作者用什么论据证明它可靠？",
        "第4问 → 论证/案例章: 证据够不够，有没有反例？→ 逼出：它能迁移到我的哪个场景，什么情况下不适用？",
        "读后·收摄: 只带走一招，我能做一个什么 7 天实验来验证它？",
    ]
    lines.extend(f"- {item}" for item in generic_questions)

    lines.append("\n## 高频术语线索")
    if terms:
        for term in terms:
            lines.append(f"- {term}: 作为候选概念，精读时补充定义、边界和应用场景。")
    else:
        lines.append("- 当前提取文本不足，无法稳定识别术语。")

    lines.append("\n## 关键词地图")
    lines.append("- 核心词: 从高频术语中选 1-3 个最能解释全书的概念。")
    lines.append("- 支撑词: 记录帮助作者论证核心概念的理论、案例和机制。")
    lines.append("- 行动词: 记录作者要求读者做的动作，例如比较、记录、练习、测试、复盘。")
    lines.append("- 边界词: 记录作者承认的限制、反例、不适用场景和风险。")

    lines.append("\n## 金句与可转述句")
    lines.append("- 原文短句: 只收能代表核心主张的短句，并在可能时标页码。")
    lines.append("- 可转述句: 用自己的话把作者主张压成更好讲、更好用的一句话。")
    lines.append("- 使用场景: 标注这句话适合用于海报、教学、行动提醒还是概念复习。")
    lines.append("- 误用边界: 标注这句话什么时候会被过度泛化或误解。")

    lines.append("\n## 费曼讲解卡")
    lines.append("- 讲给小孩: 用一个生活类比解释核心概念。")
    lines.append("- 讲给同事: 用“问题 -> 模型 -> 例子 -> 行动”讲清楚。")
    lines.append("- 讲给自己: 写成下一次遇到相关场景时能立刻执行的一句话。")
    lines.append("- 检验标准: 如果讲解里没有例子和动作，就还没有真正理解。")

    lines.append("\n## 观点卡 方法卡 案例卡")
    lines.append("- 观点卡: 记录作者最重要的判断、原则或反常识。格式: 观点是什么；反例是什么；能改变哪个判断。")
    lines.append("- 方法卡: 记录作者给出的行动步骤。格式: 做什么；按什么顺序；风险和边界是什么。")
    lines.append("- 案例卡: 记录最能解释观点的具体场景。格式: 场景；冲突；做法；结果；可迁移原则。")

    lines.append("\n## 写作外化")
    lines.append("- 一句话解释: 用自己的话写出这本书最有用的观点。")
    lines.append("- 一段话解释: 用“问题 -> 作者答案 -> 一个例子 -> 我的行动”写成 150 字。")
    lines.append("- 系列文章入口: 如果主题值得长期研究，拆成 3 篇短文: 概念定义、方法实践、案例复盘。")

    lines.append("\n## 体系化输出")
    lines.append("- 体系图: 画出核心概念、支撑概念、行动步骤和反馈环。")
    lines.append("- 主题研究报告: 用“体系图 -> 系列文章 -> 观点优化”组织材料。")
    lines.append("- 拼图原则: 主动寻找不同观点，包括自己可能反对的观点，不要只找答案。")

    lines.append("\n## 反常识洞见")
    lines.append("- 待读验证 1: 找作者明确反对的常识判断，确认其论据是否充分。")
    lines.append("- 待读验证 2: 找与读者原有经验冲突但可实践检验的观点。")
    lines.append("- 待读验证 3: 找“看似低效但长期有效”或“看似正确但实际有害”的论点。")

    lines.append("\n## 章节精读模板")
    lines.append("- 一句话总结: 本章到底推进了哪个问题？")
    lines.append("- 核心观点: 作者最想让读者接受什么判断？")
    lines.append("- 关键概念: 本章新增或重新定义了什么概念？")
    lines.append("- 关键案例: 哪个例子最能证明观点？")
    lines.append("- 论证逻辑: 前提、推理、证据、结论分别是什么？")
    lines.append("- 可能问题: 哪个前提可疑，哪个边界没有说清？")
    lines.append("- 对我启发: 它改变了我哪个判断或行动？")
    lines.append("- 可执行建议: 今天或本周能做什么？")

    lines.append("\n## 方法论卡片")
    method_cards = [
        "评测: 先看标题、目录、序言、结论和外部评价，决定继续读、只速读、跳读或暂不读。边界: 信息不足时不要伪造判断。应用: 10 分钟决定时间投入。",
        "提问: 把阅读目标写成 3-7 个问题。边界: 问题太泛会导致摘抄堆积。应用: 每章只为回答问题而读。",
        "扫读: 用标题、首尾段、图表、转折词和概念密度找重点。边界: 不适合小说审美阅读。应用: 30 分钟建立全书地图。",
        "休息: 速读后暂停，让大脑自动过滤弱信息。边界: 不是拖延，必须约定返回时间。应用: 精读前间隔 30 分钟到 1 天。",
        "精读: 只对能回答核心问题的章节逐段拆论点和论据。边界: 不从头到尾平均用力。应用: 把 20% 高价值内容读透。",
        "输出: 用九宫格、卡片、教学脚本和行动实验逼迫理解。边界: 不输出就难以发现理解漏洞。应用: 读完立刻讲给别人或写 HTML 笔记。",
    ]
    lines.extend(f"- {item}" for item in method_cards)

    lines.append("\n## 九宫格提取")
    grid_items = [
        ("书名", title),
        ("问题", "这本书最值得回答的一个问题是什么？"),
        ("阿哈", "精读后填入最颠覆直觉的一句话。"),
        ("概念", "从高频术语中选 3 个核心概念。"),
        ("核心", "用一句话压缩作者主张。"),
        ("案例", "找 1 个能证明主张的关键案例。"),
        ("书单延伸", "找同主题 2-3 本书对读。"),
        ("感悟", "它改变了我哪个旧判断？"),
        ("接下来做", "设计一个 7 天内可验证的小实验。"),
    ]
    for key, value in grid_items:
        lines.append(f"- {key}: {value}")

    lines.append("\n## 已知领域连接")
    lines.append("- 相似概念: 把本书概念连接到你已知的模型，避免孤立记忆。边界: 类比不是证明。应用: 用一个熟悉领域解释新概念。")
    lines.append("- 可迁移原则: 提取“在什么条件下，做什么会产生什么效果”。边界: 缺少条件的原则不可迁移。应用: 写到工作、学习、关系或产品场景。")
    lines.append("- 不可迁移边界: 标出行业、样本、文化、风险等级差异。边界: 不写边界的读书笔记容易变鸡汤。应用: 决定哪些建议不能照搬。")

    lines.append("\n## 跨场景迁移矩阵")
    lines.append("- 工作场景: 触发=遇到类似问题；旧反应=凭经验硬做；新动作=先查本书原则；失败边界=书中证据不适用于当前约束；验证信号=决策质量提升。")
    lines.append("- 学习场景: 触发=遇到新概念；旧反应=摘抄；新动作=写定义、边界、应用；失败边界=概念没有可操作含义；验证信号=能讲给别人听。")
    lines.append("- 生活场景: 触发=遇到重复困扰；旧反应=泛泛自责；新动作=套用一个方法论卡片；失败边界=涉及医疗、法律、财务高风险；验证信号=行为有可观测变化。")

    lines.append("\n## 读后行动闭环")
    lines.append("- 行动目标: 从书中选一个最小方法，在 7 天内验证。")
    lines.append("- 现实差距: 写出当前做不到的具体原因，而不是写“缺少自律”。")
    lines.append("- 最小行动 MVP: 只执行一个动作，能在 15 分钟内开始。")
    lines.append("- 成功标准: 7 天内至少完成 3 次，并记录效果。")
    lines.append("- 失败标准: 连续 3 天无法启动，说明动作过大或问题不真实，需要重写。")
    lines.append("- 迭代信号: 更快启动、更少阻力、更能解释给别人。")
    lines.append("- 反馈周期: 为行动设置明确检查点，短任务 7 天，长期主题 30 天，重大决策 9-12 个月。")

    lines.append("\n## 7 天复盘日志")
    for day in range(1, 8):
        lines.append(f"- 第 {day} 天: 日期、执行次数、阻力等级 1-5、是否出现旧做法、下一步调整。")

    lines.append("\n## 教学输出包")
    lines.append("- 60 秒讲法: 用“问题 -> 作者答案 -> 一个例子 -> 我的行动”讲清楚。")
    lines.append("- 3 个类比: 分别连接工作、学习、生活场景。")
    lines.append("- 5 个问题: 用来测试别人是否理解核心概念。")
    lines.append("- 1 个练习: 让听众现场完成一个最小应用。")
    lines.append("- 常见误解: 列出最容易把本书用错的 2-3 种方式。")

    lines.append("\n## 全书复盘")
    lines.append("- 核心框架: 用一张图或一条链路呈现全书结构。")
    lines.append("- 10 条关键观点: 只保留能改变判断、行动或表达的观点。")
    lines.append("- 5 个可执行方法: 每个方法都要有使用场景和边界。")
    lines.append("- 3 个深思问题: 能继续驱动主题阅读或实践验证的问题。")
    lines.append("- 最值得重读章节: 标出概念、模型、方法、关键案例所在章节。")
    lines.append("- 可跳读章节: 标出重复论证、背景铺垫、低密度案例。")

    lines.append("\n## 知识资产转换")
    lines.append("- 一页纸读书卡: 书核、结构、反常识、方法、行动。")
    lines.append("- 执行摘要: 面向决策者，用 5 分钟说明为什么值得读、怎么用。")
    lines.append("- 内容选题: 3 个适合写文章、朋友圈或视频的观点。")
    lines.append("- 团队分享/PPT: 10 分钟讲清问题、模型、案例、行动。")
    lines.append("- 产品/业务/管理启发: 转成原则、风险假设和可验证实验。")
    lines.append("- 个人行动计划: 一个 7 天 MVP，一个 30 天复盘点。")

    if mode == "baopo":
        lines.append("\n## 33 张知识卡片框架")
        for group, count in (("概念卡", 10), ("框架卡", 6), ("问题卡", 5), ("案例卡", 5), ("行动卡", 5), ("总结构卡", 2)):
            lines.append(f"\n### {group} x{count}")
            for i in range(1, count + 1):
                lines.append(f"- {group}{i}: 从本书证据中提炼一个独立知识点；需包含含义、使用边界、应用场景，精读确认后固化。")

    lines.append("\n## 选读法门")
    lines.append("- 判断: 这本书该“压缩成一个模型”，还是该“保留复杂性、当成对话来读”？工具/方法书偏前者，思想/历史/文学偏后者。")
    lines.append("- 压缩型读法: 求骨架——锁定一件事、一个模型、几张卡，快速进入行动实验。")
    lines.append("- 保真型读法: 求张力——保留作者的矛盾、细节与未解处，不要把厚书榨成一句口号。")
    lines.append("- 慢热判断: 区分“垃圾”和“暂时看不懂的好东西”，别让评测门槛错杀慢热好书。")

    lines.append("\n## 模型证伪与反例")
    lines.append("- 模型解释不了的点: 找出至少一处本书核心模型无法覆盖的内容，写下来而不是忽略它。")
    lines.append("- 我可能读错的地方: 标出最可能因先入框架而误读的概念或结论。")
    lines.append("- 作者会反对我的地方: 设想作者如何反驳你的压缩，借此检验理解是否诚实。")
    lines.append("- 预测检验: 能否预测作者在书里没写的新情境下会怎么说？答得出才算抓住机制而非结论。")

    lines.append("\n## 复用调度")
    lines.append("- 间隔复盘: 为复习卡片排定 7 天 / 30 天 / 90 天的回看节点，避免卡片沦为墓地。")
    lines.append("- 撞旧模型: 把本书模型与你已有的旧模型对照——它和谁冲突、补充了谁、边界差在哪。")
    lines.append("- 跨书连接: 找 2-3 本同主题书让作者互相争论，避免把一家之言当真理。")
    lines.append("- 调用触发: 约定一个真实场景，下次遇到时主动调出本书的模型来用一次。")

    lines.append("\n## 复习卡片")
    review_cards = [
        ("这本书想解决的核心问题是什么？", "从序言、结论和章节标题定位作者反复回到的那一个问题，用一句话写下来。"),
        ("作者反对的旧观念或低效做法是什么？", "找出作者明确否定的常识，确认他给出的替代主张更可信在哪里。"),
        ("全书最关键的概念有哪些？", "从高频术语中挑出 1-3 个支撑全书论证的概念，补上定义、边界和应用。"),
        ("哪些章节是原理，哪些只是案例？", "原理章节决定理解深度，案例章节只做一句话记录，避免逐章平均用力。"),
        ("读完后最小可执行的行动是什么？", "选一个能在 7 天内验证的动作，而不是再收集更多笔记。"),
        ("这个概念能迁移到我的什么场景，边界在哪里？", "写出可迁移的条件，并标出行业、样本或风险层级不适用的情况。"),
    ]
    for question, answer in review_cards:
        lines.append(f"- Q: {question}\n  A: {answer}")

    lines.append("\n## 阅读计划")
    lines.append("- 30 分钟: 评测、目录骨架、候选问题、九宫格。")
    lines.append("- 2 小时: 精读能回答核心问题的章节，补齐方法论卡片。")
    lines.append("- 完整阅读: 做 33 卡、迁移矩阵、7 天行动实验和教学输出。")

    return "\n".join(lines).rstrip() + "\n"


def build_generic_notes_en(metadata: dict, chapters: object, full_text: str, title: str, author: str, mode: str) -> str:
    lines: list[str] = []
    quality = evidence_quality(metadata, chapters, full_text)
    terms = top_terms(full_text)
    lines.append(f"# {markdown_escape(title)}")
    if author:
        lines.append(f"\nAuthor: {markdown_escape(author)}")
    lines.append(f"\nSource: `{metadata.get('source', '')}`")
    lines.append(f"Pages: {metadata.get('pages', '')}")
    lines.append(f"Estimated words: {metadata.get('total_words_estimate', '')}")
    lines.append(f"Reading mode: {mode}")
    lines.append("\n## One-Page Brief")
    lines.append(f"\nExtraction quality: {quality}. This is a neutral reading scaffold based on structure, headings, and recurring terms. Deep-reading claims must be confirmed before final use.")
    lines.append("\n## Candidate Thesis")
    lines.append("\nDo not invent the final thesis yet. Use the next pass to verify the author's central problem, rejected assumption, argument, and action path.")
    lines.append("\n## Structure Skeleton")
    if isinstance(chapters, list) and chapters:
        for item in chapters[:18]:
            lines.append(f"- p. {item.get('page')}: {item.get('title')}")
    else:
        lines.append("- No reliable table of contents detected. Build a skeleton from headings and recurring terms.")
    lines.append("\n## Candidate Questions")
    for item in (
        "What problem is the author trying to solve?",
        "What common belief or practice does the author reject?",
        "Which concepts carry the argument?",
        "Which sections are principles, and which are examples?",
        "What is the smallest action to test after reading?",
    ):
        lines.append(f"- {item}")
    lines.append("\n## Term Signals")
    for term in terms or ["insufficient extracted text"]:
        lines.append(f"- {term}: candidate concept for definition, boundary, and application.")
    lines.append("\n## Nine-Grid Extraction")
    for key, value in (
        ("Title", title),
        ("Question", "What is the highest-value question this book can answer?"),
        ("Aha", "Fill after deep reading."),
        ("Concepts", "Select three core terms."),
        ("Core", "Compress the thesis into one sentence."),
        ("Case", "Find one decisive example."),
        ("Further reading", "Choose two to three comparison books."),
        ("Reflection", "What old belief changed?"),
        ("Next action", "Run a seven-day experiment."),
    ):
        lines.append(f"- {key}: {value}")
    lines.append("\n## Action Loop")
    for item in (
        "Goal: choose one method from the book and test it within seven days.",
        "Gap: state what currently blocks use.",
        "MVP: one action that starts within 15 minutes.",
        "Success signal: at least three attempts and recorded effects.",
        "Iteration signal: lower friction, faster start, better explanation.",
    ):
        lines.append(f"- {item}")
    lines.append("\n## Review Cards")
    for question, answer in (
        ("What problem can this book solve?", "Confirm from the author's thesis and chapter structure."),
        ("What are the central concepts?", "Use recurring terms, then verify definitions in the text."),
        ("When should I apply it?", "Only when the book's conditions match the current scenario."),
        ("What is the boundary?", "Mark evidence gaps, domain limits, and high-risk cases."),
        ("What will I do next?", "Run one small experiment rather than collect more notes."),
    ):
        lines.append(f"- Q: {question}\n  A: {answer}")
    return "\n".join(lines).rstrip() + "\n"


def build_notes_en(extract_dir: Path, mode: str = "baopo") -> str:
    metadata = load_json(extract_dir / "metadata.json")
    chapters = load_json(extract_dir / "chapters.json")
    full_text = read_text(extract_dir / "full-text.txt")
    title, author = detect_identity(full_text, metadata)
    if not is_half_second_book(title, chapters):
        return build_generic_notes_en(metadata, chapters, full_text, title, author, mode)
    takeaways = extract_takeaways(full_text)
    arise = extract_arise(full_text)

    lines: list[str] = []
    lines.append(f"# {markdown_escape(title)}")
    if author:
        lines.append(f"\nAuthor: {markdown_escape(author)}")
    lines.append(f"\nSource: `{metadata.get('source', '')}`")
    lines.append(f"Pages: {metadata.get('pages', '')}")
    lines.append(f"Estimated words: {metadata.get('total_words_estimate', '')}")
    lines.append("\n## One-Page Brief")
    lines.append("\n- Best use case: practical behavior change where first reactions matter.")
    lines.append("- Recommendation: deep-read the mechanism chapters and the ARISE cheatsheet; skim references unless researching evidence.")
    lines.append("- Core thesis: durable change happens when the first half-second reaction is edited, not when willpower tries to override it later.")
    lines.append("- Practical output: choose one concrete action script, repeat it past the protest phase, and maintain it against environmental rewriting.")

    lines.append("\n## Chapter Map")
    if isinstance(chapters, list):
        for item in chapters:
            lines.append(f"- p. {item.get('page')}: {item.get('title')}")

    lines.append("\n## Chapter Takeaways")
    if takeaways:
        for item in takeaways:
            lines.append(f"- {item}")
    else:
        lines.append("- No explicit takeaways section detected. Fill from chapter notes.")

    lines.append("\n## ARISE Practice Sheet")
    lines.append("\nUse this to write one script at a time.")
    lines.append("\n- Action: What observable behavior should run in the half-second?")
    lines.append("- Scope: Universal (`I never...`, `I always...`) or situated (`When X, I...`)?")
    lines.append("- Identity: What kind of person does this action install?")
    lines.append("- Situation: What exact cue starts the old reaction?")
    lines.append("- Reason: What short, honest because-clause can survive the thousandth repetition?")
    lines.append("- Emotion: What real felt content can be invested without acting?")
    if arise:
        lines.append("\n### Extracted ARISE Notes")
        for line in arise.splitlines()[:80]:
            lines.append(f"- {line}")

    lines.append("\n## Review Cards")
    cards = [
        ("What is the half-second?", "The stimulus-to-action window where first reactions fire before deliberation catches up."),
        ("Why is willpower insufficient?", "It usually arrives after the old reaction has already begun."),
        ("What must every script contain?", "A concrete action the body can perform."),
        ("What is the common script failure?", "Targeting a mood or attitude instead of an observable behavior."),
        ("When should a script be situated?", "When the desired action only makes sense in a specific recurring cue context."),
    ]
    for question, answer in cards:
        lines.append(f"- Q: {question}\n  A: {answer}")

    lines.append("\n## Reading Plan")
    lines.append("\n- 30 minutes: Prologue, chapter map, Takeaways, ARISE cheatsheet.")
    lines.append("- 2 hours: Prologue, Ch1-Ch7, Ch11-Ch13, Takeaways, ARISE cheatsheet.")
    lines.append("- Full pass: Read all chapters, then write one personal script and test it for seven days.")

    lines.append("\n## Personal Script Draft")
    lines.append("\n- Old first reaction:")
    lines.append("- Cue:")
    lines.append("- New action:")
    lines.append("- Script:")
    lines.append("- Repetition plan:")
    lines.append("- Maintenance signal:")

    return "\n".join(lines).rstrip() + "\n"


def build_notes_zh(extract_dir: Path, mode: str = "baopo") -> str:
    metadata = load_json(extract_dir / "metadata.json")
    chapters = load_json(extract_dir / "chapters.json")
    full_text = read_text(extract_dir / "full-text.txt")
    title, author = detect_identity(full_text, metadata)
    if is_half_second_book(title, chapters):
        return build_half_second_notes_zh(metadata, chapters, title, author, mode)
    return build_generic_notes_zh(metadata, chapters, full_text, title, author, mode)


def build_notes(extract_dir: Path, language: str, mode: str) -> str:
    if language == "zh-CN":
        return build_notes_zh(extract_dir, mode)
    return build_notes_en(extract_dir, mode)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reading-notes.md from an extracted PDF directory.")
    parser.add_argument("extract_dir", type=Path, help="Directory containing full-text.txt, metadata.json, and chapters.json")
    parser.add_argument("--out", type=Path, help="Output Markdown file")
    parser.add_argument("--lang", choices=["en", "zh-CN"], default="en", help="Output language for generated notes")
    parser.add_argument("--mode", choices=["suidan", "baopo", "hedan"], default="baopo", help="Reading depth: suidan, baopo, or hedan")
    args = parser.parse_args()

    for name in ("full-text.txt", "metadata.json", "chapters.json"):
        if not (args.extract_dir / name).exists():
            raise SystemExit(f"Missing {name} in {args.extract_dir}")

    out = args.out or (args.extract_dir / "reading-notes.md")
    out.write_text(build_notes(args.extract_dir, args.lang, args.mode), encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
