# Batched backfills and throttled migrations

Reference manual for migrating massive datasets without inducing replication lag, lock contention, or transaction log overflow.

## Core backfill principles

1. Primary key chunking. Chunk iterations using monotonically increasing indexed primary keys (`id > last_seen_id LIMIT 1000`). Never use `OFFSET` pagination because `OFFSET` scans prior rows repeatedly and degrades quadratically.
2. Throttled sleep. Sleep between batches to allow replica replication lag to drain and connection pools to breathe.
3. Resumable checkpointing. Persist the highest processed ID to a tracking table so interrupted migrations resume without duplicating work.
4. Idempotency. Ensure backfill updates produce identical outcomes when executed multiple times over the same range.

## Chunking query pattern

Use this standard pattern for chunked primary key updates:

```sql
UPDATE users
SET full_name = CONCAT(first_name, ' ', last_name)
WHERE id > :last_processed_id
  AND id <= :target_chunk_id
  AND full_name IS NULL;
```

Determine `:target_chunk_id` using a lightweight indexed range probe:

```sql
SELECT id
FROM users
WHERE id > :last_processed_id
ORDER BY id ASC
OFFSET :batch_size - 1
LIMIT 1;
```

## Checkpoint tracking schema

Create a dedicated migration progress table before launching long-running backfills:

```sql
CREATE TABLE IF NOT EXISTS schema_migration_backfills (
  backfill_name VARCHAR(128) PRIMARY KEY,
  last_processed_id BIGINT NOT NULL DEFAULT 0,
  target_max_id BIGINT NOT NULL,
  batch_size INT NOT NULL DEFAULT 1000,
  sleep_duration_ms INT NOT NULL DEFAULT 100,
  status VARCHAR(32) NOT NULL DEFAULT 'running',
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Throttling and replication lag checks

Monitor replication lag inside the worker loop before dispatching the next chunk:

### PostgreSQL lag probe

```sql
SELECT COALESCE(
  MAX(EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp())))::INT,
  0
) AS replication_lag_seconds
FROM pg_stat_replication;
```

Pause backfill execution if `replication_lag_seconds` exceeds 5 seconds.

### MySQL lag probe

Inspect replica status:

```sql
SHOW REPLICA STATUS;
```

Inspect the `Seconds_Behind_Source` column. If the lag exceeds 5 seconds, sleep for 2 seconds before retrying the batch.

## Error handling and dead-letter records

When individual rows cause conversion errors (such as invalid JSON payloads or encoding errors):
- Log the failed row ID and error payload to a dead-letter table `schema_migration_failures`.
- Increment the chunk pointer past the failed row to prevent blocking the entire backfill pipeline.
- Alert operators with the failure count at batch completion.
