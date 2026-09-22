# End-to-end and user journey testing standards

Architectural standards for end-to-end user journeys, resilient locators, web-first synchronization, and authentication session reuse.

## 1. Tier 1 user journey scope

End-to-end (E2E) testing validates that integrated software systems function correctly across the browser runtime, network layers, backend services, and persistent databases. Maintaining a fast, dependable test suite requires strict boundaries regarding what belongs in the E2E tier.

Attempting to test every input permutation, edge condition, or form validation through a real browser creates an ice cream cone anti-pattern. This produces slow execution times and high test maintenance overhead.

### Three-tier scoping matrix
Teams classify testing scenarios into three distinct operational tiers:

1. Tier 1 (Mandatory E2E journeys). Critical business paths whose failure halts revenue generation, blocks user access, or prevents core product value delivery:
   * User account registration and activation.
   * Authentication and persistent session recovery.
   * Core checkout and payment processing workflows.
   * Primary content creation and persistent saving.
   * Team onboarding and workspace invitation acceptance.
2. Tier 2 (Integration and component testing scope). Form validation permutations, error banner styling, modal open and close states, responsive mobile drawer navigation, and complex UI state machines. Validate these paths using component testing frameworks or integration suites.
3. Tier 3 (Unit testing scope). Currency formatters, date mathematics, schema serialization, calculation logic, and utility functions.

## 2. Accessibility tree locators vs brittle selectors

Tests must discover elements in the same manner that end users and assistive technologies interact with them. Binding locators to HTML tags, CSS selectors, or XPath expressions produces fragile tests that break when styling classes or structural containers change.

### Locator priority hierarchy
Select elements using Playwright locator methods in order of resilience:

1. `page.getByRole(role, options)`. Locates elements through the browser accessibility tree. Validates semantic HTML attributes, ARIA roles, and accessible names.
2. `page.getByLabel(text)`. Locates form inputs by their associated label text.
3. `page.getByPlaceholder(text)`. Locates inputs by visible placeholder attributes when labels are omitted.
4. `page.getByText(text)`. Locates non-interactive textual elements such as status banners or headings.
5. `page.getByTestId(id)`. Last resort fallback for non-semantic interactive canvas components or complex custom graphical controls.

### Selectors comparison
The following examples show the difference between fragile selectors and resilient accessibility-based locators:

```typescript
// Fragile selector anti-pattern vulnerable to layout refactors
await page.locator('div.container > form > div:nth-child(3) > button.btn-primary').click();
await page.locator('//input[@id="user_email_input"]').fill('alex@example.internal');

// Resilient pattern querying accessibility tree semantics
await page.getByRole('textbox', { name: 'Email address' }).fill('alex@example.internal');
await page.getByRole('button', { name: 'Complete checkout' }).click();
```

## 3. Web-first assertions and synchronization rules

Legacy test frameworks evaluated assertions instantaneously against the active DOM snapshot. If asynchronous rendering or network responses were still settling, assertions failed prematurely.

Modern test suites use web-first assertions that automatically poll the DOM with exponential micro-backoffs until conditions evaluate to true or the assertion timeout expires.

### Web-first assertion patterns
Always assert conditions using asynchronous web-first matchers:

```typescript
// Fragile instantaneous check vulnerable to race conditions
const heading = await page.locator('h1').innerText();
expect(heading).toBe('Billing Settings');

// Resilient web-first pattern with automatic polling and retry
await expect(page.getByRole('heading', { level: 1 })).toHaveText('Billing Settings');
await expect(page.getByRole('button', { name: 'Save Changes' })).toBeEnabled();
await expect(page.getByTestId('subscription-badge')).toBeVisible();
await expect(page.getByRole('listitem')).toHaveCount(5);
```

### Prohibition of networkidle
Using `page.waitForLoadState('networkidle')` is an anti-pattern discouraged in modern production suites.

Modern web applications continuously transmit network traffic for background telemetry, WebSocket pings, periodic notification polling, and analytics trackers. A 500 millisecond window of complete network silence may never occur, resulting in spurious 30-second test timeouts. Conversely, on slow connections, an arbitrary quiet window may fire before dynamic script bundles finish downloading.

Replace `networkidle` with explicit synchronization:

```typescript
// Discouraged pattern prone to flakiness
await page.goto('/projects');
await page.waitForLoadState('networkidle');

// Standard pattern waiting for observable domain UI state
await page.goto('/projects');
await expect(page.getByRole('heading', { name: 'Active Projects' })).toBeVisible();

// Explicit backend response synchronization pattern
const createProjectResponse = page.waitForResponse(
  (response) => response.url().includes('/api/v1/projects') && response.status() === 201
);
await page.getByRole('button', { name: 'Confirm Project' }).click();
await createProjectResponse;
```

### Prohibition of arbitrary timeouts
Calling `page.waitForTimeout(3000)`, `sleep(3)`, or `setTimeout` is prohibited in automated test suites.

Arbitrary timeouts introduce two critical failure modes:
1. Pipeline drag. If an operation completes in 100 milliseconds, an arbitrary 3-second sleep wastes 2.9 seconds. Across hundreds of tests, build times expand from minutes to hours.
2. Contention failures. A duration that passes reliably on a developer laptop often fails under high CPU load on shared continuous integration runners.

Rely exclusively on auto-waiting actions (`click`, `fill`, `check`) and retriable web-first assertions (`expect(locator).toBeVisible()`).

## 4. Authentication session reuse via storageState

Authenticating through the web user interface before every single test case introduces significant execution delay and increases flakiness.

The recommended pattern performs authentication once during a global setup routine, saves the resulting storage state (cookies, local storage keys, authorization tokens) to a JSON file on disk, and injects that state into worker browser contexts.

### Playwright configuration with storage state
The following configuration registers an authentication setup project and passes the stored session to worker projects:

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  projects: [
    {
      name: 'setup-auth',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'authenticated-e2e',
      dependencies: ['setup-auth'],
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user-session.json',
      },
    },
    {
      name: 'public-flows',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
  ],
});
```

### Global authentication setup script
The following setup script authenticates through a backend API endpoint, populates browser storage, and exports the session snapshot:

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const authFile = path.resolve(process.cwd(), '.auth/user-session.json');

setup('authenticate user via API and preserve session tokens', async ({ request, page }) => {
  const authDir = path.dirname(authFile);
  if (!fs.existsSync(authDir)) {
    fs.mkdirSync(authDir, { recursive: true });
  }

  const response = await request.post('https://api.example.internal/v1/auth/login', {
    data: {
      username: 'automated-tester@example.internal',
      password: process.env.E2E_USER_PASSWORD || 'SecretPassword123!',
    },
  });
  expect(response.ok()).toBeTruthy();
  const credentials = await response.json();

  await page.goto('/blank.html');
  await page.evaluate((token) => {
    window.localStorage.setItem('auth_token', token);
    window.localStorage.setItem('auth_expiry', String(Date.now() + 86400000));
  }, credentials.accessToken);

  await page.context().storageState({ path: authFile });
});
```

Worker tests under the `authenticated-e2e` project start immediately inside an authenticated session, navigating directly to protected routes without repeating login interactions.
