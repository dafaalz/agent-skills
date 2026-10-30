---
name: testing-patterns
description: Use when writing automated tests, creating test fixtures, configuring test mocks or testcontainers, implementing contract tests, or refactoring test suites. Don't use for manual QA testing plans (author manual QA checklists directly), load testing scripts (author load testing scripts directly), or visual regression screenshot testing (use ui-ux-review).
---

# Testing patterns

Build deterministic, architecture-aligned test suites with clear network boundaries, isolated fixtures, and declarative assertions across frontend, backend, and browser layers.

Read the reference guides for domain-specific execution details:
* For frontend web interfaces, component trees, and accessibility auditing, read `references/frontend-patterns.md`.
* For backend services, containerized databases, API contracts, and property fuzzing, read `references/backend-patterns.md`.
* For browser user journeys, Playwright locators, and session reuse, read `references/e2e-patterns.md`.
* For test fixture generation, fluent builders, and tenant isolation, read `references/test-data-builders.md`.
* For seam boundary and mock isolation pitfalls, read `references/tdd-anti-patterns.md`.
* For pre-commit gates, Husky setup, and lint-staged automation, read `references/pre-commit-hooks.md`.
* For boundary value analysis, equivalence partitioning, and exploratory test charters, read `references/test-matrix-and-charters.md`.

<HARD-GATE>
Write-Target Boundary. Write only to `tests/`, `spec/`, `__tests__/`, and `.agents/state/testing-patterns/`. Do not modify production source, database migrations, or CI configuration. `storageState` JSON files and captured credentials must be written to `.agents/state/testing-patterns/secrets/` and gitignored. Never modify production business logic to make a test pass.
</HARD-GATE>

## Modes

Select a testing mode before Step 1:
- Author mode (default). Write new automated test suites, contract tests, and test fixtures.
- Optimization mode. Refactor existing test suites, eliminate flaky tests, and optimize testcontainer startup latency.

## Workflow

Execute the six testing steps sequentially. Complete each verification criterion before proceeding to the next step.

### Step 1. Red-green loop and seam selection

Apply test-driven development through vertical slices at confirmed seam boundaries:

1. Identify candidate public seams:
   * Inspect the caller contract or public interface specification.
   * Target public methods, API endpoints, or top-level component boundaries. Avoid reaching into private collaborators or internal state.
   * Consult `references/tdd-anti-patterns.md` for seam boundary and mock isolation pitfalls.
2. Execute the Red-green loop per vertical slice:
   * Red. Write a minimal failing test that observes behavior at the public seam. Run the test to confirm it fails cleanly from missing behavior rather than syntax or setup errors.
   * Green. Write minimal production code to pass the test without premature optimization, unused configurability, or speculative abstractions. Run the test suite to confirm clean passes.
   * Refactor. Clean up structure, remove duplication, and improve readability only after tests pass.
   * Repeat the loop for subsequent vertical slices.

Completion criterion. Target seams map to public contracts, and every slice passes through verified red-green cycles before refactoring.

### Step 2. Scope and tier selection

Align testing scope with system topology to prevent duplicated test coverage:

1. Choose the distribution model matching target architecture:
   * Testing Trophy for web applications and client components. Concentrate coverage on integration tests and restrict unit tests to pure functions and state machines.
   * Testing Pyramid for backend monoliths with rich domain rules. Anchor the base with fast domain unit tests, intermediate service tests, and a small apex of end-to-end journeys.
   * Testing Honeycomb for microservices and event systems. Focus on service-level integration tests, Pact boundary contracts, and minimal integrated flows.
2. For browser suites, limit scope to Tier 1 business journeys whose failure blocks revenue or authentication. Delegate secondary validations, form errors, and edge layouts to component integration suites.

Completion criterion. The testing tier matches system architecture, and test scope excludes redundant coverage across tiers.

### Step 3. Test data strategy via test data builders

Construct fixtures through fluent test data builders following Google DAMP (Descriptive And Meaningful Phrases) principles:

1. Replace static JSON dumps and raw SQL scripts with fluent builders to keep test intent visible.
2. Encapsulate valid default attributes within builders. Invoking `build()` without arguments must yield a valid, persistable entity.
3. Chain override methods such as `withStatus()` or `withTier()` to declare only attributes required by the specific test.
4. Inject sequential counters or random identifiers into emails, primary keys, and tenant identifiers to maintain test isolation during parallel execution.

Completion criterion. `.agents/state/testing-patterns/fixture-strategy.md` exists on disk and records the chosen fixture authoring pattern for the primary language. `grep -rn "INSERT INTO\|JSON.parse.*\.json" tests/ --include='*.test.*' --include='*.spec.*'` returns zero matches in test file bodies. Matches inside shared fixture setup files listed in the state artifact are permitted.

### Step 4. Network and dependency isolation

Isolate network boundaries and infrastructure dependencies through environment-native interception:

1. For frontend component and integration tests:
   * Intercept HTTP requests at the transport boundary using Mock Service Worker (MSW v2) instead of monkey-patching `global.fetch` or Axios instances.
   * Configure lifecycle hooks to start MSW before tests, reset handlers after every test, and close the server on teardown.
   * Set MSW to throw errors on unhandled requests to detect missing mock endpoints.
2. For backend persistence tests:
   * Run real database instances in ephemeral containers using Testcontainers instead of in-memory SQL emulators like SQLite or H2.
   * On Linux hosts, mount database storage onto `tmpfs` to eliminate disk write latency. On macOS Darwin, do not attempt to mount `tmpfs`; the host kernel has no tmpfs. When Docker Desktop or Colima runs Linux containers, the container's own `/dev/shm` is already tmpfs-backed by the Linux VM, so container-internal tmpfs works without host-side mount. Record the resolved filesystem type in `.agents/state/testing-patterns/tmpfs-status.txt` with one of `container-tmpfs`, `host-tmpfs`, or `disk-fallback`.
   * Share a singleton container instance across test files and truncate tables with cascading resets between tests.
3. For distributed microservice boundaries:
   * Verify schema agreements using consumer-driven contracts with Pact instead of running live downstream services.

Completion criterion. Network calls intercept cleanly through MSW. Backend persistence tests execute against containerized databases. If `.agents/state/testing-patterns/tmpfs-status.txt` contains `container-tmpfs` or `host-tmpfs`, the databases are mounted on tmpfs. If it contains `disk-fallback`, the completion criterion is satisfied without tmpfs and the file records why tmpfs was unavailable.

### Step 5. Declarative assertion construction

Construct assertions that evaluate public observable behavior and accessibility trees instead of internal implementation details:

1. Test components and services as black boxes:
   * Assert on observable DOM output, HTTP responses, and database state instead of internal state variables or private methods.
   * Reserve call count verification strictly for external side-effect boundaries like payment gateways or email dispatchers.
2. Locate user interface elements through the accessibility tree:
   * Query elements in the priority order of `getByRole`, `getByLabelText`, `getByPlaceholderText`, and `getByText`.
   * Locate elements through semantic role and label queries; use `getByTestId` only as a fallback for non-semantic controls, and never query by CSS classes, HTML tags, or XPath selectors.
3. Use web-first assertions for asynchronous interfaces:
   * Assert with auto-waiting matchers like `expect(locator).toBeVisible()` or `expect(locator).toHaveText()` that poll the DOM until conditions settle.
   * Pair element checks with auto-waiting assertions; never execute immediate assertions against static snapshots.

Completion criterion. Assertions verify only public behavior, accessible roles, or persisted state without inspecting internal implementation mechanics.

### Step 6. Speed and determinism verification

Verify test execution speed, determinism, and absence of intermittent failures:

1. Meet latency budgets:
   * Meet latency budgets recorded in the test tier's configuration file (such as `jest.config.js`, `vitest.config.ts`, `phpunit.xml`, or `pytest.ini`). If a project has no configured budget, record the observed per-tier median in `.agents/state/testing-patterns/latency-baseline.txt` and judge only regressions against the recorded baseline.
   * Integration tests complete within sub-second durations per test case using connection reuse. Tmpfs mounting improves latency but is not required for the sub-second budget on a warm container runtime. Record the observed p50 per test in `.agents/state/testing-patterns/latency-baseline.txt` and treat that as the baseline.
   * Browser end-to-end journeys complete within 10 to 30 seconds per journey.
2. Eliminate flakiness sources:
   * Replace arbitrary sleep calls like `sleep()` or `waitForTimeout()` with explicit assertions on visible UI states or resolved network promises.
   * Replace `page.waitForLoadState('networkidle')` with explicit element locators or backend response listeners.
   * Inject pre-authenticated `storageState` JSON files into browser contexts instead of executing repetitive UI logins.
3. Execute the full test suite three consecutive times across multiple worker processes without failures.

Completion criterion. The suite passes three consecutive parallel test runs with zero arbitrary sleeps and within established latency budgets.

## Boundary isolation

Confine testing operations strictly to test suites (`tests/`, `spec/`), fixtures, and mock definitions. Never modify production business logic or loosen database constraints to force tests to pass.

## Quick audit checklist

Audit test implementations against this table before finalizing:

| Check | Passing condition |
|---|---|
| Public interface assertions | Assert on public interfaces, observable DOM, and return values, never private implementation details |
| Deterministic waiting | Use web-first auto-waiting assertions on visible elements, never arbitrary sleeps such as `sleep()` or `waitForTimeout()` |
| Selector resilience | Query accessible roles (`getByRole`) and explicit labels, never brittle CSS class or XPath queries |
| Database isolation | Run containerized databases on tmpfs mounts with table resets, never shared flaky state |
| Network boundary mocking | Intercept network transport boundaries cleanly with MSW v2, never direct fetch monkey patches |
| Coverage distribution | Choose the distribution model that matches the target architecture instead of duplicating coverage across tiers |
