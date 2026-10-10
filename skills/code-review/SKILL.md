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
- Two-axis separation. Review changes independently across Standards (repo standards and baseline code smells) and Spec (originating issue or requirements). Run axes in parallel sub-agents to prevent context pollution.
- Verify before implementing. Never accept reviewer suggestions blindly. Check codebase truth and test suites first.
- Technical correctness over social comfort. Maintain skepticism. Push back with concrete facts when suggestions degrade architecture.
- Structural audit depth. Consult `references/architectural-lenses.md` for classical engineering lenses, logic defects, and Fowler code smell baseline.
- Comment hygiene. Consult `references/comment-hygiene.md` to prune AI conversational narration while preserving critical business context.

## Phase 1. Requesting code review

Dispatch isolated reviewer sub-agents across Standards and Spec axes to catch defects before they cascade downstream. Provide precise git ranges and requirements without polluting reviewers with conversational session history.

### When to request review

Request code review under the following mandatory conditions:
- After completing each task in subagent-driven development.
- After finishing a major feature branch.
- Before merging any working branch into the main trunk.

Request review optionally when encountering complex bug fixes, before significant refactoring, or when stuck and requiring an objective fresh perspective.

### Step 1. Commit boundary extraction and pre-flight validation

Follow this procedure to extract commit boundaries and validate git references:

1. Identify the fixed point reference, such as a commit SHA, branch name, tag, or merge base. When unspecified, prompt the user for the reference.
2. Resolve commit references:
```bash
git rev-parse --verify ${FIXED_POINT}
BASE_SHA=$(git merge-base ${FIXED_POINT} HEAD)
HEAD_SHA=$(git rev-parse HEAD)
```
3. Inspect diff statistics and verify that the target diff is non-empty:
```bash
git diff --stat ${BASE_SHA}...${HEAD_SHA}
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

Dispatch the Standards and Spec reviewer sub-agents in parallel using templates in `references/code-reviewer-prompt.md`:

1. Standards sub-agent receives:
- The diff command `git diff ${BASE_SHA}...${HEAD_SHA}` and commit list from `git log ${BASE_SHA}..HEAD --oneline`.
- Documented repo standard files.
- The 12 Fowler code smells from `references/architectural-lenses.md`.
- Instruction to report hard standard violations and smell heuristics under 400 words, skipping tooling-enforced lints.

2. Spec sub-agent receives:
- The diff command and commit list.
- Specification text or path.
- Instruction to report missing requirements, scope creep, and incorrect implementations with exact spec quotes under 400 words.

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

Completion criterion. Findings are rendered under distinct Standards and Spec sections with zero cross-axis reranking, each categorized by priority tier.

### Workflow integration

Align review cadence with development workflows:
- Subagent-driven development. Review after each task to catch issues before they compound.
- Executing plans. Review after each batch of tasks, apply verified fixes, and proceed.
- Ad-hoc development. Review before branch merges or whenever architectural doubts arise.

## Phase 2. Evaluating and receiving feedback

Review comments represent hypotheses to evaluate, not unilateral commands to execute. Process every piece of feedback through deliberate verification.

### Step 5. Feedback verification and pushback loop

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

### Step 6. Surgical remediation and regression pass

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
