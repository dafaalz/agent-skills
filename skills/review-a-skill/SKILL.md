---
name: review-a-skill
description: Use when reviewing, auditing, benchmarking, or comparing agent skills against AgentSkills specifications, structural guidelines, or alternative implementations. Don't use for reviewing application source code, running CI test suites, or writing end-user documentation.
---

# Review a skill

Audit agent skills against AgentSkills standards, structural execution requirements, and anti-slop guidelines. Evaluate candidates in isolation or benchmark them against existing implementations to isolate sharp rules and close procedural loopholes.

## Workflow

Follow these four steps in sequence:

### Step 1. Ingestion and mode determination

Identify the review scope and intake candidate artifacts:

- Audit mode. Inspect a single target skill against structural and linguistic standards.
- Benchmark mode. Compare a candidate skill implementation against a baseline skill to determine architectural superiority and extract sharp rules.

Load prerequisite skills and target files before auditing:

1. Read both `unslop` (`/Users/groundfox/.gemini/config/skills/unslop/SKILL.md`) and `writing-for-agents` (`/Users/groundfox/.gemini/config/skills/writing-for-agents/SKILL.md`) directly using `view_file`. Never audit from memory or secondary summaries.
2. Load the target `SKILL.md` along with any disclosed files in `references/`. Check initial boundary constraints:
   - Directory naming. Confirm the directory name matches the `name` field in the YAML frontmatter using 1 to 64 lowercase alphanumeric characters and single hyphens.
   - Context budget. Confirm the main `SKILL.md` stays under 250 lines. Flag heavy documentation exceeding 100 lines that belongs in `references/`.

Completion criterion. Prerequisite skills `unslop` and `writing-for-agents` are loaded into context via `view_file`, target skills are ingested, the operating mode is determined, and directory naming plus line budget constraints are cataloged.

### Step 2. Structural and execution audit

Audit the skill against `writing-for-agents` structural requirements:

- Frontmatter routing. Check the `description` field for explicit positive triggers starting with "Use when" and negative exclusions starting with "Don't use for". Verify absence of internal workflow summaries that tempt models to skip the skill body. Note intentional use of `disable-model-invocation: true` for purely manual skills.
- Information hierarchy. Verify clean separation across the three tiers: primary sequential execution steps, secondary on-demand constraint tables, and tertiary external reference pointers.
- Workflow discipline. Verify steps run in strict numbered sequence. Check for explicit mode handling (such as Audit mode versus Edit mode) to prevent premature destructive rewrites.
- Binary completion criteria. Every numbered step must terminate on a checkable, binary, and exhaustive completion criterion. Flag vague completions like "ensure understanding" or "verify accuracy" that induce premature completion.
- Leading words and positive bounds. Confirm the text recruits pre-training priors with established leading words. Ensure every negative prohibition is paired immediately with an explicit positive action.
- Boundary isolation. Confirm explicit rules protect non-target domains, such as keeping code syntax, database schemas, and terminal commands untouched by stylistic guidelines.

Completion criterion. A written catalog listing structural findings, missing completion criteria, frontmatter defects, and boundary leaks.

### Step 3. Anti-slop and linguistic scan

Audit skill prose against `unslop` guidelines:

- Banned vocabulary and puffery. Search for promotional filler, throat-clearing openings, and sycophantic closings. Replace them with plain words and direct verbs.
- Punctuation hygiene. Check for zero em dashes, zero en dashes, and zero hyphens acting as dashes. Confirm colons appear only to introduce lists, tables, or code blocks, with zero mid-sentence colons and zero pseudo-labels.
- Mechanical grounding. Verify statements describe concrete system contracts, commands, metrics, or files instead of emotional impressions. Apply the portability test. If an instruction could appear unchanged in an unrelated project, anchor it with specific mechanics or cut it.
- Modern slop patterns. Flag redundant inline-header lists where a bold label merely repeats the following clause. Flag mannered prose, philosophical aphorisms, personified code, and over-compression that drops articles or uses telegram arrows.
- Localization and calque patterns. For Indonesian documentation, eliminate calque relative clauses like "di mana" or "yang mana", pleonasms like "guna untuk" or "adalah merupakan", and abstract metaphors.

Completion criterion. A linguistic finding log citing line numbers, offending phrases, matched slop categories, and positive replacements.

### Step 4. Synthesis, comparison, and grafting

Synthesize findings into an actionable evaluation report:

- Comparative evaluation table. In Benchmark mode, render a structured comparison table across key dimensions:
  1. Frontmatter and Discovery
  2. Workflow and State Machine
  3. Completion Criteria
  4. Language and Context Budget
  5. Boundary Isolation
  6. Rule Granularity and Anti-Slop Depth
  7. Composability and Citation
- Grounded verdict. Deliver a direct, blunt assessment in the opening sentence stating whether the candidate is better, worse, or mixed compared to the baseline.
- Sharp rule grafting. Extract novel or sharper rules from candidate versions. Formulate drop-in replacement snippets that preserve existing structure while sealing loopholes.
- Final checklist verification. Audit the candidate or proposed patch against the quick audit checklist below.

Completion criterion. An evaluation report containing the dimensional comparison table or single-audit log, a direct verdict, and concrete drop-in patch recommendations.

## Dimensional evaluation rubric

Consult these benchmarks when evaluating skills during Benchmark mode:

| Dimension | Passing standard | Failing tell |
|---|---|---|
| Frontmatter | Kebab-case name, positive triggers, negative exclusions, under 500 characters | Vague summary, missing negative bounds, workflow leaks |
| Workflow | Sequential numbered steps, distinct execution modes | Unordered bullets, vague progression, missing mode branch |
| Completion criteria | Binary, checkable, and exhaustive at the end of every step | Fuzzy assertions like "ensure quality" or missing criteria |
| Hierarchy | Main file under 250 lines, heavy reference disclosed behind pointers | Monolithic text exceeding 250 lines, sprawling inline manuals |
| Boundary isolation | Explicit guards for code, database schemas, and commands | Stylistic or persona bleed into functional code syntax |
| Anti-slop | Zero banned words, zero dashes, colons only before lists or code | Em dashes, colon reveals, puffery, mannered prose |
| Grounding | Concrete mechanism, numbers, endpoints, and CLI commands | Subjective impressions, emotional claims, generic advice |
| Composability | Stable rule IDs or modular headings for clean external citation | Unreferenced prose blocks requiring full duplication |

## Quick audit checklist

Run this check before delivering any skill review:

| Check | Passing condition |
|---|---|
| Prerequisite skills | Verified `unslop` and `writing-for-agents` are loaded directly via `view_file` |
| Mode selection | Explicitly identified as Audit mode or Benchmark mode |
| Frontmatter audit | Validated against AgentSkills schema, positive triggers, and negative exclusions |
| Context load | Verified `SKILL.md` is under 250 lines with heavy manuals in `references/` |
| Completion criteria | Every operational step audited for checkable, binary completion criteria |
| Boundary isolation | Validated presence of explicit guards protecting code and system invariants |
| Anti-slop scan | Audited for banned vocabulary, dashes, colons, inline headers, and mannered prose |
| Mechanical grounding | Verified every recommendation describes a mechanical contract or metric |
| Actionable synthesis | Findings include concrete drop-in patch snippets rather than vague advice |
