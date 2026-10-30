---
name: skill-testing
description: Use when empirically benchmarking, A/B testing, stress-testing against golden production benchmarks, and iteratively refining agent skills through multi-scenario parallel subagent execution and human evaluation. Don't use for static linting (use review-a-skill), application code test execution (use testing-patterns directly), or single-agent drafting (use writing-for-agents).
---

# Empirical skill testing arena

Empirically benchmark candidate skill instructions against baseline implementations using parallel subagents and human-in-the-loop evaluation.

<HARD-GATE>
Write-Target Boundary. Confine skill test runs, subagent outputs, and sandbox workspaces strictly to `scratch/arena-<timestamp>/` or `.agents/state/skill-testing/`. Do not modify tracked skill files, production source code, or repository configurations during benchmarking. Mutate target skills only after human evaluation confirms the patch.
</HARD-GATE>

## Modes

Declare the active operating mode before executing any steps:
- Benchmark mode (default): Execute parallel test runs across golden benchmark scenarios to evaluate skill quality. Run Steps 1 through 4 sequentially.
- Scenario authoring mode: Formulate test scenarios and master prompts without running subagents. Run Step 1 and Step 2 only. Emit test matrix to `.agents/state/skill-testing/test-plan.md` and halt.

## Overview

The skill testing arena validates prompt engineering hypotheses by measuring real model behavior instead of theoretical markdown linting. Six concurrent subagents build identical micro-components under competing skill versions across three contrasting stress scenarios. When a golden production reference is provided, the arena deconstructs its concrete mechanics first to ensure skills do not stay trapped in mediocre local optima. Human evaluation directs differential rule extraction and safe patch synthesis.

Consult deep reference documents in `references/` for scenario archetypes, concurrency protocols, and evaluation rubrics.

## Workflow router

Identify execution scope and route execution immediately:
1. Benchmarking against a golden reference artifact. When the user provides a reference file or URL, deconstruct its specific mechanics first. Consult `references/scenario-generator.md`.
2. Benchmarking UI and frontend skills. Formulate HTML micro-components using approved CDN libraries. Consult `references/scenario-generator.md` and `references/arena-orchestration.md`.
3. Benchmarking backend or architecture skills. Formulate self-contained test scripts, domain models, or query modules. Consult `references/scenario-generator.md`.
4. Benchmarking technical writing skills. Formulate parallel markdown drafts and evaluate cadence, structure, and clarity. Consult `references/scenario-generator.md`.
5. Ingesting evaluations and grafting patches. Process human decisions and synthesize surgical diffs. Consult `references/evaluation-and-grafting.md`.

## Execution invariants

Avoid these core failure modes:
1. Evaluating in an echo chamber. When a golden production reference is available, deconstruct its mechanics before formulating scenarios. Never test candidate skills against weak, synthetic strawmen alone.
2. Formulating unverified rules. Every candidate rule and patch must cite at least three verified external source URLs from official documentation or recognized industry creators via `search_web`.
3. Requesting full-page test artifacts. Restrict every scenario to an isolated micro-component under 120 lines of code. Full pages waste tokens and introduce uncontrolled variables.
4. Asymmetric scenario prompts. Candidate A and Candidate B must receive the exact same master prompt down to the character. Never inject candidate-specific hints into scenario prompts.
5. Surfacing broken artifacts to evaluators. Execute pre-flight verification on all six generated files before presenting the comparison table.
6. Mutating target skills before human review. Never alter target skill files directly during test execution. Apply changes only after human evaluation confirms the winning candidate.
7. Violating target skill context budgets. When grafting rules, keep the target `SKILL.md` strictly under 250 lines. Disclose long recipes into `references/` and commit them to git.
8. Executing subagents sequentially. Launch all six subagents concurrently in a single tool call to eliminate wait times and isolate execution contexts.

## The build sequence

### Step 1. Target ingestion, golden calibration, and hypothesis formulation

Identify target skill and isolate candidate variation:
- Read target skill file using `view_file`.
- Designate current file content as Candidate A (Baseline).
- If user provided a golden reference file or URL, deconstruct its core mechanics, math formulas, and visual rendering layers using `references/scenario-generator.md`.
- Execute targeted Google searches via `search_web` to discover industry best practices, official documentation, or proven patterns. Require at least three verified source URLs.
- Formulate proposed modifications as Candidate B (Candidate), grounding changes in verified citations and identified reference gaps.
- Document the exact hypothesis being tested along with external source URLs.

Completion criterion. `.agents/state/skill-testing/scope.json` exists on disk with `target_skill`, `candidate_a_hash`, `candidate_b_diff`, `mode`, and at least three verified `source_urls`.

### Step 2. Three-scenario matrix generation

Formulate three contrasting micro-component master prompts across distinct stress axes:
- Consult `references/scenario-generator.md` to select domain archetypes.
- Scenario 1 must target high-frequency transactional utility with zero decorative overhead.
- Scenario 2 must target dynamic tactile physics, responsive pointer interaction, or complex state transitions.
- Scenario 3 must target expressive narrative craft, editorial depth, or resilient edge-case handling.
- Keep each component prompt strictly scoped to under 120 lines of expected output.

Completion criterion. Exactly three contrasting micro-component scenarios formulated with identical prompt contracts for both candidates recorded in `.agents/state/skill-testing/test-plan.md`.

### Step 3. Six-subagent parallel execution and pre-flight verification

Launch testing arena concurrently and verify output integrity:
- Create a timestamped sandbox directory at `scratch/arena-<timestamp>/`.
- Construct subagent prompts embedding the master scenario prompt and candidate skill rules.
- Set model configuration to `inherit` by default, or apply `flash` if the user explicitly requested token optimization.
- Launch all six subagents concurrently in a single parallel dispatch:
  - S1-A and S1-B for Scenario 1
  - S2-A and S2-B for Scenario 2
  - S3-A and S3-B for Scenario 3
- Enforce deterministic output filenames including `s1_candidate_a.html`, `s1_candidate_b.html`, `s2_candidate_a.html`, `s2_candidate_b.html`, `s3_candidate_a.html`, and `s3_candidate_b.html`.
- Run pre-flight verification according to `references/arena-orchestration.md`. Confirm all six files exist, contain non-zero bytes, have valid syntax, and link approved CDNs without broken imports.

Completion criterion. All six subagents complete execution and all six output files pass pre-flight verification on disk with status recorded in `scratch/arena-<timestamp>/verification.json`.

### Step 4. Human evaluation and differential rule grafting

Ingest human decisions and synthesize the final patch:
- Present completed artifacts in a comparison table with clickable `file://` links.
- Prompt user to inspect files locally and select a winner for each scenario along with qualitative feedback.
- Consult `references/evaluation-and-grafting.md` to map win patterns and detect rule regressions.
- Execute targeted searches via `search_web` to validate evaluator feedback against authoritative technical sources before drafting rules.
- Extract differential rules responsible for superior behavior and construct a surgical diff block.
- Verify that target `SKILL.md` remains strictly under 250 lines, pushing extended documentation into `references/`.
- Present synthesized diff to user with two explicit options to run an additional iteration round or commit the patch permanently to the target skill.

Completion criterion. User evaluation ingested, external search validation completed, differential patch generated under target line budget constraints, and explicit user decision recorded in `.agents/state/skill-testing/evaluation-result.json`.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| ST-1 | Echo chamber testing | Tests candidate skills without golden production baselines | Traps skills in synthetic, mediocre local optima | Deconstruct real-world references before scenario design |
| ST-2 | Unverified rule graft | Drafts candidate rules based on intuition or unverified claims | Promotes ungrounded practices that fail under pressure | Require at least three verified source URLs via search_web |
| ST-3 | Page-level scope | Requests full application pages for arena comparisons | Blows context budget and obscures individual variables | Restrict scenarios to micro-components under 120 lines |
| ST-4 | Prompt asymmetry | Injects candidate-specific hints into master prompts | Invalidates comparative A/B benchmark integrity | Enforce character-identical master scenario prompts |
| ST-5 | Broken artifact surfacing | Presents failed subagent code directly to evaluators | Wastes evaluator attention on obvious runtime errors | Run automated pre-flight checks before user evaluation |
| ST-6 | Preemptive skill write | Overwrites target skill files before human evaluation | Risks silent regression of established skill rules | Propose diffs and await explicit user confirmation |

## Boundary isolation

Confine skill testing strictly to test harness workspaces and benchmark fixtures. Never alter active production skills without clean test verification and explicit confirmation.

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
| Anti-patterns | Anti-pattern table adheres to 5-column schema with stable IDs |
| Punctuation hygiene | Zero em dashes, zero en dashes, zero mid-sentence colons |
| Completion criteria | Every build step terminates on a checkable binary completion condition |
