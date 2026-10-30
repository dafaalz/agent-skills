---
name: wizard
description: Use when generating self-contained interactive bash scripts or terminal wizards that guide a human through manual setup, credential provisioning, third-party dashboards, or one-off cutovers. Don't use for unattended batch scripts (author shell scripts directly), CI pipelines (author CI configuration directly), or automated test runners (use testing-patterns).
allowed-tools: Bash Read Write Edit Glob Grep
---

# Interactive wizard

Generate self-contained, interactive bash wizards that guide human operators through complex manual procedures, credential provisioning, cloud dashboard navigation, or critical production cutovers.

## Boundary isolation

Wizard generation creates temporary or helper operational scripts (typically under `scripts/wizards/` or scratch storage). Never execute irreversible commands or write production secrets directly into repository files.

## Principles and constraints

1. Fail-fast safety. Begin every generated script with `set -euo pipefail`. Trap `SIGINT` and `SIGTERM` to clean up temporary resources upon early exit.
2. Idempotent re-runs. Check if a prerequisite or state already exists before prompting the user or modifying environment files.
3. Sensitive data protection. Read tokens and passwords using `read -s -p` to prevent secrets from appearing in terminal logs or shell history.
4. Immediate validation. Verify credentials against live endpoints or test commands immediately after input before proceeding to the next step.
5. Clear visual separation. Use distinct terminal formatting, step banners, and explicit browser URLs to guide the operator without ambiguity.

<HARD-GATE>
Write-Target Boundary. Write generated scripts only to `scripts/wizards/` or `.agents/state/wizard/`. Do not write to production application source, database configs, or secrets stores. Generated scripts must never write secrets into tracked files; only into gitignored environment files. Refuse to write to any path matching `**/.env`, `**/.env.*`, or `**/*credentials*` unless the path is confirmed in `.gitignore` at runtime using `git check-ignore --quiet <path>`.
</HARD-GATE>

## Modes

Select a mode before Step 1:
- Generate mode (default). Draft a complete, executable bash wizard script and grant execution permissions.
- Audit mode. Review existing manual setup runbooks or scripts to identify missing interactive confirmation guards.

## Workflow (Generate mode)

Steps 1 to 4 apply to Generate mode only. Audit mode workflow follows in Step 5.

### Step 1. Identify human prerequisites and manual boundaries

Isolate the exact operations requiring human agency before drafting code:

1. Identify actions blocked by external access:
   * Third-party web dashboards (creating OAuth apps, generating API keys).
   * Hardware or 2FA authenticators (YubiKey, SMS codes, biometric prompts).
   * Elevated administrative privileges (`sudo`, cloud IAM role assumption).
2. Map required inputs: identify variable names, validation patterns, and target destination files (such as `.env.local`).
3. Define completion criteria: determine what endpoint check or exit code proves the setup succeeded.

Completion criterion. `.agents/state/wizard/manual-steps.md` exists on disk and lists every manual step, required input, destination file, and validation command.

### Step 2. Draft script structure and terminal interaction

Assemble the script skeleton with clear interactive flow controls:

1. Implement step headers and visual banners:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail

   echo "=== [Step 1/3] Cloud Provider Setup ==="
   ```
2. Implement browser helper prompts: when an operator must visit a web console, print the exact URL and prompt for confirmation:
   ```bash
   echo "Open this URL in your browser: https://console.example.com/api-keys"
   read -r -p "Press [Enter] once you have created the key..."
   ```
3. Implement masked input collection for secrets:
   ```bash
   read -s -p "Enter API Secret: " API_SECRET
   echo ""
   ```

Completion criterion. Script drafted with structured banners, external links, masked inputs, and confirmation gates.

### Step 3. Implement validation probes and safe persistence

Add immediate verification checks to prevent invalid state propagation:

1. Validate format and non-empty inputs:
   ```bash
   if [[ -z "${API_SECRET}" ]]; then
     echo "Error: API secret cannot be empty." >&2
     exit 1
   fi
   ```
2. Test credentials against real APIs using curl before saving. Handle network failure separately from HTTP failure so that `set -e` does not mask the diagnostic message:
   ```bash
   HTTP_CODE_FILE="$(mktemp "${TMPDIR:-/tmp}/wizard-http.XXXXXX")"
   if ! curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
        -H "Authorization: Bearer ${API_SECRET}" \
        https://api.example.com/v1/auth-check \
        > "${HTTP_CODE_FILE}"; then
     echo "Error: network failure reaching auth endpoint. Check connectivity and DNS." >&2
     rm -f "${HTTP_CODE_FILE}"
     exit 1
   fi
   HTTP_CODE="$(cat "${HTTP_CODE_FILE}")"
   rm -f "${HTTP_CODE_FILE}"
   if [[ "${HTTP_CODE}" -ne 200 ]]; then
     echo "Verification failed with status ${HTTP_CODE}. Check your token." >&2
     exit 1
   fi
   ```
3. Write verified variables safely into the target environment file. Abort on any write or read failure:
   ```bash
   ENV_FILE="${ENV_FILE:-.env}"
   TMP_FILE="$(mktemp "${TMPDIR:-/tmp}/wizard-env.XXXXXX")"

   if [[ -f "${ENV_FILE}" ]]; then
     if ! grep -v "^API_KEY=" "${ENV_FILE}" > "${TMP_FILE}"; then
       echo "Error: cannot read ${ENV_FILE}. Aborting to prevent data loss." >&2
       rm -f "${TMP_FILE}"
       exit 1
     fi
   fi

   printf 'API_KEY=%s\n' "${API_SECRET}" >> "${TMP_FILE}"
   mv -- "${TMP_FILE}" "${ENV_FILE}"
   chmod 600 "${ENV_FILE}"
   ```

Completion criterion. Script contains live validation checks and safe file persistence.

### Step 4. Deliver script and verify executable permissions

Write the script to disk and make it runnable:

1. Save the file to `scripts/wizards/<wizard-name>.sh`.
2. Grant executable permissions:
   ```bash
   chmod +x scripts/wizards/<wizard-name>.sh
   ```
3. Inform the operator with the exact execution command:
   ```bash
   ./scripts/wizards/<wizard-name>.sh
   ```

Completion criterion. Script file saved, permissions confirmed with `ls -l`, and invocation instructions provided to the operator.

### Step 5. Audit existing wizard scripts

Applies only when `Audit mode` is selected:

1. Locate the target script path recorded in `.agents/state/wizard/audit-target.txt`.
2. Read the script and check for the six invariants in `## Quick audit checklist`.
3. Emit `.agents/state/wizard/audit-report.md` with one row per invariant: `invariant | status (pass/fail) | evidence line number`.
4. Do not modify the target script in Audit mode. Emit suggested patches as separate files under `.agents/state/wizard/patches/`.

Completion criterion. `.agents/state/wizard/audit-report.md` exists on disk and covers all six invariants with line-number evidence.

## Quick audit checklist

| Check | Passing condition |
|---|---|
| Fail-fast header | Script starts with `set -euo pipefail` |
| Masked secrets | Passwords and tokens captured with `read -s` |
| Live validation | Inputs tested against live endpoints before saving |
| Safe persistence | Environment file updates use safe temporary file replacement |
| Idempotency | Script checks existing state before prompting operator |
| Executable permission | File has executable bit set (`chmod +x`) |
