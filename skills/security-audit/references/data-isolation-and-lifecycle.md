# Data isolation and lifecycle hunting

Reach for this file when the target stores multi-tenant or access-controlled data, derives search, index, cache, or analytics copies, issues object links, exports or restores records, migrates schemas, or promises deletion, revocation, and retention behavior. This domain follows one data item through every copy and state transition. Use `attack-classes.md` for endpoint-level access control and `cloud-and-deployment.md` for provider-level storage policy.

Split large targets by primary storage, cache and search, object storage, analytics and logging, export and backup, deletion and revocation, and migration.

## Authoritative standards

Ground data isolation and lifecycle audits in these authoritative specifications:

| Standard | Publishing body | Reference URL | Focus |
|---|---|---|---|
| OWASP API Security Top 10 2023 | OWASP Foundation | https://owasp.org/www-project-api-security/ | BOLA and object-level authorization vulnerabilities |
| NIST SP 800-88 Rev. 1 | NIST | https://csrc.nist.gov/publications/detail/sp/800-88/rev-1/final | Media sanitization and cryptographic erasure guidelines |
| PostgreSQL Row Level Security | PostgreSQL Global Development Group | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | Database-enforced multi-tenant isolation architectures |

## Core discipline

Include these rules in every agent prompt for this domain:

```text
- A tenant or owner field on a record is not isolation. Find the query, key, path, policy, or row-level control that enforces it for each read and write path.
- Trace derived copies. Sanitized primary data can become unsafe in search, cache, analytics, export, previews, logs, replicas, and backups with different ACL and retention rules.
- Deletion and revocation are lifecycle contracts. Check current, historical, cached, indexed, exported, restored, and queued copies within the product stated boundary.
- Privacy or retention preference is not automatically a security vulnerability. Require an explicit data-access boundary or deletion guarantee and an unauthorized reader or later operation.
- Use confirmed for complete source-visible lineage and bounded dummy-tenant tests. Use needs_validation when external storage policy, retention, CDN behavior, replica lag, or backup access is unavailable.
```

## Tenant and object-isolation attack classes

### Missing tenant or owner enforcement (BOLA)

Map direct references to OWASP API1:2023 Broken Object Level Authorization. A read, update, delete, list, count, or bulk query identifies an object without binding it to the authenticated tenant or owner, or trusts request body fields to supply that identity. Compare direct lookup, nested relationship, background worker, admin, import, and legacy paths.

### Object property exposure and mass assignment (BOPLA)

Map property filtering to OWASP API3:2023 Broken Object Property Level Authorization. Verify that sensitive tenant fields, billing state, internal roles, and foreign tenant keys cannot be updated via mass assignment or retrieved via uncurated database serialization.

### Native database Row-Level Security vs application scopes

Evaluate whether data isolation relies entirely on error-prone application query scopes (e.g. ORM default scopes, `unscoped` bypasses, raw SQL queries) rather than database-enforced controls like PostgreSQL Row Level Security with `FORCE ROW LEVEL SECURITY`. Identify execution contexts where tenant ID context variables are uninitialized or overridden by connection pooling.

### Composite-key and namespace collisions

Cache keys, object paths, database uniqueness constraints, search document IDs, temporary files, or deduplication keys omit tenant or environment markers. Two principals can overwrite or retrieve the same logical key even though application records carry separate owners.

### Policy and query disagreements

Row-level policies, ORM default scopes, authorization filters, and raw bypass clients apply different predicates. Check joins, aggregates, aliases, views, transactions, service clients, and error paths where tenant context is missing.

### Blob and signed-reference overreach

Object keys, attachment IDs, version IDs, shared links, or signed URLs permit operations or namespaces beyond the issuing principal access, or remain valid after the underlying ACL changes. Bind operation, exact object version, audience, expiry, and tenant.

## Derived-data and disclosure attack classes

### Search, cache, and index ACL drift

A primary record ACL or lifecycle changes without invalidating a searchable, cached, embedded, thumbnail, RSS, preview, or index copy. Validate filtering at retrieval time as well as document ingestion and invalidation.

### Analytics, logs, traces, and diagnostics as alternate readers

Private content or credentials are emitted into systems with broader access, longer retention, or tenant mixing. Confirm the data class and realistic reader; field names, public identifiers, and operator-only content under intended policy are not enough.

### Enumeration and aggregate oracles

Counts, filters, ordering, errors, unique constraints, timings, notification behavior, or existence checks disclose protected object or account state. Require a concrete confidential predicate and observable distinction, not general response variance.

## Export, backup, restore, and migration attack classes

### Export and backup scope expansion

An export, snapshot, portability package, report, or backup includes other tenants, inaccessible object fields, soft-deleted data, secret values, or history above the requester access. Check per-item authorization after selection and authorization to download the final artifact.

### Import and restore authority expansion

Restore and import routines bypass owner, schema, ACL, uniqueness, or validation rules, overwrite existing resources, or recreate records in a tenant the requester cannot write. Validate archive contents as untrusted and authorize the resulting operation rather than trusting prior provenance.

### Migration default and ownership confusion

Old records lack tenant, ACL, or lifecycle fields, incompatible IDs collide, or partial rollout makes new and old readers apply different defaults. Review backfill, dual-read and write, compatibility, rollback, and resumed-migration paths.

### Backup and replication boundary drift

Encryption keys, storage accounts, cross-region replicas, restoration environments, or support snapshots have broader identity or tenant scope than primary data. Source can confirm only in-repo policy; hosted access and retention require `needs_validation`.

## Deletion, revocation, and lifecycle attack classes

### Soft-delete and tombstone bypass

Direct lookup, search, relation traversal, object links, background processors, or restore operations ignore the lifecycle predicate and return or act on a deleted or revoked record. Check whether soft-deleted identifiers can be re-registered before all references are gone.

### Cryptographic erasure under NIST SP 800-88

Audit whether tenant data destruction implements cryptographic erasure (crypto-shredding) where per-tenant or per-object encryption keys are securely discarded upon deletion. Without crypto-shredding, verify how multi-tenant backups, snapshots, and replicas purge deleted data within contractual retention windows.

### Stale authorization and derived copy use

Membership removal, ACL update, consent withdrawal, secret revocation, or role downgrade does not invalidate sessions, caches, subscriptions, jobs, or materialized data that continue to authorize future operations.

### Retention and queued-work overrun

Deletion completes in primary storage while queued processors, retries, exports, analytics, or generated artifacts recreate or retain the data beyond the promised boundary. Find idempotent deletion and tombstone propagation.

## Universal moves

- Pick one protected record and draw primary write, query, cache, index, event, export, backup, deletion, and restore paths. Mark principal and tenant at every edge.
- Compare two dummy tenants through the same local service methods, then repeat after ACL change, deletion, account switch, and restore. Do not use real user data.
- Start at bypass clients, background jobs, migrations, global uniqueness, and cache keys. These paths commonly omit request-scoped identity that interactive endpoints carry.

## Validation rules

1. Name attacker or lower-trust principal, protected data or state, affected owner or tenant, alternate copy or operation, and unauthorized disclosure or mutation.
2. Cite both intended source-of-truth policy and the path that omits or disagrees with it. Confirm another layer does not enforce the same tenant or lifecycle condition.
3. Use local dummy tenants and non-sensitive fixtures to prove cross-scope access or stale lifecycle behavior. Stop at the minimum observable record or operation.
4. If external cache, object storage, replicas, analytics, backup, or retention policy is required, classify `needs_validation` and state the owner-observed check.
5. Return `confirmed` only with complete lineage and concrete boundary impact. Return `needs_validation` with the exact unresolved storage, ACL, invalidation, retention, or restore fact.
