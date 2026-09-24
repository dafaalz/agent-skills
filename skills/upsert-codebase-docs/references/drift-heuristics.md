# Documentation drift heuristics

Techniques and signals for auditing codebase documentation drift and applying safe incremental updates.

## Drift signals

Documentation drifts when code implementation mutates while documentation remains static. Monitor these six signals to determine whether `CODEBASE.md` or `AGENTS.md` require updates:

### 1. Asymmetric git diff
Examine recent git commits or working tree status:
```bash
git diff --name-only HEAD~5..HEAD
```
If commits modify core business files (`app/Http/Controllers/`, `src/features/`, `app/Models/`, `routes/`) without any corresponding commit touching `CODEBASE.md`, documentation drift is present.

### 2. Migration and schema drift
Inspect the database migration directory:
- For Laravel, check files in `database/migrations/`.
- For Django, check `migrations/` directories.
- For Prisma, check `prisma/schema.prisma` or `prisma/migrations/`.
- For Go and Rust, check `migrations/` or schema definition files.

If any migration file has a timestamp newer than the `Last verified: YYYY-MM-DD` date in `CODEBASE.md`, the entity schema in `CODEBASE.md` must be refreshed.

### 3. Route matrix divergence
Inspect route declaration files (`routes/api.php`, `src/route.tsx`, `config/routes.rb`). If new endpoints or page routes exist that are absent from the Compact Routing Matrix in `CODEBASE.md`, the routing table requires synchronization.

### 4. Manifest and dependency drift
Compare package manifests (`composer.json`, `package.json`, `Cargo.toml`) against the Technology Stack table in `CODEBASE.md`. New major libraries, upgraded framework versions, or added linters must be reflected in both `AGENTS.md` (commands) and `CODEBASE.md` (stack table).

### 5. Staleness rule expiration
Parse the verification metadata at the top of `CODEBASE.md`:
```markdown
Last verified: YYYY-MM-DD
```
If the elapsed time between the verified date and the current system date exceeds 28 days (4 weeks), trigger an automatic verification pass across database migrations, routes, and operational commands.

### 6. Environment and database configuration drift
Compare the active environment file (`.env`) and live runtime database status against the Technology Stack table in `CODEBASE.md`. If `DB_CONNECTION` in `.env` or runtime CLI output (such as `php artisan db:show`) differs from the documented database engine in `CODEBASE.md`, trigger an immediate database stack update. Never assume `.env.example` or existing documentation reflects the live connection when `.env` exists on disk.

## Safe incremental synchronization procedure

When updating existing documentation files, follow this non-destructive update procedure:

### 1. Identify synchronization delimiters
In `CODEBASE.md`, identify bounded comment markers:
- `<!-- BEGIN AUTO GENERATED: STACK_MATRIX -->`
- `<!-- BEGIN AUTO GENERATED: DATABASE_SCHEMA -->`
- `<!-- BEGIN AUTO GENERATED: ROUTING_MATRIX -->`

### 2. Isolate developer customizations
Content outside these comment boundaries represents custom architectural notes, subsystem explanations, and design rationale written manually by engineers. Never overwrite or rephrase text outside the delimiters during automated updates.

### 3. Replace delimited contents
Extract the latest state from the codebase (e.g. running `php artisan route:list`, reading new migrations, or inspecting `package.json`). Replace only the lines sitting between the matching `BEGIN` and `END` comments.

### 4. Refresh the verification timestamp
Update the header timestamp to the current ISO date:
```markdown
Last verified: 2026-09-24
```

### 5. Audit line length bounds
Verify that the updated `CODEBASE.md` remains at or below 250 lines. If new entities or routes caused the file to exceed 250 lines, extract secondary domains into `.agents/references/<domain>.md`.
