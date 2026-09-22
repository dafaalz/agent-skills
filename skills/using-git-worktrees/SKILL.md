---
name: using-git-worktrees
description: Use when starting feature work needing workspace isolation or before executing implementation plans, creating isolated git worktrees with directory selection and safety verification.
---

# Using git worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle.** Systematic directory selection and safety verification produce reliable isolation.

Announce at session start:
"I'm using the using-git-worktrees skill to set up an isolated workspace."

## Directory selection process

Follow this priority order:

### 1. Check existing directories

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found.** Use that directory. If both exist, `.worktrees` wins.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**If preference specified.** Use it without asking.

### 3. Ask user

If no directory exists and no CLAUDE.md preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## Safety verification

### For project-local directories (.worktrees or worktrees)

Verify the directory is ignored before creating the worktree:

```bash
# Check if directory is ignored (respects local, global, and system gitignore)
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If not ignored:**

Follow the rule to fix broken things immediately:
1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation

This prevents accidentally committing worktree contents to the repository.

### For global directory (~/.config/superpowers/worktrees)

No .gitignore verification needed because it is outside the project entirely.

## Creation steps

### 1. Detect project name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create worktree

```bash
# Determine full path
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Run project setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verify clean baseline

Run tests to ensure worktree starts clean:

```bash
# Examples - use project-appropriate command
npm test
cargo test
pytest
go test ./...
```

**If tests fail.** Report failures, ask whether to proceed or investigate.

**If tests pass.** Report ready.

### 5. Report location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick reference

| Situation | Action |
|---|---|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

## Common mistakes

### Skipping ignore verification

- **Problem.** Worktree contents get tracked, polluting git status.
- **Fix.** Always use `git check-ignore` before creating a project-local worktree.

### Assuming directory location

- **Problem.** Creates inconsistency and violates project conventions.
- **Fix.** Follow directory priority of existing > CLAUDE.md > ask.

### Proceeding with failing tests

- **Problem.** Cannot distinguish new bugs from pre-existing issues.
- **Fix.** Report failures and obtain explicit permission to proceed.

### Hardcoding setup commands

- **Problem.** Breaks on projects using different tools.
- **Fix.** Auto-detect from project manifests like package.json.

## Example workflow

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/, exists]
[Verify ignored, git check-ignore confirms .worktrees/ is ignored]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test, 47 passing]

Worktree ready at /path/to/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## Red flags

**Never:**
- Create a worktree without verifying it is ignored for project-local paths
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip checking CLAUDE.md

**Always:**
- Follow directory priority of existing > CLAUDE.md > ask
- Verify directory is ignored for project-local paths
- Auto-detect and run project setup
- Verify a clean test baseline

## Integration

**Called by:**
- **brainstorming** (Phase 4), required when design is approved and implementation follows
- **subagent-driven-development**, required before executing any tasks
- **executing-plans**, required before executing any tasks
- Any skill needing an isolated workspace

**Pairs with:**
- **finishing-a-development-branch**, required for cleanup after work is complete
