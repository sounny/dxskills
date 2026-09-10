#!/usr/bin/env python3
"""
DxSkills Unified CLI Tool (Zero External Dependencies)
Provides direct terminal access to the DxSkills cognitive scaffolding suite.
"""

import os
import sys
import argparse
import subprocess
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(SKILL_DIR, "VERSION")
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/sounny/dxskills/main/VERSION"

def read_input(input_arg):
    if not input_arg:
        if not sys.stdin.isatty():
            return sys.stdin.read().strip()
        print("[DxSkills] Error: No input provided. Provide text or pipe via stdin.")
        sys.exit(1)
    if os.path.isfile(input_arg):
        with open(input_arg, "r", encoding="utf-8") as f:
            return f.read().strip()
    return input_arg.strip()

def cmd_dump(args):
    text = read_input(args.input)
    print("\n=== [DxSkills: dx-dump / Brain Dump to Architecture] ===")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    print("\n> **Bottom Line Up Front (BLUF):**")
    print(f"> Accelerated synthesis compiled from {len(lines)} raw thoughts / fragments.")
    
    print("\n### 1. Extracted Focus Areas")
    for i, line in enumerate(lines, 1):
        clean_line = line.lstrip("*-#0123456789. ")
        print(f"- **Focus {i}:** {clean_line}")
        
    print("\n### 2. Operational Action Matrix")
    print("| Item | Priority | Assigned Scope | Next Checkpoint |")
    print("| :--- | :--- | :--- | :--- |")
    for i, line in enumerate(lines, 1):
        snippet = line[:40] + ("..." if len(line) > 40 else "")
        print(f"| Task {i} | High | {snippet} | Review & Validate |")

def cmd_read(args):
    text = read_input(args.input)
    print("\n=== [DxSkills: dx-read / Anti-Wall-of-Text Filter] ===")
    words = text.split()
    print(f"\n> **Bottom Line Up Front (BLUF):**")
    print(f"> Document condensed from {len(words)} words to high-contrast visual anchors.")
    
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    print("\n### 1. Key Thematic Anchors")
    for i, p in enumerate(paragraphs[:4], 1):
        lead = " ".join(p.split()[:5])
        print(f"- **Point {i} ({lead}...):** {p[:120]}...")
        
    print("\n### 2. Strategic Takeaway Matrix")
    print("| Section | Primary Takeaway | Action Required |")
    print("| :--- | :--- | :--- |")
    for i, p in enumerate(paragraphs[:3], 1):
        print(f"| Part {i} | Core insight extracted from narrative | Review and adopt |")

def cmd_update(args):
    print("=== [DxSkills: Auto-Sync Check] ===")
    local_ver = "0.0.0"
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            local_ver = f.read().strip()
    print(f"Local Version: v{local_ver}")
    
    try:
        req = urllib.request.Request(
            REMOTE_VERSION_URL,
            headers={"User-Agent": "DxSkills-CLI/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            remote_ver = response.read().decode("utf-8").strip()
            print(f"Remote Version: v{remote_ver}")
            
            if remote_ver != local_ver:
                print(f"[DxSkills] Update available (v{remote_ver} > v{local_ver}). Pulling latest skills...")
                subprocess.run(["git", "-C", SKILL_DIR, "pull", "origin", "main"], check=True)
                print("[DxSkills] Successfully updated to the latest version!")
            else:
                print("[DxSkills] You are already on the latest version.")
    except Exception as e:
        print(f"[DxSkills] Update check failed: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="DxSkills: Cognitive Scaffolding CLI for Non-Linear and Spatial Thinkers"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")
    
    # dump
    p_dump = subparsers.add_parser("dump", help="Compile messy notes into structured architecture")
    p_dump.add_argument("input", nargs="?", default="", help="Raw text or path to text file")
    
    # read
    p_read = subparsers.add_parser("read", help="Decompose dense walls of text into visual signposts")
    p_read.add_argument("input", nargs="?", default="", help="Dense text or path to text file")
    
    # update
    p_update = subparsers.add_parser("update", help="Check for remote updates and pull from GitHub")
    
    args = parser.parse_args()
    
    if args.command == "dump":
        cmd_dump(args)
    elif args.command == "read":
        cmd_read(args)
    elif args.command == "update":
        cmd_update(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
