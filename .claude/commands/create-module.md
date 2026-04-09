# Create Training Module

Create a new training module with lectures, exercises, and knowledge tests.

**Depends on skill:** `curriculum` — read `.claude/skills/curriculum/SKILL.md` first for all content structure, Hugo conventions, voice/tone, and quality standards.

## Usage

```
/create-module <module-number> <module-slug> "<module-title>"
```

Example: `/create-module 08 spark-streaming "Spark Structured Streaming"`

If no arguments are provided, ask the learner what topic they want to learn next.

---

## Procedure

### 1. Load context

- Read `.claude/skills/curriculum/SKILL.md` for all structural and quality standards
- Read `AGENTS.md` for any existing guidance on this topic
- Read all `_index.md` files in `site/content/modules/` to understand what modules exist
- Read front matter tags across existing lectures to understand the concept graph

### 2. Research current material

Before writing any content:

1. **Web search** for the latest official Databricks documentation on this topic
2. **Web search** for recent blog posts, release notes, or announcements (last 12 months)
3. **Check** what already exists to avoid duplication and understand prerequisite knowledge

Collect your sources. You will cite them in lecture front matter (`sources:` field).

### 3. Plan the lecture sequence

Design 3-6 lectures that build knowledge in this order:

1. **Define** — What is this thing? Define every term and acronym.
2. **Context** — Why does it exist? What problem does it solve?
3. **Contrast** — How does it compare to alternatives?
4. **Mechanics** — How does it actually work under the hood?
5. **Practice** — Hands-on examples with real data.
6. **Judgment** — When to use it, when not to, trade-offs.

**Show the lecture plan to the learner and get approval before writing content.**

### 4. Scaffold the structure

Create both the Hugo content tree and the exercises directory:

```bash
# Hugo content (branch bundle for module, leaf bundles for lectures)
mkdir -p site/content/modules/{NN}-{slug}
mkdir -p site/content/modules/{NN}-{slug}/01-{lecture-slug}
mkdir -p site/content/modules/{NN}-{slug}/02-{lecture-slug}
# ... for each lecture (images go directly in the lecture dir, no subdirectory)
mkdir -p site/content/modules/{NN}-{slug}/99-knowledge-test

# Exercise code (standalone)
mkdir -p modules/{NN}-{slug}/exercises
```

### 5. Write content

Write all content following the standards in the curriculum skill:
- Module `_index.md` with proper front matter (including `tags`, `prerequisites`)
- Each lecture as `index.md` in its leaf bundle (including `sources` in front matter)
- Knowledge test in `99-knowledge-test/index.md`
- Exercise files in `modules/{NN}-{slug}/exercises/` with `# TODO` markers
- `VALIDATION.md` in `modules/{NN}-{slug}/`

### 6. Update project files

- Add a section in `AGENTS.md` under `## Module-by-module agent guide`
- Add a row in `README.md`'s module table with `planned` status

### 7. Verify the build

```bash
cd site && hugo --gc
```

Fix any errors before finishing.
