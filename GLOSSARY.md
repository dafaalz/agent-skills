# Agent Skills Domain Glossary

Canonical vocabulary definitions for the agent skills repository.
Maintained to prevent synonym cycling across agent sessions.

## Core Terms

| Term | Canonical Definition |
|---|---|
| **AgentSkill** | A self-contained markdown directory following the AgentSkills standard, containing a `SKILL.md` entrypoint and optional references. |
| **Context Budget** | The hard limit of at most 250 lines per main `SKILL.md` file to preserve model attention and token efficiency. |
| **Hard Gate** | A non-negotiable declarative boundary block (`<HARD-GATE>`) enforcing state mutation restrictions and directory read-only access. |
| **Operating Mode** | A deterministic execution branch declared before Step 1 that alters workflow behavior (such as Audit mode vs Benchmark mode). |
| **Boundary Isolation** | An explicit section (`## Boundary isolation`) defining strict write permissions and domain invariant protection during skill execution. |
| **Completion Criterion** | A checkable, binary termination condition anchored to a file path, exit code, or commit hash at the end of each numbered step. |
| **R13 Anti-Pattern Table** | A 5-column table schema (`ID \| Title \| Pattern description \| Why it fails \| Concrete fix`) documenting reproducible failure modes. |
| **Validator Independence Rule** | A repository invariant enforced via pre-commit hook preventing commits from touching both validator scripts and skill files. |
| **Standards-Drift Detection (R19)** | A protocol mandating a complete repository re-scan whenever validator rule thresholds or schemas are modified. |
| **Unslop** | The elimination of artificial intelligence patterns, marketing fluff, throat-clearing openings, and decorative dashes from prose. |
