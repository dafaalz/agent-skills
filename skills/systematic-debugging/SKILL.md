---
name: systematic-debugging
description: Debug any bug, test failure, unexpected behavior, or performance issue before proposing fixes
---

# Systematic debugging

Find the root cause before attempting fixes. Symptom fixes create new bugs and mask underlying flaws.

<HARD-GATE>
Do not write code, edit files, or propose fixes until Phase 1 investigation is complete. Every technical issue requires an identified root cause before implementation.
</HARD-GATE>

## When to use

Use this workflow for any technical fault:
- Test failures and regressions
- Production bugs and runtime crashes
- Unexpected behavior or corrupted state
- Performance bottlenecks
- Build failures and configuration faults

Apply this process especially when you feel pressure to apply a fast fix, when a previous fix failed, or when you have already attempted two or more changes.

## The four phases

Complete each phase in order before moving to the next.

### Phase 1. Root cause investigation

Gather evidence to explain what failed and why before touching production code.

1. **Error inspection.** Read stack traces, error messages, and logs in full. Identify line numbers, file paths, and error codes without skipping warnings.
   - Completion criterion: Exact error text, file path, failing line number, and initial call site identified in notes.

2. **Reproduction.** Execute the minimal command, script, or test case that triggers the defect deterministically.
   - Completion criterion: A single command or test triggers the failure consistently across consecutive runs.

3. **Change audit.** Inspect git history and environment changes. Run `git diff` against the last known working commit. Check recent dependency updates and configuration changes.
   - Completion criterion: List of modified files, dependencies, and settings mapped against the failure symptom.

4. **Boundary instrumentation.** If the fault spans multiple layers or services such as CI workflows, build scripts, API services, or databases, add diagnostic logging at each boundary. Log inputs, outputs, and environment variables across each boundary before running again.
   - Completion criterion: Diagnostic output isolates the exact boundary where expected state diverges.

5. **Upstream data flow tracing.** If the error originates deep in the call stack, trace bad values backward to their origin. Consult `root-cause-tracing.md` in this directory for backward tracing instructions.
   - Completion criterion: Code location that produced the initial invalid value identified.

Phase 1 exit criterion: You have identified the exact line of code, bad input, or environmental discrepancy causing the defect.

### Phase 2. Pattern analysis

Analyze the mechanism before designing a fix.

1. **Reference comparison.** Locate similar working code in the same repository or official documentation. Read the reference implementation completely.
   - Completion criterion: Working reference implementation identified and reviewed.

2. **Difference inventory.** Compare the working reference against the failing code line by line. Note differences in arguments, types, lifecycle timing, environment dependencies, and caller assumptions.
   - Completion criterion: Documented list of differences between working and broken components with zero unverified assumptions.

Phase 2 exit criterion: Structural and contextual differences between broken code and working code documented.

### Phase 3. Hypothesis and testing

Test assumptions with isolated probes.

1. **Falsifiable hypothesis.** Write a single hypothesis specifying the cause and the expected outcome. Format as: "The failure occurs because [cause], and changing [variable] will [outcome]."
   - Completion criterion: Written hypothesis documented in working notes.

2. **Targeted probe.** Make the smallest possible change to confirm or refute the hypothesis. Change one variable at a time. Do not apply a complete fix during this step.
   - Completion criterion: Test or probe execution confirms or refutes the hypothesis. If refuted, return to Phase 1 with the new data.

Phase 3 exit criterion: Root cause hypothesis confirmed by probe results.

### Phase 4. Implementation and verification

Apply the targeted fix at the source.

1. **Failing regression test.** Write the simplest reproducible automated test case that exposes the root cause before changing implementation code. If testing frameworks are unavailable, create a standalone test script. Follow the `test-driven-development` skill.
   - Completion criterion: Automated test fails with the expected error against unfixed code.

2. **Single root cause fix.** Modify the code at the identified source. Keep the change minimal. Do not bundle refactoring, cleanup, or unrelated edits into the fix.
   - Completion criterion: Code edit confined strictly to the root cause.

3. **Verification.** Run the reproduction test and the broader test suite to confirm the fix works without regressions. Follow the `verification-before-completion` skill.
   - Completion criterion: New test passes, all existing tests pass, and diagnostic logs confirm clean execution.

4. **Failure loop limit.**
   - If fix 1 or fix 2 fails, return to Phase 1 to re-evaluate evidence.
   - If 3 fixes fail consecutively, stop immediately. Do not attempt a fourth fix. Question the architecture.

Phase 4 exit criterion: Automated test passes, full test suite passes, and root cause is resolved at the source.

## Escalation for repeated failures

Three consecutive failed fixes signal an architectural flaw rather than a localized bug. Signs of architectural flaws include:
- Each fix introduces a new bug in a different component.
- The fix requires broad refactoring across multiple files.
- The fix requires complex workarounds to bypass existing abstractions.

When you reach 3 failed fixes:
1. Halt all code modifications.
2. Revert failed attempts to restore a clean state.
3. Document the 3 failed approaches and the architectural conflict they revealed.
4. Stop and ask the human partner to discuss redesigning the module boundary or data model.

## Diagnostic instrumentation

When debugging multi-component systems, log state at each component boundary before proposing changes:

```bash
# Boundary 1: Workflow environment
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Boundary 2: Build environment
env | grep IDENTITY || echo "IDENTITY not in environment"

# Boundary 3: Keychain access
security list-keychains
security find-identity -v

# Boundary 4: Signing invocation
codesign --sign "$IDENTITY" --verbose=4 "$APP"
```

This instrumentation identifies the exact layer where data or environment variables fail to propagate.

## Disclosed reference

Consult these files in this directory for specialized debugging techniques:
- `root-cause-tracing.md` for backward tracing through call stacks.
- `defense-in-depth.md` for adding multi-layer validation after fixing root causes.
- `condition-based-waiting.md` for replacing arbitrary sleeps with condition polling.

Related skills to invoke during debugging:
- `test-driven-development` for writing red regression tests before fixing code.
- `verification-before-completion` for verifying fixes before claiming resolution.
