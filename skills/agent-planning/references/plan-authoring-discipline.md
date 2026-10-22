# Plan Authoring Discipline: Empirical Invariants

This reference specifies the 10 binding rules for authoring multi-task execution plans, verification commands, and audit-ready reports.

## Rule 1: Never Predict, Always Execute
- If a command can be executed, execute it and paste the raw stdout verbatim. Never hand-sum, extrapolate, or estimate numbers.
- If a command cannot be executed, label the assertion explicitly: `projected: X (unverified)`. Never use `actual:`.
- Aggregate claims require immediate itemized evidence. "50 links" requires the 50 lines with line numbers. "100% accuracy" requires the full prompt score matrix.

```bash
# BAD
"The file has 4506 lines."

# GOOD
$ wc -l file.md
4687 file.md
```

## Rule 2: Enumerate Before Counting
- Any claim of N items must be preceded by the N-item command output (`ls`, `grep`, `find`).
- Never summarize lists ahead of execution. The list establishes the count, not the narrative.

```bash
# BAD
"24 phantom router files identified."

# GOOD
$ ls skills/*/references/*.md | wc -l
33
$ grep -c "references/" SKILL.md
12
```

## Rule 3: Ground-Truth Boundary Asserts
- Slicing files requires inspecting boundaries first: run `sed -n '${START}p'` and `sed -n '${END}p'`.
- Every slice assert must verify both the starting line (`assert slice[0] == ...`) and ending line (`assert slice[-1] == ...`).

```python
# BAD
assert len(slice_resp) == 160  # unverified boundary content

# GOOD
assert slice_resp[0] == "### Fluid Grid Patterns\n"
assert slice_resp[-1].startswith("container queries")
```

## Rule 4: Systemic Fix Propagation
- When fixing an instance of defect pattern B, grep the entire codebase for all sibling instances of B.
- Resolve all instances in a single pass or explicitly declare an itemized deferral with task assignments.

## Rule 5: Sealed State Immutability
- A sealed task cannot be modified silently. Any modification requires an amendment protocol:
  1. `git diff` showing the exact delta.
  2. Commit message prefixed with `amend(taskN):`.
  3. Coverage matrix status updated to `*+rewritten` with an itemized rationale.

## Rule 6: Executable Simulation
- Dry-runs must execute real paths or provide cryptographic/diff proof: `diff -rq <temp_dir> <real_dir>`.
- Any synthetic or mocked environment must be labeled as synthetic.

## Rule 7: Numerical Ambiguity Definitions
- Gates cannot rely on self-reported model confidence. Hard gates require discrete metrics (e.g., ensemble vote splits).
- Soft confidence indicators must be explicitly identified as uncalibrated diagnostic signals.

## Rule 8: Throughput Before Intelligence
- Model selection requires computing rate limits (TPM, TPD, RPD) against the total workload token budget before choosing a model.
- Capability without capacity is an automatic failure.

```
Workload: 150 calls × 790 tokens = 118,500 tokens.
- Model A: 100K TPD quota -> REJECTED (exceeds quota).
- Model B: 200K TPD quota -> APPROVED (fits budget).
```

## Rule 9: Scope Preservation
- When re-verifying a previously audited surface, re-execute the exact scope established in Task 0 rather than creating ad-hoc partial scans.

## Rule 10: Positive Pattern Preservation
- Preserve empirical disclosure: if a verification test reveals a contradiction, report the contradictory reality immediately rather than forcing the expected narrative.
