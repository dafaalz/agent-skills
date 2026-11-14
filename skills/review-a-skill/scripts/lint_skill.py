#!/usr/bin/env python3
"""
Agent Skills Contract & Linguistic Linter (lint_skill.py)
Validates SKILL.md against unified AgentSkills specifications:
1. Strict line budget (<= 250 lines)
2. Frontmatter integrity (kebab-case name matching directory, description <= 500 chars, 'Use when', 'Don't use for')
3. Structural section gates (## Modes for step-based skills, ## Boundary isolation, ## Quick audit checklist)
4. Forbidden punctuation outside frontmatter/code fences/inline code (em dash, en dash, hyphen dash, pseudo-label colons)
5. Anti-slop vocabulary scan
6. Multi-line binary completion criteria per Step/Phase ('Completion criterion.') and R9 non-fuzzy check
7. One-hop reference integrity and explicit orphan detection
8. R13 5-column anti-pattern table structure check across all rows
9. Standalone fixture testing and --self-test support
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys

BUDGET_LIMIT = 250
DESC_CHAR_LIMIT = 500

PSEUDO_LABEL_RE = re.compile(
    r"^(?:[-*]|\d+\.)?\s*(?:\*\*)?(?:Note|Important|Warning|Caution|Tip|Summary|Notice|Remember|Goal|Context|Rules|Instructions|Takeaway|Valid action|Prohibited action|Catatan|Ringkasan)(?:\*\*)?\s*:\s*\S+",
    re.IGNORECASE,
)

BANNED_WORDS = [
    "comprehensive",
    "holistic",
    "seamless",
    "leverage",
    "utilize",
    "robust",
    "crucial",
    "dive deep",
    "elevate",
    "synergy",
    "streamline",
    "revolutionize",
    "cutting-edge",
    "state-of-the-art",
    "vital",
    "paramount",
]
BANNED_WORD_RE = re.compile(r"\b(" + "|".join(BANNED_WORDS) + r")\b", re.IGNORECASE)

REF_LINK_RE = re.compile(r"`?references/([a-zA-Z0-9_\-\./]+\.md)`?")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
IDENTIFIER_RE = re.compile(r"`([A-Za-z_][A-Za-z0-9_]*)`")
KEBAB_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GFM_SEP_RE = re.compile(r"^\|[\s:\-\|]+\|$")
FENCE_OPEN_RE = re.compile(r"^(?:(`{3,})([^`]*)|(~{3,})(.*))$")
COMPLETION_PREFIX_RE = re.compile(
    r"^(?:[-*]|\d+\.)?\s*(?:\*\*)?completion criteri(?:on|a)(?:\*\*)?[.:](?:\s+(.*))?$",
    re.IGNORECASE,
)

FUZZY_WORDS = {
    "ensure",
    "should",
    "appropriate",
    "sufficient",
    "reasonable",
    "equivalent",
}

DUMMY_PHRASES = {
    "hello world",
    "foo bar",
    "lorem ipsum",
    "quick brown fox",
    "test test",
    "sample text",
    "asdfgh",
}

FUZZY_PATTERNS = [
    r"\bensure\b",
    r"\bor equivalent\b",
    r"\bas needed\b",
    r"\bverify that it works\b",
    r"\blooks good\b",
    r"\bseems (?:correct|right)\b",
    r"\bshould\b",
    r"\bappropriate\b",
    r"\bsufficient\b",
    r"\breasonable\b",
    r"\bmanual\s+(?:check|verification)\b",
    r"\bif\s+needed\b",
]


@dataclass
class Finding:
    category: str
    message: str
    line: int | None = None
    level: str = "ERROR"


def strip_inline_code(line: str) -> str:
    return INLINE_CODE_RE.sub("", line)


def compute_outside_fence_mask(lines: list[str], start_line_1idx: int = 1) -> list[bool]:
    mask = [False] * len(lines)
    fence_char = ""
    fence_len = 0
    for idx in range(start_line_1idx - 1, len(lines)):
        stripped = lines[idx].strip()
        if not fence_char:
            m = FENCE_OPEN_RE.match(stripped)
            if m:
                fence_chars = m.group(1) or m.group(3)
                fence_char = fence_chars[0]
                fence_len = len(fence_chars)
                continue
            mask[idx] = True
        else:
            if stripped.startswith(fence_char * fence_len) and stripped.strip(fence_char) == "":
                fence_char = ""
                fence_len = 0
    return mask


def parse_frontmatter(lines: list[str]) -> tuple[int, dict[str, str], list[Finding]]:
    findings: list[Finding] = []
    if not lines or lines[0].strip() != "---":
        findings.append(Finding("frontmatter", "SKILL.md must open with '---' on line 1", 1))
        return 0, {}, findings

    close_idx = -1
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            close_idx = idx
            break

    if close_idx == -1:
        findings.append(Finding("frontmatter", "YAML frontmatter is unclosed", 1))
        return 0, {}, findings

    fm_lines = lines[1:close_idx]
    fields: dict[str, str] = {}
    current_key: str | None = None
    buffer: list[str] = []

    for raw in fm_lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            if current_key is not None:
                buffer.append("")
            continue
        if not raw[0].isspace() and ":" in raw:
            if current_key is not None:
                fields[current_key] = "\n".join(buffer).strip()
            key, val = raw.split(":", 1)
            current_key = key.strip()
            val_stripped = val.strip()
            if val_stripped in {">", ">-", ">+", "|", "|-", "|+"}:
                buffer = []
            else:
                buffer = [val_stripped]
        elif current_key is not None:
            buffer.append(raw.strip())

    if current_key is not None:
        fields[current_key] = "\n".join(buffer).strip()

    return close_idx + 1, fields, findings


def verify_frontmatter(skill_dir_name: str, fields: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    raw_name = fields.get("name", "").strip().strip("\"'")
    if not raw_name:
        findings.append(Finding("frontmatter", "Missing 'name' field in frontmatter", 2))
    else:
        if not KEBAB_NAME_RE.match(raw_name) or len(raw_name) > 64:
            findings.append(
                Finding(
                    "frontmatter",
                    f"Frontmatter name '{raw_name}' must be 1-64 chars lowercase kebab-case",
                    2,
                )
            )
        if raw_name != skill_dir_name:
            findings.append(
                Finding(
                    "frontmatter",
                    f"Frontmatter name '{raw_name}' does not match directory '{skill_dir_name}'",
                    2,
                )
            )

    raw_desc = fields.get("description", "").strip()
    if not raw_desc:
        findings.append(Finding("frontmatter", "Missing 'description' field in frontmatter", 3))
    else:
        if (raw_desc.startswith('"') and raw_desc.endswith('"')) or (
            raw_desc.startswith("'") and raw_desc.endswith("'")
        ):
            raw_desc = raw_desc[1:-1].strip()
        norm_desc = " ".join(raw_desc.split())
        if len(norm_desc) > DESC_CHAR_LIMIT:
            findings.append(
                Finding(
                    "frontmatter",
                    f"Description exceeds {DESC_CHAR_LIMIT} characters ({len(norm_desc)} chars)",
                    3,
                )
            )
        if not norm_desc.startswith("Use when"):
            findings.append(
                Finding("frontmatter", "Description must begin with 'Use when'", 3)
            )
        if "Don't use for" not in norm_desc and "Dont use for" not in norm_desc:
            findings.append(
                Finding("frontmatter", "Description must include negative bounds ('Don't use for')", 3)
            )

    return findings


def check_r13(lines: list[str], prose_mask: list[bool]) -> list[Finding]:
    findings: list[Finding] = []
    ap_start = -1
    for idx, line in enumerate(lines):
        if prose_mask[idx] and re.match(r"^##\s+Anti-patterns\b", line.strip(), re.IGNORECASE):
            ap_start = idx
            break

    if ap_start == -1:
        return findings

    header_validated = False
    seen_ap_ids: set[str] = set()
    placeholders = {
        "-",
        "--",
        "---",
        "n/a",
        "none",
        "tbd",
        "tba",
        "see above",
        "misc",
        "various",
        "todo",
        "placeholder",
        "xxx",
        "???",
        "tbd.",
        "to be determined",
        "wip",
        "lorem ipsum",
        "foo",
        "bar",
        "baz",
    }

    for idx in range(ap_start + 1, len(lines)):
        if not prose_mask[idx]:
            continue
        s_line = lines[idx].strip()
        if s_line.startswith("## "):
            break
        if not s_line.startswith("|"):
            continue
        if GFM_SEP_RE.match(s_line):
            continue

        line_num = idx + 1
        cols = [c.strip() for c in s_line.strip("|").split("|")]

        if not header_validated:
            norm_headers = [c.lower() for c in cols]
            expected = ["id", "title", "pattern description", "why it fails", "concrete fix"]
            if norm_headers != expected:
                findings.append(
                    Finding(
                        "r13",
                        f"Anti-pattern table header mismatch: expected '| ID | Title | Pattern description | Why it fails | Concrete fix |', got {cols}",
                        line_num,
                    )
                )
                return findings
            header_validated = True
            continue

        if len(cols) < 5:
            findings.append(
                Finding(
                    "r13",
                    f"Anti-pattern table row has {len(cols)} columns, requires 5 (ID, Title, Pattern description, Why it fails, Concrete fix)",
                    line_num,
                )
            )
            continue

        placeholder_cells = [
            c_idx for c_idx, c in enumerate(cols[:5]) if not c or c.lower().strip() in placeholders
        ]
        if placeholder_cells:
            findings.append(
                Finding(
                    "r13",
                    f"Anti-pattern table row {cols[0] or line_num} has empty or placeholder columns at indices {placeholder_cells}",
                    line_num,
                )
            )
            continue

        row_has_padding = False
        for c_idx, col_name in enumerate(
            ["Title", "Pattern description", "Why it fails", "Concrete fix"], start=1
        ):
            c_val = cols[c_idx]
            clean = c_val.replace(" ", "").lower()
            if len(clean) >= 4:
                if (clean + clean).find(clean, 1) < len(clean):
                    findings.append(
                        Finding(
                            "r13",
                            f"Anti-pattern table row {cols[0] or line_num} column '{col_name}' has periodic repetition padding ('{c_val}')",
                            line_num,
                        )
                    )
                    row_has_padding = True
                    break
                if all(ord(clean[i + 1]) - ord(clean[i]) == 1 for i in range(len(clean) - 1)):
                    findings.append(
                        Finding(
                            "r13",
                            f"Anti-pattern table row {cols[0] or line_num} column '{col_name}' has sequential character padding ('{c_val}')",
                            line_num,
                        )
                    )
                    row_has_padding = True
                    break
            if c_val.strip().lower() in DUMMY_PHRASES:
                findings.append(
                    Finding(
                        "r13",
                        f"Anti-pattern table row {cols[0] or line_num} column '{col_name}' contains dummy filler phrase ('{c_val}')",
                        line_num,
                    )
                )
                row_has_padding = True
                break

        if row_has_padding:
            continue

        if (
            len(cols[2]) < 10
            or len(cols[3]) < 10
            or len(cols[4]) < 10
            or (len(cols[2].split()) < 3 and "`" not in cols[2])
            or len(cols[3].split()) < 2
            or len(cols[4].split()) < 2
        ):
            findings.append(
                Finding(
                    "r13",
                    f"Anti-pattern table row {cols[0] or line_num} has substantive content too short or lacking words",
                    line_num,
                )
            )
            continue

        row_id = cols[0]
        if row_id in seen_ap_ids:
            findings.append(
                Finding(
                    "r13",
                    f"Duplicate anti-pattern ID '{row_id}' in anti-patterns table",
                    line_num,
                )
            )
            continue
        seen_ap_ids.add(row_id)

    return findings


def scan_fuzzy_criterion_line(text: str, line_num: int) -> list[Finding]:
    findings: list[Finding] = []
    for bt in IDENTIFIER_RE.findall(text):
        if bt.lower() in FUZZY_WORDS:
            findings.append(
                Finding(
                    "r9",
                    f"Completion criterion contains fuzzy word in code identifier: '`{bt}`'",
                    line_num,
                )
            )

    prose_part = IDENTIFIER_RE.sub(
        lambda m: m.group(0) if m.group(1).lower() in FUZZY_WORDS else "",
        text,
    )
    for pattern in FUZZY_PATTERNS:
        if re.search(pattern, prose_part, re.IGNORECASE):
            findings.append(
                Finding(
                    "r9",
                    f"Completion criterion contains fuzzy phrase matching '{pattern}'",
                    line_num,
                )
            )
    return findings


def check_steps_and_r9(
    lines: list[str], prose_mask: list[bool], require_step_existence: bool
) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    step_heading: str | None = None
    step_line = 0
    step_lines: list[tuple[int, str]] = []
    step_count = 0

    def flush_step() -> None:
        if step_heading is None:
            return
        criterion_start = -1
        for rel_idx, (_, s_txt) in enumerate(step_lines):
            if COMPLETION_PREFIX_RE.match(s_txt):
                criterion_start = rel_idx
                break

        if criterion_start == -1:
            if require_step_existence:
                findings.append(
                    Finding(
                        "completion_criteria",
                        f"Step '{step_heading}' missing checkable 'Completion criterion.'",
                        step_line,
                    )
                )
            return

        # Scan ONLY the completion criterion paragraph (stop on blank line gap or bullet/heading)
        prev_ln = step_lines[criterion_start][0] - 1
        for l_num, c_txt in step_lines[criterion_start:]:
            if l_num > prev_ln + 1 and prev_ln >= step_lines[criterion_start][0]:
                break
            if prev_ln >= step_lines[criterion_start][0] and re.match(r"^(?:[-*+]|\d+\.)\s+", c_txt):
                break
            findings.extend(scan_fuzzy_criterion_line(c_txt, l_num))
            prev_ln = l_num

    for idx, raw_line in enumerate(lines):
        if not prose_mask[idx]:
            continue
        stripped = raw_line.strip()
        line_num = idx + 1

        if re.match(r"^###\s+(?:Step|Phase)\b", stripped, re.IGNORECASE):
            flush_step()
            step_heading = stripped
            step_line = line_num
            step_lines = []
            step_count += 1
        elif re.match(r"^#{1,3}\s+", stripped) and step_heading is not None:
            flush_step()
            step_heading = None
            step_line = 0
            step_lines = []
        elif step_heading is not None:
            if stripped:
                step_lines.append((line_num, stripped))
        else:
            if COMPLETION_PREFIX_RE.match(stripped):
                findings.extend(scan_fuzzy_criterion_line(stripped, line_num))

    flush_step()
    return findings, step_count


def check_structural_sections(
    lines: list[str], prose_mask: list[bool], step_count: int
) -> list[Finding]:
    findings: list[Finding] = []
    prose_headings = [
        lines[idx].strip()
        for idx in range(len(lines))
        if prose_mask[idx] and lines[idx].lstrip().startswith("## ")
    ]

    has_modes = any(re.match(r"^##\s+(?:Operating\s+)?Modes\b", h, re.IGNORECASE) for h in prose_headings)
    if step_count > 0 and not has_modes:
        findings.append(
            Finding("modes", "Step-based workflow skill missing explicit '## Modes' section")
        )

    has_boundary = any(
        re.match(r"^##\s+(?:Boundary isolation|Boundaries)\b", h, re.IGNORECASE) for h in prose_headings
    )
    if not has_boundary:
        findings.append(
            Finding("boundary", "Missing explicit '## Boundary isolation' or '## Boundaries' section")
        )

    has_checklist = any(
        re.match(r"^##\s+.*checklist\b", h, re.IGNORECASE) for h in prose_headings
    )
    if not has_checklist:
        findings.append(Finding("checklist", "Missing '## Quick audit checklist' or equivalent checklist section"))

    return findings


def scan_prose_rules(
    lines: list[str], prose_mask: list[bool], exempt_slop: bool
) -> list[Finding]:
    findings: list[Finding] = []
    for idx, raw_line in enumerate(lines):
        if not prose_mask[idx]:
            continue
        line_num = idx + 1
        stripped = raw_line.strip()
        clean_line = strip_inline_code(raw_line)

        if "\u2014" in clean_line:
            findings.append(Finding("punctuation", "Contains forbidden em dash ('\u2014')", line_num))
        if "\u2013" in clean_line:
            findings.append(Finding("punctuation", "Contains forbidden en dash ('\u2013')", line_num))

        prose_line = clean_line.lstrip()
        prose_line = re.sub(r"^(?:[-*+]|\d+\.)\s+", "", prose_line)
        if " - " in prose_line:
            findings.append(Finding("punctuation", "Contains forbidden hyphen dash (' - ')", line_num))

        if PSEUDO_LABEL_RE.search(clean_line.strip()):
            findings.append(
                Finding("colon", f"Forbidden pseudo-label colon: '{stripped}'", line_num)
            )

        if not exempt_slop:
            prose_without_quotes = re.sub(r'"[^"]*"', "", clean_line)
            match = BANNED_WORD_RE.search(prose_without_quotes)
            if match:
                findings.append(
                    Finding("slop", f"Found banned anti-slop phrase '{match.group(0)}'", line_num)
                )

    return findings


def check_references(skill_dir: Path, prose_text: str) -> list[Finding]:
    findings: list[Finding] = []
    ref_matches = set(REF_LINK_RE.findall(prose_text))
    ref_dir = skill_dir / "references"

    for ref_rel in sorted(ref_matches):
        target_ref = ref_dir / ref_rel
        if not target_ref.is_file():
            findings.append(Finding("reference", f"Referenced file missing on disk: references/{ref_rel}"))

    if ref_dir.is_dir():
        for disk_ref in sorted(ref_dir.rglob("*.md")):
            rel_name = disk_ref.relative_to(ref_dir).as_posix()
            ref_path = f"references/{rel_name}"
            if rel_name not in ref_matches:
                findings.append(
                    Finding(
                        "orphan_reference",
                        f"Orphan reference file not pointed to by SKILL.md: {ref_path}",
                        level="WARNING",
                    )
                )

            try:
                ref_content = disk_ref.read_text(encoding="utf-8")
            except Exception as exc:
                findings.append(
                    Finding(
                        "reference_read",
                        f"Failed to read reference file {ref_path}: {exc}",
                        level="WARNING",
                    )
                )
                continue

            nested_refs = [
                nested
                for nested in REF_LINK_RE.findall(ref_content)
                if (ref_dir / nested).exists()
            ]
            if nested_refs:
                findings.append(
                    Finding(
                        "reference_depth",
                        f"Multi-hop reference detected in {ref_path} pointing to {nested_refs}",
                        level="WARNING",
                    )
                )

    return findings


def lint_target(target: Path) -> tuple[str, list[Finding]]:
    findings: list[Finding] = []

    if target.is_file():
        skill_file = target
        skill_dir = target.parent
        target_name = target.name
        is_standalone = target.name != "SKILL.md"
    else:
        skill_dir = target
        skill_file = skill_dir / "SKILL.md"
        target_name = skill_dir.name
        is_standalone = False
        if not skill_file.exists():
            findings.append(Finding("structure", f"Missing SKILL.md in {skill_dir}"))
            return target_name, findings

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as exc:
        findings.append(Finding("read", f"Failed to read {skill_file.name}: {exc}"))
        return target_name, findings

    lines = content.splitlines()

    if is_standalone and (not lines or lines[0].strip() != "---"):
        prose_mask = compute_outside_fence_mask(lines, start_line_1idx=1)
        findings.extend(scan_prose_rules(lines, prose_mask, exempt_slop=False))
        findings.extend(check_r13(lines, prose_mask))
        step_findings, _ = check_steps_and_r9(lines, prose_mask, require_step_existence=False)
        findings.extend(step_findings)
        return target_name, findings

    if len(lines) > BUDGET_LIMIT:
        findings.append(
            Finding("line_budget", f"SKILL.md exceeds {BUDGET_LIMIT} lines (found {len(lines)})")
        )

    body_start_line, fm_fields, fm_findings = parse_frontmatter(lines)
    findings.extend(fm_findings)
    if body_start_line > 0:
        findings.extend(verify_frontmatter(skill_dir.name, fm_fields))
        prose_mask = compute_outside_fence_mask(lines, start_line_1idx=body_start_line)
    else:
        prose_mask = compute_outside_fence_mask(lines, start_line_1idx=1)

    findings.extend(scan_prose_rules(lines, prose_mask, exempt_slop=(skill_dir.name == "unslop")))
    step_findings, step_count = check_steps_and_r9(lines, prose_mask, require_step_existence=True)
    findings.extend(step_findings)
    findings.extend(check_structural_sections(lines, prose_mask, step_count))

    prose_text = "\n".join(lines[idx] for idx in range(len(lines)) if prose_mask[idx])
    findings.extend(check_references(skill_dir, prose_text))
    findings.extend(check_r13(lines, prose_mask))

    return target_name, findings


def lint_skill(skill_dir: Path) -> list[Finding]:
    _, findings = lint_target(skill_dir)
    return findings


def run_self_test(repo_root: Path) -> int:
    fixtures_dir = repo_root / "skills" / "review-a-skill" / "scripts" / "fixtures" / "lint"
    if not fixtures_dir.is_dir():
        print(f"Error: Fixtures directory not found: {fixtures_dir}", file=sys.stderr)
        return 1

    pos_file = fixtures_dir / "hyphen-dash-positive.md"
    neg_file = fixtures_dir / "hyphen-dash-negative.md"
    edge_file = fixtures_dir / "hyphen-dash-edge.md"

    _, pos_findings = lint_target(pos_file)
    if not any(f.category == "punctuation" and "forbidden hyphen dash" in f.message for f in pos_findings):
        print(f"SELF-TEST FAIL: {pos_file.name} did not trigger hyphen dash error", file=sys.stderr)
        return 1

    for clean_fixture in (neg_file, edge_file):
        _, clean_findings = lint_target(clean_fixture)
        if any(f.level == "ERROR" for f in clean_findings):
            print(f"SELF-TEST FAIL: {clean_fixture.name} produced errors: {clean_findings}", file=sys.stderr)
            return 1

    positive_r13 = fixtures_dir / "r13-positive.md"
    if positive_r13.exists():
        _, r13_pos_f = lint_target(positive_r13)
        if any(f.level == "ERROR" for f in r13_pos_f):
            print(f"SELF-TEST FAIL: {positive_r13.name} produced errors: {r13_pos_f}", file=sys.stderr)
            return 1

    negative_r13_names = [
        "r13-negative.md",
        "r13-empty-cell-negative.md",
        "r13-periodic-padding-negative.md",
        "r13-sequential-padding-negative.md",
        "r13-dummy-phrase-negative.md",
    ]
    for name in negative_r13_names:
        fpath = fixtures_dir / name
        if fpath.exists():
            _, f_list = lint_target(fpath)
            if not any(f.category == "r13" for f in f_list):
                print(f"SELF-TEST FAIL: {name} did not trigger r13 error", file=sys.stderr)
                return 1

    r9_pos = fixtures_dir / "r9-fuzzy-positive.md"
    if r9_pos.exists():
        _, r9_pos_f = lint_target(r9_pos)
        if any(f.level == "ERROR" for f in r9_pos_f):
            print(f"SELF-TEST FAIL: {r9_pos.name} produced errors: {r9_pos_f}", file=sys.stderr)
            return 1

    negative_r9_names = [
        "r9-fuzzy-negative.md",
        "r9-backtick-fuzzy-negative.md",
        "r9-backtick-identifier-fuzzy-negative.md",
    ]
    for name in negative_r9_names:
        fpath = fixtures_dir / name
        if fpath.exists():
            _, f_list = lint_target(fpath)
            if not any(f.category == "r9" for f in f_list):
                print(f"SELF-TEST FAIL: {name} did not trigger r9 error", file=sys.stderr)
                return 1

    print("PASS self-test (all punctuation, r13, and r9 fixtures verified)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint and verify AgentSkills contracts.")
    parser.add_argument("targets", nargs="*", help="Skill directories or SKILL.md paths")
    parser.add_argument("--all", action="store_true", help="Lint all skills in active repo")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--self-test", action="store_true", help="Run self-tests on test fixtures")
    parser.add_argument("--json", action="store_true", help="Output machine-readable execution metrics JSON")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[3]
    skills_dir = repo_root / "skills"

    if args.self_test:
        return run_self_test(repo_root)

    if args.all or not args.targets:
        target_items = sorted([p for p in skills_dir.iterdir() if p.is_dir()])
    else:
        target_items = []
        for t in args.targets:
            p = Path(t)
            if not p.is_absolute():
                if (skills_dir / t).is_dir():
                    p = skills_dir / t
                elif (Path.cwd() / t).exists():
                    p = Path.cwd() / t
                elif (skills_dir / t).exists():
                    p = skills_dir / t
            if p.is_file() and p.name == "SKILL.md":
                p = p.parent
            if p.exists():
                target_items.append(p)
            else:
                print(f"Error: Target '{t}' not found", file=sys.stderr)
                return 1

    total_errors = 0
    total_warnings = 0
    failed_target_count = 0
    all_results: list[tuple[Path, str, list[Finding]]] = []

    if not args.json:
        print("=" * 70)
        print("Agent Skills Contract & Linguistic Linter (lint_skill.py)")
        print("=" * 70)

    for item in target_items:
        t_name, findings = lint_target(item)
        all_results.append((item, t_name, findings))
        errors = [f for f in findings if f.level == "ERROR"]
        warnings = [f for f in findings if f.level == "WARNING"]
        total_errors += len(errors)
        total_warnings += len(warnings)
        if errors or (args.strict and warnings):
            failed_target_count += 1

        if not args.json:
            if not errors and not warnings:
                print(f"PASS  {t_name}")
            elif not errors and warnings:
                print(f"WARN  {t_name} ({len(warnings)} warnings)")
                for w in warnings:
                    loc = f"Line {w.line}: " if w.line else ""
                    print(f"      - [{w.category}] {loc}{w.message}")
            else:
                print(f"FAIL  {t_name} ({len(errors)} errors, {len(warnings)} warnings)")
                for e in errors:
                    loc = f"Line {e.line}: " if e.line else ""
                    print(f"      - [{e.category}] {loc}{e.message}")
                for w in warnings:
                    loc = f"Line {w.line}: " if w.line else ""
                    print(f"      - (warn) [{w.category}] {loc}{w.message}")

    if args.json:
        line_counts: dict[str, int] = {}
        cat_errors: dict[str, int] = {}
        for item, _, item_findings in all_results:
            sk_file = item / "SKILL.md" if item.is_dir() else item
            if sk_file.is_file():
                line_counts[item.name] = len(sk_file.read_text(encoding="utf-8").splitlines())
            for f in item_findings:
                if f.level == "ERROR":
                    cat_errors[f.category] = cat_errors.get(f.category, 0) + 1

        rule_keys = [
            ("line_budget", "line_budget"),
            ("frontmatter", "frontmatter"),
            ("modes", "modes"),
            ("boundary", "boundary"),
            ("checklist", "checklist"),
            ("punctuation", "punctuation"),
            ("pseudo_labels", "colon"),
            ("anti_slop", "slop"),
            ("completion_criteria", "completion_criteria"),
            ("references", "reference"),
            ("r13_anti_patterns", "r13"),
            ("r9_fuzzy_criteria", "r9"),
        ]
        rules_array = [
            {"id": rid, "checked": len(target_items), "failed": cat_errors.get(cat, 0)}
            for rid, cat in rule_keys
        ]

        report = {
            "rules": rules_array,
            "rules_executed": [r["id"] for r in rules_array],
            "targets_checked": len(target_items),
            "targets_passed": len(target_items) - failed_target_count,
            "targets_failed": failed_target_count,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "line_counts": line_counts,
            "max_line_count": max(line_counts.values()) if line_counts else 0,
            "budget_limit": BUDGET_LIMIT,
        }
        print(json.dumps(report, indent=2))
    else:
        print("-" * 70)
        print(
            f"Summary: {len(target_items)} targets checked. "
            f"{len(target_items) - failed_target_count} passed, {failed_target_count} failed "
            f"({total_errors} errors, {total_warnings} warnings)."
        )
        print("=" * 70)

    if failed_target_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
