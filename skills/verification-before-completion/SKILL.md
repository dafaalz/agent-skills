---
name: verification-before-completion
description: Require fresh terminal verification evidence before claiming tasks are complete. Use when about to claim work is complete, fixed, or passing, before committing or creating PRs, requiring fresh verification command output before making assertions. Don't use for initial exploratory brainstorming or rough drafting phases.
---

# Verification before completion

Execute verification commands and confirm terminal exit codes before asserting completion. Do not assert that code compiles or tests pass without running the relevant command in the active turn.

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Never rely on cached assertions, previous turn outputs, or assumptions. Run the verification command in the current turn before stating that the task is finished.

## Workflow

Follow these five steps in sequence before claiming completion:

### Step 1. Command identification

Identify the deterministic command that validates the exact claim, including test runners, linters, and type checkers.

Completion criterion. An exact terminal command selected that directly inspects the modified code or behavior.

### Step 2. Fresh command execution

Execute the verification command in full without relying on cached logs or previous runs.

Completion criterion. Fresh command execution output captured in the current turn.

### Step 3. Output inspection and exit code triage

Read the full terminal output, verify exit code 0, and confirm zero errors or failures.

Completion criterion. Terminal output confirms zero failing assertions, zero type errors, and zero unhandled exceptions.

### Step 4. Git diff and repository safety gate

Inspect working tree status and diffs to confirm no core documentation files were inadvertently deleted and untracked artifacts are cleaned up.

Completion criterion. `git status --short` confirms all touched files are intentional, with zero unwanted file deletions or orphan scratch files.

### Step 5. Claim with evidence

State the completion claim citing the exact command run, test counts, and exit status.

Completion criterion. The user receives a factual statement backed by terminal evidence, with zero unverified assumptions.

## Common failures

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | Test command output showing 0 failures | Previous run, "should pass" |
| Linter clean | Linter output showing 0 errors | Partial check, extrapolation |
| Build succeeds | Build command returning exit 0 | Linter passing, logs look good |
| Bug fixed | Test verifying original symptom passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red flags

- Using "should", "probably", or "seems to".
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!").
- Preparing to commit, push, or open a PR without running tests.
- Trusting agent success reports without inspecting diffs.
- Relying on partial verification.
- Any wording implying success without having run verification.

## Rationalization prevention

| Excuse | Reality |
|---|---|
| "Should work now" | Run the verification command directly |
| "I'm confident" | Confidence is not evidence |
| "Just this once" | Zero exceptions |
| "Linter passed" | Linter is not a compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion does not excuse verification |
| "Partial check is enough" | Partial check proves nothing |
| "Different words so rule does not apply" | Procedural invariants apply to all claims |

## Key patterns

### Tests
- Valid action: Execute the test command, verify clean output (such as 34 of 34 passed), then report that tests pass.
- Prohibited action: Asserting "should pass now" or "looks correct" without running the test command.

### Regression tests (TDD red-green)
- Valid action: Write the test, run it to confirm it passes with the fix, temporarily revert the fix to confirm the test fails, and restore the fix.
- Prohibited action: Claiming regression coverage without verifying the failure step.

### Build
- Valid action: Run the build command and verify exit code 0 before asserting compilation success.
- Prohibited action: Claiming the build passes based solely on a passing linter.

### Requirements
- Valid action: Re-read the plan or issue, create an itemized checklist, verify each item with evidence, and report completion status.
- Prohibited action: Concluding a feature is complete merely because test suites pass.

### Agent delegation
- Valid action: When an agent reports success, inspect the version control diff directly, verify the changes, and report the confirmed state.
- Prohibited action: Forwarding agent success claims without independent diff verification.

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
