#!/usr/bin/env python3
"""
DxSkills Distribution Bundler
Packages the complete skill suite into standalone distribution archives.
"""

import os
import zipfile
import json

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(SKILL_DIR, "dist")
VERSION_FILE = os.path.join(SKILL_DIR, "VERSION")

def get_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "0.1.0"

def build_bundle():
    os.makedirs(DIST_DIR, exist_ok=True)
    version = get_version()
    zip_name = f"dxskills-v{version}.zip"
    zip_path = os.path.join(DIST_DIR, zip_name)
    
    print(f"[DxSkills] Building distribution bundle: {zip_name}...")
    
    include_dirs = ["skills", "prompts", "scripts"]
    include_files = ["README.md", "SKILL.md", "VERSION", "RESEARCH.md", "CITATION.cff", "LICENSE"]
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in include_files:
            p = os.path.join(SKILL_DIR, file)
            if os.path.exists(p):
                zipf.write(p, arcname=file)
                
        for d in include_dirs:
            base_d = os.path.join(SKILL_DIR, d)
            if os.path.exists(base_d):
                for root, _, files in os.walk(base_d):
                    for file in files:
                        if file.endswith(".pyc") or "__pycache__" in root:
                            continue
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, SKILL_DIR)
                        zipf.write(full_path, arcname=rel_path)
                        
    # Build Manifest JSON
    manifest = {
        "name": "dxskills",
        "version": version,
        "description": "Universal cognitive scaffolding for non-linear and spatial thinkers.",
        "repository": "https://github.com/sounny/dxskills",
        "download_url": f"https://github.com/sounny/dxskills/raw/main/dist/{zip_name}",
        "bundle_file": zip_name,
        "active_skills": [
            "dx-dump",
            "dx-read",
            "dx-write",
            "dx-interview",
            "dx-map",
            "dx-voice"
        ]
    }
    
    manifest_path = os.path.join(DIST_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"[DxSkills] Successfully built bundle at {zip_path}")
    print(f"[DxSkills] Manifest written to {manifest_path}")

if __name__ == "__main__":
    build_bundle()
