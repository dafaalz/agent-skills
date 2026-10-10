---
name: systematic-debugging
description: Use when debugging any bug, test failure, unexpected behavior, or performance issue before proposing fixes. Don't use for feature additions, code generation, or routine refactoring.
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
   - Completion criterion. Exact error text, file path, failing line number, and initial call site identified in notes.

2. **Reproduction and feedback loop.** Build a tight, red-capable command that triggers the failure before reading source code to form theories.
   - Assert the user's exact symptom rather than an unrelated crash.
   - Keep the loop fast, deterministic, and runnable unattended.
   - For non-deterministic bugs, raise the reproduction rate instead of giving up. Loop the trigger 100 times, add concurrency stress, narrow timing windows, or inject sleeps until reproducible above 50 percent.
   - Minimize the repro by pruning inputs, callers, and state one by one. The repro is minimal when every remaining element is load-bearing, where removing any single element turns the loop green.
   - If an automated loop cannot be built, stop immediately. Ask the user for environment access, redacted trace logs, or permission for temporary production probes. Do not guess without a loop.
   - Consult `references/reproduction-and-loops.md` for test runner patterns, minimization, and credential redaction.
   - Completion criterion. One verified command executed and confirmed red against the user symptom across consecutive runs, or an explicit escalation blocker sent to the user.

3. **Change audit.** Inspect git history and environment changes. Run `git diff` against the last known working commit. Check recent dependency updates and configuration changes.
   - Completion criterion. List of modified files, dependencies, and settings mapped against the failure symptom.

4. **Boundary instrumentation.** If the fault spans multiple layers or services such as CI workflows, build scripts, API services, or databases, add diagnostic logging at each boundary. Log inputs, outputs, and environment variables across each boundary before running again.
   - Completion criterion. Diagnostic output isolates the exact boundary where expected state diverges.

5. **Upstream data flow tracing.** If the error originates deep in the call stack, trace bad values backward to their origin. Consult `references/root-cause-tracing.md` for backward tracing instructions.
   - Completion criterion. Code location that produced the initial invalid value identified.

6. **Large-scale scope and context compaction defense.** If the investigation requires surveying massive logs, hundreds of database files, or multi-repository history:
   - Dispatch a dedicated `research` or `self` subagent via `invoke_subagent` to isolate heavy tool outputs and prevent context window compaction in the primary agent session.
   - Persist intermediate findings directly to disk artifacts (`<appDataDir>/brain/<conversation-id>/` or `scratch/`) instead of relying solely on chat memory.
   - Completion criterion. Heavy data collection delegated to a subagent and key synthesis written to a disk artifact.

Phase 1 exit criterion. The exact line of code, bad input, or environmental discrepancy causing the defect is identified.

### Phase 2. Pattern analysis

Analyze the mechanism before designing a fix.

1. **Reference comparison.** Locate similar working code in the same repository or official documentation. Read the reference implementation completely.
   - Completion criterion. Working reference implementation identified and reviewed.

2. **Difference inventory.** Compare the working reference against the failing code line by line. Note differences in arguments, types, lifecycle timing, environment dependencies, and caller assumptions.
   - Completion criterion. Documented list of differences between working and broken components with zero unverified assumptions.

Phase 2 exit criterion. Structural and contextual differences between broken code and working code are documented.

### Phase 3. Hypothesis and testing

Test assumptions with isolated probes.

1. **Ranked falsifiable hypotheses.** Formulate 3 to 5 distinct hypotheses ranked by likelihood before testing any of them. Single hypothesis generation anchors on the first plausible idea and wastes investigation time.
   - Format each hypothesis as an explicit prediction like "If [cause] is the root issue, changing [variable] will [outcome]."
   - Share the ranked list with the user as a rapid checkpoint. Proceed with testing if the user is away.
   - Completion criterion. List of 3 to 5 ranked falsifiable predictions recorded in working notes and presented to the user.

2. **Targeted probes and instrumentation.** Test hypotheses one variable at a time using the smallest possible probe.
   - Prefer breakpoints or REPL inspection when the runtime allows.
   - Tag every temporary log statement with a unique identifier like `[DEBUG-probe1]`. This makes teardown a single grep command.
   - For performance regressions, establish a baseline measurement with a benchmark script, profiler, or query plan before bisecting. Measure before modifying code.
   - Completion criterion. Probe results confirm or disprove the lead hypothesis without touching unrelated code. If refuted, test the next ranked hypothesis.

Phase 3 exit criterion. A single root cause hypothesis confirmed by probe data.

### Phase 4. Implementation and verification

Apply the targeted fix at the source.

1. **Failing regression test and seam audit.** Write an automated test reproducing the root cause before changing implementation code.
   - Verify the test exercises the genuine call site seam. If available test seams are too shallow and provide false confidence, document the architectural seam limitation as an explicit finding.
   - Follow the `test-driven-development` skill.
   - Completion criterion. Automated regression test fails against unfixed code at a verified architectural seam, or seam limitation is documented.

2. **Surgical root cause fix.** Modify code strictly at the identified root cause.
   - Touch only what must be changed to fix the defect. Match existing indentation and conventions.
   - Never reformat, "improve", or refactor adjacent unbroken code or comments.
   - Do not delete pre-existing dead code unless explicitly requested.
   - Clean up only orphan variables, imports, or functions created by the fix.
   - Completion criterion. Code edit confined strictly to the root cause with zero unrelated diff lines.

3. **Verification and cleanup pass.** Validate the fix and purge temporary instrumentation. Follow the `verification-before-completion` skill.
   - Re-run the Phase 1 reproduction loop against the original un-minimised scenario to confirm it passes.
   - Verify all regression tests and suite tests pass.
   - Run grep for the debug tag prefix to remove every temporary probe.
   - Remove throwaway test scripts from scratch storage.
   - Record the confirmed root cause hypothesis in the commit message for future maintainers.
   - Completion criterion. Regression and suite tests pass, original repro is verified green, and grep confirms zero remaining debug tags.

4. **Failure loop limit.**
   - If fix 1 or fix 2 fails, return to Phase 1 to re-evaluate evidence.
   - If 3 fixes fail consecutively, stop immediately. Do not attempt a fourth fix. Question the architecture.

Phase 4 exit criterion. Automated tests pass, original repro passes, debug tags are purged, and the root cause fix is verified without regressions.

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

Consult these files in `references/` for specialized debugging techniques:
- `references/root-cause-tracing.md` for backward tracing through call stacks.
- `references/defense-in-depth.md` for adding multi-layer validation after fixing root causes.
- `references/condition-based-waiting.md` for replacing arbitrary sleeps with condition polling.

Related skills to invoke during debugging:
- `test-driven-development` for writing red regression tests before fixing code.
- `verification-before-completion` for verifying fixes before claiming resolution.
