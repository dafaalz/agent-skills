---
name: web-advisor-prompt
description: Use when packaging sliced repository context into injection-hardened XML prompts for external frontier reasoning models, or when auditing external advisor responses against local files and macOS BSD rules. Don't use for local subagent dispatch (use executing-plans), multi-task plan verification (use agent-planning), internal code review (use code-review), or skill audits (use review-a-skill).
---

# Web advisor prompt

Package sliced repository context into cache-aligned, injection-hardened XML prompts via deterministic Python scripts, and audit external advisor critiques against local repository files before editing source code.

<HARD-GATE>
1. Write-Target Boundary. Write prompt payloads and state artifacts strictly under `scratch/advisor_prompts/` and `.agents/state/web-advisor-prompt/`. Never write payloads or unverified advisor patches into application source directories.
2. Script-First Execution. Delegate file slicing, 1-indexed line numbering, CDATA escaping, credential redaction, XML parsing, and response auditing to `scripts/package_prompt.py` and `scripts/audit_response.py`. Never hand-roll inline `awk`, `sed`, or `grep` pipelines in chat turns.
3. Zero-Leak Credential Gate. Run `scripts/package_prompt.py` so raw repository secrets are redacted outside LLM context and verified with `MATCHES=0` in `.agents/state/web-advisor-prompt/redaction-audit.txt` before clipboard emission.
4. Prompt Budget Ceiling. Keep the assembled `<advisor_payload>` strictly at or below 1500 total lines by passing targeted `path:start-end` slices across the decision boundary.
</HARD-GATE>

## Modes

Declare one operating mode before executing Step 1:
- **Package mode (default).** Build, validate, hygiene-lint, and copy an outbound XML payload using profile `adversarial` (flaw-first stress test) or `synthesis` (multi-variant decision matrix). Execute Step 1 and Step 2.
- **Ingest mode.** Audit an external advisor response against local file line bounds, macOS BSD shell rules, and code completeness invariants before applying changes. Execute Step 1, Step 3, and Step 4.

## Reference modules

Load reference manuals on demand only when customizing directives or running offline benchmarks:

| Concern | Reference file |
|---|---|
| Anti-sycophancy framing, unified severity taxonomy, and prompt-caching calibration | references/framing-and-calibration.md |
| Domain-neutral XML payload templates and offline benchmark rubric | references/xml-templates-and-benchmarks.md |

## Workflow

Execute the steps required by the active mode in strict order.

### Step 1. Script self-test and scope initialization

Verify both local helper scripts and initialize `.agents/state/web-advisor-prompt/scope.json` before packaging or ingesting:
1. Run `python3 skills/web-advisor-prompt/scripts/package_prompt.py --self-test` and `python3 skills/web-advisor-prompt/scripts/audit_response.py --self-test`. Halt immediately if either exits non-zero.
2. Create `.agents/state/web-advisor-prompt/` and `scratch/advisor_prompts/` if absent.
3. Write `.agents/state/web-advisor-prompt/scope.json` containing keys `target_slug` (lowercase alphanumeric and underscores matching `^[a-z0-9_]+$`), `mode` (`package` or `ingest`), `profile` (`adversarial` or `synthesis`), `model` (`claude`, `openai`, `gemini`, or `generic`), and `context_files` (array of `path` or `path:start-end` slices).

Completion criterion. Both script `--self-test` commands exit with status 0 and `python3 -m json.tool .agents/state/web-advisor-prompt/scope.json >/dev/null` exits with status 0.

### Step 2. Deterministic XML packaging and clipboard emission (package mode)

Stage a neutral problem statement and run the packager script to generate `scratch/advisor_prompts/<target_slug>.xml`:
1. Write the architectural dilemma to `scratch/advisor_prompts/<target_slug>.proposal.md` using neutral constraints without telegraphing a preferred answer.
2. Execute the packager in one call:
   ```bash
   python3 skills/web-advisor-prompt/scripts/package_prompt.py \
     --scope .agents/state/web-advisor-prompt/scope.json \
     --proposal-file scratch/advisor_prompts/<target_slug>.proposal.md

```

3. Pass `--no-clipboard` only in headless SSH or CI environments without macOS WindowServer pasteboard access.
4. If the script exits non-zero because line count exceeds 1500, narrow `context_files` slices in `scope.json` and rerun.

Completion criterion. `package_prompt.py` exits with status 0, `.agents/state/web-advisor-prompt/redaction-audit.txt` contains `MATCHES=0`, and `.agents/state/web-advisor-prompt/emission.txt` contains `XML_VALID=1`, `HYGIENE_EXIT=0`, and `LINE_COUNT_LE_1500=1`.

### Step 3. Ground-truth response ingestion and audit (ingest mode)

Capture the external advisor output and verify every citation, shell command, and code block before editing repository files:

1. Execute the auditor directly from the macOS clipboard in one call:
   ```bash
   python3 skills/web-advisor-prompt/scripts/audit_response.py \
     --scope .agents/state/web-advisor-prompt/scope.json \
     --from-clipboard
   ```
   Alternatively, pass `--response scratch/advisor_prompts/<target_slug>.response.md` when auditing from a saved file.
2. Inspect `.agents/state/web-advisor-prompt/ingestion-audit.json`. Every finding is classified as `VERIFIED`, `HALLUCINATED_LINE`, `PLATFORM_INVALID`, or `INCOMPLETE_STUB`.

Completion criterion. `.agents/state/web-advisor-prompt/ingestion-audit.json` and `.agents/state/web-advisor-prompt/verified-findings.json` exist on disk and `python3 -m json.tool .agents/state/web-advisor-prompt/verified-findings.json >/dev/null` exits with status 0.

### Step 4. Verified surgical patch gating (ingest mode)

Apply repository edits strictly from verified findings:

1. Discard every finding in `ingestion-audit.json` whose status is `HALLUCINATED_LINE`, `PLATFORM_INVALID`, or `INCOMPLETE_STUB`.
2. Implement only changes anchored to file paths listed under `verified_files` in `.agents/state/web-advisor-prompt/verified-findings.json`.
3. Run the repository verification commands against the modified files.

Completion criterion. Every path returned by `git diff --name-only` appears in `.agents/state/web-advisor-prompt/verified-findings.json` and the target project test suite exits with status 0.

## Boundary isolation

Confine prompt assembly, redaction logs, and ingestion reports strictly to `scratch/advisor_prompts/` and `.agents/state/web-advisor-prompt/`. Never apply prose or punctuation rewrite rules to code syntax inside `<codebase_context>` slices, database schemas, or shell commands. Never apply external advisor patches directly to tracked source files without a completed Step 3 `verified-findings.json` allowlist.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
| --- | --- | --- | --- | --- |
| WAP-01 | Inline shell orchestration | Generating multi-turn `awk`, `sed`, and `grep` pipelines in chat to build XML | Burns 1,800+ extra tokens per run and introduces shell quoting bugs | Run `scripts/package_prompt.py` in one CLI call |
| WAP-02 | Resetting slice line numbers | Piping sliced files through `awk` using `NR` starting at 1 | Real line offsets shift to 1 and corrupt all advisor `file:line` citations | Slice files with `scripts/package_prompt.py` preserving original 1-indexed line numbers |
| WAP-03 | Leaky credential regexes | Matching only `sk-[A-Za-z0-9]{20,}` and quoted assignments | Leaks `sk-ant-`, `sk-proj-`, unquoted `.env` secrets, URI passwords, and PGP blocks | Use `scripts/package_prompt.py` multi-pattern redactor and verify `MATCHES=0` |
| WAP-04 | Uncontained citation paths | Joining `repo_root / rel_path` without `resolve()` containment | External advisors can cite `../../etc/passwd:1` and pass verification | Enforce `is_relative_to(repo_root)` via `scripts/audit_response.py` |
| WAP-05 | Scanning prose for GNU flags | Running BSD shell checks across markdown prose outside fenced blocks | Flags advisor warnings about `grep -P` as `PLATFORM_INVALID` false positives | Restrict BSD CLI checks to shell code fences in `scripts/audit_response.py` |
| WAP-06 | Unescaped CDATA or control bytes | Wrapping raw text without splitting CDATA terminators or stripping control bytes | Enables CDATA breakout injection and crashes `xml.etree.ElementTree.parse` | Escape CDATA terminators, quote XML attributes, and sanitize control bytes in `package_prompt.py` |
| WAP-07 | Cache-busting prefix order | Placing volatile proposal text or timestamps before static directives and context | Breaks prefix KV caching across Anthropic, OpenAI, and Gemini models | Emit canonical byte-identical directives, environment, and context before `<current_proposal>` |
| WAP-08 | Conflicting diff vs rewrite bounds | Asking for under-100-line diffs in `SKILL.md` while demanding full rewrites in templates | Causes web interface timeouts and inconsistent advisor outputs | Align templates to bounded surgical replacements under 100 lines per unit |

## Quick audit checklist

Run this check before pasting an outbound payload or applying an advisor patch:

| Check | Passing condition |
| --- | --- |
| Script integrity | Both `package_prompt.py --self-test` and `audit_response.py --self-test` exit 0 |
| Single-root XML | `XML_VALID=1` recorded in `.agents/state/web-advisor-prompt/emission.txt` |
| Credential redaction | `MATCHES=0` recorded in `.agents/state/web-advisor-prompt/redaction-audit.txt` |
| Prompt budget and hygiene | `LINE_COUNT_LE_1500=1` and `HYGIENE_EXIT=0` in `emission.txt` |
| Ground-truth patch gate | All edited files exist in `verified-findings.json` with zero non-`VERIFIED` items applied |

