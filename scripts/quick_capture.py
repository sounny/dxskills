#!/usr/bin/env python3
"""
DxSkills Quick-Capture Clipboard Utility
Reads messy text from clipboard, formats via D-Mode, and copies result back to clipboard.
"""

import os
import sys
import subprocess

def get_clipboard_text():
    if sys.platform == "win32":
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                capture_output=True,
                text=True,
                check=True
            )
            return res.stdout.strip()
        except Exception:
            return ""
    elif sys.platform == "darwin":
        try:
            res = subprocess.run(["pbpaste"], capture_output=True, text=True, check=True)
            return res.stdout.strip()
        except Exception:
            return ""
    return ""

def set_clipboard_text(text):
    if sys.platform == "win32":
        try:
            p = subprocess.Popen(["powershell", "-NoProfile", "-Command", "$input | Set-Clipboard"], stdin=subprocess.PIPE, text=True)
            p.communicate(input=text)
            return True
        except Exception:
            return False
    elif sys.platform == "darwin":
        try:
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
            p.communicate(input=text)
            return True
        except Exception:
            return False
    return False

def compile_d_mode(raw_text):
    if not raw_text:
        return "No text found on clipboard."
    
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    output = []
    
    # 1. BLUF
    output.append("> **BLUF:** Rapid synthesis compiled from clipboard input.")
    output.append("")
    
    # 2. Key Items
    output.append("### 1. Key Actionable Points")
    for i, line in enumerate(lines, 1):
        clean = line.lstrip("*-#0123456789. ")
        output.append(f"- **Point {i}:** {clean}")
        
    output.append("")
    
    # 3. Action Table
    output.append("### 2. Execution Matrix")
    output.append("| Item | Priority | Scope | Status |")
    output.append("| :--- | :--- | :--- | :--- |")
    for i, line in enumerate(lines, 1):
        short = line[:45] + ("..." if len(line) > 45 else "")
        output.append(f"| Task {i} | High | {short} | In Progress |")
        
    return "\n".join(output)

def main():
    print("[DxSkills Quick-Capture] Reading clipboard...")
    raw = get_clipboard_text()
    if not raw:
        print("[DxSkills Quick-Capture] Clipboard is empty.")
        sys.exit(1)
        
    print(f"[DxSkills Quick-Capture] Read {len(raw)} characters. Compiling in D-Mode...")
    compiled = compile_d_mode(raw)
    
    if set_clipboard_text(compiled):
        print("[DxSkills Quick-Capture] Success! Formatted D-Mode Markdown is now on your clipboard.")
    else:
        print("[DxSkills Quick-Capture] Output:\n")
        print(compiled)

if __name__ == "__main__":
    main()
