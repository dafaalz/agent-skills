---
name: laravel
description: Use when building, modifying, reviewing, testing, or debugging Laravel applications, Eloquent queries, Artisan commands, Blade or Livewire components, Inertia adapters, Form Requests, migrations, or queue jobs.
---

# Laravel

Deterministic, test-driven workflows for Laravel applications.

## Overview

Build, refactor, and debug Laravel applications using native Artisan inspection and established repository conventions. Delegate architectural scoping to superpower skills, write tests before implementation, and verify changes with automated test suites and Pint formatting.

## Workflow

Follow these four steps in sequence:

### Step 1. Environment and runtime probe

Probe framework version, configuration, and database state before modifying application files:

1. Check the Laravel version and PHP runtime:
   ```bash
   php artisan --version
   ```
2. Detect the `laravel/boost` MCP server in available tools:
   - When `search-docs` is present, query it for version-specific documentation and package contracts.
   - When `search-docs` is absent, inspect framework behavior with native Artisan commands in `references/cli-introspection.md` or read vendor source directly.
3. Inspect affected database tables and route definitions:
   ```bash
   php artisan model:show <ModelName>
   php artisan route:list --name=<routeName>
   ```

Completion criterion. Command output confirms Laravel version, runtime settings, affected database schemas, and route mappings.

### Step 2. Convention mapping and reference selection

Audit sibling controllers, models, migrations, and test files for established project patterns. Match affected application layers to the reference index below:

| Concern | Reference guide |
|---|---|
| CLI introspection, runtime discovery, logs | `references/cli-introspection.md` |
| Eloquent queries, N+1 prevention, migrations, casts | `references/eloquent-and-database.md` |
| Controllers, Form Requests, route binding, resources | `references/routing-and-controllers.md` |
| Pest and PHPUnit tests, HTTP assertions, service fakes | `references/testing-patterns.md` |
| Authorization policies, SQL injection safety, mass assignment | `references/security-and-hardening.md` |

Completion criterion. Every modified file adheres to conventions observed in sibling files and matches its corresponding reference guide.

### Step 3. Implementation and boundary isolation

Apply minimal, isolated modifications using test-first development:

1. For new features or bug fixes, coordinate with the `tdd` skill to establish failing tests before writing production code.
2. For error diagnosis, coordinate with the `systematic-debugging` skill to inspect `storage/logs/laravel.log` and verify reproducing steps first.
3. Keep database queries inside Eloquent models, repositories, or query scopes, keeping Blade templates, Inertia controllers, and JsonResource classes free of queries.
4. Extract validation into Form Request classes and pass only `$request->validated()` into models.
5. Eager load relationships using `with()` or `loadMissing()` to eliminate N+1 queries.

Completion criterion. Implementation passes input validation, eagerly loads database relations, and keeps business logic separated from HTTP controllers.

### Step 4. Verification pass

Run automated verification commands before finishing work:

1. Execute the narrowest relevant test suite:
   ```bash
   php artisan test --filter=<TestClassOrMethod>
   ```
2. Check code style with Laravel Pint when installed in the repository:
   ```bash
   vendor/bin/pint --test
   ```
3. Inspect the git diff of modified files. Confirm that input passes through validation, migrations declare explicit constraints, and queries load relationships eagerly.

Completion criterion. Targeted tests pass with exit code 0 and Pint reports zero code style violations.

## Decision rules

- Audit sibling files before introducing patterns. Consistent project conventions take precedence over alternate architectures.
- Prefer native framework utilities over custom helper functions or external packages.
- Pass raw SQL through parameterized bindings with positional placeholders.
- Maintain CSRF protection, route middleware, and model authorization policies during tests. Fix test fixtures rather than disabling security middleware.
- Store credentials and private keys in `.env` and `config/` files. Application code must never contain hardcoded secrets.
