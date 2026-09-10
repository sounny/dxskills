#!/usr/bin/env python3
"""
DxSkills Background Clipboard Listener Daemon
Continuously monitors clipboard for trigger prefixes (e.g., 'dx:' or '/dx ')
and automatically compiles messy inputs into structured D-Mode markdown.
"""

import os
import sys
import time
import subprocess
import argparse

TYPO_DICT = {
    "yestreday": "yesterday",
    "chekc": "check",
    "runing": "running",
    "refrence": "reference",
    "shure": "sure",
    "pct": "%",
    "wont": "won't",
    "reimbused": "reimbursed",
    "architechture": "architecture",
    "delievry": "delivery",
    "milstone": "milestone"
}

def get_clipboard():
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

def set_clipboard(text):
    if sys.platform == "win32":
        try:
            p = subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", "$input | Set-Clipboard"],
                stdin=subprocess.PIPE,
                text=True
            )
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

def compile_text(raw_input):
    clean = raw_input.strip()
    if clean.startswith("dx:"):
        clean = clean[3:].strip()
    elif clean.startswith("/dx "):
        clean = clean[4:].strip()

    words = clean.split()
    corrected_words = []
    typos_fixed = 0
    for w in words:
        stripped = w.lower().strip(".,!?:;()")
        if stripped in TYPO_DICT:
            typos_fixed += 1
            w = w.lower().replace(stripped, TYPO_DICT[stripped])
        corrected_words.append(w)

    clean_text = " ".join(corrected_words).replace("\u2014", " - ")
    sentences = [s.strip() for s in clean_text.split(".") if s.strip()]
    if not sentences:
        sentences = [clean_text]

    bluf = sentences[0]
    if not bluf.endswith("."):
        bluf += "."
    bluf = bluf[0].upper() + bluf[1:]

    rows = []
    remaining = sentences[1:]
    if not remaining:
        rows.append(("Core Objective", "Active", bluf))
    else:
        for idx, s in enumerate(remaining, 1):
            s_low = s.lower()
            if any(k in s_low for k in ["deadline", "friday", "month", "sync", "wednesday"]):
                item = "Timeline / Sync"
                status = "Scheduled"
            elif any(k in s_low for k in ["package", "runway", "work", "proposal"]):
                item = "Deliverable"
                status = "In Progress"
            else:
                item = f"Milestone {idx}"
                status = "Active"
            rows.append((item, status, s))

    md = []
    md.append(f"> **BLUF:** {bluf}")
    md.append("")
    md.append("| Item | Status | Action / Detail |")
    md.append("| :--- | :--- | :--- |")
    for item, status, action in rows:
        md.append(f"| {item} | {status} | {action} |")
    md.append("")
    md.append("### Refined Action Draft")
    md.append("")
    md.append("Team,")
    md.append("")
    md.append(bluf)
    md.append("")
    for item, _, action in rows:
        md.append(f"- **{item}:** {action}")
    md.append("")
    md.append("Let me know if anything is blocked.")

    result = "\n".join(md).replace("\u2014", " - ")
    return result, typos_fixed

def listen_loop(poll_interval=1.0, output_file=None):
    print("[DxSkills Listener] Background clipboard daemon active.")
    print("[DxSkills Listener] Prefix any copied text with 'dx:' or '/dx' to trigger auto-compilation.")
    last_text = get_clipboard()

    try:
        while True:
            time.sleep(poll_interval)
            current_text = get_clipboard()
            if current_text and current_text != last_text:
                last_text = current_text
                if current_text.startswith("dx:") or current_text.startswith("/dx "):
                    print("[DxSkills Listener] Trigger detected on clipboard. Compiling...")
                    compiled_md, typos = compile_text(current_text)
                    set_clipboard(compiled_md)
                    last_text = compiled_md
                    print(f"[DxSkills Listener] Compiled ({typos} typos fixed). Result copied back to clipboard.")
                    
                    if output_file:
                        with open(output_file, "a", encoding="utf-8") as f:
                            f.write("\n\n---\n\n" + compiled_md)
                        print(f"[DxSkills Listener] Appended to {output_file}")
    except KeyboardInterrupt:
        print("\n[DxSkills Listener] Daemon stopped by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DxSkills Background Clipboard Listener")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds")
    parser.add_argument("--log", type=str, default=None, help="Optional markdown file to log compilations")
    args = parser.parse_args()

    listen_loop(poll_interval=args.interval, output_file=args.log)
