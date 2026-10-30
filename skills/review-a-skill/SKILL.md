---
name: review-a-skill
description: Use when reviewing, auditing, benchmarking, or comparing agent skills against AgentSkills specifications, structural guidelines, or alternative implementations. Don't use for reviewing application source code (use code-review directly), running CI test suites (use testing-patterns directly), or writing end-user documentation (use technical-writing directly).
---

# Review a skill

Audit agent skills against AgentSkills standards, structural execution requirements, and anti-slop guidelines. Evaluate one candidate in isolation or benchmark it against a baseline to isolate sharp rules and close procedural loopholes.

<HARD-GATE>
Write-Target Boundary. Execute skill reviews in read-only mode. Write only to `.agents/state/review-a-skill/` or explicitly targeted evaluation reports. Do not modify tracked skill files, application source code, database schemas, or test suites during an audit.
</HARD-GATE>

## Modes

Declare the active operating mode before executing any steps:
- Audit mode (default): Inspect one target skill against structural and linguistic standards. Run Steps 1 through 4 sequentially and emit `.agents/state/review-a-skill/review.md`.
- Benchmark mode: Compare a candidate skill against a baseline skill across the seven dimensions. Run Steps 1 through 4 sequentially and emit `.agents/state/review-a-skill/benchmark-report.md`.

## Workflow

Follow the four steps in sequence.

### Step 1. Ingestion and mode determination

Identify review scope and intake candidate artifacts:
1. Load standards source. Read `unslop` and `writing-for-agents` from the first existing path among `.agents/skills/`, `$HOME/.agents/skills/`, `$HOME/.config/agents/skills/`, or the repository `skills/`. If either file is missing, fall back to the embedded rubric in `## Dimensional evaluation rubric` and record `standards_source: embedded`. Do not inspect session history or scratchpad files, and never audit from memory.
   Before invoking the linter, run `python3 skills/review-a-skill/scripts/lint_skill.py --self-test`. The self-test runs positive, negative, and edge fixtures for each active pattern (R13 anti-pattern tables, R16 evidence formats, R9 completion criteria). If `--self-test` fails, halt the audit and report the fixture name. A passing linter against a stale self-test is not evidence of compliance.
2. Load the target `SKILL.md` plus its `references/`, `scripts/`, `assets/`, and `examples/`. Check three boundary constraints:
   - Directory naming. Confirm directory name matches `name` in YAML frontmatter with 1 to 64 lowercase alphanumeric characters and single hyphens.
   - Context budget. Confirm main `SKILL.md` line count is strictly under 250 lines. The 250-line target is a hard limit; 250 or more lines fails the audit. Move documentation exceeding 100 lines into `references/`.
   - Executable integrity. Verify scripts declare explicit error handling, avoid unpinned dependencies, and contain zero unexplained constants.

Completion criterion. `.agents/state/review-a-skill/scope.json` exists on disk with `target_skill`, `mode`, `line_count`, and `standards_source`.

### Step 2. Structural and execution audit

Audit the skill against `writing-for-agents` structural requirements:
- Frontmatter routing. Check `description` for positive triggers ("Use when") and negative exclusions ("Don't use for"). Verify absence of internal workflow summaries. Require every negative exclusion to name the overlapping sibling skill it disambiguates against or provide an actionable direct command.
- Information hierarchy. Verify clean separation across primary sequential execution steps, secondary on-demand constraint tables, and tertiary external reference pointers.
- Workflow discipline. Verify steps run in strict numbered sequence with explicit mode handling declared before Step 1.
- Binary completion criteria. Every numbered step must terminate on a checkable, binary, and exhaustive completion criterion anchored to a tangible artifact path, exit code, or commit hash.
- Leading words and positive bounds. Confirm text recruits pre-training priors. Ensure every negative prohibition is paired immediately with an explicit positive action.
- Boundary isolation. Confirm explicit rules protect non-target domains, keeping code syntax, database schemas, and terminal commands untouched by stylistic guidelines.

Completion criterion. A written structural catalog at `.agents/state/review-a-skill/structural-findings.md` records all structural defects and missing criteria.

### Step 3. Anti-slop and linguistic scan

Audit skill prose against `unslop` guidelines:
- Banned vocabulary and puffery. Search for promotional filler, throat-clearing openings, and sycophantic closings. Replace them with plain words and direct verbs.
- Punctuation hygiene. Check for zero em dashes, zero en dashes, and zero hyphens acting as dashes. Confirm colons appear only before lists, tables, or code blocks, with zero mid-sentence colons and zero pseudo-labels.
- Mechanical grounding. Verify statements describe concrete system contracts, commands, metrics, or files instead of emotional impressions.
- Modern slop patterns. Flag redundant inline-header lists, mannered prose, philosophical aphorisms, personified code, and telegram-style over-compression.
- Localization patterns. For Indonesian text, eliminate calque relative clauses ("di mana"), pleonasms ("guna untuk"), and abstract metaphors.

Completion criterion. A linguistic log at `.agents/state/review-a-skill/linguistic-findings.md` records line numbers, offending phrases, slop categories, and replacements.

### Step 4. Synthesis, comparison, and grafting

Synthesize findings into an actionable evaluation report:
- Comparative evaluation table. In Benchmark mode, render a structured comparison table across the seven rubric dimensions below.
- Grounded verdict. Deliver a direct, blunt assessment in the opening sentence stating whether the candidate is better, worse, or mixed against baseline.
- Sharp rule grafting. Extract novel or sharper rules from candidate. Formulate drop-in replacement snippets that preserve existing structure while sealing loopholes.
- Automated lint verification. Run `python3 skills/review-a-skill/scripts/lint_skill.py <path-to-skill>` to execute AST, frontmatter, punctuation, and reference integrity checks.
- Final checklist verification. Audit proposed patch against quick audit checklist below.

Completion criterion. The review report is written to `.agents/state/review-a-skill/review.md` (in Audit mode) or `.agents/state/review-a-skill/benchmark-report.md` (in Benchmark mode), and `python3 skills/review-a-skill/scripts/lint_skill.py <path-to-skill>` exit code is recorded in `.agents/state/review-a-skill/review-verification.json`.

## Boundary isolation

Execute skill reviews in read-only mode. Never alter application source code, database schemas, project dependencies, or test configurations during a skill audit. Apply recommendations as proposed patches or review reports. When applying approved skill patches directly to meta-tooling under `skills/` or `.agents/`, record whether changes target a dedicated feature branch or execute under single-branch maintenance mode on `main`.

## Dimensional evaluation rubric

Consult these benchmarks when evaluating skills during Benchmark mode:

| Dimension | Passing standard | Failing tell |
|---|---|---|
| 1. Frontmatter and Discovery | Kebab-case name, positive triggers, negative exclusions, sibling disambiguation, description under 1024 characters | Vague summary, missing negative bounds, workflow leaks |
| 2. Workflow and State Machine | Sequential numbered steps, deterministic mode branch declared before Step 1 | Unordered bullets, missing mode branch, mode handling buried inside a step |
| 3. Completion Criteria | Binary and exhaustive at the end of every step. Anchored to a file path, an exit code, or a commit hash. Evaluated via `python3 skills/review-a-skill/scripts/lint_skill.py <skill>` (enforcing per-step binary termination and non-fuzzy allowlists across singular and plural forms) returning zero errors. | Fuzzy assertions like "ensure quality", "verify it works", "or equivalent", or criteria with no verifiable artifact. |
| 4. Language and Context Budget | Main file strictly under 250 lines, one-hop references with trigger conditions, bounded aggregate reference size | Monolithic text exceeding 250 lines, multi-hop reference chains |
| 5. Boundary Isolation | Explicit guards for code syntax, database schemas, and commands | Stylistic or persona bleed into functional code syntax |
| 6. Rule Granularity and Anti-Slop Depth | Zero banned words, zero dashes, colons only before lists or code, every ban paired with a positive replacement | Em dashes, colon reveals, puffery, unpaired bans |
| 7. Composability and Citation | Stable rule IDs or modular headings for clean external citation | Unreferenced prose blocks requiring full duplication |

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| RAS-1 | Monolithic file | Keeps deep domain reference manuals inside primary SKILL.md | Context budget blowout | Move domain reference manuals to `references/` |
| RAS-2 | Phantom sibling | Excludes imaginary skill names in frontmatter | Agent attempts to invoke non-existent skills | Reference real sibling skills or explicit CLI tools |
| RAS-3 | Budget contradiction | Allows 350-400 lines in step text while rubric caps at 250 | Inconsistent pass/fail audit results | Unify line limit strictly to 250 lines across all sections |
| RAS-4 | Disjunctive exit | Uses "or" in completion criterion (delivered or saved) | Downstream tools cannot locate the artifact | Anchor output to a single deterministic file path |
| RAS-5 | Sibling lock-in | Fails audit when unslop or writing-for-agents is absent | Breaks in minimal or trimmed skill distributions | Fall back to embedded rubric and record source |
| RAS-6 | Unchecked graft | Writes mutations directly into skills without diff or approval | Corrupts governing skills for subsequent sessions | Enforce two-phase propose/diff/confirm protocol |
| RAS-7 | Marker-vs-content conflation | Emits `grep -c '<HARD-GATE>'` as proof of closing findings about gate body content | Content findings remain open while marker count satisfies surface check | Findings concerning gate body or table entries require `sed -n '/<section>/,/<next-section>/p'` output as evidence |
| RAS-8 | Unscoped meta-claim | Asserts "100% compliant" without partitioning structural compliance from content compliance | Claims are unauditable across disparate audit depths | Format claim as: `<N>/<total> structural; <M>/<total> content with 1:1 raw diff evidence for batches <X>, <Y>` |

## Grafted rules

Apply these rules when grafting sharper behavior from candidate skills:
- [R7] Write-target hard gate. Require an explicit write-target boundary before any analytical workflow, and block mutations to production directories until the audit gate passes. Source, `brainstorming`.
- [R8] Sibling disambiguation. Require every negative frontmatter bound to name the overlapping sibling skill it disambiguates against. Source, external AgentSkills research.
- [R9] Deterministic artifact verification. Prefer mechanical verification over visual inspection. Source, `conventional-commit` and `verification-before-completion`.
- [R10] Up-down-up reversibility. Subject any state mutation to forward, rollback, and idempotent reapplication before approval. Source, `schema-migration`.
- [R11] Zero-paraphrase envelope. When delegating, pass the source spec verbatim inside a write-allowlist envelope and validate with `git diff --name-only`. Source, `executing-plans`.
- [R12] Interaction frequency gate. Disqualify a mechanism outright when its trigger rate exceeds the useful threshold, before inspecting implementation. Source, `ui-motion`.
- [R13] Five-column anti-pattern schema. Structure every anti-pattern table with exact headers: ID, Title, Pattern description, Why it fails, and Concrete fix. All cells must be non-empty and carry unique, stable IDs. Source, `review-a-skill`.
- [R14] Inverted critique order. State fatal flaws and boundary violations before any positive synthesis. Source, `web-advisor-prompt`.
- [R15] Banned performative agreement. Never emit praise or empty agreement. State file path, line number, and defect. Source, `code-review`.
- [R16] Evidence-Format Rule. Every claim of closed, verified, or passing for a finding must be accompanied by raw `sed -n '/<section>/,/<next-section>/p'`, raw `git diff <sha> -- <path>`, or raw `grep -n` output showing exact file path, line range, and changed content. Marker-presence counts (`grep -c`) close only findings concerning marker presence. Source, `review-a-skill`.
- [R17] Meta-Claim Scope Rule. Aggregate claims such as N skills at 100% compliance must partition the claim by dimension (structural, content, content-with-1:1-evidence) and batch scope. A single aggregate number without partitions is rejected. Source, `review-a-skill`.
- [R19] Standards-Drift Detection. When a validator rule threshold changes (such as column counts, rule IDs, or regex guards), re-scan all repository skills against the new standard before committing the validator. Record the threshold delta, list of migrated skills, and commit dependencies in the commit message. Claims of aggregate compliance do not carry over across standard increments without a fresh scan. Source, `review-a-skill`.

## Quick audit checklist

Run this check before delivering any skill review:

| Check | Passing condition |
|---|---|
| Prerequisite skills | Standards source loaded via `view_file` or embedded rubric activated |
| Mode selection | Audit mode or Benchmark mode identified |
| Frontmatter audit | AgentSkills schema, positive triggers, negative exclusions, sibling disambiguation |
| Context load | `SKILL.md` strictly under 250 lines, heavy manuals in `references/` |
| Completion criteria | Every step ends on a checkable, binary criterion anchored to a verifiable artifact |
| Anti-patterns | Anti-pattern table adheres to 5-column schema with stable IDs |
| Boundary isolation | Explicit guards for code and system invariants |
| Anti-slop scan | Banned vocabulary, dashes, colons, inline headers, mannered prose |
| Mechanical grounding | Every recommendation names a mechanical contract or metric |
| Actionable synthesis | Concrete drop-in patch snippets, not vague advice |
