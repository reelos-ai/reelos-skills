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
  'references/auto-motion-director.md',
  'references/vfx-supervisor.md',
  'references/final-acceptance.md',
  'references/deep-signal-system-mode.md',
];

for (const path of requiredFiles) {
  assert(existsSync(join(skillRoot, path)), `missing required file: ${path}`);
}

if (failures.length === 0) {
  const skill = read('SKILL.md');
  const mode = read('references/slide-story-mode.md');
  const templates = read('references/slide-story-templates.md');
  const autoMotion = read('references/auto-motion-director.md');
  const vfx = read('references/vfx-supervisor.md');
  const acceptance = read('references/final-acceptance.md');
  const deepSignal = read('references/deep-signal-system-mode.md');
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
  assert(skill.includes('自动择效'), 'SKILL.md must enable automatic motion selection');
  assert(autoMotion.includes('总分不低于 75'), 'auto motion director must define the acceptance threshold');
  assert(autoMotion.includes('语义准确'), 'auto motion director must define semantic scoring');
  assert(autoMotion.includes('MotionDecisionPlan'), 'auto motion director must define the decision contract');
  assert(skill.includes('特效师强化'), 'SKILL.md must include the VFX supervisor stage');
  assert(skill.includes('终审验收'), 'SKILL.md must include final acceptance');
  assert(vfx.includes('VFXEnhancementPlan'), 'VFX supervisor must define the enhancement contract');
  assert(vfx.includes('英雄时刻'), 'VFX supervisor must define hero moments');
  assert(vfx.includes('效果预算'), 'VFX supervisor must define an effect budget');
  assert(acceptance.includes('FinalAcceptanceReport'), 'final acceptance must define its report contract');
  assert(acceptance.includes('四种观看模式'), 'final acceptance must define four review modes');
  assert(acceptance.includes('硬门槛'), 'final acceptance must define hard gates');
  assert(acceptance.includes('85'), 'final acceptance must define the 85-point delivery threshold');
  assert(openai.includes('特效师'), 'openai.yaml must expose the VFX supervisor stage');
  assert(openai.includes('终审'), 'openai.yaml must expose final acceptance');
  assert(skill.includes('深空信号系统风'), 'SKILL.md must expose the deep signal system style');
  assert(deepSignal.includes('三层信息架构'), 'deep signal system mode must define information layers');
  assert(deepSignal.includes('相邻场景'), 'deep signal system mode must prevent repeated compositions');
  assert(deepSignal.includes('强度 5'), 'deep signal system mode must define a single hero-moment budget');

  const referencePaths = [...skill.matchAll(/`(references\/[^`]+\.md)`/g)].map((match) => match[1]);
  for (const path of new Set(referencePaths)) {
    assert(existsSync(join(skillRoot, path)), `SKILL.md references missing file: ${path}`);
  }
}

if (failures.length > 0) {
  for (const failure of failures) console.error(`[FAIL] ${failure}`);
  process.exit(1);
}

console.log('[OK] Slide Story routing, automatic motion, VFX supervision, final acceptance, examples, and metadata are valid.');
