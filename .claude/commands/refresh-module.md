# Refresh Training Module

Update an existing module's lectures with current information without rewriting from scratch.

**Depends on skill:** `curriculum` — read `.claude/skills/curriculum/SKILL.md` first for all content structure, Hugo conventions, voice/tone, and quality standards.

## Usage

```
/refresh-module <module-number-or-slug>
```

Example: `/refresh-module 02` or `/refresh-module delta-lake`

If no argument is provided, list all modules with their `last_refreshed` dates and ask which one to refresh.

---

## Procedure

### 1. Read all existing content for this module

- Read the module's `_index.md` — note `tags`, `status`, `last_refreshed`
- Read **every lecture's `index.md`** — note `tags`, `sources`, `last_refreshed`, and the actual content
- Read the knowledge test
- Read `modules/{NN}-{slug}/VALIDATION.md` and exercise files
- Read the module's section in `AGENTS.md`

Build a complete picture of what the module currently teaches before searching for updates.

### 2. Research what's changed

Using the `tags` and `sources` from lecture front matter:

1. **Revisit each source URL** listed in lecture front matter — check if the content has changed or been superseded
2. **Web search** for the latest Databricks documentation on each tag
3. **Web search** for recent announcements, deprecations, or new features (last 12 months) related to the module's tags
4. **Check** the Databricks release notes for relevant changes

### 3. Identify what needs updating

Create a change summary for the learner:

- **New information** — Features, APIs, or concepts that didn't exist when the lecture was written
- **Corrections** — Things that have changed (renamed, deprecated, replaced)
- **Deepening** — Areas where better explanations or examples are now available
- **No change needed** — Lectures that are still accurate and current

**Show this summary to the learner and get approval before making changes.**

### 4. Update surgically

For each lecture that needs changes:

- **Add** new information where it fits naturally in the existing flow
- **Update** outdated information in place
- **Do NOT rewrite from scratch** — preserve the structure and context the learner has already read
- **Update `sources:`** in front matter with any new URLs used
- **Set `last_refreshed:`** to today's date (YYYY-MM-DD)

If a topic has grown enough to warrant a new lecture, create one following the curriculum skill's leaf bundle pattern and slot it into the sequence (adjust weights).

### 5. Update the knowledge test if needed

If new concepts were added:
- Add relevant oral questions
- Update the code challenge if exercise files changed
- Adjust the interview question if the module's scope grew

### 6. Update supporting files

- Update `modules/{NN}-{slug}/VALIDATION.md` to match any knowledge test changes
- Update `AGENTS.md` module section if emphasis or "must know cold" items changed
- Update exercise files if APIs or patterns changed (keep `# TODO` markers for unfilled exercises)

### 7. Verify the build

```bash
cd site && hugo --gc
```

### 8. Report what changed

Give the learner a concise summary:
- Which lectures were updated and why
- Any new lectures added
- Whether exercises or validation criteria changed
- The new `last_refreshed` date
