---
name: upsert-codebase-docs
description: Use when creating or updating AGENTS.md, CODEBASE.md, and GLOSSARY.md documentation files for a project, auditing documentation drift against git changes, or bootstrapping agent instructions for new repositories. Don't use for writing user guides (use technical-writing), product changelogs, or external API documentation (use technical-writing).
allowed-tools: Read Write Edit Glob Grep Bash
---

# Upsert codebase docs

Create and maintain concise operational documentation files for AI coding agents and developers. This skill governs the generation and incremental synchronization of `AGENTS.md`, `CODEBASE.md`, and project domain definitions in `GLOSSARY.md`.

<HARD-GATE>
Write-Target Boundary. Modify only `AGENTS.md`, `CLAUDE.md`, `CODEBASE.md`, and `GLOSSARY.md`. Never modify application source code, configuration files, test suites, or database migrations while updating documentation.

Before modifying an existing `AGENTS.md`, write a timestamped backup to `.agents/state/upsert-codebase-docs/backups/AGENTS.md.<timestamp>.bak` and generate a diff. Require user confirmation before overwriting any existing documentation file. Never truncate an existing `AGENTS.md` without explicit user confirmation.
</HARD-GATE>

## Modes

Declare the active operating mode before executing any steps:
- Mode 1: Greenfield bootstrap (applies when target documentation files do not exist). Run Steps 1 through 6 sequentially.
- Mode 2: Incremental drift synchronization (applies when target documentation files exist). Run Steps 1 through 6 sequentially with backup creation and preservation of custom developer rules.
- Mode 3: Dry-run drift audit. Run Steps 1, 2, and 6 only. Emit `.agents/state/upsert-codebase-docs/drift-report.md` without modifying documentation files on disk.

## Principles and constraints

1. Budget limits. Keep `AGENTS.md` within 150 lines, and keep `CODEBASE.md` within 250 lines.
2. Progressive disclosure. Move subsystem specifications exceeding 30 lines to `.agents/references/` rather than cluttering root files.
3. Ubiquitous language. Maintain core business terms in `GLOSSARY.md` to prevent synonym cycling across agent sessions.
4. Anti-slop and punctuation. Zero em dashes, zero en dashes, and zero hyphens acting as dashes. Restrict colons to introducing lists, tables, or code blocks. Never use mid-sentence colons or pseudo-labels.
5. Positive operational framing. Pair every negative constraint immediately with a concrete positive action.
6. Single source of truth. Rely on environment files and live terminal commands rather than copying static code into documentation.

## Workflow

Follow these six steps in sequence:

### Step 1. Workspace topology and stack profiling

Inspect the target repository to determine structure and technology stack before creating or editing files:
1. Execute the topology detection script to profile manifests:
   ```bash
   bash scripts/scan-topology.sh .
   ```
2. Classify repository topology using `references/topology-detection.md`: single-root application, multi-tier decoupled architecture, or monorepo workspace.
3. Inspect stack manifests and environment files using `references/stack-profilers.md` to identify runtime versions, framework, database driver, test runners, and linters.

Completion criterion. `.agents/state/upsert-codebase-docs/topology.json` exists on disk with detected topology, runtime versions, and identified manifests.

### Step 2. Operational mode selection and ambiguity resolution

Determine whether to run greenfield generation, incremental drift synchronization, or dry-run audit:
1. Inspect target directories for existing documentation files to confirm active mode.
2. If Mode 2 is selected, check for drift indicators: new migrations, modified routes, added dependencies, or verification staleness exceeding 4 weeks. Consult `references/drift-heuristics.md`.
3. If Mode 3 is selected, compile drift findings into `.agents/state/upsert-codebase-docs/drift-report.md` and halt.
4. Resolve profile ambiguities through clarifying questions with concrete options.

Completion criterion. Target mode confirmed and logged in `.agents/state/upsert-codebase-docs/mode-plan.json` with exact target file paths.

### Step 3. User alignment and backup gate

Present discovery summary to the user, take backups of existing files, and secure confirmation before modifying files on disk:
1. When existing files are present, write timestamped backups to `.agents/state/upsert-codebase-docs/backups/`.
2. Present discovery brief: detected stack, target files, proposed commands, and core architectural patterns.
3. Pause for explicit user confirmation before writing changes to disk.

Completion criterion. User confirms discovery brief, and backup files exist in `.agents/state/upsert-codebase-docs/backups/` for all pre-existing documentation targets.

### Step 4. Drafting AGENTS.md

Assemble operational instructions in `AGENTS.md` strictly within the 150-line limit. Consult `references/agents-standard.md` for section anatomy:
1. In Mode 1, write mandatory sections: heading, project context, documentation map, commands cheatsheet, critical rules, non-default conventions, and definition of done.
2. In Mode 2, preserve existing custom guidelines:
   - Retain all manual developer instructions and custom rules.
   - Update only commands or conventions that changed based on manifest updates.
   - If an existing file exceeds 150 lines, extract secondary domain notes into `.agents/references/` rather than deleting developer guidance.
   - Maintain total file length within 150 lines.

Completion criterion. `AGENTS.md` written to disk with verified commands, zero dangling negative rules, and total line count within 150 lines.

### Step 5. Drafting CODEBASE.md and GLOSSARY.md

Assemble technical architectural reference in `CODEBASE.md` strictly within the 250-line limit. Consult `references/codebase-standard.md` for notation rules:
1. Write or update core sections: verification metadata, technology stack table, ASCII architecture data flow diagram, annotated directory layout, and domain model pointers.
2. In Mode 2, refresh content bounded by `<!-- BEGIN AUTO GENERATED: <SECTION> -->` and `<!-- END AUTO GENERATED: <SECTION> -->` delimiters while preserving manual prose. Update verification timestamp to current date.
3. Manage subsystem sprawl: move domain descriptions exceeding 30 lines into `.agents/references/<domain>.md` and leave context pointers in `CODEBASE.md`. Update `GLOSSARY.md` with core entity definitions.

Completion criterion. `CODEBASE.md` written to disk with updated staleness date, delimited blocks, and total line count within 250 lines.

### Step 6. Verification and unslop audit

Audit generated files against technical standards before concluding task:
1. Run deterministic line count validation:
   ```bash
   wc -l AGENTS.md CODEBASE.md
   ```
   Confirm `AGENTS.md` is 150 or fewer lines, and `CODEBASE.md` is 250 or fewer lines.
2. Run formatting and style audit: zero em dashes, zero en dashes, colons only before lists or code blocks, and zero banned vocabulary words.
3. Verify all documented file paths, scripts, and commands exist and execute on disk.

Completion criterion. Both files satisfy line budgets, `wc -l` output recorded in `.agents/state/upsert-codebase-docs/verification.txt`, and all paths verified on disk.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| UCD-1 | Bloated AGENTS.md | Allows AGENTS.md to sprawl past 150 lines | Context budget exhaustion on every agent session | Cap at 150 lines; delegate detail to `CODEBASE.md` |
| UCD-2 | Transient docs | Documents sprint tasks or temporary bug workarounds | Docs rot the moment the task is completed | Document only stable architecture and persistent patterns |
| UCD-3 | Rotting links | Uses relative links to files that get relocated | Breaks context navigation pointers on future sessions | Use root-relative paths and verify with `test -f` |
| UCD-4 | README cloning | Duplicates human marketing copy into AGENTS.md | Dilutes machine-executable signal with promotional fluff | Keep AGENTS.md focused strictly on commands and rules |
| UCD-5 | Silent overwrite | Replaces AGENTS.md without taking a backup or diff | Erases hard-won custom developer rules and invariants | Create timestamped backup and obtain user confirmation |
| UCD-6 | Codebase mutation | Modifies application source code during doc updates | Leaks documentation updates into functional systems | Restrict file modifications strictly to doc paths |

## Boundary isolation

Confine updates strictly to documentation files (`AGENTS.md`, `CODEBASE.md`, `GLOSSARY.md`). Never modify project source code, configuration files, or database migrations while updating documentation.

## Quick audit checklist

| Check | Passing condition |
|---|---|
| User alignment gate | Findings and target files presented to user and approved before editing files |
| Backup protection | Timestamped backups created in `.agents/state/` before modifying existing files |
| Line budget | `AGENTS.md` <= 150 lines, `CODEBASE.md` <= 250 lines verified with `wc -l` |
| Progressive disclosure | Subsystems exceeding 30 lines placed in `.agents/references/` |
| Domain terminology | Core entities mapped to `GLOSSARY.md` to prevent synonym cycling |
| Delimiters | Auto-generated sections in `CODEBASE.md` wrapped in HTML comment bounds |
| Anti-patterns | Anti-pattern table adheres to 5-column schema with stable IDs |
| Style and punctuation | Zero em dashes, zero mid-sentence colons, sentence case headings |
| Concrete rules | Every negative constraint paired with an immediate positive action |
| Truth grounding | All paths, commands, and pointers match repository reality |
