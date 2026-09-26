---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs, requiring fresh verification command output before making assertions.
---

# Verification before completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle.** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The iron law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The gate function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common failures

| Claim | Requires | Not Sufficient |
|---|---|---|
| Tests pass | Test command output showing 0 failures | Previous run, "should pass" |
| Linter clean | Linter output showing 0 errors | Partial check, extrapolation |
| Build succeeds | Build command returning exit 0 | Linter passing, logs look good |
| Bug fixed | Test verifying original symptom passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red flags

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit, push, or open a PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization prevention

| Excuse | Reality |
|---|---|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key patterns

### Tests

```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

### Regression tests (TDD red-green)

```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

### Build

```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

### Requirements

```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

### Agent delegation

```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```


## Git state and documentation preservation gate

Run these git checks before making any completion claim:

1. Execute `git status --short` to verify all touched files.
2. Inspect deleted files marked with `D`.
   - Core files must never be deleted without an explicit user prompt. Protected files include `CODEBASE.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`, and `.env.example`.
   - If any core documentation file was deleted inadvertently, restore it immediately using `git checkout -- <file>`.
3. Confirm that untracked temporary files, scratch scripts, or dump files are either cleaned up or added to `.gitignore`.

## Scoped linter and code style verification

Run linters against modified files to prevent shipping formatting bugs or breaking pre-commit hooks:

1. Detect configured linters:
   - For PHP or Laravel, check `composer.json` for `laravel/pint` or `phpstan/phpstan`.
   - For JavaScript or TypeScript, check `package.json` for `eslint`, `biome`, or `prettier`.
2. Scope execution to modified files:
   - Identify touched files using `git diff --name-only`.
   - Run the linter strictly against those files, such as `vendor/bin/pint --test path/to/File.php` or `npx eslint path/to/File.tsx`.
   - Do not execute full-repository scans that pull in pre-existing legacy errors outside the active scope.
3. If no linter is configured in project manifests, record "none configured" under linter status in the verification report without failing the gate.

## Automated web performance and accessibility gate

For web applications with automated auditing configured, consult `references/lighthouse-ci.md` to run Lighthouse CI assertions against production builds.

## Why this matters

From 24 failure memories:
- Your human partner said "I don't believe you", which broke trust
- Undefined functions shipped and crashed in production
- Missing requirements shipped with incomplete features
- Time wasted on false completion, redirect, and rework
- Violates the rule that honesty is a core value

## When to apply

Always verify before:
- ANY variation of success or completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

The rule applies to:
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion or correctness

## The bottom line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
