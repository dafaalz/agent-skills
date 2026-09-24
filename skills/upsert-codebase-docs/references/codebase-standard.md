# CODEBASE.md construction standard

Structural rules, compact notation standards, and templates for assembling `CODEBASE.md`.

## Core requirements

Keep `CODEBASE.md` under 250 lines. This file provides an architectural reference for AI agents and human contributors. It records durable architectural facts, data flow paths, structural layout, and database relationships.

When any subsystem or domain description exceeds 30 lines, move the full breakdown to `.agents/references/<domain>.md` and leave a context pointer in `CODEBASE.md`.

## Section anatomy

Every `CODEBASE.md` file must contain these six sections in order:

### 1. Document title and staleness rule
State the codebase name and include the mandatory staleness guardrail with current ISO date.

```markdown
# Backend Codebase Reference (Laravel 13 API)

Deep factual reference for AI agents and developers. **Last verified: 2026-09-24.**
If you modify code that alters architecture, models, routes, or services documented here, update this file in the same change.
Consult [`AGENTS.md`](./AGENTS.md) for working instructions and operational boundaries.

> If this file is older than 4 weeks, verify schema and routes against `database/migrations/` and `routes/api.php` before trusting it.
```

### 2. Technology stack matrix
Present a Markdown table classifying each technology layer, specific version, and architectural role. Enclose in synchronization delimiters:
```markdown
<!-- BEGIN AUTO GENERATED: STACK_MATRIX -->
| Layer | Technology | Details |
|---|---|---|
| Framework | Laravel 13 | PHP 8.3+, Strict Types enabled |
| Database | PostgreSQL 16 | Relational storage, strict foreign keys |
| Auth | Laravel Sanctum | Bearer token API authentication |
| Pattern | Service-Repository | Thin Controllers, Fat Services, API Resources |
<!-- END AUTO GENERATED: STACK_MATRIX -->
```

### 3. Architecture data flow (ASCII representation)
Map the end-to-end lifecycle of an incoming request through the layers down to storage and back out to client response:

```text
HTTP Request (Frontend Client)
  → routes/api.php (Route declaration + middleware guards: auth, role)
  → app/Http/Middleware/ (RBAC, DecryptRequest)
  → app/Http/Controllers/ (Thin HTTP dispatcher)
      → FormRequest (Validation and authorization)
      → Service Layer (Business rules and DB transactions)
          → Eloquent Models (Query database, relations, scopes)
          → PostgreSQL Database
      → API JsonResource (Filter and transform response attributes)
      → ResponseService (Wrap into standard JSON envelope)
  → HTTP JSON Response to Client
```

### 4. Annotated directory layout
Display the essential directory tree with functional annotations explaining the responsibility of each folder. Exclude generated directories (`node_modules`, `vendor`, `.git`, `build`, `dist`):

```text
app/
├── Http/
│   ├── Controllers/Api/           # Thin dispatchers organized by role (Admin, HRD)
│   ├── Middleware/                # RBAC guards and request processors
│   ├── Requests/                  # Form Request validation rules
│   └── Resources/                 # JSON API response transformers
├── Models/                        # Eloquent models and entity relationships
└── Services/                      # Pure business logic and transactions
```

### 5. Compact schema notation
Do not copy full SQL DDL or verbose migration dumps. Use single-line entity notation listing primary keys, foreign keys, and critical domain attributes:
```markdown
<!-- BEGIN AUTO GENERATED: DATABASE_SCHEMA -->
users (id PK, email unique, password_hash, role enum[admin|user], is_active bool)
profiles (id PK, user_id FK -> users.id, full_name, phone nullable)
posts (id PK, author_id FK -> users.id, title, slug unique, content, status enum[draft|published])
comments (id PK, post_id FK -> posts.id, user_id FK -> users.id, body)
<!-- END AUTO GENERATED: DATABASE_SCHEMA -->
```
If the schema contains more than 15 tables, summarize the top 10 core tables here and place the complete table list in `.agents/references/database-schema.md`.

### 6. Compact routing matrix
Do not enumerate every repetitive sub-route. Summarize routes in a compact table showing HTTP method, path pattern, handler class, and middleware guards:
```markdown
<!-- BEGIN AUTO GENERATED: ROUTING_MATRIX -->
| METHOD | PATH | HANDLER | GUARDS |
|---|---|---|---|
| POST | /api/v1/auth/login | AuthController@login | guest |
| POST | /api/v1/auth/logout | AuthController@logout | auth:sanctum |
| GET | /api/v1/posts | PostController@index | auth:sanctum, role:all |
| POST | /api/v1/posts | PostController@store | auth:sanctum, role:admin |
| GET,PUT,DELETE | /api/v1/posts/{id} | PostController | auth:sanctum, role:admin |
<!-- END AUTO GENERATED: ROUTING_MATRIX -->
```
If routes exceed 25 endpoints, group related CRUD resources into single rows or move full endpoint documentation to `.agents/references/routes.md`.

## Subsystem documentation pointer rules

When a repository contains rich features requiring deep explanation:
1. Create a dedicated markdown document inside `.agents/references/`.
2. Name the file cleanly in kebab-case, such as `.agents/references/auth-flow.md` or `.agents/references/audio-engine.md`.
3. Add a dedicated pointer row or subsection in `CODEBASE.md`:
```markdown
## Subsystems and deep references
- [auth-flow.md](file://.agents/references/auth-flow.md) covers authentication and session lifecycle.
- [audio-engine.md](file://.agents/references/audio-engine.md) covers audio DSP and synthesis engine.
- [database-schema.md](file://.agents/references/database-schema.md) covers complete database schema catalog.
```
