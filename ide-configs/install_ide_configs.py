#!/usr/bin/env python3
"""
DxSkills IDE Configuration Installer
Copies or symlinks D-Mode configuration files for Cursor, Claude Code, and Windsurf.
"""

import os
import sys
import shutil
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

CONFIG_MAP = {
    "cursor": [
        (".cursorrules", ".cursorrules"),
    ],
    "claude": [
        ("CLAUDE.md", "CLAUDE.md"),
        (".clauderc", ".clauderc"),
    ],
    "windsurf": [
        (".windsurfrules", ".windsurfrules"),
    ],
}


def install_configs(target_dir: str, ides: list, mode: str = "copy", dry_run: bool = False):
    """Installs IDE configuration files into the target directory."""
    print(f"[DxSkills IDE Setup] Target Directory: {target_dir}")
    print(f"[DxSkills IDE Setup] Mode: {mode.upper()} | Dry Run: {dry_run}")
    print("---------------------------------------------------------------")

    os.makedirs(target_dir, exist_ok=True)
    installed_count = 0

    for ide in ides:
        if ide not in CONFIG_MAP:
            print(f"[Warning] Unknown IDE specified: {ide}")
            continue

        for src_rel, dest_rel in CONFIG_MAP[ide]:
            src_path = os.path.join(SCRIPT_DIR, src_rel)
            dest_path = os.path.join(target_dir, dest_rel)

            if not os.path.exists(src_path):
                print(f"  [Missing] Source file not found: {src_path}")
                continue

            if dry_run:
                print(f"  [Dry Run] Would {mode} {src_rel} -> {dest_rel}")
                installed_count += 1
                continue

            try:
                if os.path.exists(dest_path) or os.path.islink(dest_path):
                    if os.path.islink(dest_path) or os.path.isfile(dest_path):
                        os.remove(dest_path)
                    elif os.path.isdir(dest_path):
                        shutil.rmtree(dest_path)

                if mode == "symlink":
                    try:
                        os.symlink(src_path, dest_path)
                        print(f"  [Symlinked] {src_rel} -> {dest_rel}")
                    except OSError:
                        # Fallback to copy if symlink privileges are missing (e.g. standard Windows user)
                        shutil.copy2(src_path, dest_path)
                        print(f"  [Copied (Symlink fallback)] {src_rel} -> {dest_rel}")
                else:
                    shutil.copy2(src_path, dest_path)
                    print(f"  [Copied] {src_rel} -> {dest_rel}")

                installed_count += 1
            except Exception as e:
                print(f"  [Error] Failed to install {src_rel}: {e}")

    print("---------------------------------------------------------------")
    print(f"[DxSkills IDE Setup] Finished. Total configs configured: {installed_count}")


def main():
    parser = argparse.ArgumentParser(description="Install DxSkills D-Mode IDE configurations.")
    parser.add_argument(
        "--target",
        default=REPO_ROOT,
        help="Target project directory (defaults to repository root).",
    )
    parser.add_argument(
        "--ide",
        choices=["all", "cursor", "claude", "windsurf"],
        default="all",
        help="Target IDE configuration to install (default: all).",
    )
    parser.add_argument(
        "--mode",
        choices=["copy", "symlink"],
        default="copy",
        help="Installation method (default: copy).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the installation without writing files.",
    )

    args = parser.parse_args()

    ides = ["cursor", "claude", "windsurf"] if args.ide == "all" else [args.ide]
    install_configs(target_dir=args.target, ides=ides, mode=args.mode, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
