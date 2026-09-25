# Architecture Decision Record: Hallmark Skill Unslop and Modular Refactor

## Status
Accepted

## Context
The hallmark skill located at `skills/hallmark/SKILL.md` guides AI assistants in generating differentiated, high-quality user interfaces. While its underlying design methodology is sound, the document structure violates modern agent authoring and unslop guidelines:

1. **Context sprawl.** `SKILL.md` spans 558 lines (67 KB), exceeding the 250-line limit mandated by Antigravity and `writing-skills` standards.
2. **Punctuation and style violations.** The file contains 138 em dashes, 16 en dashes, and numerous mid-sentence connector colons.
3. **Frontmatter non-compliance.** The description field contains a workflow summary rather than pure trigger conditions starting with "Use when...". A non-standard `version` field is present.
4. **Missing completion criteria.** Operational steps do not conclude with verifiable binary completion criteria.
5. **Promotional phrasing and conversational filler.** The document includes third-party marketing tags and narrative essay text.

## Decision
Refactor `SKILL.md` using progressive disclosure and strict unslop rules:

1. **Primary tier (`SKILL.md`).**
   - Keep the file concise, strictly under 250 lines (target: 160 to 190 lines).
   - Standardize frontmatter with clean operational trigger syntax.
   - Retain core verb routing, universal disciplines, scope checks, and high-level sekuensial execution steps.
   - Add explicit binary completion criteria to every operational step.
   - Point to secondary reference files for deep procedures.

2. **Secondary tier (modular reference files).**
   - Create `references/component-flow.md` to hold the complete single-component workflow, the 8-state interactive checklist, the `.preview.html` wrapper schema, and component stamp formatting.
   - Create `references/pre-flight.md` to hold the 6 signal sources audit, `.hallmark/preflight.json` caching rules, and configuration conflict resolution.

3. **Style and typography enforcement.**
   - Eliminate all em dashes and en dashes. Use commas, periods, or separate sentences.
   - Restrict colons to introducing lists, tables, and code blocks.
   - Enforce sentence case on all headings.
   - Strip banned AI vocabulary, including words such as additionally, crucial, delve, enhance, and vibrant.

## Alternatives Considered

1. **Status Quo.**
   - Maintain the monolithic 558-line file.
   - Rejected because the token overhead degrades agent focus and fails automated compliance tests.

2. **Global Repository Sweep.**
   - Modify `SKILL.md` and simultaneously rewrite all 24 reference files in `references/`.
   - Rejected due to high churn and operational delivery risk. Secondary files are loaded conditionally and can be updated incrementally.

3. **In-place Truncation without New Reference Files.**
   - Condense all material inside `SKILL.md` without extracting sub-files.
   - Rejected because critical component-state and pre-flight instructions would be lost.

## Consequences

- **Positive:** Context window load drops significantly during initial skill discovery and execution.
- **Positive:** Agent determinism improves through explicit completion criteria on every step.
- **Positive:** The skill passes all automated linters and unslop verification tests.
- **Trade-off:** Agents execute one additional file read for component-specific tasks or deep pre-flight edge cases.

## Verification Plan

### Automated Verification
- Create a test script based on `writing-skills/tests/test_writing_skills.py`.
- Verify `SKILL.md` line count is below 250 lines.
- Verify zero em dashes and zero en dashes exist in `SKILL.md`.
- Verify zero banned AI words appear in `SKILL.md`.
- Verify frontmatter starts with `Use when...` and contains valid keys.
- Verify all steps have binary completion criteria.

### Manual Verification
- Verify that default design, audit, redesign, and study workflows preserve all original functional capabilities.
- Confirm links to existing reference files remain valid.
