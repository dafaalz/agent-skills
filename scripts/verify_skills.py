#!/usr/bin/env python3
"""Deterministic verification harness for agent skills.

Validates skills in skills/<skill_name>/SKILL.md against 8 automated contract dimensions:
1. Frontmatter check (name matches directory, description format and length bounds)
2. Line count check (<= 250 lines)
3. Modes check (explicit ## Modes section for operational skills)
4. Boundary check (explicit ## Boundary isolation or ## Boundaries section)
5. Punctuation check (zero em dashes, en dashes, or hyphen dashes)
6. Colon check (zero pseudo-labels like Valid action:, Prohibited action:, Note:, etc.)
7. Completion criteria check (every ### Step or ### Phase terminates on Completion criterion.)
8. Checklist check (contains ## Quick audit checklist or reference equivalent)
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys

# Operational skills that require an explicit ## Modes section.
# Non-operational / exempt skills: brainstorming (exploratory branches),
# executing-plans (meta-orchestrator), i18n (specification rules),
# review-a-skill (audit runbook), unslop (styleguide), upsert-codebase-docs (sync doc tool).
OPERATIONAL_SKILLS = {
    "code-review",
    "codebase-design",
    "conventional-commit",
    "copy-web-design",
    "frontend-design",
    "laravel",
    "prototype",
    "react",
    "s13n",
    "schema-migration",
    "security-audit",
    "skill-testing",
    "summarize",
    "systematic-debugging",
    "technical-writing",
    "testing-patterns",
    "ui-motion",
    "ui-ux-review",
    "verification-before-completion",
    "vibe-wise",
    "web-advisor-prompt",
    "workspace-onboarding",
    "writing-for-agents",
    "writing-plans",
}

PSEUDO_LABEL_PATTERN = re.compile(
    r"^(?:[\s\-\*]*)(?:Valid action|Prohibited action|Note|Catatan|Summary|Ringkasan):",
    re.IGNORECASE,
)


@dataclass
class Defect:
    check: str
    message: str
    line_number: int | None = None

    def __str__(self) -> str:
        if self.line_number is not None:
            return f"[{self.check}] Line {self.line_number}: {self.message}"
        return f"[{self.check}] {self.message}"


@dataclass
class SkillReport:
    skill_name: str
    skill_path: Path
    defects: list[Defect] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.defects) == 0


def verify_frontmatter(skill_name: str, content: str, lines: list[str]) -> list[Defect]:
    defects: list[Defect] = []
    if not content.startswith("---"):
        defects.append(Defect("frontmatter", "Missing opening frontmatter delimiter (---)"))
        return defects

    parts = content.split("---", 2)
    if len(parts) < 3:
        defects.append(Defect("frontmatter", "Missing closing frontmatter delimiter (---)"))
        return defects

    fm_text = parts[1]

    # Name check
    name_match = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
    if not name_match:
        defects.append(Defect("frontmatter", "Missing 'name' field in frontmatter"))
    else:
        parsed_name = name_match.group(1).strip().strip("\"'")
        if parsed_name != skill_name:
            defects.append(
                Defect(
                    "frontmatter",
                    f"Frontmatter name '{parsed_name}' does not match directory basename '{skill_name}'",
                )
            )

    # Description check
    desc_match = re.search(r"^description:\s*(.*?)(?=\n[a-zA-Z0-9_-]+:|\Z)", fm_text, re.MULTILINE | re.DOTALL)
    if not desc_match:
        defects.append(Defect("frontmatter", "Missing 'description' field in frontmatter"))
    else:
        raw_desc = desc_match.group(1).strip()
        if (raw_desc.startswith('"') and raw_desc.endswith('"')) or (
            raw_desc.startswith("'") and raw_desc.endswith("'")
        ):
            raw_desc = raw_desc[1:-1].strip()
        normalized_desc = " ".join(raw_desc.split())

        if len(normalized_desc) >= 500:
            defects.append(
                Defect(
                    "frontmatter",
                    f"Description exceeds 500 character limit ({len(normalized_desc)} chars)",
                )
            )

        if not normalized_desc.startswith("Use when"):
            defects.append(
                Defect(
                    "frontmatter",
                    "Description must start with 'Use when' without preceding summary or overview",
                )
            )

        if "Don't use for" not in normalized_desc:
            defects.append(
                Defect(
                    "frontmatter",
                    "Description must contain negative exclusion clause 'Don\\'t use for'",
                )
            )

    return defects


def verify_line_count(lines: list[str]) -> list[Defect]:
    defects: list[Defect] = []
    line_count = len(lines)
    if line_count > 250:
        defects.append(Defect("line_count", f"File exceeds 250 line budget ({line_count} lines)"))
    return defects


def verify_modes(skill_name: str, content: str) -> list[Defect]:
    defects: list[Defect] = []
    if skill_name in OPERATIONAL_SKILLS:
        has_modes = bool(re.search(r"^##\s+(?:Operating\s+)?[Mm]odes\b", content, re.MULTILINE))
        if not has_modes:
            defects.append(
                Defect("modes", f"Operational skill '{skill_name}' missing explicit '## Modes' section")
            )
    return defects


def verify_boundaries(content: str) -> list[Defect]:
    defects: list[Defect] = []
    has_boundary = bool(re.search(r"^##\s+(?:Boundary isolation|Boundaries)\b", content, re.MULTILINE))
    if not has_boundary:
        defects.append(
            Defect("boundary", "Missing explicit '## Boundary isolation' or '## Boundaries' section")
        )
    return defects


def verify_punctuation(lines: list[str]) -> list[Defect]:
    defects: list[Defect] = []
    for line_idx, line in enumerate(lines, start=1):
        if "—" in line:
            defects.append(Defect("punctuation", "Contains forbidden em dash ('—')", line_idx))
        if "–" in line:
            defects.append(Defect("punctuation", "Contains forbidden en dash ('–')", line_idx))
        if " - " in line:
            defects.append(Defect("punctuation", "Contains forbidden hyphen dash (' - ')", line_idx))
    return defects


def verify_colons(lines: list[str]) -> list[Defect]:
    defects: list[Defect] = []
    in_code_fence = False
    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        if PSEUDO_LABEL_PATTERN.search(line):
            defects.append(
                Defect("colon", f"Contains forbidden pseudo-label colon: '{line.strip()}'", line_idx)
            )
    return defects


def verify_completion_criteria(lines: list[str]) -> list[Defect]:
    defects: list[Defect] = []
    in_code_fence = False
    current_step_heading: str | None = None
    current_step_line: int = 0
    current_step_body: list[str] = []

    def check_current_step() -> None:
        if current_step_heading is not None:
            body_text = "\n".join(current_step_body)
            has_criterion = bool(re.search(r"Completion criterion\.", body_text, re.IGNORECASE))
            if not has_criterion:
                defects.append(
                    Defect(
                        "completion_criteria",
                        f"Step '{current_step_heading}' missing checkable 'Completion criterion.'",
                        current_step_line,
                    )
                )

    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            if current_step_heading is not None:
                current_step_body.append(line)
            continue

        if in_code_fence:
            if current_step_heading is not None:
                current_step_body.append(line)
            continue

        # Outside code fence: check for Step or Phase headings
        if re.match(r"^###\s+(?:Step|Phase)\b", line):
            check_current_step()
            current_step_heading = line.strip()
            current_step_line = line_idx
            current_step_body = []
        elif re.match(r"^#{1,3}\s+", line) and current_step_heading is not None:
            # Reached a new section of level 1, 2, or 3
            check_current_step()
            current_step_heading = None
            current_step_line = 0
            current_step_body = []
        else:
            if current_step_heading is not None:
                current_step_body.append(line)

    check_current_step()
    return defects


def verify_checklist(content: str) -> list[Defect]:
    defects: list[Defect] = []
    has_checklist = bool(re.search(r"^##\s+.*checklist\b", content, re.MULTILINE | re.IGNORECASE))
    if not has_checklist:
        defects.append(Defect("checklist", "Missing '## Quick audit checklist' or reference equivalent"))
    return defects


def verify_skill(skill_dir: Path) -> SkillReport:
    skill_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"

    report = SkillReport(skill_name=skill_name, skill_path=skill_file)

    if not skill_file.exists():
        report.defects.append(Defect("file", f"Missing SKILL.md entrypoint at {skill_file}"))
        return report

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as exc:
        report.defects.append(Defect("file", f"Failed to read {skill_file}: {exc}"))
        return report

    lines = content.splitlines()

    report.defects.extend(verify_frontmatter(skill_name, content, lines))
    report.defects.extend(verify_line_count(lines))
    report.defects.extend(verify_modes(skill_name, content))
    report.defects.extend(verify_boundaries(content))
    report.defects.extend(verify_punctuation(lines))
    report.defects.extend(verify_colons(lines))
    report.defects.extend(verify_completion_criteria(lines))
    report.defects.extend(verify_checklist(content))

    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify agent skills against specification and anti-slop guidelines."
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Optional skill directory names to verify. If omitted or --all, verifies all skills.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="check_all",
        help="Verify all skills in skills/ directory.",
    )

    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    skills_root = repo_root / "skills"

    if not skills_root.exists() or not skills_root.is_dir():
        print(f"Error: skills directory not found at {skills_root}", file=sys.stderr)
        return 1

    if args.check_all or len(args.skills) == 0:
        target_dirs = sorted([p for p in skills_root.iterdir() if p.is_dir()])
    else:
        target_dirs = []
        for name in args.skills:
            skill_dir = skills_root / name
            if not skill_dir.exists() or not skill_dir.is_dir():
                print(f"Error: skill '{name}' not found at {skill_dir}", file=sys.stderr)
                return 1
            target_dirs.append(skill_dir)

    reports: list[SkillReport] = []
    for skill_dir in target_dirs:
        report = verify_skill(skill_dir)
        reports.append(report)

    # Print results
    failed_reports = [r for r in reports if not r.passed]
    passed_reports = [r for r in reports if r.passed]

    print("=" * 70)
    print("Agent Skills Automated Verification Harness")
    print("=" * 70)

    for report in reports:
        if report.passed:
            print(f"PASS  {report.skill_name}")
        else:
            print(f"FAIL  {report.skill_name} ({len(report.defects)} defects)")
            for defect in report.defects:
                print(f"      - {defect}")

    print("-" * 70)
    print(
        f"Summary: {len(reports)} skills checked. "
        f"{len(passed_reports)} passed, {len(failed_reports)} failed."
    )
    print("=" * 70)

    return 0 if len(failed_reports) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
