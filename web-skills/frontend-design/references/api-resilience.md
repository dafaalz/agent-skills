# Resilient frontend API integration patterns

Production patterns for resilient asynchronous network communication, race condition elimination, and state consistency in browser applications.

## 1. Race condition prevention with AbortController

Rapid user typing or tab switching triggers out-of-order network responses where an earlier slow request overwrites a newer response.

Cancel previous in-flight requests using `AbortController`:

```typescript
let activeController: AbortController | null = null;

export async function searchEntities(query: string): Promise<Entity[]> {
  if (activeController) {
    activeController.abort();
  }

  activeController = new AbortController();
  const { signal } = activeController;

  try {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`, { signal });
    if (!response.ok) {
      throw new Error(`Search request failed with status ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      return []; // Request was aborted cleanly by subsequent user input
    }
    throw error;
  }
}
```

## 2. Exponential backoff with jitter

Retry failed network requests on transient failures (network drop, 502, 503, 504 status codes):

```typescript
export async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  retries = 3,
  delayMs = 500
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (retries <= 0) {
      throw error;
    }
    // Exponential backoff with full jitter to avoid thundering herds
    const jitter = Math.random() * delayMs;
    await new Promise((resolve) => setTimeout(resolve, delayMs + jitter));
    return fetchWithRetry(fn, retries - 1, delayMs * 2);
  }
}
```

Rule. Only retry idempotent operations (GET, HEAD, PUT). Never retry POST requests without an idempotency key header.

## 3. Optimistic UI mutations with rollback

Update interface state immediately, then revert if the network request fails:

```typescript
export async function toggleBookmark(
  itemId: string,
  currentState: boolean,
  updateLocalUI: (state: boolean) => void
): Promise<void> {
  const previousState = currentState;
  const nextState = !currentState;

  // 1. Optimistic apply
  updateLocalUI(nextState);

  try {
    const response = await fetch(`/api/items/${itemId}/bookmark`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bookmarked: nextState }),
    });

    if (!response.ok) {
      throw new Error('Server rejected mutation');
    }
  } catch (error) {
    // 2. Rollback on failure
    updateLocalUI(previousState);
    throw error;
  }
}
```
