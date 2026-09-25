---
name: writing-for-agents
description: Use when drafting or editing agent instructions, AGENTS.md, CLAUDE.md, prompt runbooks, context pointers, or skill documentation.
---

# Writing for agents

Write predictable, high-demand documentation that AI agents consume, including skills, AGENTS.md, CLAUDE.md, and context pointers. Packaging differs across formats, but governing mechanisms remain identical. Predictable agent execution requires clear information hierarchy, tight leading words, binary completion criteria, and strict anti-slop discipline.

When authoring or updating skills, follow test-driven verification and consult `references/testing-skills.md` for baseline failure scans, subagent evaluation, and loophole closure.

## Workflow

Follow these four steps in sequence:

### Step 1. Scope audit and budget allocation

Determine document category, context load versus cognitive load budget, and trigger branches.

- Classify the target into an always-loaded file (AGENTS.md, CLAUDE.md, system prompt) or an on-demand pointer (skill description, disclosed reference).
- Identify distinct trigger branches. Each branch represents a separate operational path that changes agent actions.
- Front-load trigger keywords so the model catches them early. Eliminate duplicate synonyms that consume tokens without changing behavior.
- Calculate token impact. Keep always-loaded pointers minimal and push extensive reference material behind pointers.

Completion criterion. A defined document target with explicit trigger branches and confirmed budget mode.

### Step 2. Information hierarchy and progressive disclosure

Classify content across three information tiers to protect model attention and context budgets.

- Primary tier. In-file ordered execution steps in the main document. Keep steps sequential, operational, and under 250 lines.
- Secondary tier. In-file reference, constraints, and lookup tables consulted on demand. Group related rules under cohesive headings.
- Tertiary tier. Disclosed reference files in `references/` or standalone markdown documents. Move material exceeding 100 lines into external reference files reached by explicit pointers.
- Apply co-location. Keep concept definitions, associated rules, and edge cases together under one heading.

Completion criterion. An outline separating primary operational steps, secondary on-demand rules, and tertiary disclosed reference files.

### Step 3. Drafting with leading words and positive bounds

Draft the document using established pre-training priors and positive operational constraints.

- Write numbered steps ending in binary, checkable, and exhaustive completion criteria. Every step must allow the agent to verify whether the work is done without guessing.
- Recruit model priors with established leading words such as tracer, probe, baseline, invariant, audit, red, or tight instead of verbose explanations.
- State what the system does, not what it feels like. Replace abstract metaphors with concrete files, endpoints, types, and commands.
- Pair every negative constraint immediately with the required positive action. Avoid dangling prohibitions that pull forbidden patterns into context.
- For skills, test against observed baseline failures and consult `references/testing-skills.md` to seal procedural loopholes.

Completion criterion. A complete draft containing operational steps, each ending in a checkable binary completion criterion, with zero dangling negative bans.

### Step 4. Anti-slop audit and verification pass

Audit the draft against anti-slop standards and prune redundant text.

- Strip promotional vocabulary, throat-clearing openings, and sycophantic closings.
- Remove em dashes, en dashes, and hyphens acting as dashes. Use periods or commas instead.
- Restrict colons to introducing lists, tables, or code blocks. Remove mid-sentence colons.
- Eliminate passive voice, vague adverbs, and decorative emojis.
- Prune no-ops and duplicate instructions. Rely on environment truth such as directory layouts, package manifests, and CLI help output instead of copying static tables.
- For skills, verify two consecutive runs pass in subagents without procedural evasion.

Completion criterion. The draft passes every check in the quick audit checklist with zero violations.

## Skill authoring and frontmatter

Organize skills within standard workspace or global customization roots:

```text
skills/<skill-name>/
├── SKILL.md              # Required entrypoint and runbook
├── references/           # Optional deep reference manuals and guides
├── scripts/              # Optional deterministic executable helpers
├── assets/               # Optional static templates, boilerplate, and mock data
└── examples/             # Optional verified sample implementations
```

The directory name must match the `name` field in the frontmatter. Discovery priority runs in sequence:
1. Universal workspace project skills in `.agents/skills/`
2. Universal user skills in `~/.agents/skills/` or platform configs in `~/.gemini/config/skills/`
3. Built-in application mounts

Every skill entrypoint must contain YAML frontmatter compliant with the AgentSkills specification:

```yaml
---
name: skill-name-in-kebab-case
description: Short functional summary. Use when [triggering conditions]. Don't use for [negative exclusions].
compatibility: Optional environment requirements (max 500 chars)
license: Optional SPDX license or path to license file
metadata:
  version: "1.0.0"
  author: "Team"
allowed-tools: optional tool names separated by spaces
---
```

Frontmatter rules:
- Format the `name` with 1 to 64 lowercase alphanumeric characters and single hyphens. Do not use leading, trailing, or consecutive hyphens. The name must match the parent directory name.
- Write descriptions in third person up to 1024 characters (recommended under 500 characters to conserve context). State the core function, positive triggers starting with "Use when", and negative exclusions starting with "Don't use for" to prevent false positive routing. Never summarize the internal workflow in the description, because models may execute the summary instead of reading the complete skill body.
- Optional fields include `compatibility` for environment constraints, `license` for distribution terms, `metadata` for arbitrary attributes, and `allowed-tools` to restrict tool access.
- Choose invocation mode intentionally. Model-invoked skills include a description for autonomous discovery. User-invoked skills set `disable-model-invocation: true` (platform extension) to save context load when human command suffices. Read `references/agentskills-spec.md` and `references/skill-mechanics.md` for full schema rules and router skills.

## Progressive disclosure and context pointers

A context pointer names external material and states when to load it. A skill description is a context pointer. A line in AGENTS.md that names a file is also a context pointer. The wording of the pointer determines whether the agent loads the file. If an agent misses a required document because the pointer is vague, sharpen the wording. Inline the material only if sharpening fails.

A pointer performs two jobs. It describes the material, and it lists the trigger branches that require reading it. Every word in an always-loaded pointer costs tokens on every turn. Prune pointers ruthlessly:
- Front-load the leading trigger word so it catches model attention early.
- Keep one trigger per branch. Synonyms that describe the same task waste tokens.
- Remove background details that the body file already explains.

Every document and pointer spends one of two budgets:
- Context load is the cost of always-loaded material on the context window. An AGENTS.md line, a skill description, and text sitting in context on every turn spend tokens whether they fire or not.
- Cognitive load is the cost on the human. The human must remember which documents exist and when to invoke each one. Spend human attention where human judgment matters, and automate or hide the rest.

Progressive disclosure moves material out of the main file and behind a pointer. Inline material that every branch needs, and move material behind a pointer if only certain branches need it. Move heavy documentation exceeding 100 lines out of `SKILL.md` into `references/`.

Co-location keeps related concepts together. Keep a concept definition, its rules, and its edge cases under one heading. Grouped instructions read like intentional technical documentation. Scattered rules confuse the model.

Sprawl happens when a document grows too long, even if every line is accurate. Attention thins across long files. When a document sprawls, push reference behind pointers and split tasks by branch or sequence.

## Steps and completion criteria

Every step must end on a clear completion criterion that tells the agent when the step is done. A strong criterion has two properties:
- **Clarity.** The agent must distinguish done from not done. Vague phrasing like "ensure understanding" leads to premature completion, where the agent rushes to finish before doing the actual work. Visible upcoming steps pull the model forward. A sharp bound resists that pull. Sharpen the boundary first. If the step remains fuzzy, move subsequent steps to a later prompt or a subagent.
- **Demand.** Demand sets the standard of work. Writing "account for every modified database model" forces thorough inspection, while "list the changes" does not. Demand drives legwork without needing a dozen micro-steps. High demand applies to flat reference rules just as strongly as it applies to ordered steps.

The strongest completion criteria are checkable, binary, and exhaustive.

Split only when separation earns its cost:
- Split by sequence when visible future steps tempt the agent to rush the current step. Hiding upcoming steps forces the agent to focus on the immediate work.
- Split by invocation when a skill should fire independently. Read `references/skill-mechanics.md` for details.

## Leading words and positive framing

A leading word is a compact concept already present in model pre-training. Words like tracer, probe, baseline, invariant, or audit recruit existing model priors without spending tokens on long explanations. Prefer established terms over custom jargon:
- Replace "fast, deterministic, low overhead" with "tight".
- Replace "a test that genuinely catches the issue" with "red".

Prefer positive instructions over negative bans. Steering by prohibition pulls forbidden concepts into context, making the model more likely to fixate on them. Instead of saying "do not write long narrative paragraphs", say "write one-line bullet points". If a prohibition is necessary as a hard guardrail, pair it immediately with the required positive action.

## Anti-slop discipline for agent docs

Agents mirror the tone, formatting, and density of the documents they consume. Writing bloated, vague, or decorative documentation causes agents to produce sloppy code, run-on prose, and unfocused tool calls. Apply strict anti-slop rules:
- Cut puffery and promotional phrasing. Strip words like "comprehensive", "essential", "vital", "cutting-edge", or "seamless". State concrete behavior directly.
- Strip conversational filler. Delete phrases like "in order to", "it is important to remember that", and "please note that". Start directly with the action verb.
- Ban em dashes, en dashes, and hyphens used as dashes. Do not trade dashes for parentheses. Use simple periods or commas.
- Avoid colons as mid-sentence connectors. Use a colon only to introduce an explicit list, a table, or a code block. Break run-on sentences into two complete sentences instead.
- Replace abstract jargon with concrete nouns. Change "API surface" to "endpoints", "substrate" to "base", "vector" to "method", and "paradigm" to "pattern". Name the actual file, command, or data structure.
- Say what it does, not how it feels. Replace vague claims like "keeps types close" with exact mechanisms like "generates TypeScript types directly from the database schema".
- Use active voice and short sentences. Name the actor and the action. Keep one operational instruction per sentence.

## Testing skills and loophole closure

Treat skill authoring as test-driven development for process documentation. An untested skill is an unverified hypothesis. Before deploying a skill, follow the testing loop in `references/testing-skills.md`:
1. Run baseline scenarios with a subagent without the skill to capture unguided failure modes and model rationalizations.
2. Draft minimal instructions that directly prevent observed failure paths.
3. Dispatch fresh subagents with the candidate skill to uncover evasions and close loopholes.
4. Verify subagent compliance across consecutive runs.

Read `references/testing-methodology.md` for deep behavioral testing patterns, `references/agentskills-spec.md` for the official specification, and `references/google-agent-standards.md` for platform standards.

## Quick audit checklist

Run this check before deploying any agent document or publishing a skill:

| Check | Passing condition |
|---|---|
| Frontmatter | Contains 1 to 64 char kebab-case name matching directory, valid description with positive and negative triggers, and valid optional metadata |
| Information hierarchy | Primary steps, secondary rules, and tertiary references cleanly separated |
| Context load | `SKILL.md` is under 250 lines with heavy reference moved to `references/` |
| Completion criteria | Every operational step terminates on a checkable, binary completion criterion |
| Leading words | Recruits established pre-training priors and pairs positive actions to guardrails |
| Anti-slop | Zero banned vocabulary, zero em dashes, zero emojis, and colons appear only before lists, tables, or code |
| Verification | Baseline failures captured, loopholes closed, and compliance verified via `references/testing-skills.md` |
