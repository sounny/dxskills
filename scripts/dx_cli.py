#!/usr/bin/env python3
"""
DxSkills Unified CLI Tool (Zero External Dependencies)
Provides direct terminal access to the DxSkills cognitive scaffolding suite.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys
import re
import json
import argparse
import subprocess
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)
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
    print("\n> **Bottom Line Up Front (BLUF):**")
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

def cmd_export(args):
    text = read_input(args.input)
    fmt = args.format.lower()
    out_file = args.output
    title = args.title or "Executive Strategic Briefing"

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    bluf = lines[0] if lines else "Operational summary and key directive."
    remaining = lines[1:] if len(lines) > 1 else [bluf]

    takeaways = remaining[:3]
    matrix_rows = []
    for idx, item in enumerate(remaining[:4], 1):
        clean_item = item.lstrip("*-#0123456789. ")
        matrix_rows.append((f"Deliverable {idx}", "In Progress", clean_item))

    if fmt == "typst":
        if not out_file:
            out_file = "briefing.typ"
        typ_content = f"""// DxSkills Exported Typst Briefing
#import "templates/executive_briefing.typ": executive-briefing

#show: doc => executive-briefing(
  title: "{title}",
  subtitle: "Single-Page Spatial Scaffolding",
  author: "DxSkills Compiler",
  date: "2026-09-10",
  classification: "INTERNAL STRATEGY",
  bluf: "{bluf}",
  takeaways: (
"""
        for t in takeaways:
            clean_t = t.lstrip("*-#0123456789. ").replace('"', '\\"')
            typ_content += f'    [{clean_t}],\n'
        typ_content += "  ),\n  action-items: (\n"
        for r in matrix_rows:
            typ_content += f'    ("{r[0]}", "{r[1]}", "{r[2]}"),\n'
        typ_content += "  ),\n  doc\n)\n"

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(typ_content)
        print(f"[DxSkills] Exported Typst briefing: {out_file}")

    elif fmt in ("html", "pdf"):
        if not out_file:
            out_file = "briefing.html" if fmt == "html" else "briefing.pdf"

        template_path = os.path.join(SKILL_DIR, "templates", "executive_briefing.html")
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                html_template = f.read()
        else:
            html_template = "<html><body><h1>DxSkills Briefing</h1></body></html>"

        html_rendered = html_template.replace("Executive Strategic Briefing", title)
        html_rendered = html_rendered.replace("Milestone 2 cutover scheduled for Friday at 5:00 PM with zero production downtime expected across secondary clusters.", bluf)

        li_items = "".join([f"<li><strong>Point {i}:</strong> {t.lstrip('*-#0123456789. ')}</li>\n        " for i, t in enumerate(takeaways, 1)])
        old_li_block = (
            '<li><strong>Redundancy:</strong> Secondary failover clusters verified in Frankfurt and Ireland regions.</li>\n'
            '        <li><strong>Performance:</strong> Database synchronization lag sustained below 24 milliseconds.</li>\n'
            '        <li><strong>Configuration:</strong> Coordinate reference systems (CRS) updated across geospatial microservices.</li>'
        )
        if old_li_block in html_rendered:
            html_rendered = html_rendered.replace(old_li_block, li_items.strip())

        html_path = out_file if fmt == "html" else out_file.replace(".pdf", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_rendered)
        print(f"[DxSkills] Exported printable HTML briefing: {html_path}")

        if fmt == "pdf":
            try:
                subprocess.run(["typst", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                temp_typ = out_file.replace(".pdf", ".typ")
                subprocess.run(["typst", "compile", temp_typ, out_file], check=True)
                print(f"[DxSkills] Compiled PDF successfully: {out_file}")
            except Exception:
                print(f"[DxSkills] PDF notice: Typst CLI not found on PATH. Generated print-ready HTML at '{html_path}'.")
                print("           Open in any browser and press Ctrl+P -> Save as PDF for publication-grade output.")

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
    
    # export
    p_export = subparsers.add_parser("export", help="Export notes to Typst, HTML, or PDF executive briefings")
    p_export.add_argument("input", nargs="?", default="", help="Raw text or path to file")
    p_export.add_argument("--format", "-f", choices=["typst", "html", "pdf"], default="html", help="Output format (default: html)")
    p_export.add_argument("--output", "-o", default="", help="Output filepath")
    p_export.add_argument("--title", "-t", default="", help="Document title")

    # update
    p_update = subparsers.add_parser("update", help="Check for remote updates and pull from GitHub")

    # tui
    p_tui = subparsers.add_parser("tui", help="Launch interactive terminal scaffolding interface")

    # stamina
    p_stamina = subparsers.add_parser("stamina", help="Estimate working memory fatigue and phonological load")
    p_stamina.add_argument("--minutes", "-m", type=int, default=30, help="Minutes of active drafting (default: 30)")
    p_stamina.add_argument("--words", "-w", type=int, default=500, help="Words drafted or processed (default: 500)")

    # reset
    p_reset = subparsers.add_parser("reset", help="Launch 60-second terminal box breathing spatial reset")
    p_reset.add_argument("--cycles", "-c", type=int, default=3, help="Number of 16-second breathing cycles (default: 3)")

    # obsidian
    p_obsidian = subparsers.add_parser("obsidian", help="Export notes to native Obsidian vault Markdown with frontmatter")
    p_obsidian.add_argument("input", nargs="?", default="", help="Raw text or path to file")
    p_obsidian.add_argument("--vault", "-v", default="", help="Target Obsidian vault name")
    p_obsidian.add_argument("--title", "-t", default="", help="Note title")
    p_obsidian.add_argument("--tags", default="dxskills,cognitive-scaffolding", help="Comma-separated tags")
    p_obsidian.add_argument("--output", "-o", default="", help="Output filepath")

    # notion
    p_notion = subparsers.add_parser("notion", help="Export notes to structured Notion page block payload")
    p_notion.add_argument("input", nargs="?", default="", help="Raw text or path to file")
    p_notion.add_argument("--database", "-d", default="", help="Target Notion database ID")
    p_notion.add_argument("--title", "-t", default="", help="Page title")
    p_notion.add_argument("--webhook", "-w", default="", help="Webhook URL to dispatch payload")
    p_notion.add_argument("--output", "-o", default="", help="Output JSON filepath")

    # audio
    p_audio = subparsers.add_parser("audio", help="Generate spoken audio digest script or synthesize WAV audio")
    p_audio.add_argument("input", nargs="?", default="", help="Raw text or path to file")
    p_audio.add_argument("--title", "-t", default="", help="Title for the audio overview")
    p_audio.add_argument("--lang", "-l", default="en", choices=["en", "fr"], help="Language ('en' or 'fr')")
    p_audio.add_argument("--output", "-o", default="", help="Output WAV audio filepath (synthesizes audio if provided)")

    # canvas
    p_canvas = subparsers.add_parser("canvas", help="Export notes to Obsidian Canvas (.canvas) JSON or vector SVG")
    p_canvas.add_argument("input", nargs="?", default="", help="Raw text or path to file")
    p_canvas.add_argument("--title", "-t", default="", help="Note title")
    p_canvas.add_argument("--format", "-f", default="canvas", choices=["canvas", "svg"], help="Export format (canvas or svg)")
    p_canvas.add_argument("--output", "-o", default="", help="Output filepath")
    
    # parity
    p_parity = subparsers.add_parser("parity", help="Verify lossless multi-modal synchronization across visual, audio, and text")
    p_parity.add_argument("input", nargs="?", default="", help="Raw text or path to file (defaults to benchmark sample)")
    p_parity.add_argument("--title", "-t", default="", help="Specification title")
    p_parity.add_argument("--lang", "-l", default="en", choices=["en", "fr"], help="Audio language ('en' or 'fr')")
    p_parity.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    
    # companion
    p_comp = subparsers.add_parser("companion", help="Launch desktop menubar companion floating HUD or background daemon")
    p_comp.add_argument("--popup", "-p", action="store_true", help="Launch floating HUD window immediately (default)")
    p_comp.add_argument("--daemon", "-d", action="store_true", help="Run background hotkey and clipboard listener daemon")
    p_comp.add_argument("--compile", "-c", nargs="?", default="", help="Compile input directly")
    
    # dictation / voice-stream
    p_stream = subparsers.add_parser("dictation", help="Stream voice dictation in real time into Obsidian Canvas (.canvas) and SVG")
    p_stream.add_argument("input", nargs="?", default="", help="Input text, audio transcript, or file path")
    p_stream.add_argument("--title", "-t", default="Voice Dictation Session", help="Session title")
    p_stream.add_argument("--canvas", "-c", default="", help="Output .canvas file path")
    p_stream.add_argument("--svg", "-s", default="", help="Output vector .svg file path")
    p_stream.add_argument("--export", "-e", default="", help="Base filepath prefix to export .canvas, .svg, and .md")
    
    # cluster
    p_cluster = subparsers.add_parser("cluster", help="Cluster spatial nodes into constellation groups and discover cross-links")
    p_cluster.add_argument("input", nargs="?", default="", help="Input .canvas file, markdown file, or text list (defaults to sample nodes)")
    p_cluster.add_argument("--threshold", "-t", type=float, default=0.15, help="Similarity threshold (default: 0.15)")
    p_cluster.add_argument("--output", "-o", default="", help="Output clustered Obsidian Canvas (.canvas) filepath")
    p_cluster.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    
    # debate
    p_debate = subparsers.add_parser("debate", help="Autonomous Socratic debate and adversarial thesis stress-testing simulator")
    p_debate.add_argument("input", nargs="?", default="", help="Input text, proposal markdown file, or raw claim")
    p_debate.add_argument("--topic", "-t", default="", help="Explicit topic title for the debate")
    p_debate.add_argument("--format", "-f", choices=["markdown", "html", "canvas", "json"], default="markdown", help="Output format (default: markdown)")
    p_debate.add_argument("--output", "-o", default="", help="Output filepath")
    
    # sync
    p_sync = subparsers.add_parser("sync", help="Multi-vault spatial bi-directional synchronizer and topology resolver")
    p_sync.add_argument("vaults", nargs="*", help="Paths to vault root directories")
    p_sync.add_argument("--canvas", "-c", default="", help="Output filepath for consolidated federation .canvas")
    p_sync.add_argument("--json", "-j", action="store_true", help="Output raw JSON topology telemetry")
    
    # decompile
    p_dec = subparsers.add_parser("decompile", help="Decompile linear slide decks into 2D spatial canvas topologies")
    p_dec.add_argument("input", nargs="?", default="", help="Input slide deck markdown, HTML, or transcript")
    p_dec.add_argument("--title", "-t", default="", help="Presentation title")
    p_dec.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_dec.add_argument("--svg", "-s", default="", help="Output vector .svg filepath")
    p_dec.add_argument("--markdown", "-m", default="", help="Output markdown summary filepath")
    p_dec.add_argument("--json", "-j", action="store_true", help="Output raw JSON topology")
    
    # geomap
    p_geomap = subparsers.add_parser("geomap", help="Project geospatial features into multi-projection SVG and Obsidian Canvas")
    p_geomap.add_argument("input", nargs="?", default="", help="GeoJSON file, coordinate list, or geographic note markdown")
    p_geomap.add_argument("--projection", "-p", choices=["winkel", "mercator", "equirectangular", "orthographic"], default="winkel", help="Map projection (default: winkel)")
    p_geomap.add_argument("--title", "-t", default="", help="Map title")
    p_geomap.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_geomap.add_argument("--svg", "-s", default="", help="Output vector .svg filepath")
    p_geomap.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    
    # cards
    p_cards = subparsers.add_parser("cards", help="Multi-modal audio-spatial flashcards and rapid retrieval engine")
    p_cards.add_argument("input", nargs="?", default="", help="Input markdown note, Q&A list, or vocabulary file")
    p_cards.add_argument("--title", "-t", default="", help="Flashcard deck title")
    p_cards.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_cards.add_argument("--html", default="", help="Output interactive HTML session filepath")
    p_cards.add_argument("--json", "-j", action="store_true", help="Output raw JSON cards")
    
    # storyboard
    p_story = subparsers.add_parser("storyboard", help="Autonomous multi-modal spatial audio-visual storyboarder")
    p_story.add_argument("input", nargs="?", default="", help="Input narrative script, pitch markdown, or text file")
    p_story.add_argument("--title", "-t", default="", help="Storyboard title")
    p_story.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_story.add_argument("--svg", "-s", default="", help="Output vector .svg animatic strip filepath")
    p_story.add_argument("--json", "-j", action="store_true", help="Output raw JSON storyboard telemetry")
    
    # diff
    p_diff = subparsers.add_parser("diff", help="Spatial cognitive architecture graph differential and version divergence engine")
    p_diff.add_argument("canvas_a", help="Base Obsidian .canvas file (Branch A / Snapshot 1)")
    p_diff.add_argument("canvas_b", help="Target Obsidian .canvas file (Branch B / Snapshot 2)")
    p_diff.add_argument("--title", "-t", default="", help="Title for the diff report")
    p_diff.add_argument("--canvas", "-c", default="", help="Output differential Obsidian .canvas filepath")
    p_diff.add_argument("--svg", "-s", default="", help="Output vector SVG differential dashboard filepath")
    p_diff.add_argument("--json", "-j", action="store_true", help="Output raw JSON diff telemetry")
    
    # audit
    p_audit = subparsers.add_parser("audit", help="Autonomous cognitive metacognition and synthesis audit suite")
    p_audit.add_argument("input", nargs="?", default="", help="Input text, markdown note, or document file")
    p_audit.add_argument("--title", "-t", default="", help="Audit report title")
    p_audit.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas scorecard filepath")
    p_audit.add_argument("--svg", "-s", default="", help="Output vector SVG dashboard filepath")
    p_audit.add_argument("--json", "-j", action="store_true", help="Output raw JSON audit telemetry")
    
    # buffer
    p_buf = subparsers.add_parser("buffer", help="Autonomous cognitive spatial working memory buffer monitor")
    p_buf.add_argument("input", nargs="?", default="", help="Input draft text, transcription, or note file")
    p_buf.add_argument("--minutes", "-m", type=float, default=15.0, help="Total active session minutes")
    p_buf.add_argument("--uninterrupted", "-u", type=float, default=15.0, help="Continuous uninterrupted minutes")
    p_buf.add_argument("--title", "-t", default="", help="Memory buffer HUD title")
    p_buf.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_buf.add_argument("--svg", "-s", default="", help="Output vector SVG HUD filepath")
    p_buf.add_argument("--json", "-j", action="store_true", help="Output raw JSON buffer telemetry")
    
    # dataset
    p_data = subparsers.add_parser("dataset", help="Autonomous spatial cognitive model fine-tuning dataset synthesizer")
    p_data.add_argument("input", nargs="?", default="", help="Input text note, markdown file, or directory")
    p_data.add_argument("--format", "-f", choices=["alpaca", "sharegpt", "openai"], default="alpaca", help="Dataset format (default: alpaca)")
    p_data.add_argument("--output", "-o", default="", help="Output JSONL filepath")
    p_data.add_argument("--title", "-t", default="", help="Document title for single input")
    p_data.add_argument("--validate", "-v", action="store_true", help="Validate and report dataset quality score")
    p_data.add_argument("--json", "-j", action="store_true", help="Output raw JSON preview")
    
    # palace
    p_palace = subparsers.add_parser("palace", help="Autonomous cognitive spatial mind palace virtual tour and spatial audio navigator")
    p_palace.add_argument("input", nargs="?", default="", help="Input markdown note, topic outline, or text file")
    p_palace.add_argument("--title", "-t", default="", help="Mind Palace title")
    p_palace.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_palace.add_argument("--svg", "-s", default="", help="Output vector SVG blueprint floorplan filepath")
    p_palace.add_argument("--json", "-j", action="store_true", help="Output raw JSON palace telemetry")
    
    # code-arch
    p_code = subparsers.add_parser("code-arch", help="Autonomous spatial multi-modal code architecture and dependency graph decompiler")
    p_code.add_argument("target", nargs="?", default=".", help="Target Python source file or directory (default: current dir)")
    p_code.add_argument("--title", "-t", default="", help="Code architecture title")
    p_code.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_code.add_argument("--svg", "-s", default="", help="Output vector SVG circuit filepath")
    p_code.add_argument("--json", "-j", action="store_true", help="Output raw JSON AST telemetry")

    # vault-search
    p_vsearch = subparsers.add_parser("vault-search", help="Autonomous cognitive multi-vault semantic vector search and spatial similarity mesh")
    p_vsearch.add_argument("query", nargs="?", default="", help="Search query string or conceptual topic")
    p_vsearch.add_argument("--vaults", "-v", nargs="+", required=True, help="One or more vaults in format name:path (e.g. VaultA:/path/to/vault)")
    p_vsearch.add_argument("--top-k", "-k", type=int, default=8, help="Number of top results to return (default: 8)")
    p_vsearch.add_argument("--min-sim", type=float, default=0.02, help="Minimum cosine similarity threshold (default: 0.02)")
    p_vsearch.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_vsearch.add_argument("--svg", "-s", default="", help="Output vector SVG constellation filepath")
    p_vsearch.add_argument("--json", "-j", action="store_true", help="Output raw JSON search results")

    # saccade-opt
    p_saccade = subparsers.add_parser("saccade-opt", help="Autonomous cognitive spatial working memory saccade and visual glance path optimizer")
    p_saccade.add_argument("canvas", help="Target Obsidian .canvas filepath to evaluate and optimize")
    p_saccade.add_argument("--cols", type=int, default=3, help="Grid columns for serpentine repack (default: 3)")
    p_saccade.add_argument("--gutter-x", type=int, default=60, help="Horizontal gutter spacing in px (default: 60)")
    p_saccade.add_argument("--gutter-y", type=int, default=80, help="Vertical gutter spacing in px (default: 80)")
    p_saccade.add_argument("--output-canvas", "-c", default="", help="Output optimized Obsidian .canvas filepath")
    p_saccade.add_argument("--svg", "-s", default="", help="Output ocular scanpath SVG filepath")
    p_saccade.add_argument("--json", "-j", action="store_true", help="Output raw JSON saccadic metrics")

    # glare-opt
    p_glare = subparsers.add_parser("glare-opt", help="Autonomous cognitive visual attention heatmap and dyslexia glare optimizer")
    p_glare.add_argument("canvas", help="Target Obsidian .canvas filepath to evaluate for optical glare and crowding")
    p_glare.add_argument("--palette", "-p", choices=["warm_paper", "soft_slate", "solarized_dark"], default="soft_slate", help="Target dyslexia-friendly palette (default: soft_slate)")
    p_glare.add_argument("--output-canvas", "-c", default="", help="Output optimized Obsidian .canvas filepath")
    p_glare.add_argument("--svg", "-s", default="", help="Output visual attention heatmap SVG filepath")
    p_glare.add_argument("--json", "-j", action="store_true", help="Output raw JSON optical audit telemetry")

    # audio-beacon
    p_beacon = subparsers.add_parser("audio-beacon", help="Autonomous cognitive spatial audio landmark and acoustic beacon anchoring")
    p_beacon.add_argument("canvas", help="Target Obsidian .canvas filepath to extract beacons and synthesize soundscape")
    p_beacon.add_argument("--duration", "-d", type=float, default=4.0, help="Audio duration in seconds (default: 4.0)")
    p_beacon.add_argument("--max-beacons", "-m", type=int, default=5, help="Maximum number of acoustic beacons (default: 5)")
    p_beacon.add_argument("--output-wav", "-w", default="", help="Output binaural 16-bit WAV filepath")
    p_beacon.add_argument("--svg", "-s", default="", help="Output soundstage vector SVG filepath")
    p_beacon.add_argument("--json", "-j", action="store_true", help="Output raw JSON beacon telemetry")

    # dialectic
    p_dialectic = subparsers.add_parser("dialectic", help="Autonomous cognitive multi-perspective thesis dialectic matrix and consensus engine")
    p_dialectic.add_argument("--viewpoints", "-v", nargs="+", required=True, help="Two or more viewpoints in format 'Name:Text or File' (e.g. Eng:eng.md Product:prod.md)")
    p_dialectic.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_dialectic.add_argument("--svg", "-s", default="", help="Output vector SVG dialectic matrix filepath")
    p_dialectic.add_argument("--json", "-j", action="store_true", help="Output raw JSON consensus telemetry")

    # typo-balance
    p_typo = subparsers.add_parser("typo-balance", help="Autonomous cognitive visual typography kerning and lexical anchor balancer")
    p_typo.add_argument("input", help="Target markdown file or Obsidian .canvas filepath")
    p_typo.add_argument("--mode", "-m", choices=["bionic_anchor", "syllable_dot", "hybrid_dx"], default="bionic_anchor", help="Balancing mode (default: bionic_anchor)")
    p_typo.add_argument("--output", "-o", default="", help="Output balanced text/canvas filepath")
    p_typo.add_argument("--svg", "-s", default="", help="Output comparative typography SVG filepath")
    p_typo.add_argument("--json", "-j", action="store_true", help="Output raw JSON typography audit telemetry")

    # narrative-branch
    p_narrative = subparsers.add_parser("narrative-branch", help="Autonomous cognitive non-linear narrative branching simulator and plot mesh")
    p_narrative.add_argument("input", nargs="?", help="Target markdown storyline file or structured text")
    p_narrative.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_narrative.add_argument("--svg", "-s", default="", help="Output 2D narrative timeline SVG filepath")
    p_narrative.add_argument("--json", "-j", action="store_true", help="Output raw JSON narrative audit telemetry")

    # semantic-zoom
    p_zoom = subparsers.add_parser("semantic-zoom", help="Autonomous cognitive multi-scale hierarchical zoom and semantic chunking engine")
    p_zoom.add_argument("input", nargs="?", help="Target text file or Obsidian .canvas file to decompose")
    p_zoom.add_argument("--lod", "-l", type=int, choices=[0, 1, 2], default=1, help="Target Level of Detail: 0 (Macro), 1 (Meso), 2 (Micro)")
    p_zoom.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_zoom.add_argument("--svg", "-s", default="", help="Output multi-scale semantic zoom SVG filepath")
    p_zoom.add_argument("--json", "-j", action="store_true", help="Output raw JSON semantic zoom telemetry")

    # rhythm-pacer
    p_rhythm = subparsers.add_parser("rhythm-pacer", help="Autonomous cognitive spatial working memory saccadic pacing and rhythm metronome")
    p_rhythm.add_argument("input", nargs="?", help="Target text to pace")
    p_rhythm.add_argument("--wpm", "-w", type=int, default=160, help="Target WPM (default: 160)")
    p_rhythm.add_argument("--chunk", "-k", type=int, default=2, help="Words per fixation beat (default: 2)")
    p_rhythm.add_argument("--output-wav", "-a", default="", help="Output acoustic metronome WAV filepath")
    p_rhythm.add_argument("--svg", "-s", default="", help="Output visual metronome SVG filepath")
    p_rhythm.add_argument("--json", "-j", action="store_true", help="Output raw JSON rhythm telemetry")

    # triangulate
    p_triangulate = subparsers.add_parser("triangulate", help="Autonomous cognitive multimodal knowledge synthesis and triangulation radar")
    p_triangulate.add_argument("input", nargs="?", help="Target markdown claims file or structured text")
    p_triangulate.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_triangulate.add_argument("--svg", "-s", default="", help="Output multimodal synthesis radar SVG filepath")
    p_triangulate.add_argument("--json", "-j", action="store_true", help="Output raw JSON triangulation telemetry")

    # tradeoff
    p_tradeoff = subparsers.add_parser("tradeoff", help="Autonomous cognitive multi-perspective architectural trade-off radar and Pareto frontier")
    p_tradeoff.add_argument("input", nargs="?", help="Target JSON file or structured candidates data")
    p_tradeoff.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_tradeoff.add_argument("--svg", "-s", default="", help="Output architectural trade-off radar SVG filepath")
    p_tradeoff.add_argument("--json", "-j", action="store_true", help="Output raw JSON Pareto analysis telemetry")
    p_tradeoff.add_argument("--demo", action="store_true", help="Run with demonstration architecture candidates")

    # compress
    p_compress = subparsers.add_parser("compress", help="Autonomous cognitive spatial working memory anchor stacking and chunk compression")
    p_compress.add_argument("input", nargs="?", help="Target markdown outline or structured notes")
    p_compress.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_compress.add_argument("--svg", "-s", default="", help="Output working memory buffer telemetry SVG filepath")
    p_compress.add_argument("--slots", type=int, default=4, help="Maximum working memory active slot limit (default: 4)")
    p_compress.add_argument("--json", "-j", action="store_true", help="Output raw JSON chunk compression telemetry")

    # morph
    p_morph = subparsers.add_parser("morph", help="Autonomous cognitive spatial schema morphing and cross-domain associative bridge weaver")
    p_morph.add_argument("concept", nargs="?", default="", help="Target concept name or architecture dynamic")
    p_morph.add_argument("--role", "-r", default="buffer", choices=["buffer", "governor", "failsafe", "distributor", "filter", "resonator"], help="System archetype role (default: buffer)")
    p_morph.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_morph.add_argument("--svg", "-s", default="", help="Output cross-domain schema isomorphism SVG filepath")
    p_morph.add_argument("--json", "-j", action="store_true", help="Output raw JSON schema morphing telemetry")

    # decision
    p_decision = subparsers.add_parser("decision", help="Autonomous cognitive multi-perspective decision matrix and opportunity cost evaluator")
    p_decision.add_argument("input", nargs="?", default="", help="Target JSON options file or structured decisions text")
    p_decision.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_decision.add_argument("--svg", "-s", default="", help="Output 2D decision quadrant SVG filepath")
    p_decision.add_argument("--json", "-j", action="store_true", help="Output raw JSON decision matrix telemetry")
    p_decision.add_argument("--demo", action="store_true", help="Run with demonstration strategic software initiatives")

    # shed
    p_shed = subparsers.add_parser("shed", help="Autonomous cognitive dynamic working memory stress-tester and load shedder")
    p_shed.add_argument("input", nargs="?", default="", help="Target markdown outline or structured notes")
    p_shed.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_shed.add_argument("--svg", "-s", default="", help="Output cognitive load stress gauge SVG filepath")
    p_shed.add_argument("--target-cdi", type=float, default=0.55, help="Target Cognitive Degradation Index threshold (default: 0.55)")
    p_shed.add_argument("--json", "-j", action="store_true", help="Output raw JSON load shedding telemetry")
    
    # resilience / break
    p_resilience = subparsers.add_parser("resilience", aliases=["break", "fatigue"], help="Autonomous cognitive spatial dynamic micro-break and fatigue resiliency harness")
    p_resilience.add_argument("--minutes", "-m", type=float, default=25.0, help="Session duration in minutes (default: 25.0)")
    p_resilience.add_argument("--fixations", "-k", type=int, default=60, help="Simulated or tracked fixation sample count (default: 60)")
    p_resilience.add_argument("--regression-rate", "-r", type=float, default=0.20, help="Saccadic regression rate 0.0 to 1.0 (default: 0.20)")
    p_resilience.add_argument("--mean-dwell", "-d", type=float, default=260.0, help="Mean fixation dwell time in ms (default: 260.0)")
    p_resilience.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_resilience.add_argument("--svg", "-s", default="", help="Output breathing cadence SVG visualizer filepath")
    p_resilience.add_argument("--json", "-j", action="store_true", help="Output raw JSON fatigue telemetry")
    
    args = parser.parse_args()
    
    if args.command == "dump":
        cmd_dump(args)
    elif args.command == "read":
        cmd_read(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "tui":
        import scripts.dx_tui as tui_mod
        tui_mod.main_menu()
    elif args.command == "stamina":
        import scripts.cognitive_fatigue as cf
        report = cf.calculate_cognitive_stamina(minutes_active=args.minutes, words_drafted=args.words)
        cf.print_stamina_report(report)
    elif args.command == "reset":
        import scripts.cognitive_fatigue as cf
        cf.run_terminal_box_breathing(cycles=args.cycles)
    elif args.command == "obsidian":
        import scripts.vault_exporter as ve
        text = read_input(args.input)
        res = ve.format_obsidian_markdown(text, title=args.title, tags=args.tags, vault=args.vault)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(res["markdown"])
            print(f"[DxSkills] Exported Obsidian note: {args.output}")
        else:
            print("\n=== [DxSkills: Obsidian Markdown Note] ===")
            print(res["markdown"])
        print(f"\n[Obsidian URI]: {res['obsidian_uri']}")
    elif args.command == "notion":
        import scripts.vault_exporter as ve
        text = read_input(args.input)
        payload = ve.format_notion_payload(text, title=args.title, database_id=args.database)
        if args.webhook:
            status, resp = ve.dispatch_notion_webhook(payload, args.webhook)
            print(f"[DxSkills] Dispatched to Notion webhook (Status {status}): {resp[:120]}")
        elif args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            print(f"[DxSkills] Exported Notion JSON payload: {args.output}")
        else:
            print("\n=== [DxSkills: Notion Page Payload] ===")
            print(json.dumps(payload, indent=2))
    elif args.command == "audio":
        import scripts.audio_digest as ad
        text = read_input(args.input)
        script = ad.generate_audio_digest_script(text, title=args.title, lang=args.lang)
        if args.output:
            print(f"[DxSkills] Synthesizing audio to: {args.output}...")
            ok = ad.synthesize_audio_file(script, args.output, lang=args.lang)
            if ok:
                print(f"[DxSkills] Successfully generated audio file: {args.output}")
            else:
                print("[DxSkills] Audio synthesis failed or unsupported on this platform.")
        else:
            print("\n=== [DxSkills: Spoken Audio Digest Script] ===")
            print(script)
    elif args.command == "canvas":
        import scripts.canvas_exporter as ce
        text = read_input(args.input)
        if args.format == "svg":
            graph = ce.parse_markdown_to_spatial_graph(text, title=args.title)
            svg_content = ce.generate_svg_canvas(graph)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(svg_content)
                print(f"[DxSkills] Exported Canvas SVG: {args.output}")
            else:
                print(svg_content)
        else:
            canvas_json = ce.generate_obsidian_canvas(text, title=args.title)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(canvas_json)
                print(f"[DxSkills] Exported Obsidian Canvas (.canvas): {args.output}")
            else:
                print("\n=== [DxSkills: Obsidian Canvas JSON] ===")
                print(canvas_json)
    elif args.command == "parity":
        import scripts.multimodal_parity as mp
        text = read_input(args.input) if args.input else """# Example Strategic Deliverable
> **BLUF:** Deploying low-latency cognitive offload layer to eliminate phonological friction.

## Core Spatial Architecture
- High-contrast visual grid with 3:1 spatial margin.
- Zero linear paragraphs over 3 sentences.

## Execution Milestones
- [ ] 1. Ship Manifest V3 browser extension and test suite.
- [ ] 2. Benchmark multi-modal parity across 10 sample corpora.
- [ ] 3. Verify zero em dash compliance across export pipelines.
"""
        res = mp.validate_multimodal_parity(text, title=args.title or None, lang=args.lang)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(mp.format_terminal_parity_report(res))
    elif args.command == "companion":
        import scripts.desktop_companion as dc
        companion = dc.DesktopCompanion()
        if args.compile:
            res = companion.compile_text(args.compile)
            print(res["markdown"])
        elif args.daemon:
            companion.run_daemon_loop()
        else:
            companion.launch_floating_hud()
    elif args.command == "dictation":
        import scripts.voice_streamer as vs
        text = read_input(args.input) if args.input else "The primary objective is to launch the voice streaming canvas engine. First, decouple audio chunk queues. Second, verify live Obsidian Canvas JSON updates. Third, ship the release to production."
        streamer = vs.LiveCanvasStreamer(session_title=args.title)
        chunks = [s.strip() + "." for s in text.split(".") if s.strip()]
        print(f"\n=== [DxSkills: Live Voice Dictation & Canvas Streamer] ===")
        for idx, chunk in enumerate(chunks, 1):
            status = streamer.process_chunk(chunk)
            print(f" [Stream Chunk {idx}] Nodes: {status['nodes_count']} | Edges: {status['edges_count']} | BLUF: {status['bluf'][:40]}...")
        
        if args.export:
            files = streamer.export_session(output_prefix=args.export)
            print(f"\n[DxSkills] Session exported:")
            for k, p in files.items():
                print(f"  - {k}: {p}")
        elif args.canvas:
            with open(args.canvas, "w", encoding="utf-8") as f:
                f.write(streamer.get_canvas_json())
            print(f"\n[DxSkills] Saved Obsidian Canvas: {args.canvas}")
        elif args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(streamer.get_canvas_svg())
            print(f"\n[DxSkills] Saved Vector SVG Canvas: {args.svg}")
        else:
            print("\n--- Finalized D-Mode Markdown Summary ---")
            print(streamer.get_markdown_summary())
    elif args.command == "cluster":
        import scripts.spatial_cluster as sc
        raw_nodes = []
        if args.input and os.path.isfile(args.input):
            if args.input.endswith(".canvas"):
                with open(args.input, "r", encoding="utf-8") as f:
                    c_data = json.load(f)
                    raw_nodes = c_data.get("nodes", [])
            else:
                with open(args.input, "r", encoding="utf-8") as f:
                    lines = [l.strip() for l in f.readlines() if l.strip()]
                    for idx, line in enumerate(lines, 1):
                        raw_nodes.append({"id": f"node-{idx}", "text": line})
        elif args.input:
            lines = [l.strip() for l in args.input.splitlines() if l.strip()]
            for idx, line in enumerate(lines, 1):
                raw_nodes.append({"id": f"node-{idx}", "text": line})
        else:
            raw_nodes = [
                {"id": "node-1", "text": "Deploying Kubernetes cluster with worker replicas and load balancing."},
                {"id": "node-2", "text": "Venture pitch deck financial projections and SaaS recurring revenue."},
                {"id": "node-3", "text": "Container orchestration, Docker worker pods, and cluster autoscaling."},
                {"id": "node-4", "text": "Customer acquisition cost, sales pipeline, and seed round pitch."},
                {"id": "node-5", "text": "Database indexing, query optimization, and connection pooling."}
            ]

        clusterer = sc.SpatialGraphClusterer(similarity_threshold=args.threshold)
        res = clusterer.generate_clustered_canvas(raw_nodes)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(res["canvas_json"])
            print(f"\n[DxSkills] Exported clustered Canvas to: {args.output}")
        elif args.json:
            print(json.dumps({
                "clusters_count": res["clusters_count"],
                "cross_links_count": res["cross_links_count"],
                "clusters": res["clusters"],
                "cross_links": res["cross_links"]
            }, indent=2))
        else:
            print(sc.format_cluster_terminal_report(res))
    elif args.command == "debate":
        import scripts.socratic_debate as sd
        text = read_input(args.input) if args.input else (
            "Our spatial canvas architecture effortlessly eliminates all cognitive friction for non-linear thinkers. "
            "Because users navigate ideas spatially, traditional linear hierarchies will become completely obsolete. "
            "The engine automatically syncs high-dimensional vector graphs without any configuration overhead."
        )
        debate_data, formatted = sd.run_socratic_debate(
            text,
            topic=args.topic or None,
            output_format=args.format,
            output_file=args.output or None
        )
        if not args.output:
            print(formatted)
        else:
            print(f"\n[DxSkills] Debate output written to: {args.output} (Score: {debate_data['thesis_readiness_score']}/100)")
    elif args.command == "sync":
        import scripts.vault_sync as vs
        vault_paths = args.vaults if args.vaults else [os.getcwd()]
        topology, report = vs.run_vault_sync(vault_paths, output_canvas=args.canvas or None)
        if args.json:
            print(json.dumps(topology, indent=2))
        else:
            print(report)
        if args.canvas:
            print(f"\n[DxSkills] Consolidated federation canvas written to: {args.canvas}")
    elif args.command == "decompile":
        import scripts.deck_decompiler as dd
        text = read_input(args.input) if args.input else (
            "# Slide 1: Mission Overview\n"
            "- Goal: Decouple spatial thinking from rigid linear hierarchies.\n"
            "- Audience: Non-linear and dyslexic spatial architectures.\n\n"
            "---\n\n"
            "# Slide 2: Core System Architecture\n"
            "- Vector embedding cluster engine with Szymkiewicz-Simpson overlap.\n"
            "- Bi-directional multi-vault synchronizer with real-time file watcher.\n\n"
            "---\n\n"
            "# Slide 3: Deep Dive: Cognitive Load Telemetry\n"
            "- Empirical evaluation across 10 diverse corpus domains.\n"
            "- Memory buffer stamina tracking and 60-second spatial reset guide.\n\n"
            "---\n\n"
            "# Slide 4: Strategic Deployment Roadmap\n"
            "- Phase 1: Deploy standalone local CLI and Obsidian canvas exporter.\n"
            "- Phase 2: Launch progressive web app with offline service worker."
        )
        slides, canvas_data, md_summary = dd.decompile_deck(
            text,
            deck_title=args.title or None,
            output_canvas=args.canvas or None,
            output_svg=args.svg or None,
            output_markdown=args.markdown or None
        )
        if args.json:
            print(json.dumps({"slides_count": len(slides), "canvas": canvas_data}, indent=2))
        elif not (args.canvas or args.svg or args.markdown):
            print(md_summary)
        else:
            print(f"\n[DxSkills] Decompiled {len(slides)} slides into spatial architecture.")
            if args.canvas:
                print(f"  - Canvas: {args.canvas}")
            if args.svg:
                print(f"  - SVG: {args.svg}")
            if args.markdown:
                print(f"  - Markdown: {args.markdown}")
    elif args.command == "geomap":
        import scripts.geospatial_map as gm
        text = read_input(args.input) if args.input else (
            "# Global Academic and Spatial Research Nodes\n"
            "- Strasbourg: European space research and ISU headquarters\n"
            "- Austin: Texas State University geography campus\n"
            "- Madison: UW-Madison GISPP cartography laboratory\n"
            "- Paris: French research archives and national library\n"
            "- Riyadh: Saudi Executive Space Course\n"
        )
        parsed, canvas_data, svg_code = gm.run_geospatial_mapping(
            text,
            projection=args.projection,
            title=args.title or None,
            output_canvas=args.canvas or None,
            output_svg=args.svg or None
        )
        if args.json:
            print(json.dumps({
                "projection": args.projection,
                "points_count": len(parsed.get("points", [])),
                "points": parsed.get("points", []),
                "canvas": canvas_data
            }, indent=2))
        elif not (args.canvas or args.svg):
            print(svg_code)
        else:
            print(f"\n[DxSkills] Projected {len(parsed['points'])} geospatial landmarks using {args.projection.upper()} projection.")
            if args.canvas:
                print(f"  - Canvas: {args.canvas}")
            if args.svg:
                print(f"  - SVG: {args.svg}")
    elif args.command == "cards":
        import scripts.spatial_flashcards as sf
        text = read_input(args.input) if args.input else (
            "M-Reasoning (Material/Spatial) :: 3D spatial reasoning, mechanics, topology, and physical geometry\n"
            "I-Reasoning (Interconnected) :: Discovering non-obvious patterns, analogies, and holistic connections\n"
            "N-Reasoning (Narrative) :: Episodic memory, causal narrative storytelling, and contextual framing\n"
            "D-Reasoning (Dynamic/Predictive) :: Simulation of future systems, anticipating edge cases, and trend forecasting"
        )
        cards, canvas_data, html_code = sf.run_flashcards(
            text,
            title=args.title or None,
            output_canvas=args.canvas or None,
            output_html=args.html or None
        )
        if args.json:
            print(json.dumps({"deck_title": args.title or "Spatial Retrieval Deck", "cards_count": len(cards), "cards": cards}, indent=2))
        elif not (args.canvas or args.html):
            print(f"\n=== [DxSkills: Spatial Flashcard Deck ({len(cards)} Cards)] ===")
            for c in cards:
                print(f"[{c['id']}] {c['front']} ({c['sector']}) -> {c['back']}")
        else:
            print(f"\n[DxSkills] Generated {len(cards)} spatial flashcards.")
            if args.canvas:
                print(f"  - Canvas: {args.canvas}")
            if args.html:
                print(f"  - HTML: {args.html}")
    elif args.command == "storyboard":
        import scripts.spatial_storyboard as ss
        text = read_input(args.input) if args.input else (
            "Establish the friction: Linear text walls overload phonological working memory.\n"
            "Inciting shift: Non-linear thinkers struggle to communicate complex holistic architectures through sequential slides.\n"
            "Core exploration: The DxSkills cognitive engine decouples spatial mental models from linear output streams.\n"
            "Technical deep dive: High-dimensional vector similarity clusters ideas into constellation topologies.\n"
            "Multi-vault bridge: Cross-repository synchronizers identify dangling wikilinks and orphan nodes in real time.\n"
            "Resolution vista: The user presents a hardened spatial canvas that disarms reductionist critics instantly."
        )
        storyboard, canvas_data, svg_code = ss.run_storyboard(
            text,
            title=args.title or None,
            output_canvas=args.canvas or None,
            output_svg=args.svg or None
        )
        if args.json:
            print(json.dumps(storyboard, indent=2))
        elif not (args.canvas or args.svg):
            print(f"\n=== [DxSkills: 3-Act Spatial Storyboard ({storyboard['total_shots']} Shots | {storyboard['total_duration_seconds']}s)] ===")
            for s in storyboard["shots"]:
                print(f"[{s['act']}] Shot {s['shot_index']} ({s['framing']}, {s['duration_seconds']}s): {s['action']}")
        else:
            print(f"\n[DxSkills] Sequenced {storyboard['total_shots']} shots across 3 acts ({storyboard['total_duration_seconds']}s total).")
            if args.canvas:
                print(f"  - Canvas: {args.canvas}")
            if args.svg:
                print(f"  - SVG: {args.svg}")
    elif args.command == "diff":
        import scripts.spatial_diff as sd
        if not os.path.exists(args.canvas_a) or not os.path.exists(args.canvas_b):
            print(f"[DxSkills] Error: Specified canvas paths must exist on disk.")
            sys.exit(1)
        diff_report, merged_canvas, svg_code = sd.run_spatial_diff(
            args.canvas_a,
            args.canvas_b,
            title=args.title or None,
            output_canvas=args.canvas or None,
            output_svg=args.svg or None
        )
        if args.json:
            print(json.dumps(diff_report, indent=2))
        elif not (args.canvas or args.svg):
            s = diff_report["summary"]
            print(f"\n=== [DxSkills: Spatial Graph Differential Report] ===")
            print(f"Topological Stability Index (TSI): {diff_report['topological_stability_index'] * 100:.1f}%")
            print(f"Architectural Drift: {diff_report['graph_drift_percentage']}%")
            print(f"Nodes: +{s['nodes_added']} added, -{s['nodes_removed']} removed, {s['nodes_modified']} modified, {s['nodes_relocated']} relocated")
            print(f"Edges: +{s['edges_added']} new connections, -{s['edges_removed']} severed links, {s['edges_retained']} preserved")
        else:
            print(f"\n[DxSkills] Computed graph differential (Stability: {diff_report['topological_stability_index'] * 100:.1f}%).")
            if args.canvas:
                print(f"  - Differential Canvas: {args.canvas}")
            if args.svg:
                print(f"  - SVG Diff Dashboard: {args.svg}")
    elif args.command == "audit":
        import scripts.metacognition_audit as ma
        text = read_input(args.input) if args.input else (
            "# Strategic Spatial Deliverable\n"
            "> **BLUF:** Decouple phonological working memory from spatial reasoning models.\n\n"
            "## Architectural Vectors\n"
            "- 1. High-contrast spatial canvas topology.\n"
            "- 2. Automated cross-vault synchronization without manual ID linking.\n"
            "- 3. Lossless multi-modal audio-spatial flashcards.\n\n"
            "| Pillar | Latency | Status |\n"
            "| :--- | :--- | :--- |\n"
            "| Canvas | 0ms | Active |\n"
            "| Audio | 12ms | Verified |\n"
        )
        audit_data, canvas_data, svg_code = ma.run_audit(
            text,
            title=args.title or None,
            output_canvas=args.canvas or None,
            output_svg=args.svg or None
        )
        if args.json:
            print(json.dumps(audit_data, indent=2))
        elif not (args.canvas or args.svg):
            m = audit_data["metrics"]
            print(f"\n=== [DxSkills: Metacognitive Synthesis Audit ({m['cognitive_leverage_score']}/100)] ===")
            print(f"Phonological Friction: {m['phonological_friction']}% | Spatial Leverage: {m['spatial_leverage']}%")
            print(f"Working Memory Tax: {m['working_memory_tax']}% | Connectivity: {m['connectivity_score']}%")
            print("\nPrimary Directives:")
            for r in audit_data["recommendations"]:
                print(f"  - {r}")
        else:
            print(f"\n[DxSkills] Completed audit (Cognitive Leverage: {audit_data['metrics']['cognitive_leverage_score']}/100).")
            if args.canvas:
                print(f"  - Scorecard Canvas: {args.canvas}")
            if args.svg:
                print(f"  - SVG Dashboard: {args.svg}")
    elif args.command == "buffer":
        import scripts.memory_buffer as mb
        text = read_input(args.input) if args.input else (
            "# Cognitive Architecture Working Draft\n"
            "> **BLUF:** Eliminating phonological working memory bottleneck through spatial anchors.\n\n"
            "- Spatial Vector 1: High-contrast 2D node map.\n"
            "- Spatial Vector 2: Dynamic buffer load evaluation.\n"
            "- Spatial Vector 3: 4-4-4-4 Box Breathing reset triggers.\n\n"
            "Reviewing technical documentation without visual anchors creates severe phonological loop friction."
        )
        telemetry, canvas_data, svg_code = mb.run_buffer_monitor(
            text,
            session_minutes=args.minutes,
            uninterrupted_minutes=args.uninterrupted,
            title=args.title or None,
            output_canvas=args.canvas or None,
            output_svg=args.svg or None
        )
        if args.json:
            print(json.dumps(telemetry, indent=2))
        elif not (args.canvas or args.svg):
            m = telemetry["metrics"]
            print(f"\n=== [DxSkills: Working Memory Buffer HUD ({m['exhaustion_risk'].upper()} RISK)] ===")
            print(f"Phonological Saturation: {m['phonological_saturation_pct']}% | Visuospatial Utilization: {m['visuospatial_utilization_pct']}%")
            print(f"Channel Asymmetry Index: {m['channel_asymmetry_index']} | Recommended Reset: {m['recommended_reset_seconds']}s")
            print(f"\nAction: {telemetry['action_prompt']}")
        else:
            print(f"\n[DxSkills] Buffer evaluated: {telemetry['metrics']['exhaustion_risk']} Risk ({telemetry['metrics']['phonological_saturation_pct']}% Phono Load).")
            if args.canvas:
                print(f"  - Canvas: {args.canvas}")
            if args.svg:
                print(f"  - SVG HUD: {args.svg}")
    elif args.command == "dataset":
        import scripts.dataset_synthesizer as dsync
        corpus = []
        if args.input:
            if os.path.isdir(args.input):
                for root, _, files in os.walk(args.input):
                    for file in files:
                        if file.endswith((".md", ".txt")):
                            p = os.path.join(root, file)
                            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                                corpus.append((os.path.splitext(file)[0], f.read()))
            elif os.path.isfile(args.input):
                with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
                    corpus.append((args.title or os.path.basename(args.input), f.read()))
            else:
                corpus.append((args.title or "Interactive CLI Sample", args.input))
        else:
            corpus.append((
                "Core Spatial Scaffolding",
                "# Cognitive Spatial Architecture\n"
                "> **BLUF:** Decouple phonological memory from spatial reasoning models.\n\n"
                "- Spatial Vector 1: 2D radial coordinate positioning.\n"
                "- Spatial Vector 2: Multi-vault topology federation without orphan links.\n"
                "- Spatial Vector 3: Working memory dual-channel stamina balance."
            ))
        dataset, meta = dsync.compile_dataset(corpus, output_filepath=args.output or None, fmt=args.format)
        if args.json:
            print(json.dumps({"meta": meta, "sample": dataset[0] if dataset else None}, indent=2))
        elif not args.output:
            print(f"\n=== [DxSkills: Spatial Model Dataset Synthesizer] ===")
            print(f"Compiled {meta['total_pairs']} pairs ({meta['valid_pairs']} valid) in `{meta['format']}` format.")
            print(f"Average Quality Score: {meta['average_quality_score']}/100")
            if dataset:
                print(f"\n--- Preview Sample ---")
                sample = dataset[0]
                if "instruction" in sample:
                    print(f"Instruction: {sample['instruction']}")
                    print(f"Input: {sample['input'][:100]}...")
                elif "conversations" in sample:
                    print(f"Human: {sample['conversations'][1]['value'][:100]}...")
        else:
            print(f"\n[DxSkills] Compiled {meta['total_pairs']} fine-tuning pairs to: {args.output}")
            print(f"  - Format: {meta['format']}")
            print(f"  - Quality Score: {meta['average_quality_score']}/100")
    elif args.command == "palace":
        import scripts.mind_palace as mp_tour
        text = read_input(args.input) if args.input else (
            "# Spatial Memory Architecture\n"
            "- Linear text creates phonological loop bottleneck.\n"
            "- Method-of-loci memory palaces activate hippocampal spatial navigation.\n"
            "- Binaural acoustic orientation reinforces episodic memory recall.\n"
            "- Structured chambers allow non-linear review without cognitive exhaustion."
        )
        palace, canvas_data, svg_code = mp_tour.run_mind_palace(
            text,
            title=args.title or None,
            output_canvas=args.canvas or None,
            output_svg=args.svg or None
        )
        if args.json:
            print(json.dumps(palace, indent=2))
        elif not (args.canvas or args.svg):
            print(f"\n=== [DxSkills: Cognitive Mind Palace ({palace['total_chambers']} Chambers | {palace['total_loci']} Loci)] ===")
            for c in palace["chambers"]:
                print(f"\n[{c['name']}] - {c['theme']}")
                for loc in c["loci"]:
                    sa = loc["spatial_audio"]
                    print(f"  * {loc['fixture']}: {loc['title']} (Azimuth: {sa['azimuth_degrees']} deg, Pan: {sa['stereo_pan']})")
        else:
            print(f"\n[DxSkills] Mind Palace projected: {palace['total_chambers']} Chambers with {palace['total_loci']} Memory Loci.")
            if args.canvas:
                print(f"  - Canvas: {args.canvas}")
            if args.svg:
                print(f"  - Blueprint: {args.svg}")
    elif args.command == "code-arch":
        import scripts.code_decompiler as cdec
        target_path = os.path.abspath(args.target)
        if not os.path.exists(target_path):
            print(f"[DxSkills] Error: Target path not found: {target_path}")
            sys.exit(1)
        decompiled, canvas_data, svg_code = cdec.run_code_decompiler(
            target_path,
            title=args.title or None,
            output_canvas=args.canvas or None,
            output_svg=args.svg or None
        )
        if args.json:
            print(json.dumps(decompiled, indent=2))
        elif not (args.canvas or args.svg):
            print(f"\n=== [DxSkills: Code Architecture Topology ({decompiled['total_modules']} Modules)] ===")
            for mod_name, data in decompiled["modules"].items():
                classes = [c["name"] for c in data.get("classes", [])]
                funcs = [f["name"] for f in data.get("functions", [])]
                print(f"- {mod_name}.py: Classes: {classes or 'None'} | Functions: {funcs or 'None'}")
            if decompiled["circular_cycles"]:
                print(f"\n⚠️ Identified {len(decompiled['circular_cycles'])} Circular Dependency Loops:")
                for c in decompiled["circular_cycles"]:
                    print(f"  * {' -> '.join(c)}")
            else:
                print("\nClean architecture: Zero circular import loops detected.")
        else:
            print(f"\n[DxSkills] Decompiled {decompiled['total_modules']} modules into spatial architecture.")
            if args.canvas:
                print(f"  - Canvas: {args.canvas}")
            if args.svg:
                print(f"  - SVG Circuit: {args.svg}")
    elif args.command == "vault-search":
        import scripts.vault_search as vs
        if not args.query:
            print("[DxSkills] Error: Query string required.")
            sys.exit(1)
        searcher = vs.MultiVaultVectorSearch()
        total_indexed = 0
        for v_spec in args.vaults:
            if ":" in v_spec:
                parts = v_spec.split(":", 1)
                v_name, v_path = parts[0], parts[1]
            else:
                v_name = os.path.basename(os.path.abspath(v_spec))
                v_path = v_spec
            count = searcher.register_vault(v_name, os.path.abspath(v_path))
            total_indexed += count
        searcher.build_index()
        results = searcher.search(args.query, top_k=args.top_k, min_similarity=args.min_sim)
        bridges = searcher.compute_cross_vault_bridges(results)

        if args.json:
            out = {
                "query": args.query,
                "total_docs_indexed": total_indexed,
                "results": [
                    {
                        "doc_id": r.doc_id,
                        "vault_name": r.vault_name,
                        "title": r.title,
                        "similarity": r.similarity,
                        "shared_keywords": r.shared_keywords,
                        "excerpt": r.excerpt
                    } for r in results
                ],
                "bridges": [
                    {
                        "vault_a": b.doc_a_vault,
                        "title_a": b.doc_a_title,
                        "vault_b": b.doc_b_vault,
                        "title_b": b.doc_b_title,
                        "similarity": b.similarity,
                        "shared_keywords": b.shared_keywords
                    } for b in bridges
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            summary = vs.VaultSearchCanvasExporter.export_summary(args.query, results, bridges)
            print("\n" + summary)

        if args.canvas:
            canvas_data = vs.VaultSearchCanvasExporter.export_canvas(args.query, results, bridges)
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Obsidian .canvas constellation exported to: {args.canvas}")

        if args.svg:
            svg_code = vs.VaultSearchCanvasExporter.export_svg(args.query, results)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Vector SVG constellation exported to: {args.svg}")
    elif args.command == "saccade-opt":
        import scripts.saccade_optimizer as so
        canvas_path = os.path.abspath(args.canvas)
        if not os.path.isfile(canvas_path):
            print(f"[DxSkills] Error: Canvas file not found: {canvas_path}")
            sys.exit(1)
        with open(canvas_path, "r", encoding="utf-8") as f:
            canvas_data = json.load(f)

        optimizer = so.SaccadeGlancePathOptimizer()
        optimizer.load_canvas_data(canvas_data)
        scanpath_orig = optimizer.compute_scanpath()
        orig_metrics = optimizer.evaluate_metrics(scanpath_orig)

        opt_nodes = optimizer.optimize_layout(cols=args.cols, gutter_x=args.gutter_x, gutter_y=args.gutter_y)
        opt_scanpath = list(opt_nodes.values())
        opt_metrics = optimizer.evaluate_metrics(opt_scanpath)

        if args.json:
            out = {
                "canvas": canvas_path,
                "original_metrics": orig_metrics.__dict__,
                "optimized_metrics": opt_metrics.__dict__
            }
            print(json.dumps(out, indent=2))
        else:
            summary = so.SaccadeGlancePathOptimizer.export_audit_summary(orig_metrics, opt_metrics)
            print("\n" + summary)

        if args.output_canvas:
            opt_canvas = optimizer.export_canvas(opt_nodes)
            with open(args.output_canvas, "w", encoding="utf-8") as f:
                json.dump(opt_canvas, f, indent=2)
            print(f"\n[DxSkills] Optimized .canvas exported to: {args.output_canvas}")

        if args.svg:
            svg_code = optimizer.export_scanpath_svg(opt_scanpath)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Visual scanpath SVG exported to: {args.svg}")
    elif args.command == "glare-opt":
        import scripts.glare_optimizer as go
        canvas_path = os.path.abspath(args.canvas)
        if not os.path.isfile(canvas_path):
            print(f"[DxSkills] Error: Canvas file not found: {canvas_path}")
            sys.exit(1)
        with open(canvas_path, "r", encoding="utf-8") as f:
            canvas_data = json.load(f)

        optimizer = go.DyslexiaGlareOptimizer()
        optimizer.load_canvas(canvas_data)
        audit = optimizer.audit_optical_comfort()

        if args.json:
            out = {
                "canvas": canvas_path,
                "optical_comfort_score": audit.optical_comfort_score,
                "average_contrast_ratio": audit.average_contrast_ratio,
                "stark_contrast_violations": audit.stark_contrast_violations,
                "low_contrast_violations": audit.low_contrast_violations,
                "high_crowding_nodes": audit.high_crowding_nodes,
                "palette_recommendation": audit.palette_recommendation,
                "nodes": [
                    {
                        "id": p.node_id,
                        "contrast_ratio": p.contrast_ratio,
                        "glare_risk": p.glare_risk,
                        "crowding_factor": p.crowding_factor
                    } for p in audit.node_profiles
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            report = go.DyslexiaGlareOptimizer.export_audit_markdown(audit)
            print("\n" + report)

        if args.output_canvas:
            opt_canvas = optimizer.optimize_canvas(target_palette=args.palette)
            with open(args.output_canvas, "w", encoding="utf-8") as f:
                json.dump(opt_canvas, f, indent=2)
            print(f"\n[DxSkills] Glare-optimized .canvas exported to: {args.output_canvas}")

        if args.svg:
            svg_code = optimizer.export_heatmap_svg(audit)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Visual attention heatmap SVG exported to: {args.svg}")
    elif args.command == "audio-beacon":
        import scripts.acoustic_beacon as ab
        canvas_path = os.path.abspath(args.canvas)
        if not os.path.isfile(canvas_path):
            print(f"[DxSkills] Error: Canvas file not found: {canvas_path}")
            sys.exit(1)
        with open(canvas_path, "r", encoding="utf-8") as f:
            canvas_data = json.load(f)

        engine = ab.AcousticBeaconEngine()
        beacons = engine.extract_beacons_from_canvas(canvas_data, max_beacons=args.max_beacons)

        if args.json:
            out = {
                "canvas": canvas_path,
                "total_beacons": len(beacons),
                "beacons": [
                    {
                        "beacon_id": b.beacon_id,
                        "node_id": b.node_id,
                        "title": b.title,
                        "x": b.x,
                        "y": b.y,
                        "frequency_hz": b.frequency,
                        "tone_label": b.tone_label,
                        "pulse_hz": b.pulse_hz
                    } for b in beacons
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            summary = ab.AcousticBeaconEngine.export_summary(beacons)
            print("\n" + summary)

        if args.output_wav:
            engine.write_wav_file(args.output_wav, duration_sec=args.duration)
            print(f"\n[DxSkills] Synthesized binaural soundscape WAV: {args.output_wav}")

        if args.svg:
            svg_code = engine.export_soundstage_svg()
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] 3D soundstage map SVG exported to: {args.svg}")
    elif args.command == "dialectic":
        import scripts.dialectic_matrix as dm
        engine = dm.DialecticMatrixEngine()
        for vp in args.viewpoints:
            if ":" in vp:
                parts = vp.split(":", 1)
                vp_name, vp_val = parts[0], parts[1]
            else:
                vp_name = f"Perspective {len(engine.perspectives) + 1}"
                vp_val = vp

            if os.path.isfile(vp_val):
                with open(vp_val, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            else:
                content = vp_val
            engine.add_perspective(vp_name, content)

        result = engine.analyze_dialectic()

        if args.json:
            out = {
                "consensus_readiness_index": result.consensus_readiness_index,
                "shared_vocabulary_pct": result.shared_vocabulary_pct,
                "total_false_divergences": result.total_false_divergences,
                "perspectives": [{"name": p.name, "core_values": p.core_values} for p in result.perspectives],
                "tensions": [
                    {
                        "topic": t.topic,
                        "perspective_a": t.perspective_a,
                        "perspective_b": t.perspective_b,
                        "claim_a": t.claim_a,
                        "claim_b": t.claim_b,
                        "is_false_divergence": t.is_false_divergence,
                        "shared_concept": t.shared_concept
                    } for t in result.tensions
                ],
                "syntheses": [
                    {
                        "title": s.title,
                        "description": s.description,
                        "consensus_score": s.consensus_score
                    } for s in result.syntheses
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            summary = dm.DialecticMatrixEngine.export_summary(result)
            print("\n" + summary)

        if args.canvas:
            canvas_data = engine.export_canvas(result)
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Dialectic matrix .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = engine.export_svg(result)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Dialectic matrix SVG diagram exported to: {args.svg}")
    elif args.command == "typo-balance":
        import scripts.typography_balancer as tb
        balancer = tb.VisualTypographyBalancer()

        is_canvas = args.input.endswith(".canvas") and os.path.isfile(args.input)
        if is_canvas:
            with open(args.input, "r", encoding="utf-8") as f:
                canvas_data = json.load(f)
            all_text = " ".join(n.get("text", "") for n in canvas_data.get("nodes", []) if n.get("type") == "text")
            audit = balancer.audit_text(all_text)
            balanced_canvas = balancer.balance_canvas(canvas_data, mode=args.mode)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(balanced_canvas, f, indent=2)
                print(f"\n[DxSkills] Balanced .canvas exported to: {args.output}")
            sample_before = all_text[:200]
            sample_after = balancer.balance_text(sample_before, mode=args.mode)
        else:
            if os.path.isfile(args.input):
                with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
                    raw_text = f.read()
            else:
                raw_text = args.input

            audit = balancer.audit_text(raw_text)
            balanced_text = balancer.balance_text(raw_text, mode=args.mode)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(balanced_text)
                print(f"\n[DxSkills] Balanced text exported to: {args.output}")
            sample_before = raw_text[:200]
            sample_after = balanced_text[:200]

        if args.json:
            out = {
                "total_words": audit.total_words,
                "complex_words_count": audit.complex_words_count,
                "average_word_length": audit.average_word_length,
                "lexical_friction_index": audit.lexical_friction_index,
                "estimated_standard_wpm": audit.estimated_standard_wpm,
                "estimated_anchored_wpm": audit.estimated_anchored_wpm,
                "wpm_boost_pct": audit.wpm_boost_pct
            }
            print(json.dumps(out, indent=2))
        else:
            summary = tb.VisualTypographyBalancer.export_summary(audit, sample_before, sample_after)
            print("\n" + summary)

        if args.svg:
            svg_code = balancer.export_comparison_svg(sample_before, audit)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Typography comparison SVG exported to: {args.svg}")
    elif args.command == "narrative-branch":
        import scripts.narrative_brancher as nb
        sim = nb.NarrativeBranchingSimulator()
        if args.input:
            content = read_input(args.input)
            sim.parse_markdown_storyline(content)
        else:
            default_story = """### Beat: The Signal Intercept
- Character: Cryptographer
- Tension: 30
- Act: Act 1
- Description: Deep-space quantum signal intercepted at relay station.
- Leads To: Decryption Protocol | Condition: If cipher key resolves

### Beat: Decryption Protocol
- Character: AI Architect
- Tension: 55
- Act: Act 2
- Description: AI unravels anomalous coordinate vector pointing to exoplanet.
- Leads To: Hostile Encounter | Condition: If containment breached
- Leads To: First Contact Handshake | Condition: If diplomatic beacon deployed

### Beat: Hostile Encounter
- Character: Commander
- Tension: 90
- Act: Act 3
- Description: Kinetic defense grid activated under swarm pressure.
- Terminal: true

### Beat: First Contact Handshake
- Character: Ambassador
- Tension: 45
- Act: Act 3
- Description: Mutual peaceful synthesis established across species.
- Terminal: true"""
            sim.parse_markdown_storyline(default_story)

        audit = sim.audit_narrative()

        if args.json:
            out = {
                "total_beats": audit.total_beats,
                "total_branches": audit.total_branches,
                "characters_count": audit.characters_count,
                "dangling_threads_count": audit.dangling_threads_count,
                "pacing_bottlenecks_count": audit.pacing_bottlenecks_count,
                "narrative_agency_score": audit.narrative_agency_score,
                "average_tension": audit.average_tension,
                "beats": [
                    {
                        "id": b.id,
                        "title": b.title,
                        "character": b.character,
                        "act": b.act,
                        "tension": b.tension_level,
                        "is_terminal": b.is_terminal
                    } for b in sim.beats.values()
                ],
                "branches": [
                    {
                        "source": br.source_id,
                        "target": br.target_id,
                        "condition": br.condition,
                        "consequence": br.consequence
                    } for br in sim.branches
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            summary = nb.NarrativeBranchingSimulator.export_summary(audit, list(sim.beats.values()))
            print("\n" + summary)

        if args.canvas:
            canvas_data = sim.export_canvas()
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Narrative plot mesh .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = sim.export_svg()
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Narrative timeline SVG exported to: {args.svg}")
    elif args.command == "semantic-zoom":
        import scripts.semantic_zoom as sz
        engine = sz.SemanticZoomEngine()

        is_canvas = args.input and args.input.endswith(".canvas") and os.path.isfile(args.input)
        if is_canvas:
            with open(args.input, "r", encoding="utf-8") as f:
                canvas_data = json.load(f)
            decomposed_canvas = engine.decompose_canvas(canvas_data, max_words=70)
            for n in decomposed_canvas.get("nodes", []):
                if n.get("type") == "text":
                    engine.add_node(n.get("id", "node"), n.get("text", ""), x=n.get("x", 0), y=n.get("y", 0))

            if args.canvas:
                with open(args.canvas, "w", encoding="utf-8") as f:
                    json.dump(decomposed_canvas, f, indent=2)
                print(f"\n[DxSkills] Decomposed semantic .canvas exported to: {args.canvas}")
        else:
            if args.input:
                raw_text = read_input(args.input)
            else:
                raw_text = (
                    "Distributed spatial memory models offload executive working memory onto spatial canvasing. "
                    "Visual nodes eliminate linear phonological decoding fatigue. "
                    "Bi-directional graph topologies provide immediate topological context. "
                    "Satellite detail cards unpack dense technical explanations without breaking focus."
                )

            paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
            for idx, p in enumerate(paragraphs, 1):
                title_match = re.match(r'^(?:#+\s*)?([^\n]+)', p)
                title = title_match.group(1).strip() if title_match else f"Core Concept {idx}"
                engine.add_node(title, p)

            if args.canvas:
                canvas_data = engine.export_canvas_lod(lod_level=args.lod)
                with open(args.canvas, "w", encoding="utf-8") as f:
                    json.dump(canvas_data, f, indent=2)
                print(f"\n[DxSkills] Exported LOD {args.lod} .canvas to: {args.canvas}")

        audit = engine.audit_engine()

        if args.json:
            out = {
                "total_nodes": audit.total_nodes,
                "oversized_monoliths_count": audit.oversized_monoliths_count,
                "lod_levels_supported": audit.lod_levels_supported,
                "average_compression_ratio_lod0": audit.average_compression_ratio_lod0,
                "average_compression_ratio_lod1": audit.average_compression_ratio_lod1,
                "spatial_landmark_stability_index": audit.spatial_landmark_stability_index,
                "nodes": [
                    {
                        "id": n.id,
                        "title": n.title,
                        "macro_summary": n.macro_summary,
                        "meso_bullets": n.meso_bullets,
                        "micro_body": n.micro_body
                    } for n in engine.nodes.values()
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            summary = sz.SemanticZoomEngine.export_summary(audit, list(engine.nodes.values()))
            print("\n" + summary)

        if args.svg:
            svg_code = engine.export_svg(lod_level=args.lod)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Semantic zoom SVG exported to: {args.svg}")
    elif args.command == "rhythm-pacer":
        import scripts.rhythm_pacer as rp
        pacer = rp.SaccadicRhythmPacer()
        if args.input:
            raw_text = read_input(args.input)
        else:
            raw_text = (
                "Spatial cognition and visual memory offload phonological decoding stress. "
                "Rhythmic saccadic pacing stabilizes ocular fixation jumps across sentences, "
                "reducing regression rates and eliminating visual fatigue."
            )

        cadence = pacer.calculate_cadence(raw_text, target_wpm=args.wpm, words_per_fixation=args.chunk)
        audit = pacer.audit_cadence(cadence)
        timeline = pacer.generate_pacing_timeline(raw_text, target_wpm=args.wpm, words_per_fixation=args.chunk)

        if args.json:
            out = {
                "wpm": cadence.wpm,
                "words_per_fixation": cadence.words_per_fixation,
                "fixation_interval_ms": cadence.fixation_interval_ms,
                "beats_per_minute": cadence.beats_per_minute,
                "total_words": cadence.total_words,
                "estimated_duration_sec": cadence.estimated_duration_sec,
                "cadence_profile": audit.cadence_profile,
                "regression_risk_reduction_pct": audit.regression_risk_reduction_pct,
                "fixation_consistency_score": audit.fixation_consistency_score,
                "soundtrack_frequency_hz": audit.soundtrack_frequency_hz,
                "timeline": timeline[:20]
            }
            print(json.dumps(out, indent=2))
        else:
            summary = rp.SaccadicRhythmPacer.export_summary(cadence, audit, timeline)
            print("\n" + summary)

        if args.output_wav:
            pacer.write_audio_metronome(cadence, args.output_wav, frequency_hz=audit.soundtrack_frequency_hz, max_duration_sec=8.0)
            print(f"\n[DxSkills] Synthesized acoustic metronome WAV: {args.output_wav}")

        if args.svg:
            svg_code = pacer.export_svg_pacer(timeline, cadence, audit)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Visual metronome SVG exported to: {args.svg}")
    elif args.command == "triangulate":
        import scripts.knowledge_triangulator as kt
        triangulator = kt.MultimodalKnowledgeTriangulator()
        if args.input:
            content = read_input(args.input)
            triangulator.parse_markdown_evidence(content)
        else:
            sample_doc = """### Claim: Zero-Copy Network Buffers Minimize Latency
- Text: Architecture Specification Section 3.2 | Ref: docs/spec.md | Excerpt: Zero-copy DMA buffers eliminate kernel copies.
- Code: fn send_packet_zerocopy() | Ref: src/net.rs:L140
- Audio: Core Engineering Sync 14:10 | Ref: audio/sync_04.mp3
- Visual: Packet Pipeline Topology | Ref: diagrams/packet_flow.svg

### Claim: Visual Canvases Accelerate Conceptual Reasoning
- Text: Cognitive Research Monograph | Ref: papers/eide2023.pdf | Excerpt: Spatial mapping offloads working memory.
- Code: Canvas Renderer AST | Ref: scripts/canvas_exporter.py:L50
- Visual: 2D Spatial Constellation | Ref: assets/canvas_preview.svg

### Claim: Linear Monolith Outlines Suffer Cognitive Drift
- Text: Working Memory Study | Ref: notes/baddeley.md | Excerpt: Single-track linear processing creates phonological stalls."""
            triangulator.parse_markdown_evidence(sample_doc)

        audit = triangulator.audit_synthesis()

        if args.json:
            out = {
                "total_claims": audit.total_claims,
                "corroborated_claims_count": audit.corroborated_claims_count,
                "uncorroborated_claims_count": audit.uncorroborated_claims_count,
                "overall_synthesis_confidence": audit.overall_synthesis_confidence,
                "modality_distribution": audit.modality_distribution,
                "claims": [
                    {
                        "claim_id": c.claim_id,
                        "statement": c.statement,
                        "confidence_score": c.confidence_score,
                        "is_corroborated": c.is_corroborated,
                        "modalities": list(c.modalities_present),
                        "recommendation": c.recommendation,
                        "sources_count": len(c.sources)
                    } for c in triangulator.claims.values()
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            summary = kt.MultimodalKnowledgeTriangulator.export_summary(audit, list(triangulator.claims.values()))
            print("\n" + summary)

        if args.canvas:
            canvas_data = triangulator.export_canvas()
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Triangulation .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = triangulator.export_svg()
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Synthesis radar SVG exported to: {args.svg}")
    elif args.command == "tradeoff":
        import scripts.tradeoff_radar as tor
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            radar = tor.ArchitecturalTradeoffRadar.from_dict(data)
        else:
            radar = tor.create_sample_tradeoff_radar()

        analysis = radar.evaluate_pareto()

        if args.json:
            out = {
                "candidates_count": len(analysis.candidates),
                "pareto_frontier_count": len(analysis.pareto_frontier_ids),
                "dominated_count": len(analysis.dominated_ids),
                "pareto_frontier_ids": analysis.pareto_frontier_ids,
                "dominated_ids": analysis.dominated_ids,
                "tradeoff_tensions": analysis.tradeoff_tensions,
                "archetype_recommendations": analysis.archetype_recommendations,
                "candidates": [
                    {
                        "id": c.candidate_id,
                        "name": c.name,
                        "scores": c.scores,
                        "is_pareto_optimal": c.is_pareto_optimal,
                        "dominates": c.dominates,
                        "dominated_by": c.dominated_by
                    }
                    for c in analysis.candidates
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + radar.export_summary_markdown())

        if args.canvas:
            canvas_data = radar.export_pareto_canvas()
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Pareto Frontier .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = radar.export_radar_svg()
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Architectural Trade-Off Radar SVG exported to: {args.svg}")
    elif args.command == "compress":
        import scripts.chunk_compressor as cc
        compressor = cc.WorkingMemoryChunkCompressor(max_working_memory_slots=args.slots)
        if args.input:
            content = read_input(args.input)
            compressor.load_markdown_outline(content)
        else:
            sample_outline = """# Distributed Edge Gateway
- Dynamic route dispatch
- Rate-limiting token bucket
- Mutual TLS termination

# In-Memory Cache Mesh
- Consistent hash ring
- LRU eviction policy
- Eviction tombstone replication

# Event Sinks and Storage
- Parquet columnar batcher
- S3 object storage sink
- Audit logging pipeline"""
            compressor.load_markdown_outline(sample_outline)

        audit = compressor.compress_chunks()

        if args.json:
            out = {
                "original_node_count": audit.original_node_count,
                "compressed_anchor_count": audit.compressed_anchor_count,
                "original_slots_used": audit.original_slots_used,
                "compressed_slots_used": audit.compressed_slots_used,
                "slot_reduction_count": audit.slot_reduction_count,
                "slot_reduction_percentage": audit.slot_reduction_percentage,
                "cowan_capacity_respected": audit.cowan_capacity_respected,
                "anchors": [
                    {
                        "id": a.anchor_id,
                        "label": a.label,
                        "summary": a.summary,
                        "child_nodes_count": len(a.child_node_ids),
                        "compression_ratio": a.compression_ratio
                    }
                    for a in audit.anchors
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + compressor.export_summary_markdown(audit))

        if args.canvas:
            canvas_data = compressor.export_compressed_canvas(audit)
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Compressed Anchor .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = compressor.export_svg_telemetry(audit)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Working Memory Telemetry SVG exported to: {args.svg}")
    elif args.command == "morph":
        import scripts.schema_morpher as sm
        morpher = sm.SpatialSchemaMorpher()
        if args.concept:
            schema = morpher.morph_concept(args.concept, role=args.role)
            schemas = [schema]
        else:
            schemas = list(morpher.library.values())

        if args.json:
            out = {
                "schemas_count": len(schemas),
                "schemas": [
                    {
                        "id": s.schema_id,
                        "title": s.title,
                        "primary_role": s.primary_role,
                        "cognitive_takeaway": s.cognitive_takeaway,
                        "domains": {
                            "computational": s.computational.name,
                            "mechanical": s.mechanical.name,
                            "biological": s.biological.name,
                            "spatial": s.spatial.name
                        },
                        "bridges_count": len(s.bridges)
                    }
                    for s in schemas
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + morpher.export_summary_markdown(schemas))

        if args.canvas:
            canvas_data = morpher.export_canvas(schemas)
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Cross-Domain Schema .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = morpher.export_svg_morph(schemas[0])
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Schema Isomorphism SVG exported to: {args.svg}")
    elif args.command == "decision":
        import scripts.decision_matrix as dm
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            matrix = dm.SpatialDecisionMatrix.from_dict(data)
        else:
            matrix = dm.create_sample_decision_matrix()

        audit = matrix.evaluate_matrix()

        if args.json:
            out = {
                "total_options": audit.total_options,
                "q1_count": audit.q1_count,
                "q2_count": audit.q2_count,
                "q3_count": audit.q3_count,
                "q4_count": audit.q4_count,
                "highest_leverage_option": audit.highest_leverage_option.name if audit.highest_leverage_option else None,
                "highest_opportunity_cost_option": audit.highest_opportunity_cost_option.name if audit.highest_opportunity_cost_option else None,
                "action_roadmap": [
                    {
                        "id": o.option_id,
                        "name": o.name,
                        "quadrant": o.quadrant,
                        "leverage_score": o.leverage_score,
                        "compounding_leverage": o.compounding_leverage,
                        "cognitive_flow": o.cognitive_flow,
                        "opportunity_cost_risk": o.opportunity_cost_risk,
                        "reversibility": o.reversibility
                    }
                    for o in audit.action_roadmap
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + matrix.export_summary_markdown(audit))

        if args.canvas:
            canvas_data = matrix.export_canvas(audit)
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Decision Matrix .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = matrix.export_svg_matrix(audit)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Decision Matrix SVG exported to: {args.svg}")
    elif args.command == "shed":
        import scripts.load_shedder as ls
        shedder = ls.WorkingMemoryLoadShedder()
        if args.input:
            content = read_input(args.input)
            shedder.load_from_markdown(content)
        else:
            sample_outline = """# Distributed Storage Engine
- Master coordinator node
  - Heartbeat lease monitor
  - Election timeout listener
  - Cluster metadata cache
    - Cache invalidation hook
    - Cache hit telemetry
    - Serialized TTL eviction
- Write-Ahead Log Partition
  - Segment file rotation
  - Group commit fsync batcher
  - Checkpoint barrier snapshot
    - Snapshot compression worker
    - S3 cold backup replica
- Client Connection Multiplexer
  - TLS handshake terminator
  - Keep-alive ping responder
  - Backpressure request buffer
    - Micro-buffer watermark high
    - Micro-buffer watermark low"""
            shedder.load_from_markdown(sample_outline)

        audit = shedder.execute_load_shedding(target_cdi=args.target_cdi)

        if args.json:
            out = {
                "initial_load_points": audit.initial_telemetry.total_load_points,
                "initial_cdi": audit.initial_telemetry.cognitive_degradation_index,
                "initial_status": audit.initial_telemetry.status,
                "post_shed_load_points": audit.post_shed_telemetry.total_load_points,
                "post_shed_cdi": audit.post_shed_telemetry.cognitive_degradation_index,
                "post_shed_status": audit.post_shed_telemetry.status,
                "load_points_freed": audit.load_points_freed,
                "reduction_percentage": audit.reduction_percentage,
                "pruned_leaves_count": audit.pruned_leaves_count,
                "retained_nodes_count": len(audit.retained_nodes),
                "shed_nodes": [
                    {
                        "label": n.label,
                        "depth": n.depth,
                        "shed_tier": n.shed_tier
                    }
                    for n in audit.shed_nodes
                ]
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + shedder.export_summary_markdown(audit))

        if args.canvas:
            canvas_data = shedder.export_canvas(audit)
            with open(args.canvas, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)
            print(f"\n[DxSkills] Decluttered Cognitive Canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = shedder.export_svg_gauge(audit)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Cognitive Stress Gauge SVG exported to: {args.svg}")
    elif args.command in ["resilience", "break", "fatigue"]:
        import scripts.fatigue_resilience as fr
        harness = fr.FatigueResilienceHarness()
        step_denom = max(1, int(1.0 / max(0.01, args.regression_rate)))
        samples = [
            fr.SaccadeSample(
                timestamp=i * 0.35,
                fixation_duration_ms=args.mean_dwell,
                jump_amplitude_deg=2.5,
                is_regression=(i % step_denom == 0),
            )
            for i in range(args.fixations)
        ]
        telemetry = harness.analyze_saccade_stream(samples, session_duration_min=args.minutes)
        protocol = harness.generate_break_protocol(telemetry)

        if args.json:
            out = {
                "telemetry": telemetry.to_dict(),
                "protocol": protocol.to_dict(),
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + harness.generate_markdown_report(telemetry, protocol))

        if args.canvas:
            harness.export_spatial_canvas(protocol, output_path=args.canvas)
            print(f"\n[DxSkills] Micro-Break .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = harness.export_svg_breathing_visualizer(protocol)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Breathing Visualizer SVG exported to: {args.svg}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
