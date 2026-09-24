# AGENTS.md construction standard

Structural rules, section hierarchy, and templates for assembling `AGENTS.md`.

## Core requirements

Keep `AGENTS.md` under 150 lines. The purpose of `AGENTS.md` is to establish operational boundaries, command shortcuts, non-negotiable negative constraints, and verification criteria for AI agents and human developers. It is not an architecture encyclopedia.

## Section anatomy

Every `AGENTS.md` file must contain these seven sections in order:

### 1. Document title
Use a level 1 heading identifying the role and layer, such as `# Backend Agent Instructions (Laravel 13 API)`.

### 2. Project context
Provide a compact summary of one to two paragraphs covering framework, runtime, database, core libraries, and timezone.

```markdown
## Project context
Decoupled REST API for recruitment management.
Laravel 13, PHP 8.3+, PostgreSQL, Laravel Sanctum authentication. Timezone: Asia/Jakarta.
```

### 3. Documentation map
Provide direct markdown links to primary and secondary documentation:

```markdown
## Documentation map
- `CODEBASE.md`, deep technical reference on architecture, schema, models, and routes.
- `.agents/references/api-specs.md`, detailed endpoint specifications.
- `routes/api.php`, live route definitions.
```

### 4. Commands cheatsheet
List the most common shell commands needed for dependency management, local serving, testing, and database operations. Include token-saving tools if available on the system:

```bash
composer install                           # Install PHP dependencies
php artisan serve                          # Start dev server
php artisan test                           # Run test suite
php artisan migrate                        # Run pending migrations
```

### 5. Critical rules (negative bounds paired with positive actions)
State absolute boundaries clearly. Never use dangling prohibitions. Always pair the forbidden action with the required alternative:

| Bad dangling prohibition | Good paired constraint |
|---|---|
| Do not write logic in controllers. | Keep controllers thin as HTTP dispatchers; delegate all business logic to `app/Services/`. |
| Never edit migrations. | Never modify existing migration files; create new migration files for any schema updates. |
| Do not use any in TypeScript. | Define explicit interfaces or types for all component props and API payloads. |
| Never use git add all. | Stage files explicitly with `git add <file>` to avoid committing unintended edits. |
| Do not touch vendor. | Never edit files in `vendor/` or `node_modules/`; submit changes through package managers. |

### 6. Non-default conventions
Document project-specific deviations from framework defaults that AI models typically get wrong. Focus on custom base classes, response envelopes, form conventions, or transaction patterns.

### 7. Git workflow and definition of done
Define branch conventions, commit message formatting, and terminal verification criteria that must pass before marking any task complete.

## Sample golden template for single-root projects

```markdown
# Agent Instructions

## Project context
[Brief project description].
[Runtime, Framework, Database, Auth, Timezone].

## Documentation map
- `CODEBASE.md`, deep technical architecture, schema, and routing reference.
- `.agents/references/`, deep subsystem references.

## Commands cheatsheet
```bash
[Install command]
[Dev server command]
[Test command]
[Lint and build command]
```

## Critical rules (READ FIRST)
1. NEVER edit or commit `.env` files; update `.env.example` with mock defaults instead.
2. NEVER modify existing migration files; generate new migration files for schema changes.
3. NEVER edit files inside dependency directories (`vendor/`, `node_modules/`, `dist/`).
4. NEVER commit code without explicit user instruction.
5. ALWAYS enforce strict typing and check terminal output before declaring work done.

## Non-default conventions (Things You'd Get Wrong)
- Architecture pattern uses [Thin Controllers, Fat Services, API Resources].
- Wrap responses in standard JSON envelope `{ success, message, data, errors }`.
- Route custom exceptions through [Specific custom exceptions or HTTP error handlers].

## Git workflow
- Active working branch is `development`.
- Format commits following Conventional Commits (`feat`, `fix`, `refactor`, `test`, `docs`, `chore`).
- Stage only relevant files explicitly; avoid `git add .` or `git add -A`.

## Definition of done
A task is complete when:
1. Feature logic is isolated in dedicated service or module layers.
2. Form requests or schemas validate all incoming parameters.
3. Automated test suite passes with zero failures.
4. `CODEBASE.md` is updated if new entities, tables, or routes were added.
```

## Banned vocabulary substitution table

Apply these substitutions when drafting or reviewing agent documentation:

| Banned term | Concrete replacement |
|---|---|
| crucial / vital / paramount | required, mandatory, or state the exact failure condition |
| delve / dive deep | inspect, read, analyze |
| utilize / leverage | use |
| seamless / holistic | direct, integrated, unified |
| vibrant / breathtaking | delete or specify concrete metrics |
| landscape (abstract) | codebase, system, architecture |
| di mana / yang mana (calque) | restructure as separate sentences or direct relative clauses |
| adalah merupakan | adalah |
| sangat penting | wajib, atau jelaskan dampak kegagalan |
