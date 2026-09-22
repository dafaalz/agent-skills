#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REFERENCES_DIR = SKILL_DIR / "references"
SCRIPTS_DIR = SKILL_DIR / "scripts"
SKILL_MD = SKILL_DIR / "SKILL.md"

REQUIRED_REFERENCES = [
    "legal-and-ethics.md",
    "visual-tokens-and-typography.md",
    "layout-and-dom-decomposition.md",
    "motion-and-microinteractions.md",
    "tooling-and-code-synthesis.md",
]

EXPECTED_URLS = [
    # Legal & Ethics (8)
    "https://law.justia.com/cases/federal/appellate-courts/F2/982/693/",
    "https://law.justia.com/cases/federal/appellate-courts/F3/35/1435/",
    "https://supreme.justia.com/cases/federal/us/516/233/",
    "https://supreme.justia.com/cases/federal/us/593/18-956/",
    "https://www.copyright.gov/comp3/chap1000/ch1000-websites.pdf",
    "https://supreme.justia.com/cases/federal/us/505/763/",
    "https://www.eff.org/issues/coders/reverse-engineering-faq",
    "https://austinkleon.com/steal/",

    # Visual Tokens & Typography (8)
    "https://developer.chrome.com/docs/css-ui/high-definition-css-color-guide",
    "https://evilmartians.com/chronicles/oklch-in-css-why-we-moved-from-rgb-and-hsl",
    "https://developer.mozilla.org/en-US/docs/Learn/CSS/Styling_text/Variable_fonts_guide",
    "https://www.smashingmagazine.com/2021/04/meet-utopia-fluid-type-space-scales/",
    "https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62",
    "https://www.joshwcomeau.com/css/designing-shadows/",
    "https://css-tricks.com/how-to-get-all-custom-properties-on-a-page-in-javascript/",
    "https://developer.chrome.com/docs/devtools/css",

    # Layout & DOM Decomposition (7)
    "https://ishadeed.com/article/rebuilding-techcrunch-layout-modern-css/",
    "https://labs.jensimmons.com/",
    "https://www.smashingmagazine.com/2018/04/best-practices-grid-layout/",
    "https://moderncss.dev/solutions-to-replace-the-12-column-grid/",
    "https://web.dev/articles/new-responsive",
    "https://web.dev/articles/optimize-cls",
    "https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Document_and_website_structure",

    # Motion & Micro-interactions (8)
    "https://developer.chrome.com/docs/devtools/animations/",
    "https://www.joshwcomeau.com/animation/css-transitions/",
    "https://emilkowal.ski/ui/great-animations",
    "https://lenis.darkroom.engineering/",
    "https://gsap.com/docs/v3/Plugins/ScrollTrigger/",
    "https://tympanus.net/codrops/2021/01/26/magnetic-buttons/",
    "https://webglfundamentals.org/",
    "https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count",

    # Tooling & Code Synthesis (8)
    "https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/",
    "https://playwright.dev/docs/evaluating",
    "https://github.com/gildas-lormeau/SingleFile",
    "https://images.guide/",
    "https://github.com/cure53/DOMPurify",
    "https://tailwindcss.com/docs/styling-with-utility-classes",
    "https://developer.chrome.com/docs/lighthouse/overview/",
    "https://www.w3.org/WAI/ARIA/apg/",
]

BANNED_WORDS = [
    "delve",
    "tapestry",
    "testament to",
    "crucial",
    "pivotal",
    "vibrant",
    "utilize",
    "leverage",
    "holistic",
    "seamless",
    "furthermore",
    "additionally",
]

def check_skill_md():
    errors = []
    if not SKILL_MD.exists():
        return ["SKILL.md does not exist"]
    
    content = SKILL_MD.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    if len(lines) > 250:
        errors.append(f"SKILL.md exceeds 250 lines (has {len(lines)} lines)")
        
    if not content.startswith("---\n"):
        errors.append("SKILL.md missing frontmatter opening ---")
        
    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        errors.append("SKILL.md invalid frontmatter structure")
    else:
        fm = frontmatter_match.group(1)
        if "name: copy-web-design" not in fm:
            errors.append("SKILL.md frontmatter missing 'name: copy-web-design'")
        if "description: Use when" not in fm:
            errors.append("SKILL.md frontmatter description must start with 'Use when'")
            
    return errors

def check_references():
    errors = []
    if not REFERENCES_DIR.exists():
        return ["references directory does not exist"]
        
    for ref_name in REQUIRED_REFERENCES:
        ref_path = REFERENCES_DIR / ref_name
        if not ref_path.exists():
            errors.append(f"Missing reference file: {ref_name}")
            
    # Gather all text from references and SKILL.md
    all_text = ""
    for md_file in SKILL_DIR.glob("**/*.md"):
        all_text += md_file.read_text(encoding="utf-8") + "\n"
        
    # Check all 39 URLs
    for url in EXPECTED_URLS:
        if url not in all_text:
            errors.append(f"Missing expected URL: {url}")
            
    return errors

def check_unslop():
    errors = []
    for md_file in SKILL_DIR.glob("**/*.md"):
        content = md_file.read_text(encoding="utf-8")
        rel_path = md_file.relative_to(SKILL_DIR)
        
        # Check em dash and en dash
        if "—" in content:
            errors.append(f"Em dash found in {rel_path}")
        if "–" in content:
            errors.append(f"En dash found in {rel_path}")
            
        # Check isolated hyphen dash " - "
        for i, line in enumerate(content.splitlines(), start=1):
            if " - " in line and not line.strip().startswith("-"):
                # allow list items but not mid-sentence " - "
                errors.append(f"Hyphen dash found in {rel_path}:{i}: {line}")
                
            # Check banned AI words
            for word in BANNED_WORDS:
                if re.search(r'\b' + re.escape(word) + r'\b', line, re.IGNORECASE):
                    errors.append(f"Banned word '{word}' found in {rel_path}:{i}: {line}")
                    
    return errors

def check_scripts():
    errors = []
    script_file = SCRIPTS_DIR / "extract_tokens.js"
    if not script_file.exists():
        return ["extract_tokens.js does not exist"]
        
    try:
        res = subprocess.run(["node", "-c", str(script_file)], capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"Node syntax check failed: {res.stderr}")
    except Exception as e:
        errors.append(f"Could not run node syntax check: {e}")
        
    return errors

def main():
    print("Running copy-web-design verification test suite...")
    all_errors = []
    
    skill_errors = check_skill_md()
    all_errors.extend(skill_errors)
    
    ref_errors = check_references()
    all_errors.extend(ref_errors)
    
    unslop_errors = check_unslop()
    all_errors.extend(unslop_errors)
    
    script_errors = check_scripts()
    all_errors.extend(script_errors)
    
    if all_errors:
        print(f"FAILED with {len(all_errors)} error(s):")
        for err in all_errors:
            print(f"  [X] {err}")
        sys.exit(1)
    else:
        print("PASS: All 39 sources verified, frontmatter valid, unslop compliant, scripts valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()
