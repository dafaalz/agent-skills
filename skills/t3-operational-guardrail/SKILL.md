---
name: t3-operational-guardrail
description: "Use when orchestrating autonomous agent workflows, enforcing pre-flight contract boundaries, locking semantic worktree units against subagent collisions, or gating destructive actions behind human approval in T3 Code / Antigravity. Don't use for host-level untrusted sandbox isolation (use Docker/microVM containers) or kernel-level network/userland separation."
---

# T3 Operational Integrity Guardrail

Enforce pre-flight contract boundaries, fail-closed tool dispatching, semantic-unit worktree locking, and context pinning across multi-turn autonomous agent sessions in T3 Code / Antigravity.

Announce the starting stance at session start:
`I am using the t3-operational-guardrail skill to enforce task boundaries and prevent operational friction.`

<HARD-GATE>
Operational Scope Boundary & Threat Model.
1. Cooperative Agent Model: ENFORCED. Protects against agent hallucinations, unintended file overwrites, unapproved tool invocations, accidental branch deletions, worktree discard, semantic worktree collisions across subagents, and goal drift across 200+ turns.
2. Adversarial Host Security Model: EXCLUDED & NOT CERTIFIED. Same-UID processes (including code executed inside allowed interpreters like PHP artisan or npm) share OS user privileges and can bypass userland Python dispatchers. Untrusted code execution requires microVM/container isolation.
3. Destructive Git commands (`git push`, `git reset`) REQUIRE a cryptographically signed HMAC approval token minted via macOS Keychain and consumed via atomic CAS.
4. Git flags that discard working tree state (`checkout -- .`, `branch -D`, `commit --amend`, `clean -fd`, `restore`, `switch --discard-changes`, `-C`, `-B`, `-S`, `--no-index`, `--output`) are strictly prohibited (EC 73/74).
5. All safe Git invocations MUST have hooks and external drivers neutralized via injected `-c` flags and reject any user-supplied `-c` or `--config` flags.
6. All shell command executions, tool invocations, and file mutations MUST strictly route through `t3_dispatch.py` or ACP Gateway harness. Direct native-tool writes or edits that bypass dispatch mediation are prohibited.
7. Direct mutation or forgery of verification receipts (`.agents/state/`, `verification-receipt.json`, `receipt-hash.txt`) and iteration budget counters (`iteration_counter.json`) is strictly prohibited and denied fail-closed with Exit 80 (`EC_CONTROL_ARTIFACT_TAMPER`).
8. Hard session loop budget is capped at 250 iterations via cross-process atomic file locking (`fcntl.flock`). Dispatches exceeding the budget fail-closed with Exit 89 (`EC_LOOP_BUDGET_EXCEEDED`).
</HARD-GATE>

## Dual Threat Model Matrix

| Threat Model | Status | Target Surface | Enforcement Mechanism |
|---|---|---|---|
| **Cooperative Autonomous Agent** | **PASS & ENFORCED** | ACP/MCP Tool-Call Interface | Pre-flight brief linting, closed subcommand allowlists, flag denial matrix, semantic worktree locking, message-slot context pinning, and attestation. (Note: Runtime attestation is cooperative-only and self-referential against same-UID host compromise). |
| **Malicious Host Adversary** | **FAIL (Excluded)** | OS Process & Kernel Boundaries | Cannot be mitigated under single-user POSIX execution. Requires microVM/container isolation (Docker/Firecracker). |


## Target Environment & Intentional Exclusions (Cooperative Model Boundary)

1. **Closed Git Configuration Surface**: To eliminate arbitrary unmediated code execution vectors, custom user-installed diff/merge drivers, git-lfs, and executable INI sections ([filter], [diff], [merge], [pager], [gpg], [url], [credential]) are strictly prohibited and neutralized. Projects requiring Git-LFS or external diff tools must run those outside the autonomous agent tool boundary.
2. **User Git Config Protection**: User-level git configurations (~/.gitconfig and ~/.config/git/config) are classified as protected paths: modification is blocked (EC 80) and unauthorized read is blocked (EC 76).
3. **Attestation Self-Referentiality**: Runtime attestation (verify_runtime_attestation) verifies control binary digests against trusted_root_hashes.json. Under the cooperative model, the ledger is protected against tool-call mutation via is_control_path() (EC 80). Against an adversarial unmediated process with same-UID host access, this boundary is conceded under the Dual Threat Model.
4. **Signature Inspection Double-Defense**: Defense-in-depth on GPG signature inspection. Although gpg.program=true in enforcing_configs neutralizes external signature verification execution, any invocation containing --show-signature or format specifiers with %G / %g is proactively denied at dispatch (EC 73) to prevent spawning the verification subsystem.
5. **Scoped Git Commit & Component-Wise Target Enforcement**: Blanket staging flags on git commit (-a, --all, --include, -i, -p, -e, --edit) are prohibited (EC 74). Explicit staging and file mutations are strictly restricted to manifest targets via component-wise resolved path comparison, rejecting suffix-similarity bypasses (EC 79).
6. **Interpreter Code Execution Boundary**: Unmediated arbitrary code execution through repository-controlled interpreter scripts or package test runners (`npm run test`, `php artisan test`, `node oxlint`) runs under the same OS user privileges (same-UID) and is explicitly excluded from the guardrail boundary. This boundary is conceded under the Dual Threat Model.
7. **Intentional Over-Blocking of Exclusion Pathspecs**: Exclusion pathspecs (`:!pattern` or `:(exclude)pattern`) that target sensitive paths (e.g., `git log -p ':!config/app.php'`) are deliberately rejected fail-closed (EC 76). While an exclusion pathspec semantically avoids printing the targeted file, distinguishing safe inverse queries from potential bypasses is omitted in favor of strict fail-closed boundary enforcement.
8. **Scope of History Inspection vs. Path-Bound Reads**: General Git history inspection (e.g., bare `git log -p HEAD`) is not scoped to task manifest targets; under the cooperative model, read operations are permitted broadly across the codebase, while secret path access filters explicitly defend against targeted disclosure of sensitive credentials (`.env`, `config/app.php`, keys).
9. **Tilde and Shell Stack Expansion Limits**: Shell directory stack tokens (`~+`, `~-`) are not expanded by Python runtime tools and remain unexpanded literals. Segment-level tildes (`~user`, `~path`) are treated defensively as backup markers and stripped during path normalization rather than expanded into alternate user homes, enforcing a strict safe-direction boundary.

## Core Modules & Architecture

The guardrail is structured into discrete Python stdlib-only modules located in `scripts/`:

| Component | File | Responsibilities | Exit Codes |
|---|---|---|---|
| **ACP Gateway** | `scripts/t3_acp_gateway.py` | Intercepts ACP JSON-RPC wire calls (`tools/call`, `terminal/create`, `fs/read_text_file`, `fs/write_text_file`). Maintains append-only hash-chained ledger and verifies runtime attestation. | 75, 76, 78, 80 |
| **Dispatcher** | `scripts/t3_dispatch.py` | Fail-closed argument parser, closed subcommand allowlists, shell metacharacter rejection, combined-option blocking, and Git flag safety enforcement. | 70-77, 79, 80 |
| **Approval Gate** | `scripts/t3_approval.py` | Mints and verifies single-use HMAC-SHA256 tokens with atomic CAS replay protection backed exclusively by macOS Keychain (`service: t3-approval-key`). | 75 |
| **Brief Linter** | `scripts/t3-brief-lint.py` | Validates initial task briefs before work starts (mode, explicit targets, design anchor existence, tool allowlists, symlink denial). | 84-88 |
| **Worktree Queue** | `scripts/t3_worktree_queue.py` | Enforces semantic-unit atomic locking (e.g., Controller + Blade partial pair) preventing interdependent file collisions across subagents. | 81 |
| **Model Router** | `scripts/t3_router.py` | Tracks model availability and API errors (503/429), tripping an open-circuit fail-closed breaker after 3 consecutive failures. | 78, 83 |

## Reference modules

Load reference manuals on demand based on task context:

| Concern | Reference file |
|---|---|
| Technical defect catalog and mitigations | [references/flaws-resolution.md](references/flaws-resolution.md) |
| Adversarial test matrix (64 cases) | [references/adversarial-matrix-evidence.md](references/adversarial-matrix-evidence.md) |

---

## De-collided Exit Codes Reference (20 Codes: 70-89)

Diagnostic exit codes are strictly de-collided across all execution phases (20 unique exit codes):

- **70**: Shell Metacharacter or Chaining Operator (`&&`, `;`, `\|`, `` ` ``, `$()`, `>`, `<`)
- **71**: Empty or Whitespace-only Command String
- **72**: Denied Binary / Interpreter Spawner (`awk`, `ruby`, `python3 -c`, `php -r`, `node -e`, unapproved script)
- **73**: Destructive Git Flag (`-D`, `--amend`, `-fd`, `-f`, `--discard-changes`), combined/redirection flag (`-c`, `-C`, `-B`, `-S`, `--output`), or Environment Variable Override (`GIT_CONFIG_*`, `GIT_EXTERNAL_DIFF`)
- **74**: Forbidden Git Subcommand (`remote`, `clone`, `fetch`, `tag`, `config`, `worktree`, `clean`, `stash`, `reflog`, `gc`, `restore`), missing `-m` on commit, or path checkout
- **75**: Destructive Action Missing Valid HMAC Approval Token (`git push`, `git reset`)
- **76**: Secret Path Access (`.env`, `id_rsa`) or Unauthorized Network Egress Domain
- **77**: Direct Environment Variable Dump Binary (`env`, `printenv`)
- **78**: Router Circuit Breaker Open (Mutation Fail-Closed during API outage)
- **79**: File Mutation Target Outside Manifest Scope (`edit_file`, `create_file`)
- **80**: Control Artifact Tampering (`.git`, `node_modules`, `package.json`, `.github/`, scripts, ledgers)
- **81**: Subagent Semantic-Unit Worktree Conflict (Atomic lock held by another session)
- **82**: Task Manifest SHA-256 Digest Mismatch (Tamper Abort)
- **83**: Model Probe Failure / Unregistered Model Tier
- **84**: Lint-Phase Agent-Supplied Session ID Injection Rejection
- **85**: Lint-Phase Target Path Directory Traversal or Absolute Path Rejection
- **86**: Lint-Phase Missing Design Anchor File Rejection
- **87**: Lint-Phase Unauthorized Tool Request Rejection
- **88**: Lint-Phase Symlink Target Rejection
- **89**: Hard Session Execution-Loop Budget Exceeded (Dispatched tool calls exceed 250 iterations)

---

## Standard Workflow

### 1. Pre-Flight Task Brief Linting
Before spawning an autonomous implementation thread, generate and lint the task brief:
```bash
python3 scripts/t3-brief-lint.py path/to/task-brief.json
```
If linting passes (Exit 0), an isolated session manifest is minted at `~/Library/Application Support/t3/sessions/<session_id>/task-manifest.json`.

### 2. Multi-Subagent Semantic Locking
When dispatching multiple subagents working on coupled layers (e.g., a Laravel Controller and its Blade partial):
```bash
# Session A acquires lock
python3 scripts/t3_worktree_queue.py register session_A user-feature app/Http/Controllers/UserController.php,resources/views/user/index.blade.php

# Session B attempting to touch the same Blade partial exits 81:
python3 scripts/t3_worktree_queue.py register session_B user-view resources/views/user/index.blade.php # -> Exits 81
```

### 3. Human Approval for Destructive Push/Reset
Destructive actions are blocked fail-closed with Exit 75. To authorize an intentional push:
```bash
# Minter generates single-use token backed by macOS Keychain:
python3 scripts/t3_approval.py mint <session_id> "git push"

# Dispatcher verifies and consumes token via atomic CAS:
python3 scripts/t3_approval.py verify <session_id> "git push" # -> Exits 0, single-use token atomically deleted
```

### 4. Compaction Context Retention
During long-running multi-turn sessions (200+ turns), anchor the task constraint block in the message-history stream. If compaction occurs, the supervisor re-injects the manifest ground truth at message slot 1 to eliminate goal drift.
