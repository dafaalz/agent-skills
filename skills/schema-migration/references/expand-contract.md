# Expand and contract migration lifecycle

Reference manual for executing zero-downtime database changes without breaking active application instances.

## Five-phase migration sequence

Changing active schemas requires splitting one logical change across five decoupled deployment phases:

| Phase | Database state | Application state | Forward action |
|---|---|---|---|
| 1. Expand | New column or table added as nullable | Deployed code ignores new column | Add additive schema elements with lock timeouts |
| 2. Dual-Write | Both old and new structures coexist | New code writes to both old and new columns; reads old | Deploy code writing to both old and new targets |
| 3. Backfill | Historic rows synced asynchronously | Code writes dual; reads old | Run batched worker backfill over old rows |
| 4. Read-Cutover | Both structures synchronized | New code reads from new column; writes dual | Switch application reads to new column |
| 5. Contract | Old column or table deprecated | Code reads and writes new column exclusively | Drop dual-write in code, then drop old column in database |

## Phase rules and transition gates

### Phase 1. Expand (additive only)

- Add new columns exclusively as nullable, or with engine-level instant defaults.
- In PostgreSQL 11 and newer, `ADD COLUMN ... DEFAULT <constant>` executes instantly as metadata update when the default is immutable.
- In MySQL 8.0, check `ALGORITHM=INSTANT` support before adding columns.
- Never add `NOT NULL` constraints directly to existing populated tables without a phased backfill.

### Phase 2. Dual-write

- Wrap write paths in application code or database triggers to duplicate mutations to new targets.
- Application-level dual writing isolates business logic inside service layers or repository adapters.
- Database triggers eliminate distributed lag during high-throughput writes.
- Dual writing must tolerate minor failures in secondary writes when eventual consistency suffices.

### Phase 3. Backfill

- Backfill historic records in chunked batches sorted by immutable primary key.
- Throttling prevents replication lag spikes and table bloat.
- Consult chunked backfill guides for primary key iteration algorithms and sleep throttling parameters.

### Phase 4. Read cutover

- Deploy configuration toggle directing read queries to the newly backfilled column or table.
- Verify parity between old and new columns via background sampling or shadow comparison before cutover.
- Keep rollback path open. If anomalies surface, toggle application reads back to the old column immediately without database rollback.

### Phase 5. Contract

- Deploy application release removing writes to the old deprecated column.
- Verify zero active queries read from or write to the old column via query analytics:
  - In PostgreSQL, query `pg_stat_statements` or `pg_stat_user_tables`.
  - In MySQL, inspect `performance_schema.events_statements_summary_by_digest`.
- Run final contraction migration dropping the deprecated column or table.

## Common anti-patterns

1. Atomic rename. Running `ALTER TABLE users RENAME COLUMN email TO primary_email` locks the table and breaks running instances expecting `email`. Always use expand, dual-write, backfill, cutover, contract.
2. In-place column type alteration. Changing `VARCHAR(50)` to `TEXT` or `INTEGER` to `BIGINT` triggers full table rewrites and exclusive locks. Create a new column, dual-write, backfill, cutover, and drop the old column.
3. Premature contraction. Dropping the old column in the same deployment that switches reads prevents rollback if bugs surface. Keep old structures intact for at least one full deployment cycle.
