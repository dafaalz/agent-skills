---
name: code-review
description: Use when requesting review for code changes, evaluating review feedback, pushing back against incorrect suggestions, or verifying review fixes. Don't use for automated test execution or lint fixing.
---

# Code review

Unify requesting and receiving code review into a single disciplined workflow. Catch regressions early, protect architectural boundaries, and evaluate all review feedback against codebase reality before applying fixes.

## Overview and core principles

Code review demands technical rigor rather than emotional performance or unverified agreement.

Follow these core principles:
- Review early, review often. Request review after each discrete task or major feature to prevent compounding defects.
- Verify before implementing. Never accept reviewer suggestions blindly. Check codebase truth and test suites first.
- Technical correctness over social comfort. Maintain skepticism. Push back with concrete facts when suggestions degrade architecture.
- Structural audit depth. Consult `references/architectural-lenses.md` for classic engineering lenses and logic defect categories.
- Comment hygiene. Consult `references/comment-hygiene.md` to prune AI conversational narration while preserving critical business context.

## Phase 1. Requesting code review

Dispatch an isolated code reviewer subagent to catch defects before they cascade into downstream tasks. Provide precise context and git ranges without polluting the reviewer with conversational session history.

### When to request review

Request code review under the following mandatory conditions:
- After completing each task in subagent-driven development.
- After finishing a major feature branch.
- Before merging any working branch into the main trunk.

Request review optionally when encountering complex bug fixes, before significant refactoring, or when stuck and requiring an objective fresh perspective.

### Step 1. Commit boundary extraction and reviewer dispatch

Follow this procedure to extract commit boundaries and dispatch the reviewer:

1. Extract git commit SHAs:
```bash
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```

When reviewing across a feature branch, resolve `BASE_SHA` from the merge base with trunk:
```bash
BASE_SHA=$(git merge-base origin/main HEAD)
HEAD_SHA=$(git rev-parse HEAD)
```

2. Inspect the git diff statistics before dispatching:
```bash
git diff --stat ${BASE_SHA}..${HEAD_SHA}
```

3. Dispatch the code reviewer subagent using the template at `references/code-reviewer-prompt.md`. Populate all template variables:
- `WHAT_WAS_IMPLEMENTED`. The exact feature, fix, or module completed.
- `PLAN_OR_REQUIREMENTS`. The task specification or requirements reference.
- `BASE_SHA`. Starting commit SHA for the diff range.
- `HEAD_SHA`. Ending commit SHA for the diff range.
- `DESCRIPTION`. Brief summary of architectural decisions and changed files.

Completion criterion. The code reviewer subagent is dispatched with verified commit SHA boundaries, diff stats, and requirements context.

### Step 2. Finding triage and priority ranking

Categorize all review findings into three priority tiers:
- Critical. Bugs, security vulnerabilities, data loss risks, broken invariants, or failing tests. Fix these immediately before any further work.
- Important. Architectural debt, missing error handling, test coverage gaps, or performance regressions. Address these before merging.
- Minor. Style inconsistencies, naming improvements, or documentation polish. Track or address these after functional concerns pass.

Completion criterion. Every review item is cataloged into Critical, Important, or Minor tier with confirmed file locations.

### Workflow integration

Align review cadence with development workflows:
- Subagent-driven development. Review after each task to catch issues before they compound.
- Executing plans. Review after each batch of tasks, apply verified fixes, and proceed.
- Ad-hoc development. Review before branch merges or whenever architectural doubts arise.

## Phase 2. Evaluating and receiving feedback

Review comments represent hypotheses to evaluate, not unilateral commands to execute. Process every piece of feedback through deliberate verification.

### Step 3. Feedback verification and pushback loop

Follow this six-step loop for every review item:
1. Read. Process the entire review item without defensive or emotional reactions.
2. Understand. Restate the core technical requirement in your own words.
3. Verify. Inspect the codebase, git history, and tests to confirm whether the premise matches reality.
4. Evaluate. Assess whether the proposed change is technically sound for this specific stack.
5. Respond. Provide a factual technical response or reasoned pushback.
6. Implement. Apply approved modifications one item at a time, running tests after each edit.

Completion criterion. All review comments verified against codebase truth, with ambiguous items clarified and grounded counter-arguments formulated where architecture is degraded.

### Banned performative agreement

Never generate performative agreement, excessive gratitude, or subservient conversational fillers.

Strictly avoid phrases like these:
- "You're absolutely right!"
- "Great point!" or "Excellent catch!"
- "Thanks for pointing that out!"
- "Let me implement that right away!"

Respond instead with direct technical substance:
- State the factual requirement or issue directly.
- Point to the specific file and line under review.
- Confirm the fix factually, such as "Fixed date validation in search.ts by rejecting non-ISO strings."
- Jump directly to running tests and showing diffs. Actions carry authority over words.

### Handling unclear items

Never guess intent or apply partial assumptions when review comments lack clarity.

Apply this clarification protocol:
- Stop immediately when any item in a review list is ambiguous.
- Do not implement clear items prematurely if ambiguous items may alter shared architecture.
- State exactly which items are understood and ask targeted questions regarding the unclear items.
- Resume implementation only after requirements are fully unambiguous.

### Architectural integrity and counter-argument protocol

Protect system boundaries when suggestions violate Single Responsibility Principle, introduce tight coupling, or cause lifecycle mismatches:
- Never accept anti-patterns to avoid interpersonal friction.
- Check blast radius across modules. Verify whether the suggestion forces unrelated domains into a shared file or puts request-time logic into static initialization.
- Ground counter-arguments in external consensus. Run targeted searches using official framework documentation or industry standards before responding.
- Formulate a structured technical counter-argument. State the concrete tradeoff, cite the authoritative source, and propose a clean, decoupled alternative that satisfies the caller's true requirement.

### YAGNI verification

Reviewers frequently recommend building speculative abstraction layers, extra configuration flags, or unused data exports.

Verify necessity using this process:
1. Search the codebase for actual call sites using grep or file search tools.
2. If the feature has zero active callers, reject the abstraction and propose removing dead code instead.
3. If active callers exist, implement the minimum clean logic required to satisfy those callers without speculative generalizations.

### Step 4. Surgical remediation and regression pass

Execute accepted review changes methodically to avoid compound regressions:
- Clarify ambiguous items first before touching code.
- Fix blocking and critical bugs first, including broken tests and security concerns.
- Apply simple localized fixes second, such as typos, imports, or boundary checks.
- Address complex refactorings and structural modifications last.
- Test each fix individually. Run targeted test suites immediately after modifying each file.
- Execute full test suites and linters after all items are resolved to confirm zero regressions.

Completion criterion. Accepted fixes implemented one by one, each verified by targeted test runs, followed by a clean full test suite pass.

### Handling pushback and corrections

Navigate disagreements with technical facts:
- When pushing back, reference test results, benchmark metrics, or architectural constraints rather than personal preference.
- If you pushed back and later discover the reviewer was correct, acknowledge the facts directly without lengthy apologies.
- State the verified finding plainly, such as "Verified the 10.15 backward compatibility requirement. Implementing the fallback branch now."

### Review anti-patterns

Review these common pitfalls and their corrections:

| Anti-pattern | Correct practice |
|---|---|
| Performative agreement | State technical facts directly or apply the fix |
| Blind implementation | Verify suggestions against codebase truth first |
| Batching fixes without testing | Implement one item at a time and test each |
| Assuming reviewer is always right | Verify if proposed changes break existing features |
| Avoiding pushback | Prioritize technical correctness over comfort |
| Partial implementation | Clarify ambiguous items before writing code |
| Speculative generalizations | Check YAGNI by grepping for actual callers |

### Thread replies

Reply directly in the comment thread for inline GitHub pull request comments rather than submitting top-level PR comments. Keep all discussion tied to the relevant line diff.
