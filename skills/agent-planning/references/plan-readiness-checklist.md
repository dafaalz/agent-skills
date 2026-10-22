# Plan Readiness Checklist

This checklist defines mandatory quality gates that an agent must verify before submitting execution plans or task completion reports for audit review.

## 1. Empirical Verification Gate
- [ ] Every command output cited was executed in the active session and pasted verbatim from raw stdout.
- [ ] No placeholder counts, hand-summed totals, or extrapolated metrics appear in the report.
- [ ] Every Python file slice has verified line assertions on both first (`[0]`) and last (`[-1]`) elements.
- [ ] File and directory lists reflect physical `ls` output, not mental or design taxonomies.
- [ ] Any test output claiming `EXIT_CODE: 0` is preceded by an executable command block.

## 2. Invariant & Boundary Gate
- [ ] User working files (WIP) verified untouched and pristine with `git status --porcelain`.
- [ ] Any modification to a previously sealed task includes an amendment commit and coverage matrix update.
- [ ] Sibling dependencies checked across the entire repository to prevent unbudgeted scope creep.
- [ ] Deletion operations simulated first (e.g., via temporary move and smoke test) before execution.

## 3. Capacity & Quota Gate
- [ ] API token and request requirements calculated against published provider quotas (TPM, TPD, RPD).
- [ ] Timeouts, pacing delays, and completion token caps explicitly tuned to prevent payload truncation.
- [ ] Model endpoint existence confirmed with standalone probe before launching full batch suites.

## 4. Adversarial Review Self-Check
- [ ] If an auditor independently runs every command in my report, will their terminal match my output byte-for-byte?
- [ ] Have I enumerated all instances of the pattern being addressed, rather than just the single blocker cited?
- [ ] Are all negative results or margin variances disclosed transparently rather than smoothed over?
