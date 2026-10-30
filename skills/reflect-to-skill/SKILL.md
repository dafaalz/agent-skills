---
name: reflect-to-skill
description: Use when reflecting on conversation sessions, analyzing failure modes, bugs, or user corrections, and grafting preventive rules into agent skills to prevent recurrence. Don't use for generic session summaries without skill updates (use summarize), application code debugging (use systematic-debugging), or writing end-user documentation (use technical-writing).
---

# Reflect to skill

Distill failures, regressions, and user corrections from completed agent sessions into sharp, permanent rules across relevant agent skills.

## Overview

When an agent stumbles on a bug, generates an unintended UI defect, or receives course corrections from the user, the incident provides the exact failure envelope needed to harden instructions. This skill extracts those mechanics and grafts concrete invariants into existing or new skills so subsequent sessions never repeat the error.

<HARD-GATE>
Write-Target Boundary. Modify only `skills/<target>/SKILL.md` and `skills/<target>/references/*.md` in Author mode, and only after the user has reviewed the exact diff in `.agents/state/reflect-to-skill/<target>-diff.txt` and confirmed the graft. Writes under `.agents/state/reflect-to-skill/` are always permitted. Do not modify application source code, test suites, database schemas, or package lockfiles. Never graft a rule whose target skill was selected by heuristic alone without user confirmation.

Before writing to any skill file, write `.agents/state/reflect-to-skill/<target>-before.md` containing the original content verbatim for full reversibility via `git restore --worktree --staged -- skills/<target>/SKILL.md` plus `git clean -fd skills/<target>/references/`.
</HARD-GATE>

## Modes

Declare the active operating mode before executing any steps:
- Author mode (default): Analyze session failures, propose diffs, obtain explicit user confirmation, and apply verified patches to target skills. Run Steps 1 through 4 sequentially.
- Audit mode: Analyze session failures and output proposed skill patches to `.agents/state/reflect-to-skill/proposed-patches.md` without mutating skill files. Run Steps 1 through 3 only and halt.

## Workflow

Follow these four steps in sequence.

### Step 1. Session failure extraction and evidence logging

Inspect conversation logs, user interventions, error logs, and git diffs to isolate concrete defects:
1. Locate user interventions and course corrections. Identify where the user flagged broken output or sent visual evidence of distorted UI.
2. If the user or an auditor reports a defect in text attributed to disk (skill file, plan, documentation), run `git log -S "<exact string>" -- <path>` before accepting or rejecting the report. If `git log -S` returns empty, the string never existed on disk and the report is paste-fidelity divergence, not a disk defect. Record the result in `.agents/state/reflect-to-skill/disambiguation.json` with `finding_id`, `string_searched`, `git_log_exit_code`, `commit_hits`, and `verdict: disk-defect | paste-divergence | no-match`.
3. Cross-reference with git history and terminal output to capture the exact broken code snippet, failing test, or visual artifact.
4. Categorize the defect into one structural failure class: syntax or runtime bug, styling or rendering artifact, execution or motion defect, or verification gap.

Completion criterion. `.agents/state/reflect-to-skill/incident-log.json` exists on disk recording each defect with its user trigger, broken snippet, and operational failure category.

### Step 2. Root cause mapping and skill routing

Trace each defect to the governing skill using deterministic lookup.

| Domain | Governing skill |
|---|---|
| CSS rendering, typography, tokens, layout | `frontend-design` |
| Transitions, keyframes, physics, reduced motion | `ui-motion` |
| Heuristics, accessibility, forms, tap targets | `ui-ux-review` |
| Backend Eloquent, controllers, artisan commands | `laravel` |
| Verification procedures and test patterns | `verification-before-completion` or `testing-patterns` |
| Agent instructions, prompts, skill documentation | `writing-for-agents` |
| User-facing prose and anti-slop review | `unslop` |
| Human documentation, README, RFC | `technical-writing` |

1. Identify the governing skill domain from the table.
2. Inspect the governing skill using `view_file`. Audit why the failure occurred: missing invariant, vague completion criterion, or missing anti-pattern entry.
3. Record target resolution. Require user confirmation if domain routing is ambiguous.

Completion criterion. `.agents/state/reflect-to-skill/target-resolution.json` exists on disk with `target_skill`, `target_section`, and `resolution_source`.

### Step 3. Sharp rule synthesis

Draft rules using the standards from `writing-for-agents` and `unslop`:
1. Apply positive framing and leading words. Pair every negative prohibition with an immediate required action on the same line.
2. Structure anti-pattern additions using the standard schema: ID, Title, Pattern description, Why it fails, Concrete fix. Consult `references/grafting-recipes.md` for copy-paste templates when adding invariants and anti-pattern entries.
3. Enforce mechanical grounding. Specify exact CSS classes, attribute names, thresholds, or API patterns rather than general advice.
4. Verify anti-slop compliance. Require zero em dashes, zero en dashes, sentence case headings, active verbs, and zero conversational filler.

Completion criterion. Written candidate patch snippets drafted for every diagnosed failure, saved to `.agents/state/reflect-to-skill/proposed-patches.md`.

### Step 4. Budget check, two-phase grafting, and verification

Graft candidate rules into target skills using a two-phase write protocol.

#### Phase 1. Propose

1. Confirm main `SKILL.md` remains strictly under 250 lines. Move extended catalogues into `references/` if budget requires.
2. Write `.agents/state/reflect-to-skill/<target>-before.md` with original file content.
3. Write `.agents/state/reflect-to-skill/<target>-proposed.md` with updated content.
4. Generate the diff: `diff -u .agents/state/reflect-to-skill/<target>-before.md .agents/state/reflect-to-skill/<target>-proposed.md > .agents/state/reflect-to-skill/<target>-diff.txt`.

#### Phase 2. Apply and verify

1. On explicit user confirmation, apply the diff to `skills/<target>/SKILL.md`.
2. Run `python3 skills/review-a-skill/scripts/lint_skill.py skills/<target>`.
3. Record the outcome in `.agents/state/reflect-to-skill/<target>-verification.json` with `lint_exit_code` and the rollback command.

Completion criterion. Target skill updated, `lint_skill.py` exits with status code 0, line count verified under 250 lines, and `.agents/state/reflect-to-skill/<target>-verification.json` exists on disk.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| RTS-1 | Vague rule graft | Adds "Be more careful" or "Always check layout" without trigger | Agent cannot act on instruction and failure recurs | Specify exact prohibited action and concrete permitted alternative |
| RTS-2 | Unbounded growth | Grafts rules without pruning until skill exceeds 250 lines | Context budget blowout degrades model compliance | Move extended catalogues and recipes into `references/` |
| RTS-3 | Redundant skill creation | Creates a new skill instead of patching existing governing skill | Fragments discovery and duplicates rules across repo | Graft into the existing domain skill |
| RTS-4 | Unpaired prohibition | Adds "Never do X" without specifying permitted alternative | Paralyzes agent when edge case demands action | Pair every prohibition with an immediate required alternative |
| RTS-5 | Heuristic routing | Selects target skill by keyword match without verification | Rules land in wrong skills and remain undiscovered | Confirm target path via explicit lookup or user decision |
| RTS-6 | Unsandboxed mutation | Overwrites skill files directly without backup or diff preview | Corrupts governing skills for subsequent sessions | Enforce two-phase propose/diff/confirm protocol with rollback |
| RTS-7 | Validator conflict of interest | Edits `skills/review-a-skill/scripts/lint_skill.py` or test harness during reflection to make newly grafted rules pass | Rule passes linter validation because validator was weakened, not because rule is correct | Validator changes require a separate commit with `[validator]` subject suffix and self-test fixtures as specified in `verification-before-completion` |

## Boundary isolation

Execute skill grafting exclusively on skill directories (such as `skills/` or `.agents/skills/`). Never alter application project files, database migrations, or test files during a skill reflection run.

Keep code fences, backticked tokens, and syntax samples exact. Apply prose rules only to explanatory instructions.

## Quick audit checklist

Run this check before finishing any reflection task:

| Check | Passing condition |
|---|---|
| Evidence grounded | Every drafted rule links directly to a concrete bug or user correction from session |
| Routing verified | Correct governing skill identified via explicit lookup and recorded in JSON |
| Budget maintained | Main `SKILL.md` of target skills remains strictly under 250 lines |
| Sharp framing | Every prohibition paired with an explicit positive action on the same line |
| Anti-slop clean | Zero em dashes, zero en dashes, sentence case headings, and active voice |
| Anti-patterns | Anti-pattern table adheres to 5-column schema with stable IDs |
| Two-phase protocol | Backup taken, diff generated, user confirmed, and linter verified |
