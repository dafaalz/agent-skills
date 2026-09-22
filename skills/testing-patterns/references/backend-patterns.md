# Backend testing patterns and infrastructure standards

Architectural standards for test doubles, ephemeral containerized dependencies, database cleanup strategies, consumer-driven contracts, and property-based API fuzzing.

## 1. Test double taxonomy (Fowler and Meszaros)

The term mock is often used loosely for any test replacement object. Gerard Meszaros formalized the exact classification in xUnit Test Patterns, later expanded by Martin Fowler in Mocks Aren't Stubs. Using the correct test double preserves test clarity and prevents over-coupling to implementation details.

| Double type | Definition | Verification style | Typical backend use case |
| :--- | :--- | :--- | :--- |
| **Dummy** | Objects passed into methods solely to satisfy parameter signatures. They are never invoked or inspected. | No verification | Passing empty configuration objects or unused authorization contexts into constructors. |
| **Stub** | Objects providing canned responses to calls made during the test. They return fixed data and do not respond to calls outside their programmed set. | State verification | Providing a canned exchange rate response from an external currency converter service. |
| **Spy** | Advanced stubs that record execution telemetry such as call counts, passed parameters, and invocation ordering. | State and indirect output verification | Verifying an email dispatcher received a specific recipient email address without transmitting real messages. |
| **Mock** | Objects pre-programmed with exact behavioral expectations. They verify interactions directly and fail if expected invocations do not match actual calls. | Behavior verification | Asserting that an event publisher method was called exactly once with specific binary payloads. |
| **Fake** | Fully functional implementations that take architectural shortcuts unsuitable for production workloads. | State verification | In-memory repository implementations using hash maps, embedded key-value stores, or simulated clock providers. |

### Classical (Detroit) vs mockist (London) verification

The testing community distinguishes between two testing philosophies:

1. The Classical School (Detroit / state-based). Focuses on testing collaborating domain objects together. Avoids mocking internal classes, using test doubles almost exclusively for out-of-process boundaries such as external third-party HTTP gateways. Verification inspects the final state of the system under test. Tests remain resilient to internal refactoring because method signatures can evolve without breaking the test suite.
2. The London School (London / interaction-based). Drives design outside-in by mocking all immediate collaborators of the class under test. Verification focuses on method calls, argument passing, and call counts. While this approach enforces strict class isolation, it often produces brittle test suites that break whenever internal collaborator call graphs change.

Modern backend engineering favors the Classical approach for domain logic. Test real domain entities collaborating with real domain services, replacing only outbound port interfaces with in-memory Fakes or boundary Stubs when necessary.

## 2. Testcontainers PostgreSQL setup with tmpfs and singleton reuse

Relying on in-memory database emulators like SQLite or H2 when running PostgreSQL in production creates dangerous false positives. Emulators lack Postgres-specific JSONB operators, concurrency locking semantics (`FOR UPDATE SKIP LOCKED`), sequence generation rules, and distinct syntax.

Modern backend testing runs real production engines inside ephemeral Docker containers using Testcontainers. To achieve sub-second test runtimes, suites must adopt two optimizations:
1. Singleton container lifecycle. Spin up a single container shared across all test files in the process rather than recreating containers per test file.
2. In-memory tmpfs mount. Mount the database data directory to `/var/lib/postgresql/data` with `rw` tmpfs options, eliminating disk synchronization overhead.

### Singleton Postgres test harness
The following TypeScript class provides a complete singleton container harness:

```typescript
import { GenericContainer, StartedTestContainer } from "testcontainers";
import { Pool } from "pg";

export class PostgresTestEnvironment {
  private static instance: PostgresTestEnvironment;
  private container: StartedTestContainer | null = null;
  private pool: Pool | null = null;

  private constructor() {}

  public static getInstance(): PostgresTestEnvironment {
    if (!PostgresTestEnvironment.instance) {
      PostgresTestEnvironment.instance = new PostgresTestEnvironment();
    }
    return PostgresTestEnvironment.instance;
  }

  public async start(): Promise<void> {
    if (this.container) {
      return;
    }

    this.container = await new GenericContainer("postgres:16-alpine")
      .withEnvironment({
        POSTGRES_USER: "test_user",
        POSTGRES_PASSWORD: "test_password",
        POSTGRES_DB: "test_database",
      })
      .withExposedPorts(5432)
      .withTmpfs({ "/var/lib/postgresql/data": "rw" })
      .start();

    const host = this.container.getHost();
    const port = this.container.getMappedPort(5432);

    this.pool = new Pool({
      host,
      port,
      user: "test_user",
      password: "test_password",
      database: "test_database",
      max: 10,
    });

    await this.runMigrations();
  }

  private async runMigrations(): Promise<void> {
    if (!this.pool) {
      throw new Error("Connection pool not initialized.");
    }

    await this.pool.query(`
      CREATE TABLE IF NOT EXISTS accounts (
        id UUID PRIMARY KEY,
        balance_cents BIGINT NOT NULL CHECK (balance_cents >= 0),
        version INT NOT NULL DEFAULT 1,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );

      CREATE TABLE IF NOT EXISTS idempotency_keys (
        key VARCHAR(255) PRIMARY KEY,
        locked_until TIMESTAMPTZ NOT NULL,
        response_code INT,
        response_body JSONB
      );
    `);
  }

  public getPool(): Pool {
    if (!this.pool) {
      throw new Error("PostgreSQL test container has not started.");
    }
    return this.pool;
  }

  public async stop(): Promise<void> {
    if (this.pool) {
      await this.pool.end();
      this.pool = null;
    }
    if (this.container) {
      await this.container.stop();
      this.container = null;
    }
  }
}
```

## 3. Database cleanup strategies (cascading truncation vs transaction rollback)

Shared database containers require reliable data isolation between test cases. Two primary strategies exist, each with specific tradeoffs.

### Comparison of reset mechanisms

1. Transaction rollback strategy. Each test opens a transaction (`BEGIN`), performs inserts and queries, and executes an explicit `ROLLBACK` in the teardown hook.
   * Advantages. Fast execution because writes remain uncommitted in memory buffers.
   * Caveats and failure modes. Cannot test asynchronous background jobs that read data via independent database connections. Fails when application code manages its own transactions, issues nested commits, or uses savepoints. Cannot validate distributed locks or multi-connection concurrency scenarios.

2. Cascading truncation strategy. Tests commit real transactions to the database. In the test setup or teardown hook, the test harness dynamically discovers all user tables and issues a cascading truncate command.
   * Advantages. Provides production fidelity. Supports concurrent HTTP requests, background workers, and multi-connection transaction verification.
   * Performance mitigation. Combining table truncation with tmpfs mounts keeps cleanup execution times under 10 milliseconds per test.

### Dynamic truncation utility
The following utility dynamically queries Postgres system catalogs to truncate all non-migration tables in a single statement:

```typescript
import { Pool } from "pg";

export async function truncateAllTables(pool: Pool): Promise<void> {
  const query = `
    SELECT tablename 
    FROM pg_tables 
    WHERE schemaname = 'public' 
      AND tablename != 'schema_migrations';
  `;

  const { rows } = await pool.query<{ tablename: string }>(query);
  if (rows.length === 0) {
    return;
  }

  const tableList = rows.map((r) => `"${r.tablename}"`).join(", ");
  await pool.query(`TRUNCATE TABLE ${tableList} RESTART IDENTITY CASCADE;`);
}
```

## 4. Consumer-driven contract testing with Pact

In distributed microservice systems, maintaining end-to-end integration environments with all live services running simultaneously introduces high operational overhead and brittle CI pipelines. Consumer-Driven Contract Testing provides cross-service verification without live dependencies.

The consumer service defines a contract specifying the exact HTTP requests it sends and the expected response shapes. The Pact framework records these interactions into a contract JSON file. The provider service subsequently replays the recorded contract against its own endpoints in its isolated build pipeline.

### Pact consumer test example
The following test defines a contract between an Order service consumer and an Inventory service provider:

```typescript
import { PactV3, MatchersV3 } from "@pact-foundation/pact";
import path from "node:path";

const provider = new PactV3({
  consumer: "OrderService",
  provider: "InventoryService",
  dir: path.resolve(process.cwd(), "pacts"),
});

describe("Inventory Service Contract Verification", () => {
  it("validates reservation endpoint contract successfully", async () => {
    provider
      .given("item sku-99 is available in inventory with quantity 10")
      .uponReceiving("a request to reserve inventory for an order")
      .withRequest({
        method: "POST",
        path: "/api/v1/reservations",
        headers: {
          "Content-Type": "application/json",
        },
        body: {
          sku: "sku-99",
          quantity: 3,
        },
      })
      .willRespondWith({
        status: 201,
        headers: {
          "Content-Type": "application/json",
        },
        body: {
          reservationId: MatchersV3.uuid("b3d683a2-192a-4648-936b-592f15309320"),
          sku: MatchersV3.equal("sku-99"),
          reservedQuantity: MatchersV3.integer(3),
          status: MatchersV3.regex(/^(PENDING|CONFIRMED)$/, "CONFIRMED"),
        },
      });

    await provider.executeTest(async (mockServer) => {
      const response = await fetch(`${mockServer.url}/api/v1/reservations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sku: "sku-99", quantity: 3 }),
      });

      const body = await response.json();
      expect(response.status).toBe(201);
      expect(body.sku).toBe("sku-99");
      expect(body.reservedQuantity).toBe(3);
    });
  });
});
```

## 5. Property-based testing and API fuzzing with Schemathesis

Example-based tests only verify input variations that developers explicitly imagine. Property-based fuzzing systematically sends thousands of generated, edge-case, and boundary-value inputs to expose unhandled crashes, memory leaks, and OpenAPI specification drift.

Schemathesis automates this process by parsing an OpenAPI definition and executing property checks using the Hypothesis framework.

### Schemathesis conformance suite
The following Python suite automatically tests an API against its OpenAPI specification:

```python
import schemathesis
from schemathesis import Case

schema = schemathesis.from_uri("http://127.0.0.1:8000/openapi.json")

@schema.parametrize()
def test_api_conformance(case: Case):
    response = case.call()

    case.validate_response(
        response,
        checks=(
            schemathesis.checks.not_a_server_error,
            schemathesis.checks.status_code_conformance,
            schemathesis.checks.content_type_conformance,
            schemathesis.checks.response_schema_conformance,
        ),
    )
```

### CLI quick-fuzz execution
Teams can also integrate Schemathesis directly into continuous integration workflows via the command-line interface:

```bash
schemathesis run http://127.0.0.1:8000/openapi.json \
  --checks all \
  --workers 4 \
  --hypothesis-max-examples 100
```

This command asserts three baseline invariants:
1. The server never responds with an unhandled 500 status code.
2. Returned status codes strictly match those declared in the specification.
3. Response headers and JSON payloads conform to their OpenAPI schemas.
