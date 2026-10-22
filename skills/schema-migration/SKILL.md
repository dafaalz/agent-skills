---
name: schema-migration
description: Use when authoring, reviewing, testing, or executing database schema migrations, column renames, type conversions, table splits, or backfills. Don't use for raw application query optimization, static mock data seeding (use testing-patterns), or schema-less document modeling.
---

# Schema migration

Design, test, and execute zero-downtime relational database schema migrations. Enforce the four-gate zero-downtime contract across destructive DDL audits, dual-compatibility expand-contract phases, batched backfills, and reversibility rehearsals.

## Modes

Select the execution mode before starting Step 1:
- Plan and Author mode (default). Inspect database engine and schema, author decoupled expand and contract migration files, configure lock timeouts, and write backfill scripts.
- Audit and Rehearsal mode. Review proposed migration files against lock hazards, simulate migrations on shadow databases, measure lock acquisition durations, and verify reversible rollbacks.

## The four-gate zero-downtime contract

Every schema evolution must satisfy four verification gates:
1. Destructive DDL gate. Zero unbounded table rewrites, zero exclusive locks without timeouts, and zero direct `NOT NULL` constraints on existing tables.
2. Dual-compatibility gate. Old application code versions and new application code versions can read and write simultaneously during the transition phase.
3. Batched backfill gate. Historic records migrated in chunked batches by primary key with sleep throttling and checkpoint tracking.
4. Up-down-up reversibility gate. Migration applies cleanly forward, rolls back cleanly backward, and reapplies forward in test environments with zero orphaned artifacts.

## Reference modules

Load reference files on demand based on migration scope:

| Concern | Reference file |
|---|---|
| Multi-phase lifecycle | [references/expand-contract.md](references/expand-contract.md) |
| Locks and online DDL | [references/lock-timeouts-and-ddl.md](references/lock-timeouts-and-ddl.md) |
| Batched backfills | [references/batched-backfills.md](references/batched-backfills.md) |

## Workflow

Follow these four steps in sequence.

### Step 1. Engine and schema reconnaissance

Inspect target database engine, version, active table volume, and existing migration state:
- Identify database platform and engine version (such as PostgreSQL 14+, MySQL 8.0+, SQLite).
- Check current migration toolchain (such as Knex, Prisma, Flyway, Liquibase, Django, Laravel, or raw SQL).
- Inspect table row counts and index footprint:
```sql
SELECT relname, n_live_tup
FROM pg_stat_user_tables
WHERE relname = 'target_table';
```
- Classify proposed change into additive, backfill, cutover, or destructive contraction.

Completion criterion. Target database engine identified, active table volume recorded, and migration classification logged with zero assumptions.

### Step 2. Expand and contract phase planning

Map requested structural changes to the five-phase expand-contract pattern:
- Consult `references/expand-contract.md` to split changes across separate deployments.
- For column renames or type conversions, design new column alongside old column; never alter existing columns in place.
- Plan dual-writing in application service layer or database triggers.
- Plan asynchronous worker backfill for existing rows.
- Define application read cutover toggle.
- Schedule final contraction migration dropping deprecated structures for a separate subsequent release.

Completion criterion. Written phase plan mapping change across expand, dual-write, backfill, cutover, and contract phases.

### Step 3. Author migration scripts and lock controls

Write deterministic migration scripts with mandatory lock safeguards:
- Set session-level lock timeouts before running DDL commands. Consult `references/lock-timeouts-and-ddl.md`.
```sql
SET lock_timeout = '2s';
SET statement_timeout = '10s';
```
- Add indexes concurrently without blocking writes (`CREATE INDEX CONCURRENTLY` in PostgreSQL, `ALGORITHM=INPLACE, LOCK=NONE` in MySQL).
- Add foreign keys as `NOT VALID` first, then run asynchronous validation in a separate step.
- Write batched backfill scripts using chunked primary keys (`id > last_seen_id LIMIT 1000`) and throttling. Consult `references/batched-backfills.md`.
- Provide paired down-migration script restoring previous schema state.

Completion criterion. Migration scripts authored with explicit lock timeouts, non-blocking index creation, and functional down-migration rollback blocks.

### Step 4. Rehearsal and reversibility verification

Rehearse migration on local test database or shadow container before staging deployment:
1. Baseline verification. Run existing test suite against current schema.
2. Forward migration test. Apply forward migration script (`up`):
```bash
npm run migrate:up || python manage.py migrate || php artisan migrate
```
3. Reversibility test. Execute rollback script (`down`) and confirm database returns to baseline state without residual constraints or invalid indexes.
4. Reapplication test. Re-apply forward migration script (`up`) to confirm idempotent execution.
5. Lock duration check. Confirm DDL execution completes within configured lock timeout budget.

Completion criterion. Migration executes forward, rolls back backward, and reapplies forward in test database with zero failures and zero unhandled lock timeouts.

## Common migration hazards

| Hazard | Consequence | Safe alternative |
|---|---|---|
| Unindexed foreign key | Table lock cascade during parent row deletion | Create index on referencing column concurrently |
| Adding column with non-constant default | Full table rewrite locking writes on old engines | Add nullable column, backfill in batches, apply default |
| In-place type change | Long exclusive table lock and full rewrite | Create new column, dual-write, backfill, cutover, drop old |
| Missing lock timeout | DDL queues behind reads and blocks all subsequent queries | Set `lock_timeout = '2s'` before running DDL |
| Atomic column rename | Breaks active application instances expecting old name | Expand-contract lifecycle across separate releases |

## Boundary isolation

Design and audit database migrations, DDL statements, and backfill scripts only. Do not rewrite frontend UI components, modify application business logic, or generate artificial seed data during migration authoring.

## Quick audit checklist

Run this check before approving any database migration:

| Check | Passing condition |
|---|---|
| Lock timeout | Session `lock_timeout` declared before DDL statements |
| Online indexing | Indexes created concurrently without blocking concurrent writes |
| Expand-contract | Destructive changes split across distinct expand and contract steps |
| Batched backfill | Historic updates chunked by indexed primary key with throttling |
| Reversibility | Script verified forward, backward, and forward in test container |
| Down script | Complete, matching rollback logic provided for every migration step |
