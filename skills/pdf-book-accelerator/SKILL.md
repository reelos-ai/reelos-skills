---
name: pdf-book-accelerator
description: Accelerates reading PDF ebooks by extracting structure, producing chapter-level summaries, question-led notes, action lists, review cards, and follow-up reading plans. Use when the user wants to read, skim, summarize, study, learn from, or speed-read a PDF ebook or long-form PDF.
---

# PDF Book Accelerator

## Core principle

Do not summarize a book page by page by default. First discover the book's structure, then read with questions, then produce reusable outputs.

Default professional reading protocol: read `references/professional-reading-methodology.md` for new book tasks, especially when the user gives reading goals, asks for deep extraction, or wants a reusable knowledge system.

Default reading-process protocol: read `references/onion-reading-system.md` when optimizing the reading method, doing fast/deep reading, building card outputs, or turning reading into teaching, writing, posters, or courses.

Default fast-reading protocol: read `references/zhang-kai-fast-reading.md` when deciding whether to continue, skim, skip, rest, deep-read, or force output.

Default concept-compression protocol: read `references/single-concept-books.md` when a book appears to repeat one core concept across many chapters, examples, or application scenes.

Default learning-to-action protocol: read `references/wang-zhuan-learning-system.md` when the user provides learning-method notes, asks to improve the reading skill itself, or wants reading outputs that become writing, knowledge systems, workplace influence, or practical action.

Default knowledge-asset protocol: read `references/knowledge-asset-workflow.md` when the user wants the book converted into reusable assets such as one-page notes, articles, team sharing, PPT outlines, product/business implications, management practices, or personal action plans.

## When triggered

Use this skill when the user provides or mentions a PDF ebook, book manuscript, course PDF, whitepaper, report, or long-form PDF and wants to read faster, understand deeply, extract notes, or build a study plan.

## Workflow

1. **Intake**
   - Confirm the PDF path if missing.
   - Parse the startup protocol if present: book title, author, three pre-reading questions, and reading mode.
   - Ask for the reading goal only when it materially changes the output. If missing, infer a default and mark it as an assumption.
   - Classify the reading goal: quick overview, deep study, writing/content, product/startup, management/organization learning, investment/business research, or personal action.
   - Default reading mode is 爆破模式 for serious PDF book tasks; use 碎弹模式 for quick poster-only tasks; use 核弹模式 for cross-book comparison.
   - For new books, establish the three pre-reading questions: why read, what problem to solve, what to do after reading.

2. **Extract**
   - Run `python3 scripts/extract_pdf.py <pdf> --out <workdir>` from this skill directory.
   - If extraction returns very little text, report that the PDF is likely scanned and OCR is needed.
   - Keep raw extraction separate from synthesized notes.

3. **Map**
   - Build a reading map: title clues, table of contents if present, chapter boundaries, recurring terms, diagrams/tables worth inspecting.
   - Apply `knowledge-asset-workflow.md`: first produce the book map, reading priority, and target knowledge assets before deep chapter work.
   - Detect whether the book is a single-concept repetitive book. If yes, follow `references/single-concept-books.md` and stop treating every chapter as equally important.
   - Start with the user's problem: why read this book, what problem it should solve, and what the reader intends to do after reading.
   - Apply the sequence from `onion-reading-system.md`: evaluation, fast reading, rest, deep reading, forced output.
   - Apply the Zhang Kai gate from `zhang-kai-fast-reading.md`: output 继续读, 只速读, 跳读, or 暂不读 before investing in deep extraction.
   - Use the nine-grid note when a fast-reading extraction table is needed.
   - Build a question chain, keyword map, and golden-sentence bank before writing long summaries.
   - For learning-method books, apply `wang-zhuan-learning-system.md`: convert insights into question chains, keyword maps, cards, system diagrams, writing outputs, and practice feedback.
   - Identify the highest-value 20 percent of the book before writing detailed summaries.

4. **Read in passes**
   - Pass 1: orientation - what the book is about, who it is for, and whether to continue.
   - Pass 2: question-led reading - answer 3-7 guiding questions and update the question chain when a better question appears.
   - Pass 3: keyword-led reading - identify core terms, supporting terms, action terms, and boundary terms.
   - Pass 4: quote-led compression - collect short original gold sentences only when legally and cognitively useful; otherwise write agent-owned paraphrase sentences.
   - Pass 5: output - convert useful ideas into structure, counterintuitive insights, Feynman explanations, methodology cards, and reusable knowledge cards.
   - For learning-method tasks, add a final write-do loop: thought -> card -> short article or explanation -> practice -> feedback -> revised view.
   - For knowledge-asset tasks, add asset conversion: one-page note, executive summary, article/social post, team-sharing outline, PPT outline, product/business/management implications, or personal action plan.

5. **Deliver**
   - Use the output schema in `references/reading-output-schema.md`.
   - Run `python3 scripts/generate_reading_notes.py <extract-dir> --mode baopo --out <extract-dir>/reading-notes.md` to create the working notes file.
   - For Chinese users, run `python3 scripts/generate_reading_notes.py <extract-dir> --lang zh-CN --mode baopo --out <extract-dir>/reading-notes.zh-CN.md`.
   - Final delivery must be HTML: run `python3 scripts/render_reading_html.py <notes.md> --out <extract-dir>/reading-notes.zh-CN.html`.
   - Verify final artifacts: run `python3 scripts/verify_reading_output.py <extract-dir> --md reading-notes.zh-CN.md --html reading-notes.zh-CN.html`.
   - When the user wants quick capture or a poster, deliver a one-page poster HTML first, with a link to the full notes HTML.
   - The Chinese generator may use known-structure adapters. If no adapter matches, treat the output as a neutral scaffold and refine it with `references/chinese-reading-notes.md`; never let known-book concepts pollute unknown-book fallback.
   - Fill or refine the generated notes with synthesis from the extracted text; do not leave placeholders in the final answer unless the user asks for a worksheet.
   - For polished Chinese notes, read `references/chinese-reading-notes.md` after the scaffold is generated.
   - Cite page numbers when extraction provides reliable page boundaries.
   - Separate author claims from the agent's interpretation.
   - Mark uncertain extraction, missing pages, OCR risk, or weak evidence explicitly.

## Default outputs

- One-page poster HTML
- Full reading-notes HTML
- Reading goal and asset target
- Book map and reading priority
- Core thesis
- SVG mental-model diagram when the book has a reusable model
- One-concept diagnosis when applicable
- Structure skeleton
- Question chain
- Keyword map
- Golden sentences and paraphrase bank
- Feynman explanation card
- View/method/case cards
- System diagram or article outline when building a knowledge system
- Counterintuitive insights
- Methodology cards
- Knowledge cards
- Chapter map
- Core arguments
- Practical actions
- Key terms
- Review cards
- Chapter deep-read template for high-value chapters
- Full-book synthesis: 10 key ideas, 5 actions, 3 questions
- Knowledge asset conversion: one-page card, article ideas, team/PPT outline, product/business/management implications
- What to skip, skim, or deep-read
- Generated Markdown artifacts only as intermediate files
- Transfer matrix and 7-day application log when the goal is practical use
- Teaching output package when the user wants to explain or internalize the book

## Quality rules

- Preserve the author's argument structure before judging it.
- Prefer concise, useful synthesis over exhaustive summaries.
- Build the map before details; choose depth before summarizing chapters.
- Convert useful insights into knowledge assets, not just notes.
- When a book's value is a model, render the model as SVG: name the model, show inputs, mechanism, output, intervention point, and usage formula.
- For repetitive single-concept books, optimize for concept compression and transfer, not chapter coverage.
- Use questions to decide what to read, keywords to decide what to extract, and gold sentences/paraphrases to decide what to remember.
- For learning-method books, treat writing as thinking: if a claim cannot be written clearly, do not mark it as understood.
- Separate card types: 观点卡 for how to think, 方法卡 for how to act, 案例卡 for concrete scenes.
- Every practical output should define expected result, feedback cycle, and review point.
- Do not invent citations or page numbers.
- Do not quote long passages; paraphrase unless the user explicitly asks for short excerpts.
- If the book is copyrighted, provide summaries, brief excerpts, and analysis only.
- If verification fails, fix the artifact before claiming the HTML is final.
