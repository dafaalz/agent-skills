# Conventional Commit Types

Reference guide for conventional commit types, boundary conditions, and ordering.

## Type Taxonomy

Choose exactly one type per commit. The type describes the intent of the change, not the file extension or path.

| Type | Intent | Included Examples | Excluded Examples |
| --- | --- | --- | --- |
| `feat` | New capability | New API route, user feature, CLI command | Internal refactoring without new capability |
| `fix` | Bug fix | Resolving regression, null check, memory leak | Changing working behavior to a new design |
| `docs` | Documentation | README updates, typedoc, architectural notes | Code comments delivered alongside a feature |
| `style` | Formatting | Whitespace cleanup, prettier formatting, semicolons | Code restructuring that modifies AST |
| `refactor` | Structural redesign | Extracting functions, simplifying complexity | Fixes paired with refactoring (split them) |
| `perf` | Performance improvement | Query optimization, caching, memory efficiency | General refactor with incidental speed gain |
| `test` | Automated tests | Unit tests, e2e test cases, test fixtures | Application code modified to pass tests |
| `build` | Build system and dependencies | Manifest updates, lockfiles, bundler config | Internal application scripts |
| `ci` | Continuous integration | GitHub Actions, pipeline workflows, CI scripts | Local developer tooling |
| `chore` | Maintenance tasks | Tool configuration, gitignore updates | User-visible behavior or features |
| `revert` | Revert commit | Rolling back a previous git commit SHA | Forward bug fixes that repair regressions |

## Disallowed Types

Never invent custom types such as `wip`, `update`, `improvement`, `misc`, or `clean`. If a commit seems to require multiple types, split it into separate commits.

## Commit Order for Split Changes

When a working tree contains multiple types, stage and commit them in this sequence:

1. Build and configuration changes (`build`, `ci`, `chore`)
2. Mechanical refactoring and renames (`refactor`)
3. Behavioral changes (`feat`, `fix`, `perf`)
4. Independent test additions (`test`)
5. Documentation updates (`docs`)
