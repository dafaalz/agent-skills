---
name: tdd
description: Use when building features or fixing bugs test-first via red-green cycles and vertical slices.
---

# Test-driven development

Execute the red-to-green loop. Every cycle builds one vertical slice at a confirmed seam.

<HARD-GATE>
Do not write production code without a failing test first. If production code was written before the test, delete it and restart from a failing test.
</HARD-GATE>

## Seam selection

A seam is the public boundary of a component. Tests observe behavior at this boundary without reaching into internals.

1. Inspect the caller contract or interface specification.
2. Identify candidate public methods, endpoints, or function boundaries.
3. Confirm the target seam with the user if the boundary is ambiguous.

Completion criterion. Target seam matches the public contract.

## The loop

Work one vertical slice at a time. Each slice pairs one behavior test with its minimal implementation.

1. **Red.** Write one minimal test for the target behavior. Run the test suite. Confirm the test fails because the feature is missing, not due to syntax or test configuration errors.
   Completion criterion. Test runner reports a clean failure matching the expected assertion.

2. **Green.** Write only the minimal production code needed to make the test pass. Run the test suite. Confirm all tests pass.
   Completion criterion. Test runner reports zero failures and clean test output.

3. **Repeat.** Proceed to the next slice or seam.

Refactor only after all slices pass. Keep refactoring separate from this loop.

## Test quality rules

Follow three core testing rules:
- Assert against known independent values, never formulas copied from production logic.
- Test only observable output at the public seam. Never inspect private properties or internal state.
- Invoke the component using the exact caller path used by production code.

## Disclosed reference

Consult `references/anti-patterns.md` only if the seam boundary, assertion strategy, or mock isolation requirements are unclear. Do not load this file during normal execution.
