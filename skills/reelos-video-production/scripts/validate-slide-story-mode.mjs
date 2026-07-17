#!/usr/bin/env node

import {readFileSync, existsSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const skillRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(join(skillRoot, path), 'utf8');
const failures = [];

const assert = (condition, message) => {
  if (!condition) failures.push(message);
};

const requiredFiles = [
  'SKILL.md',
  'agents/openai.yaml',
  'references/slide-story-mode.md',
  'references/slide-story-templates.md',
];

for (const path of requiredFiles) {
  assert(existsSync(join(skillRoot, path)), `missing required file: ${path}`);
}

if (failures.length === 0) {
  const skill = read('SKILL.md');
  const mode = read('references/slide-story-mode.md');
  const templates = read('references/slide-story-templates.md');
  const openai = read('agents/openai.yaml');

  assert(skill.split('\n').length <= 500, 'SKILL.md must stay under 500 lines');
  assert(skill.includes('显式模式高于内容风格'), 'missing conflict priority in SKILL.md');
  assert(mode.includes('显式模式 > 交付物 > 内容形态 > 视觉关键词'), 'missing mode conflict hierarchy');
  assert(skill.includes('不要仅因输入里出现'), 'missing negative Slide Story trigger');
  assert(mode.includes('以下情况不自动进入'), 'missing mode exclusion cases');

  for (const route of ['slides-web', 'slides-video', 'slides-dual']) {
    assert(skill.includes(route), `SKILL.md missing route: ${route}`);
    assert(mode.includes(route), `slide-story-mode.md missing route: ${route}`);
    assert(templates.includes(route), `slide-story-templates.md missing route: ${route}`);
  }

  const templateIds = [
    'promo-fast-8',
    'explainer-core-10',
    'pitch-decision-12',
    'report-evidence-12',
  ];
  const selectionTable = templates.split('## 路由与模板的边界')[0];

  for (const id of templateIds) {
    assert(templates.includes(`### \`${id}\``), `missing template heading: ${id}`);
    assert(selectionTable.includes(`\`${id}\``), `missing template selection row: ${id}`);
  }

  assert(templates.includes('type SlideStoryPlan ='), 'missing shared SlideStoryPlan contract');
  assert(templates.includes('## 触发与冲突样例'), 'missing routing examples');
  assert(templates.includes('## 反模式'), 'missing anti-patterns');
  assert(openai.includes('$reelos-video-production'), 'default_prompt must invoke the skill explicitly');
  assert(openai.includes('Slide Story'), 'openai.yaml must expose Slide Story capability');

  const referencePaths = [...skill.matchAll(/`(references\/[^`]+\.md)`/g)].map((match) => match[1]);
  for (const path of new Set(referencePaths)) {
    assert(existsSync(join(skillRoot, path)), `SKILL.md references missing file: ${path}`);
  }
}

if (failures.length > 0) {
  for (const failure of failures) console.error(`[FAIL] ${failure}`);
  process.exit(1);
}

console.log('[OK] Slide Story mode entry, routes, templates, examples, and metadata are valid.');
