---
name: skill-testing
description: Use when empirically benchmarking, A/B testing, stress-testing against golden production references, and iteratively refining agent skills through blinded multi-scenario subagent execution, automated pre-flight verification, and adversarial advisor or human evaluation. Don't use for static linting (use review-a-skill), application code test execution (use testing-patterns directly), or single-agent drafting (use writing-for-agents).
---

# Empirical skill testing arena

Empirically benchmark candidate skill instructions against baseline implementations using wave-throttled subagents, deterministic pre-flight verifiers, and slot-blinded pairwise evaluation.

<HARD-GATE>
Write-Target Boundary. Confine all test runs, subagent outputs, and run state strictly to `scratch/arena-<run_id>/` and `.agents/state/skill-testing/runs/<run_id>/`. Never mutate tracked skill files or repository source code during benchmarking. Apply target skill patches only after evaluation confirms a winner, backup snapshot exists, and post-patch regression checks pass.
</HARD-GATE>

## Modes

Declare the active operating mode before executing any step:
- `benchmark` (default). Execute Steps 1 through 4 across three stress scenarios with blinded evaluation.
- `scenario-authoring`. Execute Steps 1 and 2 only, write `test-plan.md` to the run directory, and halt.
- `advisor-assisted`. Execute a pre-arena Web Advisor critique on Candidate B in Step 1B and run a position-swapped LLM-as-a-Judge council alongside human review in Step 4.

## Domain adapters and workflow router

Resolve the target domain adapter in Step 1 before generating scenarios:
1. `ui` adapter (`references/scenario-generator.md` and `references/arena-orchestration.md`). Generates self-contained `.html` micro-components (`<= 150` lines) using pinned CDN versions and headless DOM/syntax checks.
2. `backend` adapter (`references/scenario-generator.md` and `references/arena-orchestration.md`). Generates runnable `.ts` or `.py` modules (`<= 200` lines) with inline assertions verified via `node` or `python3`.
3. `writing` adapter (`references/scenario-generator.md` and `references/arena-orchestration.md`). Generates `.md` artifacts (`<= 900` words) verified via deterministic structural and anti-slop regex linters.
4. `grafting` router (`references/evaluation-and-grafting.md`). Ingests blinded verdicts, extracts differential rules, verifies line budget, and replays regression baselines.

## Execution invariants

1. **Run-scoped state isolation.** Generate `<run_id>` as `YYYYMMDD-HHMMSS-<4hex>` and store all state under `.agents/state/skill-testing/runs/<run_id>/`. Never write to unversioned singleton state paths.
2. **Write-capable subagent dispatch.** Dispatch subagents using a write-enabled worker role (`default` or `coder`, never read-only `research`) and require returning the full artifact in response text as a fallback if disk write fails.
3. **Wave-throttled bounded concurrency.** Execute the six subagents in two waves of three (`WAVE_SIZE=3`, or `WAVE_SIZE=2` on Tier 1 keys) with `1500ms` inter-wave jitter, `thinking_budget` capped at `8192` tokens, and `MAX_RETRIES=2` with exponential backoff (`2s`, `4s`). Proceed on partial quorum if at least 2 of 3 scenario pairs pass pre-flight verification.
4. **Tiered empirical grounding.** Validate Candidate B modifications against at least three verified external URLs via `search_web` for public standards, or three concrete repository/golden-artifact citations (`path:line` or benchmark trace) for internal harness skills.
5. **Character-identical scenario prompts.** Candidate A and Candidate B receive identical master scenario prompts without candidate-specific hints.
6. **Cryptographic slot blinding.** Map Candidate A and Candidate B randomly to `slot_x` and `slot_y` per scenario in `blind-key.json`. Conceal true candidate identities until evaluation verdicts are recorded.
7. **Target context budget.** Keep target `SKILL.md` strictly under 250 lines (`wc -l < 250`), disclosing extended procedures into `references/`.
8. **Snapshot and regression defense.** Save `SKILL.md.bak` before patching, verify frontmatter YAML and line count post-patch, and replay the highest-risk historical scenario from `.agents/state/skill-testing/golden-regressions/`.

## The build sequence

### Step 1. Target ingestion, golden calibration, and hypothesis formulation

1. Initialize `<run_id>` and create `.agents/state/skill-testing/runs/<run_id>/` and `scratch/arena-<run_id>/`.
2. Read target `SKILL.md` and any referenced files required by the scenario domain; record SHA-256 hash (`shasum -a 256`) as `candidate_a_hash`.
3. Select domain adapter (`ui`, `backend`, or `writing`) and artifact file extension (`.html`, `.ts`, `.py`, or `.md`).
4. If a golden reference file or URL is supplied, deconstruct its concrete mechanics using `references/scenario-generator.md`.
5. Gather at least three grounding citations (external `search_web` URLs or internal `file:line` traces) and formulate Candidate B's unified diff.
6. In `advisor-assisted` mode, run the pre-arena Web Advisor critique in `references/evaluation-and-grafting.md` to stress-test Candidate B before spending arena tokens.

Completion criterion. `.agents/state/skill-testing/runs/<run_id>/scope.json` exists on disk with `run_id`, `target_skill`, `domain_adapter`, `artifact_ext`, `candidate_a_hash`, `candidate_b_diff`, `mode`, and at least three `grounding_citations`.

### Step 2. Three-scenario matrix generation

1. Consult `references/scenario-generator.md` for the active domain adapter (`ui`, `backend`, or `writing`).
2. Author three contrasting master prompts covering utility/integrity (Scenario 1), dynamic state/tactile interaction (Scenario 2), and narrative/edge-case resilience (Scenario 3) within the domain size budget.
3. Generate cryptographic slot assignments (`slot_x` and `slot_y`) for each scenario and persist to `.agents/state/skill-testing/runs/<run_id>/blind-key.json`.

Completion criterion. `.agents/state/skill-testing/runs/<run_id>/test-plan.md` and `blind-key.json` exist on disk with three identical master prompt contracts and randomized slot mappings.

### Step 3. Wave-throttled subagent execution and pre-flight verification

1. Synthesize subagent prompts following `references/arena-orchestration.md` using anonymized output paths `s1_slot_x.<ext>` through `s3_slot_y.<ext>` inside `scratch/arena-<run_id>/`.
2. Dispatch Wave 1 (`S1-X`, `S1-Y`, `S2-X`) concurrently, pause `1500ms`, and dispatch Wave 2 (`S2-Y`, `S3-X`, `S3-Y`) concurrently.
3. If a subagent omits disk write but emits valid fenced code, materialize the artifact from its response text; retry genuine timeouts or HTTP 429 errors up to `MAX_RETRIES=2` with exponential backoff.
4. Execute the domain-specific pre-flight verifier from `references/arena-orchestration.md` across all six artifacts. If 1 scenario pair fails permanently, mark it `SKIPPED_QUORUM` and continue if at least 2 pairs pass.

Completion criterion. `scratch/arena-<run_id>/verification.json` records `PASS` status for at least 2 complete scenario pairs (4 to 6 files) with zero broken imports or syntax errors.

### Step 4. Blinded evaluation, differential grafting, and regression verification

1. Present anonymized `slot_x` and `slot_y` artifacts in a comparison table with clickable `file://` links.
2. In `advisor-assisted` mode, execute the position-swapped LLM-as-a-Judge pass (`(X, Y)` and `(Y, X)`) per `references/evaluation-and-grafting.md` before revealing human or advisor verdicts.
3. Unblind `blind-key.json` only after verdicts are locked; map wins and regressions across scenarios.
4. Extract operative differential clauses, validate against grounding citations, and verify zero em dashes, zero en dashes, and colons only before lists or code blocks.
5. Snapshot target `SKILL.md` to `.agents/state/skill-testing/runs/<run_id>/SKILL.md.bak`, present the surgical diff for user confirmation, apply upon approval, verify `wc -l < 250` and valid YAML frontmatter, and append winning prompts to `.agents/state/skill-testing/golden-regressions/`.

Completion criterion. `.agents/state/skill-testing/runs/<run_id>/evaluation-result.json` records unblinded verdicts, line-budget check (`< 250`), and final user decision (`iterate` or `committed`).

## Boundary isolation

Execute skill testing within isolated run workspaces. Write benchmark outputs and evaluations strictly under `.agents/state/skill-testing/runs/<run_id>/`. Never mutate production skills or application code during evaluation rounds. Apply candidate patches only after blinded comparisons pass the regression gate.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| ST-1 | Read-only worker dispatch | Launches `research` subagents to write benchmark files | Causes file-write deadlock and retry loops | Use write-capable worker role and text fallback |
| ST-2 | Singleton state collision | Writes `scope.json` to unversioned shared path | Cross-contaminates parallel skill runs | Scope all state under `runs/<run_id>/` |
| ST-3 | Unblinded fixed slots | Labels Candidate A and B in fixed columns | Induces position and confirmation bias | Randomize `slot_x` and `slot_y` via `blind-key.json` |
| ST-4 | Unthrottled 6-way burst | Fires 6 extended-thinking agents at $t=0$ | Triggers HTTP 429 cascades on Tier 1/2 keys | Dispatch in waves of 3 with backoff and quorum |
| ST-5 | HTML-locked verification | Checks CDN tags on `.ts`, `.py`, or `.md` outputs | Misses runtime and structural defects | Route through `ui`, `backend`, and `writing` adapters |
| ST-6 | Unpinned `@latest` CDNs | Links mutable package tags in UI sandboxes | Breaks longitudinal reproducibility | Pin exact immutable CDN versions |
| ST-7 | Unverified patch commit | Writes diffs without backup or regression check | Accumulates silent routing regressions | Snapshot `.bak`, check `wc -l`, update regression suite |

## Quick verification checklist

| Check | Passing condition |
|---|---|
| Frontmatter routing | Name matches directory with explicit positive and negative triggers |
| Context budget | `SKILL.md` strictly under 250 lines (`wc -l < 250`) |
| Run state isolation | All state files scoped under `.agents/state/skill-testing/runs/<run_id>/` |
| Worker write capability | Subagents run with write permissions and response-text extraction fallback |
| Wave concurrency | Dispatched in waves of 3 with `thinking_budget <= 8192` and `MAX_RETRIES=2` |
| Domain adapter parity | Pre-flight verifier matches `ui`, `backend`, or `writing` extension |
| Slot blinding | `blind-key.json` randomizes `slot_x` and `slot_y` before evaluation |
| Position-swap judge | Automated advisor judge runs both `(X, Y)` and `(Y, X)` orderings |
| Grounding citations | At least 3 external URLs or internal `file:line` traces recorded |
| Punctuation hygiene | Zero em dashes, zero en dashes, colons only before lists or code blocks |
| Post-patch safety | `SKILL.md.bak` saved and target `wc -l < 250` verified after commit |
