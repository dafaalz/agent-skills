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

## 2. Reproduction minimization

Never debug against large production payloads. Minimize reproduction cases following these rules:

1. **Slice inputs by half.** Prune request bodies, arrays, and JSON objects until removing one more key stops triggering the failure.
2. **Eliminate indirect dependencies.** Mock or strip external API gateways, caching layers, and asynchronous queue workers.
3. **Isolate load bearing state.** Verify whether the fault depends on accumulated state or occurs on clean system startup.
4. **Pin deterministic seeds.** Freeze pseudo-random number generators, clock timestamps, and database sequence IDs during the test run.

## 3. Secret and credential redaction protocol

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

## 4. Falsifiable hypotheses formulation

When the root cause remains non-obvious after reproduction:

1. Formulate 3 to 5 distinct hypotheses ranked by likelihood.
2. Each hypothesis must state an explicit mechanism, a predicted symptom, and a disproving test.
3. If an experiment disproves a hypothesis, discard it completely before testing the next branch.
