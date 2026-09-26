---
name: s13n
description: Use when standardizing inconsistent code patterns across a repository, resolving architectural divergence, or installing linter guards. Don't use for deep module redesign or single-file refactoring.
allowed-tools: Read Write Edit Glob Grep Bash
---

# Standardization (s13n)

Normalize diverging patterns across a repository into a single canonical architecture protected by automated linter guards.

## Governing principle

Never silently select a canonical variant without verified repository evidence or user authorization. The majority pattern is evidence, not authority. A minority pattern may represent an active architectural migration. Normalizing to the majority without checking destroys intentional migrations.

## Precedence hierarchy

Resolve convention questions against this hierarchy, evaluated highest to lowest:

| Rank | Source | Authority | Action |
| --- | --- | --- | --- |
| 1 | Repository convention documents (`AGENTS.md`, `CLAUDE.md`, `CODEBASE.md`) | Absolute | Apply documented standard. Never ask user to vote against their own docs |
| 2 | Enforced tooling configuration (`.editorconfig`, `eslint.config.js`, `ruff.toml`) | Absolute | Apply configured rules directly |
| 3 | Dominant unambiguous pattern in code (such as 47 out of 48 files) | Tentative | Recommend majority but check git history for intentional migrations |
| 4 | User confirmation | Authoritative | Ask via structured choice when patterns conflict |
| 5 | Per-language standards in `references/std-*.md` | Advisory | Baseline default when the repository lacks conventions |

## Reference modules

Load relevant reference files on demand based on repository language and scope:

| Concern | Reference File |
| --- | --- |
| Divergence taxonomy and probes | [references/divergence-taxonomy.md](references/divergence-taxonomy.md) |
| Architecture and file layout | [references/std-structure.md](references/std-structure.md) |
| TypeScript and JavaScript | [references/std-ts.md](references/std-ts.md), [references/std-js.md](references/std-js.md) |
| Python | [references/std-python.md](references/std-python.md) |
| Go | [references/std-go.md](references/std-go.md) |
| PHP | [references/std-php.md](references/std-php.md) |
| Rust | [references/std-rust.md](references/std-rust.md) |
| Java and C# | [references/std-java.md](references/std-java.md), [references/std-csharp.md](references/std-csharp.md) |
| SQL, Shell, HTML, CSS | [references/std-sql.md](references/std-sql.md), [references/std-shell.md](references/std-shell.md), [references/std-html.md](references/std-html.md), [references/std-css.md](references/std-css.md) |
| Configuration, Docs, Git | [references/std-yaml-json.md](references/std-yaml-json.md), [references/std-docs.md](references/std-docs.md), [references/std-git.md](references/std-git.md) |

## Workflow

### Phase 1. Reconnaissance

Inspect existing repository conventions and tool configurations before modifying code:

```bash
ls -la AGENTS.md CLAUDE.md CODEBASE.md CONTRIBUTING.md .editorconfig 2>/dev/null
ls -la .eslintrc* eslint.config* .prettierrc* ruff.toml pyproject.toml .golangci.yml 2>/dev/null
```

Determine primary languages and file distributions:

```bash
find . -type f -not -path './.git/*' -not -path '*/node_modules/*' -not -path '*/vendor/*' \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -15
```

If the repository is mid-migration (indicated by `TODO(migrate)` comments or dual implementations), clarify migration intent before touching files.

Completion criterion. An inventory of repository convention files, active formatters, and language distribution counts.

### Phase 2. Detect divergences

Probe codebase concerns systematically. Consult [references/divergence-taxonomy.md](references/divergence-taxonomy.md) for full taxonomy:

```bash
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "require\(|from ['\"]|import .* from" . | head -30
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "\.then\(|await |async function" . | head -30
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "throw new|raise |return Err|panic\(" . | head -30
```

Record each divergence with exact file counts and sample locations. Check git history for recent changes in minority variants to distinguish intentional modernizations from accidental deviations.

Completion criterion. A catalog of identified divergences mapping file counts and sample snippets to each variant.

### Phase 3. Resolve canonical variants

Resolve canonical patterns using the Precedence Hierarchy. When rank 1 and rank 2 answer the question, proceed directly to normalization.

When code patterns conflict and rank 1 or 2 does not specify a rule, present options to the user:
- State the concern concisely in one line.
- Present each variant with its file count and sample snippet.
- Highlight the recommended variant with clear rationale.
- Highlight counter-signals such as newer modules or recent commit ranges.
- Cap questions to at most four major divergences per round.

Completion criterion. A confirmed canonical variant selected via convention documents, tool configs, or explicit user sign-off.

### Phase 4. Normalize

Execute normalization in two distinct stages:

1. Mechanical normalization. Run project formatters and linters first:

```bash
# JS/TS
npx prettier --write . && npx eslint . --fix

# Python
ruff format . && ruff check . --fix

# Go
gofmt -w . && goimports -w .
```

2. Semantic normalization. Update call sites, imports, and error handling manually:
- Replace losing variants with the canonical pattern.
- Update every caller site across the codebase.
- Update associated test cases and documentation.
- Add an automated linter guard (such as `no-restricted-imports` in ESLint or `banned-api` in Ruff) to prevent regressions.

Never touch generated files, lockfiles, or external vendor dependencies (`vendor/`, `node_modules/`, `dist/`).

Completion criterion. All instances of the deprecated variant replaced across the codebase, with automated linter guards installed.

### Phase 5. Verify

Confirm the codebase is healthy and consistent:
- Project builds cleanly with zero errors.
- Test suite passes completely.
- Linter passes with new guard rules enabled.
- Repository search for the eliminated variant returns zero matches outside documented exemptions:

```bash
grep -rn "disallowed-pattern" --exclude-dir={node_modules,.git,dist,build,vendor} . && echo "FAIL" || echo "CLEAN"
```

Completion criterion. Clean build exit code, passing test suite, and grep confirmation showing zero remaining deprecated occurrences.

## Common mistakes

| Mistake | Consequence | Correct Approach |
| --- | --- | --- |
| Selecting majority pattern automatically | Destroys ongoing architectural migrations | Verify git history and confirm with user when ambiguous |
| Asking questions answered by `AGENTS.md` | Wastes user attention and invites documentation drift | Inspect convention documents first |
| Hand-editing formatting discrepancies | Introduces typos and contradicts formatter rules | Run project formatter directly |
| Modifying definitions without updating callers | Breaks builds and unit tests | Search repository for all caller references |
| Omitting automated linter guard | Divergence returns in subsequent pull requests | Add linter restriction rule to config |
| Normalizing third-party or generated directories | Edits get overwritten on subsequent builds | Exclude vendor and build output paths |
