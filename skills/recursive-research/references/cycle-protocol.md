# Cycle protocol

Keep the run resumable. Read this file at Step 4 and before you continue a saved run.

## Directory layout

```text
.agents/research/<slug>/
├── state.md                  # cycle count, coverage per thread, saturation
├── threads.md                # kept threads with scores and dropped candidates
├── findings.md               # consolidated findings and cross-thread links
├── sources-tier-1.md
├── sources-tier-2.md
├── sources-tier-3.md
├── sources-rejected.md       # every rejected source with the reason
├── cycle-01.md, cycle-NN.md  # one checkpoint per cycle
├── synthesis.md              # written at close
├── gaps.md                   # unknowns, conflicts, source bias
└── actions.md                # checklist of next actions
```

## Slug rules

Derive the slug from the topic in kebab case, lowercase, and 40 characters or fewer. Reuse the same slug when the user returns to the same topic.

## state.md schema

| Field | Value |
|---|---|
| Topic | The seed topic in one line |
| Mode | Cycle or Targeted |
| Scope | web, local, or both, plus the local paths |
| Cap | The cycle cap confirmed at intake |
| Cycle | The current cycle number |
| Coverage | Percent per thread |
| Saturation | New findings divided by accumulated findings, per cycle |
| Next thread | The thread with the lowest coverage |

## cycle-NN.md schema

| Field | Value |
|---|---|
| Thread | The thread worked this cycle |
| Sources | Title, tier, and URL per source |
| New findings | Facts, numbers, and quotes with attribution |
| Cross-thread links | Links to findings in other threads |
| Open questions | Questions handed to the next cycle |

## Context threshold

Write the checkpoint, then pause and ask the user when either threshold trips during a cycle.

- Tool calls in the session reach 150.
- Approximate output tokens reach 80000.

Report the cycle count, the threshold that tripped, the path `.agents/research/<slug>/`, and the resume command line `/recursive-research <slug>`. Continue only when the user answers `continue`, and stop at Step 6 when the user answers `pause`.

## Resume procedure

1. Read `state.md` and reconstruct the cycle count, the coverage, and the next thread.
2. Read the latest `cycle-NN.md` for the recent context.
3. Read `threads.md` for the current thread tree.
4. Report the last cycle, the next thread, and the open questions, then ask whether to continue.
5. Continue at Step 4 when the user confirms, and stop with a clear error and the Step 1 intake when the slug has no directory.
