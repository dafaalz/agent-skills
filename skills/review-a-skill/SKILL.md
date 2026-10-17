---
name: review-a-skill
description: Use when reviewing, auditing, benchmarking, or comparing agent skills against AgentSkills specifications, structural guidelines, or alternative implementations. Don't use for reviewing application source code, running CI test suites, or writing end-user documentation.
---

# Review a skill

Audit agent skills against AgentSkills standards, structural execution requirements, and anti-slop guidelines. Evaluate candidates in isolation or benchmark them against existing implementations to isolate sharp rules and close procedural loopholes.

## Workflow

Follow these four steps in sequence.

### Step 1. Ingestion and mode determination

Identify the review scope and intake candidate artifacts:

- Audit mode. Inspect a single target skill against structural and linguistic standards.
- Benchmark mode. Compare a candidate skill implementation against a baseline skill to determine architectural superiority and extract sharp rules.

Load prerequisite skills and target files before auditing:

1. Locate and read both `unslop` and `writing-for-agents` directly using `view_file` from the active skills root (such as `.agents/skills/`, `~/.agents/skills/`, `~/.gemini/config/skills/`, or the active repository `skills/` directory). Audit memory and state files only when explicitly requested; do not inspect session history or user scratchpad files during standard skill review. Inspect skill files directly and never audit from memory or secondary summaries.
2. Load the target `SKILL.md` along with disclosed files in `references/`, executables in `scripts/`, templates in `assets/`, and implementations in `examples/`. Check initial boundary constraints:
   * Directory naming. Confirm that the directory name matches the `name` field in the YAML frontmatter with 1 to 64 lowercase alphanumeric characters and single hyphens.
   * Context budget. Confirm that the main `SKILL.md` stays under 250 lines and that total secondary reference size stays bounded. Relocate documentation exceeding 100 lines into `references/` if needed.
   * Executable integrity. Verify that scripts declare explicit error handling, avoid unpinned external dependencies, and contain zero unexplained constants.

Completion criterion. Prerequisite skills `unslop` and `writing-for-agents` are loaded into context via `view_file`, target skills are ingested, the operating mode is determined, and directory naming, line budget, and executable integrity constraints are cataloged.

### Step 2. Structural and execution audit

Audit the skill against `writing-for-agents` structural requirements:

- Frontmatter routing. Check the `description` field for explicit positive triggers starting with "Use when" and negative exclusions starting with "Don't use for". Verify absence of internal workflow summaries that tempt models to skip the skill body. Confirm that manual-only skills declare the disable-model-invocation flag set to true. Require every negative exclusion to name the overlapping sibling skill it disambiguates against, and reject trivial non-sequiturs such as "Don't use for brewing coffee".
- Information hierarchy. Verify clean separation across the three tiers: primary sequential execution steps, secondary on-demand constraint tables, and tertiary external reference pointers.
- Workflow discipline. Verify steps run in strict numbered sequence. Check for explicit mode handling (such as Audit mode versus Edit mode) declared before Step 1 to prevent premature destructive rewrites.
- Binary completion criteria. Every numbered step must terminate on a checkable, binary, and exhaustive completion criterion anchored to a tangible artifact, such as a file path, test exit code 0, HTTP status code, or git commit hash. Flag vague completions like "ensure understanding" and cosmetic tautologies that name no verifiable state.
- Leading words and positive bounds. Confirm the text recruits pre-training priors with established leading words. Ensure every negative prohibition is paired immediately with an explicit positive action.
- Boundary isolation. Confirm explicit rules protect non-target domains, such as keeping code syntax, database schemas, and terminal commands untouched by stylistic guidelines.

Completion criterion. A written catalog documents structural findings, missing completion criteria, frontmatter defects, and boundary leaks.

### Step 3. Anti-slop and linguistic scan

Audit skill prose against `unslop` guidelines:

- Banned vocabulary and puffery. Search for promotional filler, throat-clearing openings, and sycophantic closings. Replace them with plain words and direct verbs.
- Punctuation hygiene. Check for zero em dashes, zero en dashes, and zero hyphens acting as dashes. Confirm colons appear only to introduce lists, tables, or code blocks, with zero mid-sentence colons and zero pseudo-labels.
- Mechanical grounding. Verify statements describe concrete system contracts, commands, metrics, or files instead of emotional impressions. Apply the portability test. If an instruction could appear unchanged in an unrelated project, anchor it with specific mechanics or cut it.
- Modern slop patterns. Flag redundant inline-header lists where a bold label merely repeats the following clause. Flag mannered prose, philosophical aphorisms, personified code, and over-compression that drops articles or uses telegram arrows.
- Localization and calque patterns. For Indonesian documentation, eliminate calque relative clauses like "di mana" or "yang mana", pleonasms like "guna untuk" or "adalah merupakan", and abstract metaphors.

Completion criterion. A linguistic finding log records line numbers, offending phrases, matched slop categories, and positive replacements.

### Step 4. Synthesis, comparison, and grafting

Synthesize findings into an actionable evaluation report:

- Comparative evaluation table. In Benchmark mode, render a structured comparison table across the seven rubric dimensions defined below.
- Grounded verdict. Deliver a direct, blunt assessment in the opening sentence stating whether the candidate is better, worse, or mixed compared to the baseline.
- Sharp rule grafting. Extract novel or sharper rules from candidate versions. Formulate drop-in replacement snippets that preserve existing structure while sealing loopholes, and apply the grafted rules below.
- Automated lint verification. Run `python3 skills/review-a-skill/scripts/lint_skill.py <path-to-skill>` to execute deterministic AST, frontmatter, punctuation, and reference integrity checks.
- Behavioral verification check. Confirm the candidate has passed empirical scenario testing across two consecutive subagent runs with zero skipped steps, with baseline failure modes and counter-instructions documented.
- Final checklist verification. Audit the candidate or proposed patch against the quick audit checklist below.

Completion criterion. The evaluation report delivers the dimensional comparison table or single-audit log, a direct verdict, and concrete drop-in patch recommendations.

## Boundary isolation

Execute skill reviews in read-only mode. Never alter application source code, database schemas, project dependencies, or test configurations during a skill audit. Apply recommendations as proposed patches or review reports.

## Dimensional evaluation rubric

Consult these benchmarks when evaluating skills during Benchmark mode:

| Dimension | Passing standard | Failing tell |
|---|---|---|
| 1. Frontmatter and Discovery | Kebab-case name, positive triggers, negative exclusions, sibling disambiguation, description under 1024 characters | Vague summary, missing negative bounds, workflow leaks |
| 2. Workflow and State Machine | Sequential numbered steps, deterministic mode branch declared before Step 1 | Unordered bullets, missing mode branch, mode handling buried inside a step |
| 3. Completion Criteria | Binary and exhaustive at the end of every step, anchored to a file path, exit code, or commit hash | Fuzzy assertions like "ensure quality" or criteria with no verifiable artifact |
| 4. Language and Context Budget | Main file under 250 lines, one-hop references with trigger conditions, bounded aggregate reference size | Monolithic text, multi-hop reference chains, unbounded secondary bloat |
| 5. Boundary Isolation | Explicit guards for code syntax, database schemas, and commands | Stylistic or persona bleed into functional code syntax |
| 6. Rule Granularity and Anti-Slop Depth | Zero banned words, zero dashes, colons only before lists or code, every ban paired with a positive replacement | Em dashes, colon reveals, puffery, unpaired bans |
| 7. Composability and Citation | Stable rule IDs or modular headings for clean external citation | Unreferenced prose blocks requiring full duplication |

## Grafted rules

Apply these rules when grafting sharper behavior from candidate skills:

- [R7] Write-target hard gate. Require an explicit write-target boundary before any analytical workflow, and block mutations to production directories until the audit gate passes. Source, `brainstorming`.
- [R8] Sibling disambiguation. Require every negative frontmatter bound to name the overlapping sibling skill it disambiguates against. Source, external AgentSkills research.
- [R9] Deterministic artifact verification. Prefer mechanical verification over visual inspection. Source, `conventional-commit` and `verification-before-completion`.
- [R10] Up-down-up reversibility. Subject any state mutation to forward, rollback, and idempotent reapplication before approval. Source, `schema-migration`.
- [R11] Zero-paraphrase envelope. When delegating, pass the source spec verbatim inside a write-allowlist envelope and validate with `git diff --name-only`. Source, `executing-plans`.
- [R12] Interaction frequency gate. Disqualify a mechanism outright when its trigger rate exceeds the useful threshold, before inspecting implementation. Source, `ui-motion`.
- [R13] Four-part anti-pattern schema. Structure every rejected pattern as title, pattern description, why it fails, and the concrete fix. Source, `reflect-to-skill`.
- [R14] Inverted critique order. State fatal flaws and boundary violations before any positive synthesis. Source, `web-advisor-prompt`.
- [R15] Banned performative agreement. Never emit praise or empty agreement. State file path, line number, and defect. Source, `code-review`.

## Quick audit checklist

Run this check before delivering any skill review:

| Check | Passing condition |
|---|---|
| Prerequisite skills | Verified `unslop` and `writing-for-agents` are loaded directly via `view_file` |
| Mode selection | Explicitly identified as Audit mode or Benchmark mode |
| Frontmatter audit | Validated against AgentSkills schema, positive triggers, negative exclusions, and sibling disambiguation |
| Context load | Verified `SKILL.md` is under 250 lines with heavy manuals in `references/` |
| Completion criteria | Every operational step audited for checkable, binary completion criteria anchored to a verifiable artifact |
| Boundary isolation | Validated presence of explicit guards protecting code and system invariants |
| Anti-slop scan | Audited for banned vocabulary, dashes, colons, inline headers, and mannered prose |
| Mechanical grounding | Verified every recommendation describes a mechanical contract or metric |
| Actionable synthesis | Findings include concrete drop-in patch snippets rather than vague advice |
