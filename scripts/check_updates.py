#!/usr/bin/env python3
"""
DxSkills Auto-Sync Helper
Checks the remote GitHub repository for newly published skills and updates.
"""

import os
import sys
import subprocess
import urllib.request

REPO_VERSION_URL = "https://raw.githubusercontent.com/sounny/dxskills/main/VERSION"
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_VERSION_FILE = os.path.join(SKILL_DIR, "VERSION")

def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "0.0.0"

def get_remote_version():
    try:
        req = urllib.request.Request(
            REPO_VERSION_URL,
            headers={"User-Agent": "DxSkills-Updater/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode("utf-8").strip()
    except Exception as e:
        print(f"[DxSkills] Unable to check remote version: {e}")
        return None

def update_repository():
    print(f"[DxSkills] Pulling latest skills from https://github.com/sounny/dxskills...")
    try:
        res = subprocess.run(
            ["git", "-C", SKILL_DIR, "pull", "origin", "main"],
            capture_output=True,
            text=True,
            check=True
        )
        print(res.stdout)
        print("[DxSkills] Successfully updated to the latest skills suite!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[DxSkills] Git pull failed: {e.stderr}")
        return False

def main():
    local_ver = get_local_version()
    print(f"[DxSkills] Local version: v{local_ver}")
    
    remote_ver = get_remote_version()
    if not remote_ver:
        sys.exit(1)
        
    print(f"[DxSkills] Remote version: v{remote_ver}")
    
    if remote_ver != local_ver:
        print(f"[DxSkills] New update available (v{remote_ver} > v{local_ver}). Updating...")
        update_repository()
    else:
        print("[DxSkills] You are running the latest version of DxSkills.")

if __name__ == "__main__":
    main()
