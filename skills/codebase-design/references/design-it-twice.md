# Design it twice

Explore alternative interface shapes using parallel sub-agents before choosing a final design.

## Overview

Based on John Ousterhout's principle in A Philosophy of Software Design, an initial design rarely represents the optimal abstraction. Exploring two or three distinct interfaces uncovers hidden assumptions and clarifies tradeoffs across depth, leverage, and locality.

## Execution workflow

Follow these four steps to run the exploratory design pass.

### Step 1. Problem frame formulation

Summarize the problem space and constraints before dispatching agents:

- State the functional responsibilities the module must deliver.
- Identify the dependency category from `references/deepening.md`.
- Define any non-negotiable performance, storage, or concurrency requirements.
- Present a brief, unoptimized signature sketch to establish concrete inputs and outputs.

### Step 2. Sub-agent dispatch

Invoke two or three sub-agents in parallel using the `invoke_subagent` tool. Assign each agent a radically distinct design priority:

- Agent 1. Minimize interface footprint. Aim for one to three entry points total. Maximize leverage by hiding configuration, orchestration, and parameter assembly inside the module.
- Agent 2. Maximize compositional flexibility. Decouple inputs and execution hooks to support varied callers, plugins, and custom adapters across the seam.
- Agent 3. Optimize for the primary caller. Design the default pathway to execute with zero boilerplate, while keeping secondary capabilities behind optional parameter overrides.
- Agent 4. Ports and adapters architecture. Isolate cross-seam dependencies when crossing network boundaries, external platforms, or third party services.

Provide each sub-agent with the problem frame, relevant file paths, and domain terminology from `AGENTS.md` or `CODEBASE.md`.

### Step 3. Interface comparison

Collect the sub-agent responses and evaluate each candidate using four objective metrics:

| Metric | Evaluation criteria |
|---|---|
| Depth | Amount of behavior provided divided by the surface of the interface |
| Locality | Concentration of logic and bug fixes within the module body |
| Leverage | Total caller code eliminated across all integration sites |
| Test simplicity | Ease of verifying behavior through public methods without mock setups |

### Step 4. User selection gate

Present the candidate interfaces side by side with their tradeoff matrix to the user:

- Display each candidate signature with sample caller usage.
- Explain the key architectural tradeoff of each variant.
- Provide a decisive, opinionated recommendation pointing to the strongest variant. Propose a hybrid design if combining key elements from multiple candidates yields higher leverage, rather than presenting a passive menu.

Wait for user selection. Once the user approves a design or combines traits from multiple candidates, return to Step 3 of the main `SKILL.md` workflow.
