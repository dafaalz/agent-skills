---
name: pull-request
description: "Use when drafting, reviewing, or structuring pull request descriptions with visual summaries, before-and-after verification evidence, and merge-danger risk assessments. Don't use for atomic git commit messages (use conventional-commit), branch cleanup (run `git branch -d` directly), or direct git push (run `git push` directly after the user reviews the diff)."
allowed-tools: Bash Read Grep Glob
---

# Pull request

Structure pull request bodies that convey intent immediately to reviewers, provide before-and-after verification evidence, and classify operational merge risk.

<HARD-GATE>
Write-Target Boundary. In Draft mode, write only to `.agents/state/pull-request/pr-body.md` and `.agents/state/pull-request/`. In Audit mode, do not modify any tracked codebase file. Never run `gh pr create`, `git push`, `git commit`, `gh api` with state-changing methods, `gh pr comment`, `gh release`, or any other network mutation; emit the publish command as text for the user to run. Never alter application code, execute destructive git resets, or amend previous session commits while drafting.
</HARD-GATE>

## Boundary isolation

Pull request authoring reads git diffs, commit histories, review notes, and test receipts. In Draft and Audit modes, do not execute `git push`, `gh pr create`, or any network mutation. The publish command in Step 5 is emitted as text for the user to run, not executed by the skill. If the user asks the skill to run the publish command, refuse and provide the resolved command to the user.

## Principles and constraints

1. Smallest visual summary. Open the pull request with the smallest visual artifact that makes the change clear: an ASCII diagram, a schema diff table, or terminal before-and-after logs.
2. Concrete verification evidence. Include exact test commands, exit codes, and output snippets. Never assert that changes work without recorded tool verification.
3. Merge-danger call. Classify every pull request as a two-way door (reversible without state corruption) or a one-way door (destructive migrations, auth alterations, external webhook updates) with an explicit blast radius estimate.
4. Operational deploy sequencing. For SQL schema alterations, declare the expand-contract phase, lock timeouts, and backward compatibility during rolling rollouts.
5. Ingest repository templates. When `.github/pull_request_template.md` or templates under `.github/PULL_REQUEST_TEMPLATE/` exist, populate that layout instead of replacing repository structure.
6. Secret and credential protection. Scan diff lines directly in stream for private keys and tokens without persisting raw secrets to disk. On match, write a blocking state marker, redact raw values from reports, halt drafting, keep git state untouched, and alert the user with file paths. Remove `.agents/state/pull-request/HALT_SECRET` manually after remediating commits.
7. Unslop compliance. Zero em dashes, zero en dashes, and zero hyphens acting as dashes. Use colons only before lists, tables, or code blocks.
8. Line budget. Keep the main pull request template concise and under 250 lines.

## Modes

Run Steps 1 through 5 in Draft mode (default) or Steps A1 through A3 in Audit mode.

## Draft workflow

### Step 1. Base branch resolution, diff inspection, and commit audit

Inspect branch divergence against target base branch before drafting. Abort if a prior unhandled `HALT_SECRET` marker exists on disk:

```bash
set -o pipefail; mkdir -p .agents/state/pull-request
[ -f .agents/state/pull-request/HALT_SECRET ] && { printf 'FATAL: HALT_SECRET marker exists. Remediate commits and remove marker before rerunning.\n' >&2; exit 1; }

CANDIDATE_BASE="${STACK_BASE:-}"
if [ -z "${CANDIDATE_BASE}" ]; then
  UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null) && CANDIDATE_BASE="${UPSTREAM}"
  for r in $(git remote 2>/dev/null); do
    SYM=$(git symbolic-ref --short "refs/remotes/${r}/HEAD" 2>/dev/null)
    [ -z "${CANDIDATE_BASE}" ] && [ -n "${SYM}" ] && CANDIDATE_BASE="${SYM}" && break
  done
  TRUNKS=$(git branch -r 2>/dev/null | tr -d ' ' | grep -E '^[^/]+/(main|master|trunk|develop)$' || true)
  [ -z "${CANDIDATE_BASE}" ] && [ "$(printf '%s\n' "${TRUNKS}" | grep -c . || true)" -eq 1 ] && CANDIDATE_BASE="${TRUNKS}"
fi

is_branch=0
case "${CANDIDATE_BASE}" in
  refs/heads/*|refs/remotes/*) git show-ref --verify --quiet "${CANDIDATE_BASE}" 2>/dev/null && is_branch=1 ;;
  ?*)
    git show-ref --verify --quiet "refs/heads/${CANDIDATE_BASE}" 2>/dev/null && is_branch=1
    git show-ref --verify --quiet "refs/remotes/${CANDIDATE_BASE}" 2>/dev/null && is_branch=1
    for r in $(git remote 2>/dev/null); do git show-ref --verify --quiet "refs/remotes/${r}/${CANDIDATE_BASE}" 2>/dev/null && is_branch=1; done ;;
esac
[ "${is_branch}" -eq 1 ] && git rev-parse --verify "${CANDIDATE_BASE}^{commit}" >/dev/null 2>&1 || {
  printf 'FATAL: Base ref %s is not a valid branch commit. Set STACK_BASE=<branch> to disambiguate.\n' "${CANDIDATE_BASE}" >&2; exit 1; }

TARGET_BRANCH="${CANDIDATE_BASE}"
case "${TARGET_BRANCH}" in refs/heads/*) TARGET_BRANCH="${TARGET_BRANCH#refs/heads/}" ;; esac
if ! git show-ref --verify --quiet "refs/heads/${TARGET_BRANCH}" 2>/dev/null; then
  for r in $(git remote 2>/dev/null); do
    case "${TARGET_BRANCH}" in
      refs/remotes/"${r}"/*) C_SHORT="${TARGET_BRANCH#refs/remotes/${r}/}" ;;
      "${r}"/*) C_SHORT="${TARGET_BRANCH#${r}/}" ;;
      *) continue ;;
    esac
    git show-ref --verify --quiet "refs/remotes/${r}/${C_SHORT}" 2>/dev/null && TARGET_BRANCH="${C_SHORT}" && break
  done
fi

git check-ref-format --branch "${TARGET_BRANCH}" 2>/dev/null || { printf 'FATAL: Invalid branch format for target: %s\n' "${TARGET_BRANCH}" >&2; exit 1; }
printf '%s' "${TARGET_BRANCH}" > .agents/state/pull-request/base-ref.txt && printf '%s' "${CANDIDATE_BASE}" > .agents/state/pull-request/candidate-base.txt
git log "${CANDIDATE_BASE}"..HEAD --oneline > .agents/state/pull-request/commit-log.txt && git diff "${CANDIDATE_BASE}"...HEAD --stat > .agents/state/pull-request/diff-stat.txt || {
  printf 'FATAL: Failed to read git history against %s.\n' "${CANDIDATE_BASE}" >&2; exit 1; }

git diff "${CANDIDATE_BASE}"...HEAD --name-only > .agents/state/pull-request/changed-files.txt
SECRET_FILES=$(grep -E '(^|/)(\.env(\.[^/]+)?|\.envrc|credentials([-_.]?[^/]+)?\.json|id_rsa$|[^/]+\.(pem|key))$' .agents/state/pull-request/changed-files.txt | grep -vE '(\.(pub|example|sample|template)(\.json)?|[-_]template.*)$' || true)
[ -n "${SECRET_FILES}" ] && { touch .agents/state/pull-request/HALT_SECRET; printf 'HALT: Sensitive credential or key file in diff.\n' >&2; exit 1; }

git diff "${CANDIDATE_BASE}"...HEAD | awk '
  /^diff --git/ { in_file=1; next }
  in_file && /^\+\+\+ / {
    in_file = 0; if ($0 ~ /^\+\+\+ \/dev\/null/) next
    line = $0; sub(/^\+\+\+ "?b\//, "", line); sub(/"?$/, "", line); file = line; next
  }
  /^@@ -[0-9]+(,[0-9]+)? \+([0-9]+)/ {
    split($3, hunk, ","); lineno = substr(hunk[1], 2) + 0 - 1; next
  }
  /^\+/ && !in_file {
    lineno++; line = substr($0, 2)
    if (line ~ /(gh[pousr]_[a-zA-Z0-9]{20,}|github_pat_[a-zA-Z0-9_]{22,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[0-9a-zA-Z]{10,48}|sk-(proj-)?[a-zA-Z0-9_-]{32,}|AIza[0-9A-Za-z_-]{35}|sk_live_[0-9a-zA-Z]{24}|[Bb][Ee][Aa][Rr][Ee][Rr][[:space:]]+[a-zA-Z0-9_.-]+)/) {
      matched = 1
      print "HALT: Credential pattern matched at " file ":" lineno ":[REDACTED_SECRET_MATCH]"
    }
  }
  /^ / && !in_file { lineno++ }
  END { if (matched) exit 42 }
' > .agents/state/pull-request/secret-scan.txt
SCAN_STATUS=$?
[ "${SCAN_STATUS}" -eq 42 ] && { touch .agents/state/pull-request/HALT_SECRET; cat .agents/state/pull-request/secret-scan.txt >&2; exit 1; }
[ "${SCAN_STATUS}" -ne 0 ] && { printf 'FATAL: Secret scan pipeline failed with exit status %d.\n' "${SCAN_STATUS}" >&2; exit 1; }
```

Identify modified subsystems, schema migrations, breaking changes, and conventional commit adherence.

Completion criterion. `test -s .agents/state/pull-request/base-ref.txt`, `test -s .agents/state/pull-request/commit-log.txt`, `test -s .agents/state/pull-request/diff-stat.txt`, `test -f .agents/state/pull-request/secret-scan.txt`, `test ! -s .agents/state/pull-request/secret-scan.txt`, and `test ! -f .agents/state/pull-request/HALT_SECRET` evaluate successfully.

### Step 2. Visual summary formulation

Before drafting, abort if `.agents/state/pull-request/HALT_SECRET` exists on disk.
Construct smallest visual representation that explains core change: ASCII data flow diagram, schema diff table, screenshot table, or command output block.
Completion criterion. One compact visual representation drafted communicating primary delta.

### Step 3. Merge-danger and blast radius assessment

Evaluate operational risk before assembling final description. Consult `references/operational-risk-and-runners.md` for definitions:
- Decision type: Two-way door or One-way door.
- Blast radius: Low, Medium, or High.
- Rollback plan: Exact `git revert <hash>` or multi-step operational recovery plan.
- For schema alterations, specify expand-contract phase, backward compatibility, and lock limits. For non-database changes, specify storage or cache rollback plans.

Completion criterion. Merge-danger classification, blast radius, rollback plan documented, and SQL deploy invariants specified for schema alterations.

### Step 4. Verification evidence compilation

Gather deterministic verification results:
```bash
RUNNER_CMD=""
for pair in "pnpm-lock.yaml:pnpm test" "yarn.lock:yarn test" "bun.lockb:bun test" "package-lock.json:npm test" "poetry.lock:poetry run pytest" "uv.lock:uv run pytest" "Pipfile.lock:pipenv run pytest" "composer.lock:vendor/bin/phpunit" "go.mod:go test ./..." "Cargo.lock:cargo test"; do
  lf="${pair%%:*}"
  if [ -f "${lf}" ]; then RUNNER_CMD="${pair#*:}"; break; fi
done
if [ -n "${RUNNER_CMD}" ]; then
  printf '%s\n' "${RUNNER_CMD}" > .agents/state/pull-request/test-command.txt
  eval "${RUNNER_CMD}" > .agents/state/pull-request/test-output.txt 2>&1
  TEST_EXIT=$?; printf '%d\n' "${TEST_EXIT}" > .agents/state/pull-request/test-status.txt && [ "${TEST_EXIT}" -eq 0 ] || { printf 'FATAL: %s failed with code %d.\n' "${RUNNER_CMD}" "${TEST_EXIT}" >&2; exit 1; }
else
  git status -s > .agents/state/pull-request/verification-evidence.txt
fi
```
Completion criterion. `([ -f .agents/state/pull-request/test-status.txt ] && [ "$(cat .agents/state/pull-request/test-status.txt)" -eq 0 ] && [ -s .agents/state/pull-request/test-output.txt ]) || [ -s .agents/state/pull-request/verification-evidence.txt ]` evaluates successfully.

### Step 5. Body assembly and registration

Assemble pull request description: ingest repository template if `.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE/` exists, populating its layout and appending missing visual summary and verification sections; otherwise use default layout below.

Write assembled description to temporary file and append stack navigation if `.agents/state/pull-request/stack.json` exists:
```bash
cat <<'BODY_EOF' > .agents/state/pull-request/pr-body.md.tmp
<assembled markdown description matching repository template or standard layout below>
BODY_EOF
PR_NUM=$(grep -Eo '"parent_pr"[ ]*:[ ]*[0-9]+' .agents/state/pull-request/stack.json 2>/dev/null | grep -Eo '[0-9]+' || true)
[ -s .agents/state/pull-request/stack.json ] && [ "$(printf '%s\n' "${PR_NUM}" | grep -c . || true)" -eq 1 ] && \
  printf '%s' "${PR_NUM}" | grep -Eq '^[1-9][0-9]*$' && \
  printf '\n\n## Stack\n- #%s (Base layer)\n- Current PR (This branch)\n' "${PR_NUM}" >> .agents/state/pull-request/pr-body.md.tmp
mv -- .agents/state/pull-request/pr-body.md.tmp .agents/state/pull-request/pr-body.md
```

Validate base branch and display publish command for user. Never run `gh pr create` directly:
```bash
[ -s .agents/state/pull-request/base-ref.txt ] || { printf 'FATAL: Missing base-ref.txt. Rerun Step 1.\n' >&2; exit 1; }
BASE_REF=$(cat .agents/state/pull-request/base-ref.txt); CAND_REF="${BASE_REF}"
[ -s .agents/state/pull-request/candidate-base.txt ] && CAND_REF=$(cat .agents/state/pull-request/candidate-base.txt)
if git check-ref-format --branch "${BASE_REF}" 2>/dev/null && git rev-parse --verify "${CAND_REF}^{commit}" >/dev/null 2>&1; then
  printf 'Suggested publish command for user:\ngh pr create --base "%s" --title "type(scope): description" --body-file "$(pwd)/.agents/state/pull-request/pr-body.md"\n' "${BASE_REF}"
else
  printf 'FATAL: Stale or invalid base branch %s. Rerun Step 1.\n' "${BASE_REF}" >&2; exit 1
fi
```

Register pull request URL immediately when collaborative harness supports PR tracking.

Completion criterion. `test -s .agents/state/pull-request/pr-body.md`, `[ "$(wc -c < .agents/state/pull-request/pr-body.md)" -gt 200 ]`, and `grep -q '^## Summary' .agents/state/pull-request/pr-body.md && grep -q '^## Verification evidence' .agents/state/pull-request/pr-body.md` evaluate successfully.

## Audit workflow

### Audit Step A1. Load and parse target description

Read target PR body from `.agents/state/pull-request/pr-body.md` or path in `.agents/state/pull-request/audit-target.txt`.
Completion criterion. `test -s .agents/state/pull-request/pr-body.md || (test -f .agents/state/pull-request/audit-target.txt && test -s "$(cat .agents/state/pull-request/audit-target.txt)")` evaluates successfully.

### Audit Step A2. Rubric pass

Evaluate each of the eight Principles and constraints. Record evaluation rows in `.agents/state/pull-request/audit-report.md` with columns `Principle | Status (pass or fail) | Evidence`.
Completion criterion. `test -s .agents/state/pull-request/audit-report.md && [ "$(grep -c '^|' .agents/state/pull-request/audit-report.md)" -ge 10 ]` evaluates successfully.

### Audit Step A3. Verdict

Emit `.agents/state/pull-request/audit-verdict.txt` containing a single line: `verdict: approve` or `verdict: changes_requested`.
Completion criterion. `test -f .agents/state/pull-request/audit-verdict.txt && grep -Eq '^verdict: (approve|changes_requested)$' .agents/state/pull-request/audit-verdict.txt` evaluates successfully.

## Pull request template

Use this standard layout for `.agents/state/pull-request/pr-body.md` when no repository template is present:

````markdown
## Summary
[One to two sentences stating objective and mechanism]

### Visual summary
```text
[ASCII diagram, schema delta, or before-and-after flow]
```

## Changes
- [Component]: [Exact change applied]
- [Test]: [Regression test added]

## Merge danger and operational risk
- **Decision type:** [Two-way door | One-way door]
- **Blast radius:** [Low | Medium | High]
- **Rollback strategy:** [git revert <hash> | specific rollback steps]

<!-- Include following block if change alters database schema -->
### Operational deploy invariants
- **Expand-contract phase:** [Phase 1 Expand | Phase 2 Backfill | Phase 3 Read Cutover | Phase 4 Contract]
- **Backward compatibility:** [Verified with existing running instances]
- **Database lock limits:** [SET lock_timeout = '2s'; index CONCURRENTLY]

## Verification evidence
```text
[Command run and test runner output confirming exit code 0]
```

## Related issues
Closes #[Issue Number]
````

## Quick audit checklist

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| PR-1 | No visual summary | PR body contains only prose bullets | Reviewers must reconstruct the change from the diff | Insert ASCII diagram, schema table, or terminal delta at the top |
| PR-2 | Unclassified danger | PR body lacks decision type, blast radius, or rollback strategy | Reviewer cannot judge merge risk | Add the Merge danger section with decision type, blast radius, and rollback strategy |
| PR-3 | No rollback | Rollback strategy field absent or empty | Reviewer cannot plan reversal | Cite git revert or an explicit rollback procedure |
| PR-4 | Asserted verification | Verification claims stated without command output | Claims are not reproducible | Paste the exact command and its exit code 0 output |
| PR-5 | Malformed title | PR title missing standard type or scope | Breaks changelog automation | Match `<type>(<scope>): <description>` format |
| PR-6 | Secret leak | Added diff lines contain credentials or private tokens | Secret exposure on push | Remediate commit history, remove HALT_SECRET marker manually, and rerun Step 1 |
| PR-7 | Unsequenced migration | SQL schema alteration PR lacks deploy invariants | Risk of downtime or table lock during rollout | Specify expand-contract phase, lock limits, and backward compatibility |
| PR-8 | Template ignored | Overwrites repository PR template | Destroys team compliance checks | Ingest and populate fields in `.github/pull_request_template.md` or directory template |
