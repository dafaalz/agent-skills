# Test data management and fluent builders

Architectural standards for test data creation, Google DAMP principles, fluent builders, sensible defaults, synthetic generation, and multi-tenant sequence isolation.

## 1. DAMP principle and builder architecture

A resilient automated test suite requires an explicit test data strategy. Poorly structured fixtures introduce hidden coupling between unrelated tests and cause non-deterministic test suites.

### Comparison of test data strategies
Teams typically encounter three approaches to managing test data:

1. Raw fixtures (static JSON, YAML, or SQL dumps).
   * Drawbacks. Static files hide the specific attributes that matter to a test. When a test verifies that an inactive user cannot checkout, reading a 40-line JSON fixture obscures which property triggers the error. Moreover, database schema migrations require updating dozens of static fixture files.
2. The Object Mother pattern.
   * Drawbacks. A static factory class returns pre-configured domain entities. As edge cases multiply, the factory experiences combinatorial explosion with methods like `createActivePremiumUserWithOverdueBalance()` or `createUnverifiedUserWithPendingOrder()`.
3. The Test Data Builder pattern.
   * Advantages. Encapsulates sensible defaults while exposing a fluent, chainable interface for selectively overriding attributes.

### Google DAMP principles
Google Engineering advocates for DAMP (Descriptive And Meaningful Phrases) over strict DRY (Don't Repeat Yourself) in test suites. Test code should be clear and self-documenting:
* Keep all fields that directly influence the test outcome visible inside the test case.
* Conceal non-relevant boilerplate fields inside the builder defaults.
* Readers should understand why a test passes or fails without cross-referencing external fixture files.

## 2. Fluent test data builder implementation

A production-ready test data builder fulfills three criteria:
1. It constructs a complete, valid domain model by default with zero manual parameters required.
2. It provides type-safe chaining methods prefixed with `with` or specific state helpers such as `asAdmin()`.
3. It optionally provides a `persist()` method to insert the entity directly into a test database.

### Complete TypeScript builder example
The following implementation demonstrates a fluent builder for an Order domain model:

```typescript
import { randomUUID } from "node:crypto";
import { Pool } from "pg";

export enum OrderStatus {
  PENDING = "PENDING",
  PAID = "PAID",
  SHIPPED = "SHIPPED",
  CANCELLED = "CANCELLED",
}

export interface OrderLineItem {
  id: string;
  sku: string;
  unitPriceCents: number;
  quantity: number;
}

export interface Order {
  id: string;
  tenantId: string;
  customerId: string;
  status: OrderStatus;
  items: OrderLineItem[];
  totalAmountCents: number;
  createdAt: Date;
}

export class OrderBuilder {
  private id: string = randomUUID();
  private tenantId: string = "tenant-" + randomUUID().slice(0, 8);
  private customerId: string = "cust-" + randomUUID().slice(0, 8);
  private status: OrderStatus = OrderStatus.PENDING;
  private items: OrderLineItem[] = [
    {
      id: randomUUID(),
      sku: "SKU-DEFAULT-01",
      unitPriceCents: 2500,
      quantity: 1,
    },
  ];
  private createdAt: Date = new Date("2026-01-15T10:00:00Z");

  public withId(id: string): this {
    this.id = id;
    return this;
  }

  public withTenantId(tenantId: string): this {
    this.tenantId = tenantId;
    return this;
  }

  public withCustomerId(customerId: string): this {
    this.customerId = customerId;
    return this;
  }

  public withStatus(status: OrderStatus): this {
    this.status = status;
    return this;
  }

  public paid(): this {
    this.status = OrderStatus.PAID;
    return this;
  }

  public cancelled(): this {
    this.status = OrderStatus.CANCELLED;
    return this;
  }

  public withItems(items: OrderLineItem[]): this {
    this.items = items;
    return this;
  }

  public addItem(item: Partial<OrderLineItem>): this {
    this.items.push({
      id: item.id || randomUUID(),
      sku: item.sku || "SKU-EXTRA",
      unitPriceCents: item.unitPriceCents ?? 1000,
      quantity: item.quantity ?? 1,
    });
    return this;
  }

  public build(): Order {
    const totalAmountCents = this.items.reduce(
      (sum, item) => sum + item.unitPriceCents * item.quantity,
      0
    );

    return {
      id: this.id,
      tenantId: this.tenantId,
      customerId: this.customerId,
      status: this.status,
      items: this.items,
      totalAmountCents,
      createdAt: this.createdAt,
    };
  }

  public async persist(pool: Pool): Promise<Order> {
    const order = this.build();
    await pool.query(
      `INSERT INTO orders (id, tenant_id, customer_id, status, total_amount_cents, created_at)
       VALUES ($1, $2, $3, $4, $5, $6);`,
      [
        order.id,
        order.tenantId,
        order.customerId,
        order.status,
        order.totalAmountCents,
        order.createdAt,
      ]
    );

    for (const item of order.items) {
      await pool.query(
        `INSERT INTO order_items (id, order_id, sku, unit_price_cents, quantity)
         VALUES ($1, $2, $3, $4, $5);`,
        [item.id, order.id, item.sku, item.unitPriceCents, item.quantity]
      );
    }

    return order;
  }
}
```

### Usage in test specifications
In the test file, only the fields dictating the test scenario are expressed:

```typescript
// Test 1. Cancelling a paid order initiates a refund
const paidOrder = new OrderBuilder().paid().build();
const result = await processOrderCancellation(paidOrder);
expect(result.refundIssued).toBe(true);

// Test 2. Empty item list throws validation error
const emptyOrder = new OrderBuilder().withItems([]).build();
expect(() => validateOrder(emptyOrder)).toThrow('Order must contain at least one item');
```

## 3. Sensible defaults and synthetic data generation

Builders must generate distinct synthetic data values to avoid unique constraint violations during parallel test runs.

### Rules for sensible defaults
1. Unique identifiers. Use version 4 UUIDs or monotonic sequence numbers rather than hardcoded IDs like `1` or `id-test`.
2. Valid relational formats. Generate valid email formats (`user-xxx@example.internal`), phone numbers conforming to E.164, and ISO timestamps.
3. Reasonable bounds. Set default monetary balances and item counts to reasonable positive amounts to satisfy check constraints.

### Integrating synthetic data libraries
Combine fluent builders with synthetic data generators such as `@faker-js/faker` to produce realistic boundary values:

```typescript
import { faker } from "@faker-js/faker";

export class UserProfileBuilder {
  private id: string = faker.string.uuid();
  private email: string = faker.internet.email({ provider: "example.internal" });
  private fullName: string = faker.person.fullName();
  private bio: string = faker.lorem.paragraph();
  private signupDate: Date = faker.date.recent({ days: 30 });

  public withEmail(email: string): this {
    this.email = email;
    return this;
  }

  public withBio(bio: string): this {
    this.bio = bio;
    return this;
  }

  public build() {
    return {
      id: this.id,
      email: this.email,
      fullName: this.fullName,
      bio: this.bio,
      signupDate: this.signupDate,
    };
  }
}
```

## 4. Multi-tenant and sequence isolation

In modern cloud applications and microservices, multi-tenancy and data concurrency require strict test isolation. Sharing static tenant identifiers across concurrent tests causes state leakage and race conditions.

### Sequence isolation helper
When entities require incremental keys (such as order numbers or invoice codes), use an atomic in-memory sequence generator:

```typescript
export class SequenceGenerator {
  private static counters = new Map<string, number>();

  public static next(prefix: string): string {
    const current = (this.counters.get(prefix) || 0) + 1;
    this.counters.set(prefix, current);
    return prefix + "-" + String(current).padStart(6, "0");
  }

  public static reset(): void {
    this.counters.clear();
  }
}
```

### Multi-tenant isolation pattern
Every test must execute within an isolated tenant partition. Builders enforce this by attaching unique tenant identifiers to all created entities:

```typescript
import { randomUUID } from "node:crypto";
import { Pool } from "pg";

export class TenantContext {
  public readonly tenantId: string;

  constructor() {
    this.tenantId = "tenant-" + randomUUID();
  }

  public createOrderBuilder(): OrderBuilder {
    return new OrderBuilder().withTenantId(this.tenantId);
  }
}
```

### Verifying row-level security boundaries
Verify multi-tenant data isolation by asserting that queries executed under Tenant A cannot observe or mutate records created under Tenant B:

```typescript
it("prevents cross-tenant data leaks under PostgreSQL Row-Level Security", async () => {
  const tenantA = new TenantContext();
  const tenantB = new TenantContext();

  const orderA = await tenantA.createOrderBuilder().persist(pool);

  // Attempt query under Tenant B database session context
  const clientB = await pool.connect();
  try {
    await clientB.query("SET LOCAL app.current_tenant_id = $1;", [tenantB.tenantId]);
    const result = await clientB.query(
      "SELECT * FROM orders WHERE id = $1;",
      [orderA.id]
    );

    expect(result.rows.length).toBe(0);
  } finally {
    clientB.release();
  }
});
```
