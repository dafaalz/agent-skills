# Scope and diff analysis

Resolve the exact review boundary, blast radius, and regression signals before evaluating code.

## 1. Scope resolution

Determine the review target from user input or git state:

1. Target explicitly specified by user (branch, PR, or commit range). Inspect that target directly.
2. Target omitted:
   - Check commit status against default branch (`git merge-base origin/main HEAD`). Inspect that range plus uncommitted changes.
   - If not ahead, inspect dirty working tree via `git status --short`.
   - If working tree is clean, stop and prompt the user for a branch or ask whether to run a full repository audit.
3. Exclude lockfiles, minified bundles, snapshots, generated schemas, and vendored code. List excluded files in the report header.

## 2. Blast radius expansion

A changed file is evidence, not the entire surface. Inspect the consumers:

- Expand one hop for standard components. Inspect direct consumers, parent layouts, and callers.
- Expand two hops for shared primitives. Inspect design tokens, global themes, or foundational input components.
- Cap consumer inspections at five files. State the number of uninspected consumers when skipping occurs.

## 3. Removed lines and regression signals

Inspect deleted lines in diff hunks. Flag removed safeguards immediately:

- Removed accessibility attributes, labels, or focus traps.
- Removed keyboard event handlers for Enter, Space, or Escape keys.
- Removed responsive wrappers, container queries, or mobile break points.
- Removed fallback states for loading, empty data, or network errors.
- Replacement of semantic tokens with hardcoded color values.
