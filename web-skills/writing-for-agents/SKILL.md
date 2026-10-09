---
name: writing-for-agents
description: Use when drafting or editing agent instructions, AGENTS.md, CLAUDE.md, prompt runbooks, context pointers, design specs, or phased implementation plans for AI agents. Don't use for human marketing copy, general technical writing, or user-facing product manuals.
---

# Writing for Agents on Claude Web

Author predictable, high-demand instructions, skills, specifications, and phased implementation plans that AI agents execute cleanly on Claude Web.

<initiative_and_scope>
When asked to draft agent instructions, skills, or implementation plans, complete the entire draft with exhaustive, binary completion criteria. Stop and report when done. Do not add unrequested templates, boilerplate files, or decorative text.
</initiative_and_scope>

<claude_web_environment>
Operate within the Claude Web interface.
- Output finalized agent instructions, `SKILL.md` drafts, `AGENTS.md`, Design Specs, or Phased Implementation Plans as standalone Markdown Claude Artifacts (`text/markdown`).
- In the chat body, provide only a high-level summary of trigger keywords, token budget allocation, and the verification checklist pass.
</claude_web_environment>

## Workflow

### Step 1. Scope audit and budget allocation

Classify target document and context budget:
1. **Always-loaded files** (`AGENTS.md`, `CLAUDE.md`, System Prompts): Keep minimal, front-load trigger keywords, and push deep reference behind pointers.
2. **On-demand skills** (`SKILL.md`): Keep main body under 250 lines. Move reference tables and specialized guides exceeding 100 lines into `references/`.
3. **Phased implementation plans**: Break tasks into sequential batches. Each task must have automated verification commands and binary completion criteria.

### Step 2. Information hierarchy and progressive disclosure

Structure content across three tiers:
- **Primary tier (Sequential Execution):** Ordered operational steps in the main document. Keep sequential and actionable.
- **Secondary tier (Invariants & Rules):** Co-located constraints, execution rules, and quick lookup tables.
- **Tertiary tier (Disclosed References):** Specialized reference manuals stored in `references/` and consulted on demand.

### Step 3. Drafting with leading words and positive bounds

- **Recruit model priors with leading words:** Use compact terms like *probe, invariant, tracer, audit, baseline, tight, red* instead of verbose explanations.
- **Pair negative bans with positive actions:** Avoid dangling negative prohibitions. Immediately state what to do instead (e.g., *"Never use `transition: all`. Name exact properties `transform` and `opacity`"*).
- **Checkable binary completion criteria:** Every step and task must end with an unambiguous passing condition:
  * Weak: *"Ensure the database query is optimized."*
  * Strong: *"The query uses the composite index on `(user_id, created_at)` and executes in under 10ms with zero N+1 queries."*

### Step 4. Phased implementation plan structure

When authoring implementation plans from a design specification:
1. Divide work into numbered phases (Phase 1: Setup/Scaffolding, Phase 2: Core Domain Logic, Phase 3: UI Integration, Phase 4: Verification).
2. For each task within a phase, include:
   - **Target files:** Explicit absolute or relative paths.
   - **Action:** Exact modifications or components to create.
   - **Verification:** Concrete test commands, curl commands, or browser assertions.
   - **Completion criterion:** Binary checkable standard.

### Step 5. Anti-slop and tone calibration

- Strip throat-clearing openings ("Certainly! Below is the plan...") and closing filler.
- Ban em dashes, en dashes, and hyphens used as dashes. Use periods or commas.
- Restrict colons to introducing lists, tables, or code blocks.
- Eliminate passive voice and vague adverbs. Keep one operational instruction per sentence.

### Step 6. Deliverable as Claude Artifact

Render the complete document (`SKILL.md`, `AGENTS.md`, or Implementation Plan) as a standalone Markdown Claude Artifact (`text/markdown`).

## Agent skill frontmatter specification

When writing or updating a skill entrypoint, use YAML frontmatter compliant with the AgentSkills specification:

```yaml
---
name: skill-name-in-kebab-case
description: Short functional summary. Use when [triggering conditions]. Don't use for [negative exclusions].
---
```

Frontmatter rules:
- `name`: 1 to 64 lowercase alphanumeric characters and single hyphens. Must match the skill directory name.
- `description`: Front-load trigger keywords. Include positive triggers ("Use when...") and negative exclusions ("Don't use for..."). Keep under 500 characters. Never summarize internal workflow in the description, to prevent models from executing the summary instead of reading the complete body.

## Quick audit checklist

| Check | Passing condition |
|---|---|
| Frontmatter | Contains valid kebab-case name and description with positive/negative triggers |
| Context load | `SKILL.md` under 250 lines; heavy reference moved to `references/` |
| Completion criteria | Every operational step or task terminates on a binary, checkable condition |
| Positive bounds | Every negative prohibition is paired with a direct positive action |
| Anti-slop | Zero banned vocabulary, zero em dashes, colons only before lists/tables/code |
| Artifact delivery | Complete document rendered as a Claude Artifact |
