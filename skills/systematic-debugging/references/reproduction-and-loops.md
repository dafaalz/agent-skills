# Fast feedback loops and reproduction protocols

Techniques to build deterministic verification loops and minimize reproduction cases before attempting fixes.

## 1. Ten fast feedback loop patterns

Choose the fastest deterministic harness available for the bug domain:

1. **Failing automated test.** Write a minimal test asserting the expected behavior. This is the gold standard for unit logic, query contracts, and data transforms.
2. **Curl or HTTP script.** Store a reproduction command in a throwaway script with exact headers, payload, and auth tokens.
3. **Snapshot diffing.** Capture before and after state snapshots (database rows, JSON responses, AST trees) and pipe to a diff tool.
4. **Headless browser trace.** Use Playwright or Puppeteer with video or trace recording to replicate frontend interaction regressions deterministically.
5. **Network trace replay.** Export a HAR file or recorded HTTP mock to isolate client regressions from backend volatility.
6. **Throwaway harness.** Create a standalone script in a scratch directory importing only the affected module with hardcoded input.
7. **Property test loop.** Run rapid fuzzing or generative inputs over boundary edge cases to trap off-by-one errors and integer overflow.
8. **Automated git bisect.** Run `git bisect run <test-command>` across historical commits to isolate the exact commit introducing the defect.
9. **Differential loop.** Run the new implementation alongside the known working legacy implementation on identical inputs and assert parity.
10. **Human in the loop script.** For hardware, terminal TTY, or interactive shell bugs, provide a deterministic one-line runner with clear pass and fail markers.

## 2. Tightening feedback loops

Treat the reproduction loop as an internal product. Tighten it using three rules:

1. **Speed.** Keep the feedback loop under 5 seconds. Skip unrelated startup, cache fixtures, and narrow test filters.
2. **Signal sharpness.** Assert the specific bug symptom rather than generic process termination or non-zero exit codes.
3. **Determinism.** Freeze time, seed pseudorandom number generators, isolate filesystem directories, and mock volatile external endpoints.

For non-deterministic bugs, aim to increase reproduction rate instead of demanding immediate determinism. Loop the trigger 100 times, run concurrent workers, narrow timing windows, or add short sleeps. Raise the reproduction rate above 50 percent so hypotheses are testable.

## 3. Reproduction minimization

Never debug against full production payloads. Minimize reproduction cases following these rules:

1. **Load-bearing isolation.** Prune inputs, callers, and configuration keys one by one. The reproduction scenario is minimal only when every remaining element is load-bearing, where removing any single remaining element makes the loop pass.
2. **Eliminate indirect dependencies.** Mock external API gateways, caching layers, and asynchronous queue workers.
3. **Isolate state.** Verify whether the fault requires accumulated state or reproduces on a clean process restart.
4. **Pin deterministic seeds.** Freeze pseudorandom number generators, clock timestamps, and database sequence identifiers during the run.

## 4. Secret and credential redaction protocol

Protect secrets during diagnostic logging and terminal outputs:

1. **Mask environment dumps.** Never execute raw `env` or `cat .env` commands. Inspect variables by checking presence:
   ```bash
   grep -sq "^API_KEY=" .env && echo "API_KEY present" || echo "API_KEY missing"
   ```
2. **Sanitize terminal traces.** Before printing error responses or headers to logs, replace sensitive values with `<REDACTED>`:
   - Authorization bearer tokens and basic auth strings
   - Private keys, PEM blocks, and API tokens
   - Passwords and database connection strings
   - Personally identifiable customer data

## 5. Performance regression diagnostics

For performance regressions, avoid arbitrary log statements:

1. **Establish baseline measurements.** Build a dedicated timing harness using profilers, runtime timestamps, or database query execution plans.
2. **Bisect against baseline.** Measure the latency delta between known-good and degraded commits under identical workloads.
3. **Measure first, modify second.** Never commit code changes without verifying a measured latency reduction against the baseline.

## 6. Falsifiable hypotheses and tagged instrumentation

When the root cause remains non-obvious after reproduction:

1. **Ranked hypothesis formulation.** Formulate 3 to 5 distinct hypotheses ranked by likelihood before testing any of them. Single hypothesis generation anchors on the first plausible explanation.
2. **Explicit prediction format.** Format each hypothesis as "If [cause] is the root issue, changing [variable] will [outcome]."
3. **Tagged instrumentation.** Tag every temporary diagnostic log with a unique session prefix like `[DEBUG-probe1]`. Verify all tags are removed via grep before completing Phase 4.
