#!/usr/bin/env python3
"""Linter and contract verification tool for AgentSkills.

Validates structural, linguistic, and reference integrity contracts for skill directories.
Zero external dependencies. Runs via pure Python standard library.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

BANNED_WORDS = [
    r"\bdelve\b",
    r"\btapestry\b",
    r"\bbeacon\b",
    r"\btestament\b",
    r"\bleverage\b",
    r"\bholistic\b",
    r"\bmultifaceted\b",
    r"\bcornerstone\b",
    r"\bparadigm\b",
    r"\bfoster(?:s|ing)?\b",
    r"\bgame-changer\b",
    r"\bseamless(?:ly)?\b",
    r"\bsynergy\b",
    r"\blinchpin\b",
    r"\bsupercharge\b",
    r"\bstreamline\b",
    r"\bcatalyst\b",
    r"\bparamount\b",
    r"\bwhat most people get wrong\b",
    r"\bhere is what nobody tells you\b",
    r"\bthe uncomfortable truth is\b",
    r"\blet that sink in\b",
    r"\bthink about it\b",
    r"\bplot twist\b",
    r"\bin order to\b",
    r"\bdue to the fact that\b",
    r"\bupon closer inspection\b",
    r"\bhaving analyzed\b",
]

BANNED_WORD_RE = re.compile("|".join(BANNED_WORDS), re.IGNORECASE)
PSEUDO_LABEL_RE = re.compile(
    r"^(?:[-*]|\d+\.)?\s*(?:\*\*)?(?:Note|Important|Warning|Caution|Tip|Summary|Notice|Remember|Goal|Context|Rules|Instructions|Takeaway)(?:\*\*)?\s*:\s*\S+",
    re.IGNORECASE,
)
REF_LINK_RE = re.compile(r"`?references/([a-zA-Z0-9_\-\./]+\.md)`?")
REF_DIR_RE = re.compile(r"references/(?:[a-zA-Z0-9_\-]+/)+")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


@dataclass
class Finding:
    category: str
    message: str
    line: int | None = None
    level: str = "ERROR"  # ERROR or WARNING


def strip_inline_code(line: str) -> str:
    return INLINE_CODE_RE.sub("", line)


def lint_skill(skill_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_file = skill_dir / "SKILL.md"

    if not skill_file.exists():
        findings.append(Finding("structure", f"Missing SKILL.md in {skill_dir}"))
        return findings

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as exc:
        findings.append(Finding("read", f"Failed to read SKILL.md: {exc}"))
        return findings

    lines = content.splitlines()

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

            desc_match = re.search(r"^description:\s*(.+)$", fm_text, re.MULTILINE)
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
        if " - " in clean_line:
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
    # Directory-scoped pointers such as references/rules/ cover every file inside them.
    ref_dir_prefixes = {m.group(0) for m in REF_DIR_RE.finditer(content)}

    for ref_rel in ref_matches:
        target = ref_dir / ref_rel
        if not target.exists():
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

            # Check for nested links to this skill's own references (enforce 1-hop max).
            # Cross-skill pointers and paths in the target repository are not multi-hop.
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

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint and verify AgentSkills contracts.")
    parser.add_argument("targets", nargs="*", help="Skill directories or SKILL.md paths")
    parser.add_argument("--all", action="store_true", help="Lint all skills in active repo")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[3]
    skills_dir = repo_root / "skills"

    if args.all or not args.targets:
        target_dirs = sorted([p for p in skills_dir.iterdir() if p.is_dir()])
    else:
        target_dirs = []
        for t in args.targets:
            p = Path(t)
            if not p.is_absolute():
                if (skills_dir / t).is_dir():
                    p = skills_dir / t
                else:
                    p = Path.cwd() / t
            if p.is_file() and p.name == "SKILL.md":
                p = p.parent
            if p.is_dir():
                target_dirs.append(p)
            else:
                print(f"Error: Target '{t}' not found", file=sys.stderr)
                return 1

    total_errors = 0
    total_warnings = 0

    print("=" * 70)
    print("Agent Skills AST & Linguistic Linter (lint_skill.py)")
    print("=" * 70)

    for s_dir in target_dirs:
        findings = lint_skill(s_dir)
        errors = [f for f in findings if f.level == "ERROR"]
        warnings = [f for f in findings if f.level == "WARNING"]
        total_errors += len(errors)
        total_warnings += len(warnings)

        if not errors and not warnings:
            print(f"PASS  {s_dir.name}")
        elif not errors and warnings:
            print(f"WARN  {s_dir.name} ({len(warnings)} warnings)")
            for w in warnings:
                loc = f"Line {w.line}: " if w.line else ""
                print(f"      - [{w.category}] {loc}{w.message}")
        else:
            print(f"FAIL  {s_dir.name} ({len(errors)} errors, {len(warnings)} warnings)")
            for e in errors:
                loc = f"Line {e.line}: " if e.line else ""
                print(f"      - [{e.category}] {loc}{e.message}")
            for w in warnings:
                loc = f"Line {w.line}: " if w.line else ""
                print(f"      - (warn) [{w.category}] {loc}{w.message}")

    print("-" * 70)
    print(f"Summary: {len(target_dirs)} skills checked. {total_errors} errors, {total_warnings} warnings.")
    print("=" * 70)

    if total_errors > 0 or (args.strict and total_warnings > 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
