#!/usr/bin/env python3
"""
DxSkills ASCII Visual Scaffolding Generator
Generates clean ASCII/Unicode flowcharts, trees, and tables for terminal-only
and SSH environments where visual rendering engines are unavailable.
"""

import sys
import argparse

def render_ascii_flowchart(steps, horizontal=True):
    clean_steps = [s.strip().replace("\u2014", " - ") for s in steps if s.strip()]
    if not clean_steps:
        return ""

    if horizontal:
        # Calculate max width per box (cap at 24 chars for terminal layout)
        box_width = max(len(s) for s in clean_steps)
        box_width = max(box_width + 4, 16)
        
        top_borders = []
        middle_lines = []
        bottom_borders = []
        
        for i, s in enumerate(clean_steps):
            pad_left = (box_width - len(s)) // 2
            pad_right = box_width - len(s) - pad_left
            content = " " * pad_left + s + " " * pad_right
            
            top_borders.append("+" + "-" * box_width + "+")
            middle_lines.append("|" + content + "|")
            bottom_borders.append("+" + "-" * box_width + "+")

        lines = []
        connector_top = "       "
        connector_mid = " ----> "
        connector_bot = "       "

        lines.append(connector_top.join(top_borders))
        lines.append(connector_mid.join(middle_lines))
        lines.append(connector_bot.join(bottom_borders))
        return "\n".join(lines)
    else:
        # Vertical flow
        box_width = max(len(s) for s in clean_steps) + 4
        box_width = max(box_width, 24)
        
        lines = []
        for i, s in enumerate(clean_steps):
            pad_left = (box_width - len(s)) // 2
            pad_right = box_width - len(s) - pad_left
            content = " " * pad_left + s + " " * pad_right
            
            lines.append("+" + "-" * box_width + "+")
            lines.append("|" + content + "|")
            lines.append("+" + "-" * box_width + "+")
            
            if i < len(clean_steps) - 1:
                center = box_width // 2
                lines.append(" " * center + "|")
                lines.append(" " * center + "v")
                
        return "\n".join(lines)

def render_ascii_tree(root_title, branches):
    clean_root = root_title.strip().replace("\u2014", " - ")
    lines = [f"[ {clean_root} ]"]
    
    total = len(branches)
    for idx, b in enumerate(branches):
        clean_b = b.strip().replace("\u2014", " - ")
        is_last = (idx == total - 1)
        prefix = "`-- " if is_last else "|-- "
        lines.append(f"    {prefix}{clean_b}")
        
    return "\n".join(lines)

def render_ascii_table(headers, rows):
    clean_headers = [h.strip().replace("\u2014", " - ") for h in headers]
    clean_rows = [[c.strip().replace("\u2014", " - ") for c in r] for r in rows]
    
    col_widths = [len(h) for h in clean_headers]
    for r in clean_rows:
        for idx, cell in enumerate(r):
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(cell))
            else:
                col_widths.append(len(cell))
                
    # Format separator
    sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    lines = [sep]
    
    # Header row
    h_cells = [f" {clean_headers[i].ljust(col_widths[i])} " for i in range(len(clean_headers))]
    lines.append("|" + "|".join(h_cells) + "|")
    lines.append(sep)
    
    # Data rows
    for r in clean_rows:
        r_cells = [f" {r[i].ljust(col_widths[i])} " if i < len(r) else " " * (col_widths[i] + 2) for i in range(len(col_widths))]
        lines.append("|" + "|".join(r_cells) + "|")
        
    lines.append(sep)
    return "\n".join(lines)

def run_demo():
    print("=== DxSkills Terminal ASCII Visual Architecture Demo ===")
    print("\n1. Horizontal Flowchart:")
    steps = ["1. Brain Dump", "2. D-Mode Parse", "3. Structured BLUF", "4. Team Action"]
    print(render_ascii_flowchart(steps, horizontal=True))
    
    print("\n2. Vertical Pipeline:")
    vsteps = ["Ingest Messy Notes", "Extract Key Deliverables", "Render Visual Hierarchy", "Dispatch Without Fluff"]
    print(render_ascii_flowchart(vsteps, horizontal=False))
    
    print("\n3. Concept Mindmap Tree:")
    branches = [
        "Zero-Friction Input (speech dictation, rough typing)",
        "Anti-Wall-of-Text (BLUF, bold hierarchy, tables)",
        "Silent Mechanical Polish (typo repair without lectures)",
        "Authentic Voice Preservation (zero generic AI filler)"
    ]
    print(render_ascii_tree("Cognitive Scaffolding Architecture", branches))
    
    print("\n4. Structured Execution Matrix:")
    headers = ["Milestone", "Target Date", "Owner", "Status"]
    rows = [
        ["Raycast Extension", "Today", "Core Team", "Shipped"],
        ["Local Ollama Bridge", "Today", "Core Team", "Shipped"],
        ["ASCII Terminal Scaffolder", "Today", "Core Team", "Active"],
        ["Live Web Mindmap", "Upcoming", "UI Team", "Queued"]
    ]
    print(render_ascii_table(headers, rows))

def main():
    parser = argparse.ArgumentParser(description="DxSkills ASCII Visual Scaffolding Generator")
    parser.add_argument("--mode", choices=["flow", "vflow", "tree", "table", "demo"], default="demo", help="Visualization mode")
    parser.add_argument("--root", type=str, default="System Architecture", help="Root title for tree mode")
    args = parser.parse_args()

    if args.mode == "demo":
        run_demo()
        return

    input_data = sys.stdin.read().strip()
    if not input_data:
        print("[DxSkills] No input data provided via stdin. Running demo mode instead.")
        run_demo()
        return

    lines = [l.strip() for l in input_data.splitlines() if l.strip()]

    if args.mode == "flow":
        print(render_ascii_flowchart(lines, horizontal=True))
    elif args.mode == "vflow":
        print(render_ascii_flowchart(lines, horizontal=False))
    elif args.mode == "tree":
        print(render_ascii_tree(args.root, lines))
    elif args.mode == "table":
        # Expect CSV or pipe separated
        delimiter = "|" if "|" in lines[0] else ","
        parsed_rows = [[c.strip() for c in l.split(delimiter) if c.strip()] for l in lines]
        if len(parsed_rows) > 1:
            headers = parsed_rows[0]
            rows = parsed_rows[1:]
            print(render_ascii_table(headers, rows))
        else:
            print("[DxSkills] Need at least 1 header line and 1 data line for table.")

if __name__ == "__main__":
    main()
