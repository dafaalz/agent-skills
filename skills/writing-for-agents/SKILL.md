---
name: writing-for-agents
description: Use when drafting or editing agent instructions, AGENTS.md, CLAUDE.md, prompt runbooks, skill files, context pointers, design specs, or phased implementation plans. Don't use for human marketing copy (author marketing copy directly), general technical writing (use technical-writing), or user-facing product manuals (use technical-writing).
---

# Writing for agents

Write files the agent runs without guessing. This covers skills, AGENTS.md, CLAUDE.md, runbooks, specs, and plans. Vendors package files differently. Same rules govern all packages. Use clear hierarchy, tight leading words, binary done checks, and no slop.

Read the `unslop` skill for banned words, punctuation bans, and Indonesian calque rules. This skill defines structure and routing. It defers prose fixes to `unslop`.

<HARD-GATE>
Write-Target Boundary. Write only to `.agents/state/writing-for-agents/` and documentation files explicitly named by the user or task. Do not modify application source code, test suites, database schemas, or package lockfiles.
</HARD-GATE>

## Modes

Declare the active operating mode before executing any steps:
- Author mode (default): Draft the target file or edit it in place. Run Steps 1 through 4 sequentially.
- Audit mode: Review without edits. Run Step 1, Step 3, and Step 4. Step 2 is skipped because the existing document already provides the structural skeleton; Step 3 audits that skeleton instead of scaffolding a new one. Emit `.agents/state/writing-for-agents/audit-report.md` and halt without modifying target files.

## Workflow

Run the operational steps in sequence.

### Step 1. Scope and budget

Name target type and set its budget before you write:
- Name target as always-loaded file (AGENTS.md, CLAUDE.md, system prompt) or on-demand pointer (skill description, disclosed reference).
- List trigger branches. A branch changes what agent does. Put trigger word first in each branch. Drop synonyms that trigger same branch.
- Set budget. Text loaded each turn spends context load. Text behind pointer spends cognitive load. See W1.

Completion criterion. `.agents/state/writing-for-agents/scope.json` exists on disk with `target_file`, `target_type`, `line_budget`, and `mode`.

### Step 2. Tier and outline

Place each section in one tier (W2):
- Primary. Agent runs ordered steps in sequence in main file. Keep file under 250 lines.
- Secondary. Agent reads rules, definitions, tables on demand. Group one concept with its rules under one heading.
- Tertiary. Agent loads disclosed files in `references/` only through pointer. Move text over 100 lines out of main file.

Completion criterion. `.agents/state/writing-for-agents/outline.md` exists on disk labeling each section with its tier.

### Step 3. Draft

Follow these rules to write:
- Close each step with done check that you can verify as yes or no and that covers all outputs (W3).
- Use leading words already in model pre-training, like tracer, probe, baseline, invariant, audit, red, instead of long definitions (W4).
- State file, endpoint, command, or mechanism. Replace vague feeling with file or command that causes it.
- Pair each ban with required action on same line (W4).
- For skill, write frontmatter and layout from Skill files section. Read `references/agentskills-spec.md` for schema rules. Read `references/testing-skills.md` and `references/google-agent-standards.md` for verification standards.

Completion criterion. Draft file exists on disk with every operational step closed by a verifiable binary completion criterion.

### Step 4. Verify

Run checklist at end of file, then fix each failing row:
- Apply `unslop` rules to prose. Check frontmatter and directory layout for skill.
- Delete lines that do not change agent behavior (W5).
- Read directory layout, manifests, and CLI help at runtime instead of copying them into file.
- Verify line budget with `wc -l <target-file>`.

Completion criterion. `python3 skills/review-a-skill/scripts/lint_skill.py <path-to-skill>` exits with status code 0 (for skills), or `wc -l <target-file>` confirms line count is within budget.

## Core rules

### W1 Context load and pointers

Each file spends one of two budgets. Context load means tokens present each turn. Cognitive load means time user spends to remember which file to load. Pointer trades context load for small fixed cost. Pointer stays loaded. Text behind it does not.

Pointer names material and lists branches that must read it. Keep one trigger per branch. Put trigger word first. Inline text each branch needs. Put text behind pointer when only some branches need it. If agent keeps missing required file, rewrite pointer wording before moving text inline.

### W2 Tiers and splitting

File holds steps, reference, or both. Steps mean ordered actions. Reference means rules, definitions, facts agent reads on demand.

Move too little to reference and main file grows past 250 lines. Move too much and agent loses detail it needs. Split file only when split pays its cost:
- Split by sequence when agent sees upcoming steps and skips current one.
- Split by invocation when skill must run on its own. Read `references/skill-mechanics.md` for invocation modes and router skills, and read `references/anthropic-best-practices.md` for harness patterns.

Put concept, rules, and edge cases under one heading. When file sprawls, move reference behind pointers and split task by branch or sequence.

### W3 Steps and completion criteria

Each step closes with done check that tells agent when step ends. Strong check must pass two checks:
- Clarity. Agent can separate done from not done. "Ensure understanding" fails this check, so agent claims success early. Rewrite boundary to make done explicit. If boundary stays fuzzy, move later steps to another prompt or subagent.
- Demand. Check requires specific inspection. "Account for every modified database model" forces inspection. "List the changes" does not.

Strongest checks are verifiable, binary, and exhaustive.

### W4 Leading words and positive framing

Leading word means compact concept already in model pre-training. Tracer, probe, baseline, invariant, audit, red use existing prior without long definition. Replace definition with word that carries it:
- "fast, deterministic, low overhead" becomes "tight".
- "a test that genuinely catches the issue" becomes "red".

Prefer positive instruction. Ban repeats banned concept, and model repeats it. Write "one-line bullet points" instead of "do not write long paragraphs". When ban guards hard invariant, pair it on same line with required action.

### W5 Anti-slop beyond unslop

Agent copies tone and density of files it reads. Long instructions produce long prose and extra tool calls. `unslop` covers words and punctuation. These rules cover agent files:
- Match reader. Write at density agent must produce.
- Delete no-ops. When line restates default behavior, cut it. Test rule against real agent runs before keeping it.
- Keep one source of truth. State each rule once. Env files, directory layout, command help state themselves. Document convention only when env does not state it.
- Delete dead lines. Remove lines that no longer change behavior.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| WFA-1 | Vague adjectives | Instructs agent to "Make it robust" or "Ensure quality" | Agent hallucinates arbitrary checks | Specify exact invariant or assertion |
| WFA-2 | Deep conditionals | Nests if-else logic 4+ levels deep in narrative prose | Instruction drift and skipped branches | Flatten into a decision table |
| WFA-3 | Prose walls | Packs dense operational instructions into uninterrupted paragraphs | Agent drops secondary constraints | Split into bulleted constraints |
| WFA-4 | Fuzzy exit | Uses subjective exit condition like "Ensure it looks right" | Premature termination without verification | Anchor to exit code or file existence |
| WFA-5 | Passive voice | Writes "changes should be applied" without actor | Ambiguous responsibility for actions | Use direct imperative verbs |
| WFA-6 | Runbook creep | Inlines exhaustive reference catalogs into main runbook | Context budget blowout | Move reference manuals to `references/` |

## Boundaries

Apply structure and style rules to prose only. Leave these byte for byte:
- Code fences and inline code, including YAML frontmatter blocks and JSON.
- SQL, shell commands, file paths, and tree output.
- Quoted slop examples that show banned pattern on purpose.

Leave code unchanged. Apply prose rules to prose only. Never rename symbol, restyle sample, or reflow command to satisfy prose rule.

## Quick audit checklist

Run this before deploying any agent file:

| Check | Passing condition |
|---|---|
| Frontmatter | 1 to 64 character kebab-case name equal to directory, description with "Use when" and "Don't use for" |
| Hierarchy | Primary steps, secondary rules, and tertiary references separated |
| Context load | Main file under 250 lines, reference over 100 lines moved to `references/` |
| Completion criteria | Every step ends on an artifact-anchored binary criterion |
| Anti-patterns | Anti-pattern table adheres to 5-column schema with stable IDs |
| Verification | Passes `lint_skill.py` with zero errors and line budget is verified |
