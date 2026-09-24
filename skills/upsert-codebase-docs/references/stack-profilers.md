# Stack profiling heuristics

Commands and inspection patterns for discovering runtime, framework, database, and tooling across common software ecosystems.

## PHP and Laravel ecosystem

### Manifest and versions
- Read `composer.json` at project root or `backend/`.
- Identify framework version from `"laravel/framework"` or `"codeigniter4/framework"`.
- Check PHP runtime requirement in `"require": { "php": "..." }`.

### Operational commands
```bash
composer install                           # Install dependencies
php artisan serve                          # Dev server
php artisan test                           # Run test suite
php artisan migrate                        # Database migrations
php artisan route:list                     # Route overview
php artisan db:show                        # Inspect active database engine, connection, and tables
```

### Database and schema discovery
- Read `.env` first to inspect `DB_CONNECTION`, `DB_HOST`, `DB_PORT`, and `DB_DATABASE`. Use `.env.example` solely as a fallback template when `.env` is absent.
- Run `php artisan db:show` to verify the active runtime database engine and table counts directly.
- Inspect test configuration files (`phpunit.xml`) to identify in-memory test databases (such as SQLite `:memory:`) and avoid misidentifying test fixtures as the application database.
- Inspect migrations inside `database/migrations/`.
- Inspect model relationships inside `app/Models/`.

### Route discovery
- Inspect `routes/api.php` for API endpoints.
- Inspect `routes/web.php` for server-rendered routes.

---

## JavaScript, TypeScript, and React ecosystem

### Manifest and versions
- Read `package.json` at project root or `frontend/`.
- Identify package manager via lockfiles such as `bun.lockb`, `pnpm-lock.yaml`, `yarn.lock`, or `package-lock.json`.
- Check framework versions in `"dependencies"` such as `react`, `vue`, `svelte`, `next`, or `vite`.
- Check UI libraries such as `@shadcn/ui`, `tailwindcss`, or `@radix-ui/*`.

### Operational commands
Map commands from `"scripts"` section in `package.json`:
```bash
bun install                                # Or pnpm / npm / yarn
bun run dev                                # Development server
bun run build                              # Typecheck and production bundle
bun run lint                               # Linter validation
bun run test                               # Test runner (Vitest or Jest)
```

### Architecture and state discovery
- Check store directory such as `src/store/`, `src/slices/` (Redux Toolkit), or `src/stores/` (Zustand or Pinia).
- Check routing paths in `src/route.tsx`, `src/routes/`, `src/App.tsx`, or `app/` (Next.js App Router).
- Check feature modules in `src/features/` or `src/components/`.

---

## Rust and Tauri ecosystem

### Manifest and versions
- Read `Cargo.toml` at project root or `src-tauri/`.
- Check crate dependencies under `[dependencies]` such as `tauri`, `tokio`, `serde`, `sqlx`, or `rusqlite`.
- Check workspace members under `[workspace]`.

### Operational commands
```bash
cargo build                                # Compile debug binary
cargo test                                 # Run test suite
cargo check                                # Fast type and syntax validation
cargo clippy                               # Rust linter
cargo tauri dev                            # Start Tauri desktop app
```

### IPC and capability discovery
- Inspect `src-tauri/src/lib.rs` or `main.rs` for `tauri::generate_handler![...]`.
- Inspect `src-tauri/capabilities/` for permission declarations.

---

## Python ecosystem

### Manifest and versions
- Read `pyproject.toml`, `Pipfile`, or `requirements.txt`.
- Identify framework such as `django`, `fastapi`, or `flask`.
- Identify test runner such as `pytest` or `unittest`.
- Identify linter and formatter such as `ruff`, `black`, or `flake8`.

### Operational commands
```bash
poetry install                             # Or uv sync / pip install -r requirements.txt
pytest                                     # Run test suite
ruff check                                 # Fast linter validation
python manage.py runserver                 # Django dev server
uvicorn main:app --reload                  # FastAPI dev server
```
