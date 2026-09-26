---
name: upsert-codebase-docs
description: Use when creating or updating AGENTS.md and CODEBASE.md documentation files for a project, auditing documentation drift against git changes, or bootstrapping agent instructions for new repositories. Don't use for writing user guides, product changelogs, or external API documentation.
---

# Upsert codebase docs

Create and maintain high signal documentation files for AI coding agents and developers. This skill governs the generation and incremental synchronization of `AGENTS.md` and `CODEBASE.md`.

## Principles and constraints

1. Budget limits. `AGENTS.md` must not exceed 150 lines. `CODEBASE.md` must not exceed 250 lines.
2. Progressive disclosure. Move subsystem specifications exceeding 30 lines to `.agents/references/` rather than cluttering root files.
3. Unslop and punctuation rules. Zero em dashes, zero en dashes, and zero hyphens acting as dashes. Restrict colons to introducing lists, tables, or code blocks. Never use mid-sentence colons or pseudo-labels.
4. Positive operational framing. Pair every negative constraint immediately with a concrete positive action.
5. Single source of truth. Rely on environment files and live terminal commands rather than copying static code into documentation.

## Workflow

Follow these six steps in sequence.

### Step 1. Workspace topology and stack profiling

Inspect the target repository to determine structure and technology stack before creating or editing files.

1. Execute the topology detection script to profile manifests:
   ```bash
   bash scripts/scan-topology.sh .
   ```
2. Classify repository topology using `references/topology-detection.md`:
   - Single-root application. One primary manifest at root (`composer.json`, `package.json`, or `Cargo.toml`). Generates root `AGENTS.md` and `CODEBASE.md`.
   - Multi-tier decoupled architecture. Distinct manifests inside subdirectories like `backend/` and `frontend/`. Generates root orchestrator `AGENTS.md` alongside dedicated `AGENTS.md` and `CODEBASE.md` pairs inside each active subsystem.
   - Monorepo workspace. Monorepo tools managing multiple packages under `packages/` or `apps/`.
3. Inspect stack manifests and environment files using `references/stack-profilers.md` to identify:
   - Language and runtime version.
   - Core framework and active database driver (prioritizing `.env` over `.env.example`, verified via runtime CLI commands where available).
   - Test runners, linters, and build tooling.
   - Primary packages and third-party integrations.

Completion criterion. A verified inventory of repository topology, active runtime versions, and manifests recorded on disk with zero unverified assumptions.

### Step 2. Operational mode selection and ambiguity resolution

Determine whether to run greenfield generation or incremental drift synchronization, and resolve manifest anomalies.

1. Inspect target directories for existing documentation files:
   - Mode A (Greenfield bootstrap). Target files do not exist. Extract the full project profile and generate initial files using standard templates.
   - Mode B (Incremental drift sync). Target files exist. Audit current code against documentation using `references/drift-heuristics.md` to update stale sections without overwriting manual developer rules.
2. If Mode B is selected, check for drift indicators:
   - Migration files added after the last verified date in `CODEBASE.md`.
   - New routes, controllers, or services introduced in git diff.
   - Dependency additions in package manifests.
   - Database engine or connection mismatches between active `.env` or runtime CLI and the documented stack.
   - Staleness rule expiry exceeding 4 weeks since the recorded verification date.
3. Resolve profile ambiguities:
   - If conflicting manifests exist, such as both npm and bun lockfiles, formulate a clarifying question with concrete options and a clear recommended choice.
   - Confirm active branch conventions and staging rules before drafting instructions.

Completion criterion. Target mode confirmed and logged with exact file paths targeted for creation or patching.

### Step 3. User alignment gate

Present the discovery summary to the user and secure confirmation before modifying or generating files on disk.

1. Present the structured discovery brief:
   - Identified repository topology and targeted documentation files.
   - Detected runtime, framework, database, and test commands.
   - Proposed operational mode (Mode A greenfield bootstrap or Mode B incremental drift sync).
   - Core non-default conventions to encode in `AGENTS.md`.
2. Secure explicit confirmation:
   - Wait for user validation or adjustments before proceeding to file drafting.
   - Never write or overwrite documentation files before securing user approval.

Completion criterion. Explicit user approval recorded for the proposed documentation plan.

### Step 4. Drafting AGENTS.md

Assemble operational instructions in `AGENTS.md` strictly within the 150-line limit. Consult `references/agents-standard.md` for exact section anatomy.

1. In Mode A, write the document with these mandatory sections:
   - Heading stating repository identity and role.
   - Project Context covering runtime, framework, database, and timezone.
   - Documentation Map pointing to `CODEBASE.md` and any deep files in `.agents/references/`.
   - Commands Cheatsheet with verified shell commands for dependencies, dev server, tests, and linting.
   - Critical Rules stating absolute boundaries. Pair every prohibition with an explicit allowed action. Include environment security, dependency directory locks, and migration preservation.
   - Non-Default Conventions listing framework gotchas and patterns AI models typically violate.
   - Git Workflow and Definition of Done requiring terminal test verification before completion.
2. In Mode B, preserve existing custom guidelines:
   - Retain all manual developer instructions and custom rules.
   - Update only commands or conventions that changed based on manifest or script updates.
   - If an existing file exceeds 150 lines, extract secondary domain notes into `.agents/references/` rather than deleting developer guidance.
   - Ensure the total file length remains at or below 150 lines.

Completion criterion. `AGENTS.md` written to disk with verified commands, zero dangling negative rules, and total line count not exceeding 150 lines.

### Step 5. Drafting CODEBASE.md

Assemble technical architectural reference in `CODEBASE.md` strictly within the 250-line limit. Consult `references/codebase-standard.md` for notation rules.

1. Write or update core sections:
   - Verification metadata and staleness rule with current ISO date (`Last verified: YYYY-MM-DD`).
   - Technology Stack table listing layer, technology, and operational boundaries.
   - Architecture Data Flow diagram using clean ASCII text showing request-to-response paths.
   - Annotated Directory Layout highlighting key feature directories and functional ownership.
   - Compact Schema Notation for database entities (one line per table showing primary keys, foreign keys, and critical columns).
   - Compact Routing Matrix mapping essential HTTP verbs, endpoints, handlers, and guards.
2. In Mode B, execute delimited synchronization:
   - Locate auto-generated blocks bounded by `<!-- BEGIN AUTO GENERATED: <SECTION> -->` and `<!-- END AUTO GENERATED: <SECTION> -->`.
   - Refresh content inside the delimiters with latest code state while leaving surrounding narrative untouched.
   - Update the verification timestamp to the current date.
3. Manage subsystem sprawl:
   - Ensure directory `.agents/references/` exists by running `mkdir -p .agents/references`.
   - If a single domain requires more than 30 lines of technical description, move it into `.agents/references/<domain>.md` and leave a context pointer in `CODEBASE.md`.

Completion criterion. `CODEBASE.md` written to disk with updated staleness date, compact notation, delimited blocks, and total line count not exceeding 250 lines.

### Step 6. Verification and unslop audit

Audit generated files against technical standards before concluding the task.

1. Run deterministic line count validation:
   ```bash
   wc -l AGENTS.md CODEBASE.md
   ```
   Confirm `AGENTS.md` is 150 or fewer lines, and `CODEBASE.md` is 250 or fewer lines.
2. Run the formatting and style audit:
   - Verify zero occurrences of em dashes, en dashes, or hyphens acting as dashes.
   - Verify colons appear only before explicit lists, tables, or code blocks.
   - Verify sentence case headings without decorative emojis.
   - Search for and eliminate banned AI vocabulary using substitution tables in `references/agents-standard.md`.
3. Run link and path verification:
   - Verify every file path and command mentioned exists and functions on disk.

Completion criterion. Both files satisfy all audit criteria with zero violations recorded.

## Quick audit checklist

| Check | Passing condition |
|---|---|
| User alignment gate | Findings and target files presented to user and approved before editing files |
| Line budget | `AGENTS.md` <= 150 lines, `CODEBASE.md` <= 250 lines verified with `wc -l` |
| Progressive disclosure | Subsystems exceeding 30 lines placed in `.agents/references/` |
| Delimiters | Auto-generated sections in `CODEBASE.md` wrapped in HTML comment bounds |
| Style and punctuation | Zero em dashes, zero mid-sentence colons, sentence case headings |
| Concrete rules | Every negative constraint paired with an immediate positive action |
| Truth grounding | All paths, commands, and schemas match repository reality |
