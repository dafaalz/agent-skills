# Operational risk and test runner reference

Reference rubrics and detection mappings for pull request authoring.

## 1. Merge danger decision classification

Evaluate operational risk before assembling pull request descriptions.

### Decision type

- Two-way door: Reversible cleanly with `git revert` with zero persistent state corruption, zero schema lock hazards, and zero data loss.
- One-way door: Destructive migrations, external API contracts, token invalidations, or live data backfills that require choreographed rollback procedures.

### Blast radius

- Low: Confined to internal utilities, isolated UI components, or behind disabled feature flags.
- Medium: Touches primary controllers, shared services, or active cache layers.
- High: Alters authentication, authorization boundaries, billing, or core relational schemas.

## 2. Deterministic test runner detection

Map repository lockfiles to verification test commands:

| Lockfile | Test command |
|---|---|
| `pnpm-lock.yaml` | `pnpm test` |
| `yarn.lock` | `yarn test` |
| `bun.lockb` | `bun test` |
| `package-lock.json` | `npm test` |
| `poetry.lock` | `poetry run pytest` |
| `uv.lock` | `uv run pytest` |
| `Pipfile.lock` | `pipenv run pytest` |
| `composer.lock` | `vendor/bin/phpunit` |
| `go.mod` | `go test ./...` |
| `Cargo.lock` | `cargo test` |
