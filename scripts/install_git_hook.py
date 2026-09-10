#!/usr/bin/env python3
"""
DxSkills Git Hook Installer
Installs the automated pre-commit hook into .git/hooks/pre-commit.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIT_HOOKS_DIR = os.path.join(REPO_ROOT, ".git", "hooks")
TARGET_HOOK_FILE = os.path.join(GIT_HOOKS_DIR, "pre-commit")

HOOK_SCRIPT_CONTENT = """#!/bin/sh
# DxSkills Pre-Commit Gatekeeper
python scripts/pre_commit_hook.py
"""


def install_hook():
    if not os.path.isdir(GIT_HOOKS_DIR):
        print(f"[DxSkills] Error: .git directory not found at {GIT_HOOKS_DIR}")
        sys.exit(1)

    with open(TARGET_HOOK_FILE, "w", encoding="utf-8") as f:
        f.write(HOOK_SCRIPT_CONTENT)

    # Attempt to make executable on Unix/macOS
    try:
        os.chmod(TARGET_HOOK_FILE, 0o755)
    except Exception:
        pass

    print(f"[DxSkills] Successfully installed pre-commit hook at:")
    print(f"           {TARGET_HOOK_FILE}")
    print("[DxSkills] Every 'git commit' will now verify zero em dashes, YAML frontmatter, and 100% benchmark score.")


if __name__ == "__main__":
    install_hook()
