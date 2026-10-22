---
name: recursive-research
description: Use when researching a topic to expert depth, tiering sources by reliability, or mapping state of the art before a design spec or a plan. Don't use for session summaries (use summarize), code review (use code-review), or packaging prompts for an external model (use web-advisor-prompt).
---

# Recursive research

Research a topic to expert depth before you write a design spec or a plan. Run regulated cycles that pick the least covered thread, tier every source, save a checkpoint each cycle, and stop only when the five fitness criteria pass or the cycle cap trips.

Read `references/source-tiering.md` when you assign a tier to a source or pick seed sources. Read `references/decision-frameworks.md` before an autonomous pick and before you declare fitness. Read `references/cycle-protocol.md` at every cycle checkpoint and when you resume a saved run.

## Modes

Select a mode before Step 1.

- Cycle mode (default). Run the loop across 3 to 5 seed threads until the five fitness criteria pass or the cap trips. Use it for a dossier, a state of the art map, or a spec input.
- Targeted mode. Answer one bounded question across the best available sources, skip cross-thread synthesis, and return a cited brief. Callers such as `brainstorming` use this mode when a design needs rules rather than a dossier.

State the mode in one line before you start.

## Workflow

Follow these six steps in sequence.

### Step 1. Intake and state file

Ask the user for the topic, the evidence scope (web, local files, or both), the priority and excluded sources, and the cycle cap (default 8). Read the local paths when the user names them.

Create `.agents/research/<slug>/` with `state.md`, `threads.md`, `findings.md`, and the four source ledgers. Keep the slug in kebab case at 40 characters or fewer.

When `.agents/research/<slug>/state.md` already exists, read it, report the last completed cycle and the next thread, and continue from that cycle instead of restarting.

Completion criterion. The user confirms the topic, the scope, and the cap in one line, and `.agents/research/<slug>/state.md` exists on disk.

### Step 2. Seed threads

List 5 to 8 candidate threads, score them with the weighted decision matrix in `references/decision-frameworks.md`, and keep the top 3 to 5. Score coverage, perspective diversity, source access, and relevance to the user goal.

Run Munger inversion over the kept threads. Name the dropped thread that carries a dissenting school, a missing region, or a counter-position. Add it when the inversion finds a hole, then rescore.

In Targeted mode, keep one thread and stop.

Completion criterion. `threads.md` lists the kept threads with scores and the dropped candidates with a reason.

### Step 3. Source plan

Tier every candidate source T1, T2, T3, or Rejected against `references/source-tiering.md`. Present the seed source list for the domain from the same file and let the user add or reject entries.

Reject a source that carries no named author, no data, or no citation trail. Record the tier, the URL, the author, the date, and the reason in the matching ledger.

Completion criterion. Every consulted source appears in one of the four ledgers with a tier and a reason, and zero sources carry an unstated tier.

### Step 4. Cycle

Run one cycle at a time.

1. Pick the thread with the lowest coverage.
2. Score the candidate sources for this cycle with the matrix in `references/decision-frameworks.md`, then invert the pick and name the contradicting source you skipped.
3. Read the sources and harvest facts, numbers, quotes with attribution, and new names.
4. Tier each source into the matching ledger.
5. Write `cycle-NN.md` with the thread, the sources, the new findings, the cross-thread links, and the open questions.
6. Update `state.md` with the cycle count, the coverage per thread, and the saturation ratio of new findings to accumulated findings.

Follow `references/cycle-protocol.md` for the checkpoint schema, the resume procedure, and the context threshold that triggers a pause before the session compacts.

Completion criterion. `cycle-NN.md` and `state.md` both carry the current cycle number and agree on the findings count.

### Step 5. Fitness check

Test the five criteria. Move to Step 6 only when all five pass.

1. Coverage at 80 percent or higher on every seed thread.
2. Three or more T1 sources per thread, or T1 plus T2 when the field holds few T1 sources.
3. Saturation at 5 percent or lower for three consecutive cycles.
4. Munger inversion written into `gaps.md` for the current knowledge state.
5. Three or more explicit links between different threads.

When the cap trips before the criteria pass, close with the gap list and state the failed criteria by number instead of claiming expert depth.

Completion criterion. You state pass or fail for each of the five criteria with the measured value and the file that holds it.

### Step 6. Close and hand back

Write `synthesis.md` with the findings per thread, the contradictions, and the open gaps. Write `gaps.md` with what you still do not know, the conflicting sources, and the bias in your source set. Write `actions.md` with the checklist of next actions.

Return the brief from the Handoff section to the caller. Ask the user whether to close, deepen one gap, add a thread, or continue.

Completion criterion. `synthesis.md`, `gaps.md`, and `actions.md` exist on disk and the brief names at least one open gap.

## Handoff

Return these fields and stop when a caller invokes this skill in Targeted mode.

- Topic and the bounded question.
- Findings grouped by the affected layer or subsystem.
- Citations with source titles, URLs, and tiers.
- Rejected sources with the rejection reason.
- Open gaps and the risk each one carries for the caller.

## Boundaries

Write evidence only inside `.agents/research/<slug>/`. Leave application source code, database schemas, migrations, configuration files, and shell commands byte for byte. Return findings to the caller and let the caller edit its own spec and plan files.

## Anti-patterns

| Rejected pattern | Why it fails | Fix |
|---|---|---|
| Flat search | Repeats queries with synonyms and never deepens | Open the source and harvest facts |
| Source picked for comfort | Confirms the first answer | Add the contradicting source from the inversion |
| Missing checkpoint | Five cycles of work lost to compaction | Write `cycle-NN.md` before the next cycle |
| Tier 3 without a citation trail | Spreads an unverified claim | Reject the source or move it to Rejected |
| Self-declared expert depth | Skips the measured criteria | State pass or fail per criterion with the number |

## Quick audit checklist

| Check | Passing condition |
|---|---|
| State file | `.agents/research/<slug>/state.md` exists and names the current cycle |
| Source ledgers | Every source carries a tier, a URL, and a reason |
| Cycle checkpoint | `cycle-NN.md` exists for each completed cycle |
| Fitness evidence | Each of the five criteria carries a measured value |
| Gaps | `gaps.md` names the unknowns, the conflicts, and the source bias |
| Handoff | The brief carries findings, citations, rejected sources, and gaps |
| Boundaries | Zero edits outside `.agents/research/<slug>/` |
