# Arena orchestration and parallel subagent execution

Execution protocol for launching six concurrent subagents in an isolated testing sandbox.

## 1. Directory isolation and file naming standards

Store all arena run artifacts inside a dedicated, timestamped scratch folder isolated from the project source tree:
`<workspace>/scratch/arena-<timestamp>/`

Enforce deterministic, lowercase file naming across all scenarios:

```
scratch/arena-20261010-143000/
├── s1_candidate_a.html
├── s1_candidate_b.html
├── s2_candidate_a.html
├── s2_candidate_b.html
├── s3_candidate_a.html
└── s3_candidate_b.html
```

When benchmarking non-HTML skills, use matching extensions (`.php`, `.ts`, `.md`).

## 2. Six-subagent parallel dispatch protocol

Launch all six subagents concurrently within a single `invoke_subagent` tool invocation. Parallel dispatch prevents sequential waiting latency and isolates execution context.

Subagent allocation matrix:
1. Agent S1-A: Master prompt Scenario 1 executed under Skill Candidate A (Baseline)
2. Agent S1-B: Master prompt Scenario 1 executed under Skill Candidate B (Mutated)
3. Agent S2-A: Master prompt Scenario 2 executed under Skill Candidate A (Baseline)
4. Agent S2-B: Master prompt Scenario 2 executed under Skill Candidate B (Mutated)
5. Agent S3-A: Master prompt Scenario 3 executed under Skill Candidate A (Baseline)
6. Agent S3-B: Master prompt Scenario 3 executed under Skill Candidate B (Mutated)

Model selection rules:
- Set `Model: "inherit"` as the default for all six subagents to match parent reasoning capacity.
- Allow explicit user override to `"flash"` or `"flash_lite"` when the user requests token optimization or rapid trial runs.

## 3. Approved CDN policy for frontend components

To keep artifacts completely self-contained without requiring local Node.js servers, subagents are permitted to link approved CDNs:

- Tailwind CSS: `<script src="https://cdn.tailwindcss.com"></script>`
- Motion dev or Motion One: `<script src="https://cdn.jsdelivr.net/npm/motion@latest/dist/motion.js"></script>`
- Lenis smooth scroll: `<script src="https://unpkg.com/lenis@1.1.18/dist/lenis.min.js"></script>`
- Lucide icons: `<script src="https://unpkg.com/lucide@latest"></script>`
- GSAP core: `<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>`

Subagents must never generate broken relative imports like `./components/Button` or unbundled JSX without in-browser Babel transform. Every HTML artifact must open cleanly via `file://` protocol.

## 4. Subagent prompt synthesis pattern

Construct each subagent prompt with strict boundary isolation:

```markdown
Role: Arena Subagent [Scenario X - Candidate Y]
TypeName: research

Instructions:
1. Read the target skill instructions provided below thoroughly.
2. Build a single, completely self-contained micro-component solving the exact specification in the Master Scenario Prompt.
3. Save the completed file directly to [targetFilePath].
4. Do not alter any existing project files.
5. Terminate immediately upon confirming the file exists on disk.

Target Skill Instructions:
[Full text of Skill Candidate A or Candidate B]

Master Scenario Prompt:
[Identical master scenario prompt for Scenario X]
```

## 5. Pre-flight artifact verification before human handoff

Before presenting the comparison table to the human evaluator, the orchestrator must verify all six generated files:

1. Confirm all six files exist on disk in the arena scratch directory and contain non-zero byte counts.
2. Check file contents for syntax integrity, unclosed HTML or script tags, and broken relative import paths.
3. For frontend components, verify that required script tags (such as Tailwind or motion libraries) are linked from approved CDNs rather than missing local modules.
4. If an artifact failed to write or crashed during generation, re-dispatch that specific subagent immediately before surfacing the comparison table to the human evaluator.
