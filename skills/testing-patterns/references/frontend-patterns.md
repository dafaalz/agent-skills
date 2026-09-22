# Frontend testing patterns and standards

Guidelines for architectural test distribution, realistic component interactions, network interception, visual regression, and accessibility verification.

## 1. Testing trophy and behavioral testing principles

Modern frontend quality assurance follows the Testing Trophy model popularized by Kent C. Dodds and Guillermo Rauch. While the classical Testing Pyramid prioritized vast volumes of solitary unit tests, web applications derive the greatest confidence from integration tests.

### Testing trophy layers
The Testing Trophy distributes testing efforts across four layers:
1. Static analysis. TypeScript, ESLint, and Biome identify syntax mistakes, type mismatches, and broken imports before execution.
2. Unit tests. Focused tests covering pure mathematical utilities, string formatters, and complex custom algorithms that contain zero DOM or network interactions.
3. Integration and component tests. The wide center of the trophy. These tests mount full component trees into a realistic DOM environment, fire realistic user events, and intercept network calls at the boundary. They provide the highest return on investment by testing how multiple units collaborate.
4. End-to-end tests. A focused set of browser tests validating critical revenue and authentication paths against real staging environments.

### Testing behavior over implementation details
Component tests must treat components as black boxes. When tests inspect internal state variables, private methods, or child component nesting, two major dysfunctions occur:
1. False positives. The test passes even when user behavior is broken. For example, an internal state variable switches to true, but an absolute CSS z-index overlay hides the submission button.
2. False negatives. The test breaks during an internal refactor even though user-facing behavior remains completely functional. For example, migrating from component local state to a shared Zustand store breaks state assertions despite the rendered interface working identically.

Locate elements through the accessibility tree in order of priority:
1. Accessible queries include `getByRole`, `getByLabelText`, `getByPlaceholderText`, `getByText`, and `getByDisplayValue`.
2. Semantic queries include `getByAltText` and `getByTitle`.
3. Test IDs using `getByTestId` serve strictly as the last resort when elements lack semantic ARIA attributes.

## 2. Component testing with user-event over fireEvent

Testing Library offers two APIs for triggering user actions, namely `fireEvent` and `@testing-library/user-event`.

### Why user-event is required
The `fireEvent` utility simply dispatches synthetic DOM events without firing the surrounding sequence of browser events. For instance, `fireEvent.click(button)` dispatches a single click event, bypassing hover states, pointer presses, focus changes, and document-level event listeners.

In contrast, `@testing-library/user-event` simulates realistic browser interactions. Calling `await user.type(searchInput, 'Bob')` focuses the input, dispatches keydown, keypress, input mutation, keyup for every character, and updates cursor selection.

### Production component test example
The following test mounts a searchable user directory component, simulates authentic keyboard input, and verifies accessible DOM updates:

```typescript
import { render, screen, waitForElementToBeRemoved } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, beforeEach } from 'vitest';
import { UserDirectory } from './UserDirectory';
import { server } from '../mocks/node';
import { http, HttpResponse } from 'msw';

describe('UserDirectory Component', () => {
  beforeEach(() => {
    server.resetHandlers();
  });

  it('renders loading indicator, displays fetched users, and filters results on user search', async () => {
    const user = userEvent.setup();

    render(<UserDirectory />);

    expect(screen.getByRole('status', { name: /loading users/i })).toBeInTheDocument();

    await waitForElementToBeRemoved(() => screen.queryByRole('status', { name: /loading users/i }));

    const userList = screen.getByRole('list', { name: /active users/i });
    expect(userList).toBeInTheDocument();
    expect(screen.getByRole('listitem', { name: /alice smith/i })).toBeInTheDocument();
    expect(screen.getByRole('listitem', { name: /bob johnson/i })).toBeInTheDocument();

    server.use(
      http.get('/api/users', ({ request }) => {
        const url = new URL(request.url);
        const query = url.searchParams.get('q');

        if (query === 'Bob') {
          return HttpResponse.json([
            { id: 'usr-2', name: 'Bob Johnson', email: 'bob@example.com', role: 'Staff Engineer' },
          ]);
        }

        return HttpResponse.json([]);
      })
    );

    const searchInput = screen.getByRole('searchbox', { name: /filter users/i });
    await user.click(searchInput);
    await user.type(searchInput, 'Bob');

    expect(await screen.findByRole('listitem', { name: /bob johnson/i })).toBeInTheDocument();
    expect(screen.queryByRole('listitem', { name: /alice smith/i })).not.toBeInTheDocument();
  });
});
```

## 3. Network mocking with Mock Service Worker (MSW v2)

Stubbing network calls through `jest.fn()`, monkey-patching `global.fetch`, or mocking Axios adapters bypasses the browser network pipeline. These artificial stubs fail to validate HTTP header formatting, request body serialization, cookie handling, and status code parsing.

Mock Service Worker (MSW v2) intercepts HTTP requests at the network layer using Service Workers in the browser and native interceptors in Node.js environments. Application code remains completely unaware that requests are intercepted.

### Handler configuration
Define reusable endpoint handlers:

```typescript
// src/mocks/handlers.ts
import { http, HttpResponse, delay } from 'msw';

export interface UserPayload {
  id: string;
  name: string;
  email: string;
  role: string;
}

export const handlers = [
  http.get('/api/users', async () => {
    await delay(20);
    return HttpResponse.json<UserPayload[]>([
      { id: 'usr-1', name: 'Alice Smith', email: 'alice@example.com', role: 'Platform Architect' },
      { id: 'usr-2', name: 'Bob Johnson', email: 'bob@example.com', role: 'Staff Engineer' },
    ]);
  }),

  http.post('/api/users', async ({ request }) => {
    const body = (await request.json()) as Omit<UserPayload, 'id'>;

    if (!body.name || !body.email) {
      return HttpResponse.json(
        { message: 'Validation failed. Name and email are required.' },
        { status: 422 }
      );
    }

    return HttpResponse.json<UserPayload>(
      { id: 'usr-new', ...body },
      { status: 201 }
    );
  }),
];
```

### Node server lifecycle setup
Initialize the MSW server and enforce strict isolation between test executions:

```typescript
// src/mocks/node.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

```typescript
// src/test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from '../mocks/node';
import '@testing-library/jest-dom/vitest';

beforeAll(() => {
  server.listen({ onUnhandledRequest: 'error' });
});

afterEach(() => {
  server.resetHandlers();
});

afterAll(() => {
  server.close();
});
```

Enforcing `onUnhandledRequest: 'error'` ensures any unhandled API call immediately triggers an error, catching missing handlers or unintentional external network calls.

## 4. Playwright visual snapshot stabilization

Pixel visual regression testing catches CSS regressions, alignment faults, and layout shifts. Without careful configuration, visual tests produce false failures caused by font antialiasing differences, running CSS animations, and dynamic timestamp values.

Stabilize visual snapshots by applying five architectural controls:
1. Disable CSS animations and transitions via Playwright configuration.
2. Emulate reduced motion media preferences to prevent infinite animation loops.
3. Fix a static viewport resolution across all test workers.
4. Mask dynamic areas such as timestamps, live countdowns, and random avatar images.
5. Apply reasonable threshold tolerances (`maxDiffPixelRatio: 0.01`).

### Stabilized visual test suite
The following Playwright test demonstrates snapshot stabilization:

```typescript
// tests/visual/dashboard.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Dashboard Visual Regression', () => {
  test.beforeEach(async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.setViewportSize({ width: 1280, height: 800 });
  });

  test('matches baseline visual snapshot with masked dynamic regions', async ({ page }) => {
    await page.goto('/analytics/dashboard');
    await expect(page.getByRole('heading', { name: 'Analytics Overview' })).toBeVisible();

    const metricCard = page.getByTestId('revenue-metrics-card');

    await expect(page).toHaveScreenshot('dashboard-overview.png', {
      maxDiffPixelRatio: 0.01,
      threshold: 0.2,
      animations: 'disabled',
      mask: [
        page.getByTestId('live-clock'),
        page.getByTestId('user-avatar'),
        page.locator('.dynamic-relative-timestamp'),
      ],
      maskColor: '#2b2b2b',
    });

    await expect(metricCard).toHaveScreenshot('revenue-metric-card.png', {
      maxDiffPixels: 25,
      animations: 'disabled',
    });
  });
});
```

## 5. Automated accessibility testing with axe-core

Automated accessibility testing prevents digital barriers and verifies compliance with Web Content Accessibility Guidelines (WCAG 2.2 Level A and AA). Automated audits catch structural issues including missing form labels, invalid ARIA roles, color contrast failures, and missing image alternatives.

Automated scanners identify between 30% and 50% of accessibility violations. Combine automated scans with manual keyboard navigation audits to verify complete accessibility coverage.

### End-to-end audits with @axe-core/playwright
Incorporate `@axe-core/playwright` into continuous integration pipelines to audit pages and interactive modals:

```typescript
// tests/a11y/checkout.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Checkout Accessibility Audits', () => {
  test('fulfills WCAG 2.2 AA accessibility requirements across the primary checkout step', async ({ page }) => {
    await page.goto('/checkout');
    await expect(page.getByRole('heading', { name: 'Checkout' })).toBeVisible();

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .exclude('#third-party-payment-iframe')
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('modal dialog traps focus and satisfies accessible tree semantics', async ({ page }) => {
    await page.goto('/checkout');
    await page.getByRole('button', { name: /view terms/i }).click();

    const dialog = page.getByRole('dialog', { name: /terms of service/i });
    await expect(dialog).toBeVisible();

    const dialogScan = await new AxeBuilder({ page })
      .include('div[role="dialog"]')
      .analyze();

    expect(dialogScan.violations).toEqual([]);
  });
});
```

### Component-level accessibility testing
For isolated unit and component suites in Vitest, use `vitest-axe` or `jest-axe` to audit rendered components before merging:

```typescript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { expect, it } from 'vitest';
import { PrimaryButton } from './PrimaryButton';

expect.extend(toHaveNoViolations);

it('renders primary button without any axe accessibility violations', async () => {
  const { container } = render(
    <PrimaryButton aria-label="Submit Order">Submit Order</PrimaryButton>
  );
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```
