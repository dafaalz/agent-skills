# Attack classes

Select attack classes relevant to the application type. Not every class applies to every codebase. The list below is an operational baseline. Add application-specific classes from Phase 1 and split large codebases per subsystem. Frame all work as finding, validating, fixing, and prioritizing source-grounded vulnerabilities. Keep validation to source review and bounded local fixtures. Do not develop payload chains, test availability on live services, or take action in shared environments.

Use `confirmed` only when source evidence and bounded validation establish the full boundary and meaningful result. Use `needs_validation` when a specific deployment, provider, platform, identity, or runtime fact is unavailable. State the missing fact and the safe owner-observed or local check that resolves it.

## Authoritative standards and taxonomic mapping

Ground all attack classes and findings in these industry standards:

| Standard or taxonomy | Publishing body | Reference URL | Primary focus |
|---|---|---|---|
| OWASP Top 10:2021 | OWASP Foundation | https://owasp.org/www-project-top-ten/ | Common web application vulnerability categories |
| 2025 CWE Top 25 | MITRE Corporation | https://cwe.mitre.org/top25/ | Most dangerous software weaknesses |
| NIST SP 800-53 Rev. 5 | NIST | https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final | Security and privacy controls |
| MITRE ATT&CK Matrix | MITRE Corporation | https://attack.mitre.org/ | Enterprise adversary tactics and techniques |
| OWASP ASVS v4.0.3 | OWASP Foundation | https://owasp.org/www-project-application-security-verification-standard/ | Technical security verification standards |
| OWASP API Security Top 10 | OWASP Foundation | https://owasp.org/www-project-api-security/ | API-specific vulnerability categories |

### Taxonomy mapping by class

- Injection: CWE-79 (Cross-Site Scripting), CWE-89 (SQL Injection), CWE-78 (OS Command Injection), CWE-94 (Code Injection), CWE-918 (Server-Side Request Forgery).
- Access control: CWE-862 (Missing Authorization), CWE-863 (Incorrect Authorization), CWE-639 (Authorization Bypass Through User-Controlled Key).
- Resource and file handling: CWE-22 (Improper Limitation of a Pathname to a Restricted Directory), CWE-502 (Deserialization of Untrusted Data), CWE-367 (Time-of-check Time-of-use Race Condition).
- Cryptography and secrets: CWE-798 (Use of Hardcoded Credentials), CWE-327 (Use of a Broken or Risky Cryptographic Algorithm), CWE-330 (Use of Insufficiently Random Values).
- Business logic and race conditions: CWE-840 (Business Logic Errors), CWE-362 (Concurrent Execution using Shared Resource with Improper Synchronization).
- Feature abuse and disclosure: CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor), CWE-213 (Exposure of Sensitive Information Due to Incompatible Policies).

## Domain companion selection

Direct specialized target architectures to their companion guides:

- Native, binary, and kernel targets (C, C++, Rust unsafe, kernel modules, parsers, FFI, concurrent runtimes, loaders, JITs, firmware): use `memory-safety-and-binary.md`.
- AI, LLM, and agent targets (chatbots, RAG, persistent memory, tool-calling agents, MCP servers and clients, prompt assembly): use `ai-and-llm.md`.
- HTTP, web, and identity targets (web apps, APIs, reverse proxies, CDNs, gateways, custom parsers, sessions, CSRF, JWT, OAuth 2.1, OIDC, SAML, MFA, passkeys): use `web-protocol-and-auth.md`.
- Client-side and browser targets (SPAs, extensions, webviews, service workers, browser storage, cross-window messaging, CORS, WebSockets, DOM): use `client-side.md`.
- Supply chain and release targets (dependency resolution, generated inputs, CI workflows, signing, promotion, updates, plugins): use `supply-chain-and-release.md`.
- Cloud and deployment targets (IAM, infrastructure as code, containers, Kubernetes, service mesh, serverless, ingress, provider events): use `cloud-and-deployment.md`.
- Protocol, RPC, and messaging targets (gRPC, GraphQL transports, Protobuf, custom protocols, queues, brokers, pub/sub, webhooks): use `protocols-rpc-and-messaging.md`.
- Resource exhaustion and availability targets (CPU, memory, disk, connections, worker pools, queues, quotas, paid APIs): use `resource-exhaustion-and-availability.md`.
- Data isolation and lifecycle targets (multi-tenant stores, search indexes, caches, object links, analytics, export, backup, deletion, retention): use `data-isolation-and-lifecycle.md`.
- Desktop, mobile, and local IPC targets (native apps, deep links, webview bridges, exported components, helpers, daemons, Unix sockets, XPC, Binder, D-Bus): use `desktop-mobile-and-local-ipc.md`.

## Core attack classes

### Injection

Trace untrusted input from entry point to dangerous sink. Identify dangerous sinks by target type:
- Web apps: SQL queries, HTML output, shell commands, template engines, file paths, HTTP redirects, deserialization.
- Libraries: functions processing caller-supplied data without validation, buffer operations, parsers, format strings.
- CLI tools: shell command construction, file path handling, environment variable interpolation.
- Services: query construction, message serialization, log injection, LDAP and XPath queries.
- Client-side: DOM XSS, prototype pollution, cross-origin message handling, and browser-side classes covered in `client-side.md`.

Trace both direct and indirect injection paths. Data stored safely in one location can be retrieved and executed in an unsafe context by another subsystem. Check field names, object keys, request headers, metadata, caches, search indexes, and analytics pipelines.

### Access control

Verify that callers cannot execute actions outside their assigned authority. Test whether permission checks enforce the correct permission on the target resource through the correct mechanism:
- Alternate state change paths that evaluate a weaker permission.
- Request body or parameter values that override server authorization state.
- Endpoints that verify authentication but omit authorization.
- Resources exposed through multiple distinct paths with inconsistent permission rules.
- Bulk, batch, import, or export operations that fail to enforce per-item permissions.

For complex access models, separate authorization logic audits from authentication bypass checks.

### Resource and file handling

- Path traversal outside intended directories using relative paths, symlinks, encoded sequences, or null bytes.
- Server-Side Request Forgery (SSRF) reaching internal hosts, cloud metadata, or unintended protocols via redirects and parser differences.
- Unsafe deserialization, archive extraction vulnerabilities like zip slip, and insecure temporary file creation.
- Race conditions on filesystem operations, including time-of-check to time-of-use (TOCTOU) windows.

### Cryptography and secrets

- Weak pseudorandom number generators used for security-critical tokens, nonces, or keys.
- Hardcoded credentials, tokens, or private keys committed to source, test fixtures, or configuration.
- Secrets leaked into application logs, error responses, URLs, or client-visible state.
- Flawed key derivation, missing HMAC verification, nonce reuse, or static initialization vectors.
- Timing side-channels during secret or signature comparisons.
- Error paths that disable encryption or fall back to plaintext.

### Business logic

Examine workflow logic manually because automated scanners routinely miss state and sequence errors:
- State machine violations: skipping intermediate verification steps, executing transitions backward, or replaying finalized transactions.
- Concurrent operations causing race conditions, including double-spending, duplicate approvals, and lost updates on check-then-act paths.
- Numeric manipulation: negative values, zero amounts, integer overflow, rounding errors, and type coercion.
- Discrepancies between frontend expectations and backend enforcement.
- Implicit trust assumptions regarding data stored by peer services or background workers.
- Time-based logic failures: expired token handling, scheduling races, rate-limit windows, and timezone conversions.
- Fail-open fallback postures when feature flags, remote dependencies, or configuration values are missing.

### Feature abuse and data leakage

Identify legitimate product features abused for unauthorized data extraction:
- Export, snapshot, or report generation exposing records belonging to other tenants or soft-deleted content.
- Import or restore routines overwriting existing resources or bypassing standard input validation.
- Search, filter, or sorting features functioning as enumeration oracles through response timing, status codes, or error variations.
- Previews, drafts, or staging records discoverable via unauthenticated endpoints, search feeds, or permissive CDN caching.
- Webhook or notification URL configurations exploited for SSRF against private infrastructure.

### Chained vulnerabilities and trust boundaries

Combine individual lower-severity issues into concrete boundary violations only when source paths connect them directly:
- Multi-step privilege escalation connecting separate actions into an unauthorized outcome.
- Cross-component contract mismatches where component A normalizes or truncates data differently than downstream component B expects.
- Second-order evaluation where benign stored strings turn into code, templates, regular expressions, or file paths in later lifecycle phases.
- Capability expansion where delegated credentials, MCP tools, or API tokens retain broad permissions across tenant boundaries.

### Wildcard and atypical patterns

Inspect atypical or experimental code paths outside standard vulnerability classifications:
- Incomplete, undocumented, or experimental endpoints and administrative routes.
- Interactions between disparate subsystems such as localization, file uploads, webhooks, and caching.
- Historical commits, reverted fixes, and commented-out authorization guards.
- Discrepancies between automated test coverage and untested operational edge cases.

### Baseline hygiene checks

Verify basic exposure points systematically:
- Hardcoded secrets, API tokens, passwords, and private keys in source and configuration manifests.
- Debug mode enabled by default or toggleable through client-controlled parameters.
- Default test credentials functioning in deployed or production-ready profiles.
- Unprotected operational endpoints including `/admin`, `/metrics`, `/health`, or `/env`.
- Sensitive configuration files tracked in version control.
- Insecure direct calls to dynamic execution primitives such as `eval()`, shell executors, or deserializers.
- Permissive CORS policies reflecting untrusted origins alongside credentials.
- Missing cookie flags (`HttpOnly`, `Secure`, `SameSite`) on session identifiers.
- Unvalidated redirects accepting arbitrary external URLs.
- Production error handlers printing stack traces, internal paths, or database schemas.

For every identified hygiene issue, verify the complete execution path and observable impact before classifying it as a confirmed vulnerability.
