# Cloud and deployment hunting

Reach for this file when the repository defines cloud identity, infrastructure, containers, Kubernetes, service mesh, serverless functions, edge workers, ingress, object storage, managed services, or environment-specific configuration. This domain asks whether deployed components receive the intended identity, isolation, network reachability, secrets, and policy. Source often expresses intent rather than live fact, so separate source-confirmed defects from deployment validation needs.

Use `supply-chain-and-release.md` for build and promotion trust, `web-protocol-and-auth.md` for HTTP proxy semantics, and `data-isolation-and-lifecycle.md` for data-store tenant scope.

## Authoritative standards

Ground cloud infrastructure and deployment audits in these authoritative specifications:

| Standard | Publishing body | Reference URL | Focus |
|---|---|---|---|
| CIS Kubernetes Benchmark v1.9.0 | Center for Internet Security | https://www.cisecurity.org/benchmark/kubernetes | Control plane and worker node security benchmarks |
| NIST SP 800-190 | NIST | https://csrc.nist.gov/publications/detail/sp/800-190/final | Application container security architecture and lifecycle |
| CNCF Cloud Native Security Whitepaper v2 | CNCF TAG Security | https://www.cncf.io/reports/cloud-native-security-whitepaper/ | Cloud native architecture lifecycle and zero trust models |

## Core discipline

Include these rules in every agent prompt for this domain:

```text
- Do not infer a live exposure from a manifest alone. Establish which environment consumes it, what defaults or overlays modify it, and whether the source path is active.
- Map each workload identity to specific operations and resources. Broad policy is a finding only when lower-trust input can reach an unauthorized action.
- Ingress, proxies, service mesh, metadata services, and admission policy are real boundaries, but only count a control when its configuration and attachment are visible.
- Secret references are not secret disclosure. Require a lower-trust reader, output, artifact, log path, or unsafe fallback.
- Use confirmed for active in-repo configurations and local rendering or policy validation. Use needs_validation for account policy, network attachment, runtime admission, hosted metadata, or drift that needs owner observation.
```

## Workload identity and IAM attack classes

### Workload identity overreach

A workload, pod, function, edge worker, or node identity can act on tenants, accounts, resources, or APIs beyond its role, and untrusted request or job input selects that target. Review cloud policy conditions, resource patterns, service-account attachment, namespace mapping, and fallback credentials.

### Cross-account or cross-tenant role confusion

Role assumption, external IDs, token exchange, workload federation, or resource policies accept identity claims not bound to the intended source account, audience, repository, namespace, or workload. Establish both trust policy and caller-controlled claim.

### Application authorization delegated to cloud metadata

An app trusts caller-supplied identity headers, tags, labels, account IDs, or resource metadata without verifying they came from the cloud control plane or a trusted proxy. Cloud IAM and application authorization are separate checks.

## Ingress, network, and control-plane attack classes

### Unexpected service or management-plane reachability

An ingress, service, listener, security group, load-balancer annotation, port mapping, or server bind exposes an admin, debug, metrics, node, control-plane, or internal API to a lower-trust network. Missing network controls alone are `needs_validation`; a repository-controlled public route to a sensitive handler can be `confirmed`.

### Trusted-proxy and mesh identity bypass

A backend accepts forwarded identity, mTLS subject, or authorization metadata from peers outside the intended ingress or sidecar, or an alternate port and health or legacy path bypasses the mesh. Verify header stripping, peer reachability, and fail-open behavior when the proxy is absent.

### Metadata service reachability and IMDSv2

An untrusted URL, destination, or protocol selection reaches instance metadata, container metadata, or control-plane sockets with workload credentials.
- Audit AWS EC2 instance launch configurations for IMDSv2 enforcement (`HttpTokens: required` and `HttpPutResponseHopLimit: 1`). Permitting IMDSv1 enables SSRF vulnerabilities to harvest temporary IAM credentials.
- Audit GCP and Azure metadata header requirements (`Metadata-Flavor: Google`) to verify that request forgery cannot access hypervisor endpoints.

## Container and orchestration attack classes

### Host or control-plane capability exposure

Evaluate container manifests against NIST SP 800-190 baseline isolation standards:
- Verify whether containers run as non-root (`runAsNonRoot: true` and non-zero `runAsUser`).
- Verify whether all default Linux capabilities are dropped (`capabilities: drop: ["ALL"]`).
- Verify whether the root filesystem is mounted read-only (`readOnlyRootFilesystem: true`).
- Verify whether a restrictive default seccomp profile is applied (`type: RuntimeDefault`).
- Review host namespaces, host paths, device mounts, container runtime sockets, or service-account tokens that cross into node or control-plane authority.

### Admission and policy path inconsistency

One deployment route enforces image identity, namespace, resource, secret, or privilege policy while another controller, job, upgrade, restore, or compatibility path does not. Evaluate whether Kubernetes Pod Security Standards (PSS Restricted profile) or admission controllers like Kyverno or OPA Gatekeeper govern all deployment entry points.

### Namespace and label trust confusion

Network, admission, secret, or workload-identity policy relies on labels, annotations, names, or namespaces that a less-trusted principal can set. Compare who controls selectors with what authority matching grants.

## Configuration and secret lifecycle attack classes

### Security-control precedence drift

Development values, chart defaults, environment variables, command-line flags, feature gates, sidecar injection, or per-region overlays disable authentication, transport security, tenant scoping, or audit policy in a deployed environment. Render the final configuration for each maintained deployment, not just the base file.

### Secret exposure across workload boundaries

Secrets enter logs, crash reports, process arguments, shared environment, broad volumes, build outputs, service discovery, or read APIs accessible to another workload or tenant. Check secret type and authority; a public endpoint or key ID is not a credential.

### Credential renewal and outage fallback

Failure to mount, refresh, rotate, or revoke a workload credential causes stale credentials to remain active or an app to accept a less trusted identity mode. Review startup, readiness, reconnect, and cached-client behavior.

## Managed storage, events, and edge attack classes

### Object and signed-URL policy confusion

Bucket policy, object keys, CDN origins, or signed URLs fail to bind principal, operation, object namespace, audience, or expiry. Review list and version operations and write paths as well as reads.

### Event-source identity confusion

A function or worker trusts event body fields as source identity without validating provider-signed envelopes, subscription topics, account, region, and replay state. Compare push, pull, retry, and dead-letter paths.

### Edge and runtime boundary mismatch

An edge or serverless runtime assumes a secret, API, filesystem, isolation, or tenant policy that differs from the origin runtime, and fallback to origin changes authority or cache behavior. Confirm which configuration selects each path.

## Universal moves

- Render every maintained environment and make a matrix of external port, workload identity, network peers, mounted secrets, and cloud resources. Differences require an owner or policy explanation.
- Follow a lower-trust request, object, label, or event into cloud policy. Show which workload credential performs the final operation and what condition should scope it.
- Diff normal deploy, migration, restore, node maintenance, failover, and local or emulator paths. Review behavior when mesh, admission, identity, secret, or policy service is unavailable.

## Validation rules

1. Establish the active source path and effective deployment object; otherwise use `needs_validation` and state which rendered manifest or owner-observed attachment is missing.
2. Name the lower-trust caller or workload, cloud or application identity, controllable selector, affected resource, and unauthorized operation or disclosure.
3. Verify provider and orchestrator defaults at the pinned version. Do not assume a public IP, reachable metadata service, permissive firewall, or absent admission attachment.
4. Local validation may render templates, evaluate policy, inspect container namespaces in an isolated fixture, or run an emulator with dummy identities. Do not probe live endpoints or alter shared cloud resources.
5. Return `confirmed` only with a complete active source trace and concrete boundary result. Return `needs_validation` with the exact deployed policy, identity attachment, overlay, network, or drift observation needed.
