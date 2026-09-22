# Client-side and browser hunting

Reach for this file when meaningful trust decisions or untrusted rendering happen in a browser: single-page apps, browser extensions, embedded webviews, service workers, offline applications, and code that renders attacker-influenceable content into the DOM, receives cross-window messages, or uses browser storage. These paths include sources the server never sees, such as URL fragments, `window.name`, `postMessage`, and previously cached content.

Use alongside `attack-classes.md`. This file covers browser sources and sinks, origin boundaries, browser persistence, and cross-site state oracles. Use `desktop-mobile-and-local-ipc.md` for the native side of a webview bridge, and `web-protocol-and-auth.md` for server-side CSRF, sessions, and auth callbacks.

## Authoritative standards

Ground client-side security audits in these authoritative specifications:

| Standard | Publishing body | Reference URL | Focus |
|---|---|---|---|
| Content Security Policy Level 3 | W3C | https://www.w3.org/TR/CSP3/ | Script execution, frame restrictions, and content sandboxing |
| OWASP XSS Prevention Cheat Sheet | OWASP Foundation | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html | Context-aware output encoding and injection sinks |
| OWASP DOM XSS Prevention Cheat Sheet | OWASP Foundation | https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html | DOM sources, sinks, and script execution APIs |
| W3C Trusted Types | W3C WebAppSec WG | https://w3c.github.io/trusted-types/dist/spec/ | DOM XSS prevention through typed injection sink control |
| W3C Fetch Metadata Headers | W3C | https://www.w3.org/TR/fetch-metadata/ | Cross-origin isolation and request purpose validation |

## Core discipline

Include these rules in every agent prompt for this domain:

```text
- A client-side candidate needs a controllable source and an executing or disclosing sink. Name both and show attacker-influenced data reaching the sink.
- The impact must reach a victim session, another origin, or shared persistence. Self-injection and disclosure of the attacker own data are not findings.
- Framework escaping, browser same-origin policy, CSP, COOP/CORP, service-worker scope, and modern noopener defaults are real controls. Verify them before assigning impact.
- Browser storage and caches are shared by origin and may outlive login state. Identify who writes, who reads, and which account, tenant, or worker lifecycle clears each record.
- Use confirmed only for complete source evidence plus bounded local browser tests. Use needs_validation when renderer, extension permission, deployed header, or browser-policy behavior is required but unavailable.
```

## DOM and object-state attack classes

### DOM-based XSS and sink control

Trace `location` fields, `document.referrer`, `window.name`, message data, storage, and browser-controlled document state into `innerHTML`, `outerHTML`, `document.write`, string-evaluating APIs, executable URLs, jQuery HTML APIs, or framework escape hatches. Interpolation escaped by the framework is not a finding.

Audit adherence to modern W3C Trusted Types:
- Check whether the application defines policies via `window.trustedTypes.createPolicy`.
- Verify whether the Content Security Policy directive `require-trusted-types-for 'script'` is enforced.
- Identify bypasses where untrusted user input is directly wrapped into a Trusted Type without validation.

### DOM clobbering

Attacker-injected `id` or `name` attributes shadow a global, form property, configuration object, or initialization flag later trusted by code. Require both a markup path that preserves the attribute and a security-relevant use of the clobbered value.

### Prototype pollution and gadget chains

An attacker-controlled key reaches a recursive write such as deep merge or path assignment and modifies prototype state. Then a reachable gadget consumes the polluted property to change authorization, execution, navigation, or rendering. `JSON.parse`, a shallow copy, or pollution without an active gadget is not a vulnerability.

## Cross-origin messaging and network attack classes

### Cross-document messaging origin trust

A `window.postMessage` handler performs a sensitive action with `event.data` without an exact origin allowlist and, where multiple frames share an origin, the expected `event.source`. On the send side, sensitive data sent to `*` reaches an unintended embedder. Weak substring, prefix, suffix, or unanchored regular expression origin matching is an ineffective origin check.

### Cross-site WebSocket request execution

A WebSocket upgrade accepts ambient cookies from an untrusted origin without an `Origin` check or channel-specific token, allowing the victim session to read or mutate data. Confirm both the upgrade behavior and a security-relevant message handler.

### Credentialed CORS trust

The server reflects or weakly matches `Origin` while allowing credentials and returns sensitive responses. A bare wildcard with credentials is rejected by browsers; report only the actual reflected or allowed origin path and cross-origin data or mutation.

### Fetch Metadata isolation gaps

Evaluate whether the backend or client routing audits incoming request metadata:
- Review handling of `Sec-Fetch-Site` (`same-origin`, `same-site`, `cross-site`, `none`).
- Review handling of `Sec-Fetch-Mode` (`navigate`, `cors`, `no-cors`) and `Sec-Fetch-Dest`.
- Discrepancies allowing cross-site state-changing actions without appropriate fetch destination verification represent isolation gaps.

## Service-worker and browser-storage attack classes

### Service-worker registration and scope takeover

Attacker-influenceable content can become the registered worker script, control a path that receives an over-broad `Service-Worker-Allowed` scope, or alter update imports without integrity control. Verify the final script URL, response MIME type, origin, scope, and who controls every imported script. A normal same-origin worker with intended scope is not a defect.

### Service-worker cache and identity confusion

The worker caches personalized responses without including account, tenant, authorization state, or request mode in its policy, then serves them after account switch or logout. Review fetch-event routing, cache names and keys, navigation fallbacks, cache cleanup, and whether error or offline paths return another user prior response.

### Browser-storage disclosure and stale authorization

Tokens, private responses, draft data, or authorization decisions remain in `localStorage`, `sessionStorage`, IndexedDB, Cache Storage, extension storage, or client state and become readable by another account or less-trusted same-origin component. Storage of a token alone is not a finding; require a realistic reader with less authority, or continued use after revocation or logout.

### Cross-context storage and broadcast confusion

`storage` events, `BroadcastChannel`, shared workers, or origin-wide caches carry identity or commands between tabs without binding them to the current session. Check account switching, private and public windows, tenant changes, and stale tabs that can overwrite newer auth state.

## Cross-site information leak classes

### XS-Leaks and cross-origin state oracles

An attacker page can distinguish protected cross-origin state through resource load or error events, frame or window state, redirect behavior, timing, cache state, or response size while the browser attaches victim credentials. Require one concrete secret-bearing predicate such as whether a private object, role, or account exists. Generic timing variance or public-resource availability is not a finding.

### Window and opener state disclosure

A cross-origin window permitted metadata or navigation result reveals protected state, or a retained opener or named-window relationship lets an attacker-controlled page influence a privileged navigation. Check Cross-Origin Opener Policy (COOP), frame protections, `noopener`, exact origin, and whether the observable state is confidential.

## UI-redress and navigation attack classes

### Clickjacking and frame isolation

A framed, state-changing action lacks effective `frame-ancestors` in CSP, `X-Frame-Options`, or equivalent UI isolation. Require the sensitive action and confirm it can complete in the framed state. Missing headers on read-only content are hardening notes.

### Client-side navigation confusion

A client source controls redirect or navigation without scheme and destination policy, including executable `javascript:` or `data:` destinations. Reverse tabnabbing applies only where code explicitly keeps `window.opener`, uses `window.open` without isolation, or supports an environment without implicit `noopener`.

## Universal moves

- Start from DOM, navigation, worker, message, and storage sinks, then trace backward to browser-only and server-controlled sources. Record the browser policy that should stop the path.
- Test account switch, logout, worker update, offline fallback, and stale-tab state with a local test origin and dummy accounts. Do not use production users, origins, or shared services.
- For XS-Leaks, list only predicates proved by source and local browser behavior. Then identify the response headers or rendering choice that would remove the oracle.

## Validation rules

1. Cite the source, sink, browser policy, affected origin or session, and observable mutation or disclosure.
2. For prototype pollution, prove the recursive write and a security-relevant gadget. For DOM clobbering, prove the markup survives and the shadowed value is used.
3. For service workers and storage, prove lifecycle reachability: an attacker-controlled write or cache entry must reach a different account, tenant, or later authorization state.
4. For messaging, CORS, WebSocket, and XS-Leaks, show exact origin and source validation and the protected state or action exposed. Confirm that CSP, COOP, CORP, cookies, and SameSite policy do not already block it.
5. Return `confirmed` findings only with a complete client path and bounded local evidence. Return `needs_validation` with the precise deployed header, extension permission, browser version, or renderer behavior an owner must verify.
