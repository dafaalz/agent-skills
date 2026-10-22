---
name: skill-testing
description: Use when empirically benchmarking, A/B testing, stress-testing against golden production benchmarks, and iteratively refining agent skills through multi-scenario parallel subagent execution and human evaluation. Don't use for static linting (use review-a-skill), application code test execution (use testing-patterns), or single-agent drafting (use writing-for-agents).
---

# Empirical skill testing arena

Empirically benchmark candidate skill instructions against baseline implementations using parallel subagents and human-in-the-loop evaluation.

## Modes

Select an execution mode before Step 1:
- Benchmark mode (default). Execute parallel test runs across golden benchmark scenarios to evaluate skill quality.
- Evaluation and grafting mode. Compare variant outputs, extract superior techniques, and merge refinements into target skills.

## Overview

The skill testing arena validates prompt engineering hypotheses by measuring real model behavior instead of theoretical markdown linting. Six concurrent subagents build identical micro-components under competing skill versions across three contrasting stress scenarios. When a golden production reference is provided, the arena deconstructs its concrete mechanics first to ensure skills do not stay trapped in mediocre local optima. Human evaluation directs differential rule extraction and safe patch synthesis.

Consult deep reference documents in `references/` for scenario archetypes, concurrency protocols, and evaluation rubrics.

## Workflow router

Identify execution scope and route execution immediately:

1. **Benchmarking against a golden reference artifact.** When the user provides a reference file or URL, deconstruct its specific mechanics first. Consult [references/scenario-generator.md](references/scenario-generator.md).
2. **Benchmarking UI and frontend skills.** Formulate HTML micro-components using approved CDN libraries. Consult [references/scenario-generator.md](references/scenario-generator.md) and [references/arena-orchestration.md](references/arena-orchestration.md).
3. **Benchmarking backend or architecture skills.** Formulate self-contained test scripts, domain models, or query modules. Consult [references/scenario-generator.md](references/scenario-generator.md).
4. **Benchmarking technical writing skills.** Formulate parallel markdown drafts and evaluate cadence, structure, and clarity. Consult [references/scenario-generator.md](references/scenario-generator.md).
5. **Ingesting evaluations and grafting patches.** Process human decisions and synthesize surgical diffs. Consult [references/evaluation-and-grafting.md](references/evaluation-and-grafting.md).

## Execution invariants

Avoid these core failure modes:

1. **Evaluating in an echo chamber.** When a golden production reference is available, deconstruct its mechanics before formulating scenarios. Never test candidate skills against weak, synthetic strawmen alone.
2. **Formulating unverified rules.** Every candidate rule and patch must cite at least three verified external source URLs from official documentation or recognized industry creators via `search_web`.
3. **Requesting full-page test artifacts.** Restrict every scenario to an isolated micro-component under 120 lines of code. Full pages waste tokens and introduce uncontrolled variables.
4. **Asymmetric scenario prompts.** Candidate A and Candidate B must receive the exact same master prompt down to the character. Never inject candidate-specific hints into scenario prompts.
5. **Surfacing broken artifacts to evaluators.** Execute pre-flight verification on all six generated files before presenting the comparison table.
6. **Mutating target skills before human review.** Never alter target skill files directly during test execution. Apply changes only after human evaluation confirms the winning candidate.
7. **Violating target skill context budgets.** When grafting rules, keep the target `SKILL.md` strictly under 250 lines. Disclose long recipes into `references/`.
8. **Executing subagents sequentially.** Launch all six subagents concurrently in a single tool call to eliminate wait times and isolate execution contexts.

## The build sequence

### Step 1. Target ingestion, golden calibration, and hypothesis formulation

Identify the target skill and isolate the candidate variation:

- Read the target skill file using `view_file`.
- Designate the current file content as Candidate A (Baseline).
- If the user provided a golden reference file or URL, deconstruct its core mechanics, math formulas, and visual rendering layers using `references/scenario-generator.md`.
- Execute targeted Google searches via `search_web` to discover industry best practices, official documentation, or proven engineering patterns before drafting candidate rules. Require at least three verified source URLs.
- Formulate the proposed modifications as Candidate B (Candidate), grounding changes in verified external citations and identified golden reference gaps.
- Document the exact hypothesis being tested along with external source URLs.

Completion criterion. Target skill file ingested, golden reference deconstructed if provided, external search completed with three verified source URLs, Candidate A and Candidate B rulesets isolated, and the test hypothesis documented.

### Step 2. Three-scenario matrix generation

Formulate three contrasting micro-component master prompts across distinct stress axes:

- Consult [references/scenario-generator.md](references/scenario-generator.md) to select domain archetypes.
- Scenario 1 must target high-frequency transactional utility with zero decorative overhead.
- Scenario 2 must target dynamic tactile physics, responsive pointer interaction, or complex state transitions.
- Scenario 3 must target expressive narrative craft, editorial depth, or resilient edge-case handling.
- Keep each component prompt strictly scoped to under 120 lines of expected output.

Completion criterion. Exactly three contrasting micro-component scenarios formulated with identical prompt contracts for both candidates.

### Step 3. Six-subagent parallel execution and pre-flight verification

Launch the testing arena concurrently and verify output integrity:

- Create a timestamped sandbox directory at `<workspace>/scratch/arena-<timestamp>/`.
- Construct subagent prompts embedding the master scenario prompt and candidate skill rules.
- Set model configuration to `inherit` by default, or apply `flash` if the user explicitly requested token optimization.
- Launch all six subagents concurrently in a single parallel dispatch:
  * S1-A and S1-B for Scenario 1
  * S2-A and S2-B for Scenario 2
  * S3-A and S3-B for Scenario 3
- Enforce deterministic output filenames including `s1_candidate_a.html`, `s1_candidate_b.html`, `s2_candidate_a.html`, `s2_candidate_b.html`, `s3_candidate_a.html`, and `s3_candidate_b.html`.
- Run pre-flight verification according to [references/arena-orchestration.md](references/arena-orchestration.md). Confirm all six files exist, contain non-zero bytes, have valid syntax, and link approved CDNs without broken imports.

Completion criterion. All six subagents complete execution and all six output files pass pre-flight verification on disk.

### Step 4. Human evaluation and differential rule grafting

Ingest human decisions and synthesize the final patch:

- Present the completed artifacts in a comparison table with clickable `file://` links.
- Prompt the user to inspect the files locally and select a winner for each scenario along with qualitative feedback.
- Consult [references/evaluation-and-grafting.md](references/evaluation-and-grafting.md) to map win patterns and detect rule regressions.
- Execute targeted searches via `search_web` to validate evaluator feedback against authoritative technical sources before drafting rules.
- Extract the differential rules responsible for superior behavior and construct a surgical diff block.
- Verify that the target `SKILL.md` remains strictly under 250 lines, pushing extended documentation into `references/`.
- Present the synthesized diff to the user with two explicit options to run an additional iteration round or commit the patch permanently to the target skill.

Completion criterion. User evaluation ingested, external search validation completed, differential patch generated under target line budget constraints, and explicit user decision received on iteration or permanent commit.

## Boundary isolation

Confine skill testing strictly to test harness workspaces and benchmark fixtures. Never alter active production skills without clean test verification and explicit confirmation.

## Quick audit checklist

Verify execution against this checklist before delivering. Every item represents an automatic rejection:

| Never | Instead |
|---|---|
| Full-page landing prompts in arena runs | Scoped micro-components under 120 lines |
| Different master prompts between candidates | Character-identical master prompts |
| Spawning subagents in sequential batches | Concurrent 6-subagent dispatch in one call |
| Testing in an echo chamber without golden references | Calibrating scenarios against real-world references |
| Formulating candidate rules from unverified guesswork | Grounding rules via at least three search_web citations |
| Surfacing broken or unverified artifacts to evaluators | Running pre-flight verification on disk first |
| Mutating target skill before human sign-off | Proposing diffs after human evaluation |
| Hardcoded local paths in subagent code | Relative paths or approved CDN script tags |
| Unstructured human feedback collection | Clear scenario comparison table with file links |
| Overwriting entire skill files for small fixes | Surgical differential rule grafting |
| Bloating target `SKILL.md` past 250 lines during grafting | Progressively disclosing recipes into `references/` |

## Quick verification checklist

| Check | Passing condition |
|---|---|
| Frontmatter routing | Name matches directory, positive triggers and negative exclusions defined |
| Context budget | Main `SKILL.md` under 250 lines with deep archetypes in `references/` |
| Golden calibration | Real-world reference deconstructed into scenarios when provided |
| External search | Candidate rules and patches validated against at least three search_web URLs |
| Concurrency | Six subagents dispatched concurrently in a single tool call |
| Output isolation | Artifacts stored under scratch arena directory with standardized names |
| Pre-flight check | All six generated files verified non-empty with valid syntax before review |
| Human gate | Comparison table delivered with local file links before patching target skills |
| Patch budget | Target skill verified under 250 lines with clean diff presentation |
| Punctuation hygiene | Zero em dashes, zero en dashes, zero mid-sentence colons |
| Completion criteria | Every build step terminates on a checkable binary completion condition |
