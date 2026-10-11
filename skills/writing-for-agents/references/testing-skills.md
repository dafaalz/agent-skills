# Testing skills

Treat a skill as a hypothesis until a subagent run confirms it. An untested skill is an unverified guess about how an agent will behave.

Testing a skill follows test-driven development. Run the task without the skill, record where the agent deviates, write the smallest instruction that prevents each deviation, verify compliance with the skill loaded, then close the loopholes that remain. Read `google-agent-standards.md` for the platform rules that shape the instructions themselves.

## When to test

Test a skill that:

- Enforces a workflow sequence, such as test-first development or pre-commit verification.
- Contains non-obvious operational choices where agents default to a shortcut.
- Requires multi-step tool calls where an intermediate check is mandatory.

Pure reference documents with static lookup tables or syntax do not need a baseline run. Spend testing effort on procedural runbooks and discipline rules.

## The testing cycle

Run these four steps in order.

### 1. Baseline run (RED)

Give a subagent a concrete task with the candidate skill absent.
- Use a realistic prompt drawn from normal project work.
- Record the subagent's choices, commands, and explanations.
- Mark the exact points where it skips verification or breaks the convention you want.

Completion criterion. A written log of the unguided failure modes and the exact model rationalizations.

### 2. Minimal drafting (GREEN)

Write only the instructions needed to stop the recorded failures.
- Answer the specific rationalizations from the baseline run.
- Pair each boundary with the positive action that replaces it.
- Name exact file paths, shell commands, and preconditions.
- Skip speculation about edge cases you did not observe.
- Omit emotional appeals and artificial urgency, because modern models degrade under simulated pressure.

Completion criterion. A draft of `SKILL.md` that addresses every baseline failure.

### 3. Compliance verification (VERIFY GREEN)

Run a fresh subagent with the skill loaded.
- Reuse the identical task scenario from the baseline phase.
- Confirm the subagent follows the steps in order.
- Confirm it produces each required intermediate artifact and verification output.

Completion criterion. The subagent completes the task following every step, with no validation step skipped.

### 4. Loophole closure (REFACTOR)

Read the transcript for friction points and new shortcuts.
- When the subagent satisfies the letter of a rule while dodging its intent, add an explicit counter.
- Delete instructions that produced no measurable change in behavior.
- Re-run with a fresh subagent.

Completion criterion. Zero observed shortcuts across two consecutive runs.

## Designing test scenarios

A reliable scenario has three parts:

1. Concrete context. Supply real code, configuration, and dependencies. Avoid riddles and abstract puzzles.
2. Competing incentives. Make a shortcut tempting, such as working code with no tests or an urgent bug report.
3. Objective evaluation. Define one binary success condition, such as running the test command before editing production code.

## Directory structure

```text
skills/<skill-name>/
├── SKILL.md              # Required entrypoint and runbook
├── references/           # Deep reference manuals, read on demand
├── scripts/              # Deterministic executables
├── assets/               # Static templates and mock data
└── examples/             # Verified sample implementations
```

Discovery runs in this order:

1. Workspace project skills in `.agents/skills/`
2. Universal user skills in `~/.agents/skills/` or platform config in `~/.gemini/config/skills/`
3. Built-in application mounts

## Frontmatter and hierarchy

Minimum valid frontmatter:

```yaml
---
name: skill-name-in-kebab-case
description: Use when [triggering conditions]. Don't use for [negative exclusions].
---
```

- Keep `name` to lowercase alphanumerics and single hyphens, matching the directory.
- Write the `description` in third person with positive triggers at "Use when" and negative exclusions at "Don't use for". Omit any workflow summary, because a model may run the summary and skip the body. Stay under 500 characters.

Place content on three tiers:

1. Primary. Ordered steps in `SKILL.md`, under 250 lines.
2. Secondary. Rules and lookup tables read on demand.
3. Tertiary. Files in `references/`, reached by a pointer and loaded only when needed. Move material over 100 lines out of `SKILL.md`.

Use a Mermaid flowchart only for a non-obvious branch. Use numbered steps for a linear procedure.

## Quick reference checklist

Run this check before publishing a skill.

| Check | Passing condition |
|---|---|
| Frontmatter | Kebab-case name matching the directory, trigger-only description at "Use when" |
| Context load | `SKILL.md` under 250 lines, with reference over 100 lines moved to `references/` |
| Style | Zero em dashes, zero decorative emojis, sentence case headings |
| Verification | Baseline failures recorded without the skill, compliance confirmed with it |
| Completion criteria | Every step ends on a binary, checkable criterion |
