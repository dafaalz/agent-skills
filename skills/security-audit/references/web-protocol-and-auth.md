# HTTP protocol and authentication hunting

Reach for this file when the target speaks HTTP at a parsing, caching, browser authentication, or identity boundary: web applications, APIs, reverse proxies, CDNs, gateways, custom HTTP servers, and services implementing sessions, JWT, OAuth 2.1, OIDC, SAML, password recovery, MFA, passkeys, API keys, or mTLS. Use this with `attack-classes.md`: access-control review asks whether a principal may perform an operation; this file asks whether the HTTP or identity layer can confuse which principal, request, assurance level, or token the operation belongs to.

## Authoritative standards

Ground HTTP protocol and identity audits in these authoritative specifications:

| Standard | Publishing body | Reference URL | Primary focus |
|---|---|---|---|
| OWASP ASVS v4.0.3 | OWASP Foundation | https://owasp.org/www-project-application-security-verification-standard/ | Web authentication and session controls |
| OAuth 2.1 Framework | IETF | https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/ | Consolidated OAuth authorization and token security |
| RFC 6749 (OAuth 2.0) | IETF | https://datatracker.ietf.org/doc/html/rfc6749 | Base OAuth authorization framework |
| OpenID Connect Core 1.0 | OpenID Foundation | https://openid.net/specs/openid-connect-core-1_0.html | Federated identity and ID token verification |
| NIST SP 800-63B | NIST | https://csrc.nist.gov/publications/detail/sp/800-63b/rev-4/final | Digital identity, authentication, and lifecycle management |
| RFC 9449 (DPoP) | IETF | https://datatracker.ietf.org/doc/html/rfc9449 | Sender-constrained token proof-of-possession |

## Core discipline

Include these rules in every agent prompt for this domain:

```text
- Framing and cache findings require two interpretations of the same request, response, or key. Name both components and the exact normalized value on each side.
- For every credential, find the signature or secret verification and every binding required for its role: issuer, audience, origin, relying party, client, session, principal, resource, assurance, expiry, and one-time state.
- Host, Forwarded, X-Forwarded-*, Origin, Referer, redirect targets, callback state, and request-derived URLs are trust decisions. Trace each to the affected identity or response.
- A missing header, cookie attribute, MFA prompt, or rate limit is not a finding alone. Require an accepted invalid request, cross-principal impact, assurance downgrade, or credential disclosure.
- Classify confirmed only from complete source evidence and bounded local request or token tests. Use needs_validation when proxy, IdP, browser, certificate, secret, or deployed configuration is required but not visible.
```

## HTTP framing and cache attack classes

### Request framing and desynchronization

Front end and back end disagree on request length or header normalization. Review multiple `Content-Length` values, `Transfer-Encoding`, HTTP/2 or HTTP/3 downgrade, header-name normalization, forbidden connection headers, and CR and LF conversion. Confirm which bytes one component assigns to a request and which bytes its peer assigns to the next request.

### Web cache poisoning through unkeyed input

A request value changes cached content or security-relevant headers but is absent from the cache key. Compare cache key construction with every response variant, including forwarded host and scheme, selected cookies, query normalization, language and device headers, and authorization state.

### Cache deception and private-response caching

Cache routing treats a private dynamic path as a public static asset, or caches a response whose identity and authorization inputs are missing from policy. Compare edge cacheability with application route parsing, suffix and path-parameter normalization, and response cache directives.

### Host and forwarded-header trust

Untrusted host or proxy metadata determines absolute URLs, tenant routing, callbacks, reset links, cache keys, or the client address used by authorization. Confirm who can supply the header and whether trusted ingress removes client-provided copies.

### Response-header injection

Untrusted data reaches `Location`, `Set-Cookie`, CSP, or another response header with unsafe control characters or normalization. Verify framework rejection before reporting and require a security-relevant response change.

## Browser-session attack classes

### Cross-site request forgery

A browser sends ambient credentials to a state-changing endpoint that accepts a cross-site request without an effective anti-CSRF token, same-site request binding, or strict Origin and Referer validation. Inventory every cookie-authenticated mutation, including form, JSON-like, multipart, method-override, and legacy routes. `SameSite` is effective only for the cookie and browser contexts actually used; login CSRF and cross-site subresource requests can have different requirements.

### Session fixation and invalidation

Session identifiers are not rotated on login, account switch, MFA completion, impersonation, or other privilege changes, or remain valid after logout, password change, revocation, and account disable. Check server sessions, refresh tokens, signed cookies, websocket state, cache copies, and fallback endpoints.

### Cookie scope and transport

A sensitive cookie has an over-broad `Domain` or `Path`, can cross an insecure transport, or conflicts with a sibling cookie that another component selects differently. Bare missing flags remain hardening notes unless a realistic less-trusted origin, network position, or browser path can gain or replace the credential.

## Federated-identity attack classes

First establish role. Authorization-server controls such as redirect allowlisting and code issuance do not belong to a relying-party client. Verification and binding defects belong to the component consuming the artifact.

### JWT verification and claim binding

Check signature verification, server-pinned algorithm and key source, then `exp`, `nbf`, `aud`, and `iss`. Review `kid`, `jku`, and `x5u` as untrusted key selectors, duplicate header normalization, and decode-without-verify paths. A valid token for another service is invalid here even when signed by a trusted issuer.

### OAuth 2.1 and OIDC request and callback binding

Evaluate implementations against strict OAuth 2.1 requirements:
- Proof Key for Code Exchange (PKCE) is mandatory for all authorization code grants, across both confidential and public clients.
- The Implicit Grant and Resource Owner Password Credentials Grant (ROPC) are deprecated and represent confirmed security design anti-patterns.
- Redirect URIs require exact string matching without wildcards, path traversal, or partial subdomain matching.
- Enforce sender-constrained token models where available, including DPoP (RFC 9449) and mutual-TLS client certificate-bound access tokens (RFC 8705).
- Validate exact `redirect_uri` ownership where the target is the authorization server; session-bound `state`; PKCE code challenge binding; ID token issuer, audience, signature, and nonce; and selected IdP binding in multi-provider flows.

### SAML signed-object and assertion binding

Ensure the element whose signature is validated is the element used as identity. Review unsigned and fallback paths, safe XML parser configuration, canonicalization differences, and freshness or binding fields such as validity windows, audience or recipient, request correlation, and replay state.

## MFA, passkey, and account transition attack classes

### MFA enrollment and assurance downgrade

Enrollment, replacement, disablement, recovery-code generation, trusted-device creation, and fallback login require the intended prior assurance. Check that a valid first factor cannot enroll or replace the second factor without policy-required fresh authentication, and that disabled or stale factors stop authorizing sessions.

### Step-up binding and bypass

A successful challenge upgrades the wrong session, account, tenant, action, or API request, or an alternate route omits the assurance check. Bind the challenge to principal, current session, assurance target, operation or resource when required, expiry, and one-time completion. Compare UI, API, batch, recovery, and resumed-flow paths.

### WebAuthn and passkey verification

At registration, bind challenge, relying party ID, expected origin, credential, user handle, algorithm, and policy-required user verification to the initiating session. At authentication, verify challenge, relying party origin, credential membership, signature, and intended user presence and verification. Check account-discovery and linking flows for user handle or credential-to-account confusion. Signature-counter handling is meaningful only when the product treats regressions as a clone signal.

### Account linking and identity collision

Adding an IdP, passkey, email, phone, device, or external account to an existing account must require a current authenticated session, verified ownership of the new identity, policy-required step-up, and callback state bound to the account that initiated linking. Review unlink, relink, and invite-acceptance paths for verified-identifier or tenant collisions.

### Password reset and account recovery

Recovery tokens, support recovery, backup codes, device migration, and email or phone changes often become the weakest authentication path. Verify token randomness, user and action binding, expiry, one-time state, rate and accounting controls, delivery URL trust, and invalidation of prior tokens and sessions. Different responses that only reveal public account existence are not automatically security findings.

## API-key and mTLS attack classes

### API-key scope and resource binding

A key authenticates to broader tenants, resources, actions, or environments than its server-side record grants, or request parameters override those bindings. Review key lookup, prefix or full-secret verification, type confusion between publishable and secret keys, scope checks, rotation, revocation caches, and bulk endpoints.

### API-key exposure and unsafe transport

Keys appear in client bundles, URLs, redirects, logs, error paths, build artifacts, or responses accessible to a lower-trust principal. A public identifier called a key is not a secret. Confirm key type and the authority gained by disclosure.

### mTLS peer and application-identity confusion

A process trusts client-certificate identity headers from any network peer, verifies a chain but maps attacker-influenceable subject text to an account incorrectly, or accepts a certificate for the wrong trust domain, extended usage, audience, or validity policy. Where a trusted proxy terminates mTLS, verify only that proxy can connect, it removes incoming identity headers, and the backend binds the sanitized identity to the request.

### Certificate lifecycle fallback

Expired, revoked, missing, or renewal-failed certificates cause silent fallback to bearer-only or anonymous operation, or long-lived pooled connections retain authorization after revocation. Missing deployment revocation data makes the result `needs_validation`; an in-repo fail-open branch is source-confirmable.

## Universal moves

- Walk issue, store, transmit, consume, refresh, and revoke for every credential and challenge. Compare normal, error, retry, migration, legacy, and account-switch paths.
- Enumerate every door to the same identity and every route to the same sensitive operation. The effective policy is the weakest parallel path, not the most polished UI.
- Diff parser, proxy, router, cache, and application normalization side by side. For local validation, feed identical bounded request fixtures into each component rather than sending traffic to a live deployment.
- For recovery and linking, draw the account state graph. Each transition must name the current principal, proof of the new identity, required assurance, callback or session binding, and revocation effect.

## Validation rules

1. Apply a source-visibility gate. Proxy chains, edge cache keys, IdP policy, certificate trust, browser cookie behavior, secrets, and deployed auth modes may be outside the repository. Record a precise `needs_validation` candidate instead of asserting missing infrastructure behavior.
2. For framing and cache findings, name both components and the divergent parse or key. Confirm cross-request, cross-user, or private-response impact with bounded local fixtures.
3. For token, MFA, passkey, account-link, recovery, API-key, and mTLS findings, cite the verification line and missing principal, session, resource, origin, audience, action, or assurance binding. Prove the server accepts the invalid transition or credential.
4. For CSRF, name the ambient credential, state-changing route, accepted cross-site request shape, browser cookie policy, and missing effective check. Read-only actions and routes requiring a non-ambient bearer token do not qualify.
5. Verify framework and library defaults. If version or configuration is unknown, use `needs_validation`; do not turn an unverified critical claim into a lower-severity confirmed finding.
6. Return `confirmed` only with a complete source trace and observable unauthorized identity, state, or disclosure. For `needs_validation`, name the missing fact and safe local or owner-observed check that resolves it.
