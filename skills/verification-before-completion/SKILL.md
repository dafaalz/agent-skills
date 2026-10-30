---
name: verification-before-completion
description: "Use when about to claim work is complete, fixed, or passing, before committing or creating PRs, requiring fresh verification command output before making assertions. Don't use for initial exploratory brainstorming (use brainstorming) or rough drafting phases (verify only before publishing a claim; exploration is exempt until a completion claim is imminent)."
---

# Verification before completion

Execute verification commands and confirm terminal exit codes before asserting completion. Do not assert that code compiles or tests pass without running the relevant command in the active turn.

<HARD-GATE>
Write-Target Boundary. Read verification command output and git state only. Write only to `.agents/state/verification-before-completion/`. Never alter test assertion thresholds, delete failing tests, mock passing states, skip failed steps, or claim completion without a fresh exit-code-0 output in the current turn. Do not state a completion claim until Step 5's verification-receipt.json exists with exit_code 0 in the current turn. Never run destructive git restore on files with unstaged modifications.

When reporting file content in the response, run `shasum -a 256 <path>` first, include the hash and the path adjacent to the pasted content, and paste the file content verbatim from `cat <path>`. Regenerated, paraphrased, or summarized file content without the hash and without the literal `cat` output is treated as unverified. The user or a reviewer can rerun `shasum -a 256 <path>` to confirm the paste matches the disk.

Do not modify any file under `skills/review-a-skill/scripts/`, `skills/*/tests/`, or any file whose path matches `*/lint*.py`, `*/validate*.sh`, or `*/test_runner*.py` in the same commit, pull request, or agent turn as a skill patch. Validator changes require: (a) a commit whose subject ends with `[validator]`, (b) three self-test fixtures in `skills/review-a-skill/scripts/fixtures/lint/<pattern>-{positive,negative,edge}.<ext>`, (c) `python3 skills/review-a-skill/scripts/lint_skill.py --self-test` passing, (d) `shasum -a 256` of the previous and new linter recorded in the commit message. If any of (a)-(d) is missing, the commit is treated as a validator-and-skill co-mutation and rejected.

Validator independence requires the pre-commit hook to be wired into git. Before any skill patch, confirm:
`git config --get core.hooksPath | grep -q 'skills/review-a-skill/scripts'`
If unconfigured, run `git config core.hooksPath "$(pwd)/skills/review-a-skill/scripts"` before continuing.
</HARD-GATE>

## Modes

Select a verification mode before Step 1:
- Scoped turn verification (default). Run Steps 1 through 6 to verify the specific command output and echo receipt for the current task before responding to the user.
- Pre-release gate. Run Steps 1 through 10 in full, including adversarial falsification, git safety, scoped linting, and performance gates before committing or submitting a pull request.

## Boundary isolation

Verification evaluates execution state and test outcomes only. Never alter test assertion thresholds, delete failing tests, or mock passing states to bypass verification gates.

## Workflow

Follow these steps in sequence:

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

Inspect working tree status and diffs. Confirm no core documentation files were inadvertently deleted and untracked artifacts are cleaned up. If in Pre-release gate mode for a pull request, verify that `.agents/state/pull-request/pr-body.md` exists and is consistent with the verified diff.

Completion criterion. `git status --short` confirms all touched files are intentional, with zero unwanted file deletions or orphan scratch files.

### Step 5. Execution-bound receipt recording

Execute verification commands strictly through the trusted executor wrapper to bind receipts directly to subprocess execution:

```bash
python3 skills/verification-before-completion/scripts/run_receipt.py \
  --command "$CMD" \
  --claim "$CLAIM"
```

The executor executes the command, captures raw stdout and stderr to disk, computes cryptographic digests (`stdout_sha256`, `stderr_sha256`), captures git commit and tree SHAs, records ISO8601 timestamps, rejects dummy commands (such as `true` or `:`), and writes `.agents/state/verification-before-completion/verification-receipt.json` and `receipt-hash.txt`.

Completion criterion. `.agents/state/verification-before-completion/verification-receipt.json` exists on disk with fields `claim`, `command`, `argv`, `cwd`, `git_commit`, `git_tree`, `start_time_iso8601`, `end_time_iso8601`, `exit_code` (0), `stdout_sha256`, `stderr_sha256`, `test_count_passed` (integer), and `test_count_failed` (0), with authoritative sha256 recorded in `.agents/state/verification-before-completion/receipt-hash.txt`.

### Step 6. Receipt echo verification

Before emitting any completion claim to the user, verify the claim against disk state:
1. Run `python3 skills/verification-before-completion/scripts/run_receipt.py --verify`.
2. Confirm the command exits with code 0, confirming receipt hash matches `receipt-hash.txt`, exit code is 0, stdout digest matches captured stdout, and command is not a dummy no-op.
3. Read the receipt with `cat .agents/state/verification-before-completion/verification-receipt.json` and quote the `claim`, `command`, `exit_code`, and `stdout_sha256` fields verbatim inside a fenced text code block in the response.
4. The response text must contain the exact strings from the receipt, character for character. Paraphrase, summary, or restatement in different words fails this step.
5. If the receipt does not exist on disk, or if `--verify` fails, halt and do not emit the completion claim.

Completion criterion. `python3 skills/verification-before-completion/scripts/run_receipt.py --verify` exits with status code 0, the response contains a fenced text code block with receipt fields verbatim, and the `shasum -a 256` output matches `.agents/state/verification-before-completion/receipt-hash.txt`. In Scoped turn verification mode, stop here.

### Step 7. Adversarial falsification gate

Before asserting completion on non-trivial logic, schema migrations, security boundaries, or multi-file refactoring, execute an adversarial falsification check:
1. Identify the core invariant that must hold true.
2. Formulate a disproof hypothesis under boundary inputs or concurrent states.
3. Run a targeted negative test case or invalid payload.
4. Record results in `.agents/state/verification-before-completion/falsification.json`.

Completion criterion. `.agents/state/verification-before-completion/falsification.json` exists on disk with fields `invariant`, `disproof_hypothesis`, `test_command`, `test_exit_code`, `observed_result`, and `graceful_failure_confirmed`.

### Step 8. Git state and documentation preservation gate

Run these git checks before completing pre-release verification:
1. Execute `git status --short` and record output to `.agents/state/verification-before-completion/git-state.txt`.
2. Inspect deleted files marked with `D`. Core files must never be deleted without an explicit user prompt. Protected files include `CODEBASE.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`, and `.env.example`.
3. If any protected file was deleted inadvertently, notify the user with recovery options:
   - `git restore --source=HEAD --staged --worktree -- <file>`
   - `git show HEAD:<file> > <file>`
   Do not run any restore command without explicit user selection.

Completion criterion. `.agents/state/verification-before-completion/git-state.txt` exists on disk with git status recorded, protected files preserved, and any recovery plan approved.

### Step 9. Scoped linter gate

Run configured linters strictly against modified files identified via `git diff --name-only`:
1. Check project manifests (`composer.json`, `package.json`) for configured linters (`pint`, `phpstan`, `eslint`, `biome`, `prettier`).
2. Run linters against touched files only. If no linter is configured, record status as `none configured`.
3. Write results to `.agents/state/verification-before-completion/linter.json`.

Completion criterion. `.agents/state/verification-before-completion/linter.json` exists on disk with records for all modified files showing exit code 0 or status `none configured`.

### Step 10. Automated performance gate

Applies conditionally when the repository configures Lighthouse CI or automated benchmarks. Consult `references/lighthouse-ci.md` for execution setup. If unconfigured, record `perf_gate: skipped` in the receipt.

Completion criterion. `.agents/state/verification-before-completion/verification-receipt.json` records `perf_gate: passed` with exit code 0 or `perf_gate: skipped`.

## Common failures

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| VC-1 | Assumed test pass | Claiming tests pass without running them this turn | Cached or hallucinated output | Run the test command in the current turn; capture exit code |
| VC-2 | Extrapolated lint | Assuming linter passes because tests pass | Different tool, different failure surface | Run the linter separately; capture exit code |
| VC-3 | Lint-as-build | Claiming build success from lint success | Lint does not compile | Run the build; capture exit code 0 |
| VC-4 | Assumed fix | Claiming a bug is fixed because code changed | Change without test of original symptom | Write and run the failing-then-passing test |
| VC-5 | Single-pass regression | Claiming regression coverage after one green run | Test may pass for wrong reason | Perform red-green cycle: revert, observe red, restore, observe green |
| VC-6 | Agent self-report | Forwarding subagent "success" without diff inspection | Subagent may fail silently | Inspect `git diff` and re-run verification yourself |
| VC-7 | Passing-test completion | Claiming requirements met because tests pass | Tests may not cover the requirement | Re-read the plan or issue; verify each item with evidence |
| VC-8 | Happy-path falsification | Claiming invariant holds after only positive test | Boundary cases untested | Run the negative test case |

## Rationalization prevention

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| RP-1 | Should-work | "Should work now" | Confidence without evidence | Run the verification command directly |
| RP-2 | Confidence-as-evidence | "I'm confident" | Confidence is not evidence | Run and capture exit code |
| RP-3 | One-time exception | "Just this once" | Exceptions become the norm | Zero exceptions; always run the command |
| RP-4 | Lint-as-build | "Linter passed" | Linter is not a compiler | Run build separately |
| RP-5 | Agent self-report | "Agent said success" | Subagents report optimistically | Inspect `git diff` independently |
| RP-6 | Fatigue | "I'm tired" | Fatigue does not excuse verification | Run the command |
| RP-7 | Partial-check | "Partial check is enough" | Partial check proves nothing about the rest | Run the full command |
| RP-8 | Semantic evasion | "Different words so rule does not apply" | Procedural invariants cover all claims | Apply rule to all completion claims |
| RP-9 | Impossibility assumption | "Edge case is impossible" | Boundary cases are the bug source | Run the negative test case |

## Red flags and key patterns

### Red flags
- RF-1. Using "should", "probably", or "seems to".
- RF-2. Expressing satisfaction before verification ("Great!", "Perfect!", "Done!").
- RF-3. Preparing to commit, push, or open a PR without running tests.
- RF-4. Trusting agent success reports without inspecting diffs.
- RF-5. Relying on partial verification.
- RF-6. Any wording implying success without having run verification.

### Key patterns
- KP-1. Tests. Execute the test command and verify clean output before reporting passing status.
- KP-2. Regression tests. Perform red-green TDD cycle verifying failure before fix.
- KP-3. Build. Verify compiler exit code 0 before asserting build success.
- KP-4. Requirements. Verify each item against an itemized checklist with command evidence.
- KP-5. Agent delegation. Inspect git diff directly when subagents report completion.

## Quick audit checklist

| Check | Passing condition |
|---|---|
| Fresh command output | Direct terminal execution output captured in active turn |
| Zero failures | Exit code 0 with zero test failures or type errors |
| Repository safety | Git working tree clean and protected documentation files intact |
| Scoped linting | Modified files pass configured linters with zero errors |
| Factual claims | Completion claim cites exact commands and passing counts |
| Adversarial check | Negative boundary test confirms invariant holds without silent failure |
| Receipt echo verified | Response text character-for-character quotes disk receipt |
