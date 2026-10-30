#!/usr/bin/env python3
"""
Agent Skills AST & Linguistic Linter (lint_skill.py)
Validates SKILL.md against AgentSkills specifications:
1. Strict line budget (<= 250 lines)
2. Frontmatter integrity (name matching, description <= 500 chars, 'Use when', 'Don't use for')
3. Forbidden punctuation (em dash '—', en dash '–', hyphen dash ' - ', pseudo-label colons)
4. Anti-slop vocabulary scan
5. Binary completion criteria per step ('Completion criterion.')
6. One-hop reference integrity and orphan detection
7. Standalone fixture testing and --self-test support
8. R13 Anti-pattern table structure check (5 columns with stable IDs)
9. R9 Deterministic non-fuzzy completion criteria check
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import re
import sys

# Banned punctuation and patterns
PSEUDO_LABEL_RE = re.compile(
    r"^(?:[-*]|\d+\.)?\s*(?:\*\*)?(?:Note|Important|Warning|Caution|Tip|Summary|Notice|Remember|Goal|Context|Rules|Instructions|Takeaway)(?:\*\*)?\s*:\s*\S+",
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
BANNED_WORD_RE = re.compile(
    r"\b(" + "|".join(BANNED_WORDS) + r")\b",
    re.IGNORECASE,
)
REF_LINK_RE = re.compile(r"`?references/([a-zA-Z0-9_\-\./]+\.md)`?")
REF_DIR_RE = re.compile(r"references/(?:[a-zA-Z0-9_\-]+/)+")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
IDENTIFIER_RE = re.compile(r"`([A-Za-z_][A-Za-z0-9_]*)`")

FUZZY_WORDS = {
    "ensure", "should", "appropriate", "sufficient", "reasonable", "equivalent"
}

DUMMY_PHRASES = {
    "hello world", "foo bar", "lorem ipsum", "quick brown fox", "test test", "sample text", "asdfgh"
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
    level: str = "ERROR"  # ERROR or WARNING


def strip_inline_code(line: str) -> str:
    return INLINE_CODE_RE.sub("", line)


def check_r13(content: str) -> list[Finding]:
    findings: list[Finding] = []
    if "## Anti-patterns" not in content:
        return findings
    ap_section = content.split("## Anti-patterns", 1)[1].split("\n## ", 1)[0]
    header_validated = False
    seen_ap_ids = set()
    for line_idx, line in enumerate(ap_section.splitlines(), start=1):
        s_line = line.strip()
        if not s_line.startswith("|") or s_line.startswith("|---"):
            continue
        cols = [c.strip() for c in s_line.strip("|").split("|")]
        if not header_validated:
            norm_headers = [c.lower() for c in cols]
            expected = ["id", "title", "pattern description", "why it fails", "concrete fix"]
            if norm_headers != expected:
                findings.append(
                    Finding(
                        "r13",
                        f"Anti-pattern table header mismatch: expected '| ID | Title | Pattern description | Why it fails | Concrete fix |', got {cols}",
                        line_idx,
                    )
                )
                break
            header_validated = True
            continue

        if len(cols) < 5:
            findings.append(
                Finding(
                    "r13",
                    f"Anti-pattern table row has {len(cols)} columns, requires at least 5 (ID, Title, Pattern description, Why it fails, Concrete fix)",
                    line_idx,
                )
            )
            break

        placeholders = {
            "-", "--", "---", "n/a", "none", "tbd", "tba", "see above", "misc", "various", "todo", "placeholder",
            "xxx", "???", "tbd.", "to be determined", "wip", "lorem ipsum", "foo", "bar", "baz"
        }
        placeholder_cells = [
            idx for idx, c in enumerate(cols[:5])
            if not c or c.lower().strip() in placeholders
        ]
        if placeholder_cells:
            findings.append(
                Finding(
                    "r13",
                    f"Anti-pattern table row {cols[0] or line_idx} has empty or placeholder columns at indices {placeholder_cells}",
                    line_idx,
                )
            )
            break

        # Reject repeated characters / periodic padding / sequential padding / dummy phrases
        has_padding = False
        for c_idx, col_name in enumerate(["Title", "Pattern description", "Why it fails", "Concrete fix"], start=1):
            c_val = cols[c_idx]
            clean = c_val.replace(" ", "").lower()
            if len(clean) >= 4:
                # Periodic string repetition check (e.g. xxxxx, abcabc, ababab)
                if (clean + clean).find(clean, 1) < len(clean):
                    findings.append(
                        Finding(
                            "r13",
                            f"Anti-pattern table row {cols[0] or line_idx} column '{col_name}' has periodic repetition padding ('{c_val}')",
                            line_idx,
                        )
                    )
                    has_padding = True
                    break
                # Sequential alphabet padding check (e.g. abcdef)
                if all(ord(clean[i + 1]) - ord(clean[i]) == 1 for i in range(len(clean) - 1)):
                    findings.append(
                        Finding(
                            "r13",
                            f"Anti-pattern table row {cols[0] or line_idx} column '{col_name}' has sequential character padding ('{c_val}')",
                            line_idx,
                        )
                    )
                    has_padding = True
                    break
            # Dummy filler phrase check (e.g. hello world)
            if c_val.strip().lower() in DUMMY_PHRASES:
                findings.append(
                    Finding(
                        "r13",
                        f"Anti-pattern table row {cols[0] or line_idx} column '{col_name}' contains dummy filler phrase ('{c_val}')",
                        line_idx,
                    )
                )
                has_padding = True
                break
        if has_padding:
            break

        # Length and multi-word substantive checks
        if len(cols[2]) < 10 or len(cols[3]) < 10 or len(cols[4]) < 10 or (len(cols[2].split()) < 3 and "`" not in cols[2]) or len(cols[3].split()) < 2 or len(cols[4].split()) < 2:
            findings.append(
                Finding(
                    "r13",
                    f"Anti-pattern table row {cols[0] or line_idx} has substantive content too short or lacking words (Pattern >=3 words, Why >=2 words, or Fix >=2 words)",
                    line_idx,
                )
            )
            break

        row_id = cols[0]
        if row_id in seen_ap_ids:
            findings.append(
                Finding(
                    "r13",
                    f"Duplicate anti-pattern ID '{row_id}' in anti-patterns table",
                    line_idx,
                )
            )
            break
        seen_ap_ids.add(row_id)
    return findings


def check_r9(lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for line_idx, raw_line in enumerate(lines, start=1):
        s_line = raw_line.strip()
        s_lower = s_line.lower()
        if (
            s_lower.startswith("completion criterion.")
            or s_lower.startswith("completion criterion ")
            or s_lower.startswith("completion criteria.")
            or s_lower.startswith("completion criteria ")
        ):
            # Check if any backticked code token itself is a fuzzy word
            bt_identifiers = IDENTIFIER_RE.findall(s_line)
            for bt in bt_identifiers:
                if bt.lower() in FUZZY_WORDS:
                    findings.append(
                        Finding(
                            "r9",
                            f"Completion criterion contains fuzzy word in code identifier: '`{bt}`'",
                            line_idx,
                        )
                    )
            # Strip only non-fuzzy identifiers before scanning prose
            prose_part = IDENTIFIER_RE.sub(
                lambda m: m.group(0) if m.group(1).lower() in FUZZY_WORDS else "",
                s_line,
            )
            for pattern in FUZZY_PATTERNS:
                if re.search(pattern, prose_part, re.IGNORECASE):
                    findings.append(
                        Finding(
                            "r9",
                            f"Completion criterion contains fuzzy phrase matching '{pattern}'",
                            line_idx,
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

    # For standalone test snippets without frontmatter, only run punctuation/anti-slop/R13/R9 scan
    if is_standalone and not content.startswith("---\n"):
        in_code_fence = False
        for line_idx, raw_line in enumerate(lines, start=1):
            stripped = raw_line.strip()
            if stripped.startswith("```"):
                in_code_fence = not in_code_fence
                continue
            if in_code_fence:
                continue

            clean_line = strip_inline_code(raw_line)

            if "\u2014" in clean_line:
                findings.append(Finding("punctuation", "Contains forbidden em dash ('—')", line_idx))
            if "\u2013" in clean_line:
                findings.append(Finding("punctuation", "Contains forbidden en dash ('–')", line_idx))
            prose_line = clean_line.lstrip()
            if prose_line.startswith(("- ", "* ", "+ ")):
                prose_line = prose_line[2:]
            if " - " in prose_line:
                findings.append(Finding("punctuation", "Contains forbidden hyphen dash (' - ')", line_idx))

            if PSEUDO_LABEL_RE.search(raw_line):
                findings.append(
                    Finding("colon", f"Forbidden pseudo-label colon: '{stripped}'", line_idx)
                )

            prose_without_quotes = re.sub(r'"[^"]*"', '', clean_line)
            match = BANNED_WORD_RE.search(prose_without_quotes)
            if match:
                findings.append(
                    Finding("slop", f"Found banned anti-slop phrase '{match.group(0)}'", line_idx)
                )

        findings.extend(check_r13(content))
        findings.extend(check_r9(lines))

        return target_name, findings

    # Full SKILL.md validation
    # 1. Line budget check (budget: 250)
    line_count = len(lines)
    if line_count > 250:
        findings.append(
            Finding("line_budget", f"SKILL.md exceeds 250 lines (found {line_count})")
        )

    # 2. Frontmatter verification
    if not content.startswith("---\n"):
        findings.append(Finding("frontmatter", "SKILL.md must open with '---'"))
    else:
        parts = content.split("---\n", 2)
        if len(parts) < 3:
            findings.append(Finding("frontmatter", "YAML frontmatter is unclosed"))
        else:
            fm_text = parts[1]
            name_match = re.search(r"^name:\s*([a-z0-9_\-]+)\s*$", fm_text, re.MULTILINE)
            if not name_match:
                findings.append(Finding("frontmatter", "Missing or invalid 'name' field in frontmatter"))
            elif name_match.group(1) != skill_dir.name:
                findings.append(
                    Finding(
                        "frontmatter",
                        f"Frontmatter name '{name_match.group(1)}' does not match directory '{skill_dir.name}'",
                    )
                )

            desc_match = re.search(
                r"^description:\s*(?:>|\|)?\s*\n?([^\n]+(?:\n\s+[^\n]+)*)",
                fm_text,
                re.MULTILINE,
            )
            if not desc_match:
                findings.append(Finding("frontmatter", "Missing 'description' field in frontmatter"))
            else:
                desc = desc_match.group(1).strip()
                if len(desc) > 500:
                    findings.append(
                        Finding("frontmatter", f"Description exceeds 500 characters ({len(desc)} chars)")
                    )
                norm_desc = desc.replace('"', "").replace("'", "")
                if not norm_desc.startswith("Use when"):
                    findings.append(
                        Finding("frontmatter", "Description must begin with 'Use when'")
                    )
                if "Don't use for" not in desc and "Dont use for" not in norm_desc:
                    findings.append(
                        Finding("frontmatter", "Description must include negative bounds ('Don't use for')")
                    )

    # 3. Punctuation, pseudo-labels, and anti-slop scan outside code fences
    in_code_fence = False
    for line_idx, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        clean_line = strip_inline_code(raw_line)

        # Forbidden punctuation
        if "\u2014" in clean_line:
            findings.append(Finding("punctuation", "Contains forbidden em dash ('—')", line_idx))
        if "\u2013" in clean_line:
            findings.append(Finding("punctuation", "Contains forbidden en dash ('–')", line_idx))
        prose_line = clean_line.lstrip()
        if prose_line.startswith(("- ", "* ", "+ ")):
            prose_line = prose_line[2:]
        if " - " in prose_line:
            findings.append(Finding("punctuation", "Contains forbidden hyphen dash (' - ')", line_idx))

        # Pseudo-label colons
        if PSEUDO_LABEL_RE.search(raw_line):
            findings.append(
                Finding("colon", f"Forbidden pseudo-label colon: '{stripped}'", line_idx)
            )

        # Banned anti-slop vocabulary (exempt unslop which defines negative patterns)
        if skill_dir.name != "unslop":
            prose_without_quotes = re.sub(r'"[^"]*"', '', clean_line)
            match = BANNED_WORD_RE.search(prose_without_quotes)
            if match:
                findings.append(
                    Finding("slop", f"Found banned anti-slop phrase '{match.group(0)}'", line_idx)
                )

    # 4. Binary completion criteria check
    in_code_fence = False
    step_heading: str | None = None
    step_line: int = 0
    has_completion = False

    for line_idx, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        if re.match(r"^###?\s+Step\s+\d+", stripped, re.IGNORECASE):
            if step_heading and not has_completion:
                findings.append(
                    Finding(
                        "completion_criteria",
                        f"Step '{step_heading}' missing 'Completion criterion.'",
                        step_line,
                    )
                )
            step_heading = stripped
            step_line = line_idx
            has_completion = False

        if "completion criterion" in stripped.lower():
            has_completion = True

    if step_heading and not has_completion:
        findings.append(
            Finding(
                "completion_criteria",
                f"Step '{step_heading}' missing 'Completion criterion.'",
                step_line,
            )
        )

    # 5. One-hop reference integrity
    ref_matches = set(REF_LINK_RE.findall(content))
    ref_dir = skill_dir / "references"
    ref_dir_prefixes = {m.group(0) for m in REF_DIR_RE.finditer(content)}

    for ref_rel in ref_matches:
        target_ref = ref_dir / ref_rel
        if not target_ref.exists():
            findings.append(Finding("reference", f"Referenced file missing on disk: references/{ref_rel}"))

    if ref_dir.is_dir():
        for disk_ref in ref_dir.rglob("*.md"):
            rel_name = disk_ref.relative_to(ref_dir).as_posix()
            ref_path = f"references/{rel_name}"
            if rel_name not in ref_matches and not any(
                ref_path.startswith(prefix) for prefix in ref_dir_prefixes
            ):
                findings.append(
                    Finding(
                        "orphan_reference",
                        f"Orphan reference file not pointed to by SKILL.md: {ref_path}",
                        level="WARNING",
                    )
                )

            try:
                ref_content = disk_ref.read_text(encoding="utf-8")
                nested_refs = [
                    nested
                    for nested in REF_LINK_RE.findall(ref_content)
                    if (ref_dir / nested).exists()
                ]
                if nested_refs:
                    findings.append(
                        Finding(
                            "reference_depth",
                            f"Multi-hop reference detected in references/{rel_name} pointing to {nested_refs}",
                            level="WARNING",
                        )
                    )
            except Exception:
                pass

    # 6. Anti-pattern table structure check (R13)
    findings.extend(check_r13(content))

    # 7. Fuzzy completion criterion check (R9)
    findings.extend(check_r9(lines))

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

    # positive must FAIL
    _, pos_findings = lint_target(pos_file)
    has_dash_error = any(
        f.category == "punctuation" and "forbidden hyphen dash" in f.message
        for f in pos_findings
    )
    if not has_dash_error:
        print(f"SELF-TEST FAIL: {pos_file.name} did not trigger hyphen dash error", file=sys.stderr)
        return 1

    # negative must PASS
    _, neg_findings = lint_target(neg_file)
    if any(f.level == "ERROR" for f in neg_findings):
        print(f"SELF-TEST FAIL: {neg_file.name} produced errors: {neg_findings}", file=sys.stderr)
        return 1

    # edge must PASS
    _, edge_findings = lint_target(edge_file)
    if any(f.level == "ERROR" for f in edge_findings):
        print(f"SELF-TEST FAIL: {edge_file.name} produced errors: {edge_findings}", file=sys.stderr)
        return 1

    # R13 fixtures
    r13_pos = fixtures_dir / "r13-positive.md"
    r13_neg = fixtures_dir / "r13-negative.md"
    if r13_pos.exists():
        _, r13_pos_f = lint_target(r13_pos)
        if any(f.level == "ERROR" for f in r13_pos_f):
            print(f"SELF-TEST FAIL: {r13_pos.name} produced errors: {r13_pos_f}", file=sys.stderr)
            return 1

    if r13_neg.exists():
        _, r13_neg_f = lint_target(r13_neg)
        has_r13_err = any(f.category == "r13" for f in r13_neg_f)
        if not has_r13_err:
            print(f"SELF-TEST FAIL: {r13_neg.name} did not trigger r13 error", file=sys.stderr)
            return 1

    r13_empty_neg = fixtures_dir / "r13-empty-cell-negative.md"
    if r13_empty_neg.exists():
        _, r13_empty_f = lint_target(r13_empty_neg)
        has_r13_empty_err = any(f.category == "r13" for f in r13_empty_f)
        if not has_r13_empty_err:
            print(f"SELF-TEST FAIL: {r13_empty_neg.name} did not trigger r13 empty cell error", file=sys.stderr)
            return 1

    r13_periodic = fixtures_dir / "r13-periodic-padding-negative.md"
    if r13_periodic.exists():
        _, r13_p_f = lint_target(r13_periodic)
        if not any(f.category == "r13" for f in r13_p_f):
            print(f"SELF-TEST FAIL: {r13_periodic.name} did not trigger r13 error", file=sys.stderr)
            return 1

    r13_seq = fixtures_dir / "r13-sequential-padding-negative.md"
    if r13_seq.exists():
        _, r13_s_f = lint_target(r13_seq)
        if not any(f.category == "r13" for f in r13_s_f):
            print(f"SELF-TEST FAIL: {r13_seq.name} did not trigger r13 error", file=sys.stderr)
            return 1

    r13_dummy = fixtures_dir / "r13-dummy-phrase-negative.md"
    if r13_dummy.exists():
        _, r13_d_f = lint_target(r13_dummy)
        if not any(f.category == "r13" for f in r13_d_f):
            print(f"SELF-TEST FAIL: {r13_dummy.name} did not trigger r13 error", file=sys.stderr)
            return 1

    # R9 fixtures
    r9_pos = fixtures_dir / "r9-fuzzy-positive.md"
    r9_neg = fixtures_dir / "r9-fuzzy-negative.md"
    if r9_pos.exists():
        _, r9_pos_f = lint_target(r9_pos)
        if any(f.level == "ERROR" for f in r9_pos_f):
            print(f"SELF-TEST FAIL: {r9_pos.name} produced errors: {r9_pos_f}", file=sys.stderr)
            return 1

    if r9_neg.exists():
        _, r9_neg_f = lint_target(r9_neg)
        has_r9_err = any(f.category == "r9" for f in r9_neg_f)
        if not has_r9_err:
            print(f"SELF-TEST FAIL: {r9_neg.name} did not trigger r9 error", file=sys.stderr)
            return 1

    r9_bt_neg = fixtures_dir / "r9-backtick-fuzzy-negative.md"
    if r9_bt_neg.exists():
        _, r9_bt_f = lint_target(r9_bt_neg)
        has_r9_bt_err = any(f.category == "r9" for f in r9_bt_f)
        if not has_r9_bt_err:
            print(f"SELF-TEST FAIL: {r9_bt_neg.name} did not trigger r9 error for backticked fuzzy phrase", file=sys.stderr)
            return 1

    r9_bt_ident = fixtures_dir / "r9-backtick-identifier-fuzzy-negative.md"
    if r9_bt_ident.exists():
        _, r9_bi_f = lint_target(r9_bt_ident)
        if not any(f.category == "r9" for f in r9_bi_f):
            print(f"SELF-TEST FAIL: {r9_bt_ident.name} did not trigger r9 error for backticked identifier", file=sys.stderr)
            return 1

    print("PASS self-test (positive, negative, edge, r13, r13-empty, r13-periodic, r13-sequential, r13-dummy, r9, and r9-backtick fixtures verified)")
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

    print("=" * 70)
    print("Agent Skills AST & Linguistic Linter (lint_skill.py)")
    print("=" * 70)

    for item in target_items:
        t_name, findings = lint_target(item)
        errors = [f for f in findings if f.level == "ERROR"]
        warnings = [f for f in findings if f.level == "WARNING"]
        total_errors += len(errors)
        total_warnings += len(warnings)

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
        line_counts = {}
        for item in target_items:
            sk_file = item / "SKILL.md" if item.is_dir() else item
            if sk_file.is_file():
                line_counts[item.name] = len(sk_file.read_text(encoding="utf-8").splitlines())
        # Count failures per category
        cat_errors = {}
        for item in target_items:
            _, item_findings = lint_target(item)
            for f in item_findings:
                if f.level == "ERROR":
                    cat_errors[f.category] = cat_errors.get(f.category, 0) + 1

        rule_keys = [
            ("line_budget", "line_budget"),
            ("frontmatter", "frontmatter"),
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
            "targets_passed": len(target_items) - (total_errors if total_errors <= len(target_items) else len(target_items)),
            "targets_failed": total_errors,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "line_counts": line_counts,
            "max_line_count": max(line_counts.values()) if line_counts else 0,
            "budget_limit": 250,
        }
        print(json.dumps(report, indent=2))
    else:
        print("-" * 70)
        print(f"Summary: {len(target_items)} targets checked. {total_errors} errors, {total_warnings} warnings.")
        print("=" * 70)

    if total_errors > 0 or (args.strict and total_warnings > 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
