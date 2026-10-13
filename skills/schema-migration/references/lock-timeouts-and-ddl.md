# Lock timeouts and online DDL operations

Reference manual for controlling lock queues, preventing table lock starvation, and executing online DDL in production.

## Lock queue starvation mechanism

DDL statements require exclusive locks (AccessExclusiveLock in PostgreSQL, Metadata Lock in MySQL). When a DDL statement queues waiting for long-running read queries to complete, subsequent incoming read queries queue behind the DDL request. This creates connection pool exhaustion and application downtime within seconds.

## PostgreSQL lock configuration

Always set session-level lock timeouts before executing DDL commands:

```sql
SET lock_timeout = '2s';
SET statement_timeout = '10s';
ALTER TABLE orders ADD COLUMN status_code VARCHAR(32);
```

If lock acquisition fails after 2 seconds, the transaction aborts cleanly without blocking incoming read traffic. Implement exponential retry loops with jitter in migration harnesses.

### PostgreSQL index operations

Never create indexes with standard `CREATE INDEX` on production tables. Use concurrent creation:

```sql
SET lock_timeout = '5s';
SET statement_timeout = '0';
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders (user_id);
```

Concurrent index creation does not lock writes, but runs in two passes outside a transaction block. Verify index validity after completion:

```sql
SELECT indrelid::regclass, indexrelid::regclass, indisvalid
FROM pg_index
WHERE indisvalid = false;
```

If an index fails during concurrent creation, drop it with `DROP INDEX CONCURRENTLY` and recreate it.

### Adding foreign keys safely

Add foreign keys using two distinct non-blocking steps:

1. Add constraint with `NOT VALID` (requires brief lock, skips table validation scan):
```sql
ALTER TABLE orders
  ADD CONSTRAINT fk_orders_user_id
  FOREIGN KEY (user_id) REFERENCES users(id)
  NOT VALID;
```

2. Validate constraint concurrently in background (does not block writes):
```sql
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_user_id;
```

## MySQL online DDL

MySQL 8.0 supports online DDL through `ALGORITHM` and `LOCK` clauses. Explicitly specify these parameters to prevent unexpected table copying:

```sql
ALTER TABLE customers
  ADD COLUMN loyalty_tier INT DEFAULT 0,
  ALGORITHM=INSTANT,
  LOCK=NONE;
```

### MySQL algorithm options

- `ALGORITHM=INSTANT`. Modifies metadata only. Completes in milliseconds without locking reads or writes. Available for adding columns at table end in MySQL 8.0.12+, and at arbitrary positions in MySQL 8.0.29+.
- `ALGORITHM=INPLACE`. Rebuilds table in place without moving data to temporary copy table. Concurrent DML permitted when `LOCK=NONE` is set.
- `ALGORITHM=COPY`. Copies entire table into temporary table with shared read lock. Blocks writes during operation. Reject migrations requiring copy algorithm on large tables.

For operations unsupported by `INSTANT` or `INPLACE`, use external online schema tools like `gh-ost` or `pt-online-schema-change`.

## DDL safety matrix

| Operation | PostgreSQL safe pattern | MySQL safe pattern |
|---|---|---|
| Add nullable column | Set `lock_timeout`, run `ADD COLUMN` | `ALGORITHM=INSTANT, LOCK=NONE` |
| Add column with default | Default is constant (PG 11+) | `ALGORITHM=INSTANT, LOCK=NONE` |
| Create index | `CREATE INDEX CONCURRENTLY` | `ALGORITHM=INPLACE, LOCK=NONE` |
| Add foreign key | `ADD CONSTRAINT ... NOT VALID`, then `VALIDATE` | Requires pt-online-schema-change or gh-ost |
| Drop column | Drop or rename column with lock timeout | `ALGORITHM=INSTANT` (MySQL 8.0.29+) |
