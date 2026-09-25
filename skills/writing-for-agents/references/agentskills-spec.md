# AgentSkills Specification Reference

Authoritative technical specification based on https://agentskills.io/skill-creation/ for authoring portable, high-efficiency agent skills.

## 1. Directory layout and naming

Every skill lives in a dedicated directory. The directory name must match the `name` field in the frontmatter exactly.

```text
<skill-name>/
├── SKILL.md              # Required entrypoint containing frontmatter and body
├── scripts/              # Optional deterministic executable tools (bash, python, node)
├── references/           # Optional deep reference manuals, API docs, and guides
├── assets/               # Optional static files, templates, boilerplates, mock data
└── examples/             # Optional verified reference implementations
```

### Directory rules
- The skill root directory name must match the frontmatter `name` string byte for byte.
- `SKILL.md` must sit directly in the skill root. Subdirectories cannot contain nested skills.
- Scripts in `scripts/` must be executable. Agents run scripts via shell commands and capture stdout and stderr, avoiding loading script source code into the context window.
- Documents in `references/` are read on demand. Do not load reference files at startup.

## 2. Discovery paths and portability

Skills conform to universal discovery roots supported across multiple agent runtimes:

| Scope | Standard path | Platform notes |
|---|---|---|
| Project / Workspace | `.agents/skills/<skill-name>/` | Universal root checked first across all compatible tools |
| User / Global | `~/.agents/skills/<skill-name>/` | Universal global root available in all user workspaces |
| Antigravity Global | `~/.gemini/config/skills/<skill-name>/` | Platform specific global configuration root |
| Claude Project | `.claude/skills/<skill-name>/` | Vendor specific workspace root |
| Built-in Mounts | System application bundle paths | Read-only bundled system skills |

Discovery prioritizes workspace skills over global skills, allowing projects to override global defaults.

## 3. YAML frontmatter schema

Frontmatter must appear at the very top of `SKILL.md`, enclosed between triple-dash delimiters (`---`).

```yaml
---
name: pdf-form-filler
description: Extracts fields, fills form values, and validates PDF outputs. Use when parsing PDF templates or populating dynamic form documents. Don't use for raw OCR on scanned images or plain text files.
compatibility: Requires python >= 3.10 and poppler-utils installed on host (max 500 chars)
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: "Data Engineering Team"
  repository: "https://github.com/example/skills"
allowed-tools: run_command view_file
---
```

### Field definitions

| Field | Type | Requirement | Constraints |
|---|---|---|---|
| `name` | string | Required | 1 to 64 characters. Lowercase alphanumeric and single hyphens. No leading or trailing hyphens. No consecutive hyphens (`--`). Must match parent folder name. |
| `description` | string | Required | 1 to 1024 characters. Third-person imperative. Explains function, positive triggers, and negative exclusions. |
| `compatibility` | string | Optional | Up to 500 characters. Describes execution environment prerequisites (OS, runtime, external binaries, network requirements). |
| `license` | string | Optional | SPDX license identifier (such as MIT, Apache-2.0) or relative path to a local license file. |
| `metadata` | map | Optional | Arbitrary key-value map for non-functional properties (version, author, tags, upstream URLs). |
| `allowed-tools` | string | Optional | Space-separated list of tool names allowed during skill execution. Enforces least privilege. |
| `disable-model-invocation` | boolean | Platform extension | Set to `true` to hide the skill from autonomous model discovery. Used for user-only invoked skills in Antigravity and Claude Code. |

## 4. Description authoring and routing formula

The `description` field acts as the primary indexing filter during startup discovery. Follow the three-part routing formula:

1. **Functional summary.** State what the skill does in one direct sentence.
2. **Positive triggers.** Start with "Use when..." and specify distinct symptoms, requests, and operational contexts.
3. **Negative triggers.** Start with "Don't use for..." and name closely related domains or edge cases that belong to other tools or standard agent reasoning.

### Bad example (Vague, summarizes workflow, misses negative boundaries)
```yaml
description: A comprehensive tool that guides users through creating and verifying forms by checking inputs, saving outputs, and providing full walkthroughs.
```

### Good example (Crisp, positive bounds, negative guardrails)
```yaml
description: Extracts fields, fills form values, and validates PDF outputs. Use when parsing PDF templates or populating dynamic form documents. Don't use for raw OCR on scanned images or plain text files.
```

## 5. Three-layer progressive disclosure

Agent skills optimize context consumption across three distinct lifecycle layers:

- **Layer 1. Catalog discovery (Startup).** The agent loads only the `name` and `description` of all registered skills into the system prompt. Token cost is roughly 50 to 100 tokens per skill.
- **Layer 2. Instruction activation (Matching).** When user intent matches the description, the agent reads `SKILL.md`. Keep `SKILL.md` under 250 lines to leave room for user files and tool outputs.
- **Layer 3. Resource execution (On demand).** The agent executes scripts or reads specific files in `references/` and `assets/` only when triggered by explicit instructions in the body.

## 6. Execution discipline for run versus read

Differentiate between deterministic helpers and reference text:
- If a task requires mechanical calculations, schema validation, or text transforms, place an executable script in `scripts/`. Instruct the agent to run the script via shell and inspect the output. Never instruct the agent to view or read the script source code unless debugging the script itself.
- If a task requires architectural guidelines, complex heuristics, or human standards, store them in `references/` as Markdown documents and point the agent to them conditionally.
