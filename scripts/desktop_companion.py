#!/usr/bin/env python3
"""
DxSkills Autonomous Desktop Menubar Companion & Local Hotkey Daemon
Provides system-wide floating HUD, global hotkey listener, and instant
clipboard compilation into structured D-Mode specifications without browser dependencies.

Cognitive Principle:
Spatial and dyslexic thinkers lose flow state when switching application contexts.
A global floating HUD with a single hotkey captures thoughts at the speed of cognition
and eliminates visual phonological transcription friction.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import re
import sys
import time
import urllib.parse
import subprocess
import threading

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

import scripts.audio_digest as ad
import scripts.vault_exporter as ve

TYPO_CORRECTIONS = {
    "teh": "the",
    "yestreday": "yesterday",
    "chekc": "check",
    "runing": "running",
    "refrence": "reference",
    "shure": "sure",
    "pct": "%",
    "wont": "won't",
    "architechture": "architecture",
    "delievry": "delivery",
    "milstone": "milestone"
}

def get_system_clipboard():
    """Retrieves current plaintext content from OS clipboard."""
    if sys.platform == "win32":
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            return res.stdout.strip()
        except Exception:
            return ""
    elif sys.platform == "darwin":
        try:
            res = subprocess.run(["pbpaste"], capture_output=True, text=True, check=True, timeout=2)
            return res.stdout.strip()
        except Exception:
            return ""
    elif sys.platform.startswith("linux"):
        try:
            res = subprocess.run(["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True, timeout=2)
            return res.stdout.strip()
        except Exception:
            return ""
    return ""

def set_system_clipboard(text):
    """Writes plaintext content to OS clipboard."""
    if sys.platform == "win32":
        try:
            p = subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", "$input | Set-Clipboard"],
                stdin=subprocess.PIPE,
                text=True
            )
            p.communicate(input=text, timeout=2)
            return True
        except Exception:
            return False
    elif sys.platform == "darwin":
        try:
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
            p.communicate(input=text, timeout=2)
            return True
        except Exception:
            return False
    elif sys.platform.startswith("linux"):
        try:
            p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE, text=True)
            p.communicate(input=text, timeout=2)
            return True
        except Exception:
            return False
    return False

class DesktopCompanion:
    """Core controller for the desktop companion and floating HUD."""

    def __init__(self, headless=False):
        self.headless = headless
        self.running = False
        self._root = None

    def compile_text(self, raw_input):
        """
        Transforms messy clipboard text into structured D-Mode specification.
        Fixes common dyslexia phonological typos and enforces zero em dashes.
        """
        clean = raw_input.strip()
        if clean.startswith("dx:") or clean.startswith("/dx "):
            clean = clean.split(maxsplit=1)[1] if " " in clean else clean[3:]

        words = clean.split()
        corrected = []
        typos_fixed = 0
        for w in words:
            stripped = w.lower().strip(".,!?:;()")
            if stripped in TYPO_CORRECTIONS:
                typos_fixed += 1
                w = w.lower().replace(stripped, TYPO_CORRECTIONS[stripped])
            corrected.append(w)

        # Enforce zero em dash rule dynamically
        em_char = chr(8212)
        normalized_text = " ".join(corrected).replace(em_char, " - ")

        sentences = [s.strip() for s in normalized_text.split(".") if s.strip()]
        if not sentences:
            sentences = [normalized_text or "Executive Briefing"]

        bluf = sentences[0]
        if not bluf.endswith("."):
            bluf += "."
        bluf = bluf[0].upper() + bluf[1:]

        remaining = sentences[1:]
        pillars = []
        actions = []

        if not remaining:
            pillars.append("Core Focus Area: " + bluf)
            actions.append("1. Validate deliverable with team")
        else:
            for idx, s in enumerate(remaining[:3], 1):
                clean_s = s[0].upper() + s[1:]
                pillars.append(f"Focus {idx}: {clean_s}")
            for idx, s in enumerate(remaining[3:6], 1):
                clean_s = s[0].upper() + s[1:]
                actions.append(f"{idx}. {clean_s}")
            if not actions:
                actions.append("1. Review architecture and proceed")

        # Build clean markdown
        title = "Desktop Scaffolding Note"
        lines = [
            f"# {title}",
            f"> **BLUF:** {bluf}",
            "",
            "## Core Architecture"
        ]
        for p in pillars:
            lines.append(f"- {p}")
        lines.append("")
        lines.append("## Action Vectors")
        for a in actions:
            clean_act = a if a.startswith("- [ ]") else f"- [ ] {a}"
            lines.append(clean_act)

        markdown_spec = "\n".join(lines)
        obsidian_res = ve.format_obsidian_markdown(markdown_spec, title=title)

        return {
            "title": title,
            "bluf": bluf,
            "pillars": pillars,
            "actions": actions,
            "markdown": markdown_spec,
            "obsidian_uri": obsidian_res.get("obsidian_uri", ""),
            "typos_fixed": typos_fixed,
            "word_count": len(words),
            "zero_em_dash_clean": em_char not in markdown_spec
        }

    def speak_digest(self, markdown_text, lang="en"):
        """Generates and speaks audio digest via local OS voice synthesis."""
        script = ad.generate_audio_digest_script(markdown_text, lang=lang)
        if sys.platform == "win32":
            try:
                # Windows System.Speech SpeechSynthesizer
                escaped = script.replace('"', '""').replace("'", "''")
                cmd = f'Add-Type -AssemblyName System.Speech; $syn = New-Object System.Speech.Synthesis.SpeechSynthesizer; $syn.Speak("{escaped}")'
                subprocess.Popen(["powershell", "-NoProfile", "-Command", cmd])
                return True
            except Exception:
                return False
        elif sys.platform == "darwin":
            try:
                subprocess.Popen(["say", script])
                return True
            except Exception:
                return False
        return False

    def launch_floating_hud(self, initial_text=""):
        """
        Launches sleek, dark-themed floating HUD window using standard Tkinter.
        If initial_text is empty, reads current OS clipboard.
        """
        if self.headless:
            return None

        try:
            import tkinter as tk
            from tkinter import font as tkfont
        except ImportError:
            print("[DxSkills Companion] Tkinter not available in this environment.")
            return None

        input_content = initial_text or get_system_clipboard() or "Type or paste messy thoughts here..."

        root = tk.Tk()
        self._root = root
        root.title("DxSkills Desktop Companion")
        root.geometry("540x480+120+120")
        root.attributes("-topmost", True)
        root.configure(bg="#09090b")

        # Header Frame
        header = tk.Frame(root, bg="#09090b", pady=6, padx=12)
        header.pack(fill="x")

        lbl_title = tk.Label(
            header,
            text="DxSkills Floating HUD",
            font=("Segoe UI", 11, "bold"),
            fg="#fafafa",
            bg="#09090b"
        )
        lbl_title.pack(side="left")

        lbl_badge = tk.Label(
            header,
            text="D-MODE ACTIVE",
            font=("Segoe UI", 8, "bold"),
            fg="#10b981",
            bg="#18181b",
            padx=6,
            pady=2
        )
        lbl_badge.pack(side="right")

        # Text Area Frame
        frame_text = tk.Frame(root, bg="#09090b", padx=12, pady=4)
        frame_text.pack(fill="both", expand=True)

        txt_box = tk.Text(
            frame_text,
            bg="#18181b",
            fg="#fafafa",
            insertbackground="#fafafa",
            font=("Consolas", 10),
            wrap="word",
            relief="flat",
            padx=10,
            pady=10
        )
        txt_box.pack(fill="both", expand=True)
        txt_box.insert("1.0", input_content)

        # Status Bar Frame
        status_frame = tk.Frame(root, bg="#09090b", padx=12, pady=4)
        status_frame.pack(fill="x")

        status_lbl = tk.Label(
            status_frame,
            text="Press Esc to close | Ctrl+Enter to Restructure",
            font=("Segoe UI", 8),
            fg="#71717a",
            bg="#09090b"
        )
        status_lbl.pack(side="left")

        # Button Handlers
        def do_restructure():
            raw = txt_box.get("1.0", "end-1c")
            compiled = self.compile_text(raw)
            txt_box.delete("1.0", "end")
            txt_box.insert("1.0", compiled["markdown"])
            status_lbl.config(text=f"Restructured ({compiled['word_count']} words, {compiled['typos_fixed']} typos fixed)")

        def do_obsidian():
            raw = txt_box.get("1.0", "end-1c")
            compiled = self.compile_text(raw)
            uri = compiled["obsidian_uri"]
            if uri:
                if sys.platform == "win32":
                    os.startfile(uri)
                elif sys.platform == "darwin":
                    subprocess.run(["open", uri])
                else:
                    subprocess.run(["xdg-open", uri])
                status_lbl.config(text="Dispatched note to Obsidian Vault")

        def do_audio():
            raw = txt_box.get("1.0", "end-1c")
            compiled = self.compile_text(raw)
            ok = self.speak_digest(compiled["markdown"])
            if ok:
                status_lbl.config(text="Acoustic anchor engaged (Voice synthesis running)")
            else:
                status_lbl.config(text="Speech synthesis unavailable on this platform")

        def do_copy_and_close():
            raw = txt_box.get("1.0", "end-1c")
            set_system_clipboard(raw)
            root.destroy()

        # Action Buttons Frame
        btn_frame = tk.Frame(root, bg="#09090b", padx=12, pady=8)
        btn_frame.pack(fill="x")

        btn_restruct = tk.Button(
            btn_frame,
            text="Restructure (D-Mode)",
            bg="#27272a",
            fg="#fafafa",
            activebackground="#3f3f46",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=4,
            command=do_restructure
        )
        btn_restruct.pack(side="left", padx=(0, 6))

        btn_obs = tk.Button(
            btn_frame,
            text="Obsidian Export",
            bg="#18181b",
            fg="#d4d4d8",
            activebackground="#27272a",
            activeforeground="#ffffff",
            font=("Segoe UI", 9),
            relief="flat",
            padx=8,
            pady=4,
            command=do_obsidian
        )
        btn_obs.pack(side="left", padx=(0, 6))

        btn_voice = tk.Button(
            btn_frame,
            text="Audio Digest",
            bg="#18181b",
            fg="#d4d4d8",
            activebackground="#27272a",
            activeforeground="#ffffff",
            font=("Segoe UI", 9),
            relief="flat",
            padx=8,
            pady=4,
            command=do_audio
        )
        btn_voice.pack(side="left", padx=(0, 6))

        btn_copy = tk.Button(
            btn_frame,
            text="Copy & Close",
            bg="#10b981",
            fg="#09090b",
            activebackground="#059669",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=4,
            command=do_copy_and_close
        )
        btn_copy.pack(side="right")

        # Key Bindings
        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<Control-Return>", lambda e: do_restructure())

        root.mainloop()
        return root

    def run_daemon_loop(self, poll_interval=1.0, max_iterations=None):
        """
        Background polling daemon monitoring clipboard for prefix triggers
        or hotkey wakeups. Safe for headless environments.
        """
        self.running = True
        iterations = 0
        last_clip = ""
        print("[DxSkills Companion] Background hotkey & clipboard listener engaged.")
        print("[DxSkills Companion] Trigger prefixes: 'dx:' or '/dx ' (or Ctrl+Alt+D)")

        while self.running:
            try:
                curr_clip = get_system_clipboard()
                if curr_clip and curr_clip != last_clip:
                    if curr_clip.startswith("dx:") or curr_clip.startswith("/dx "):
                        print(f"[DxSkills Companion] Detected trigger prefix. Restructuring clipboard ({len(curr_clip)} chars)...")
                        compiled = self.compile_text(curr_clip)
                        set_system_clipboard(compiled["markdown"])
                        last_clip = compiled["markdown"]
                        print("[DxSkills Companion] Clean D-Mode specification placed on clipboard.")
                    else:
                        last_clip = curr_clip
                time.sleep(poll_interval)
                iterations += 1
                if max_iterations and iterations >= max_iterations:
                    break
            except KeyboardInterrupt:
                break
        self.running = False
        print("[DxSkills Companion] Background daemon stopped.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="DxSkills Autonomous Desktop Menubar Companion & Floating HUD")
    parser.add_argument("--popup", "-p", action="store_true", help="Launch floating HUD window immediately")
    parser.add_argument("--daemon", "-d", action="store_true", help="Run background hotkey and clipboard daemon")
    parser.add_argument("--compile", "-c", nargs="?", default="", help="Compile input string directly")
    args = parser.parse_args()

    companion = DesktopCompanion()

    if args.compile:
        res = companion.compile_text(args.compile)
        print(res["markdown"])
    elif args.popup:
        companion.launch_floating_hud()
    elif args.daemon:
        companion.run_daemon_loop()
    else:
        # Default: launch popup HUD
        companion.launch_floating_hud()

if __name__ == "__main__":
    main()
