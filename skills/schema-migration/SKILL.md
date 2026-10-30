---
name: schema-migration
description: Use when authoring, reviewing, testing, or executing database schema migrations, column renames, type conversions, table splits, or backfills. Don't use for raw application query optimization (use systematic-debugging or inspect query plans directly), static mock data seeding (use testing-patterns), or schema-less document modeling (use codebase-design).
---

# Schema migration

Design, test, and execute zero-downtime relational database schema migrations. Enforce the four-gate zero-downtime contract across destructive DDL audits, dual-compatibility expand-contract phases, batched backfills, and reversibility rehearsals.

<HARD-GATE>
Write-Target Boundary. Write only to migration directories (`database/migrations/`, `prisma/migrations/`, `src/db/migrations/`) and `.agents/state/schema-migration/`. Do not execute migration or backfill commands against non-local databases without explicit user approval recorded in `.agents/state/schema-migration/apply-approval.md` naming the target host and database. Refuse any command whose resolved connection string is not `localhost`, `127.0.0.1`, or a container-local host.
</HARD-GATE>

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
- Inspect table row counts and index footprint using the query for the engine detected above:
  * PostgreSQL:
    ```sql
    SELECT relname, n_live_tup FROM pg_stat_user_tables WHERE relname = 'target_table';
    ```
  * MySQL 8.0+:
    ```sql
    SELECT TABLE_NAME, TABLE_ROWS FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'target_table';
    ```
  * SQLite:
    ```sql
    SELECT COUNT(*) FROM target_table;
    ```
  * Record the observed count and the query used in `.agents/state/schema-migration/recon.json` under `row_count_query` and `row_count`.
- Classify proposed change into additive, backfill, cutover, or destructive contraction.

Completion criterion. `.agents/state/schema-migration/recon.json` exists on disk with `engine`, `engine_version`, `row_count`, `index_count`, `migration_toolchain`, and `change_class`.

### Step 2. Expand and contract phase planning

Map requested structural changes to the five-phase expand-contract pattern:
- Consult `references/expand-contract.md` to split changes across separate deployments.
- For column renames or type conversions, design new column alongside old column; never alter existing columns in place.
- Plan dual-writing in application service layer or database triggers.
- Plan asynchronous worker backfill for existing rows.
- Define application read cutover toggle.
- Schedule final contraction migration dropping deprecated structures for a separate subsequent release.

Completion criterion. `.agents/state/schema-migration/phase-plan.md` exists on disk with five headings: `## Expand`, `## Dual-write`, `## Backfill`, `## Cutover`, `## Contract`, each mapped to a specific release tag or file path.

### Step 3. Author migration scripts and lock controls

Write deterministic migration scripts with mandatory lock safeguards:
- Set session-level lock timeouts before running DDL commands. Use the syntax for the engine detected in Step 1:
  * PostgreSQL: `SET lock_timeout = '2s'; SET statement_timeout = '10s';`
  * MySQL 8.0+: `SET SESSION lock_wait_timeout = 2; SET SESSION innodb_lock_wait_timeout = 2;`
  * SQLite: no session lock timeout applies. Use `PRAGMA busy_timeout = 2000;` and note that SQLite serializes writers; treat DDL as exclusive and schedule offline.
  * Consult `references/lock-timeouts-and-ddl.md` for the full per-engine matrix.
- Add indexes concurrently without blocking writes (`CREATE INDEX CONCURRENTLY` in PostgreSQL, `ALGORITHM=INPLACE, LOCK=NONE` in MySQL).
- Add foreign keys as `NOT VALID` first, then run asynchronous validation in a separate step.
- Write batched backfill scripts using chunked primary keys (`id > last_seen_id LIMIT 1000`) and throttling. Consult `references/batched-backfills.md`.
- Provide paired down-migration script restoring previous schema state.

Completion criterion. Migration files exist on disk with paired `_up.sql` and `_down.sql` (or framework equivalents). `grep -n "lock_timeout\|lock_wait_timeout\|busy_timeout" <up-migration-file>` returns at least one match for the engine detected in Step 1.

### Step 4. Rehearsal and reversibility verification

Rehearse migration on local test database or shadow container before staging deployment:
1. Baseline verification. Run existing test suite against current schema.
2. Forward migration test. Resolve the migration command for the toolchain detected in Step 1. Do not use `||` fallback chains; a non-zero exit from the resolved command is a hard failure. Run only the command for the detected toolchain:
   * Prisma: `npx prisma migrate deploy`
   * Knex: `npx knex migrate:latest`
   * Flyway: `flyway migrate`
   * Liquibase: `liquibase update`
   * Django: `python manage.py migrate`
   * Laravel: `php artisan migrate --force`
   * Raw SQL: `psql -v ON_ERROR_STOP=1 -f <file>` or the engine equivalent with stop-on-error enabled

   Run the resolved command exactly once. If it exits non-zero, record the exact command and exit code in `.agents/state/schema-migration/rehearsal-failure.json` and stop. Do not attempt the next toolchain command.
3. Reversibility test. Execute rollback script (`down`) and confirm database returns to baseline state without residual constraints or invalid indexes.
4. Reapplication test. Re-apply forward migration script (`up`) to confirm idempotent execution.
5. Lock duration check. Confirm DDL execution completes within configured lock timeout budget.

Completion criterion. Migration executes forward, rolls back backward, and reapplies forward in test database with zero failures and zero unhandled lock timeouts.

## Common migration hazards

| Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|
| Unindexed foreign key | Foreign key column without an index on the referencing side | Parent row deletion acquires a table-wide lock cascade | Create the index concurrently before adding the foreign key |
| Adding column with non-constant default | `ALTER TABLE ... ADD COLUMN ... DEFAULT now()` on old engines | Full table rewrite under an exclusive lock blocks all writes | Add the column nullable, backfill in batches, then apply the default |
| In-place type change | `ALTER COLUMN ... TYPE ...` on a live table | Long exclusive table lock and full table rewrite | Create new column, dual-write, backfill, cut over, drop old |
| Missing lock timeout | DDL executed without a session lock timeout | DDL queues behind reads and blocks all subsequent queries | Set the per-engine lock timeout from Step 3 before running DDL |
| Atomic column rename | `ALTER TABLE ... RENAME COLUMN` in a single release | Breaks active application instances expecting the old name | Split across expand-contract releases; run in Step 2 plan |

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
