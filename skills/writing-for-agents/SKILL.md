---
name: writing-for-agents
description: Use when drafting or editing agent instructions, AGENTS.md, CLAUDE.md, prompt runbooks, skill files, context pointers, design specs, or phased implementation plans. Don't use for human marketing copy, general technical writing, or user-facing product manuals.
---

# Writing for agents

Write files the agent runs without guessing. This covers skills, AGENTS.md, CLAUDE.md, runbooks, specs, and plans. Vendors package files differently. Same rules govern all packages. Use clear hierarchy, tight leading words, binary done checks, and no slop.

Read the `unslop` skill for banned words, punctuation bans, and Indonesian calque rules. This skill defines structure and routing. It defers prose fixes to `unslop`.

## Modes

Pick the mode before Step 1.

- Author mode (default). You draft the file or edit it in place.
- Audit mode. User asks for review without edits. You report each defect with line number and patch, then stop. You leave target file untouched.

## Workflow

Run four steps in order.

### Step 1. Scope and budget

Name target type and set its budget before you write.

- You name target as always-loaded file (AGENTS.md, CLAUDE.md, system prompt) or on-demand pointer (skill description, disclosed reference).
- You list trigger branches. A branch changes what agent does. You put trigger word first in each branch. You drop synonyms that trigger same branch.
- You set budget. Text loaded each turn spends context load. Text behind pointer spends cognitive load. See W1.

Completion criterion. You write down target, trigger branches, and budget mode.

### Step 2. Tier and outline

You place each section in one tier (W2).

- Primary. Agent runs ordered steps in sequence in main file. You keep file under 250 lines.
- Secondary. Agent reads rules, definitions, tables on demand. You group one concept with its rules under one heading.
- Tertiary. Agent loads disclosed files in `references/` only through pointer. You move text over 100 lines out of main file.

Completion criterion. You produce outline that labels each section with its tier.

### Step 3. Draft

You follow these rules to write.

- You close each step with done check that you can verify as yes or no and that covers all outputs (W3).
- You use leading words already in model pre-training, like tracer, probe, baseline, invariant, audit, red, instead of long definitions (W4).
- You state file, endpoint, command, or mechanism. You replace vague feeling with file or command that causes it.
- You pair each ban with required action on same line (W4).
- For skill, you write frontmatter and layout from Skill files section, then run two subagent runs and log each skipped step.

Completion criterion. You close every step with verifiable done check and pair every ban with required action.

### Step 4. Verify

You run checklist at end of file, then fix each failing row.

- You apply `unslop` rules to prose. You check frontmatter and directory layout for skill.
- You delete lines that do not change agent behavior (W5).
- You read directory layout, manifests, and CLI help at runtime instead of copying them into file.
- For skill, you pass two consecutive subagent runs with zero skipped steps.

Completion criterion. Draft passes each checklist row with zero open items.

## Core rules

### W1 Context load and pointers

Each file spends one of two budgets. Context load means tokens present each turn. Cognitive load means time user spends to remember which file to load. Pointer trades context load for small fixed cost. Pointer stays loaded. Text behind it does not.

Pointer names material and lists branches that must read it. You keep one trigger per branch. You put trigger word first. You inline text each branch needs. You put text behind pointer when only some branches need it. If agent keeps missing required file, you rewrite pointer wording before you move text inline.

### W2 Tiers and splitting

File holds steps, reference, or both. Steps mean ordered actions. Reference means rules, definitions, facts agent reads on demand.

Move too little to reference and main file grows past 250 lines. Move too much and agent loses detail it needs. You split file only when split pays its cost:

- Split by sequence when agent sees upcoming steps and skips current one.
- Split by invocation when skill must run on its own. Read `references/skill-mechanics.md` for invocation modes and router skills, and read `references/anthropic-best-practices.md` for harness patterns.

You put concept, rules, and edge cases under one heading. File sprawls when it grows long though each line stays true. When file sprawls, you move reference behind pointers and split task by branch or sequence.

### W3 Steps and completion criteria

Each step closes with done check that tells agent when step ends. Strong check must pass two checks:

- Clarity. Agent can separate done from not done. "Ensure understanding" fails this check, so agent claims success early. You rewrite boundary to make done explicit. If boundary stays fuzzy, you move later steps to another prompt or subagent.
- Demand. Check requires specific inspection. "Account for every modified database model" forces inspection. "List the changes" does not.

Strongest checks are verifiable, binary, and exhaustive.

### W4 Leading words and positive framing

Leading word means compact concept already in model pre-training. Tracer, probe, baseline, invariant, audit, red use existing prior without long definition. You replace definition with word that carries it:

- "fast, deterministic, low overhead" becomes "tight".
- "a test that genuinely catches the issue" becomes "red".

You prefer positive instruction. Ban repeats banned concept, and model repeats it. You write "one-line bullet points" instead of "do not write long paragraphs". When ban guards hard invariant, you pair it on same line with required action.

### W5 Anti-slop beyond unslop

Agent copies tone and density of files it reads. Long instructions produce long prose and extra tool calls. `unslop` covers words and punctuation. These rules cover agent files.

- Match reader. You write at density agent must produce.
- Delete no-ops. When line restates default behavior, you cut it. You test rule against real agent runs before you keep it.
- Keep one source of truth. You state each rule once. Env files, directory layout, command help state themselves. You document convention only when env does not state it.
- Delete dead lines. You remove lines that no longer change behavior.

## Boundaries

You apply structure and style rules to prose only. You leave these byte for byte:

- Code fences and inline code, including YAML frontmatter blocks and JSON.
- SQL, shell commands, file paths, and tree output.
- Quoted slop examples that show banned pattern on purpose.

You leave code unchanged. You apply prose rules to prose only. You never rename symbol, restyle sample, or reflow command to satisfy prose rule.

## Skill files

A skill is a directory whose entrypoint is `SKILL.md`.

```text
skills/<skill-name>/
├── SKILL.md              # Required entrypoint and runbook
├── references/           # Deep reference manuals, read on demand
├── scripts/              # Deterministic executables
├── assets/               # Static templates and mock data
└── examples/             # Verified sample implementations
```

Directory name must equal frontmatter `name`. Minimum valid frontmatter:

```yaml
---
name: skill-name-in-kebab-case
description: Use when [triggering conditions]. Don't use for [negative exclusions].
---
```

You keep `name` to lowercase alphanumerics and single hyphens. You write `description` in third person with positive triggers that start at "Use when" and negative exclusions that start at "Don't use for". You omit workflow summary. Model may run summary and skip body. Read `references/agentskills-spec.md` for full schema, optional fields, and discovery roots. Read `references/skill-mechanics.md` to choose model invocation against user invocation. Commit reference files directly to git; never ignore, hide, or stash secondary reference documents.

## Testing a skill

You treat skill as hypothesis until subagent run proves it:

1. You run task with subagent and no skill loaded. You record failures and exact rationalizations.
2. You write minimum instruction that blocks each recorded failure.
3. You run fresh subagent with skill loaded. You count each shortcut it finds.
4. You pass two consecutive runs with zero shortcuts.

Read `references/testing-skills.md` for full loop and scenario design. Read `references/google-agent-standards.md` for platform standards.

## Quick audit checklist

You run this before you deploy any agent file.

| Check | Passing condition |
|---|---|
| Frontmatter | 1 to 64 character kebab-case name equal to the directory, a description with "Use when" and "Don't use for", valid optional fields |
| Hierarchy | Primary steps, secondary rules, and tertiary references separated |
| Context load | Main file under 250 lines, reference over 100 lines moved to `references/` |
| Completion criteria | Every step ends on a checkable, binary criterion |
| Leading words | Recruits pre-training priors and pairs each guardrail with a positive action |
| Anti-slop | Passes every `unslop` check, with code and commands left untouched |
| Verification | Baseline failures captured and two consecutive compliant runs recorded |
