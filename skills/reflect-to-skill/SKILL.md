---
name: reflect-to-skill
description: Use when reflecting on conversation sessions, analyzing failure modes, bugs, or user corrections, and grafting preventive rules into agent skills to prevent recurrence. Don't use for generic session summaries without skill updates, application code debugging, or writing end-user documentation.
---

# Reflect to skill

Distill failures, regressions, and user corrections from completed agent sessions into sharp, permanent rules across relevant agent skills.

## Overview

When an agent stumbles on a bug, generates an unintended UI defect, or receives course corrections from the user, the incident provides the exact failure envelope needed to harden instructions. This skill extracts those mechanics and grafts concrete invariants into existing or new skills so subsequent sessions never repeat the error.

## Modes

Pick an execution mode before Step 1:
- Author mode (default). Analyze session failures and patch target skills directly in place.
- Audit mode. Analyze session failures and output proposed skill patches and rule snippets without mutating skill files.

## Workflow

Follow these four steps in sequence.

### Step 1. Session failure extraction and evidence logging

Inspect conversation logs, user interventions, error logs, and git diffs to isolate concrete defects:

1. Locate user interventions and course corrections. Identify where the user said things like "riwayat pesan hilang", "pesan tidak muncul", or sent visual screenshots of distorted UI.
2. Cross-reference with git history and terminal output to capture the exact broken code snippet, failing test, or visual artifact.
3. Categorize the defect into its structural failure class:
   * Syntax or runtime bug (race condition, unhandled state, null dereference).
   * Styling or rendering artifact (whitespace leak, contrast failure, unbounded container).
   * Execution or motion defect (bulk animation shock, missing exit transition, excessive duration).
   * Verification gap (skipping visual audit, false positive test assertions).

Completion criterion. A written log documents each defect with its user trigger, broken code snippet or visual evidence, and operational failure category.

### Step 2. Root cause mapping and skill routing

Trace each defect to the skill that should have prevented it:

1. Identify the governing skill domain:
   * CSS rendering, typography, tokens, layout: `frontend-design`.
   * Transitions, keyframes, physics, reduced motion: `ui-motion`.
   * Heuristics, accessibility, forms, tap targets: `ui-ux-review`.
   * Backend Eloquent, controllers, artisan commands: `laravel`.
   * Verification procedures and test patterns: `verification-before-completion` or `testing-patterns`.
2. Inspect the governing skill using `view_file`. Audit why the failure occurred:
   * Missing invariant (the failure mode was never cataloged).
   * Vague completion criterion (the rule used subjective terms like "ensure good layout").
   * Missing anti-pattern entry (the specific code pattern had no explicit named entry).
3. If no existing skill governs the domain, create a new skill directory following the AgentSkills standard.

Completion criterion. Target skills identified with explicit file paths and diagnosed root causes indicating whether the defect stems from a missing invariant, vague criterion, or missing anti-pattern.

### Step 3. Sharp rule synthesis

Draft rules using the standards from `writing-for-agents` and `unslop`:

1. Apply positive framing and leading words. Pair every negative prohibition with an immediate required action on the same line.
2. Structure anti-pattern additions using the standard pattern:
   * Named tell heading.
   * Description of the exact code or layout pattern.
   * "Why it fails" paragraph explaining the mechanical breakdown.
   * "Fix" paragraph providing the exact code snippet, CSS utility, or formula.
3. Enforce mechanical grounding. Specify exact CSS classes, attribute names, thresholds, or API patterns rather than general advice.
4. Verify anti-slop compliance. Ensure zero em dashes, zero en dashes, sentence case headings, active verbs, and zero conversational filler.

Completion criterion. Written candidate patch snippets drafted for every diagnosed failure, containing grounded code examples, explicit fixes, and zero anti-slop violations.

### Step 4. Budget check, grafting, and verification

Graft candidate rules into target skills while protecting context budgets:

1. Audit target skill line budget:
   * Confirm the main `SKILL.md` remains strictly under 250 lines.
   * If adding rules pushes `SKILL.md` over 250 lines, move detailed recipes or catalogues into `references/`.
2. Apply patches to skill files using file edit tools.
3. Run `git diff` against modified skills to verify that only target lines changed without collateral formatting mutations.
4. Verify modified skills against the quick audit checklist below.

Completion criterion. Target skills patched, verified via `git diff`, line budgets confirmed under 250 lines, and all checklist checks passing.

## Boundary isolation

Execute skill grafting exclusively on skill directories (such as `.agents/skills/` or config skills). Never alter application project files, database migrations, or test files during a skill reflection run.

Keep code fences, backticked tokens, and syntax samples exact. Apply prose rules only to explanatory instructions.

## Rule grafting templates

Consult `references/grafting-recipes.md` for copy-paste structures when adding invariants, anti-pattern entries, and failure triage tables.

## Quick audit checklist

Run this check before finishing any reflection task:

| Check | Passing condition |
|---|---|
| Evidence grounded | Every drafted rule links directly to a concrete bug or user correction from the session |
| Routing verified | Correct governing skill identified via `view_file` |
| Budget maintained | Main `SKILL.md` of target skills remains strictly under 250 lines |
| Sharp framing | Every prohibition paired with an explicit positive action on the same line |
| Anti-slop clean | Zero em dashes, zero en dashes, sentence case headings, and active voice |
| Clean diff | `git diff` confirms exact patch boundaries with zero accidental edits |
