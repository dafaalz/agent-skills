# Feedback evaluation and remediation protocol

Standard operating procedures for receiving, evaluating, and addressing code review feedback.

## Banned performative agreement

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
- Jump directly to running tests and showing diffs.

## Handling unclear items

Never guess intent or apply partial assumptions when review comments lack clarity.

Apply this clarification protocol:
- Stop immediately when any item in a review list is ambiguous.
- Do not implement clear items prematurely if ambiguous items may alter shared architecture; hold implementation until shared architecture is confirmed.
- State exactly which items are understood and ask targeted questions regarding the unclear items.
- Resume implementation only after requirements are fully unambiguous.

## Architectural integrity and counter-argument protocol

Protect system boundaries when suggestions violate Single Responsibility Principle, introduce tight coupling, or cause lifecycle mismatches:
- Require technical correctness and push back with concrete facts; never accept anti-patterns to avoid interpersonal friction.
- Check blast radius across modules. Verify whether the suggestion forces unrelated domains into a shared file or puts request-time logic into static initialization.
- Ground counter-arguments in external consensus. Run targeted searches using official framework documentation or industry standards before responding.
- Formulate a structured technical counter-argument. State the concrete tradeoff, cite the authoritative source, and propose a clean, decoupled alternative that satisfies the caller's true requirement.

## YAGNI verification

Reviewers frequently recommend building speculative abstraction layers, extra configuration flags, or unused data exports.

Verify necessity using this process:
1. Search the codebase for actual call sites using grep or file search tools.
2. If the feature has zero active callers, reject the abstraction and propose removing dead code instead.
3. If active callers exist, implement the minimum clean logic required to satisfy those callers without speculative generalizations.
4. Enforce the reuse hierarchy. Existing codebase helpers and standard library utilities beat writing custom wrappers or adding third-party dependencies.
5. Protect essential boundaries. Never sacrifice trust boundary validation, error handling preventing data loss, security invariants, or accessibility in the name of YAGNI.

## Handling pushback and corrections

Navigate disagreements with technical facts:
- When pushing back, reference test results, benchmark metrics, or architectural constraints rather than personal preference.
- If you pushed back and later discover the reviewer was correct, acknowledge the facts directly without lengthy apologies.
- State the verified finding plainly, such as "Verified the 10.15 backward compatibility requirement. Implementing the fallback branch now."

## Thread replies

Reply directly in the comment thread for inline GitHub pull request comments rather than submitting top-level PR comments. Keep all discussion tied to the relevant line diff.
