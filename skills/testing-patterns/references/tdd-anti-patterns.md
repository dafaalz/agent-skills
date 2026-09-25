# Testing anti-patterns and examples

Load this reference only when the seam boundary, assertion strategy, or mock isolation requirements in the main skill are unclear. Do not load during normal execution.

## Anti-pattern 1: implementation coupling

Tests that mock private collaborators or inspect private state break whenever internal code changes, even if behavior stays correct.

### Bad
Mocking internal collaborators or verifying private fields:
```typescript
test('saves user to repository', async () => {
  const mockRepo = { save: jest.fn() };
  const service = new UserService(mockRepo);
  await service.register({ name: 'Alex' });
  expect(mockRepo.save).toHaveBeenCalledWith({ name: 'Alex' });
});
```

### Good
Testing observable behavior through the public contract:
```typescript
test('registers active user', async () => {
  const service = new UserService();
  const user = await service.register({ name: 'Alex' });
  expect(user.status).toBe('active');
});
```

## Anti-pattern 2: tautological assertions

Assertions that duplicate production calculation logic inside the test suite cannot catch logic bugs.

### Bad
Duplicating the formula:
```typescript
const taxRate = 0.11;
const total = price + (price * taxRate);
expect(calculateTotal(price)).toBe(total);
```

### Good
Asserting against a pre-calculated invariant:
```typescript
expect(calculateTotal(100)).toBe(111);
```

## Anti-pattern 3: horizontal slicing

Writing all tests upfront before writing production code produces speculative tests that miss boundary constraints.

Always use vertical slicing. Write one test, watch it fail, write minimal code to pass, then proceed to the next behavior.
