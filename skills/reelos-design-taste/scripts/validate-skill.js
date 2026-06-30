#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const root = path.resolve(process.argv[2] || path.join(__dirname, ".."));
const requiredFiles = [
  "SKILL.md",
  "agents/openai.yaml",
  "references/cultural-aesthetics.md",
  "references/typography.md",
  "references/visual-systems.md",
  "references/taste-review.md",
  "references/output-format.md",
  "references/decision-boundaries.md",
  "references/user-guide.md",
  "references/craft-routing.md",
  "references/anti-ai-slop.md",
  "references/design-contract.md",
  "examples/basic-case.md",
  "examples/advanced-case.md",
  "examples/failure-case.md",
  "examples/typography-case.md",
  "examples/reference-extraction-case.md",
  "examples/guided-choice-case.md",
];

const errors = [];
const expectedName = "reelos-design-taste";

for (const file of requiredFiles) {
  if (!fs.existsSync(path.join(root, file))) {
    errors.push(`Missing required file: ${file}`);
  }
}

const skillPath = path.join(root, "SKILL.md");
if (fs.existsSync(skillPath)) {
  const skill = fs.readFileSync(skillPath, "utf8");
  const frontmatter = skill.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatter) {
    errors.push("SKILL.md is missing YAML frontmatter.");
  } else {
    const fm = frontmatter[1];
    for (const key of ["name:", "description:", "license:", "metadata:"]) {
      if (!fm.includes(key)) errors.push(`Frontmatter missing ${key}`);
    }
    const nameLine = fm.split("\n").find((line) => line.startsWith("name:"));
    if (nameLine && !nameLine.includes(expectedName)) {
      errors.push(`Frontmatter name must be ${expectedName}.`);
    }
    const metadataLine = fm.split("\n").find((line) => line.startsWith("metadata:"));
    if (metadataLine && !metadataLine.includes('{"openclaw"')) {
      errors.push("metadata must be a single-line JSON object with openclaw settings.");
    }
  }

  for (const phrase of ["## Professional stance", "## When to use", "## Workflow", "## Quality gates", "## Required output", "## Decision boundaries", "## Safety notes"]) {
    if (!skill.includes(phrase)) errors.push(`SKILL.md missing section: ${phrase}`);
  }
}

const openaiPath = path.join(root, "agents/openai.yaml");
if (fs.existsSync(openaiPath)) {
  const openai = fs.readFileSync(openaiPath, "utf8");
  if (!openai.includes("Reelos Design Taste")) errors.push("agents/openai.yaml missing Reelos display name.");
  if (!openai.includes(`$${expectedName}`)) errors.push("agents/openai.yaml default_prompt must use $reelos-design-taste.");
}

for (const file of requiredFiles) {
  const fullPath = path.join(root, file);
  if (!fs.existsSync(fullPath)) continue;
  const text = fs.readFileSync(fullPath, "utf8");
  const legacyInvocation = "$" + "design-taste";
  const legacyFrontmatterName = "name: " + "design-taste";
  if (text.includes(legacyInvocation) || text.includes(legacyFrontmatterName)) {
    errors.push(`Legacy design-taste reference found in ${file}`);
  }
}

if (errors.length) {
  console.error(errors.map((error) => `- ${error}`).join("\n"));
  process.exit(1);
}

console.log("reelos-design-taste skill structure is valid.");
