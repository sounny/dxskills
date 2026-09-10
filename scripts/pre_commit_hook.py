#!/usr/bin/env python3
"""
DxSkills Automated Git Pre-Commit Quality & Compliance Hook

Enforces:
1. STRICT ZERO EM DASH POLICY (Unicode U+2014) across all repository files.
2. YAML Frontmatter validity for all SKILL.md files.
3. 100% pass rate on the synthetic benchmark evaluation suite.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORE_DIRS = {".git", "dist", "node_modules", ".vscode", "__pycache__", "out"}
TEXT_EXTENSIONS = {".md", ".py", ".html", ".js", ".ts", ".json", ".typ", ".cff", ".yml", ".yaml", ".txt", ".mmd"}


def check_zero_em_dashes() -> int:
    """Scans all tracked text files for em dashes (Unicode U+2014)."""
    violations = []

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in TEXT_EXTENSIONS:
                continue

            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, REPO_ROOT)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_idx, line in enumerate(f, 1):
                        if "\u2014" in line:
                            violations.append((relpath, line_idx, line.strip()))
            except Exception:
                continue

    if violations:
        print("\n[PRE-COMMIT ERROR] Em Dash Policy Violation Detected!")
        print("Strict Rule: NO em dashes (Unicode U+2014). Use hyphens, commas, or parentheses.\n")
        for path, line_no, content in violations:
            print(f"  {path}:{line_no} -> {content[:70]}")
        print(f"\nTotal violations: {len(violations)}")
        return 1

    print("[PRE-COMMIT] Zero em dashes verified across all repository files.")
    return 0


def check_skill_frontmatter() -> int:
    """Verifies that all modular skills contain valid YAML frontmatter."""
    skills_dir = os.path.join(REPO_ROOT, "skills")
    if not os.path.isdir(skills_dir):
        return 0

    missing_frontmatter = []
    for skill_name in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
        if os.path.isfile(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()
            if not content.startswith("---"):
                missing_frontmatter.append(skill_name)
            elif "name:" not in content or "description:" not in content:
                missing_frontmatter.append(skill_name)

    if missing_frontmatter:
        print(f"\n[PRE-COMMIT ERROR] Skills missing valid YAML frontmatter: {missing_frontmatter}")
        return 1

    print("[PRE-COMMIT] Skill YAML frontmatter verified.")
    return 0


def run_benchmarks() -> int:
    """Runs the synthetic evaluation benchmark suite."""
    eval_script = os.path.join(REPO_ROOT, "scripts", "eval_benchmarks.py")
    if not os.path.isfile(eval_script):
        return 0

    res = subprocess.run([sys.executable, eval_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0 or "100.0%" not in res.stdout:
        print("\n[PRE-COMMIT ERROR] Benchmark evaluation failed!")
        print(res.stdout)
        print(res.stderr)
        return 1

    print("[PRE-COMMIT] Benchmark evaluation score: 100.0% (Passed).")
    return 0


def main():
    print("================================================================")
    print("  DxSkills Pre-Commit Quality & Compliance Verification")
    print("================================================================")

    step1 = check_zero_em_dashes()
    if step1 != 0:
        sys.exit(step1)

    step2 = check_skill_frontmatter()
    if step2 != 0:
        sys.exit(step2)

    step3 = run_benchmarks()
    if step3 != 0:
        sys.exit(step3)

    print("================================================================")
    print("  All Quality Gates Passed! Ready to Commit.")
    print("================================================================")
    sys.exit(0)


if __name__ == "__main__":
    main()
