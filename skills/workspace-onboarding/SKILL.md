---
name: workspace-onboarding
description: Use when starting a new conversation, initializing work on a project, or onboarding to an unfamiliar workspace to discover the active stack, load rules, and establish execution constraints. Don't use for single-file edits in established sessions with known runtime environments.
---

# Workspace onboarding

Inspect repository context, verify environment configurations, and load governing rules before proposing solutions or running modifications.

## Workflow

Follow these four steps in sequence.

### Step 1. Stack and environment discovery

Identify the active runtime, framework, database, and package managers from files on disk and live runtime commands.

1. Inspect project manifests:
   - For PHP or Laravel projects, read `composer.json` to verify framework version, packages, and custom scripts.
   - For Node, React, Vue, or Next.js projects, read `package.json` to check dependencies, Tailwind versions, and test runners.
   - For Python projects, inspect `pyproject.toml`, `Pipfile`, or `requirements.txt`.
2. Inspect environment files with strict priority:
   - Read `.env` first whenever the file exists on disk. Use `.env.example` solely as a fallback template when `.env` is absent.
   - Check `DB_CONNECTION`, `DATABASE_URL`, port bindings, and external services in the active `.env`.
   - Never assume a default SQLite or MySQL database from template files when a configured `.env` file exists.
3. Validate active runtime database configuration:
   - Run framework introspection commands when available (such as `php artisan db:show` or `php artisan env` for Laravel) to verify the live database engine, host, and port.
   - Check test configuration files (such as `phpunit.xml`) to identify test specific overrides (such as in-memory SQLite) and avoid misclassifying test fixtures as the application database.
4. Record discovered stack properties including runtime version, framework, database driver, test runner, and linter.

Completion criterion. A verified inventory of the runtime, framework, database engine confirmed via active environment files or runtime CLI, and tooling without unverified assumptions.

### Step 2. Rule discovery and binding

Locate and read the applicable project guidelines and behavioral constraints.

1. Execute the deterministic rule discovery chain in this order:
   - First, check `.agents/rules/AGENTS.md` or `.agents/skills/` if present in the workspace.
   - Second, check `AGENTS.md`, `CODEBASE.md`, or `CLAUDE.md` in the project root.
   - Third, check global machine rules at `~/.gemini/config/rules/AGENTS.md`.
2. Bind rule constraints to the current session:
   - Adopt the persona, tone, and language defined in the discovered rules immediately from turn 1.
   - Respect boundaries on file manipulation and tool usage.

Completion criterion. Governing rule file identified and its constraints applied to the current context.

### Step 3. Unslop baseline calibration

Activate core unslop constraints across all human-facing responses.

1. Enforce zero filler openings. Do not use greeting tokens like "Halo", "Tentu", "Siap", or polite padding.
2. Ban em dashes, en dashes, and hyphens acting as dashes. Use commas, periods, or separate sentences.
3. Restrict colons to introducing lists, tables, or code blocks. Never use colons as connectors in the middle of sentences or as pseudo-labels.
4. Consult the full vocabulary substitution table in `unslop` only when generating detailed documentation, reviews, or prose.

Completion criterion. Response draft verified to contain zero filler phrases and zero dash defects.

### Step 4. Onboarding synthesis line

Deliver a single substantive verification statement before proceeding to task execution.

Format:
`[Stack: <framework> <version> | DB: <driver> | Tooling: <test_runner>, <linter> | Rules: <governing_file>]`

Follow immediately with the substantive technical answer or the next concrete investigation step. Never output empty confirmation filler.

Completion criterion. Exactly one dense status bracket output followed directly by task execution.
