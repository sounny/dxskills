#!/usr/bin/env python3
"""
DxSkills Standalone Terminal User Interface (TUI)
Cross-platform speed-of-thought interactive terminal navigator.
Zero external dependencies (works natively on Windows, macOS, and Linux).

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys
import time
import re

# ANSI Color & Style Constants
CLEAR_SCREEN = "\033[2J\033[H"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
WHITE_BG = "\033[47m\033[30m"
DARK_GRAY = "\033[90m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

TYPO_DICT = {
    "teh": "the",
    "taht": "that",
    "waht": "what",
    "wierd": "weird",
    "recieved": "received",
    "recieve": "receive",
    "seperate": "separate",
    "acheive": "achieve",
    "calender": "calendar",
    "definately": "definitely",
    "delievry": "delivery",
    "milstone": "milestone"
}

DIAGRAMS = {
    "1": ("System Architecture Flowchart", """```mermaid
flowchart TD
    Ingress[1. Input Stream / Speech] --> Compiler[2. D-Mode Compiler]
    Compiler --> Core[3. Executive BLUF]
    Compiler --> Matrix[4. Action Matrix]
    Compiler --> Topology[5. Spatial Architecture]
    style Compiler fill:#18181b,stroke:#888,stroke-width:2px,color:#fff
```"""),
    "2": ("Strategy Flywheel Loop", """```mermaid
graph TD
    A([1. Fast Brain Dump]) --> B([2. Visual Spatial Synthesis])
    B --> C([3. High-Leverage Alignment])
    C --> D([4. Accelerated Execution])
    D --> A
```"""),
    "3": ("State Machine Lifecycle", """```mermaid
stateDiagram-v2
    [*] --> RawDraft : Capture Speed-of-Thought
    RawDraft --> SpatialScaffold : Compile D-Mode
    SpatialScaffold --> ReviewMatrix : Review Actions
    ReviewMatrix --> Published : Final Sign-off
    Published --> [*]
```"""),
    "4": ("Decision Matrix", """```mermaid
quadrantChart
    title Decision Prioritization Matrix
    x-axis Low Effort --> High Effort
    y-axis Low Leverage --> High Leverage
    quadrant-1 Strategic Bets
    quadrant-2 Quick Wins
    quadrant-3 Deprioritize
    quadrant-4 Resource Drains
    "D-Mode Compiler": [0.25, 0.85]
    "Quiet Typo Normalizer": [0.18, 0.75]
    "Custom UI Themes": [0.70, 0.30]
    "Manual Formatting": [0.85, 0.15]
```"""),
    "5": ("Concept Mindmap", """```mermaid
mindmap
  root((DxSkills))
    Ingestion
      Whisper Voice
      Raw Brain Dump
    Cognitive Scaffolding
      BLUF
      Action Tables
      Mermaid Topology
    Deliverables
      Executive Briefs
      Architecture Specs
```""")
}


def clear():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def print_banner():
    print(f"{BOLD}================================================================{RESET}")
    print(f"{BOLD}  DxSkills: Speed-of-Thought Cognitive Scaffolding TUI{RESET}")
    print(f"{DIM}  Spatial Reasoning & Anti-Wall-of-Text Interface for Terminal{RESET}")
    print(f"{BOLD}================================================================{RESET}")


def compile_text_d_mode(raw: str) -> str:
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        return "No text entered."

    words = raw.split()
    fixed_words = []
    typo_count = 0
    for w in words:
        clean = w.lower().strip(".,!?:;()")
        if clean in TYPO_DICT:
            typo_count += 1
            w = w.lower().replace(clean, TYPO_DICT[clean])
        fixed_words.append(w)

    clean_text = " ".join(fixed_words).replace("\u2014", " - ")
    sentences = [s.strip() for s in clean_text.split(".") if s.strip()]
    if not sentences:
        sentences = [clean_text]

    bluf = sentences[0]
    if not bluf.endswith("."):
        bluf += "."
    bluf = bluf[0].upper() + bluf[1:]

    out = []
    out.append(f"\n{BOLD}## BLUF (Bottom Line Up Front){RESET}")
    out.append(f"> {CYAN}{bluf}{RESET}\n")

    out.append(f"{BOLD}## Key Takeaways & Drivers{RESET}")
    remaining = sentences[1:]
    if not remaining:
        out.append(f"- {clean_text}")
    else:
        for s in remaining:
            out.append(f"- **Focus:** {s.strip()}")

    out.append(f"\n{BOLD}## Operational Action Matrix{RESET}")
    out.append("| Focus Area | Status | Next Checkpoint |")
    out.append("| :--- | :--- | :--- |")
    for idx, s in enumerate(remaining[:4] if remaining else [bluf], 1):
        out.append(f"| Task {idx} | In Progress | {s[:45]}... |")

    out.append(f"\n{DIM}[Telemetry: Silently stabilized {typo_count} typos | Em dashes: 0]{RESET}")
    return "\n".join(out)


def handle_brain_dump():
    clear()
    print(f"{BOLD}=== [1] Quick-Capture Brain Dump to Architecture ==={RESET}")
    print(f"{DIM}Paste or type raw thoughts below. Submit with an empty line or press Ctrl+C to cancel:{RESET}\n")

    lines = []
    try:
        while True:
            line = input()
            if not line.strip() and len(lines) > 0:
                break
            lines.append(line)
    except KeyboardInterrupt:
        return

    raw_text = "\n".join(lines).strip()
    if not raw_text:
        return

    result = compile_text_d_mode(raw_text)
    print("\n" + result)
    print(f"\n{DIM}Press Enter to return to main menu...{RESET}")
    input()


def handle_anti_wall_of_text():
    clear()
    print(f"{BOLD}=== [2] Anti-Wall-of-Text Reading Filter ==={RESET}")
    print(f"{DIM}Paste dense narrative text below. Submit with an empty line:{RESET}\n")

    lines = []
    try:
        while True:
            line = input()
            if not line.strip() and len(lines) > 0:
                break
            lines.append(line)
    except KeyboardInterrupt:
        return

    raw_text = "\n".join(lines).strip()
    if not raw_text:
        return

    words = raw_text.split()
    paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]

    print(f"\n{BOLD}## High-Signal Cognitive Anchors{RESET}")
    print(f"> {GREEN}Condensed from {len(words)} dense words into visual anchors.{RESET}\n")

    for idx, p in enumerate(paragraphs[:4], 1):
        lead = " ".join(p.split()[:4])
        print(f"- **Point {idx} ({lead}...):** {p[:110]}...")

    print(f"\n{BOLD}## Structured Intake Matrix{RESET}")
    print("| Section | Core Assertion | Operational Implication |")
    print("| :--- | :--- | :--- |")
    for idx, p in enumerate(paragraphs[:3], 1):
        print(f"| Part {idx} | {p[:40]}... | Review and adopt |")

    print(f"\n{DIM}Press Enter to return to main menu...{RESET}")
    input()


def handle_diagram_injection():
    clear()
    print(f"{BOLD}=== [3] Spatial Architecture & Mindmap Generator ==={RESET}")
    print("Select a diagram template to render:\n")
    for key, (title, _) in DIAGRAMS.items():
        print(f"  [{key}] {title}")
    print(f"  [b] Back to Main Menu\n")

    choice = input(f"{BOLD}Select option (1-5): {RESET}").strip()
    if choice in DIAGRAMS:
        title, snippet = DIAGRAMS[choice]
        print(f"\n{BOLD}--- Template: {title} ---{RESET}\n")
        print(snippet)
    print(f"\n{DIM}Press Enter to return to main menu...{RESET}")
    input()


def handle_cognitive_telemetry():
    clear()
    print(f"{BOLD}=== [4] Cognitive Load Reduction Calculator ==={RESET}")
    print(f"{DIM}Enter text or a word count to estimate phonological loop savings:{RESET}\n")

    user_input = input("Enter text or approximate word count (e.g. 250): ").strip()
    if not user_input:
        return

    if user_input.isdigit():
        words_count = int(user_input)
    else:
        words_count = len(user_input.split())

    syllables = int(words_count * 1.5)
    subvocal_sec = syllables * 0.18
    visual_scan_sec = (syllables * 0.45 * 0.18) / 3.2
    time_saved = max(1.0, subvocal_sec - visual_scan_sec)
    drop_pct = 74 if words_count > 25 else 48
    buffer_chunks = min(4, max(2, words_count // 30))

    print(f"\n{BOLD}------------------------------------------------------------{RESET}")
    print(f"  Raw Word Count:              {words_count} words")
    print(f"  Phonological Syllables:      ~{syllables} syllables")
    print(f"  Serial Sub-vocal Rehearsal:  ~{subvocal_sec:.1f}s (phonological loop fatigue)")
    print(f"  Parallel Visual Scanning:    ~{visual_scan_sec:.1f}s (visuospatial sketchpad)")
    print(f"  Decisional Latency Saved:    ~{time_saved:.1f}s faster to action")
    print(f"  Extraneous Load Reduction:   {drop_pct}% reduction")
    print(f"  Optimal Buffer Footprint:    {buffer_chunks} / 4 chunks (Cowan limit compliant)")
    print(f"{BOLD}------------------------------------------------------------{RESET}")

    print(f"\n{DIM}Press Enter to return to main menu...{RESET}")
    input()


def main_menu():
    while True:
        clear()
        print_banner()
        print(f"\n{BOLD}Available Scaffolding Actions:{RESET}\n")
        print(f"  {CYAN}[1]{RESET} Quick-Capture Brain Dump to Architecture")
        print(f"  {CYAN}[2]{RESET} Anti-Wall-of-Text Reading Filter")
        print(f"  {CYAN}[3]{RESET} Insert Spatial Architecture Diagram (Mermaid)")
        print(f"  {CYAN}[4]{RESET} Calculate Cognitive Load & Telemetry")
        print(f"  {CYAN}[5]{RESET} Test Quiet Typo Normalizer")
        print(f"  {CYAN}[q]{RESET} Exit TUI\n")

        choice = input(f"{BOLD}Enter selection: {RESET}").strip().lower()

        if choice == "1":
            handle_brain_dump()
        elif choice == "2":
            handle_anti_wall_of_text()
        elif choice == "3":
            handle_diagram_injection()
        elif choice == "4":
            handle_cognitive_telemetry()
        elif choice == "5":
            clear()
            print(f"{BOLD}=== [5] Quiet Typo Normalizer ==={RESET}\n")
            sample = input("Enter text containing typos (e.g. 'teh calender was recieved yestreday'): ")
            words = sample.split()
            fixed = []
            count = 0
            for w in words:
                c = w.lower().strip(".,!?:;()")
                if c in TYPO_DICT:
                    count += 1
                    w = w.lower().replace(c, TYPO_DICT[c])
                fixed.append(w)
            print(f"\n{GREEN}Clean Text:{RESET} {' '.join(fixed)}")
            print(f"{DIM}Quietly stabilized {count} words without red squiggles.{RESET}")
            print(f"\n{DIM}Press Enter to return to main menu...{RESET}")
            input()
        elif choice in ("q", "quit", "exit"):
            clear()
            print(f"{BOLD}DxSkills TUI closed.{RESET}")
            break


if __name__ == "__main__":
    main_menu()
