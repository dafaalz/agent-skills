---
name: code-review
description: "Use when requesting review for code changes, evaluating review feedback, pushing back against incorrect suggestions, or verifying review fixes. Don't use for automated test execution (use testing-patterns) or lint fixing (apply the lint fix directly and verify with the linter's own command)."
---

# Code review

Unify requesting and receiving code review into a single disciplined workflow. Catch regressions early, protect architectural boundaries, and evaluate all review feedback against codebase reality before applying fixes.

## Overview and core principles

Review code with technical rigor rather than emotional performance or unverified agreement.

Follow these core principles:
- Review early, review often. Request review after each discrete task or major feature to prevent compounding defects.
- Two-axis separation. Review changes independently across Standards (repo standards and baseline code smells) and Spec (originating issue or requirements). Run axes in parallel sub-agents to prevent context pollution.
- Verify before implementing. Never accept reviewer suggestions blindly. Check codebase truth and test suites first.
- Technical correctness over social comfort. Maintain skepticism. Push back with concrete facts when suggestions degrade architecture.
- Adversarial disproof. Apply doubt-driven evaluation. Never assume code is correct because it looks clean or passes happy-path tests. Actively formulate disproof hypotheses showing where invariants could break.
- Structural audit depth. Consult `references/architectural-lenses.md` for classical engineering lenses, logic defects, and Fowler code smell baseline.
- Comment hygiene. Consult `references/comment-hygiene.md` to prune AI conversational narration while preserving critical business context.
- Feedback discipline. Consult `references/feedback-protocol.md` for counter-arguments, YAGNI verification, and anti-performative response rules.

<HARD-GATE>
Write-Target Boundary. In Request mode, write only to `.agents/state/code-review/`. In Feedback mode, modify only files that appear in the reviewed commit range. Never refactor working logic outside the reviewed commit range, change formatting conventions across unreviewed files, or run destructive git commands (`reset --hard`, `rebase -i`, `push --force`). Do not modify files owned by the `conventional-commit` or `pull-request` skills' write targets.
</HARD-GATE>

## Modes

Select one operating mode before Step 1:
- Request mode (default). Run Steps 1 through 4 to dispatch and aggregate review findings. Emit `.agents/state/code-review/review.md`.
- Feedback mode. Run Steps 5 and 6 only, consuming `.agents/state/code-review/review.md` if it exists. Emit `.agents/state/code-review/feedback-response.md`.
- End-to-end mode. Run Steps 1 through 6 in sequence.

Do not interleave modes. Steps 1 through 4 belong exclusively to Request mode or the first half of End-to-end mode. Steps 5 and 6 belong exclusively to Feedback mode or the second half of End-to-end mode.

## Phase 1. Requesting code review

Dispatch isolated reviewer sub-agents across Standards and Spec axes to catch defects before they cascade downstream.

### Step 1. Commit boundary extraction and pre-flight validation

Follow this procedure to extract commit boundaries and validate git references:

1. Identify the fixed point reference, such as a commit SHA, branch name, tag, or merge base. When unspecified, prompt the user for the reference.
2. Resolve commit references:
```bash
git rev-parse --verify "${FIXED_POINT}"
BASE_SHA=$(git merge-base "${FIXED_POINT}" HEAD)
HEAD_SHA=$(git rev-parse HEAD)
```
3. Inspect diff statistics and verify that the target diff is non-empty:
```bash
git diff --stat "${BASE_SHA}"..."${HEAD_SHA}"
```
If `git rev-parse` fails or if the diff contains zero changes, stop execution immediately.

Completion criterion. Target ref is verified with `git rev-parse`, merge base is resolved, and the diff is confirmed non-empty.

### Step 2. Spec and standards discovery

Identify the inputs for each review axis before dispatching sub-agents:

1. Identify specification sources in order of priority:
- Issue references in commit messages matching patterns like `#123`, `Closes #45`, or GitLab `!67`.
- Explicit path or URL passed by the user.
- Spec files in `docs/` or `specs/` matching the branch or feature name.
When no spec exists, ask the user. If unavailable, mark the Spec axis as skipped.

2. Identify standards sources:
- Repo guideline files including `CODING_STANDARDS.md` or `CONTRIBUTING.md`.
- Baseline Fowler code smells in `references/architectural-lenses.md` section 3. Repo standards always override the baseline.

Completion criterion. Specification text and repository standards files are located or explicitly marked unavailable.

### Step 3. Two-axis parallel reviewer dispatch

Dispatch the Standards and Spec reviewer sub-agents in parallel using templates in `references/code-reviewer-prompt.md`. Pass each sub-agent the following invariant envelope without paraphrasing or summarizing:

```yaml
# STANDARDS ENVELOPE (DO NOT MODIFY)
axis: standards
diff_command: "git diff BASE_SHA...HEAD_SHA"
commit_log_command: "git log BASE_SHA..HEAD --oneline"
base_sha: "<sha>"
head_sha: "<sha>"
standard_files:
  - "<explicit path 1>"
  - "<explicit path 2>"
smell_reference: "skills/code-review/references/architectural-lenses.md#section-3"
required_output_schema:
  - "id"
  - "tier"
  - "file"
  - "line"
  - "finding"
  - "suggested_fix"
word_budget: 400
```

```yaml
# SPEC ENVELOPE (DO NOT MODIFY)
axis: spec
diff_command: "git diff BASE_SHA...HEAD_SHA"
spec_source: "<explicit path or URL or 'unavailable'>"
required_output_schema:
  - "id"
  - "tier"
  - "file"
  - "line"
  - "spec_quote"
  - "finding"
  - "suggested_fix"
word_budget: 400
```

If the specification is marked unavailable, dispatch only the Standards sub-agent.

Completion criterion. Both sub-agents are dispatched concurrently with verified diff parameters and strict 400-word budget constraints.

### Step 4. Independent axis aggregation and triage

Aggregate findings from both sub-agents without merging or cross-ranking findings:

1. Present findings under separate `## Standards` and `## Spec` markdown sections.
2. Never rerank findings across axes. Code that follows all standards may still fail the specification, and code that implements the specification may violate repository conventions.
3. Conclude with a single summary line reporting total findings per axis and the highest-severity issue within each separate axis.
4. Categorize findings within each axis into three priority tiers:
- Critical. Bugs, broken functionality, security risks, or violated specification invariants. Fix these immediately.
- Important. Missing error handling, architectural debt, smell baseline issues, or test gaps. Address these before merging.
- Minor. Style inconsistencies or documentation improvements. Address these after functional items pass.

Completion criterion. `.agents/state/code-review/review.md` exists on disk. The file contains two top-level sections, `## Standards` and `## Spec`. Every finding under each section is a table row with columns `ID | Tier (Critical|Important|Minor) | File | Line | Finding | Suggested fix`. The `## Spec` section is omitted (with an explicit `spec: skipped` line) only if Step 2 marked the Spec axis unavailable.

## Phase 2. Evaluating and receiving feedback

Review comments represent hypotheses to evaluate, not unilateral commands to execute. Process every piece of feedback through deliberate verification. Consult `references/feedback-protocol.md` for detailed rules on banned performative agreement, ambiguity clarification, YAGNI verification, and technical pushback.

### Step 5. Feedback verification and pushback loop

Follow this six-step loop for every review item:
1. Read. Process the entire review item without defensive or emotional reactions.
2. Understand. Restate the core technical requirement in your own words.
3. Verify. Inspect the codebase, git history, and tests to confirm whether the premise matches reality.
4. Evaluate. Assess whether the proposed change is technically sound for this specific stack.
5. Respond. Provide a factual technical response or reasoned pushback.
6. Plan remediation. Queue approved modifications for Step 6 and run tests after each subsequent edit.

Completion criterion. All review comments verified against codebase truth, recorded in `.agents/state/code-review/feedback-response.md`, with ambiguous items clarified and grounded counter-arguments formulated where architecture is degraded.

### Step 6. Surgical remediation and regression pass

Execute accepted review changes methodically to avoid compound regressions:
- Clarify ambiguous items first before touching code.
- Fix blocking and critical bugs first: resolve broken tests and security concerns before other edits.
- Grep all callers before editing shared functions to fix the root cause once across all call sites.
- Apply simple localized fixes second, such as typos, imports, or boundary checks.
- If taking an intentional shortcut with a known limit, mark it in code using `shortcut: <the limit>, <when to upgrade>`.
- Address complex refactorings and structural modifications last.
- Test each fix individually. Run targeted test suites immediately after modifying each file.
- Execute full test suites and linters after all items are resolved to confirm zero regressions.

Completion criterion. Accepted fixes implemented one by one, each verified by targeted test runs, followed by a clean full test suite pass.

## Adversarial falsification protocol

Reviewers must not evaluate code solely on happy-path execution or cosmetic cleanliness. When auditing diffs touching core business logic, permissions, migrations, or shared utilities:

1. Formulate a failure hypothesis. Ask: under what boundary condition or concurrent state will this change corrupt data or throw unhandled exceptions?
2. Trace the blast radius. Grep all call sites to verify that changed return types, modified parameter orders, or altered error contracts do not break downstream consumers.
3. Verify failure behavior. Inspect whether the code fails loudly and safely when downstream services, network calls, or invalid parameters arrive.
4. Challenge unverified assertions. When a pull request author asserts "this cannot happen", require concrete evidence (a failing-then-passing test or compiler constraint) before accepting the assertion.

Completion criterion. High-stakes review items evaluated with explicit disproof hypotheses and verified downstream blast radius.

## Quick audit checklist

Review this table before completing the code review:

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| CR-1 | Performative agreement | Responds with "You're absolutely right!" or "Great catch!" instead of a technical statement | Masks whether the agent verified the suggestion; trains the user to expect praise instead of evidence | State the factual finding and file path; cite the verification step |
| CR-2 | Blind implementation | Applies a reviewer suggestion without inspecting codebase truth | May break existing behavior that the reviewer did not consider | Run the review protocol Steps 5.1-5.6; verify against tests and callers |
| CR-3 | Fix batching | Applies all findings in one edit and tests once at the end | Regressions compound and become hard to attribute | Implement one item at a time; run targeted test after each |
| CR-4 | Unverified claim of fix | States the fix is done without a targeted test run | User deploys broken code believing it is fixed | Run `verification-before-completion` after each fix |
| CR-5 | Pushback without facts | Disagrees based on preference | Erodes trust and hides real defects | Cite tests, benchmarks, or architectural constraints |
| CR-6 | Skipped clarification | Implements ambiguous items while others remain unclear | Order of operations may invalidate already-applied fixes | Apply the clarification protocol; hold all changes until ambiguity resolves |
| CR-7 | Speculative abstraction | Adds config flags or exports with no call sites | Violates YAGNI and adds maintenance surface | Grep for call sites first; reject if zero |
| CR-8 | Happy-path review | Reviews without adversarial falsification on high-stakes diffs | Boundary, permission, or migration defects ship undetected | Apply the Adversarial falsification protocol before completion |
