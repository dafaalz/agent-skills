---
name: testing-patterns
description: Use when writing automated tests, creating test fixtures, configuring test mocks or testcontainers, implementing contract tests, or refactoring test suites.
---

# Testing patterns

Build deterministic, architecture-aligned test suites with clear network boundaries, isolated fixtures, and declarative assertions across frontend, backend, and browser layers.

Read the reference guides for domain-specific execution details:
* For frontend web interfaces, component trees, and accessibility auditing, read `references/frontend-patterns.md`.
* For backend services, containerized databases, API contracts, and property fuzzing, read `references/backend-patterns.md`.
* For browser user journeys, Playwright locators, and session reuse, read `references/e2e-patterns.md`.
* For test fixture generation, fluent builders, and tenant isolation, read `references/test-data-builders.md`.

## Workflow

Execute the five testing steps sequentially. Complete each verification criterion before proceeding to the next step.

### Step 1. Scope and tier selection

Align testing scope with system topology to prevent duplicated test coverage:

1. Choose the distribution model matching target architecture:
   * Testing Trophy for web applications and client components. Concentrate coverage on integration tests while keeping unit tests restricted to pure functions and state machines.
   * Testing Pyramid for backend monoliths with rich domain rules. Anchor the base with fast domain unit tests, intermediate service tests, and a small apex of end-to-end journeys.
   * Testing Honeycomb for microservices and event systems. Focus on service-level integration tests, Pact boundary contracts, and minimal integrated flows.
2. For browser suites, limit scope to Tier 1 business journeys whose failure blocks revenue or authentication. Delegate secondary validations, form errors, and edge layouts to component integration suites.

Completion criterion. The testing tier matches system architecture, and test scope excludes redundant coverage across tiers.

### Step 2. Test data strategy via test data builders

Construct fixtures through fluent test data builders following Google DAMP (Descriptive And Meaningful Phrases) principles:

1. Replace static JSON dumps and raw SQL scripts with fluent builders to keep test intent visible.
2. Encapsulate valid default attributes within builders. Calling `build()` without arguments must yield a valid, persistable entity.
3. Chain override methods such as `withStatus()` or `withTier()` to declare only attributes required by the specific test.
4. Inject sequential counters or random identifiers into emails, primary keys, and tenant identifiers to maintain test isolation during parallel execution.

Completion criterion. Tests construct domain fixtures through fluent builders, declaring only behavior-critical fields while running deterministically in parallel.

### Step 3. Network and dependency isolation

Isolate network boundaries and infrastructure dependencies through environment-native interception:

1. For frontend component and integration tests:
   * Intercept HTTP requests at the transport boundary using Mock Service Worker (MSW v2) instead of monkey-patching `global.fetch` or Axios instances.
   * Configure lifecycle hooks to start MSW before tests, reset handlers after every test, and close the server on teardown.
   * Set MSW to throw errors on unhandled requests to detect missing mock endpoints.
2. For backend persistence tests:
   * Run real database instances in ephemeral containers using Testcontainers instead of using in-memory SQL emulators like SQLite or H2.
   * Mount database storage directories onto in-memory filesystems (`tmpfs`) to eliminate disk write latency.
   * Share a singleton container instance across test files and truncate tables with cascading resets between tests.
3. For distributed microservice boundaries:
   * Verify schema agreements using consumer-driven contracts with Pact instead of running live downstream services.

Completion criterion. Network calls intercept cleanly through MSW, and backend persistence tests execute against containerized databases on tmpfs mounts.

### Step 4. Declarative assertion construction

Construct assertions evaluating public observable behavior and accessibility trees instead of internal implementation details:

1. Test components and services as black boxes:
   * Assert on observable DOM output, HTTP responses, and database state instead of internal state variables or private methods.
   * Reserve call count verification strictly for external side-effect boundaries like payment gateways or email dispatchers.
2. Locate user interface elements through the accessibility tree:
   * Query elements following the priority order of `getByRole`, `getByLabelText`, `getByPlaceholderText`, and `getByText`.
   * Use `getByTestId` only as a fallback for non-semantic canvas controls or complex custom graphics. Avoid querying by CSS classes, HTML tags, or XPath selectors.
3. Use web-first assertions for asynchronous interfaces:
   * Assert using auto-waiting matchers like `expect(locator).toBeVisible()` or `expect(locator).toHaveText()` that poll the DOM until conditions settle.
   * Pair element checks with auto-waiting assertions instead of executing immediate assertions against static snapshots.

Completion criterion. Assertions verify only public behavior, accessible roles, or persisted state without inspecting internal implementation mechanics.

### Step 5. Speed and determinism verification

Verify test execution speed, determinism, and absence of intermittent failures:

1. Meet latency budgets:
   * Domain unit tests complete within sub-millisecond durations per test case.
   * Integration tests complete within sub-second durations per test case using tmpfs and connection reuse.
   * Browser end-to-end journeys complete within 10 to 30 seconds per journey.
2. Eliminate flakiness sources:
   * Replace arbitrary sleep calls like `sleep()` or `waitForTimeout()` with explicit assertions on visible UI states or resolved network promises.
   * Replace `page.waitForLoadState('networkidle')` with explicit element locators or backend response listeners.
   * Inject pre-authenticated `storageState` JSON files into browser contexts instead of executing repetitive UI logins.
3. Execute the full test suite three consecutive times across multiple worker processes without failures.

Completion criterion. The suite passes three consecutive parallel test runs with zero arbitrary sleeps and within established latency budgets.
