# Credentials and secret handling hygiene

Protocols for safely verifying, handling, and prompting credentials without leaking sensitive values into agent context, command logs, or working trees.

## 1. Zero exposure inspection rules

Never output plaintext secrets to terminal stdout, logs, or agent conversation history.

1. **Verify presence without values.** Test whether a credential exists by checking exit codes rather than printing content:
   ```bash
   grep -sq "^DATABASE_PASSWORD=" .env && echo "DATABASE_PASSWORD is set" || echo "DATABASE_PASSWORD is missing"
   ```
2. **Prohibited dump commands.** Never run commands that serialize entire environment tables:
   - Do not execute `cat .env`, `tail .env`, or `head .env`.
   - Do not run bare `printenv` or `env`. Use `printenv KEY_NAME > /dev/null` to check return codes.
   - Do not execute `echo $SECRET_NAME` or `set`.
3. **Redact tokens from network traces.** When inspecting network requests with curl, use `-H "Authorization: Bearer <REDACTED>"` in logged representations.

## 2. Interactive credential collection protocol

When a required API key or password is absent from the local environment:

1. Identify the missing key name, the provider documentation URL, and the target configuration file.
2. Prompt the user with a single explicit command pattern using silent terminal input:
   ```bash
   read -s -p "Enter API token: " TOKEN && echo "API_TOKEN=$TOKEN" >> .env
   ```
3. Confirm credential storage by checking variable key presence only, never echoing the stored value back to the shell.

## 3. Pre commit secret leak audit

Scan the working directory before committing code:

1. Verify `.env`, `.env.local`, and credential files match `.gitignore`.
2. Inspect staged diffs for accidental hardcoded secrets:
   ```bash
   git diff --staged | grep -Ei "(api[_-]?key|secret|password|bearer|private[_-]?key)"
   ```
3. If an API key was committed previously, revoke and rotate the credential immediately. Overwriting history alone does not neutralize a leaked secret.

## 4. Client-side build and bundle prefix hygiene

Client framework prefixes inline environment variables into public browser bundles and mobile binary packages at build time:

| Framework | Prefix | Exposure mode |
|---|---|---|
| Next.js | `NEXT_PUBLIC_` | Inlined into client JavaScript bundles |
| Vite | `VITE_` | Inlined into static frontend output |
| Expo / React Native | `EXPO_PUBLIC_` | Baked into packaged mobile application binaries |
| Create React App | `REACT_APP_` | Inlined into client build artifacts |

### Credential placement boundaries
- Safe client values: public analytics identifiers, Stripe publishable keys (`pk_live_*`, `pk_test_*`), Firebase client configurations (`apiKey`, `projectId`), and Supabase anonymous keys (`anon`).
- Forbidden client values: Supabase `service_role` keys, Stripe secret keys (`sk_live_*`), database connection strings, third-party API private keys, JWT signing keys, and OAuth client secrets.

### Search heuristics for leaked client variables
Scan repository configurations for secret tokens bound to public prefixes:
```bash
grep -rEi "(NEXT_PUBLIC_|VITE_|EXPO_PUBLIC_|REACT_APP_)[A-Z0-9_]*(SECRET|KEY|TOKEN|PASSWORD|PRIVATE)" .
```

