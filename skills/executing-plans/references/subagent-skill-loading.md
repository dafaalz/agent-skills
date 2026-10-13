# Subagent skill loading and domain mapping

Mandatory procedures for mapping task domains to skills, injecting skill requirements into subagent prompts, and verifying compliance.

## 1. Domain to skill mapping

When delegating tasks to subagents, the orchestrator must map each task to applicable skills and reference documents.

| Task domain | Mandatory primary skills | Required reference documents |
|---|---|---|
| Automated testing and fixtures | `testing-patterns` | `references/frontend-patterns.md`, `references/backend-patterns.md`, `references/tdd-anti-patterns.md` |
| Frontend UI, layouts, and components | `frontend-design`, `ui-motion` | `references/structure.md`, `references/ui-patterns.md`, `references/impeccable-delta.md` |
| Backend services, APIs, and domain logic | `codebase-design`, `security-audit` | `references/attack-classes.md`, `references/web-protocol-and-auth.md` |
| Internationalization and locale formatting | `i18n` | `references/locale-negotiation.md`, `references/bidi-rtl.md` |
| Security audits and auth boundaries | `security-audit` | `references/hunting.md`, `references/validation-and-reporting.md` |
| Code review and diff inspection | `code-review` | `references/pull-request-review.md` |
| Documentation and prose | `unslop`, `technical-writing` | `references/slop-patterns.md`, `references/indonesian-patterns.md` |
| Performance optimization | `react` (if React or Next.js) | `references/waterfalls.md`, `references/bundle-size.md` |

## 2. Orchestrator delegation protocol

The orchestrator executes this sequence before dispatching an implementer:

1. Analyze task files and behavioral requirements to identify all applicable domains.
2. Locate installed skill paths in the workspace configuration (`skills/` or provider skill directories).
3. Extract absolute paths for each primary `SKILL.md` and required `references/` files.
4. Insert the `## Required Skill Ingestion` block into the subagent prompt template.
5. Instruct the subagent that reading these skills via `view_file` is a mandatory prerequisite before editing any codebase files.

## 3. Subagent compliance verification

The implementer subagent must execute the following sequence:

1. Call `view_file` on each mandated `SKILL.md` path.
2. Call `view_file` on each referenced guide relevant to the specific task.
3. State in its initial response turn which skills were ingested and what core constraints apply to the task.
4. Only then proceed to inspect code, run baseline tests, and author modifications.

If an implementer begins editing files without ingesting mandated skills, the orchestrator halts execution, provides the skill paths, and re-dispatches the subagent.

## 4. Prompt injection template

Insert this exact block into the implementer dispatch prompt:

```markdown
## Required Skill Ingestion

Before reading codebase files or writing code, read these mandatory skills and their reference files using view_file:
- Skill: [absolute path to SKILL.md]
  References: [absolute paths to references/*.md]

Confirm that you loaded these skills in your first turn before writing code.
```
