---
name: security-audit
description: Use when auditing codebases for security vulnerabilities, conducting threat modeling, reviewing auth boundaries, evaluating exploitability, or verifying security fixes. Don't use for feature development, code formatting, or routine dependency upgrades.
---

# Security audit

Find source-grounded vulnerabilities that violate a real trust boundary, then give owners source evidence, safe reproduction steps, priority calibration, and the smallest effective fix. This is a defensive, source-first workflow. A candidate without an affected principal, concrete resource, and observable security outcome is not a confirmed finding.

## Operating modes

This skill operates in guidance mode by default. Loading it does not authorize unsolicited file creation or execution of the full audit workflow.

- Guidance mode. For security questions, focused reviews, methodology checks, triage, or investigating specific findings, use only the relevant parts of this skill. Do not create run directories or audit report files. Launch focused subagents when helpful and return results directly to the active task.
- Full audit mode. Use the complete workflow only when the user explicitly requests an audit of a codebase, asks for an end-to-end security review, or requests formal report artifacts. Run all phases in sequence and write the required artifacts.

When user intent between modes is ambiguous, ask one clarifying question before creating files or starting the full workflow.

## Platform terminology and roles

This skill coordinates specialized agent roles:
- Parent. The orchestrator that owns run metadata, directory setup, and shared state files.
- Task tool. The platform delegation or subagent mechanism.
- Research agent. A read-only subagent for source exploration and factual verification without disk modifications.
- General agent. A delegated subagent for bounded investigation, sandboxed reproduction, and isolated verification.

## Universal execution safety

These invariants apply across all modes. Source inspection is strictly read-only. Run target-controlled builds, tests, processes, browsers, and parsers only inside an OS-enforced sandbox providing:
- No external network access. Use an isolated loopback namespace only when testing local client or server traffic.
- An empty environment populated from an explicit allowlist with safe values, using scratch-local directories for temporary files and caches.
- Read-only target source and toolchain mounts. Target-controlled processes may write only inside their assigned scratch directory.
- Strict limits on CPU, memory, process count, file size, disk usage, and wall-clock duration.

Use dummy principals, fixtures, and tokens. Never probe deployed endpoints, external services, shared infrastructure, production identities, or live control planes. If a decisive fact cannot be evaluated locally or through source analysis, record it as needing validation.

## Full audit setup

In full audit mode, resolve these configuration values before reconnaissance:
- Skill directory. The absolute path to this skill directory.
- Target. The absolute repository root under audit.
- Repo name. A stable repository identifier from the directory or local git remote.
- Output directory. A writable directory outside the target, defaulting to `~/security-audit-skill/<repo-name>/run-<N>`, where `<N>` is the next unused integer.
- Source ref. The reviewed commit hash and worktree status.

### Write isolation

The parent agent creates and exclusively updates shared run files:
- `run-metadata.json`
- `architecture.md`
- `coverage-ledger.json`
- `findings.json`
- `REPORT.md`
- `FINDINGS-DETAIL.md`
- `NEEDS-VALIDATION.md`

Each hunter and verifier receives an isolated workspace under `<output-dir>/agents/<agent-id>/` with separate `scratch/` and `artifacts/` directories. Target-controlled processes write only to `scratch/`. The parent alone promotes allowlisted files to `artifacts/` using descriptor-based no-follow traversal. Review `references/hunting.md` and `references/validation-and-reporting.md` for exact promotion procedures.

## Progressive disclosure and domain guides

Consult specific reference guides on demand based on target architecture:

| Domain or task | Reference file | Trigger conditions |
|---|---|---|
| Attack classes and taxonomy | `references/attack-classes.md` | Baseline injection, access control, SSRF, path traversal |
| Reconnaissance and scoping | `references/reconnaissance.md` | Mapping entry surfaces, trust boundaries, and ledger units |
| Hunter wave coordination | `references/hunting.md` | Dispatching hunter waves and managing agent scratch spaces |
| Verification and reporting | `references/validation-and-reporting.md` | Independent verification, schema validation, and deliverables |
| Web and authentication | `references/web-protocol-and-auth.md` | HTTP framing, cookies, sessions, JWT, OAuth 2.1, OIDC, SAML |
| Client-side and browser | `references/client-side.md` | DOM XSS, prototype pollution, Trusted Types, CSP, postMessage |
| Cloud and deployment | `references/cloud-and-deployment.md` | Cloud IAM, Kubernetes, containers, IMDSv2, ingress, secrets |
| Credentials and secret hygiene | `references/credentials-hygiene.md` | Safe verification, token masking, zero exposure inspection |
| Supply chain and release | `references/supply-chain-and-release.md` | Dependencies, CI workflows, SLSA provenance, build inputs |
| AI, LLM, and agents | `references/ai-and-llm.md` | Prompt assembly, RAG context, MCP servers, tool-call loops |
| Memory safety and binary | `references/memory-safety-and-binary.md` | C, C++, Rust unsafe, FFI, parsers, allocators, race conditions |
| Data isolation and lifecycle | `references/data-isolation-and-lifecycle.md` | Multi-tenancy, BOLA, object links, soft deletion, retention |
| Desktop, mobile, and IPC | `references/desktop-mobile-and-local-ipc.md` | Deep links, webview bridges, Electron, IPC daemons, helpers |
| Protocols, RPC, and messaging | `references/protocols-rpc-and-messaging.md` | gRPC, Protobuf, GraphQL transports, webhooks, message queues |
| Resource exhaustion | `references/resource-exhaustion-and-availability.md` | ReDoS, amplification, memory leaks, queue starvation |
| BaaS and fullstack frameworks | `references/baas-and-fullstack-frameworks.md` | Next.js, Supabase, Firebase, Convex, Prisma, Server Actions |

## Full audit workflow

Follow these seven sequential phases in full audit mode.

### Phase 1. Reconnaissance

Map source structure, trust boundaries, entrypoints, local build paths, and initial coverage units.
- Inspect project configuration, package manifests, route definitions, and permission decorators.
- Select applicable domain companion guides from `references/`.
- Seed the deterministic coverage ledger with initial units.
- Consult `references/reconnaissance.md` for ledger schema and domain selection rules.

Completion criterion. An initial `coverage-ledger.json` seeded with all in-scope boundaries is written to disk.

### Phase 1b. Threat modeling and scoping gate

Align with the user on attack surface priority, trade-offs, and run profile before dispatching hunters.
- Present the mapped trust boundaries, entrypoints, and sensitive assets discovered in Phase 1.
- Formulate 2 to 3 distinct audit approaches with trade-offs. For example, compare a targeted auth and API sweep against deep data lifecycle analysis or a full-spectrum audit.
- State the proposed run profile (`quick`, `standard`, or `deep`) and agent invocation budget.
- Ask clarifying questions one at a time with concrete options and recommendations if scope boundaries or test harnesses require confirmation.
- Wait for explicit user confirmation before proceeding.

Completion criterion. Explicit user approval is recorded for the selected audit approach, scope paths, and run profile.

### Phase 2. Coverage-led hunting waves

Assign ledger units to focused hunter agents in waves.
- Hunter agents inspect source invariants and run sandboxed local checks where safe.
- Hunters output structured JSON candidates containing source traces, proof of concept inputs, and observed results.
- Run a coverage critic wave after hunter execution to identify gaps or reassignments.
- Consult `references/hunting.md` and `references/attack-classes.md` for hunting rules.

Completion criterion. All planned ledger units are resolved to candidate, covered, or deferred states with zero unassigned units.

### Phase 3. Candidate validation

Subject every candidate vulnerability to independent verification.
- Deduplicate candidates by unique vulnerability fingerprint.
- Dispatch fresh, isolated verifier agents with clean contexts for each candidate.
- Verifiers attempt independent reproduction and confirm source invariants.
- Consult `references/validation-and-reporting.md` for verification protocols.

Completion criterion. Every candidate is evaluated by an isolated verifier and assigned a confirmed, needs-validation, or rejected verdict.

### Phase 4. Structured output

Compile verified results into structured machine-readable format.
- Write all final records to `findings.json`.
- Validate findings with `scripts/validate-findings.cjs`.
- Validate coverage claims with `scripts/validate-coverage-ledger.cjs`.

Completion criterion. Both validation scripts execute with exit code 0 against the generated output files.

### Phase 5. Independent record verification

Run a final verification pass across all confirmed records before reporting.
- Fresh agents re-verify that code references and line numbers match current target source.
- Resolve any discrepancies or state changes.

Completion criterion. All confirmed records are verified against the exact target source revision.

### Phase 6. Reporting

Generate human-readable audit deliverables from validated records.
- Produce `REPORT.md` summarizing executive posture, methodology, and coverage metrics.
- Produce `FINDINGS-DETAIL.md` documenting confirmed vulnerabilities with source traces and fixes.
- Produce `NEEDS-VALIDATION.md` listing hypotheses blocked on external environment facts.
- Exclude live probe instructions or exploit payloads targeting external systems.

Completion criterion. All three report markdown files are written to disk matching final validated JSON records.

## Severity calibration

Only confirmed records receive severity ratings. Overall severity must not exceed observed impact:
- critical. An unauthenticated actor gains code execution, full datastore compromise, or arbitrary account takeover.
- high. An actor fully defeats an explicit security control with real consequences, including auth bypass, cross-tenant data access, or stored script execution affecting other users.
- medium. A boundary violation with limited blast radius, uncommon preconditions, or impact restricted to narrow resources.
- low. Disclosure of non-sensitive internal state or effects requiring disproportionate effort for minor impact.
- informational. A confirmed observation with minimal standalone impact, useful as part of defense-in-depth.

## Anti-patterns

1. Presenting checklist omissions as security vulnerabilities without an exploitable boundary.
2. Offering general hardening advice without a demonstrable breach of an invariant.
3. Attempting network testing against external systems or production services.
4. Guessing cloud provider, proxy, or browser behaviors not declared in repository source.
5. Treating authorized same-principal actions as security boundaries.
6. Skipping the Phase 1b scoping gate to launch unaligned hunting waves.
7. Reporting prose-only findings that lack structured reproduction evidence.
8. Modifying target repository code during the audit.
