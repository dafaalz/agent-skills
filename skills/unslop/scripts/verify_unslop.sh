#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    "Usage:" \
    "  verify_unslop.sh --check-boundaries <file> [--before <before-file>] [--register <conversational|technical-prose>]" \
    "  verify_unslop.sh --check-hygiene <file> [--register <conversational|technical-prose>]" \
    "  verify_unslop.sh --verify-run <audit-meta.json>" >&2
  exit 2
}

MODE=""
TARGET=""
BEFORE=""
REGISTER="technical-prose"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --check-boundaries|--check-hygiene|--verify-run)
      MODE="$1"
      shift
      [ "$#" -gt 0 ] || usage
      TARGET="$1"
      shift
      ;;
    --before)
      shift
      [ "$#" -gt 0 ] || usage
      BEFORE="$1"
      shift
      ;;
    --register)
      shift
      [ "$#" -gt 0 ] || usage
      REGISTER="$1"
      shift
      ;;
    *)
      usage
      ;;
  esac
done

[ -n "$MODE" ] && [ -n "$TARGET" ] || usage
[ -f "$TARGET" ] || { printf 'Target file missing: %s\n' "$TARGET" >&2; exit 1; }

check_hygiene() {
  local file="$1"
  local reg="$2"
  python3 - "$file" "$reg" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
register = sys.argv[2]
raw = path.read_text(encoding="utf-8")

# Isolate unquoted prose by stripping fenced code, inline code, and blockquotes.
no_fences = re.sub(r"```.*?```", "", raw, flags=re.DOTALL)
no_inline = re.sub(r"`[^`\n]+`", "", no_fences)
prose_lines = [
    (idx, ln)
    for idx, ln in enumerate(no_inline.splitlines(), start=1)
    if not ln.lstrip().startswith(">")
]

errors = []
id_particle_re = re.compile(
    r"(?i)(?:^|[\s,(])(nih|deh|dong|kok|kan|sih|nah|lho|yuk)(?:$|[\s,.;:!?\)])"
)
id_stance_adverb_re = re.compile(
    r"(?i)\b(sebenarnya|sejujurnya|pada dasarnya|secara harfiah)\b"
)
trailing_ya_re = re.compile(r"(?i)(?:^|\s)ya[\s.!?]*$")
en_filler_re = re.compile(
    r"(?i)(?:^|[.!?]\s+)(okay|alright|so|well|hmm|wait)(?:,|[\s.!?]|$)"
)
en_stance_adverb_re = re.compile(
    r"(?i)\b(honestly|actually|literally|simply)\b"
)
praise_re = re.compile(
    r"(?i)(?:\b(?:certainly|great question|tentu saja)!|\b(?:good job|nice work|looks great|semoga membantu|sudah rapi dan jelas)\b)"
)
meta_opener_re = re.compile(
    r"(?i)\b(berikut\s+(?:adalah|ini\s+adalah)|di\s+bawah\s+ini\s+adalah)\b"
)
url_re = re.compile(r"https?://[^\s)\]`'\"<>]+|file://[^\s)\]`'\"<>]+", re.I)
file_line_re = re.compile(r"[\w./\\-]+:\d+(?::\d+)?")
timestamp_re = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")
ratio_re = re.compile(r"\b\d+:\d+\b")
math_re = re.compile(r"\$[^$\n]+\$")
cc_re = re.compile(
    r"^(?:[-*+]\s+)?(?:feat|fix|refactor|test|docs|chore|style|perf|ci|build)(?:\([^)]+\))?:\s+",
    re.I,
)

for lineno, line in prose_lines:
    stripped = line.strip()
    if not stripped:
        continue
    prose_line = re.sub(r"^(?:[-*+]|\d+\.)\s+", "", stripped)
    if "\u2014" in line or "\u2013" in line or " - " in prose_line:
        errors.append(f"{path}:{lineno} UNS-1 decorative dash detected")
    if id_particle_re.search(line) or trailing_ya_re.search(line):
        errors.append(f"{path}:{lineno} UNS-13 banned Indonesian colloquial particle detected")
    if id_stance_adverb_re.search(line):
        errors.append(f"{path}:{lineno} UNS-13 banned Indonesian stance adverb detected")
    if en_filler_re.search(line):
        errors.append(f"{path}:{lineno} UNS-13 banned English filler marker detected")
    if en_stance_adverb_re.search(line):
        errors.append(f"{path}:{lineno} UNS-13 banned English stance adverb detected")
    if praise_re.search(line) or meta_opener_re.search(line):
        errors.append(f"{path}:{lineno} UNS-3 chatbot filler or meta-opener detected")

    if not (stripped.startswith("|") and stripped.endswith("|")) and not stripped.endswith(":"):
        cleaned = math_re.sub("", stripped)
        cleaned = url_re.sub("", cleaned)
        cleaned = file_line_re.sub("", cleaned)
        cleaned = timestamp_re.sub("", cleaned)
        cleaned = ratio_re.sub("", cleaned)
        cleaned = cc_re.sub("", cleaned)
        if ":" in cleaned:
            errors.append(f"{path}:{lineno} UNS-2 mid-sentence colon detected")

if register not in ("conversational", "technical-prose"):
    errors.append(f"Invalid register value: {register}")

if errors:
    sys.stderr.write("\n".join(errors) + "\n")
    sys.exit(1)
PY
}

check_boundaries() {
  local file="$1"
  local before_file="${2:-}"
  python3 - "$file" "$before_file" <<'PY'
import collections
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
before_arg = sys.argv[2]
raw = path.read_text(encoding="utf-8")

# Verify balanced code fences and zero leaked quarantine tags in final output.
fence_count = len(re.findall(r"(?m)^```", raw))
if fence_count % 2 != 0:
    sys.stderr.write(f"{path} UNS-5 unbalanced code fence count ({fence_count})\n")
    sys.exit(1)

if re.search(r"</?untrusted_target_text\b", raw, flags=re.IGNORECASE):
    sys.stderr.write(f"{path} UNS-8 leaked quarantine wrapper tag in output\n")
    sys.exit(1)

if before_arg:
    before_path = Path(before_arg)
    if not before_path.is_file():
        sys.stderr.write(f"Before file missing: {before_path}\n")
        sys.exit(1)
    before_raw = before_path.read_text(encoding="utf-8")

    def extract_protected(text: str) -> dict[str, list[str]]:
        return {
            "inline_code": re.findall(r"`[^`\n]+`", text),
            "url": re.findall(r"https?://[^\s)\]`'\"<>]+", text),
            "pragma": re.findall(
                r"<!--\s*(?:prettier-ignore|markdownlint-[a-z-]+|vale\s+(?:on|off)|eslint-[a-z-]+|TOC)\b[^>]*-->",
                text,
            ),
            "math": re.findall(r"\$[^$\n]+\$", text),
            "code_block": re.findall(r"```[\w-]*\n.*?```", text, flags=re.DOTALL),
        }

    before_tokens = extract_protected(before_raw)
    after_tokens = extract_protected(raw)
    errors = []

    for category, b_list in before_tokens.items():
        b_counter = collections.Counter(b_list)
        a_counter = collections.Counter(after_tokens[category])
        for token, count in b_counter.items():
            if a_counter[token] < count:
                display_token = token.replace("\n", " ")
                if len(display_token) > 60:
                    display_token = display_token[:57] + "..."
                errors.append(
                    f"{path} UNS-5 boundary breach: count of protected {category} '{display_token}' "
                    f"dropped from {count} to {a_counter[token]}"
                )

    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        sys.exit(1)
PY
}

verify_run() {
  local meta="$1"
  python3 - "$meta" <<'PY'
import json
import sys
from pathlib import Path

meta_path = Path(sys.argv[1])
data = json.loads(meta_path.read_text(encoding="utf-8"))
required = ("run_id", "mode", "register", "target_scope", "target_path", "match_count")
missing = [k for k in required if k not in data]
if missing:
    sys.stderr.write(f"Missing keys in audit-meta.json: {', '.join(missing)}\n")
    sys.exit(1)

if data["mode"] not in ("detect", "edit"):
    sys.stderr.write(f"Invalid mode: {data['mode']}\n")
    sys.exit(1)

if data["register"] not in ("conversational", "technical-prose"):
    sys.stderr.write(f"Invalid register: {data['register']}\n")
    sys.exit(1)

if data["mode"] == "detect":
    findings = meta_path.parent / "findings.md"
    if not findings.is_file():
        sys.stderr.write(f"Missing detect findings report: {findings}\n")
        sys.exit(1)
    header = "| Line | Rule | Span | Action |"
    if header not in findings.read_text(encoding="utf-8"):
        sys.stderr.write(f"Malformed findings table schema in {findings}\n")
        sys.exit(1)
PY
}

case "$MODE" in
  --check-boundaries)
    check_boundaries "$TARGET" "$BEFORE"
    ;;
  --check-hygiene)
    check_hygiene "$TARGET" "$REGISTER"
    ;;
  --verify-run)
    verify_run "$TARGET"
    ;;
esac
