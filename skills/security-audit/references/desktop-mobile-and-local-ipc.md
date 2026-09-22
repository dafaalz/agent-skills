# Desktop, mobile, and local IPC hunting

Reach for this file when the target is a desktop or mobile app, privileged helper, updater, local daemon, webview host, deep-link handler, browser native-messaging host, or local IPC client or server. Relevant untrusted actors may be a downloaded document, remote web content, another local app, another OS user, a sandboxed process, or a lower-privilege account. State that starting capability instead of treating all local users as equivalent.

Use `client-side.md` for browser-side webview behavior, `memory-safety-and-binary.md` for native memory and loader safety, and `supply-chain-and-release.md` for update authenticity.

## Authoritative standards

Ground client runtime, mobile, and IPC audits in these authoritative specifications:

| Standard | Publishing body | Reference URL | Focus |
|---|---|---|---|
| OWASP MASVS v2.1.0 | OWASP Foundation | https://mas.owasp.org/MASVS/ | Mobile application security verification standard |
| Electron Security Tutorial | OpenJS Foundation / Electron | https://www.electronjs.org/docs/latest/tutorial/security | Desktop webview isolation and native capability security |
| Apple Associated Domains | Apple Developer | https://developer.apple.com/documentation/xcode/supporting-associated-domains | Universal link verification and app sandboxing guidelines |

## Core discipline

Include these rules in every agent prompt for this domain:

```text
- Establish the realistic local or remote-content attacker: another app, another OS user, a sandboxed child, an untrusted document, or a remote origin. Self-harm within the same account and authority is not a boundary violation.
- Paths, process names, bundle IDs, and claimed sender fields are not peer authentication. Use OS peer credentials, code identity, capability handles, or protected channel state.
- The native bridge or helper must authorize each operation and final resource after parsing. A trusted UI or broker does not make attacker-influenceable arguments trusted.
- OS sandbox, signing, entitlements, permissions, keychain ACLs, exported-component policy, and prompt behavior are real controls when pinned and visible.
- Use confirmed for source evidence plus bounded local or emulator tests. Use needs_validation when signing, manifest merge, OS version, device policy, installer ACL, or packaging is required but not observable.
```

## Deep-link, callback, and navigation attack classes

### Custom-scheme and deep-link ambiguity

Another app or page can invoke a route that mutates state, imports data, completes authentication, or selects an account without a current-session and one-time callback binding.
- Audit custom URI scheme handlers versus verified deep links. On iOS, verify Universal Links via `apple-app-site-association`. On Android, verify App Links via Digital Asset Links JSON. Unverified custom schemes can be claimed by malicious sibling apps.
- Review URI normalization, duplicate query fields, scheme and host path matching, exported activity policy, and stale replayed links.

### App and account handoff confusion

OAuth, SSO, magic-link, invite, device pairing, passwordless, or payment callbacks return to the wrong installed app, profile, tenant, or pending transaction. Bind state to the initiating app identity, current session, account, provider, operation, and expiry.

### File-open and intent authority confusion

An associated file, share intent, drag-and-drop item, clipboard record, notification action, or open-file event triggers a privileged operation without confirming content type, sender trust where applicable, current user intent, and final target.

## Webview and desktop runtime attack classes

### Electron security checklist audit

Inspect desktop Electron configurations against canonical security rules:
- `contextIsolation: true` must be enforced in `webPreferences`.
- `nodeIntegration: false` must be enforced across all windows and webviews.
- `sandbox: true` must be enabled.
- `webSecurity: true` and `allowRunningInsecureContent: false` must be preserved.
- Navigation interception: verify that `setWindowOpenHandler` and `will-navigate` listeners validate URLs against an exact allowlist rather than permitting arbitrary external navigation.

### Navigation-origin to bridge confusion

Remote or attacker-controlled frames can reach a JavaScript or native bridge intended only for packaged content. Validate origin at call time and after every navigation, redirect, subframe creation, popup, and error page. URL-prefix checks and initial-load checks are insufficient.

### Over-broad native bridge capabilities

Web content can select arbitrary files, commands, IPC methods, credentials, or system actions through a generic bridge. Check method allowlists, normalized arguments, user or tenant authority, gesture confirmation requirements, and return-value disclosure.

## Local IPC and exported-component attack classes

### Mobile component export overreach (MASVS-PLATFORM)

Audit Android and mobile application components:
- Explicitly set `android:exported="false"` on Activities, Services, BroadcastReceivers, and ContentProviders unless public consumption is required by design.
- For exported components, enforce signature permissions (`android:protectionLevel="signature"`).
- Verify `PendingIntent` creation enforces `FLAG_IMMUTABLE` to prevent malicious apps from mutating intent targets or extras.

### IPC peer-authentication gaps

Unix sockets, named pipes, XPC, Binder, D-Bus, native messaging, RPC, shared memory, or loopback listeners accept a lower-trust peer without checking OS credentials, code identity, sandbox token, or channel ownership. Require a meaningful method or disclosure behind the channel.

### Claimed principal versus channel identity

The authenticated process or channel belongs to one app or user, but request fields select another user, tenant, profile, or capability. Bind each method and resource to the peer credential rather than a caller-declared identifier.

### IPC lifecycle and correlation confusion

Predictable request IDs, reused handles, stale channels, inherited descriptors, world-writable socket paths, or restart behavior lets one peer answer, cancel, or reuse another peer operation. Review creation permissions and cleanup of socket files, locks, ports, and shared mappings.

## Privileged-helper and local-file attack classes

### Privileged helper as confused deputy

A low-privilege caller can select a privileged command, file, service, user, or system setting without per-operation authorization. Review sudo, polkit, UAC, and XPC helper rules and ensure the helper independently validates normalized arguments.

### Install, update, and repair path trust

A privileged installer or helper reads manifests, scripts, packages, symlinks, working directories, or repair state writable by a lower-trust actor after authorization. Bind authorization to immutable content and safe destination paths.

### Local file ownership and TOCTOU

The app checks a file path then follows replacement, symlink, mount, or normalization changes during a privileged read or write. Use descriptor-relative operations and verify final ownership.

### Credential-store and local-secret boundary mismatch

A keychain or keystore item, token file, backup, log, clipboard, notification preview, or local configuration is readable by another app, profile, or user with less authority. Plaintext readable only by the same intended OS account is not automatically a vulnerability; state the lower-trust reader and credential power.

## Universal moves

- Enumerate every process, app component, local endpoint, URI scheme, file association, webview origin, and helper. Record OS identity, runtime privilege, caller, and callable operation.
- Read final packaging inputs: merged manifest, entitlements, installer rules, native-messaging registration, protocol handlers, and ACL creation. Source declarations can be overwritten downstream.
- Validate with dummy profiles and non-sensitive local fixtures on an isolated machine or emulator. Do not interact with other users apps, credentials, or production services.

## Validation rules

1. Name the attacker starting capability, OS or app principal crossed, entry channel, accepted argument or state, and unauthorized operation or disclosure.
2. Confirm OS sandbox, peer credential, signing, entitlement, permission, user-consent, and installer controls that apply. Unknown packaging or runtime facts require `needs_validation`.
3. For webview bridges, cite both navigation origin control and privileged native sink. For IPC, cite peer authentication and per-resource authorization. For helpers, verify final normalized destination.
4. Keep local tests bounded and use dummy content or accounts. Stop after proving the boundary result; do not extend proof into persistence or broader system modification.
5. Return `confirmed` only with a complete source and local evidence chain. Return `needs_validation` with the exact OS, manifest, signing, ACL, or device-lifecycle fact required.
