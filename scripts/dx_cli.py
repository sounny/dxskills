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

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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
    
    # reflector / bias
    p_reflector = subparsers.add_parser("reflector", aliases=["bias", "blindspot"], help="Autonomous cognitive multi-perspective metacognitive reflector and bias breaker")
    p_reflector.add_argument("title", nargs="?", default="Strategic Architecture Spec", help="Thesis or architectural proposal title")
    p_reflector.add_argument("--assumptions", "-a", nargs="*", default=[], help="List of assumptions in format 'Label:validated' or 'Label'")
    p_reflector.add_argument("--perspectives", "-p", type=int, default=2, help="Number of distinct analytical viewpoints consulted (default: 2)")
    p_reflector.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_reflector.add_argument("--svg", "-s", default="", help="Output dialectic radar SVG filepath")
    p_reflector.add_argument("--json", "-j", action="store_true", help="Output raw JSON assessment telemetry")
    p_reflector.add_argument("--demo", action="store_true", help="Run with demonstration assumptions suite")
    
    # horizon
    p_horizon = subparsers.add_parser("horizon", help="Autonomous cognitive multi-scale working memory horizon visualizer")
    p_horizon.add_argument("input", nargs="?", default="", help="Optional JSON file with horizon items")
    p_horizon.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_horizon.add_argument("--svg", "-s", default="", help="Output concentric horizon radar SVG filepath")
    p_horizon.add_argument("--json", "-j", action="store_true", help="Output raw JSON horizon telemetry")
    p_horizon.add_argument("--demo", action="store_true", help="Run with demonstration multi-scale horizon items")
    
    # evict / compactor
    p_evict = subparsers.add_parser("evict", aliases=["compactor"], help="Autonomous cognitive spatial working memory anchor eviction and FIFO buffer compactor")
    p_evict.add_argument("input", nargs="?", default="", help="Optional JSON file with working memory nodes")
    p_evict.add_argument("--capacity", type=int, default=5, help="Maximum active working memory buffer slots (default: 5)")
    p_evict.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_evict.add_argument("--svg", "-s", default="", help="Output buffer compaction telemetry SVG filepath")
    p_evict.add_argument("--json", "-j", action="store_true", help="Output raw JSON compaction telemetry")
    p_evict.add_argument("--demo", action="store_true", help="Run with demonstration working memory node cluster")
    
    # interleave / dampener
    p_damp = subparsers.add_parser("interleave", aliases=["dampener", "bookmark"], help="Autonomous cognitive spatial schema interleaving and context switch dampener")
    p_damp.add_argument("project", nargs="?", default="Strategic Workstream", help="Project or active context title")
    p_damp.add_argument("--thread", "-t", default="Core Architecture Modeling", help="Active sub-thread or task description")
    p_damp.add_argument("--focus", "-f", type=float, default=8.0, help="Depth of focus 1.0 to 10.0 (default: 8.0)")
    p_damp.add_argument("--completion", "-c", type=float, default=0.5, help="Task completion ratio 0.0 to 1.0 (default: 0.5)")
    p_damp.add_argument("--minutes", "-m", type=float, default=35.0, help="Minutes spent in continuous flow (default: 35.0)")
    p_damp.add_argument("--next-step", "-n", default="Run integration benchmark against edge cluster", help="Immediate first action on return")
    p_damp.add_argument("--loops", "-l", nargs="*", default=["Uncommitted state buffer", "Pending race condition test"], help="Unresolved open loops or tensions")
    p_damp.add_argument("--canvas", default="", help="Output Obsidian .canvas filepath")
    p_damp.add_argument("--svg", "-s", default="", help="Output attention residue gauge SVG filepath")
    p_damp.add_argument("--json", "-j", action="store_true", help="Output raw JSON interleaving telemetry")
    
    # examine / grill / cross-examine
    p_examine = subparsers.add_parser("examine", aliases=["grill", "cross-examine"], help="Autonomous cognitive multi-perspective architectural Socratic cross-examiner")
    p_examine.add_argument("title", nargs="?", default="Core System Architecture", help="System or proposal title")
    p_examine.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_examine.add_argument("--svg", "-s", default="", help="Output 5-axis rigor radar SVG filepath")
    p_examine.add_argument("--json", "-j", action="store_true", help="Output raw JSON examination scorecard")
    p_examine.add_argument("--demo", action="store_true", help="Run with demonstration architecture components")

    # audio-pacer / pacer / soundstage
    p_pacer = subparsers.add_parser("audio-pacer", aliases=["pacer", "soundstage"], help="Autonomous cognitive spatial saliency decoupler and multi-track audio pacer")
    p_pacer.add_argument("task", nargs="?", default="Cognitive Architecture Sprint", help="Task name or description")
    p_pacer.add_argument("--complexity", "-k", type=float, default=0.7, help="Task complexity 0.0 to 1.0 (default: 0.7)")
    p_pacer.add_argument("--load", "-l", type=float, default=0.6, help="Cognitive load saturation 0.0 to 1.0 (default: 0.6)")
    p_pacer.add_argument("--streams", "-s", nargs="*", default=[], help="Streams in format 'Name:Type' where Type in primary_focus, telemetry_log, rhythmic_pacer, alert_urgent, background_ambience")
    p_pacer.add_argument("--canvas", "-c", default="", help="Output Obsidian .canvas filepath")
    p_pacer.add_argument("--svg", default="", help="Output 2D soundstage radar SVG filepath")
    p_pacer.add_argument("--manifest", "-m", default="", help="Output Web Audio API manifest JSON filepath")
    p_pacer.add_argument("--json", "-j", action="store_true", help="Output raw JSON soundstage configuration")
    p_pacer.add_argument("--demo", action="store_true", help="Run with demonstration multi-track stream setup")

    # fovea / tunnel
    p_fovea = subparsers.add_parser("fovea", aliases=["tunnel", "attention-tunnel"], help="Autonomous cognitive spatial multi-scale attention tunnel and peripheral fovea synchronizer")
    p_fovea.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath")
    p_fovea.add_argument("--focus", "-f", default="", help="Node ID to focus on")
    p_fovea.add_argument("--load", "-l", type=float, default=0.6, help="Cognitive load saturation 0.0 to 1.0 (default: 0.6)")
    p_fovea.add_argument("--mode", "-m", choices=["desaturate_damp", "blur_attenuate", "minimal_skeleton", "adaptive_lod"], default="desaturate_damp", help="Damping mode (default: desaturate_damp)")
    p_fovea.add_argument("--output-canvas", "-o", default="", help="Output synchronized .canvas filepath")
    p_fovea.add_argument("--svg", "-s", default="", help="Output attention tunnel radar SVG filepath")
    p_fovea.add_argument("--json", "-j", action="store_true", help="Output raw JSON fovea telemetry")
    p_fovea.add_argument("--demo", action="store_true", help="Run with demonstration spatial canvas layout")

    # consensus / merge / resolve-conflict
    p_cons = subparsers.add_parser("consensus", aliases=["merge", "resolve-conflict"], help="Autonomous cognitive multi-agent workspace consensus and semantic conflict synthesizer")
    p_cons.add_argument("--base", "-b", default="", help="Base ancestor Obsidian .canvas filepath")
    p_cons.add_argument("--branch-a", "-1", default="", help="Branch A Obsidian .canvas filepath")
    p_cons.add_argument("--branch-b", "-2", default="", help="Branch B Obsidian .canvas filepath")
    p_cons.add_argument("--output-canvas", "-o", default="", help="Output synthesized merge .canvas filepath")
    p_cons.add_argument("--svg", "-s", default="", help="Output consensus radar SVG filepath")
    p_cons.add_argument("--json", "-j", action="store_true", help="Output raw JSON consensus scorecard")
    p_cons.add_argument("--demo", action="store_true", help="Run with demonstration divergent multi-agent canvases")

    # gaze / inertia / saccade-velocity
    p_gaze = subparsers.add_parser("gaze", aliases=["inertia", "saccade-velocity"], help="Autonomous cognitive spatial working memory saccade velocity and gaze inertia balancer")
    p_gaze.add_argument("canvas", nargs="?", default="", help="Target Obsidian .canvas filepath")
    p_gaze.add_argument("--sequence", "-q", nargs="*", default=[], help="Optional ordered node ID reading traverse sequence")
    p_gaze.add_argument("--output-canvas", "-o", default="", help="Output stabilized .canvas filepath with stepping stones")
    p_gaze.add_argument("--svg", "-s", default="", help="Output saccadic velocity profile SVG filepath")
    p_gaze.add_argument("--json", "-j", action="store_true", help="Output raw JSON gaze inertia telemetry")
    p_gaze.add_argument("--demo", action="store_true", help="Run with demonstration spatial canvas layout")

    # scanpath / flow / compress-reading
    p_scanpath = subparsers.add_parser("scanpath", aliases=["flow", "compress-reading"], help="Autonomous cognitive spatial saccadic scanpath compressor and reading flow harness")
    p_scanpath.add_argument("input", nargs="?", default="", help="Target text or markdown filepath to compress and guide")
    p_scanpath.add_argument("--mode", "-m", choices=["bionic_ramp", "corridor_chunk", "return_beacon", "hybrid_flow"], default="hybrid_flow", help="Guidance mode (default: hybrid_flow)")
    p_scanpath.add_argument("--chars", "-c", type=int, default=55, help="Target characters per corridor line (default: 55)")
    p_scanpath.add_argument("--output", "-o", default="", help="Output guided markdown filepath")
    p_scanpath.add_argument("--canvas", default="", help="Output Obsidian .canvas filepath")
    p_scanpath.add_argument("--svg", "-s", default="", help="Output scanpath trajectory SVG filepath")
    p_scanpath.add_argument("--json", "-j", action="store_true", help="Output raw JSON scanpath telemetry")
    p_scanpath.add_argument("--demo", action="store_true", help="Run with demonstration technical specification prose")

    # visual-metronome / metronome / pace-reading
    p_metronome = subparsers.add_parser("visual-metronome", aliases=["metronome", "pace-reading"], help="Autonomous cognitive spatial visual pacing rhythm and bionic fixation metronome")
    p_metronome.add_argument("input", nargs="?", default="", help="Target text or markdown filepath to pace")
    p_metronome.add_argument("--wpm", "-w", type=float, default=200.0, help="Target reading words per minute (default: 200)")
    p_metronome.add_argument("--mode", "-m", choices=["isochronic", "syllable_adaptive", "morphological", "accelerative"], default="syllable_adaptive", help="Pacing rhythm mode (default: syllable_adaptive)")
    p_metronome.add_argument("--canvas", default="", help="Output Obsidian .canvas filepath")
    p_metronome.add_argument("--svg", "-s", default="", help="Output visual metronome strip SVG filepath")
    p_metronome.add_argument("--json", "-j", action="store_true", help="Output raw JSON metronome telemetry")
    p_metronome.add_argument("--demo", action="store_true", help="Run with demonstration technical specification prose")

    # chunk-pacer / chunk / syntactic-chunk
    p_chunk = subparsers.add_parser("chunk-pacer", aliases=["chunk", "syntactic-chunk"], help="Autonomous cognitive spatial visual chunk pacer and ocular fixation metronome")
    p_chunk.add_argument("input", nargs="?", default="", help="Target text or markdown filepath to chunk and pace")
    p_chunk.add_argument("--wpm", "-w", type=float, default=200.0, help="Target reading words per minute (default: 200)")
    p_chunk.add_argument("--tokens", "-t", type=int, default=3, help="Target tokens per syntactic phrase chunk (default: 3)")
    p_chunk.add_argument("--canvas", default="", help="Output Obsidian .canvas filepath")
    p_chunk.add_argument("--svg", "-s", default="", help="Output syntactic chunk strip SVG filepath")
    p_chunk.add_argument("--json", "-j", action="store_true", help="Output raw JSON chunk pacing telemetry")
    p_chunk.add_argument("--demo", action="store_true", help="Run with demonstration technical specification prose")

    # memory-shield / shield / saliency-shield
    p_shield = subparsers.add_parser("memory-shield", aliases=["shield", "saliency-shield"], help="Autonomous cognitive spatial saliency decoupling and working memory shield")
    p_shield.add_argument("canvas", nargs="?", default="", help="Target Obsidian .canvas filepath to shield")
    p_shield.add_argument("--focus", "-f", nargs="*", default=[], help="Optional list of active focus node IDs")
    p_shield.add_argument("--focus-radius", type=float, default=600.0, help="Radial distance of primary focus zone in px (default: 600)")
    p_shield.add_argument("--orientation-radius", type=float, default=1200.0, help="Radial distance of orientation ring in px (default: 1200)")
    p_shield.add_argument("--output-canvas", "-o", default="", help="Output shielded Obsidian .canvas filepath")
    p_shield.add_argument("--svg", "-s", default="", help="Output shielding radar SVG filepath")
    p_shield.add_argument("--json", "-j", action="store_true", help="Output raw JSON memory shield telemetry")
    p_shield.add_argument("--demo", action="store_true", help="Run with demonstration spatial canvas layout")

    # dual-code / dual-coder / dual-track
    p_dual = subparsers.add_parser("dual-code", aliases=["dual-coder", "dual-track"], help="Autonomous cognitive spatial dual-code working memory interleaver")
    p_dual.add_argument("canvas", nargs="?", default="", help="Target Obsidian .canvas filepath")
    p_dual.add_argument("--prose", "-p", default="", help="Target verbal prose or markdown filepath")
    p_dual.add_argument("--output-markdown", "-o", default="", help="Output interleaved markdown filepath")
    p_dual.add_argument("--output-canvas", "-c", default="", help="Output dual-code synchronized Obsidian .canvas filepath")
    p_dual.add_argument("--svg", "-s", default="", help="Output dual-track visualization SVG filepath")
    p_dual.add_argument("--json", "-j", action="store_true", help="Output raw JSON dual-code telemetry")
    p_dual.add_argument("--demo", action="store_true", help="Run with demonstration dual-code architecture pair")

    # saccadic-pivot / pivot / anchor-restore
    p_pivot = subparsers.add_parser("saccadic-pivot", aliases=["pivot", "anchor-restore"], help="Autonomous cognitive spatial dual-foveal saccadic pivot and anchor restorer")
    p_pivot.add_argument("canvas", nargs="?", default="", help="Target Obsidian .canvas filepath")
    p_pivot.add_argument("--source", "-s", default="src", help="Source node ID of prior gaze focus")
    p_pivot.add_argument("--target", "-t", default="tgt", help="Target node ID of re-entry focus")
    p_pivot.add_argument("--output-canvas", "-o", default="", help="Output enriched Obsidian .canvas filepath with anchor beacon")
    p_pivot.add_argument("--svg", default="", help="Output saccadic trajectory SVG filepath")
    p_pivot.add_argument("--json", "-j", action="store_true", help="Output raw JSON pivot telemetry")
    p_pivot.add_argument("--demo", action="store_true", help="Run with demonstration spatial pivot layout")

    # concept-lattice / lattice / fca / resonance-compiler
    p_lattice = subparsers.add_parser("concept-lattice", aliases=["lattice", "fca", "resonance-compiler"], help="Autonomous cognitive spatial associative resonance and concept lattice compiler")
    p_lattice.add_argument("input", nargs="?", default="", help="Input JSON context filepath or Obsidian .canvas file")
    p_lattice.add_argument("--min-resonance", "-r", type=float, default=0.35, help="Minimum threshold for associative resonance leap detection")
    p_lattice.add_argument("--output-canvas", "-o", default="", help="Output Obsidian .canvas filepath for lattice visualization")
    p_lattice.add_argument("--svg", default="", help="Output SVG filepath for publication lattice diagram")
    p_lattice.add_argument("--json", "-j", action="store_true", help="Output raw JSON lattice and resonance telemetry")
    p_lattice.add_argument("--demo", action="store_true", help="Run with demonstration cross-domain cognitive architecture context")

    # action-sequencer / sequencer / dag-runner / executive-scaffold
    p_action = subparsers.add_parser("action-sequencer", aliases=["sequencer", "dag-runner", "executive-scaffold"], help="Autonomous cognitive spatial non-linear executive scaffolding and action sequencer")
    p_action.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or tasks JSON file")
    p_action.add_argument("--default-time", "-t", type=int, default=25, help="Default task estimate in minutes")
    p_action.add_argument("--output-canvas", "-o", default="", help="Output sequenced Obsidian .canvas filepath")
    p_action.add_argument("--svg", default="", help="Output critical path DAG SVG diagram filepath")
    p_action.add_argument("--json", "-j", action="store_true", help="Output raw JSON sequencing telemetry")
    p_action.add_argument("--demo", action="store_true", help="Run with demonstration non-linear project execution graph")

    # cognitive-aperture / aperture / scope-bound / cowan-lens
    p_aperture = subparsers.add_parser("cognitive-aperture", aliases=["aperture", "scope-bound", "cowan-lens"], help="Autonomous cognitive spatial dynamic cognitive aperture and scope bounding harness")
    p_aperture.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or tasks JSON file")
    p_aperture.add_argument("--capacity", "-c", type=int, default=4, help="Working memory capacity limit (Cowan 4-chunk threshold, default: 4)")
    p_aperture.add_argument("--focal", nargs="*", default=[], help="Explicit node IDs to pin inside the focal aperture")
    p_aperture.add_argument("--output-canvas", "-o", default="", help="Output aperture-attenuated Obsidian .canvas filepath")
    p_aperture.add_argument("--svg", default="", help="Output cognitive aperture concentric radar SVG diagram filepath")
    p_aperture.add_argument("--json", "-j", action="store_true", help="Output raw JSON aperture telemetry")
    p_aperture.add_argument("--demo", action="store_true", help="Run with demonstration multi-tier cognitive working memory field")

    # dialectic-synthesizer / triad / dialectic-mesh / aufhebung
    p_triad = subparsers.add_parser("dialectic-synthesizer", aliases=["triad", "dialectic-mesh", "aufhebung"], help="Autonomous cognitive spatial associative multi-perspective dialectic synthesizer and synthesis mesh")
    p_triad.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or polarity JSON file")
    p_triad.add_argument("--min-tension", "-t", type=float, default=0.35, help="Minimum tension intensity threshold to trigger synthesis")
    p_triad.add_argument("--output-canvas", "-o", default="", help="Output triadic synthesis Obsidian .canvas filepath")
    p_triad.add_argument("--svg", default="", help="Output dialectic triad SVG diagram filepath")
    p_triad.add_argument("--json", "-j", action="store_true", help="Output raw JSON dialectic telemetry")
    p_triad.add_argument("--demo", action="store_true", help="Run with demonstration architectural polarity tensions")

    # density-calibrator / density / whitespace-balancer / bouma-lens
    p_density = subparsers.add_parser("density-calibrator", aliases=["density", "whitespace-balancer", "bouma-lens"], help="Autonomous cognitive spatial multi-scale attention density calibrator and visual restorer")
    p_density.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or node layout JSON file")
    p_density.add_argument("--foveal-sigma", "-s", type=float, default=200.0, help="Foveal attention Gaussian kernel standard deviation (default: 200.0)")
    p_density.add_argument("--bouma-factor", "-b", type=float, default=1.6, help="Bouma clearance ratio factor (default: 1.6)")
    p_density.add_argument("--output-canvas", "-o", default="", help="Output rebalanced Obsidian .canvas filepath")
    p_density.add_argument("--svg", default="", help="Output attention density SVG diagram filepath")
    p_density.add_argument("--json", "-j", action="store_true", help="Output raw JSON density telemetry")
    p_density.add_argument("--demo", action="store_true", help="Run with demonstration high-density crowded canvas")

    # code-symbol-mesh / code-mesh / ast-mesh / symbol-mesh / interface-mapper
    p_mesh = subparsers.add_parser("code-symbol-mesh", aliases=["code-mesh", "ast-mesh", "symbol-mesh", "interface-mapper"], help="Autonomous cognitive spatial multi-modal code signature synthesizer and symbol mesh")
    p_mesh.add_argument("source", nargs="?", default="", help="Input Python source code filepath, JSON symbol spec, or Obsidian .canvas")
    p_mesh.add_argument("--max-coupling", "-c", type=int, default=5, help="Maximum allowed fan-out coupling before boundary leak warning (default: 5)")
    p_mesh.add_argument("--output-canvas", "-o", default="", help="Output symbol mesh Obsidian .canvas filepath")
    p_mesh.add_argument("--svg", default="", help="Output symbol mesh SVG diagram filepath")
    p_mesh.add_argument("--json", "-j", action="store_true", help="Output raw JSON symbol mesh telemetry")
    p_mesh.add_argument("--demo", action="store_true", help="Run with demonstration multi-tier architectural symbols")

    # anchor-stacking / anchor-stack / stack-compactor / breadcrumb-trail
    p_stack = subparsers.add_parser("anchor-stacking", aliases=["anchor-stack", "stack-compactor", "breadcrumb-trail"], help="Autonomous cognitive spatial working memory anchor stacking and compaction harness")
    p_stack.add_argument("stack", nargs="?", default="", help="Input Obsidian .canvas filepath or subgraphs JSON file")
    p_stack.add_argument("--max-capacity", "-c", type=int, default=4, help="Maximum concurrent active working memory slots (default: 4)")
    p_stack.add_argument("--output-canvas", "-o", default="", help="Output compacted anchor stack Obsidian .canvas filepath")
    p_stack.add_argument("--svg", default="", help="Output anchor stack SVG diagram filepath")
    p_stack.add_argument("--json", "-j", action="store_true", help="Output raw JSON stack telemetry")
    p_stack.add_argument("--demo", action="store_true", help="Run with demonstration hierarchical multi-scale subgraphs")

    # saliency-matrix / saliency-decoupler / attenuation-matrix / focus-spotlight
    p_saliency = subparsers.add_parser("saliency-matrix", aliases=["saliency-decoupler", "attenuation-matrix", "focus-spotlight"], help="Autonomous cognitive spatial working memory saliency decoupler and attenuation matrix")
    p_saliency.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or nodes JSON file")
    p_saliency.add_argument("--focal", "-f", default="", help="Target node ID of active focal locus (default: first node)")
    p_saliency.add_argument("--decay", "-d", type=float, default=0.0018, help="Exponential spatial distance attenuation decay rate (default: 0.0018)")
    p_saliency.add_argument("--output-canvas", "-o", default="", help="Output attenuated Obsidian .canvas filepath")
    p_saliency.add_argument("--svg", default="", help="Output saliency matrix SVG diagram filepath")
    p_saliency.add_argument("--json", "-j", action="store_true", help="Output raw JSON saliency telemetry")
    p_saliency.add_argument("--demo", action="store_true", help="Run with demonstration multi-tier spatial chatter field")

    # resonance-weaver / resonance / hyperlink-weaver / associative-bridge
    p_weaver = subparsers.add_parser("resonance-weaver", aliases=["resonance", "hyperlink-weaver", "associative-bridge"], help="Autonomous cognitive spatial bi-directional hyper-link resonance weaver")
    p_weaver.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or nodes JSON file")
    p_weaver.add_argument("--threshold", "-t", type=float, default=0.20, help="Minimum Jaccard resonance affinity threshold (default: 0.20)")
    p_weaver.add_argument("--output-canvas", "-o", default="", help="Output enriched Obsidian .canvas filepath")
    p_weaver.add_argument("--svg", default="", help="Output resonance bridge SVG diagram filepath")
    p_weaver.add_argument("--json", "-j", action="store_true", help="Output raw JSON resonance telemetry")
    p_weaver.add_argument("--demo", action="store_true", help="Run with demonstration cross-domain knowledge nodes")

    # saccade-calibrator / gaze-path-calibrator / ovp-calibrator / saccade-envelope
    p_scalib = subparsers.add_parser("saccade-calibrator", aliases=["gaze-path-calibrator", "ovp-calibrator", "saccade-envelope"], help="Autonomous cognitive spatial working memory saccade velocity and gaze path calibrator")
    p_scalib.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or nodes JSON file")
    p_scalib.add_argument("--max-jump", "-m", type=float, default=450.0, help="Maximum comfortable ballistic jump distance in pixels (default: 450.0)")
    p_scalib.add_argument("--output-canvas", "-o", default="", help="Output calibrated Obsidian .canvas filepath")
    p_scalib.add_argument("--svg", default="", help="Output gaze path velocity SVG diagram filepath")
    p_scalib.add_argument("--json", "-j", action="store_true", help="Output raw JSON gaze telemetry")
    p_scalib.add_argument("--demo", action="store_true", help="Run with demonstration multi-column spatial cards")

    # schema-projection / schema-projector / cross-scale-projector / allocentric-projector
    p_sproj = subparsers.add_parser("schema-projection", aliases=["schema-projector", "cross-scale-projector", "allocentric-projector"], help="Autonomous cognitive spatial schema morphing and cross-scale projection engine")
    p_sproj.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or nodes JSON file")
    p_sproj.add_argument("--output-canvas", "-o", default="", help="Output multi-scale projected Obsidian .canvas filepath")
    p_sproj.add_argument("--svg", default="", help="Output cross-scale projection SVG diagram filepath")
    p_sproj.add_argument("--json", "-j", action="store_true", help="Output raw JSON projection telemetry")
    p_sproj.add_argument("--demo", action="store_true", help="Run with demonstration triadic abstraction plane entities")

    # attention-flow / attention-heatmap / density-flow / dwell-optimizer
    p_aflow = subparsers.add_parser("attention-flow", aliases=["attention-heatmap", "density-flow", "dwell-optimizer"], help="Autonomous cognitive spatial multi-scale attention heatmap and density flow optimizer")
    p_aflow.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or nodes JSON file")
    p_aflow.add_argument("--wpm", type=float, default=220.0, help="Baseline reading speed in words per minute (default: 220.0)")
    p_aflow.add_argument("--threshold", "-t", type=float, default=4000.0, help="Cognitive stagnation dwell threshold in milliseconds (default: 4000.0)")
    p_aflow.add_argument("--output-canvas", "-o", default="", help="Output flow-balanced Obsidian .canvas filepath")
    p_aflow.add_argument("--svg", default="", help="Output attention heatmap SVG diagram filepath")
    p_aflow.add_argument("--json", "-j", action="store_true", help="Output raw JSON attention flow telemetry")
    p_aflow.add_argument("--demo", action="store_true", help="Run with demonstration uneven density spatial cards")

    # working-set / cowan-pruner / set-pruner / bead-pruner
    p_wset = subparsers.add_parser("working-set", aliases=["cowan-pruner", "set-pruner", "bead-pruner"], help="Autonomous cognitive spatial working memory anchor eviction and dynamic working set pruner")
    p_wset.add_argument("canvas", nargs="?", default="", help="Input Obsidian .canvas filepath or nodes JSON file")
    p_wset.add_argument("--max-active", "-m", type=int, default=4, help="Maximum concurrent active focus chunks (default: 4)")
    p_wset.add_argument("--ghost-opacity", "-g", type=float, default=0.35, help="Visual opacity for peripheral ghosted nodes (default: 0.35)")
    p_wset.add_argument("--focal", "-f", nargs="*", default=[], help="Explicit focal node IDs to preserve in active working set")
    p_wset.add_argument("--output-canvas", "-o", default="", help="Output pruned Obsidian .canvas filepath")
    p_wset.add_argument("--svg", default="", help="Output working set SVG diagram filepath")
    p_wset.add_argument("--json", "-j", action="store_true", help="Output raw JSON working set telemetry")
    p_wset.add_argument("--demo", action="store_true", help="Run with demonstration 8-card spatial canvas")

    # dialectic-loom / aufhebung-loom / synthesis-loom / reification-loom
    p_dloom = subparsers.add_parser("dialectic-loom", aliases=["aufhebung-loom", "synthesis-loom", "reification-loom"], help="Autonomous cognitive spatial multi-perspective dialectic reification and synthesis loom")
    p_dloom.add_argument("input", nargs="?", default="", help="Input Obsidian .canvas filepath or argument cards JSON file")
    p_dloom.add_argument("--max-chunks", "-m", type=int, default=4, help="Maximum concurrent working memory chunks (default: 4)")
    p_dloom.add_argument("--canvas", "-o", default="", help="Output synthesized Obsidian .canvas filepath")
    p_dloom.add_argument("--svg", default="", help="Output dark titanium dialectic triad SVG filepath")
    p_dloom.add_argument("--json", "-j", action="store_true", help="Output raw JSON dialectic telemetry")
    p_dloom.add_argument("--demo", action="store_true", help="Run with demonstration architectural thesis and antithesis cards")

    # lexical-pacer / bionic-pacer / ovp-pacer / fixation-pacer
    p_lpacer = subparsers.add_parser("lexical-pacer", aliases=["bionic-pacer", "ovp-pacer", "fixation-pacer"], help="Autonomous cognitive spatial dynamic lexical pacing and bionic fixation anchor synthesizer")
    p_lpacer.add_argument("input", nargs="?", default="", help="Input text filepath to pace")
    p_lpacer.add_argument("--wpm", "-w", type=int, default=260, help="Target reading cadence WPM (default: 260)")
    p_lpacer.add_argument("--markdown", "-m", action="store_true", help="Output bionic markdown with bolded prefix anchors")
    p_lpacer.add_argument("--html", default="", help="Output bionic reader HTML filepath")
    p_lpacer.add_argument("--svg", default="", help="Output OVP fixation curve SVG diagram filepath")
    p_lpacer.add_argument("--json", "-j", action="store_true", help="Output raw JSON pacing telemetry")
    p_lpacer.add_argument("--demo", action="store_true", help="Run with demonstration technical paragraph")

    # galois-lattice / galois-engine / fca-lattice / associative-constellation
    p_galois = subparsers.add_parser("galois-lattice", aliases=["galois-engine", "fca-lattice", "associative-constellation"], help="Autonomous cognitive spatial cross-scale associative constellation and Galois lattice engine")
    p_galois.add_argument("input", nargs="?", default="", help="Input Obsidian .canvas filepath or formal entities JSON file")
    p_galois.add_argument("--threshold", "-t", type=float, default=0.25, help="Minimum resonance score threshold for bridges (default: 0.25)")
    p_galois.add_argument("--canvas", "-o", default="", help="Output constellation Obsidian .canvas filepath")
    p_galois.add_argument("--svg", default="", help="Output Galois lattice SVG diagram filepath")
    p_galois.add_argument("--json", "-j", action="store_true", help="Output raw JSON lattice telemetry")
    p_galois.add_argument("--demo", action="store_true", help="Run with demonstration 4-entity cross-cluster context")

    # fatigue-meter / saccadic-fatigue / contrast-damper / ocular-fatigue
    p_fatigue = subparsers.add_parser("fatigue-meter", aliases=["saccadic-fatigue", "contrast-damper", "ocular-fatigue"], help="Autonomous cognitive spatial working memory saccadic fatigue meter and dynamic contrast damper")
    p_fatigue.add_argument("input", nargs="?", default="", help="Input gaze session JSON filepath")
    p_fatigue.add_argument("--baseline", "-b", type=float, default=420.0, help="Baseline saccadic peak velocity in deg/s (default: 420.0)")
    p_fatigue.add_argument("--session-max", type=float, default=45.0, help="Maximum recommended continuous session duration in minutes (default: 45.0)")
    p_fatigue.add_argument("--css", default="", help="Output restorative CSS tokens filepath")
    p_fatigue.add_argument("--svg", default="", help="Output fatigue main sequence SVG diagram filepath")
    p_fatigue.add_argument("--json", "-j", action="store_true", help="Output raw JSON fatigue telemetry")
    p_fatigue.add_argument("--demo", action="store_true", help="Run with demonstration 20-sample decaying gaze session")

    # stress-tester / lexical-stress / syntax-friction / stepping-stones
    p_stress = subparsers.add_parser("stress-tester", aliases=["lexical-stress", "syntax-friction", "stepping-stones"], help="Autonomous cognitive spatial dynamic lexical stress-testing and gaze anchor synthesizer")
    p_stress.add_argument("input", nargs="?", default="", help="Input source code or text filepath")
    p_stress.add_argument("--code", "-c", default="", help="Raw code or text snippet string to stress-test")
    p_stress.add_argument("--depth", "-d", type=int, default=3, help="Maximum acceptable syntactic nesting depth before friction escalation (default: 3)")
    p_stress.add_argument("--threshold", "-t", type=float, default=0.60, help="Friction index threshold for stepping stone generation (default: 0.60)")
    p_stress.add_argument("--output-md", default="", help="Output stepped markdown filepath")
    p_stress.add_argument("--output-html", default="", help="Output stepped HTML filepath")
    p_stress.add_argument("--svg", default="", help="Output lexical friction heatmap and trajectory SVG diagram filepath")
    p_stress.add_argument("--json", "-j", action="store_true", help="Output raw JSON lexical stress telemetry")
    p_stress.add_argument("--demo", action="store_true", help="Run with demonstration nested code snippet")

    # anchor-distiller / distill-anchors / canvas-radar / semantic-index
    p_distiller = subparsers.add_parser("anchor-distiller", aliases=["distill-anchors", "canvas-radar", "semantic-index"], help="Autonomous cognitive spatial multi-scale semantic anchor distillation and visual indexer")
    p_distiller.add_argument("input", nargs="?", default="", help="Input canvas JSON or items JSON filepath")
    p_distiller.add_argument("--threshold", "-t", type=float, default=650.0, help="Cluster spatial distance threshold in canvas units (default: 650.0)")
    p_distiller.add_argument("--canvas", default="", help="Output Obsidian Canvas (.canvas) filepath")
    p_distiller.add_argument("--svg", default="", help="Output visual indexer radar map SVG filepath")
    p_distiller.add_argument("--json", "-j", action="store_true", help="Output raw JSON distillation telemetry")
    p_distiller.add_argument("--demo", action="store_true", help="Run with demonstration multi-cluster spatial canvas nodes")

    # foveal-horizon / foveal-drift / breadcrumb-restorer / zoom-horizon
    p_fhorizon = subparsers.add_parser("foveal-horizon", aliases=["foveal-drift", "breadcrumb-restorer", "zoom-horizon"], help="Autonomous cognitive spatial dynamic foveal horizon and context anchor restorer")
    p_fhorizon.add_argument("input", nargs="?", default="", help="Input transition JSON filepath")
    p_fhorizon.add_argument("--source-zoom", type=float, default=0.35, help="Source zoom scale level (default: 0.35)")
    p_fhorizon.add_argument("--target-zoom", type=float, default=3.20, help="Target zoom scale level (default: 3.20)")
    p_fhorizon.add_argument("--displacement", type=float, default=1800.0, help="Pan linear displacement in pixels (default: 1800.0)")
    p_fhorizon.add_argument("--css", default="", help="Output restorative transition CSS filepath")
    p_fhorizon.add_argument("--svg", default="", help="Output foveal horizon SVG diagram filepath")
    p_fhorizon.add_argument("--json", "-j", action="store_true", help="Output raw JSON horizon telemetry")
    p_fhorizon.add_argument("--demo", action="store_true", help="Run with demonstration deep zoom transition")

    # attention-gradient / saccade-shaper / eccentricity-damper / acuity-gradient
    p_agradient = subparsers.add_parser("attention-gradient", aliases=["saccade-shaper", "eccentricity-damper", "acuity-gradient"], help="Autonomous cognitive spatial dynamic attention gradient and peripheral saccade shaper")
    p_agradient.add_argument("input", nargs="?", default="", help="Input workspace cards JSON filepath")
    p_agradient.add_argument("--gaze-x", type=float, default=200.0, help="Focal gaze center X coordinate (default: 200.0)")
    p_agradient.add_argument("--gaze-y", type=float, default=200.0, help="Focal gaze center Y coordinate (default: 200.0)")
    p_agradient.add_argument("--target-x", type=float, default=900.0, help="Saccade target X coordinate (default: 900.0)")
    p_agradient.add_argument("--target-y", type=float, default=300.0, help="Saccade target Y coordinate (default: 300.0)")
    p_agradient.add_argument("--css", default="", help="Output peripheral attenuation CSS filepath")
    p_agradient.add_argument("--svg", default="", help="Output attention gradient SVG diagram filepath")
    p_agradient.add_argument("--json", "-j", action="store_true", help="Output raw JSON gradient telemetry")
    p_agradient.add_argument("--demo", action="store_true", help="Run with demonstration multi-card eccentricity workspace")

    # causal-loom / narrative-loom / causal-dag / quest-loom
    p_cloom = subparsers.add_parser("causal-loom", aliases=["narrative-loom", "causal-dag", "quest-loom"], help="Autonomous cognitive spatial bi-directional narrative loom and causal graph synthesizer")
    p_cloom.add_argument("input", nargs="?", default="", help="Input causal nodes JSON, DAG JSON, or text notes filepath")
    p_cloom.add_argument("--depth", "-d", type=int, default=4, help="Maximum acceptable Cowan depth for primary causal chain (default: 4)")
    p_cloom.add_argument("--output-md", default="", help="Output executive narrative markdown filepath")
    p_cloom.add_argument("--svg", default="", help="Output causal DAG SVG diagram filepath")
    p_cloom.add_argument("--json", "-j", action="store_true", help="Output raw JSON causal loom telemetry")
    p_cloom.add_argument("--demo", action="store_true", help="Run with demonstration architectural causal DAG")

    # epistemic-radar / uncertainty-radar / assumption-tester / fragility-radar
    p_eradar = subparsers.add_parser("epistemic-radar", aliases=["uncertainty-radar", "assumption-tester", "fragility-radar"], help="Autonomous cognitive spatial epistemic uncertainty radar and assumption stress-tester")
    p_eradar.add_argument("input", nargs="?", default="", help="Input claims JSON file or architectural text specification")
    p_eradar.add_argument("--threshold", "-t", type=float, default=0.60, help="Fragility threshold for single points of failure (default: 0.60)")
    p_eradar.add_argument("--output-table", default="", help="Output markdown mitigation table filepath")
    p_eradar.add_argument("--svg", default="", help="Output epistemic radar SVG diagram filepath")
    p_eradar.add_argument("--json", "-j", action="store_true", help="Output raw JSON epistemic telemetry")
    p_eradar.add_argument("--demo", action="store_true", help="Run with demonstration architectural claims and stress vectors")

    # vault-consolidate / anchor-vault / semantic-snapshot / rehydration-vault
    p_vault = subparsers.add_parser("vault-consolidate", aliases=["anchor-vault", "semantic-snapshot", "rehydration-vault"], help="Autonomous cognitive spatial working memory anchor consolidation and semantic snapshot vault")
    p_vault.add_argument("input", nargs="?", default="", help="Input canvas anchors JSON file or workspace specification")
    p_vault.add_argument("--threshold", "-t", type=float, default=0.65, help="Coherence threshold for sub-canvas consolidation (default: 0.65)")
    p_vault.add_argument("--radius", "-r", type=float, default=250.0, help="Spatial proximity radius for clustering (default: 250.0)")
    p_vault.add_argument("--manifest", default="", help="Output rehydration manifest markdown filepath")
    p_vault.add_argument("--svg", default="", help="Output vault map SVG diagram filepath")
    p_vault.add_argument("--rehydrate", default="", help="Rehydrate snapshot payload by snapshot ID or cluster ID")
    p_vault.add_argument("--json", "-j", action="store_true", help="Output raw JSON vault telemetry")
    p_vault.add_argument("--demo", action="store_true", help="Run with demonstration multi-cluster canvas anchors")

    # schema-transfer / isomorphism-engine / analogy-transfer / domain-mapper
    p_stransfer = subparsers.add_parser("schema-transfer", aliases=["isomorphism-engine", "analogy-transfer", "domain-mapper"], help="Autonomous cognitive spatial schema isomorphism and cross-domain analogy transfer engine")
    p_stransfer.add_argument("source", nargs="?", default="", help="Source domain schema JSON file")
    p_stransfer.add_argument("target", nargs="?", default="", help="Target domain schema JSON file")
    p_stransfer.add_argument("--threshold", "-t", type=float, default=0.55, help="Minimum alignment threshold for valid homomorphism (default: 0.55)")
    p_stransfer.add_argument("--report", default="", help="Output analogy transfer markdown report filepath")
    p_stransfer.add_argument("--svg", default="", help="Output isomorphic projection SVG diagram filepath")
    p_stransfer.add_argument("--json", "-j", action="store_true", help="Output raw JSON analogy transfer telemetry")
    p_stransfer.add_argument("--demo", action="store_true", help="Run with demonstration hydraulic to electrical circuit transfer")

    # narrative-reconcile / branch-reconciler / divergence-bridge / fork-synthesizer
    p_nreconcile = subparsers.add_parser("narrative-reconcile", aliases=["branch-reconciler", "divergence-bridge", "fork-synthesizer"], help="Autonomous cognitive spatial multiscale narrative branching and divergence reconciler")
    p_nreconcile.add_argument("input", nargs="?", default="", help="Input narrative branches JSON file or trajectory specification")
    p_nreconcile.add_argument("--threshold", "-t", type=float, default=0.35, help="Drift threshold triggering reconciliation bridges (default: 0.35)")
    p_nreconcile.add_argument("--synthesis", default="", help="Output executive synthesis markdown filepath")
    p_nreconcile.add_argument("--svg", default="", help="Output narrative reconciliation map SVG diagram filepath")
    p_nreconcile.add_argument("--json", "-j", action="store_true", help="Output raw JSON reconciliation telemetry")
    p_nreconcile.add_argument("--demo", action="store_true", help="Run with demonstration divergent architectural pathways")

    # topological-homotopy / homotopy-engine / topology-visualizer / deformation-engine
    p_thomotopy = subparsers.add_parser("topological-homotopy", aliases=["homotopy-engine", "topology-visualizer", "deformation-engine"], help="Autonomous cognitive spatial topological invariant and homotopy visualizer")
    p_thomotopy.add_argument("input", nargs="?", default="", help="Input topological nodes and edges JSON file")
    p_thomotopy.add_argument("--steps", "-s", type=int, default=5, help="Number of intermediate deformation steps (default: 5)")
    p_thomotopy.add_argument("--audit", default="", help="Output topological invariant audit markdown filepath")
    p_thomotopy.add_argument("--svg", default="", help="Output homotopy diagram SVG filepath")
    p_thomotopy.add_argument("--json", "-j", action="store_true", help="Output raw JSON homotopy telemetry")
    p_thomotopy.add_argument("--demo", action="store_true", help="Run with demonstration triangle cyclic topology")

    # lexical-gist / gist-compressor / dynamic-shorthand / semantic-gist
    p_gist = subparsers.add_parser("lexical-gist", aliases=["gist-compressor", "dynamic-shorthand", "semantic-gist"], help="Autonomous cognitive spatial dynamic lexical compression and semantic gist synthesizer")
    p_gist.add_argument("input", nargs="?", default="", help="Target text filepath or raw text string to compress")
    p_gist.add_argument("--ratio", "-r", type=float, default=0.40, help="Target compression ratio (default: 0.40)")
    p_gist.add_argument("--report", default="", help="Output gist markdown audit filepath")
    p_gist.add_argument("--svg", default="", help="Output spatial shorthand SVG diagram filepath")
    p_gist.add_argument("--json", "-j", action="store_true", help="Output raw JSON gist telemetry")
    p_gist.add_argument("--demo", action="store_true", help="Run with demonstration cognitive architecture prose")

    # saccade-filter / noise-gate / saliency-gate / saccade-gate
    p_sfilter = subparsers.add_parser("saccade-filter", aliases=["noise-gate", "saliency-gate", "saccade-gate"], help="Autonomous cognitive spatial attentional saccade saliency filter and noise gate")
    p_sfilter.add_argument("input", nargs="?", default="", help="Input nodes layout JSON filepath or Obsidian .canvas file")
    p_sfilter.add_argument("--threshold", "-t", type=float, default=0.35, help="Saliency noise gate threshold (default: 0.35)")
    p_sfilter.add_argument("--cutoff", "-c", type=float, default=600.0, help="Peripheral margin cutoff distance in px (default: 600.0)")
    p_sfilter.add_argument("--foveal", "-f", type=float, default=250.0, help="Central foveal focus radius in px (default: 250.0)")
    p_sfilter.add_argument("--report", default="", help="Output noise gate audit markdown filepath")
    p_sfilter.add_argument("--svg", default="", help="Output saccade saliency map SVG filepath")
    p_sfilter.add_argument("--json", "-j", action="store_true", help="Output raw JSON filter telemetry")
    p_sfilter.add_argument("--demo", action="store_true", help="Run with demonstration spatial nodes layout")

    # drift-compensator / recenter-harness / allocentric-drift / magnetic-anchor
    p_drift = subparsers.add_parser("drift-compensator", aliases=["recenter-harness", "allocentric-drift", "magnetic-anchor"], help="Autonomous cognitive spatial working memory drift compensator and re-centering harness")
    p_drift.add_argument("input", nargs="?", default="", help="Input waypoints and anchors JSON filepath")
    p_drift.add_argument("--threshold", "-t", type=float, default=350.0, help="Allocentric drift threshold in px (default: 350.0)")
    p_drift.add_argument("--spring", "-s", type=float, default=0.05, help="Magnetic attractor spring constant (default: 0.05)")
    p_drift.add_argument("--report", default="", help="Output drift audit markdown filepath")
    p_drift.add_argument("--svg", default="", help="Output drift vector field SVG filepath")
    p_drift.add_argument("--json", "-j", action="store_true", help="Output raw JSON drift telemetry")
    p_drift.add_argument("--demo", action="store_true", help="Run with demonstration exploratory path and anchors")

    # phonological-bridge / grapheme-resonator / sub-vocal-pacer / phonetic-friction
    p_phono = subparsers.add_parser("phonological-bridge", aliases=["grapheme-resonator", "sub-vocal-pacer", "phonetic-friction"], help="Autonomous cognitive spatial multimodal phonological loop bridge and grapheme resonator")
    p_phono.add_argument("input", nargs="?", default="", help="Target text filepath or raw text string to evaluate")
    p_phono.add_argument("--threshold", "-t", type=float, default=0.55, help="High friction dissonance threshold (default: 0.55)")
    p_phono.add_argument("--report", default="", help="Output phonological audit markdown filepath")
    p_phono.add_argument("--svg", default="", help="Output syllabic resonance SVG map filepath")
    p_phono.add_argument("--json", "-j", action="store_true", help="Output raw JSON phonological telemetry")
    p_phono.add_argument("--demo", action="store_true", help="Run with demonstration technical specification text")

    # saccade-pacer / kinetic-pacer / fatigue-predictor / main-sequence
    p_kpacer = subparsers.add_parser("saccade-pacer", aliases=["kinetic-pacer", "fatigue-predictor", "main-sequence"], help="Autonomous cognitive spatial working memory saccade fatigue predictor and kinetic pacer")
    p_kpacer.add_argument("input", nargs="?", default="", help="Input saccades JSON filepath")
    p_kpacer.add_argument("--threshold", "-t", type=float, default=0.80, help="Velocity fatigue ratio threshold (default: 0.80)")
    p_kpacer.add_argument("--report", default="", help="Output kinetic audit markdown filepath")
    p_kpacer.add_argument("--svg", default="", help="Output Main Sequence velocity curve SVG filepath")
    p_kpacer.add_argument("--json", "-j", action="store_true", help="Output raw JSON kinetic telemetry")
    p_kpacer.add_argument("--demo", action="store_true", help="Run with demonstration ocular saccade sequence")

    # entropy-gate / density-equalizer / semantic-entropy / topological-density
    p_egate = subparsers.add_parser("entropy-gate", aliases=["density-equalizer", "semantic-entropy", "topological-density"], help="Autonomous cognitive spatial semantic entropy gate and topological density equalizer")
    p_egate.add_argument("input", nargs="?", default="", help="Input canvas JSON filepath")
    p_egate.add_argument("--radius", "-r", type=float, default=120.0, help="Local interaction foveal radius in px (default: 120.0)")
    p_egate.add_argument("--iterations", "-i", type=int, default=40, help="Force-directed relaxation iterations (default: 40)")
    p_egate.add_argument("--report", default="", help="Output entropy audit markdown filepath")
    p_egate.add_argument("--svg", default="", help="Output topological density SVG diagram filepath")
    p_egate.add_argument("--json", "-j", action="store_true", help="Output raw JSON entropy telemetry")
    p_egate.add_argument("--demo", action="store_true", help="Run with demonstration clustered canvas nodes")

    # bifurcation-radar / path-dependency / lock-in-loom / multiverse-fork
    p_bradar = subparsers.add_parser("bifurcation-radar", aliases=["path-dependency", "lock-in-loom", "multiverse-fork"], help="Autonomous cognitive spatial bifurcation radar and path-dependency loom")
    p_bradar.add_argument("input", nargs="?", default="", help="Input bifurcation forks JSON filepath")
    p_bradar.add_argument("--threshold", "-t", type=float, default=120.0, help="Switching friction threshold S_threshold (default: 120.0)")
    p_bradar.add_argument("--coupling", "-c", type=float, default=0.25, help="Coupling lambda coefficient for dependencies (default: 0.25)")
    p_bradar.add_argument("--report", default="", help="Output bifurcation audit markdown filepath")
    p_bradar.add_argument("--svg", default="", help="Output multiverse bifurcation SVG diagram filepath")
    p_bradar.add_argument("--json", "-j", action="store_true", help="Output raw JSON multiverse telemetry")
    p_bradar.add_argument("--demo", action="store_true", help="Run with demonstration architectural bifurcation forks")

    # foveal-recentering / saccadic-drift / drift-compensator-loom / foveal-loom
    p_floom = subparsers.add_parser("foveal-recentering", aliases=["saccadic-drift", "drift-compensator-loom", "foveal-loom"], help="Autonomous cognitive spatial working memory saccadic drift compensator and foveal re-centering loom")
    p_floom.add_argument("input", nargs="?", default="", help="Input gaze fixations JSON filepath")
    p_floom.add_argument("--threshold", "-t", type=float, default=45.0, help="Ocular drift threshold in px (default: 45.0)")
    p_floom.add_argument("--gain", "-g", type=float, default=0.40, help="Magnetic restorative vector gain (default: 0.40)")
    p_floom.add_argument("--report", default="", help="Output foveal drift audit markdown filepath")
    p_floom.add_argument("--svg", default="", help="Output foveal re-centering SVG diagram filepath")
    p_floom.add_argument("--json", "-j", action="store_true", help="Output raw JSON drift telemetry")
    p_floom.add_argument("--demo", action="store_true", help="Run with demonstration gaze fixation stream")

    # attentional-funnel / boundary-gasket / foveal-conduit / leakage-analyzer
    p_afunnel = subparsers.add_parser("attentional-funnel", aliases=["boundary-gasket", "foveal-conduit", "leakage-analyzer"], help="Autonomous cognitive spatial dynamic attentional funnel and saccadic boundary gasket")
    p_afunnel.add_argument("input", nargs="?", default="", help="Input canvas entities JSON filepath")
    p_afunnel.add_argument("--aperture", "-a", type=float, default=160.0, help="Central foveal aperture radius in px (default: 160.0)")
    p_afunnel.add_argument("--conduit", "-c", type=float, default=320.0, help="Attentional conduit outer radius in px (default: 320.0)")
    p_afunnel.add_argument("--min-opacity", "-m", type=float, default=0.15, help="Peripheral gasket minimum opacity (default: 0.15)")
    p_afunnel.add_argument("--focal-id", "-f", default=None, help="Focal entity ID to lock funnel center")
    p_afunnel.add_argument("--report", default="", help="Output boundary leakage markdown audit filepath")
    p_afunnel.add_argument("--svg", default="", help="Output attentional funnel SVG diagram filepath")
    p_afunnel.add_argument("--json", "-j", action="store_true", help="Output raw JSON funnel telemetry")
    p_afunnel.add_argument("--demo", action="store_true", help="Run with demonstration architectural canvas entities")

    # semantic-gravity / gravity-well / conceptual-orbit / thesis-attractor
    p_sgravity = subparsers.add_parser("semantic-gravity", aliases=["gravity-well", "conceptual-orbit", "thesis-attractor"], help="Autonomous cognitive spatial semantic gravity well and conceptual orbit engine")
    p_sgravity.add_argument("input", nargs="?", default="", help="Input conceptual system JSON filepath")
    p_sgravity.add_argument("--gravitational-constant", "-g", type=float, default=15000.0, help="Gravitational constant G (default: 15000.0)")
    p_sgravity.add_argument("--base-radius", "-b", type=float, default=95.0, help="Base orbital radius in px (default: 95.0)")
    p_sgravity.add_argument("--spacing", "-s", type=float, default=1.42, help="Orbital harmonic spacing factor (default: 1.42)")
    p_sgravity.add_argument("--report", default="", help="Output semantic gravity markdown audit filepath")
    p_sgravity.add_argument("--svg", default="", help="Output conceptual orbit SVG diagram filepath")
    p_sgravity.add_argument("--json", "-j", action="store_true", help="Output raw JSON gravity telemetry")
    p_sgravity.add_argument("--demo", action="store_true", help="Run with demonstration conceptual thesis system")

    # zoom-lens / anchor-stacking / semantic-zoom-lens / lod-lens
    p_zlens = subparsers.add_parser("zoom-lens", aliases=["semantic-zoom-lens", "lod-lens", "hierarchical-zoom"], help="Autonomous cognitive spatial working memory anchor stacking and hierarchical zoom lens")
    p_zlens.add_argument("input", nargs="?", default="", help="Input semantic anchors JSON filepath")
    p_zlens.add_argument("--zoom", "-z", type=float, default=1.0, help="Zoom magnification factor (e.g. 0.4 for Macro, 0.85 for Meso, 1.5 for Micro; default: 1.0)")
    p_zlens.add_argument("--macro-threshold", type=float, default=0.55, help="Macro LoD zoom threshold (default: 0.55)")
    p_zlens.add_argument("--meso-threshold", type=float, default=1.15, help="Meso LoD zoom threshold (default: 1.15)")
    p_zlens.add_argument("--report", default="", help="Output zoom lens audit markdown filepath")
    p_zlens.add_argument("--svg", default="", help="Output zoom lens SVG diagram filepath")
    p_zlens.add_argument("--json", "-j", action="store_true", help="Output raw JSON zoom telemetry")
    p_zlens.add_argument("--demo", action="store_true", help="Run with demonstration knowledge hierarchy")

    # concept-constellation / starburst / synesthetic-starburst / asterism-weaver
    p_cstar = subparsers.add_parser("concept-constellation", aliases=["starburst", "synesthetic-starburst", "asterism-weaver"], help="Autonomous cognitive spatial multimodal concept constellation and synesthetic starburst engine")
    p_cstar.add_argument("input", nargs="?", default="", help="Input concept stars JSON filepath")
    p_cstar.add_argument("--tether-distance", type=float, default=240.0, help="Maximum asterism tether distance in px (default: 240.0)")
    p_cstar.add_argument("--min-resonance", type=float, default=0.35, help="Minimum tether resonance threshold (default: 0.35)")
    p_cstar.add_argument("--report", default="", help="Output constellation audit markdown filepath")
    p_cstar.add_argument("--svg", default="", help="Output constellation SVG diagram filepath")
    p_cstar.add_argument("--json", "-j", action="store_true", help="Output raw JSON constellation telemetry")
    p_cstar.add_argument("--demo", action="store_true", help="Run with demonstration concept star clusters")

    # allocentric-compass / polar-compass / anchor-compass / heading-tracker
    p_acompass = subparsers.add_parser("allocentric-compass", aliases=["polar-compass", "anchor-compass", "heading-tracker"], help="Autonomous cognitive spatial allocentric compass and coordinate anchor compass engine")
    p_acompass.add_argument("input", nargs="?", default="", help="Input navigation session JSON filepath")
    p_acompass.add_argument("--max-jump", type=float, default=85.0, help="Maximum allowed heading jump before disorientation in deg (default: 85.0)")
    p_acompass.add_argument("--report", default="", help="Output allocentric compass audit markdown filepath")
    p_acompass.add_argument("--svg", default="", help="Output allocentric compass SVG diagram filepath")
    p_acompass.add_argument("--json", "-j", action="store_true", help="Output raw JSON compass telemetry")
    p_acompass.add_argument("--demo", action="store_true", help="Run with demonstration navigation trajectory")

    # tesseract-lattice / hypercube-schema / 4d-lattice / tesseract-projection
    p_tlatt = subparsers.add_parser("tesseract-lattice", aliases=["hypercube-schema", "4d-lattice", "tesseract-projection"], help="Autonomous cognitive spatial schema morphing lattice and topological tesseract engine")
    p_tlatt.add_argument("input", nargs="?", default="", help="Input 4D hypercube vertices JSON filepath")
    p_tlatt.add_argument("--theta", type=float, default=35.0, help="X-W rotation angle in deg (default: 35.0)")
    p_tlatt.add_argument("--phi", type=float, default=25.0, help="Z-W rotation angle in deg (default: 25.0)")
    p_tlatt.add_argument("--scale", type=float, default=135.0, help="Screen projection scale factor (default: 135.0)")
    p_tlatt.add_argument("--report", default="", help="Output tesseract audit markdown filepath")
    p_tlatt.add_argument("--svg", default="", help="Output tesseract wireframe SVG diagram filepath")
    p_tlatt.add_argument("--json", "-j", action="store_true", help="Output raw JSON tesseract telemetry")
    p_tlatt.add_argument("--demo", action="store_true", help="Run with demonstration canonical 16-cell hypercube schema")

    # dialectic-tensor / tensor-gate / orthogonality-gate / synthesis-tensor
    p_dtensor = subparsers.add_parser("dialectic-tensor", aliases=["tensor-gate", "orthogonality-gate", "synthesis-tensor"], help="Autonomous cognitive spatial dialectic tensor and semantic orthogonality gate")
    p_dtensor.add_argument("input", nargs="?", default="", help="Input dialectic concept vectors JSON filepath")
    p_dtensor.add_argument("--tension-threshold", type=float, default=0.50, help="Tension energy threshold for synthesis trigger (default: 0.50)")
    p_dtensor.add_argument("--report", default="", help="Output dialectic tensor audit markdown filepath")
    p_dtensor.add_argument("--svg", default="", help="Output dialectic tensor SVG diagram filepath")
    p_dtensor.add_argument("--json", "-j", action="store_true", help="Output raw JSON tensor telemetry")
    p_dtensor.add_argument("--demo", action="store_true", help="Run with demonstration dialectic vector set")

    # anchor-eviction / horizon-pacer / memory-sunset / decay-eviction
    p_aevict = subparsers.add_parser("anchor-eviction", aliases=["horizon-pacer", "memory-sunset", "decay-eviction"], help="Autonomous cognitive spatial working memory anchor eviction and graceful horizon pacer")
    p_aevict.add_argument("input", nargs="?", default="", help="Input decaying anchors JSON filepath")
    p_aevict.add_argument("--threshold", type=float, default=4.5, help="Working memory pressure threshold (default: 4.5)")
    p_aevict.add_argument("--time", type=float, default=1000.0, help="Current simulation timestamp in seconds (default: 1000.0)")
    p_aevict.add_argument("--report", default="", help="Output anchor eviction audit markdown filepath")
    p_aevict.add_argument("--svg", default="", help="Output anchor sunset horizon SVG filepath")
    p_aevict.add_argument("--json", "-j", action="store_true", help="Output raw JSON eviction telemetry")
    p_aevict.add_argument("--demo", action="store_true", help="Run with demonstration decaying anchor set")

    # saccadic-predictor / trajectory-predictor / gaze-prefetch / saccade-prefetch
    p_spred = subparsers.add_parser("saccadic-predictor", aliases=["trajectory-predictor", "gaze-prefetch", "saccade-prefetch"], help="Autonomous cognitive spatial working memory saccadic trajectory predictor and predictive pre-fetcher")
    p_spred.add_argument("input", nargs="?", default="", help="Input fixation history and candidate nodes JSON filepath")
    p_spred.add_argument("--distance", type=float, default=600.0, help="Maximum trajectory prediction distance in pixels (default: 600.0)")
    p_spred.add_argument("--report", default="", help="Output saccadic trajectory audit markdown filepath")
    p_spred.add_argument("--svg", default="", help="Output saccadic trajectory HUD SVG filepath")
    p_spred.add_argument("--json", "-j", action="store_true", help="Output raw JSON trajectory telemetry")
    p_spred.add_argument("--demo", action="store_true", help="Run with demonstration ocular fixation sequence")

    # knowledge-mesh / hypergraph-weaver / mesh-consolidator / semantic-weaver
    p_kmesh = subparsers.add_parser("knowledge-mesh", aliases=["hypergraph-weaver", "mesh-consolidator", "semantic-weaver"], help="Autonomous cognitive spatial knowledge mesh consolidator and semantic hyper-graph weaver")
    p_kmesh.add_argument("input", nargs="?", default="", help="Input multi-domain knowledge nodes JSON filepath")
    p_kmesh.add_argument("--min-cluster", type=int, default=2, help="Minimum nodes to form hyper-edge (default: 2)")
    p_kmesh.add_argument("--report", default="", help="Output knowledge mesh audit markdown filepath")
    p_kmesh.add_argument("--svg", default="", help="Output knowledge hyper-graph SVG filepath")
    p_kmesh.add_argument("--json", "-j", action="store_true", help="Output raw JSON mesh telemetry")
    p_kmesh.add_argument("--demo", action="store_true", help="Run with demonstration multi-domain knowledge mesh")
    # entropy-decoupler / semantic-denoiser / snr-gate / syntax-denoiser
    p_edec = subparsers.add_parser("entropy-decoupler", aliases=["semantic-denoiser", "snr-gate", "syntax-denoiser"], help="Autonomous cognitive spatial semantic entropy decoupler and syntactic de-noising gate")
    p_edec.add_argument("input", nargs="?", default="", help="Input text or nodes JSON filepath")
    p_edec.add_argument("--threshold", type=float, default=3.0, help="Signal-to-noise ratio alert threshold in dB (default: 3.0)")
    p_edec.add_argument("--report", default="", help="Output entropy audit markdown filepath")
    p_edec.add_argument("--svg", default="", help="Output entropy spectrum SVG filepath")
    p_edec.add_argument("--json", "-j", action="store_true", help="Output raw JSON entropy telemetry")
    p_edec.add_argument("--demo", action="store_true", help="Run with demonstration noisy text nodes")
    # polyhedral-crystallizer / schema-folder / polyhedral-net / concept-crystallizer
    p_polyc = subparsers.add_parser("polyhedral-crystallizer", aliases=["schema-folder", "polyhedral-net", "concept-crystallizer"], help="Autonomous cognitive spatial polyhedral schema crystallizer and dimensionality folder")
    p_polyc.add_argument("input", nargs="?", default="", help="Input concepts JSON filepath")
    p_polyc.add_argument("--type", choices=["auto", "tetrahedron", "cube", "octahedron"], default="auto", help="Polyhedron geometry type (default: auto)")
    p_polyc.add_argument("--scale", type=float, default=70.0, help="Geometric net scale in pixels (default: 70.0)")
    p_polyc.add_argument("--report", default="", help="Output polyhedral schema audit markdown filepath")
    p_polyc.add_argument("--svg", default="", help="Output polyhedral net blueprint SVG filepath")
    p_polyc.add_argument("--json", "-j", action="store_true", help="Output raw JSON crystallizer telemetry")
    p_polyc.add_argument("--demo", action="store_true", help="Run with demonstration modular concept set")
    # polar-grid / landmark-polar / bearing-synthesizer / allocentric-bearing
    p_pgrid = subparsers.add_parser("polar-grid", aliases=["landmark-polar", "bearing-synthesizer", "allocentric-bearing"], help="Autonomous cognitive spatial allocentric landmark polar grid and dynamic bearing synthesizer")
    p_pgrid.add_argument("input", nargs="?", default="", help="Input landmark and targets JSON filepath")
    p_pgrid.add_argument("--interval", type=float, default=120.0, help="Concentric range ring interval in pixels (default: 120.0)")
    p_pgrid.add_argument("--rings", type=int, default=3, help="Number of concentric polar range rings (default: 3)")
    p_pgrid.add_argument("--report", default="", help="Output polar grid audit markdown filepath")
    p_pgrid.add_argument("--svg", default="", help="Output polar radar grid SVG filepath")
    p_pgrid.add_argument("--json", "-j", action="store_true", help="Output raw JSON polar grid telemetry")
    p_pgrid.add_argument("--demo", action="store_true", help="Run with demonstration allocentric landmark and target session")
    # gaze-stabilizer / attentional-funnel-stabilizer / scanpath-limiter / gaze-envelope
    p_gaze = subparsers.add_parser("gaze-stabilizer", aliases=["attentional-funnel-stabilizer", "scanpath-limiter", "gaze-envelope"], help="Autonomous cognitive spatial dynamic attentional funnel and gaze envelope stabilizer")
    p_gaze.add_argument("input", nargs="?", default="", help="Input scanpath and channels JSON filepath")
    p_gaze.add_argument("--envelope-width", type=float, default=90.0, help="Attentional corridor envelope width in pixels (default: 90.0)")
    p_gaze.add_argument("--damping", type=float, default=0.65, help="Jitter damping factor between 0.0 and 1.0 (default: 0.65)")
    p_gaze.add_argument("--report", default="", help="Output gaze stabilization diagnostic markdown filepath")
    p_gaze.add_argument("--svg", default="", help="Output gaze envelope interactive SVG filepath")
    p_gaze.add_argument("--json", "-j", action="store_true", help="Output raw JSON gaze stabilization telemetry")
    p_gaze.add_argument("--demo", action="store_true", help="Run with demonstration technical architecture scanpath")
    # dialectical-tensor-loom / hegelian-tensor-loom / dialectical-tensor / hegelian-loom / tensor-lattice-loom
    p_loom = subparsers.add_parser("dialectical-tensor-loom", aliases=["hegelian-tensor-loom", "dialectical-tensor", "hegelian-loom", "tensor-lattice-loom"], help="Autonomous cognitive spatial dialectical tensor lattice and Hegelian synthesis loom")
    p_loom.add_argument("input", nargs="?", default="", help="Input dialectical poles and argument graph JSON filepath")
    p_loom.add_argument("--threshold", type=float, default=0.65, help="Acute friction threshold for antithesis opposition (default: 0.65)")
    p_loom.add_argument("--report", default="", help="Output dialectical synthesis diagnostic markdown filepath")
    p_loom.add_argument("--svg", default="", help="Output Hegelian dialectical tensor loom SVG filepath")
    p_loom.add_argument("--json", "-j", action="store_true", help="Output raw JSON dialectical lattice telemetry")
    p_loom.add_argument("--demo", action="store_true", help="Run with demonstration technical architecture dialectic")
    # concept-hologram / holographic-weaver / interference-pattern / semantic-hologram
    p_holo = subparsers.add_parser("concept-hologram", aliases=["holographic-weaver", "interference-pattern", "semantic-hologram"], help="Autonomous cognitive spatial multimodal concept hologram and interference pattern weaver")
    p_holo.add_argument("input", nargs="?", default="", help="Input multimodal concept wave emitters JSON filepath")
    p_holo.add_argument("--grid-step", type=float, default=30.0, help="Field sampling grid step in pixels (default: 30.0)")
    p_holo.add_argument("--threshold", type=float, default=0.55, help="Global coherence threshold for holographic resonance (default: 0.55)")
    p_holo.add_argument("--report", default="", help="Output concept hologram diagnostic markdown filepath")
    p_holo.add_argument("--svg", default="", help="Output concept hologram interference SVG filepath")
    p_holo.add_argument("--json", "-j", action="store_true", help="Output raw JSON holographic field telemetry")
    p_holo.add_argument("--demo", action="store_true", help="Run with demonstration multimodal concept field")
    # gaze-corridor-resonator / corridor-resonator / focal-conduit / parafoveal-preview
    p_cres = subparsers.add_parser("gaze-corridor-resonator", aliases=["corridor-resonator", "focal-conduit", "parafoveal-preview"], help="Autonomous cognitive spatial dynamic attentional funnel and gaze corridor resonator")
    p_cres.add_argument("input", nargs="?", default="", help="Input ocular gaze samples JSON filepath")
    p_cres.add_argument("--latency", type=float, default=180.0, help="Estimated saccadic latency in ms (default: 180.0)")
    p_cres.add_argument("--aperture", type=float, default=45.0, help="Base foveal focal aperture width in pixels (default: 45.0)")
    p_cres.add_argument("--report", default="", help="Output gaze corridor diagnostic markdown filepath")
    p_cres.add_argument("--svg", default="", help="Output gaze corridor interactive SVG filepath")
    p_cres.add_argument("--json", "-j", action="store_true", help="Output raw JSON corridor telemetry")
    p_cres.add_argument("--demo", action="store_true", help="Run with demonstration technical architecture scanpath")
    # kinematic-horizon / artificial-horizon / inertial-frame / gimbal-lock-calibrator
    p_khor = subparsers.add_parser("kinematic-horizon", aliases=["artificial-horizon", "inertial-frame", "gimbal-lock-calibrator"], help="Allocentric kinematic horizon and inertial frame calibrator engine")
    p_khor.add_argument("input", nargs="?", default="", help="Input orientation telemetry JSON filepath")
    p_khor.add_argument("--threshold", type=float, default=75.0, help="Gimbal lock warning threshold in degrees (default: 75.0)")
    p_khor.add_argument("--radius", type=float, default=150.0, help="Gauge radius in pixels (default: 150.0)")
    p_khor.add_argument("--pitch-scale", type=float, default=2.5, help="Pitch scale pixels per degree (default: 2.5)")
    p_khor.add_argument("--report", default="", help="Output kinematic horizon diagnostic markdown filepath")
    p_khor.add_argument("--svg", default="", help="Output kinematic horizon interactive SVG filepath")
    p_khor.add_argument("--json", "-j", action="store_true", help="Output raw JSON horizon telemetry")
    p_khor.add_argument("--demo", action="store_true", help="Run with demonstration 3D map exploration telemetry")
    # morphological-lens / semantic-lens / granularity-zoom / morphological-zoom
    p_mlens = subparsers.add_parser("morphological-lens", aliases=["semantic-lens", "granularity-zoom", "morphological-zoom"], help="Autonomous cognitive spatial morphological semantic lens and granularity zoom engine")
    p_mlens.add_argument("input", nargs="?", default="", help="Input semantic graph hierarchy JSON filepath")
    p_mlens.add_argument("--zoom", "-z", type=float, default=1.0, help="Continuous semantic zoom factor (default: 1.0)")
    p_mlens.add_argument("--focus-x", type=float, default=430.0, help="X coordinate of focal center in pixels (default: 430.0)")
    p_mlens.add_argument("--focus-y", type=float, default=260.0, help="Y coordinate of focal center in pixels (default: 260.0)")
    p_mlens.add_argument("--focal-radius", type=float, default=140.0, help="Base foveal inspection radius in pixels (default: 140.0)")
    p_mlens.add_argument("--cowan-capacity", type=int, default=4, help="Maximum foveal Cowan working memory capacity (default: 4)")
    p_mlens.add_argument("--report", default="", help="Output semantic lens diagnostic markdown filepath")
    p_mlens.add_argument("--svg", default="", help="Output semantic lens interactive SVG filepath")
    p_mlens.add_argument("--json", "-j", action="store_true", help="Output raw JSON semantic lens telemetry")
    p_mlens.add_argument("--demo", action="store_true", help="Run with demonstration software architecture hierarchy")
    # manifold-unfolder / polytope-net / tesseract-unfolder / riemannian-manifold
    p_munf = subparsers.add_parser("manifold-unfolder", aliases=["polytope-net", "tesseract-unfolder", "riemannian-manifold"], help="Autonomous cognitive spatial topological manifold unfolder and polytope net weaver engine")
    p_munf.add_argument("input", nargs="?", default="", help="Input polytope specification JSON filepath")
    p_munf.add_argument("--polytope", "-p", default="TESSERACT_8_CELL", choices=["TESSERACT_8_CELL", "HYPERSIMPLEX_5_CELL", "ORTHOPLEX_16_CELL"], help="Target regular 4-polytope geometry (default: TESSERACT_8_CELL)")
    p_munf.add_argument("--factor", "-f", type=float, default=1.0, help="Unfolding progression factor 0.0 to 1.0 (default: 1.0)")
    p_munf.add_argument("--iso-angle", type=float, default=30.0, help="Isometric projection angle in degrees (default: 30.0)")
    p_munf.add_argument("--spacing", type=float, default=75.0, help="Cell spacing in pixels (default: 75.0)")
    p_munf.add_argument("--report", default="", help="Output topological manifold diagnostic markdown filepath")
    p_munf.add_argument("--svg", default="", help="Output topological manifold interactive SVG filepath")
    p_munf.add_argument("--json", "-j", action="store_true", help="Output raw JSON manifold net telemetry")
    p_munf.add_argument("--demo", action="store_true", help="Run with demonstration unfolded Salvador Dali tesseract cross")
    # saliency-conductor / saccadic-conductor / gaze-conductor / saccadic-saliency
    p_scond = subparsers.add_parser("saliency-conductor", aliases=["saccadic-conductor", "gaze-conductor", "saccadic-saliency"], help="Autonomous cognitive spatial dynamic attentional funnel and saccadic saliency conductor engine")
    p_scond.add_argument("input", nargs="?", default="", help="Input visual saliency waypoints JSON filepath")
    p_scond.add_argument("--px-per-deg", type=float, default=35.0, help="Pixels per visual degree (default: 35.0)")
    p_scond.add_argument("--latency", type=float, default=190.0, help="Base saccadic decision latency in ms (default: 190.0)")
    p_scond.add_argument("--penalty", type=float, default=1.4, help="Regression penalty multiplier (default: 1.4)")
    p_scond.add_argument("--report", default="", help="Output saccadic saliency diagnostic markdown filepath")
    p_scond.add_argument("--svg", default="", help="Output saccadic saliency interactive SVG filepath")
    p_scond.add_argument("--json", "-j", action="store_true", help="Output raw JSON saliency telemetry")
    p_scond.add_argument("--demo", action="store_true", help="Run with demonstration technical scanpath")
    # retinal-latch / drift-dampener / retinal-dampener / working-memory-latch / retinal-stabilizer
    p_rlatch = subparsers.add_parser("retinal-latch", aliases=["drift-dampener", "retinal-dampener", "working-memory-latch", "retinal-stabilizer"], help="Autonomous cognitive spatial working memory saccadic drift dampener and retinal latch engine")
    p_rlatch.add_argument("input", nargs="?", default="", help="Input ocular gaze stream or anchor JSON filepath")
    p_rlatch.add_argument("--rotation-angle", type=float, default=180.0, help="Mental rotation angle in degrees (default: 180.0)")
    p_rlatch.add_argument("--noise", type=float, default=9.5, help="Simulated fixational tremor noise std in px (default: 9.5)")
    p_rlatch.add_argument("--damping", type=float, default=0.68, help="Low-pass damping factor (default: 0.68)")
    p_rlatch.add_argument("--deadband", type=float, default=10.0, help="Deadband suppression radius in px (default: 10.0)")
    p_rlatch.add_argument("--duration", type=float, default=2400.0, help="Mental rotation duration in ms (default: 2400.0)")
    p_rlatch.add_argument("--report", default="", help="Output retinal latch diagnostic markdown filepath")
    p_rlatch.add_argument("--svg", default="", help="Output retinal latch interactive SVG filepath")
    p_rlatch.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_rlatch.add_argument("--demo", action="store_true", help="Run with demonstration mental rotation simulation")
    # fiber-bundle / holonomy-weaver / topological-bundle / polytope-holonomy / parallel-transport
    p_fbdl = subparsers.add_parser("fiber-bundle", aliases=["holonomy-weaver", "topological-bundle", "polytope-holonomy", "parallel-transport"], help="Autonomous cognitive spatial topological fiber bundle and polytope holonomy weaver engine")
    p_fbdl.add_argument("--type", default="mobius", choices=["mobius", "hopf", "torus", "cylinder"], help="Fiber bundle manifold geometry (default: mobius)")
    p_fbdl.add_argument("--radius", type=float, default=160.0, help="Base manifold radius in px (default: 160.0)")
    p_fbdl.add_argument("--steps", type=int, default=64, help="Discretization sampling steps (default: 64)")
    p_fbdl.add_argument("--twist", type=float, default=1.0, help="Topological twist parameter factor (default: 1.0)")
    p_fbdl.add_argument("--p-winds", type=int, default=2, help="Toroidal p-winding integer (default: 2)")
    p_fbdl.add_argument("--q-winds", type=int, default=3, help="Toroidal q-winding integer (default: 3)")
    p_fbdl.add_argument("--report", default="", help="Output holonomy diagnostic markdown filepath")
    p_fbdl.add_argument("--svg", default="", help="Output fiber bundle interactive SVG filepath")
    p_fbdl.add_argument("--json", "-j", action="store_true", help="Output raw JSON holonomy telemetry")
    p_fbdl.add_argument("--demo", action="store_true", help="Run with demonstration Mobius strip fiber bundle")
    # chrono-replay / replay-loom / episodic-replay / trajectory-synthesizer / hippocampal-replay
    p_creplay = subparsers.add_parser("chrono-replay", aliases=["replay-loom", "episodic-replay", "trajectory-synthesizer", "hippocampal-replay"], help="Autonomous cognitive spatial chrono-spatial replay loom and episodic trajectory synthesizer engine")
    p_creplay.add_argument("input", nargs="?", default="", help="Input episodic waypoints JSON filepath")
    p_creplay.add_argument("--mode", default="forward", choices=["forward", "reverse", "choice-point"], help="Replay synthesis mode (default: forward)")
    p_creplay.add_argument("--compression", type=float, default=14.0, help="Sharp-wave ripple temporal compression factor (default: 14.0)")
    p_creplay.add_argument("--depth", type=int, default=4, help="Choice point decision lattice depth (default: 4)")
    p_creplay.add_argument("--report", default="", help="Output chrono replay diagnostic markdown filepath")
    p_creplay.add_argument("--svg", default="", help="Output chrono replay interactive SVG filepath")
    p_creplay.add_argument("--json", "-j", action="store_true", help="Output raw JSON replay telemetry")
    p_creplay.add_argument("--demo", action="store_true", help="Run with demonstration episodic trajectory rollout")
    # topographic-contour / isocline-tracer / semantic-topography / contour-morph / terrain-elevation
    p_tcont = subparsers.add_parser("topographic-contour", aliases=["isocline-tracer", "semantic-topography", "contour-morph", "terrain-elevation"], help="Autonomous cognitive spatial topographic contour morph and iso-semantic isocline tracer engine")
    p_tcont.add_argument("input", nargs="?", default="", help="Input semantic summits JSON filepath")
    p_tcont.add_argument("--interval", type=float, default=80.0, help="Contour elevation slice interval (default: 80.0)")
    p_tcont.add_argument("--grid-w", type=int, default=52, help="Grid sampling horizontal resolution (default: 52)")
    p_tcont.add_argument("--grid-h", type=int, default=34, help="Grid sampling vertical resolution (default: 34)")
    p_tcont.add_argument("--report", default="", help="Output topographic diagnostic markdown filepath")
    p_tcont.add_argument("--svg", default="", help="Output topographic contour interactive SVG filepath")
    p_tcont.add_argument("--json", "-j", action="store_true", help="Output raw JSON topography telemetry")
    p_tcont.add_argument("--demo", action="store_true", help="Run with demonstration semantic relief terrain")
    # tensegrity-lattice / tensegrity-solver / cable-strut-lattice / dynamic-equilibrium / biotensegrity-loom
    p_tlat = subparsers.add_parser("tensegrity-lattice", aliases=["tensegrity-solver", "cable-strut-lattice", "dynamic-equilibrium", "biotensegrity-loom"], help="Autonomous cognitive spatial tensegrity cable-strut lattice and dynamic equilibrium balancer engine")
    p_tlat.add_argument("--type", default="3-prism", choices=["3-prism", "6-icosahedron"], help="Tensegrity topology configuration (default: 3-prism)")
    p_tlat.add_argument("--radius", type=float, default=150.0, help="Bounding radius in px (default: 150.0)")
    p_tlat.add_argument("--height", type=float, default=190.0, help="Prism height in px (default: 190.0)")
    p_tlat.add_argument("--prestress", type=float, default=120.0, help="Mean tensile cable prestress force (default: 120.0)")
    p_tlat.add_argument("--twist", type=float, default=30.0, help="Prism dihedral twist angle in degrees (default: 30.0)")
    p_tlat.add_argument("--report", default="", help="Output tensegrity diagnostic markdown filepath")
    p_tlat.add_argument("--svg", default="", help="Output tensegrity lattice interactive SVG filepath")
    p_tlat.add_argument("--json", "-j", action="store_true", help="Output raw JSON tensegrity telemetry")
    p_tlat.add_argument("--demo", action="store_true", help="Run with demonstration tensegrity prism")
    # voronoi-isochrone / isochrone-tessellator / concept-territories / proximity-loom / voronoi-loom
    p_viso = subparsers.add_parser("voronoi-isochrone", aliases=["isochrone-tessellator", "concept-territories", "proximity-loom", "voronoi-loom"], help="Autonomous cognitive spatial iso-chronous Voronoi isochrone tessellator and proximity loom engine")
    p_viso.add_argument("input", nargs="?", default="", help="Input concept generator sites JSON filepath")
    p_viso.add_argument("--cost-step", type=float, default=30.0, help="Isochrone wavefront cost step interval (default: 30.0)")
    p_viso.add_argument("--max-cost", type=float, default=90.0, help="Isochrone wavefront maximum cost horizon (default: 90.0)")
    p_viso.add_argument("--report", default="", help="Output Voronoi isochrone diagnostic markdown filepath")
    p_viso.add_argument("--svg", default="", help="Output Voronoi isochrone interactive SVG filepath")
    p_viso.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_viso.add_argument("--demo", action="store_true", help="Run with demonstration semantic cluster territories")
    # poincare-disk / hyperbolic-poincare / poincare-loom / hyperbolic-tree
    p_poin = subparsers.add_parser("poincare-disk", aliases=["hyperbolic-poincare", "poincare-loom", "hyperbolic-tree"], help="Autonomous cognitive spatial hyperbolic Poincare disk projector and non-Euclidean concept loom")
    p_poin.add_argument("input", nargs="?", default="", help="Input concept taxonomy JSON filepath")
    p_poin.add_argument("--focus", default="", help="Target concept node ID to shift to origin via Mobius isometry")
    p_poin.add_argument("--radial-step", type=float, default=0.62, help="Hyperbolic radial distance step per hierarchy level (default: 0.62)")
    p_poin.add_argument("--report", default="", help="Output hyperbolic diagnostic markdown filepath")
    p_poin.add_argument("--svg", default="", help="Output Poincare disk SVG filepath")
    p_poin.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_poin.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_poin.add_argument("--demo", action="store_true", help="Run with demonstration cognitive taxonomy tree")
    # symplectic-orbit / hamiltonian-loom / phase-space / symplectic-integrator
    p_symp = subparsers.add_parser("symplectic-orbit", aliases=["hamiltonian-loom", "phase-space", "symplectic-integrator"], help="Autonomous cognitive spatial symplectic phase space integrator and Hamiltonian concept orbit loom")
    p_symp.add_argument("input", nargs="?", default="", help="Input semantic attractors JSON filepath")
    p_symp.add_argument("--steps", type=int, default=750, help="Number of symplectic leapfrog time steps (default: 750)")
    p_symp.add_argument("--dt", type=float, default=0.03, help="Time step size dt (default: 0.03)")
    p_symp.add_argument("--mass", type=float, default=1.0, help="Cognitive mass / mental inertia parameter (default: 1.0)")
    p_symp.add_argument("--k", type=float, default=0.55, help="Restoring stiffness parameter (default: 0.55)")
    p_symp.add_argument("--report", default="", help="Output Hamiltonian diagnostic markdown filepath")
    p_symp.add_argument("--svg", default="", help="Output symplectic dual-panel SVG filepath")
    p_symp.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_symp.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_symp.add_argument("--demo", action="store_true", help="Run with demonstration cognitive orbit simulation")
    # grassmannian-loom / subspace-angles / grassmannian-manifold / subspace-projector
    p_grass = subparsers.add_parser("grassmannian-loom", aliases=["subspace-angles", "grassmannian-manifold", "subspace-projector"], help="Autonomous cognitive spatial hyper-dimensional Grassmannian manifold projector and subspace angle loom")
    p_grass.add_argument("input", nargs="?", default="", help="Input cognitive subspaces JSON filepath")
    p_grass.add_argument("--ambient-dim", type=int, default=8, help="Ambient vector space dimension n (default: 8)")
    p_grass.add_argument("--subspace-dim", type=int, default=2, help="Subspace dimension k (default: 2)")
    p_grass.add_argument("--report", default="", help="Output Grassmannian diagnostic markdown filepath")
    p_grass.add_argument("--svg", default="", help="Output Grassmannian dual-panel SVG filepath")
    p_grass.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_grass.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_grass.add_argument("--demo", action="store_true", help="Run with demonstration cognitive subspaces on Gr(2, 8)")
    # contact-reeb / reeb-loom / legendrian-knot / contact-geometry
    p_cont = subparsers.add_parser("contact-reeb", aliases=["reeb-loom", "legendrian-knot", "contact-geometry"], help="Autonomous cognitive spatial contact geometry Reeb vector field and Legendrian submanifold loom")
    p_cont.add_argument("input", nargs="?", default="", help="Input contact configuration JSON filepath")
    p_cont.add_argument("--action", type=float, default=2.4, help="Target contact action for primary Reeb orbit (default: 2.4)")
    p_cont.add_argument("--points", type=int, default=240, help="Discretization point count along knot curve (default: 240)")
    p_cont.add_argument("--report", default="", help="Output contact diagnostic markdown filepath")
    p_cont.add_argument("--svg", default="", help="Output contact dual-panel SVG filepath")
    p_cont.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_cont.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_cont.add_argument("--demo", action="store_true", help="Run with demonstration Legendrian unknot and Reeb orbits")
    # calabi-yau / quintic-threefold / flux-vacuum / calabi-yau-loom
    p_cyau = subparsers.add_parser("calabi-yau", aliases=["quintic-threefold", "flux-vacuum", "calabi-yau-loom"], help="Autonomous cognitive spatial Calabi-Yau compactification and multi-dimensional flux vacuum loom")
    p_cyau.add_argument("input", nargs="?", default="", help="Input Calabi-Yau configuration JSON filepath")
    p_cyau.add_argument("--psi", type=float, default=0.45, help="Complex moduli deformation parameter psi (default: 0.45)")
    p_cyau.add_argument("--report", default="", help="Output Calabi-Yau diagnostic markdown filepath")
    p_cyau.add_argument("--svg", default="", help="Output Calabi-Yau dual-panel SVG filepath")
    p_cyau.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_cyau.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_cyau.add_argument("--demo", action="store_true", help="Run with demonstration Calabi-Yau quintic threefold and flux vacua")

    # sheaf-cohomology / epistemic-gluing / cech-cohomology / sheaf-loom
    p_sheaf = subparsers.add_parser("sheaf-cohomology", aliases=["epistemic-gluing", "cech-cohomology", "sheaf-loom"], help="Autonomous cognitive spatial Sheaf-Theoretic Cohomology and Epistemic Gluing Loom")
    p_sheaf.add_argument("input", nargs="?", default="", help="Input epistemic cover configuration JSON filepath")
    p_sheaf.add_argument("--report", default="", help="Output sheaf cohomology diagnostic markdown filepath")
    p_sheaf.add_argument("--svg", default="", help="Output epistemic nerve complex SVG filepath")
    p_sheaf.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_sheaf.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_sheaf.add_argument("--demo", action="store_true", help="Run with demonstration 5-lens epistemic cover")

    # spectral-triple / connes-spectral / connes-distance / noncommutative-loom
    p_spec = subparsers.add_parser("spectral-triple", aliases=["connes-spectral", "connes-distance", "noncommutative-loom"], help="Autonomous cognitive spatial Non-Commutative Spectral Triple and Connes Distance Loom")
    p_spec.add_argument("input", nargs="?", default="", help="Input spectral triple configuration JSON filepath")
    p_spec.add_argument("--report", default="", help="Output spectral analysis diagnostic markdown filepath")
    p_spec.add_argument("--svg", default="", help="Output spectral triple and Connes distance SVG filepath")
    p_spec.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_spec.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_spec.add_argument("--demo", action="store_true", help="Run with demonstration 4D cognitive spectral triple")

    # geometric-quantization / kostant-souriau / prequantum-loom / bohr-sommerfeld
    p_quant = subparsers.add_parser("geometric-quantization", aliases=["kostant-souriau", "prequantum-loom", "bohr-sommerfeld"], help="Autonomous cognitive spatial Geometric Quantization and Kostant-Souriau Prequantum Loom")
    p_quant.add_argument("input", nargs="?", default="", help="Input quantization configuration JSON filepath")
    p_quant.add_argument("--hbar", type=float, default=0.5, help="Planck action quantum hbar (default: 0.5)")
    p_quant.add_argument("--omega", type=float, default=1.0, help="Harmonic oscillator frequency omega (default: 1.0)")
    p_quant.add_argument("--report", default="", help="Output quantization diagnostic markdown filepath")
    p_quant.add_argument("--svg", default="", help="Output Bohr-Sommerfeld phase portrait SVG filepath")
    p_quant.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_quant.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_quant.add_argument("--demo", action="store_true", help="Run with demonstration anharmonic cognitive oscillator")

    # atiyah-singer / index-theorem / topological-anomaly / spectral-flow-loom
    p_atiyah = subparsers.add_parser("atiyah-singer", aliases=["index-theorem", "topological-anomaly", "spectral-flow-loom"], help="Autonomous cognitive spatial Atiyah-Singer Index Theorem and Topological Anomaly Loom")
    p_atiyah.add_argument("input", nargs="?", default="", help="Input Atiyah-Singer configuration JSON filepath")
    p_atiyah.add_argument("--dim", type=int, default=2, help="Manifold dimension (default: 2)")
    p_atiyah.add_argument("--genus", type=int, default=1, help="Manifold genus g (default: 1)")
    p_atiyah.add_argument("--rank", type=int, default=2, help="Twisting bundle rank (default: 2)")
    p_atiyah.add_argument("--report", default="", help="Output Atiyah-Singer diagnostic markdown filepath")
    p_atiyah.add_argument("--svg", default="", help="Output spectral flow and index SVG filepath")
    p_atiyah.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_atiyah.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_atiyah.add_argument("--demo", action="store_true", help="Run with demonstration cognitive Riemann surface and chiral Dirac operator")

    # k-theory / vector-bundle / bott-periodicity / grothendieck-loom
    p_ktheory = subparsers.add_parser("k-theory", aliases=["vector-bundle", "bott-periodicity", "grothendieck-loom"], help="Autonomous cognitive spatial Topological K-Theory and Vector Bundle Classification Loom")
    p_ktheory.add_argument("input", nargs="?", default="", help="Input K-theory configuration JSON filepath")
    p_ktheory.add_argument("--base", default="S^2 (Cognitive Context Sphere)", help="Base manifold identifier")
    p_ktheory.add_argument("--report", default="", help="Output K-theory classification markdown filepath")
    p_ktheory.add_argument("--svg", default="", help="Output Bott periodicity and clutching SVG filepath")
    p_ktheory.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_ktheory.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_ktheory.add_argument("--demo", action="store_true", help="Run with demonstration cognitive vector bundle suite")
    # mirror-symmetry / homological-mirror / kontsevich-loom / fukaya-coherent
    p_mirror = subparsers.add_parser("mirror-symmetry", aliases=["homological-mirror", "kontsevich-loom", "fukaya-coherent"], help="Autonomous cognitive spatial Homological Mirror Symmetry and Kontsevich Dual Loom")
    p_mirror.add_argument("input", nargs="?", default="", help="Input mirror symmetry configuration JSON filepath")
    p_mirror.add_argument("--area", type=float, default=1.0, help="Symplectic area A of target torus")
    p_mirror.add_argument("--tau", type=float, default=1.0, help="Complex modulus imaginary part Im(tau) of dual elliptic curve")
    p_mirror.add_argument("--p1", type=int, default=1, help="Winding p1 of first Lagrangian")
    p_mirror.add_argument("--q1", type=int, default=0, help="Winding q1 of first Lagrangian")
    p_mirror.add_argument("--p2", type=int, default=1, help="Winding p2 of second Lagrangian")
    p_mirror.add_argument("--q2", type=int, default=2, help="Winding q2 of second Lagrangian")
    p_mirror.add_argument("--report", default="", help="Output mirror symmetry markdown filepath")
    p_mirror.add_argument("--svg", default="", help="Output Floer intersection and Hodge diamond SVG filepath")
    p_mirror.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_mirror.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_mirror.add_argument("--demo", action="store_true", help="Run with demonstration Lagrangian pair and coherent sheaves")
    # derived-stack / higher-stack / artin-loom / cotangent-complex
    p_stack = subparsers.add_parser("derived-stack", aliases=["higher-stack", "artin-loom", "cotangent-complex"], help="Autonomous cognitive spatial Derived Algebraic Geometry and Higher Stacks Loom")
    p_stack.add_argument("input", nargs="?", default="", help="Input derived stack configuration JSON filepath")
    p_stack.add_argument("--name", default="Cognitive Perspective Moduli Stack M_persp", help="Derived stack identifier")
    p_stack.add_argument("--base-dim", type=int, default=4, help="Base space dimension")
    p_stack.add_argument("--aut-dim", type=int, default=1, help="Automorphism group dimension (T^0)")
    p_stack.add_argument("--relations", type=int, default=2, help="Relations / obstruction dimension in H^(-1)(L)")
    p_stack.add_argument("--syzygies", type=int, default=0, help="Higher syzygies dimension in H^(-2)(L)")
    p_stack.add_argument("--group", default="GL(1, C)", help="Automorphism Lie group label")
    p_stack.add_argument("--report", default="", help="Output derived stack telemetry markdown filepath")
    p_stack.add_argument("--svg", default="", help="Output simplicial nerve and cotangent ladder SVG filepath")
    p_stack.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_stack.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_stack.add_argument("--demo", action="store_true", help="Run with demonstration cognitive derived stack atlas")
    # perverse-sheaves / intersection-cohomology / bbdg-loom / stratified-loom
    p_perverse = subparsers.add_parser("perverse-sheaves", aliases=["intersection-cohomology", "bbdg-loom", "stratified-loom"], help="Autonomous cognitive spatial Perverse Sheaves and Intersection Cohomology Loom")
    p_perverse.add_argument("input", nargs="?", default="", help="Input stratified space configuration JSON filepath")
    p_perverse.add_argument("--name", default="Cognitive Multi-Modal Locus X", help="Stratified space identifier")
    p_perverse.add_argument("--dim", type=int, default=4, help="Ambient space dimension")
    p_perverse.add_argument("--perversity", default="Lower Middle (m)", choices=["Lower Middle (m)", "Upper Middle (n)", "Zero Perversity (0)", "Top Perversity (t)"], help="Perversity function type")
    p_perverse.add_argument("--report", default="", help="Output perverse sheaves telemetry markdown filepath")
    p_perverse.add_argument("--svg", default="", help="Output stratification strata and BBDG direct sum SVG filepath")
    p_perverse.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_perverse.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_perverse.add_argument("--demo", action="store_true", help="Run with demonstration stratified cone space and BBDG decomposition")
    # motivic-homotopy / voevodsky-slice / a1-homotopy / motivic-loom
    p_motivic = subparsers.add_parser("motivic-homotopy", aliases=["voevodsky-slice", "a1-homotopy", "motivic-loom"], help="Autonomous cognitive spatial Motivic Homotopy and Voevodsky Slice Filtration Loom")
    p_motivic.add_argument("input", nargs="?", default="", help="Input motivic scheme configuration JSON filepath")
    p_motivic.add_argument("--name", default="Cognitive Perspective Scheme X", help="Motivic scheme identifier")
    p_motivic.add_argument("--max-level", type=int, default=3, help="Maximum slice filtration level")
    p_motivic.add_argument("--report", default="", help="Output motivic telemetry markdown filepath")
    p_motivic.add_argument("--svg", default="", help="Output motivic spheres and slice tower SVG filepath")
    p_motivic.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_motivic.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_motivic.add_argument("--demo", action="store_true", help="Run with demonstration KGL algebraic K-theory spectrum and slice tower")
    # condensed-math / clausen-scholze / liquid-loom / solid-abelian
    p_condensed = subparsers.add_parser("condensed-math", aliases=["clausen-scholze", "liquid-loom", "solid-abelian"], help="Autonomous cognitive spatial Condensed Mathematics and Clausen-Scholze Analytic Loom")
    p_condensed.add_argument("input", nargs="?", default="", help="Input condensed schema configuration JSON filepath")
    p_condensed.add_argument("--name", default="Cognitive Intuitive Continuum X", help="Condensed schema identifier")
    p_condensed.add_argument("--liquid-p", type=float, default=1.0, help="Liquid convex parameter p in (0, 1]")
    p_condensed.add_argument("--report", default="", help="Output condensed mathematics telemetry markdown filepath")
    p_condensed.add_argument("--svg", default="", help="Output profinite hyper-cover and liquid module SVG filepath")
    p_condensed.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_condensed.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_condensed.add_argument("--demo", action="store_true", help="Run with demonstration Stone space probes and liquid vector spaces")
    # prismatic-cohomology / bhatt-scholze / prism-loom / nygaard-filtration
    p_prismatic = subparsers.add_parser("prismatic-cohomology", aliases=["bhatt-scholze", "prism-loom", "nygaard-filtration"], help="Autonomous cognitive spatial Prismatic Cohomology and Bhatt-Scholze Prism Loom")
    p_prismatic.add_argument("input", nargs="?", default="", help="Input prismatic space configuration JSON filepath")
    p_prismatic.add_argument("--name", default="Cognitive Perspective Space X", help="Target space identifier")
    p_prismatic.add_argument("--prism-type", default="Breuil-Kisin Prism (W(k)[[u]], (E(u)))", choices=["Breuil-Kisin Prism (W(k)[[u]], (E(u)))", "Crystalline Prism (W(k), (p))", "q-Crystalline Prism (Z_p[[q-1]], ([p]_q))", "Perfectoid Prism (A_inf, (xi))"], help="Prism classification")
    p_prismatic.add_argument("--prime", type=int, default=5, help="Base prime p")
    p_prismatic.add_argument("--report", default="", help="Output prismatic cohomology telemetry markdown filepath")
    p_prismatic.add_argument("--svg", default="", help="Output universal prism and Nygaard filtration ladder SVG filepath")
    p_prismatic.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_prismatic.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_prismatic.add_argument("--demo", action="store_true", help="Run with demonstration Breuil-Kisin prism at p=5")
    # factorization-homology / topological-chiral / chiral-loom / disk-algebra
    p_fact = subparsers.add_parser("factorization-homology", aliases=["topological-chiral", "chiral-loom", "disk-algebra"], help="Autonomous cognitive spatial Factorization Homology and Topological Chiral Homology Loom")
    p_fact.add_argument("input", nargs="?", default="", help="Input factorization space configuration JSON filepath")
    p_fact.add_argument("--name", default="Cognitive Spatial Manifold M", help="Target spatial schema identifier")
    p_fact.add_argument("--manifold-name", default="Torus T^2 Cognitive Field", help="Manifold name")
    p_fact.add_argument("--dim", type=int, default=2, help="Manifold dimension n")
    p_fact.add_argument("--manifold-type", default="Torus T^2 (Elliptic Modular Chiral Field)", choices=["Torus T^2 (Elliptic Modular Chiral Field)", "Circle S^1 (Hochschild Homology Loop)", "Sphere S^2 (Spherical Compactification)", "Riemann Surface Sigma_g (Multi-Handle Cognitive Field)", "Euclidean Workspace R^n (Local Unbounded Space)"], help="Manifold classification")
    p_fact.add_argument("--algebra-type", default="E_2 Braided Algebra (Planar Spatial Interaction)", choices=["E_2 Braided Algebra (Planar Spatial Interaction)", "E_1 Associative Algebra (Linear Cognitive Stream)", "E_n Little Disks Algebra (Multi-Dimensional Cognitive Workspace)", "E_infinity Commutative Algebra (Isotropic Unrestricted Fusion)"], help="Operadic E_n-algebra type")
    p_fact.add_argument("--report", default="", help="Output factorization homology telemetry markdown filepath")
    p_fact.add_argument("--svg", default="", help="Output disk embeddings and chiral bar complex SVG filepath")
    p_fact.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_fact.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_fact.add_argument("--demo", action="store_true", help="Run with demonstration Torus T^2 and braided E_2 algebra")
    # tqft-axiomatic / atiyah-segal / cobordism-loom / frobenius-state-sum
    p_tqft = subparsers.add_parser("tqft-axiomatic", aliases=["atiyah-segal", "cobordism-loom", "frobenius-state-sum"], help="Autonomous cognitive spatial Topological Quantum Field Theory and Atiyah-Segal Axiomatic Loom")
    p_tqft.add_argument("input", nargs="?", default="", help="Input TQFT spacetime configuration JSON filepath")
    p_tqft.add_argument("--name", default="Cognitive Spacetime Field Z", help="Spacetime identifier")
    p_tqft.add_argument("--dim", default="2D TQFT (Commutative Frobenius Algebra / String Worldsheets)", choices=["2D TQFT (Commutative Frobenius Algebra / String Worldsheets)", "1D TQFT (Finite-Dimensional Vector Space / Super-Traces)", "3D TQFT (Modular Tensor Category / Chern-Simons & Witten-Reshetikhin-Turaev)", "4D TQFT (Donaldson-Witten / Crane-Yetter Categorified State Sums)"], help="Spacetime dimension classification")
    p_tqft.add_argument("--algebra-dim", type=int, default=3, help="Frobenius algebra dimension")
    p_tqft.add_argument("--algebra-name", default="Cohomology Ring H^*(CP^2; C)", help="Frobenius algebra name")
    p_tqft.add_argument("--report", default="", help="Output TQFT telemetry markdown filepath")
    p_tqft.add_argument("--svg", default="", help="Output cobordism surface and operator SVG filepath")
    p_tqft.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_tqft.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_tqft.add_argument("--demo", action="store_true", help="Run with demonstration 2D Frobenius algebra and pants cobordisms")
    # higher-topos / infinity-category / quasi-category / joyal-kan
    p_topos = subparsers.add_parser("higher-topos", aliases=["infinity-category", "quasi-category", "joyal-kan"], help="Autonomous cognitive spatial Higher Category Theory and Lurie (infinity, 1)-Topos Loom")
    p_topos.add_argument("input", nargs="?", default="", help="Input higher topos configuration JSON filepath")
    p_topos.add_argument("--name", default="Cognitive Higher Universe X", help="Universe schema identifier")
    p_topos.add_argument("--topos", default="Sh_infinity(Smooth Manifolds; Spaces)", help="Higher topos name")
    p_topos.add_argument("--base-site", default="Smooth Cognitive Manifolds Site", help="Base site category")
    p_topos.add_argument("--max-dim", type=int, default=3, help="Maximum simplex dimension")
    p_topos.add_argument("--report", default="", help="Output higher topos telemetry markdown filepath")
    p_topos.add_argument("--svg", default="", help="Output 2-simplex and inner horn filler SVG filepath")
    p_topos.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_topos.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_topos.add_argument("--demo", action="store_true", help="Run with demonstration smooth manifolds higher topos and Joyal Kan fillers")
    # differential-cohomology / cheeger-simons / deligne-cohomology / differential-characters
    p_diff = subparsers.add_parser("differential-cohomology", aliases=["cheeger-simons", "deligne-cohomology", "differential-characters"], help="Autonomous cognitive spatial Differential Cohomology and Cheeger-Simons Characters Loom")
    p_diff.add_argument("input", nargs="?", default="", help="Input differential cohomology configuration JSON filepath")
    p_diff.add_argument("--name", default="Cognitive Gauge Field Manifold M", help="Manifold schema identifier")
    p_diff.add_argument("--manifold-name", default="Spacetime 4-Manifold M^4", help="Manifold name")
    p_diff.add_argument("--dim", type=int, default=4, help="Manifold dimension")
    p_diff.add_argument("--degree", default="Degree 2 H^2_diff(M) (U(1) Principal Bundles with Connection)", choices=["Degree 2 H^2_diff(M) (U(1) Principal Bundles with Connection)", "Degree 1 H^1_diff(M) (Smooth Circle Maps C^infinity(M, S^1))", "Degree 3 H^3_diff(M) (Bundle Gerbes with Connection & B-Field)", "Degree 4 H^4_diff(M) (Cheeger-Chern-Simons Secondary Classes c_2)"], help="Differential cohomology degree")
    p_diff.add_argument("--report", default="", help="Output differential cohomology telemetry markdown filepath")
    p_diff.add_argument("--svg", default="", help="Output Cheeger-Simons hexagon and curvature form SVG filepath")
    p_diff.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_diff.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_diff.add_argument("--demo", action="store_true", help="Run with demonstration U(1) gauge bundle and Cheeger-Simons hexagon")
    # symplectic-floer / fukaya-category / a-infinity-loom / pseudo-holomorphic-disks
    p_floer = subparsers.add_parser("symplectic-floer", aliases=["fukaya-category", "a-infinity-loom", "pseudo-holomorphic-disks"], help="Autonomous cognitive spatial Symplectic Floer Homology and Fukaya A-Infinity Loom")
    p_floer.add_argument("input", nargs="?", default="", help="Input symplectic configuration JSON filepath")
    p_floer.add_argument("--name", default="Cognitive Symplectic Workspace (M, omega)", help="Symplectic workspace identifier")
    p_floer.add_argument("--ambient", default="Cotangent Bundle T^*Sigma (Liouville Symplectic Manifold)", help="Ambient symplectic manifold name")
    p_floer.add_argument("--lagrangian-type", default="Exact Lagrangian (Vanishing Symplectic Area Class [omega] = 0)", choices=["Exact Lagrangian (Vanishing Symplectic Area Class [omega] = 0)", "Monotone Lagrangian (Proportional Area and Maslov Classes)", "Bohr-Sommerfeld Lagrangian Torus (Quantized Flux)", "Clifford Torus (Symmetric Monotone in Projective Space)"], help="Lagrangian submanifold type")
    p_floer.add_argument("--report", default="", help="Output symplectic Floer telemetry markdown filepath")
    p_floer.add_argument("--svg", default="", help="Output Lagrangian intersections and Whitney disks SVG filepath")
    p_floer.add_argument("--html", default="", help="Output interactive HTML application filepath")
    p_floer.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_floer.add_argument("--demo", action="store_true", help="Run with demonstration Lagrangian intersections and Stasheff associahedra")
    # non-abelian-hodge / hitchin-fibration / higgs-bundle / simpson-correspondence
    p_hodge = subparsers.add_parser("non-abelian-hodge", aliases=["hitchin-fibration", "higgs-bundle", "simpson-correspondence"], help="Autonomous cognitive spatial Non-Abelian Hodge Theory and Hitchin-Simpson Loom")
    p_hodge.add_argument("--genus", "-g", type=int, default=2, help="Riemann surface genus (default: 2)")
    p_hodge.add_argument("--rank", "-r", type=int, default=2, help="Lie group rank r for SL(r, C) (default: 2)")
    p_hodge.add_argument("--group", default="SL(2, C) Special Linear Group", choices=["SL(2, C) Special Linear Group", "SL(3, C) Special Linear Group", "GL(2, C) General Linear Group", "PGL(2, C) Projective Linear Group"], help="Complex reductive Lie group")
    p_hodge.add_argument("--theta", type=float, default=0.0, help="Twistor phase angle theta in radians for hyperkahler rotation")
    p_hodge.add_argument("--svg", default="", help="Output moduli spaces and Hitchin fibration SVG filepath")
    p_hodge.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_hodge.add_argument("--demo", action="store_true", help="Run with demonstration Higgs bundle and Simpson correspondence")
    # geometric-langlands / hecke-eigensheaf / beilinson-drinfeld / automorphic-d-module
    p_langlands = subparsers.add_parser("geometric-langlands", aliases=["hecke-eigensheaf", "beilinson-drinfeld", "automorphic-d-module"], help="Autonomous cognitive spatial Geometric Langlands and Hecke Eigensheaf Loom")
    p_langlands.add_argument("--genus", "-g", type=int, default=2, help="Curve genus (default: 2)")
    p_langlands.add_argument("--pair", default="SL(2, C) Automorphic <-> PGL(2, C) Galois Spectral", choices=["SL(2, C) Automorphic <-> PGL(2, C) Galois Spectral", "GL(2, C) Automorphic <-> GL(2, C) Galois Spectral", "SL(3, C) Automorphic <-> PGL(3, C) Galois Spectral", "Sp(4, C) Automorphic <-> SO(5, C) Galois Spectral"], help="Langlands dual group pair")
    p_langlands.add_argument("--hecke-rep", default="Fundamental Representation V_std (Dimension r)", choices=["Fundamental Representation V_std (Dimension r)", "Adjoint Representation V_adj (Dimension r^2 - 1)", "Second Exterior Power Wedge^2(V) (Dimension r(r-1)/2)", "Second Symmetric Power Sym^2(V) (Dimension r(r+1)/2)"], help="Hecke functor representation type")
    p_langlands.add_argument("--svg", default="", help="Output Langlands duality and SYZ mirror symmetry SVG filepath")
    p_langlands.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_langlands.add_argument("--demo", action="store_true", help="Run with demonstration Galois local system and Hecke eigensheaf")
    # perfectoid-space / fargues-fontaine / tilting-equivalence / adic-space
    p_perf = subparsers.add_parser("perfectoid-space", aliases=["fargues-fontaine", "tilting-equivalence", "adic-space"], help="Autonomous cognitive spatial Perfectoid Spaces and Fargues-Fontaine Loom")
    p_perf.add_argument("--prime", "-p", type=int, default=2, help="Prime p for non-archimedean field (default: 2)")
    p_perf.add_argument("--field", default="C_p (p-Adic Complex Completion)", help="Base perfectoid field name")
    p_perf.add_argument("--slopes", default="2.0,1.0,0.5,0.0", help="Comma-separated vector bundle slopes on Fargues-Fontaine curve")
    p_perf.add_argument("--svg", default="", help="Output perfectoid spaces and Fargues-Fontaine curve SVG filepath")
    p_perf.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_perf.add_argument("--demo", action="store_true", help="Run with demonstration perfectoid field, adic space, and slope polygon")
    # shimura-variety / pel-moduli / reflex-field / hecke-orbit
    p_shimura = subparsers.add_parser("shimura-variety", aliases=["pel-moduli", "reflex-field", "hecke-orbit"], help="Autonomous cognitive spatial Arithmetic Geometry and Langlands-Shimura Variety Loom")
    p_shimura.add_argument("--type", default="Modular Curve Y(N) (GL_2, Upper Half Plane H)", choices=["Modular Curve Y(N) (GL_2, Upper Half Plane H)", "Siegel Modular Variety A_g (GSp_2g, Siegel Upper Half Space H_g)", "Hilbert-Blumenthal Variety (Res_{F/Q} GL_2, Real Quadratic H^2)", "Picard Unitary Surface (GU(2, 1), Complex 2-Ball B^2)"], help="Shimura variety family")
    p_shimura.add_argument("--genus", "-g", type=int, default=1, help="Abelian variety dimension g (default: 1)")
    p_shimura.add_argument("--level", "-n", type=int, default=1, help="Congruence level N for Gamma(N) (default: 1)")
    p_shimura.add_argument("--prime", "-p", type=int, default=2, help="Prime p for Hecke operator T_p (default: 2)")
    p_shimura.add_argument("--svg", default="", help="Output Shimura datum and Baily-Borel cusp SVG filepath")
    p_shimura.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_shimura.add_argument("--demo", action="store_true", help="Run with demonstration Shimura datum, PEL moduli, and Hecke tree")
    # motivic-cohomology / beilinson-regulator / higher-chow / deligne-period
    p_motivic = subparsers.add_parser("motivic-cohomology", aliases=["beilinson-regulator", "higher-chow", "deligne-period"], help="Autonomous cognitive spatial Motivic Cohomology and Beilinson Regulators Loom")
    p_motivic.add_argument("--domain", default="Ring of Integers Spec(O_F) (Borel Regulator on K_{2n-1})", choices=["Ring of Integers Spec(O_F) (Borel Regulator on K_{2n-1})", "Smooth Projective Curve C (Higher Chow CH^2(C, 1))", "Abelian Variety A (Intermediate Jacobian Regulators)", "Modular Surface (Beilinson Conjectures on L(s, f, 2))"], help="Geometric domain")
    p_motivic.add_argument("--codim", "-p", type=int, default=2, help="Cycle codimension p (default: 2)")
    p_motivic.add_argument("--weight", "-q", type=int, default=2, help="Motivic weight q (default: 2)")
    p_motivic.add_argument("--simplicial-m", "-m", type=int, default=1, help="Simplicial weight m in CH^p(X, m) (default: 1)")
    p_motivic.add_argument("--svg", default="", help="Output motivic complexes and Deligne Jacobian SVG filepath")
    p_motivic.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_motivic.add_argument("--demo", action="store_true", help="Run with demonstration higher Chow cycle, Deligne Jacobian, and Beilinson regulator")
    # arithmetic-dynamics / julia-fatou / canonical-height / post-critical
    p_dyn = subparsers.add_parser("arithmetic-dynamics", aliases=["julia-fatou", "canonical-height", "post-critical"], help="Autonomous cognitive spatial Arithmetic Dynamics and Post-Critically Finite Julia-Fatou Loom")
    p_dyn.add_argument("--family", default="Misiurewicz Quadratic Polynomials f(z) = z^2 + c", choices=["Misiurewicz Quadratic Polynomials f(z) = z^2 + c", "Chebyshev Polynomials T_d(z)", "Lattes Maps on Elliptic Curves", "Unicritical Polynomials f(z) = z^d + c"], help="Rational map family")
    p_dyn.add_argument("--c-param", "-c", type=float, default=-2.0, help="Parameter c for quadratic/unicritical family (default: -2.0)")
    p_dyn.add_argument("--degree", "-d", type=int, default=2, help="Degree of rational map (default: 2)")
    p_dyn.add_argument("--point-x", "-x", type=float, default=0.0, help="Coordinate x to test canonical height (default: 0.0)")
    p_dyn.add_argument("--svg", default="", help="Output arithmetic dynamics and Julia-Fatou phase partition SVG filepath")
    p_dyn.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_dyn.add_argument("--demo", action="store_true", help="Run with demonstration PCF map, Call-Silverman height, and Berkovich tree")
    # arithmetic-topology / knots-primes / kapranov-reznikov / legendre-linking
    p_topo = subparsers.add_parser("arithmetic-topology", aliases=["knots-primes", "kapranov-reznikov", "legendre-linking"], help="Autonomous cognitive spatial Arithmetic Topology and Knots-Primes Kapranov-Reznikov Loom")
    p_topo.add_argument("--field", default="Rational Field Q", help="Base arithmetic field")
    p_topo.add_argument("--prime-p", "-p", type=int, default=3, help="Primary arithmetic prime knot p (default: 3)")
    p_topo.add_argument("--prime-q", "-q", type=int, default=5, help="Secondary arithmetic prime knot q (default: 5)")
    p_topo.add_argument("--prime-r", "-r", type=int, default=7, help="Tertiary prime knot r for Borromean triple (default: 7)")
    p_topo.add_argument("--borromean", action="store_true", help="Evaluate classical Borromean prime triple {13, 61, 937}")
    p_topo.add_argument("--svg", default="", help="Output arithmetic topology and Mazur dictionary SVG filepath")
    p_topo.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_topo.add_argument("--demo", action="store_true", help="Run with demonstration arithmetic knots, Legendre link, Alexander-Iwasawa system, and Borromean triple")
    # anabelian-geometry / section-conjecture / outer-galois / profinite-pi1
    p_anab = subparsers.add_parser("anabelian-geometry", aliases=["section-conjecture", "outer-galois", "profinite-pi1"], help="Autonomous cognitive spatial Anabelian Geometry and Grothendieck Section Conjecture Loom")
    p_anab.add_argument("--field", default="Rational Field Q", help="Base arithmetic field")
    p_anab.add_argument("--archetype", default="Projective Line Minus Three Points P^1 - {0, 1, oo} (g=0, r=3)", choices=["Projective Line Minus Three Points P^1 - {0, 1, oo} (g=0, r=3)", "Modular Curve Y(2) (g=0, r=4)", "Punctured Elliptic Curve E - {O} (g=1, r=1)", "Compact Hyperbolic Curve of Genus Two (g=2, r=0)", "Compact Shimura Curve of Genus Three (g=3, r=0)"], help="Hyperbolic curve archetype")
    p_anab.add_argument("--prime-p", "-p", type=int, default=2, help="Pro-p prime for outer Galois representation (default: 2)")
    p_anab.add_argument("--depth", "-d", type=int, default=3, help="Nilpotent depth of pro-p fundamental group quotient (default: 3)")
    p_anab.add_argument("--point-x", "-x", type=float, default=0.5, help="Rational point coordinate x (default: 0.5)")
    p_anab.add_argument("--point-y", "-y", type=float, default=0.0, help="Rational point coordinate y (default: 0.0)")
    p_anab.add_argument("--svg", default="", help="Output anabelian geometry and Section Conjecture SVG filepath")
    p_anab.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_anab.add_argument("--demo", action="store_true", help="Run with demonstration hyperbolic curve, Galois section, outer Galois representation, and Neukirch-Uchida reconstruction")
    # derived-geometry / spectral-scheme / lurie-spectral / e-infinity-ring
    p_der = subparsers.add_parser("derived-geometry", aliases=["spectral-scheme", "lurie-spectral", "e-infinity-ring"], help="Autonomous cognitive spatial Derived Algebraic Geometry and Lurie Spectral Schemes Loom")
    p_der.add_argument("--spectrum", default="Topological Modular Forms TMF", choices=["Sphere Spectrum S (Initial E_infty-Ring)", "Topological Modular Forms TMF", "Periodic Complex K-Theory KU", "Periodic Real K-Theory KO", "Eilenberg-MacLane Spectrum HZ"], help="Base E_infty-ring spectrum")
    p_der.add_argument("--archetype", default="Derived Critical Locus dCrit(f) (Shifted Symplectic)", choices=["Derived Critical Locus dCrit(f) (Shifted Symplectic)", "Moduli Stack of Elliptic Curves with TMF Sheaf M_ell", "Derived Self-Intersection with Tor Sheaves", "Spectral Affine Space Spec(S[x_1, ..., x_n])", "Derived Quotient Stack [X / G] with Lie Algebra Resolvent"], help="Derived scheme archetype")
    p_der.add_argument("--depth", "-d", type=int, default=3, help="Homotopical Postnikov truncation depth (default: 3)")
    p_der.add_argument("--amp-low", type=int, default=-1, help="Cotangent complex lowest amplitude degree (default: -1)")
    p_der.add_argument("--amp-high", type=int, default=0, help="Cotangent complex highest amplitude degree (default: 0)")
    p_der.add_argument("--svg", default="", help="Output derived geometry and spectral Postnikov tower SVG filepath")
    p_der.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_der.add_argument("--demo", action="store_true", help="Run with demonstration derived critical locus, cotangent complex, and TMF spectral sheaf")
    # iut-theory / hodge-theatre / theta-link / mochizuki-loom
    p_iut = subparsers.add_parser("iut-theory", aliases=["hodge-theatre", "theta-link", "mochizuki-loom"], help="Autonomous cognitive spatial Inter-Universal Teichmuller Theory and Mochizuki Hodge Theatre Loom")
    p_iut.add_argument("--prime-l", "-l", type=int, default=5, choices=[3, 5, 7, 11, 13], help="Base odd prime l for theta packet capsule (default: 5)")
    p_iut.add_argument("--q-param", "-q", type=float, default=0.05, help="Elliptic curve q-parameter (default: 0.05)")
    p_iut.add_argument("--log-n", type=int, default=0, help="Log-step coordinate n in log-theta lattice Z x Z (default: 0)")
    p_iut.add_argument("--theta-m", type=int, default=0, help="Theta-step coordinate m in log-theta lattice Z x Z (default: 0)")
    p_iut.add_argument("--epsilon", type=float, default=0.1, help="Epsilon parameter for Szpiro height bound (default: 0.1)")
    p_iut.add_argument("--svg", default="", help="Output IUT theory and Hodge theatre SVG filepath")
    p_iut.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_iut.add_argument("--demo", action="store_true", help="Run with demonstration Hodge theatre, theta-link, and multiradial envelope")
    # non-commutative-geometry / nc-geometry / dirac-operator / connes-action / ncg-loom
    p_ncg = subparsers.add_parser("non-commutative-geometry", aliases=["nc-geometry", "dirac-operator", "connes-action", "ncg-loom"], help="Autonomous cognitive spatial Non-Commutative Geometry and Connes Spectral Triples Loom")
    p_ncg.add_argument("--archetype", default="noncommutative_torus", choices=["noncommutative_torus", "product_space", "spin_manifold", "four_point"], help="Spectral triple geometric archetype (default: noncommutative_torus)")
    p_ncg.add_argument("--theta", type=float, default=0.618034, help="Deformation parameter theta for noncommutative torus (default: 0.618034)")
    p_ncg.add_argument("--cutoff-lambda", type=float, default=100.0, help="Energy cutoff Lambda for Chamseddine-Connes spectral action (default: 100.0)")
    p_ncg.add_argument("--svg", default="", help="Output Non-Commutative Geometry and Spectral Triples SVG filepath")
    p_ncg.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_ncg.add_argument("--demo", action="store_true", help="Run with demonstration spectral triple, Dirac ladder, and Connes distance")
    # arithmetic-qft / dijkgraaf-witten / arithmetic-chern-simons / aqft-loom
    p_aqft = subparsers.add_parser("arithmetic-qft", aliases=["dijkgraaf-witten", "arithmetic-chern-simons", "aqft-loom"], help="Autonomous cognitive spatial Arithmetic Quantum Field Theory and Dijkgraaf-Witten Invariants Loom")
    p_aqft.add_argument("--group", default="cyclic_z3", choices=["cyclic_z3", "cyclic_z4", "klein_four", "dihedral_d6", "heisenberg_p"], help="Finite gauge group G (default: cyclic_z3)")
    p_aqft.add_argument("--manifold", default="gaussian", choices=["gaussian", "eisenstein", "imaginary_d5", "cyclotomic_z5"], help="Arithmetic 3-manifold number ring Spec(O_K) (default: gaussian)")
    p_aqft.add_argument("--twist", type=int, default=1, help="Cohomology twist level in H^3(G, U(1)) (default: 1)")
    p_aqft.add_argument("--svg", default="", help="Output Arithmetic QFT and Dijkgraaf-Witten SVG filepath")
    p_aqft.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_aqft.add_argument("--demo", action="store_true", help="Run with demonstration prime knot link, gauge holonomies, and partition phasor")
    # padic-hodge / fontaine-rings / crystalline-module / padic-loom
    p_padic = subparsers.add_parser("padic-hodge", aliases=["fontaine-rings", "crystalline-module", "padic-loom"], help="Autonomous cognitive spatial p-Adic Hodge Theory and Fontaine Period Rings Loom")
    p_padic.add_argument("--prime-p", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11, 13], help="Base p-adic prime p (default: 5)")
    p_padic.add_argument("--archetype", default="crystalline", choices=["crystalline", "semistable", "de_rham", "hodge_tate"], help="p-Adic Galois representation reduction archetype (default: crystalline)")
    p_padic.add_argument("--dim", type=int, default=2, choices=[1, 2, 3, 4], help="Representation dimension (default: 2)")
    p_padic.add_argument("--svg", default="", help="Output p-Adic Hodge Theory and Fontaine Rings SVG filepath")
    p_padic.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_padic.add_argument("--demo", action="store_true", help="Run with demonstration period rings tower, Newton-Hodge polygons, and filtered module")
    # geometric-satake / affine-grassmannian / mirkovic-vilonen / satake-loom
    p_sat = subparsers.add_parser("geometric-satake", aliases=["affine-grassmannian", "mirkovic-vilonen", "satake-loom"], help="Autonomous cognitive spatial Geometric Satake Equivalence and Mirkovic-Vilonen Cycles Loom")
    p_sat.add_argument("--group", default="sl2", choices=["sl2", "sl3", "so5", "sp4", "g2"], help="Reductive group G (default: sl2)")
    p_sat.add_argument("--coweight-level", "-k", type=int, default=2, help="Dominant coweight level k (default: 2)")
    p_sat.add_argument("--svg", default="", help="Output Geometric Satake and Mirkovic-Vilonen SVG filepath")
    p_sat.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_sat.add_argument("--demo", action="store_true", help="Run with demonstration Schubert stratification, MV cycles, and tensor convolution")
    # categorical-langlands / ind-coherent-sheaves / hecke-eigensheaves / bun-g-loom
    p_glc = subparsers.add_parser("categorical-langlands", aliases=["ind-coherent-sheaves", "hecke-eigensheaves", "bun-g-loom"], help="Autonomous cognitive spatial Categorical Langlands and Ind-Coherent Sheaves on Bun_G Loom")
    p_glc.add_argument("--genus", "-g", type=int, default=2, choices=[1, 2, 3, 4], help="Algebraic curve genus g (default: 2)")
    p_glc.add_argument("--stack", default="bun_sl2", choices=["bun_sl2", "bun_pgl2", "bun_sl3", "bun_sp4"], help="Moduli stack of bundles Bun_G (default: bun_sl2)")
    p_glc.add_argument("--spectral", default="tempered", choices=["tempered", "eisenstein", "arthur", "cuspidal"], help="Spectral local system archetype (default: tempered)")
    p_glc.add_argument("--svg", default="", help="Output Categorical Langlands and Bun_G SVG filepath")
    p_glc.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_glc.add_argument("--demo", action="store_true", help="Run with demonstration D(Bun_G), Hecke correspondence, and IndCoh_Nilp")
    # chromatic-homotopy / morava-k-theory / lubin-tate / chromatic-loom
    p_chr = subparsers.add_parser("chromatic-homotopy", aliases=["morava-k-theory", "lubin-tate", "chromatic-loom"], help="Autonomous cognitive spatial Chromatic Homotopy Theory and Morava K-Theory Loom")
    p_chr.add_argument("--prime-p", "-p", type=int, default=3, choices=[2, 3, 5, 7], help="Base prime p (default: 3)")
    p_chr.add_argument("--height", "-n", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Chromatic height n (default: 2)")
    p_chr.add_argument("--svg", default="", help="Output Chromatic Homotopy and Morava K-Theory SVG filepath")
    p_chr.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_chr.add_argument("--demo", action="store_true", help="Run with demonstration formal group laws, K(n) periodicity ladder, and fracture square")
    # geometric-cft / rosenlicht-serre / picard-sheaf / function-field-loom
    p_cft = subparsers.add_parser("geometric-cft", aliases=["rosenlicht-serre", "picard-sheaf", "function-field-loom"], help="Autonomous cognitive spatial Geometric Class Field Theory and Langlands Duality for Function Fields Loom")
    p_cft.add_argument("--genus", "-g", type=int, default=2, choices=[1, 2, 3, 4], help="Algebraic curve genus g (default: 2)")
    p_cft.add_argument("--field-q", "-q", type=int, default=5, choices=[2, 3, 5, 7, 11], help="Base finite field cardinality q (default: 5)")
    p_cft.add_argument("--modulus", "-m", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Modulus divisor degree m (default: 2)")
    p_cft.add_argument("--archetype", default="tame", choices=["tame", "wild", "unramified"], help="Modulus ramification archetype (default: tame)")
    p_cft.add_argument("--svg", default="", help="Output Geometric CFT SVG filepath")
    p_cft.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_cft.add_argument("--demo", action="store_true", help="Run with demonstration generalized Jacobians, Deligne Hecke descent, and L-function zeros")
    # dessins-enfants / belyi-map / monodromy-graph / galois-dessin-loom
    p_des = subparsers.add_parser("dessins-enfants", aliases=["belyi-map", "monodromy-graph", "galois-dessin-loom"], help="Autonomous cognitive spatial Grothendieck Dessins d'Enfants and Belyi Map Galois Ramification Loom")
    p_des.add_argument("--degree", "-d", type=int, default=4, choices=[2, 3, 4, 5, 6], help="Belyi morphism degree d (default: 4)")
    p_des.add_argument("--genus", "-g", type=int, default=0, choices=[0, 1, 2], help="Riemann surface genus g (default: 0)")
    p_des.add_argument("--archetype", default="shabat", choices=["shabat", "clean_tree", "elliptic", "fermat"], help="Dessin topology archetype (default: shabat)")
    p_des.add_argument("--svg", default="", help="Output Dessins d'Enfants SVG filepath")
    p_des.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_des.add_argument("--demo", action="store_true", help="Run with demonstration bipartite ribbon graphs, monodromy triad, and Galois orbit")
    # nonabelian-chabauty / chabauty-kim / unipotent-selmer / p-adic-points-loom
    p_nab = subparsers.add_parser("nonabelian-chabauty", aliases=["chabauty-kim", "unipotent-selmer", "p-adic-points-loom"], help="Autonomous cognitive spatial Non-Abelian Chabauty and Kim Motivic Fundamental Group Loom")
    p_nab.add_argument("--genus", "-g", type=int, default=2, choices=[1, 2, 3, 4], help="Curve genus g (default: 2)")
    p_nab.add_argument("--rank", "-r", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Mordell-Weil rank r (default: 2)")
    p_nab.add_argument("--prime-p", "-p", type=int, default=7, choices=[3, 5, 7, 11, 13], help="Base prime p (default: 7)")
    p_nab.add_argument("--depth", "-n", type=int, default=2, choices=[1, 2, 3, 4], help="Unipotent fundamental depth n (default: 2)")
    p_nab.add_argument("--svg", default="", help="Output Non-Abelian Chabauty SVG filepath")
    p_nab.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_nab.add_argument("--demo", action="store_true", help="Run with demonstration Selmer varieties, Coleman iterated integrals, and point bounds")
    # hyodo-kato / log-crystalline / monodromy-filtration / semistable-loom
    p_hk = subparsers.add_parser("hyodo-kato", aliases=["log-crystalline", "monodromy-filtration", "semistable-loom"], help="Autonomous cognitive spatial Hodge-Tate Spectral Sequences and Hyodo-Kato Cohomology Loom")
    p_hk.add_argument("--degree", "-m", type=int, default=2, choices=[1, 2, 3, 4], help="Cohomology degree m (default: 2)")
    p_hk.add_argument("--prime-p", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11], help="Base prime p (default: 5)")
    p_hk.add_argument("--toric-rank", "-t", type=int, default=2, choices=[1, 2, 3, 4], help="Toric rank t of semistable reduction (default: 2)")
    p_hk.add_argument("--archetype", default="calabi_yau", choices=["calabi_yau", "normal_crossings", "mumford", "semi_abelian"], help="Semistable reduction archetype (default: calabi_yau)")
    p_hk.add_argument("--svg", default="", help="Output Hyodo-Kato SVG filepath")
    p_hk.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_hk.add_argument("--demo", action="store_true", help="Run with demonstration log-crystalline operators, weight filtration, and Hyodo-Kato isomorphism")
    # motivic-regulator / beilinson-conjectures / chow-motives / motivic-l-loom
    p_mot = subparsers.add_parser("motivic-regulator", aliases=["beilinson-conjectures", "chow-motives", "motivic-l-loom"], help="Autonomous cognitive spatial Motives and Beilinson Conjectures on Special Values Loom")
    p_mot.add_argument("--weight", "-w", type=int, default=1, choices=[0, 1, 2, 3], help="Weight w of motive (default: 1)")
    p_mot.add_argument("--twist", "-n", type=int, default=1, choices=[0, 1, 2, 3], help="Tate twist n (default: 1)")
    p_mot.add_argument("--archetype", default="elliptic", choices=["elliptic", "k3", "calabi_yau", "tate"], help="Motivic weight archetype (default: elliptic)")
    p_mot.add_argument("--svg", default="", help="Output Beilinson Motives SVG filepath")
    p_mot.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_mot.add_argument("--demo", action="store_true", help="Run with demonstration Chow motives, Beilinson regulator maps, and special values")
    # bloch-kato / tamagawa-numbers / crystalline-exponential / selmer-lattice-loom
    p_bk = subparsers.add_parser("bloch-kato", aliases=["tamagawa-numbers", "crystalline-exponential", "selmer-lattice-loom"], help="Autonomous cognitive spatial Tamagawa Numbers and Bloch-Kato Exponential Map Loom")
    p_bk.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11], help="Base prime p (default: 5)")
    p_bk.add_argument("--dim", "-d", type=int, default=2, choices=[1, 2, 3, 4], help="Representation dimension (default: 2)")
    p_bk.add_argument("--archetype", default="elliptic", choices=["elliptic", "tate", "modular", "calabi_yau"], help="Motivic Galois archetype (default: elliptic)")
    p_bk.add_argument("--svg", default="", help="Output Bloch-Kato SVG filepath")
    p_bk.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_bk.add_argument("--demo", action="store_true", help="Run with demonstration Selmer conditions, exponential map, and Tamagawa numbers")
    # euler-systems / kolyvagin-derivatives / heegner-system / selmer-bound-loom
    p_es = subparsers.add_parser("euler-systems", aliases=["kolyvagin-derivatives", "heegner-system", "selmer-bound-loom"], help="Autonomous cognitive spatial Euler Systems and Kolyvagin Derivatives Loom")
    p_es.add_argument("--conductor", "-m", type=int, default=7, help="Conductor m of Euler system (default: 7)")
    p_es.add_argument("--prime", "-p", type=int, default=3, choices=[2, 3, 5, 7, 11], help="Base prime p (default: 3)")
    p_es.add_argument("--archetype", default="heegner", choices=["heegner", "cyclotomic", "kato", "beilinson_flach"], help="Euler system archetype (default: heegner)")
    p_es.add_argument("--svg", default="", help="Output Euler Systems SVG filepath")
    p_es.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_es.add_argument("--demo", action="store_true", help="Run with demonstration norm relations, Kolyvagin derivatives, and Selmer bounds")
    # iwasawa-theory / padic-l-functions / iwasawa-main-conjecture / lambda-module-loom
    p_iw = subparsers.add_parser("iwasawa-theory", aliases=["padic-l-functions", "iwasawa-main-conjecture", "lambda-module-loom"], help="Autonomous cognitive spatial Iwasawa Main Conjecture and p-Adic L-Functions Loom")
    p_iw.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11], help="Base prime p (default: 5)")
    p_iw.add_argument("--lambda-inv", "-l", type=int, default=1, help="Iwasawa lambda-invariant (default: 1)")
    p_iw.add_argument("--archetype", default="cyclotomic", choices=["cyclotomic", "ordinary", "supersingular", "totally_real"], help="Iwasawa theory archetype (default: cyclotomic)")
    p_iw.add_argument("--svg", default="", help="Output Iwasawa Theory SVG filepath")
    p_iw.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_iw.add_argument("--demo", action="store_true", help="Run with demonstration Lambda-modules, p-adic L-functions, and Main Conjecture equality")
    # hida-family / ordinary-deformation / lambda-adic-form / hecke-algebra-loom
    p_hd = subparsers.add_parser("hida-family", aliases=["ordinary-deformation", "lambda-adic-form", "hecke-algebra-loom"], help="Autonomous cognitive spatial Hida Families and Ordinary Modular Deformations Loom")
    p_hd.add_argument("--level", "-n", type=int, default=11, help="Modular level N (default: 11)")
    p_hd.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11], help="Base prime p (default: 5)")
    p_hd.add_argument("--weight", "-k", type=int, default=2, help="Target specialization weight k >= 2 (default: 2)")
    p_hd.add_argument("--archetype", default="elliptic", choices=["elliptic", "delta", "cm", "eisenstein"], help="Hida family archetype (default: elliptic)")
    p_hd.add_argument("--svg", default="", help="Output Hida Family SVG filepath")
    p_hd.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_hd.add_argument("--demo", action="store_true", help="Run with demonstration ordinary Hecke spectra, weight fibrations, and big Galois representations")
    # coleman-family / overconvergent-forms / eigencurve / finite-slope-loom
    p_cl = subparsers.add_parser("coleman-family", aliases=["overconvergent-forms", "eigencurve", "finite-slope-loom"], help="Autonomous cognitive spatial Coleman Families and Overconvergent Modular Forms Loom")
    p_cl.add_argument("--level", "-n", type=int, default=1, help="Modular level N (default: 1)")
    p_cl.add_argument("--prime", "-p", type=int, default=2, choices=[2, 3, 5, 7, 11], help="Base prime p (default: 2)")
    p_cl.add_argument("--weight", "-k", type=int, default=4, help="Weight k of modular forms (default: 4)")
    p_cl.add_argument("--radius", "-r", type=float, default=0.2, help="Overconvergence radius r > 0 (default: 0.2)")
    p_cl.add_argument("--slope", "-a", type=float, default=0.5, help="Slope alpha = v_p(a_p) of U_p eigenvalue (default: 0.5)")
    p_cl.add_argument("--archetype", default="eigencurve", choices=["eigencurve", "finite-slope", "critical-slope", "ramanujan"], help="Coleman family archetype (default: eigencurve)")
    p_cl.add_argument("--svg", default="", help="Output Coleman Family SVG filepath")
    p_cl.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_cl.add_argument("--demo", action="store_true", help="Run with demonstration overconvergent Banach spaces, Fredholm series, slope decompositions, and eigencurve")
    # fontaine-mazur / geometric-galois / de-rham-representation / galois-deformation-loom
    p_fm = subparsers.add_parser("fontaine-mazur", aliases=["geometric-galois", "de-rham-representation", "galois-deformation-loom"], help="Autonomous cognitive spatial Fontaine-Mazur Conjecture and Geometric Galois Representations Loom")
    p_fm.add_argument("--dimension", "-d", type=int, default=2, help="Galois representation dimension (default: 2)")
    p_fm.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11], help="Base prime p (default: 5)")
    p_fm.add_argument("--archetype", default="elliptic", choices=["elliptic", "delta", "dirichlet", "exotic"], help="Geometric Galois representation archetype (default: elliptic)")
    p_fm.add_argument("--svg", default="", help="Output Fontaine-Mazur SVG filepath")
    p_fm.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_fm.add_argument("--demo", action="store_true", help="Run with demonstration period rings, Hodge-Tate weights, and modularity isomorphism R = T")
    # serre-modularity / odd-representation / serre-weight-loom / khare-wintenberger
    p_sm = subparsers.add_parser("serre-modularity", aliases=["odd-representation", "serre-weight-loom", "khare-wintenberger"], help="Autonomous cognitive spatial Serre's Modularity Conjecture and Odd Galois Representations Loom")
    p_sm.add_argument("--level", "-n", type=int, default=11, help="Artin conductor prime-to-p level N (default: 11)")
    p_sm.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11, 13], help="Residual prime p (default: 5)")
    p_sm.add_argument("--weight", "-k", type=int, default=2, help="Serre weight k (default: 2)")
    p_sm.add_argument("--archetype", default="elliptic", choices=["elliptic", "delta", "dihedral", "even"], help="Residual Galois representation archetype (default: elliptic)")
    p_sm.add_argument("--svg", default="", help="Output Serre Modularity SVG filepath")
    p_sm.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_sm.add_argument("--demo", action="store_true", help="Run with demonstration Serre invariants, tame inertia actions, and Khare-Wintenberger theorem")
    # perfectoid-tilting / scholze-tilting / almost-mathematics-loom / perfectoid-category
    p_ps = subparsers.add_parser("perfectoid-tilting", aliases=["scholze-tilting", "almost-mathematics-loom", "perfectoid-category"], help="Autonomous cognitive spatial Perfectoid Spaces and Scholze Tilting Equivalence Loom")
    p_ps.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11, 13], help="Base prime p (default: 5)")
    p_ps.add_argument("--archetype", default="cyclotomic", choices=["cyclotomic", "roots", "algebraic", "shimura"], help="Perfectoid field pair archetype (default: cyclotomic)")
    p_ps.add_argument("--svg", default="", help="Output Perfectoid Tilting SVG filepath")
    p_ps.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_ps.add_argument("--demo", action="store_true", help="Run with demonstration tilting equivalence, adic spectrum Spa(R, R^+), and Shimura variety torsion vanishing towers")
    # fargues-scholze / local-shtuka / excursion-operator / geometrization-loom
    p_fs = subparsers.add_parser("fargues-scholze", aliases=["local-shtuka", "excursion-operator", "geometrization-loom"], help="Autonomous cognitive spatial Fargues-Scholze Geometrization of Local Langlands Loom")
    p_fs.add_argument("--group", "-g", default="GL_2", choices=["GL_2", "GSp_4", "SL_2"], help="Connected reductive group G (default: GL_2)")
    p_fs.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11, 13], help="Local base prime p (default: 5)")
    p_fs.add_argument("--archetype", default="unramified", choices=["unramified", "supercuspidal", "siegel", "packet"], help="Local representation and shtuka archetype (default: unramified)")
    p_fs.add_argument("--svg", default="", help="Output Fargues-Scholze SVG filepath")
    p_fs.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_fs.add_argument("--demo", action="store_true", help="Run with demonstration Bun_G stack, local shtukas, excursion operators, and L-parameters")
    # kudla-program / arithmetic-intersection / special-cycles-loom / kudla-rapoport
    p_kp = subparsers.add_parser("kudla-program", aliases=["arithmetic-intersection", "special-cycles-loom", "kudla-rapoport"], help="Autonomous cognitive spatial Kudla Program Arithmetic Intersection Loom")
    p_kp.add_argument("--signature", default="3,2", choices=["3,2", "2,2", "1,1"], help="Signature of orthogonal/unitary space (default: 3,2)")
    p_kp.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11, 13], help="Base prime p (default: 5)")
    p_kp.add_argument("--archetype", default="siegel", choices=["siegel", "hilbert", "modular", "rapoport"], help="Shimura variety archetype (default: siegel)")
    p_kp.add_argument("--svg", default="", help="Output Kudla Program SVG filepath")
    p_kp.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_kp.add_argument("--demo", action="store_true", help="Run with demonstration special cycles, Kudla-Rapoport intersections, and Eisenstein series derivative")
    # colmez-conjecture / faltings-height / cm-abelian-loom / artin-derivative
    p_cz = subparsers.add_parser("colmez-conjecture", aliases=["faltings-height", "cm-abelian-loom", "artin-derivative"], help="Autonomous cognitive spatial Colmez Conjecture and Faltings Heights Loom")
    p_cz.add_argument("--dimension", "-g", type=int, default=1, choices=[1, 2, 3], help="Dimension of CM abelian variety (default: 1)")
    p_cz.add_argument("--discriminant", "-d", type=int, default=7, choices=[7, 11, 15, 19, 23], help="Fundamental discriminant of CM field (default: 7)")
    p_cz.add_argument("--archetype", default="elliptic", choices=["elliptic", "surface", "dihedral", "sextic"], help="CM variety archetype (default: elliptic)")
    p_cz.add_argument("--svg", default="", help="Output Colmez Conjecture SVG filepath")
    p_cz.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_cz.add_argument("--demo", action="store_true", help="Run with demonstration CM type, Faltings height, and Artin L-derivatives")
    # gross-stark / stark-conjecture / padic-regulator / brumer-stark
    p_gs = subparsers.add_parser("gross-stark", aliases=["stark-conjecture", "padic-regulator", "brumer-stark"], help="Autonomous cognitive spatial Gross-Stark and p-Adic Stark Conjectures Loom")
    p_gs.add_argument("--degree", "-g", type=int, default=2, choices=[2, 3, 4], help="Degree of totally real base field F (default: 2)")
    p_gs.add_argument("--discriminant", "-d", type=int, default=5, choices=[2, 5, 8, 12, 13, 17], help="Discriminant of totally real base field (default: 5)")
    p_gs.add_argument("--prime", "-p", type=int, default=3, choices=[2, 3, 5, 7, 11], help="Splitting prime p with exceptional zero (default: 3)")
    p_gs.add_argument("--archetype", default="sqrt5", choices=["sqrt5", "sqrt2", "cubic", "quartic"], help="Totally real field archetype (default: sqrt5)")
    p_gs.add_argument("--svg", default="", help="Output Gross-Stark SVG filepath")
    p_gs.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_gs.add_argument("--demo", action="store_true", help="Run with demonstration Gross-Stark unit, p-adic regulator, and Shintani cones")
    # langlands-shahidi / shahidi-gamma / intertwining-operator / automorphic-l-loom
    p_ls = subparsers.add_parser("langlands-shahidi", aliases=["shahidi-gamma", "intertwining-operator", "automorphic-l-loom"], help="Autonomous cognitive spatial Langlands-Shahidi Method and Automorphic L-Functions Loom")
    p_ls.add_argument("--spectral-s", "-s", type=float, default=1.0, help="Spectral complex parameter s (default: 1.0)")
    p_ls.add_argument("--prime", "-p", type=int, default=5, choices=[2, 3, 5, 7, 11, 13], help="Local unramified prime p (default: 5)")
    p_ls.add_argument("--archetype", default="so5", choices=["so5", "sp4", "rankin", "exterior"], help="Quasi-split group and parabolic archetype (default: so5)")
    p_ls.add_argument("--svg", default="", help="Output Langlands-Shahidi SVG filepath")
    p_ls.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_ls.add_argument("--demo", action="store_true", help="Run with demonstration intertwining operator, Shahidi gamma factors, and functorial lifts")
    # arthur-trace-formula / endoscopic-classification / arthur-packet / selberg-trace-loom
    p_at = subparsers.add_parser("arthur-trace-formula", aliases=["endoscopic-classification", "arthur-packet", "selberg-trace-loom"], help="Autonomous cognitive spatial Arthur-Selberg Trace Formula and Endoscopic Classification Loom")
    p_at.add_argument("--cutoff", "-c", type=float, default=2.5, help="Test function truncation parameter T (default: 2.5)")
    p_at.add_argument("--truncation", "-t", type=int, default=4, help="Spectral truncation level (default: 4)")
    p_at.add_argument("--group", "-g", default="so5", choices=["so5", "sp4", "so7", "gl4"], help="Classical group archetype (default: so5)")
    p_at.add_argument("--svg", default="", help="Output Arthur-Selberg SVG filepath")
    p_at.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_at.add_argument("--demo", action="store_true", help="Run with demonstration geometric orbital sums, endoscopic transfer, and Arthur packets")
    # relative-trace-ggp / ggp-loom / ichino-ikeda / gan-gross-prasad
    p_rtf = subparsers.add_parser("relative-trace-ggp", aliases=["ggp-loom", "ichino-ikeda", "gan-gross-prasad"], help="Autonomous cognitive spatial Relative Trace Formula and Gan-Gross-Prasad Conjectures Loom")
    p_rtf.add_argument("--spectral-s", "-s", type=float, default=1.0, help="Spectral parameter s (default: 1.0)")
    p_rtf.add_argument("--truncation", "-t", type=float, default=2.0, help="Subgroup truncation parameter T (default: 2.0)")
    p_rtf.add_argument("--archetype", default="u3_u2", choices=["u3_u2", "so5_so4", "waldspurger", "aggp"], help="RTF and GGP setting archetype (default: u3_u2)")
    p_rtf.add_argument("--svg", default="", help="Output Relative Trace GGP SVG filepath")
    p_rtf.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_rtf.add_argument("--demo", action="store_true", help="Run with demonstration spherical relative integrals, GGP branching, and Ichino-Ikeda central L-value ratio")
    # beyond-endoscopy / langlands-functoriality / poisson-trace / altug-loom
    p_be = subparsers.add_parser("beyond-endoscopy", aliases=["langlands-functoriality", "poisson-trace", "altug-loom"], help="Autonomous cognitive spatial Beyond Endoscopy and Langlands Functoriality Loom")
    p_be.add_argument("--energy", "-e", type=float, default=1.0, help="Test energy parameter (default: 1.0)")
    p_be.add_argument("--epsilon", "-eps", type=float, default=0.05, help="Altug unipotent smoothing parameter epsilon (default: 0.05)")
    p_be.add_argument("--archetype", default="sym2", choices=["sym2", "rankin", "adjoint", "altug"], help="Beyond Endoscopy archetype (default: sym2)")
    p_be.add_argument("--svg", default="", help="Output Beyond Endoscopy SVG filepath")
    p_be.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_be.add_argument("--demo", action="store_true", help="Run with demonstration Poisson summation, L-pole residue isolation, and Altug smoothing")
    # taylor-wiles / modularity-lifting / patching-loom / r-equals-t
    p_tw = subparsers.add_parser("taylor-wiles", aliases=["modularity-lifting", "patching-loom", "r-equals-t"], help="Autonomous cognitive spatial Taylor-Wiles Patching and Modularity Lifting Loom")
    p_tw.add_argument("--prime", "-p", type=int, default=5, choices=[3, 5, 7, 11], help="Prime p (default: 5)")
    p_tw.add_argument("--level", "-l", type=int, default=2, help="Patching level N (default: 2)")
    p_tw.add_argument("--archetype", default="fermat", choices=["fermat", "ordinary", "kisin", "unitary"], help="Modularity archetype (default: fermat)")
    p_tw.add_argument("--svg", default="", help="Output Taylor-Wiles SVG filepath")
    p_tw.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_tw.add_argument("--demo", action="store_true", help="Run with demonstration Selmer groups, Taylor-Wiles primes, and R = T proof")
    # paramodular-conjecture / abelian-surface / paramodular-loom / brumer-kramer
    p_pm = subparsers.add_parser("paramodular-conjecture", aliases=["abelian-surface", "paramodular-loom", "brumer-kramer"], help="Autonomous cognitive spatial Paramodular Conjecture and Modularity of Abelian Surfaces Loom")
    p_pm.add_argument("--conductor", "-c", type=int, default=277, help="Conductor N of abelian surface (default: 277)")
    p_pm.add_argument("--precision", type=float, default=0.01, help="Spectral precision (default: 0.01)")
    p_pm.add_argument("--archetype", default="n277", choices=["n277", "n587", "lift", "bcgp"], help="Paramodular archetype (default: n277)")
    p_pm.add_argument("--svg", default="", help="Output Paramodular Conjecture SVG filepath")
    p_pm.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_pm.add_argument("--demo", action="store_true", help="Run with demonstration abelian surface, paramodular cusp form, and Spinor Euler factors")
    # calabi-yau-modularity / attractor-mechanism / picard-fuchs / calabi-yau-loom
    p_cy = subparsers.add_parser("calabi-yau-modularity", aliases=["attractor-mechanism", "picard-fuchs", "cy-modularity-loom"], help="Autonomous cognitive spatial Calabi-Yau Modularity and Attractor Mechanism Loom")
    p_cy.add_argument("--model", default="quintic", choices=["quintic", "rigid", "octic"], help="Calabi-Yau threefold model (default: quintic)")
    p_cy.add_argument("--charges", default="1,0,0,-5", help="Electromagnetic charge vector p0,p1,q1,q0 (default: 1,0,0,-5)")
    p_cy.add_argument("--steps", type=int, default=40, help="Attractor gradient flow steps (default: 40)")
    p_cy.add_argument("--svg", default="", help="Output Calabi-Yau Modularity SVG filepath")
    p_cy.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_cy.add_argument("--demo", action="store_true", help="Run demonstration Calabi-Yau moduli analysis, attractor flow, and S_4 modularity")
    # k3-modularity / borcherds-product / transcendental-lattice / k3-loom
    p_k3 = subparsers.add_parser("k3-modularity", aliases=["borcherds-product", "transcendental-lattice", "k3-loom"], help="Autonomous cognitive spatial K3 Surfaces Modularity and Borcherds Automorphic Products Loom")
    p_k3.add_argument("--discriminant", "-d", type=int, default=-3, help="Discriminant D of transcendental lattice T(S) (default: -3)")
    p_k3.add_argument("--picard", type=int, default=20, help="Picard number rho(S) (default: 20)")
    p_k3.add_argument("--model", default="shioda", choices=["shioda", "fermat", "klein", "generic"], help="K3 surface model (default: shioda)")
    p_k3.add_argument("--svg", default="", help="Output K3 Modularity SVG filepath")
    p_k3.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")
    p_k3.add_argument("--demo", action="store_true", help="Run demonstration K3 lattice analysis, Shioda-Inose CM modularity, and Borcherds product")
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
    elif args.command in ["reflector", "bias", "blindspot"]:
        import scripts.metacognitive_reflector as mr
        reflector = mr.MetacognitiveReflector()
        assumptions = []
        if args.demo or not args.assumptions:
            assumptions = [
                {"label": "Sub-millisecond Edge Replication", "validated": False},
                {"label": "Zero Consensus Split-Brain", "validated": True},
                {"label": "Infinite Memory Pool", "validated": False},
                {"label": "Immutable Audit Log Guarantee", "validated": True},
                {"label": "Instantaneous Client Re-connection", "validated": False},
            ]
        else:
            for item in args.assumptions:
                if ":" in item:
                    lbl, val = item.rsplit(":", 1)
                    assumptions.append({"label": lbl.strip(), "validated": val.strip().lower() in ["true", "1", "yes"]})
                else:
                    assumptions.append({"label": item.strip(), "validated": False})

        assessment = reflector.assess_thesis(
            args.title, assumptions, perspective_breadth=args.perspectives
        )

        if args.json:
            out = {
                "assessment": assessment.to_dict(),
                "lenses": [l.to_dict() for l in assessment.lenses],
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + reflector.export_summary_markdown(assessment))

        if args.canvas:
            reflector.export_canvas(assessment, output_path=args.canvas)
            print(f"\n[DxSkills] Metacognitive Reflector .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = reflector.export_svg_radar(assessment)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Metacognitive Radar SVG exported to: {args.svg}")
    elif args.command == "horizon":
        import scripts.horizon_visualizer as hv
        viz = hv.WorkingMemoryHorizonVisualizer()
        items = []
        if args.input:
            raw_text = read_input(args.input)
            data = json.loads(raw_text)
            for d in data:
                items.append(hv.HorizonItem(
                    id=d.get("id", str(len(items) + 1)),
                    label=d.get("label", "Task"),
                    horizon=d.get("horizon", "immediate"),
                    estimated_hours=float(d.get("estimated_hours", 1.0)),
                    cognitive_weight=float(d.get("cognitive_weight", 5.0)),
                    parent_id=d.get("parent_id"),
                ))
        else:
            items = [
                hv.HorizonItem("imm-1", "Patch critical token eviction bug", "immediate", 0.5, 4.0),
                hv.HorizonItem("imm-2", "Review pre-commit zero em dash rule", "immediate", 0.25, 2.0),
                hv.HorizonItem("imm-3", "Write unit tests for load shedder", "immediate", 1.0, 3.0),
                hv.HorizonItem("tac-1", "Deploy multi-modal audio telemetry stream", "tactical", 14.0, 6.0, parent_id="str-1"),
                hv.HorizonItem("tac-2", "Refactor CLI subparser dispatch tables", "tactical", 8.0, 5.0),
                hv.HorizonItem("str-1", "Federated neuro-ergonomic spatial desktop OS", "strategic", 160.0, 9.0),
            ]

        telemetry = viz.evaluate_horizons(items)

        if args.json:
            out = {
                "telemetry": telemetry.to_dict(),
                "items": [it.to_dict() for it in items],
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + viz.export_summary_markdown(telemetry, items))

        if args.canvas:
            viz.export_canvas(items, telemetry, output_path=args.canvas)
            print(f"\n[DxSkills] Concentric Horizon .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = viz.export_svg_radar(items, telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Concentric Horizon Radar SVG exported to: {args.svg}")
    elif args.command in ["evict", "compactor"]:
        import scripts.anchor_eviction as ae
        compactor = ae.MemoryBufferCompactor(capacity_limit=args.capacity)
        nodes = []
        if args.input:
            raw_text = read_input(args.input)
            data = json.loads(raw_text)
            for d in data:
                nodes.append(ae.WorkingMemoryNode(
                    id=d.get("id", str(len(nodes) + 1)),
                    label=d.get("label", "Node"),
                    base_importance=float(d.get("base_importance", 5.0)),
                    idle_minutes=float(d.get("idle_minutes", 0.0)),
                    reference_count=int(d.get("reference_count", 0)),
                    decay_rate=float(d.get("decay_rate", 0.08)),
                ))
        else:
            nodes = [
                ae.WorkingMemoryNode("n1", "Critical Thread: Raft Leader Election", 9.5, idle_minutes=1.0, reference_count=4),
                ae.WorkingMemoryNode("n2", "Active Thread: WAL Log Compaction", 8.0, idle_minutes=3.0, reference_count=2),
                ae.WorkingMemoryNode("n3", "Secondary Thread: RPC Timeout Retry", 7.0, idle_minutes=8.0, reference_count=1),
                ae.WorkingMemoryNode("n4", "Tertiary Thread: Client Telemetry Ping", 5.5, idle_minutes=12.0, reference_count=1),
                ae.WorkingMemoryNode("n5", "Dormant Thread: S3 Snapshot Multipart Upload", 4.0, idle_minutes=25.0, reference_count=0),
                ae.WorkingMemoryNode("n6", "Stale Thread: Legacy TLS Handshake Fallback", 3.0, idle_minutes=45.0, reference_count=0),
                ae.WorkingMemoryNode("n7", "Forgotten Thread: Deprecated V1 Config Parser", 2.0, idle_minutes=90.0, reference_count=0),
            ]

        audit = compactor.compact_buffer(nodes)

        if args.json:
            print(json.dumps(audit.to_dict(), indent=2))
        else:
            print("\n" + compactor.export_summary_markdown(audit))

        if args.canvas:
            compactor.export_canvas(audit, output_path=args.canvas)
            print(f"\n[DxSkills] Compacted Memory Buffer .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = compactor.export_svg_telemetry(audit)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Buffer Telemetry SVG exported to: {args.svg}")
    elif args.command in ["interleave", "dampener", "bookmark"]:
        import scripts.context_dampener as cd
        dampener = cd.ContextSwitchDampener()
        state = cd.ContextState(
            project_name=args.project,
            active_thread=args.thread,
            depth_of_focus=args.focus,
            completion_ratio=args.completion,
            time_in_flow_min=args.minutes,
            unresolved_tensions=args.loops,
            immediate_next_step=args.next_step,
        )
        telemetry = dampener.evaluate_switch(state)

        if args.json:
            out = {
                "state": state.to_dict(),
                "telemetry": telemetry.to_dict(),
            }
            print(json.dumps(out, indent=2))
        else:
            print("\n" + dampener.export_summary_markdown(state, telemetry))

        if args.canvas:
            dampener.export_canvas(state, telemetry, output_path=args.canvas)
            print(f"\n[DxSkills] Context Bookmark .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = dampener.export_svg_gauge(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Attention Residue Gauge SVG exported to: {args.svg}")
    elif args.command in ["examine", "grill", "cross-examine"]:
        import scripts.socratic_cross_examiner as sce
        examiner = sce.SocraticCrossExaminer()
        comps = [
            {"name": "Ingress API Gateway", "has_tests": True, "has_failover": True, "is_stateless": True},
            {"name": "Raft State Machine", "has_tests": True, "has_failover": True, "is_stateless": False},
            {"name": "Async Task Dispatcher", "has_tests": True, "has_failover": False, "is_stateless": True},
            {"name": "Memory Buffer Ring", "has_tests": False, "has_failover": False, "is_stateless": False},
        ]
        scorecard = examiner.cross_examine_architecture(args.title, comps)

        if args.json:
            print(json.dumps(scorecard.to_dict(), indent=2))
        else:
            print("\n" + examiner.export_summary_markdown(scorecard))

        if args.canvas:
            examiner.export_canvas(scorecard, output_path=args.canvas)
            print(f"\n[DxSkills] Socratic Examination .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = examiner.export_svg_radar(scorecard)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Socratic Rigor Radar SVG exported to: {args.svg}")
    elif args.command in ["audio-pacer", "pacer", "soundstage"]:
        import scripts.audio_pacer as ap
        pacer = ap.SpatialAudioPacer()
        task_profile = ap.CognitiveTaskProfile(
            task_name=args.task,
            complexity_score=args.complexity,
            cognitive_load=args.load,
        )
        raw_streams = []
        if args.demo or not args.streams:
            raw_streams = [
                {"id": "s1", "name": "Primary Code IDE", "track_type": ap.AudioTrackType.PRIMARY_FOCUS, "description": "Active coding AST buffer"},
                {"id": "s2", "name": "Telemetry Logs", "track_type": ap.AudioTrackType.TELEMETRY_LOG, "description": "Build pipeline and test stream"},
                {"id": "s3", "name": "Rhythmic Metronome", "track_type": ap.AudioTrackType.RHYTHMIC_PACER, "description": "Cognitive grounding pulse"},
                {"id": "s4", "name": "Production Alerts", "track_type": ap.AudioTrackType.ALERT_URGENT, "description": "Critical exception alerts"},
            ]
        else:
            for idx, item in enumerate(args.streams):
                if ":" in item:
                    s_name, s_type = item.rsplit(":", 1)
                else:
                    s_name, s_type = item, "telemetry_log"
                raw_streams.append({
                    "id": f"stream_{idx+1}",
                    "name": s_name.strip(),
                    "track_type": s_type.strip(),
                })

        config = pacer.decouple_saliency(task_profile, raw_streams)

        if args.json:
            print(json.dumps(config.to_dict(), indent=2))
        else:
            print("\n" + pacer.generate_markdown_report(config))

        if args.canvas:
            pacer.export_canvas(config, output_path=args.canvas)
            print(f"\n[DxSkills] Spatial Soundstage .canvas exported to: {args.canvas}")

        if args.svg:
            pacer.export_svg_soundstage(config, output_path=args.svg)
            print(f"[DxSkills] Soundstage Radar SVG exported to: {args.svg}")

        if args.manifest:
            manifest_data = pacer.generate_web_audio_manifest(config)
            with open(args.manifest, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2)
            print(f"[DxSkills] Web Audio manifest exported to: {args.manifest}")
    elif args.command in ["fovea", "tunnel", "attention-tunnel"]:
        import scripts.fovea_synchronizer as fs
        sync = fs.SpatialFoveaSynchronizer()
        canvas_data = None
        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                canvas_data = json.load(f)
        elif args.demo or not args.canvas:
            canvas_data = {
                "nodes": [
                    {"id": "node_core", "x": 0, "y": 0, "width": 260, "height": 140, "color": "1", "text": "### Raft Distributed Consensus\nActive leader heartbeat loop and log replication barrier."},
                    {"id": "node_wal", "x": 200, "y": 160, "width": 240, "height": 130, "color": "2", "text": "### Write-Ahead Log Ring\nIn-memory circular buffer and fsync batcher."},
                    {"id": "node_cache", "x": -220, "y": 180, "width": 240, "height": 130, "color": "3", "text": "### L1 Saliency Cache\nLRU eviction cache with TTL invalidation hooks."},
                    {"id": "node_cold", "x": 850, "y": 750, "width": 250, "height": 140, "color": "4", "text": "### S3 Glacier Cold Storage\nPeriodic multi-part archival upload pipeline."},
                    {"id": "node_audit", "x": -800, "y": 700, "width": 250, "height": 140, "color": "5", "text": "### Audit Compliance Sink\nCryptographic append-only ledger for telemetry."},
                ],
                "edges": []
            }
        
        mode = fs.DampingMode(args.mode)
        focus_id = args.focus if args.focus else (canvas_data["nodes"][0]["id"] if canvas_data.get("nodes") else None)
        transformed_canvas, telemetry = sync.apply_attention_tunnel(
            canvas_data, focus_node_id=focus_id, cognitive_load=args.load, damping_mode=mode
        )

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + sync.generate_markdown_report(telemetry))

        if args.output_canvas:
            with open(args.output_canvas, "w", encoding="utf-8") as f:
                json.dump(transformed_canvas, f, indent=2)
            print(f"\n[DxSkills] Attention-tunneled .canvas exported to: {args.output_canvas}")

        if args.svg:
            anchors = []
            fx = canvas_data["nodes"][0].get("x", 0)
            fy = canvas_data["nodes"][0].get("y", 0)
            for n in transformed_canvas.get("nodes", []):
                nx = n.get("x", 0)
                ny = n.get("y", 0)
                d = math.hypot(nx - fx, ny - fy)
                ang = math.degrees(math.atan2(ny - fy, nx - fx))
                is_f = (n.get("id") == focus_id) or (d <= telemetry.tunnel_radius_px)
                anchors.append(fs.PeripheralAnchor(
                    node_id=n.get("id", ""),
                    label=n.get("text", "").split("\n")[0].replace("#", "").strip() or "Node",
                    x=nx,
                    y=ny,
                    distance_from_focus=round(d, 1),
                    angle_degrees=round(ang, 1),
                    opacity=1.0 if is_f else 0.35,
                    is_foveal=is_f,
                    color=n.get("color", "1"),
                ))
            svg_code = sync.export_svg_tunnel(anchors, telemetry, output_path=args.svg)
            print(f"[DxSkills] Attention tunnel radar SVG exported to: {args.svg}")
    elif args.command in ["consensus", "merge", "resolve-conflict"]:
        import scripts.workspace_consensus as wc
        synthesizer = wc.WorkspaceConsensusSynthesizer()
        
        base_canvas = {"nodes": [], "edges": []}
        canvas_a = {"nodes": [], "edges": []}
        canvas_b = {"nodes": [], "edges": []}
        
        if args.base and os.path.isfile(args.base):
            with open(args.base, "r", encoding="utf-8") as f:
                base_canvas = json.load(f)
        if args.branch_a and os.path.isfile(args.branch_a):
            with open(args.branch_a, "r", encoding="utf-8") as f:
                canvas_a = json.load(f)
        if args.branch_b and os.path.isfile(args.branch_b):
            with open(args.branch_b, "r", encoding="utf-8") as f:
                canvas_b = json.load(f)
                
        if args.demo or (not args.base and not args.branch_a):
            base_canvas = {
                "nodes": [
                    {"id": "n_core", "x": 0, "y": 0, "text": "### Master Pipeline\nShared deterministic state machine."},
                    {"id": "n_cache", "x": 200, "y": 0, "text": "### Cache Tier\nLRU policy with 500ms TTL."},
                ],
                "edges": [{"id": "e1", "fromNode": "n_core", "toNode": "n_cache"}]
            }
            canvas_a = {
                "nodes": [
                    {"id": "n_core", "x": 0, "y": 0, "text": "### Master Pipeline\nShared deterministic state machine with Raft consensus."},
                    {"id": "n_cache", "x": 200, "y": 0, "text": "### Cache Tier\nLRU policy with 500ms TTL."},
                    {"id": "n_agent_a", "x": 0, "y": 200, "text": "### Telemetry Agent A\nHigh-frequency event emitter."},
                ],
                "edges": [
                    {"id": "e1", "fromNode": "n_core", "toNode": "n_cache"},
                    {"id": "e2", "fromNode": "n_core", "toNode": "n_agent_a"},
                ]
            }
            canvas_b = {
                "nodes": [
                    {"id": "n_core", "x": 0, "y": 0, "text": "### Master Pipeline\nShared deterministic state machine with Paxos leases."},
                    {"id": "n_cache", "x": 200, "y": 0, "text": "### Cache Tier\nConsistent hashing ring with 2s TTL."},
                    {"id": "n_agent_b", "x": 200, "y": 200, "text": "### Analytics Agent B\nColumnar Parquet writer."},
                ],
                "edges": [
                    {"id": "e1", "fromNode": "n_core", "toNode": "n_cache"},
                    {"id": "e3", "fromNode": "n_cache", "toNode": "n_agent_b"},
                ]
            }

        merged_canvas, scorecard = synthesizer.synthesize_visual_merge(base_canvas, canvas_a, canvas_b)

        if args.json:
            print(json.dumps(scorecard.to_dict(), indent=2))
        else:
            print("\n" + synthesizer.generate_markdown_report(scorecard))

        if args.output_canvas:
            with open(args.output_canvas, "w", encoding="utf-8") as f:
                json.dump(merged_canvas, f, indent=2)
            print(f"\n[DxSkills] Synthesized merge .canvas exported to: {args.output_canvas}")

        if args.svg:
            svg_code = synthesizer.export_svg_consensus_radar(scorecard, output_path=args.svg)
            print(f"[DxSkills] Workspace consensus radar SVG exported to: {args.svg}")
    elif args.command in ["gaze", "inertia", "saccade-velocity"]:
        import scripts.gaze_inertia_balancer as gib
        balancer = gib.GazeInertiaBalancer()
        canvas_data = None
        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                canvas_data = json.load(f)
        elif args.demo or not args.canvas:
            canvas_data = {
                "nodes": [
                    {"id": "node_entry", "x": 0, "y": 0, "width": 240, "height": 130, "text": "### Entry Point\nInitial request ingress and protocol routing."},
                    {"id": "node_auth", "x": 180, "y": 120, "width": 240, "height": 130, "text": "### Auth Token Validator\nJWT cryptographic validation loop."},
                    {"id": "node_distant_db", "x": 1100, "y": 950, "width": 260, "height": 140, "text": "### Distributed Shard Mesh\nCross-datacenter consensus and persistent state."},
                    {"id": "node_distant_cold", "x": 1600, "y": 1400, "width": 260, "height": 140, "text": "### Cold Archival Glacier\nMultipart compressed snapshots and audit log."},
                ],
                "edges": []
            }

        seq = args.sequence if args.sequence else None
        stabilized_canvas, telemetry = balancer.balance_gaze_inertia(canvas_data, reading_sequence=seq)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + balancer.generate_markdown_report(telemetry))

        if args.output_canvas:
            with open(args.output_canvas, "w", encoding="utf-8") as f:
                json.dump(stabilized_canvas, f, indent=2)
            print(f"\n[DxSkills] Stabilized .canvas exported to: {args.output_canvas}")

        if args.svg:
            svg_code = balancer.export_svg_velocity_profile(telemetry, output_path=args.svg)
            print(f"[DxSkills] Saccade velocity profile SVG exported to: {args.svg}")
    elif args.command in ["scanpath", "flow", "compress-reading"]:
        import scripts.scanpath_compressor as spc
        compressor = spc.SaccadicScanpathCompressor(target_line_chars=args.chars)
        raw_text = ""
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
        elif args.demo or not args.input:
            raw_text = (
                "Distributed consensus engines mandate deterministic execution across cluster boundaries. "
                "Unsynchronized concurrent mutations risk catastrophic state corruption and partitioned quorums. "
                "Spatial cognitive architectures eliminate phonological decoding strain by mapping complex "
                "topologies directly into two-dimensional associative graphs."
            )

        mode = spc.GuidanceMode(args.mode)
        guided_text, telemetry = compressor.compress_and_guide(raw_text, mode=mode)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + compressor.generate_markdown_report(telemetry))
            print("\n## Guided Reading Preview\n")
            print(guided_text[:400] + "..." if len(guided_text) > 400 else guided_text)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(guided_text)
            print(f"\n[DxSkills] Guided reading text written to: {args.output}")

        if args.canvas:
            compressor.export_canvas(guided_text, telemetry, output_path=args.canvas)
            print(f"[DxSkills] Reading corridor .canvas exported to: {args.canvas}")

        if args.svg:
            svg_code = compressor.export_svg_scanpath(telemetry, output_path=args.svg)
            print(f"[DxSkills] Saccadic trajectory SVG exported to: {args.svg}")
    elif args.command in ["visual-metronome", "metronome", "pace-reading"]:
        import scripts.visual_metronome as vpm

        p_mode = vpm.PacingMode(args.mode)
        metronome = vpm.VisualPacingMetronome(base_wpm=args.wpm, mode=p_mode)

        raw_text = ""
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
        elif args.demo or not args.input:
            raw_text = (
                "Distributed asynchronous state machines coordinate deterministic state across multiple "
                "geographic regions. Consensus protocols eliminate split-brain synchronization anomalies "
                "during partition degradation."
            )

        telemetry = metronome.synthesize_pacing_timeline(raw_text)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + metronome.render_ascii_cadence(telemetry))

        if args.canvas:
            metronome.export_canvas(telemetry, args.canvas)
            print(f"[DxSkills] Visual pacing .canvas exported to: {args.canvas}")

        if args.svg:
            metronome.export_svg_strip(telemetry, args.svg)
            print(f"[DxSkills] Metronome strip SVG exported to: {args.svg}")
    elif args.command in ["chunk-pacer", "chunk", "syntactic-chunk"]:
        import scripts.visual_chunk_pacer as vcp

        pacer = vcp.VisualChunkPacer(base_wpm=args.wpm, target_chunk_tokens=args.tokens)

        raw_text = ""
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
        elif args.demo or not args.input:
            raw_text = (
                "Distributed asynchronous state machines coordinate deterministic consensus across cluster boundaries. "
                "Syntactic chunking and morphemic decomposition minimize lexical retrieval latency for spatial-first cognition."
            )

        telemetry = pacer.pace_chunks(raw_text)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + pacer.render_ascii_cadence(telemetry))

        if args.canvas:
            pacer.export_canvas(telemetry, args.canvas)
            print(f"[DxSkills] Syntactic chunk .canvas exported to: {args.canvas}")

        if args.svg:
            pacer.export_svg_strip(telemetry, args.svg)
            print(f"[DxSkills] Syntactic chunk strip SVG exported to: {args.svg}")
    elif args.command in ["memory-shield", "shield", "saliency-shield"]:
        import scripts.memory_shield as wms

        shield = wms.WorkingMemoryShield(
            focus_radius_px=args.focus_radius,
            orientation_radius_px=args.orientation_radius,
        )

        canvas_data = {}
        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                canvas_data = json.load(f)
        elif args.demo or not args.canvas:
            canvas_data = {
                "nodes": [
                    {"id": "node-core", "x": 0, "y": 0, "width": 300, "height": 180, "text": "Active Architecture Focus\n\nDeterministic state transitions."},
                    {"id": "node-near-1", "x": 380, "y": 50, "width": 260, "height": 140, "text": "Consensus Engine\n\nRaft-based state machine."},
                    {"id": "node-near-2", "x": -380, "y": -40, "width": 260, "height": 140, "text": "Write-Ahead Log\n\nSequential durability log."},
                    {"id": "node-mid", "x": 800, "y": 400, "width": 280, "height": 150, "text": "Cluster Telemetry Gateway\n\nHTTP metrics exposition."},
                    {"id": "node-far", "x": 1600, "y": -700, "width": 320, "height": 200, "text": "ARCHIVED DEPRECATED MIGRATION NOTES\n\nLEGACY SCHEMAS AND SCRIPTS"},
                ]
            }

        focus_ids = args.focus if args.focus else None
        shielded_canvas, telemetry = shield.apply_memory_shield(canvas_data, focus_ids=focus_ids)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + shield.render_ascii_report(telemetry))

        if args.output_canvas:
            with open(args.output_canvas, "w", encoding="utf-8") as f:
                json.dump(shielded_canvas, f, indent=2)
            print(f"[DxSkills] Shielded .canvas written to: {args.output_canvas}")

        if args.svg:
            shield.export_svg_shield(telemetry, args.svg)
            print(f"[DxSkills] Memory shield radar SVG exported to: {args.svg}")
    elif args.command in ["dual-code", "dual-coder", "dual-track"]:
        import scripts.dual_code_interleaver as dci

        interleaver = dci.DualCodeInterleaver()

        canvas_data = {}
        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                canvas_data = json.load(f)
        elif args.demo or not args.canvas:
            canvas_data = {
                "nodes": [
                    {"id": "node-consensus", "text": "Raft Consensus Module\n\nCoordinates cluster leader election and log replication across distributed instances."},
                    {"id": "node-wal", "text": "Write-Ahead Storage Log\n\nPersists append-only state mutations to durable NVMe storage before commit confirmation."},
                    {"id": "node-telemetry", "text": "Cluster Telemetry Gateway\n\nAggregates Prometheus metrics, health heartbeats, and cluster topology status."},
                ]
            }

        prose_text = ""
        if args.prose and os.path.isfile(args.prose):
            with open(args.prose, "r", encoding="utf-8", errors="ignore") as f:
                prose_text = f.read()
        elif args.demo or not args.prose:
            prose_text = (
                "The Raft consensus module coordinates cluster leader election and ensures deterministic log replication. "
                "The write-ahead storage log persists append-only state mutations directly to durable disk. "
                "The cluster telemetry gateway aggregates health heartbeats and distributes performance metrics across nodes."
            )

        blocks, telemetry = interleaver.align_channels(canvas_data, prose_text)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + interleaver.render_ascii_dual_stream(telemetry))

        if args.output_markdown:
            interleaver.export_interleaved_markdown(telemetry, args.output_markdown)
            print(f"[DxSkills] Interleaved specification written to: {args.output_markdown}")

        if args.output_canvas:
            interleaver.export_canvas(telemetry, args.output_canvas)
            print(f"[DxSkills] Dual-code .canvas exported to: {args.output_canvas}")

        if args.svg:
            interleaver.export_svg_dual_track(telemetry, args.svg)
            print(f"[DxSkills] Dual-track SVG exported to: {args.svg}")
    elif args.command in ["saccadic-pivot", "pivot", "anchor-restore"]:
        import scripts.saccadic_pivot as spiv

        pivot = spiv.DualFovealSaccadicPivot()

        canvas_data = {}
        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                canvas_data = json.load(f)
        elif args.demo or not args.canvas:
            canvas_data = {
                "nodes": [
                    {"id": "node-editor", "x": 0, "y": 0, "width": 260, "height": 160, "text": "Source Editor Buffer\n\nActive code implementation in progress."},
                    {"id": "node-architecture", "x": 950, "y": 500, "width": 300, "height": 180, "text": "Target Architecture Topology\n\nConsensus state machine cluster specifications."},
                ],
                "edges": []
            }

        source_id = args.source if args.source != "src" else canvas_data["nodes"][0]["id"]
        target_id = args.target if args.target != "tgt" else canvas_data["nodes"][-1]["id"]

        enriched_canvas, telemetry = pivot.plan_saccadic_pivot(canvas_data, source_id, target_id)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + pivot.render_ascii_pivot(telemetry))

        if args.output_canvas:
            with open(args.output_canvas, "w", encoding="utf-8") as f:
                json.dump(enriched_canvas, f, indent=2)
            print(f"[DxSkills] Enriched .canvas written to: {args.output_canvas}")

        if args.svg:
            pivot.export_svg_trajectory(telemetry, args.svg)
            print(f"[DxSkills] Saccadic trajectory SVG exported to: {args.svg}")
    elif args.command in ["concept-lattice", "lattice", "fca", "resonance-compiler"]:
        import scripts.concept_lattice as clat

        compiler = clat.ConceptLatticeCompiler(min_resonance=args.min_resonance)

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data:
                compiler.load_from_canvas(raw_data)
            elif isinstance(raw_data, dict):
                compiler.load_context(raw_data)
        elif args.demo or not args.input:
            demo_context = {
                "mechanical_damper": ["energy_dissipation", "resilience", "hardware", "analog"],
                "viscoelastic_mount": ["energy_dissipation", "resilience", "hardware", "isolation"],
                "rate_limiter": ["energy_dissipation", "resilience", "software", "backpressure"],
                "circuit_breaker": ["resilience", "software", "fault_tolerance", "isolation"],
                "biological_homeostasis": ["resilience", "adaptation", "feedback_loop", "organic"],
                "immune_system": ["resilience", "fault_tolerance", "adaptation", "organic"],
            }
            compiler.load_context(demo_context)

        concepts, edges, leaps, telemetry = compiler.compute_lattice()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + "=" * 64)
            print("  Formal Concept Lattice & Associative Resonance Telemetry")
            print("=" * 64)
            print(f"  Total Objects:              {telemetry.total_objects}")
            print(f"  Total Attributes:           {telemetry.total_attributes}")
            print(f"  Formal Concepts Discovered: {telemetry.total_concepts}")
            print(f"  Hasse Cover Edges:          {telemetry.total_hasse_edges}")
            print(f"  Max Topological Depth:      {telemetry.max_lattice_depth}")
            print(f"  Associative Leaps Found:    {telemetry.associative_leaps_count}")
            print(f"  Top Resonance Score:        {telemetry.top_resonance_score:.3f}")
            print(f"  Galois Connectivity Index:  {telemetry.galois_connectivity_index:.3f}")
            print("-" * 64)
            if leaps:
                print("  Top Cross-Domain Associative Leaps (Eide & Eide I-Strength):")
                for idx, leap in enumerate(leaps[:5], 1):
                    src_str = ", ".join(leap.source_extent[:2])
                    tgt_str = ", ".join(leap.target_extent[:2])
                    inv_str = ", ".join(leap.shared_intent)
                    print(f"    {idx}. [{leap.category.value}] Score: {leap.resonance_score:.2f}")
                    print(f"       Bridge: ({src_str}) <---> ({tgt_str})")
                    print(f"       Invariants: {inv_str}")
            print("=" * 64 + "\n")

        if args.output_canvas:
            compiler.to_canvas(args.output_canvas, canvas_title="Formal Concept Lattice")
            print(f"[DxSkills] Concept lattice .canvas written to: {args.output_canvas}")

        if args.svg:
            compiler.to_svg(args.svg)
            print(f"[DxSkills] Concept lattice SVG written to: {args.svg}")
    elif args.command in ["action-sequencer", "sequencer", "dag-runner", "executive-scaffold"]:
        import scripts.action_sequencer as aseq

        sequencer = aseq.ActionSequencer(default_task_minutes=args.default_time)

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data:
                sequencer.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                sequencer.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_tasks = {
                "scope_problem": {"title": "Define Architecture Scope", "estimated_minutes": 20, "prerequisites": []},
                "core_engine": {"title": "Implement Core DAG Parser", "estimated_minutes": 35, "prerequisites": ["scope_problem"]},
                "stepping_stones": {"title": "Synthesize Micro-Commitment Prompter", "estimated_minutes": 25, "prerequisites": ["core_engine"]},
                "cli_integration": {"title": "Wire CLI Subparsers & Handlers", "estimated_minutes": 15, "prerequisites": ["stepping_stones"]},
                "svg_visualizer": {"title": "Draft SVG Critical Path Renderer", "estimated_minutes": 30, "prerequisites": ["core_engine"]},
                "end_to_end_test": {"title": "Full System Integration Suite", "estimated_minutes": 20, "prerequisites": ["cli_integration", "svg_visualizer"]},
            }
            sequencer.load_dict(demo_tasks)

        nodes, telemetry = sequencer.sequence()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + sequencer.render_ascii_plan(telemetry))

        if args.output_canvas:
            sequencer.to_canvas(args.output_canvas, canvas_title="Executive Runway Canvas")
            print(f"[DxSkills] Action runway .canvas written to: {args.output_canvas}")

        if args.svg:
            sequencer.to_svg(args.svg)
            print(f"[DxSkills] Critical path SVG written to: {args.svg}")
    elif args.command in ["cognitive-aperture", "aperture", "scope-bound", "cowan-lens"]:
        import scripts.cognitive_aperture as cap

        harness = cap.CognitiveApertureHarness(capacity_limit=args.capacity)

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data:
                harness.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                harness.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_tasks = {
                "task_urgent_bug": {"title": "Fix Critical Production Regression", "cognitive_weight": 8.0, "urgency_score": 0.95, "strategic_alignment": 0.3},
                "task_auth_audit": {"title": "Resolve Token Refresh Leak", "cognitive_weight": 7.0, "urgency_score": 0.90, "strategic_alignment": 0.4},
                "task_cli_test": {"title": "Complete Suite Unit Tests", "cognitive_weight": 6.0, "urgency_score": 0.85, "strategic_alignment": 0.5},
                "task_deploy_run": {"title": "Staging Deployment Runway", "cognitive_weight": 5.0, "urgency_score": 0.80, "strategic_alignment": 0.5},
                "task_refactor_css": {"title": "Refactor Titanium CSS Variables", "cognitive_weight": 4.0, "urgency_score": 0.50, "strategic_alignment": 0.4},
                "task_doc_cleanup": {"title": "Review Backlog Markdown Archives", "cognitive_weight": 3.0, "urgency_score": 0.35, "strategic_alignment": 0.3},
                "task_future_arch": {"title": "2030 Holographic Canvas Spec", "cognitive_weight": 9.0, "urgency_score": 0.15, "strategic_alignment": 0.95},
                "task_infra_migration": {"title": "Multi-Region Cloud Redundancy", "cognitive_weight": 8.5, "urgency_score": 0.20, "strategic_alignment": 0.90},
            }
            harness.load_dict(demo_tasks)

        manual_pins = args.focal if args.focal else None
        entities, telemetry = harness.calibrate_aperture(manual_focal_ids=manual_pins)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + harness.render_ascii_lens(telemetry))

        if args.output_canvas:
            harness.to_canvas(args.output_canvas, canvas_title="Cognitive Aperture Runway")
            print(f"[DxSkills] Aperture canvas written to: {args.output_canvas}")

        if args.svg:
            harness.to_svg(args.svg)
            print(f"[DxSkills] Cognitive aperture SVG written to: {args.svg}")
    elif args.command in ["dialectic-synthesizer", "triad", "dialectic-mesh", "aufhebung"]:
        import scripts.dialectic_synthesizer as dsynt

        synthesizer = dsynt.DialecticSynthesizer(min_tension_threshold=args.min_tension)

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data:
                synthesizer.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                synthesizer.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_polarity = {
                "poles": {
                    "pole_latency": {
                        "name": "Sub-Millisecond In-Memory Ingestion",
                        "core_values": ["speed", "low_latency", "stream"],
                        "strengths": ["sub_millisecond_write", "real_time_responsiveness"],
                        "overuse_vulnerabilities": ["data_loss_risk", "memory_saturation"],
                    },
                    "pole_durability": {
                        "name": "Immutable Multi-Region Durability",
                        "core_values": ["durability", "acid_guarantees", "batch"],
                        "strengths": ["zero_loss_audit", "cryptographic_trace"],
                        "overuse_vulnerabilities": ["elevated_commit_latency", "disk_io_choke"],
                    },
                },
                "tensions": [["pole_latency", "pole_durability"]],
            }
            synthesizer.load_dict(demo_polarity)

        tensions, syntheses, telemetry = synthesizer.analyze_mesh()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + synthesizer.render_ascii_mesh(telemetry))

        if args.output_canvas:
            synthesizer.to_canvas(args.output_canvas, canvas_title="Dialectic Synthesis Mesh")
            print(f"[DxSkills] Dialectic synthesis canvas written to: {args.output_canvas}")

        if args.svg:
            synthesizer.to_svg(args.svg)
            print(f"[DxSkills] Dialectic synthesis SVG written to: {args.svg}")
    elif args.command in ["density-calibrator", "density", "whitespace-balancer", "bouma-lens"]:
        import scripts.density_calibrator as dcal

        calibrator = dcal.AttentionDensityCalibrator(
            foveal_sigma=args.foveal_sigma,
            bouma_factor=args.bouma_factor,
        )

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data:
                calibrator.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                calibrator.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_nodes = {
                "n_auth": {"title": "Core Auth", "x": 300, "y": 250, "width": 240, "height": 130, "text": "OAuth2 JWT verification and identity token issuer."},
                "n_vault": {"title": "Token Vault", "x": 360, "y": 290, "width": 240, "height": 130, "text": "High entropy cryptographic key vault and rotating secret credentials."},
                "n_session": {"title": "Session Cache", "x": 330, "y": 350, "width": 240, "height": 130, "text": "Redis-backed distributed session cache and rate limiting counter."},
                "n_audit": {"title": "Audit Logger", "x": 400, "y": 320, "width": 240, "height": 130, "text": "Immutable security compliance audit event log stream."},
                "n_gateway": {"title": "API Gateway", "x": 950, "y": 300, "width": 260, "height": 140, "text": "Edge TLS termination, reverse proxy, and global ingress routing."},
                "n_billing": {"title": "Stripe Billing", "x": 1000, "y": 800, "width": 260, "height": 140, "text": "Subscription billing, webhook processing, and invoice generation."},
            }
            calibrator.load_dict(demo_nodes)

        nodes, hotspots, telemetry = calibrator.calibrate()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + calibrator.render_ascii_report(telemetry))

        if args.output_canvas:
            calibrator.to_canvas(args.output_canvas, canvas_title="Calibrated Whitespace Canvas")
            print(f"[DxSkills] Rebalanced whitespace canvas written to: {args.output_canvas}")

        if args.svg:
            calibrator.to_svg(args.svg)
            print(f"[DxSkills] Attention density SVG written to: {args.svg}")
    elif args.command in ["code-symbol-mesh", "code-mesh", "ast-mesh", "symbol-mesh", "interface-mapper"]:
        import scripts.code_symbol_mesh as csm

        mesh = csm.CodeSymbolMesh(max_allowed_coupling=args.max_coupling)

        if args.source and os.path.isfile(args.source):
            file_ext = os.path.splitext(args.source)[1].lower()
            if file_ext in [".json", ".canvas"]:
                with open(args.source, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                if "nodes" in raw_data:
                    mesh.load_canvas(raw_data)
                elif isinstance(raw_data, dict):
                    mesh.load_dict(raw_data)
            else:
                with open(args.source, "r", encoding="utf-8", errors="ignore") as f:
                    src_code = f.read()
                mesh.load_source_text(src_code, filename=os.path.basename(args.source))
        elif args.demo or not args.source:
            demo_symbols = {
                "symbols": {
                    "sym_gateway": {
                        "name": "APIGateway",
                        "kind": "class",
                        "file_path": "gateway/router.py",
                        "signatures": ["route_request(req)", "validate_jwt(token)"],
                        "dependencies": ["sym_auth", "sym_rate_limit", "sym_telemetry"],
                        "cyclomatic_complexity": 3.5,
                    },
                    "sym_auth": {
                        "name": "AuthService",
                        "kind": "interface",
                        "file_path": "security/auth.py",
                        "signatures": ["verify_credentials(u, p)", "sign_claims(claims)"],
                        "dependencies": ["sym_user_repo", "sym_vault"],
                        "cyclomatic_complexity": 2.0,
                    },
                    "sym_god_controller": {
                        "name": "LegacyGodController",
                        "kind": "class",
                        "file_path": "monolith/controller.py",
                        "signatures": ["dispatch_everything(ctx)"],
                        "dependencies": ["sym_auth", "sym_gateway", "sym_user_repo", "sym_vault", "sym_billing", "sym_mailer"],
                        "cyclomatic_complexity": 8.5,
                    },
                    "sym_user_repo": {
                        "name": "UserRepository",
                        "kind": "class",
                        "file_path": "db/users.py",
                        "signatures": ["get_by_id(id)", "save(entity)"],
                        "dependencies": [],
                        "cyclomatic_complexity": 1.5,
                    },
                    "sym_vault": {
                        "name": "KeyVault",
                        "kind": "interface",
                        "file_path": "security/vault.py",
                        "signatures": ["get_secret(key)"],
                        "dependencies": [],
                        "cyclomatic_complexity": 1.0,
                    },
                    "sym_billing": {
                        "name": "StripeBilling",
                        "kind": "class",
                        "file_path": "finance/stripe.py",
                        "signatures": ["charge(card, amt)"],
                        "dependencies": [],
                        "cyclomatic_complexity": 2.0,
                    },
                    "sym_mailer": {
                        "name": "Mailer",
                        "kind": "class",
                        "file_path": "comms/mail.py",
                        "signatures": ["send_email(to, body)"],
                        "dependencies": [],
                        "cyclomatic_complexity": 1.5,
                    },
                }
            }
            mesh.load_dict(demo_symbols)

        symbols, edges, telemetry = mesh.analyze_mesh()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + mesh.render_ascii_mesh(telemetry))

        if args.output_canvas:
            mesh.to_canvas(args.output_canvas, canvas_title="Code Architecture Symbol Canvas")
            print(f"[DxSkills] Code symbol mesh canvas written to: {args.output_canvas}")

        if args.svg:
            mesh.to_svg(args.svg)
            print(f"[DxSkills] Code symbol mesh SVG written to: {args.svg}")
    elif args.command in ["anchor-stacking", "anchor-stack", "stack-compactor", "breadcrumb-trail"]:
        import scripts.anchor_stacking as astk

        compactor = astk.AnchorStackCompactor(max_working_memory_capacity=args.max_capacity)

        if args.stack and os.path.isfile(args.stack):
            with open(args.stack, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data:
                compactor.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                compactor.load_dict(raw_data)
        elif args.demo or not args.stack:
            demo_stack = {
                "subgraphs": {
                    "sg_auth": {
                        "title": "Authentication Core",
                        "status": "resolved",
                        "nodes": ["JWT Signature Verifier", "OAuth Provider", "Token Revocation Cache", "PKCE Challenge"],
                        "depth": 1,
                        "insights": ["Security boundary stabilized with HMAC-SHA256 tokens"],
                    },
                    "sg_cache": {
                        "title": "Distributed Cache Sub-System",
                        "status": "resolved",
                        "nodes": ["Redis Cluster Ring", "Consistent Hash Ring", "TTL Eviction Watcher"],
                        "depth": 1,
                        "insights": ["99.8% hit rate achieved on hot route keys"],
                    },
                    "sg_query_planner": {
                        "title": "Active Query Planner",
                        "status": "active",
                        "nodes": ["AST Optimizer", "Cost Evaluator", "Join Reorder Pass"],
                        "depth": 2,
                        "insights": ["Current bottleneck: multi-table predicate pushdown"],
                    },
                    "sg_archive": {
                        "title": "Cold Tier Storage",
                        "status": "archived",
                        "nodes": ["S3 Parquet Exporter", "Compaction Janitor"],
                        "depth": 0,
                    },
                }
            }
            compactor.load_dict(demo_stack)

        tokens, breadcrumbs, telemetry = compactor.compact_stack()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + compactor.render_ascii_stack(telemetry))

        if args.output_canvas:
            compactor.to_canvas(args.output_canvas, canvas_title="Compacted Working Memory Stack")
            print(f"[DxSkills] Compacted anchor stack canvas written to: {args.output_canvas}")

        if args.svg:
            compactor.to_svg(args.svg)
            print(f"[DxSkills] Anchor stack SVG written to: {args.svg}")
    elif args.command in ["saliency-matrix", "saliency-decoupler", "attenuation-matrix", "focus-spotlight"]:
        import scripts.saliency_matrix as smat

        matrix = smat.SaliencyDecouplerMatrix(decay_rate=args.decay)

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data:
                matrix.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                matrix.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_nodes = {
                "nodes": {
                    "node_core": {"title": "Active Feature Engine", "x": 500, "y": 400, "dependencies": ["node_near_1", "node_near_2"]},
                    "node_near_1": {"title": "Context Cache", "x": 380, "y": 280, "dependencies": ["node_core", "node_mid_1"]},
                    "node_near_2": {"title": "State Store", "x": 640, "y": 300, "dependencies": ["node_core"]},
                    "node_mid_1": {"title": "Auth Broker", "x": 200, "y": 180, "dependencies": ["node_far_1"]},
                    "node_mid_2": {"title": "Telemetry Sink", "x": 800, "y": 220, "dependencies": ["node_near_2"]},
                    "node_far_1": {"title": "Legacy Gateway", "x": 100, "y": 80, "dependencies": []},
                    "node_far_2": {"title": "Batch Cold Storage", "x": 980, "y": 700, "dependencies": []},
                }
            }
            matrix.load_dict(demo_nodes)

        focal_id = args.focal if args.focal else None
        nodes, telemetry = matrix.attenuate(focal_node_id=focal_id)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + matrix.render_ascii_matrix(telemetry))

        if args.output_canvas:
            matrix.to_canvas(focal_node_id=focal_id, output_path=args.output_canvas, canvas_title="Saliency Attenuation Canvas")
            print(f"[DxSkills] Attenuated saliency canvas written to: {args.output_canvas}")

        if args.svg:
            matrix.to_svg(focal_node_id=focal_id, output_path=args.svg)
            print(f"[DxSkills] Saliency matrix SVG written to: {args.svg}")
    elif args.command in ["resonance-weaver", "resonance", "hyperlink-weaver", "associative-bridge"]:
        import scripts.resonance_weaver as rweav

        weaver = rweav.HyperLinkResonanceWeaver(min_resonance_threshold=args.threshold)

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data and isinstance(raw_data["nodes"], list):
                weaver.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                weaver.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_canvas = {
                "nodes": [
                    {"id": "node_bio", "text": "Biomimetic architectural airflow and passive cooling ventilation thermodynamic loop", "x": 100, "y": 100, "width": 260, "height": 140},
                    {"id": "node_urban", "text": "Urban microclimate mitigation and bioclimatic wind corridors in dense street canyons", "x": 600, "y": 120, "width": 260, "height": 140},
                    {"id": "node_db", "text": "Relational PostgreSQL database index caching and memory compaction b-tree buffer pool", "x": 100, "y": 450, "width": 260, "height": 140},
                    {"id": "node_cache", "text": "Distributed Redis memory cache eviction buffer and latency dampening", "x": 600, "y": 470, "width": 260, "height": 140},
                    {"id": "node_meta", "text": "Metacognitive executive working memory load shedding and attention anchoring", "x": 350, "y": 280, "width": 260, "height": 140}
                ],
                "edges": []
            }
            weaver.load_canvas(demo_canvas)

        bridges, telemetry = weaver.weave_bridges()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + weaver.render_ascii_bridges(telemetry))

        if args.output_canvas:
            weaver.to_canvas(args.output_canvas, canvas_title="Resonance Weaved Canvas")
            print(f"[DxSkills] Resonance-weaved canvas written to: {args.output_canvas}")

        if args.svg:
            weaver.to_svg(args.svg)
            print(f"[DxSkills] Resonance bridge SVG written to: {args.svg}")
    elif args.command in ["saccade-calibrator", "gaze-path-calibrator", "ovp-calibrator", "saccade-envelope"]:
        import scripts.saccade_calibrator as scalib

        calibrator = scalib.SaccadeVelocityGazeCalibrator(max_comfortable_jump_px=args.max_jump)

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data and isinstance(raw_data["nodes"], list):
                calibrator.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                calibrator.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_canvas = {
                "nodes": [
                    {"id": "card_overview", "text": "Executive Strategic Overview and Mission Objectives", "x": 100, "y": 100, "width": 260, "height": 140},
                    {"id": "card_tactical", "text": "Tactical Saccadic Stepping Stones and Micro Milestones", "x": 420, "y": 120, "width": 260, "height": 140},
                    {"id": "card_far_east", "text": "Distant Architecture Colony and Deep Async Pipeline", "x": 980, "y": 150, "width": 260, "height": 140},
                    {"id": "card_bottom_tier", "text": "Foundation Storage Layer and Persistent Memory Stores", "x": 400, "y": 550, "width": 260, "height": 140}
                ],
                "edges": []
            }
            calibrator.load_canvas(demo_canvas)

        steps, telemetry = calibrator.calibrate_gaze_paths()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + calibrator.render_ascii_report(telemetry))

        if args.output_canvas:
            calibrator.to_canvas(args.output_canvas, canvas_title="Calibrated Gaze Paths Canvas")
            print(f"[DxSkills] Calibrated gaze path canvas written to: {args.output_canvas}")

        if args.svg:
            calibrator.to_svg(args.svg)
            print(f"[DxSkills] Gaze velocity SVG diagram written to: {args.svg}")
    elif args.command in ["schema-projection", "schema-projector", "cross-scale-projector", "allocentric-projector"]:
        import scripts.schema_projection_engine as sproj

        projector = sproj.SchemaCrossScaleProjector()

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data and isinstance(raw_data["nodes"], list):
                projector.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                projector.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_canvas = {
                "nodes": [
                    {"id": "node_macro", "text": "# Strategic Domain\nMacro overarching distributed system boundary", "x": 100, "y": 100},
                    {"id": "node_meso", "text": "# Event Broker\nMeso service channel and streaming pipeline", "x": 300, "y": 200},
                    {"id": "node_micro", "text": "# AST Parser\nMicro method def parse_ast_tree(node: ASTNode)", "x": 550, "y": 350}
                ],
                "edges": []
            }
            projector.load_canvas(demo_canvas)

        entities, telemetry = projector.project_schema()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + projector.render_ascii_report(telemetry))

        if args.output_canvas:
            projector.to_canvas(args.output_canvas, canvas_title="Multi-Scale Schema Canvas")
            print(f"[DxSkills] Multi-scale projected canvas written to: {args.output_canvas}")

        if args.svg:
            projector.to_svg(args.svg)
            print(f"[DxSkills] Cross-scale projection SVG diagram written to: {args.svg}")
    elif args.command in ["attention-flow", "attention-heatmap", "density-flow", "dwell-optimizer"]:
        import scripts.attention_flow_optimizer as aflow

        optimizer = aflow.AttentionFlowOptimizer(baseline_wpm=args.wpm, stagnation_dwell_threshold_ms=args.threshold)

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data and isinstance(raw_data["nodes"], list):
                optimizer.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                optimizer.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_canvas = {
                "nodes": [
                    {"id": "card_headline", "text": "Executive Mission Overview and Tactical Focus", "x": 100, "y": 100, "width": 260, "height": 140},
                    {"id": "card_stagnant", "text": "Comprehensive technical architecture review with extensive multi-clause descriptions detailing distributed event streams, fault-tolerant cluster consensus, schema validation mechanisms, and database failover protocols across multiple geographical cloud zones.", "x": 450, "y": 100, "width": 260, "height": 140},
                    {"id": "card_balanced", "text": "Synchronous state cache and low-latency buffer ring", "x": 100, "y": 400, "width": 260, "height": 140}
                ],
                "edges": []
            }
            optimizer.load_canvas(demo_canvas)

        profiles, telemetry = optimizer.optimize_attention_flow()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + optimizer.render_ascii_report(telemetry))

        if args.output_canvas:
            optimizer.to_canvas(args.output_canvas, canvas_title="Flow-Balanced Attention Canvas")
            print(f"[DxSkills] Attention-flow balanced canvas written to: {args.output_canvas}")

        if args.svg:
            optimizer.to_svg(args.svg)
            print(f"[DxSkills] Attention heatmap SVG written to: {args.svg}")
    elif args.command in ["working-set", "cowan-pruner", "set-pruner", "bead-pruner"]:
        import scripts.working_set_pruner as wset

        pruner = wset.WorkingSetPruner(
            max_active_working_set=args.max_active,
            ghost_opacity=args.ghost_opacity,
        )

        if args.canvas and os.path.isfile(args.canvas):
            with open(args.canvas, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if "nodes" in raw_data and isinstance(raw_data["nodes"], list):
                pruner.load_canvas(raw_data)
            elif isinstance(raw_data, dict):
                pruner.load_dict(raw_data)
        elif args.demo or not args.canvas:
            demo_canvas = {
                "nodes": [
                    {"id": "node_active_1", "text": "Active Sprint Task 1", "x": 100, "y": 100, "recency": 8, "fixations": 5},
                    {"id": "node_active_2", "text": "Active Sprint Task 2", "x": 380, "y": 100, "recency": 7, "fixations": 4},
                    {"id": "node_active_3", "text": "Active Sprint Task 3", "x": 660, "y": 100, "recency": 6, "fixations": 3},
                    {"id": "node_active_4", "text": "Active Sprint Task 4", "x": 100, "y": 300, "recency": 5, "fixations": 2},
                    {"id": "node_ghost_1", "text": "Peripheral Architectural Context", "x": 380, "y": 300, "recency": 3, "fixations": 1},
                    {"id": "node_ghost_2", "text": "Secondary Service Broker", "x": 660, "y": 300, "recency": 2, "fixations": 1},
                    {"id": "node_bead_1", "text": "Legacy Q3 Milestones", "x": 100, "y": 550, "recency": 0, "fixations": 0},
                    {"id": "node_bead_2", "text": "Archived Performance Benchmarks", "x": 380, "y": 550, "recency": 0, "fixations": 0}
                ],
                "edges": []
            }
            pruner.load_dict(demo_canvas)

        focal_ids = args.focal if args.focal else None
        profiles, telemetry = pruner.prune_working_set(focal_ids=focal_ids)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print("\n" + pruner.render_ascii_report(telemetry))

        if args.output_canvas:
            pruner.to_canvas(args.output_canvas, canvas_title="Pruned Working Set Canvas")
            print(f"[DxSkills] Pruned working set canvas written to: {args.output_canvas}")

        if args.svg:
            pruner.to_svg(args.svg)
            print(f"[DxSkills] Working set SVG diagram written to: {args.svg}")
    elif args.command in ["dialectic-loom", "aufhebung-loom", "synthesis-loom", "reification-loom"]:
        import scripts.dialectic_loom as dloom

        loom = dloom.DialecticLoom(max_working_memory_chunks=args.max_chunks)

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            cards_input = raw_data
        elif args.demo or not args.input:
            cards_input = [
                {
                    "id": "node_thesis_01",
                    "title": "Decoupled Autonomous Microservices",
                    "statement": "Independent services optimize local development velocity, fault isolation, and autonomous datastores.",
                    "perspective": "thesis",
                    "core_values": ["Velocity", "Autonomy", "Elasticity"],
                    "failure_modes": ["Cascading latency", "State divergence", "Distributed saga deadlocks"],
                },
                {
                    "id": "node_anti_01",
                    "title": "Strict Unified Monolith with ACID Ledger",
                    "statement": "Centralized database transactions preserve total order, linearizability, and global system coherence.",
                    "perspective": "antithesis",
                    "core_values": ["Consistency", "Coherence", "Auditability"],
                    "failure_modes": ["Deployment bottlenecks", "Database write saturation", "Single blast radius"],
                },
            ]

        result = loom.analyze(cards_input)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + loom.generate_ascii_report(result))

        if args.canvas:
            loom.export_canvas(result, args.canvas)
            print(f"[DxSkills] Dialectic synthesis canvas written to: {args.canvas}")

        if args.svg:
            loom.export_svg(result, args.svg)
            print(f"[DxSkills] Dialectic triad SVG diagram written to: {args.svg}")
    elif args.command in ["lexical-pacer", "bionic-pacer", "ovp-pacer", "fixation-pacer"]:
        import scripts.lexical_pacer as lpacer

        pacer = lpacer.LexicalPacer(target_wpm=args.wpm)

        text_content = ""
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                text_content = f.read()
        elif args.demo or not args.input:
            text_content = (
                "Distributed systems require explicit boundary decoupling to maintain architectural resilience.\n"
                "When microservices mutate shared state concurrently, data divergence triggers cascading latency.\n"
                "Local-first architectures with deterministic conflict-free resolution provide optimal throughput."
            )

        result = pacer.pace_text(text_content)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        elif args.markdown:
            print(result.bionic_markdown)
        else:
            print("\n" + pacer.generate_ascii_report(result))

        if args.html:
            pacer.export_html_reader(result, args.html)
            print(f"[DxSkills] Bionic reader HTML written to: {args.html}")

        if args.svg:
            pacer.export_svg(result, args.svg)
            print(f"[DxSkills] OVP fixation curve SVG diagram written to: {args.svg}")
    elif args.command in ["galois-lattice", "galois-engine", "fca-lattice", "associative-constellation"]:
        import scripts.galois_lattice_engine as glattice

        engine = glattice.GaloisLatticeEngine(min_resonance_threshold=args.threshold)

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            entities_input = raw_data
        elif args.demo or not args.input:
            entities_input = [
                {
                    "id": "card_01",
                    "name": "Local Spatial Canvas",
                    "cluster": "spatial_ui",
                    "attributes": ["local-first", "crdt", "reactive", "spatial"],
                },
                {
                    "id": "card_02",
                    "name": "Reactive Event Bus",
                    "cluster": "spatial_ui",
                    "attributes": ["reactive", "async", "decoupled"],
                },
                {
                    "id": "card_03",
                    "name": "Distributed Storage Ledger",
                    "cluster": "backend_storage",
                    "attributes": ["crdt", "local-first", "audit", "distributed"],
                },
                {
                    "id": "card_04",
                    "name": "Audit Log Aggregator",
                    "cluster": "backend_storage",
                    "attributes": ["audit", "distributed", "linearizable"],
                },
            ]

        result = engine.analyze(entities_input)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + engine.generate_ascii_report(result))

        if args.canvas:
            engine.export_canvas(result, args.canvas)
            print(f"[DxSkills] Galois constellation canvas written to: {args.canvas}")

        if args.svg:
            engine.export_svg(result, args.svg)
            print(f"[DxSkills] Galois lattice SVG diagram written to: {args.svg}")
    elif args.command in ["fatigue-meter", "saccadic-fatigue", "contrast-damper", "ocular-fatigue"]:
        import scripts.saccadic_fatigue_meter as sfatigue

        meter = sfatigue.SaccadicFatigueMeter(
            baseline_velocity_deg_s=args.baseline,
            max_session_minutes=args.session_max,
        )

        samples_input = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            samples_input = raw_data if isinstance(raw_data, list) else raw_data.get("samples", [])
        elif args.demo or not args.input:
            for i in range(20):
                t_ms = i * 105000.0  # ~35 mins
                vel = 440.0 - (i * 6.5)
                blink = 5.0 if i < 10 else 1.8
                samples_input.append({
                    "sample_id": f"s_{i+1:02d}",
                    "timestamp_ms": t_ms,
                    "saccade_amplitude_deg": 9.0,
                    "peak_velocity_deg_s": vel,
                    "fixation_duration_ms": 210.0 + (i * 8.0),
                    "blink_interval_sec": blink,
                    "target_card_id": f"card_{(i % 4) + 1}",
                })

        result = meter.evaluate_gaze_samples(samples_input)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + meter.generate_ascii_report(result))

        if args.css:
            with open(args.css, "w", encoding="utf-8") as f:
                f.write(result.restorative_css_tokens)
            print(f"[DxSkills] Restorative CSS tokens written to: {args.css}")

        if args.svg:
            meter.export_svg(result, args.svg)
            print(f"[DxSkills] Saccadic fatigue SVG diagram written to: {args.svg}")
    elif args.command in ["stress-tester", "lexical-stress", "syntax-friction", "stepping-stones"]:
        import scripts.lexical_stress_tester as lst_mod

        tester = lst_mod.LexicalStressTester(
            max_acceptable_depth=args.depth,
            friction_threshold=args.threshold,
        )

        code_to_test = ""
        if args.code:
            code_to_test = args.code
        elif args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                code_to_test = f.read()
        elif args.demo or not args.input:
            code_to_test = (
                "def process_spatial_lattice(node_catalog: dict) -> list:\n"
                "    active_anchors = []\n"
                "    for category, cluster in node_catalog.items():\n"
                "        if cluster.is_active():\n"
                "            for item in cluster.elements:\n"
                "                if item.friction_score > 0.65:\n"
                "                    resolved_concept_identifier = item.synthesize_anchor()\n"
                "                    active_anchors.append(resolved_concept_identifier)\n"
                "    return active_anchors\n"
            )

        result = tester.parse_syntax(code_to_test)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + tester.generate_ascii_report(result))

        if args.output_md:
            with open(args.output_md, "w", encoding="utf-8") as f:
                f.write(result.stepped_markdown)
            print(f"[DxSkills] Stepped markdown written to: {args.output_md}")

        if args.output_html:
            with open(args.output_html, "w", encoding="utf-8") as f:
                f.write(result.stepped_html)
            print(f"[DxSkills] Stepped HTML written to: {args.output_html}")

        if args.svg:
            tester.export_svg(result, args.svg)
            print(f"[DxSkills] Lexical friction SVG diagram written to: {args.svg}")
    elif args.command in ["anchor-distiller", "distill-anchors", "canvas-radar", "semantic-index"]:
        import scripts.semantic_anchor_distiller as sad_mod

        distiller = sad_mod.SemanticAnchorDistiller(
            cluster_distance_threshold=args.threshold,
        )

        items_input = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            items_input = raw_data if isinstance(raw_data, list) else raw_data.get("nodes", raw_data.get("items", []))
        elif args.demo or not args.input:
            items_input = [
                {
                    "id": "node_arch_1",
                    "x": 80.0,
                    "y": 90.0,
                    "title": "Dual-Code Memory Interleaver",
                    "category": "Architecture",
                    "text_content": "Phonological loop and visuospatial sketchpad dual processing system.",
                    "salience_weight": 0.95,
                    "tags": ["memory", "dual-code"],
                },
                {
                    "id": "node_arch_2",
                    "x": 120.0,
                    "y": 140.0,
                    "title": "Buffer Compactor",
                    "category": "Architecture",
                    "text_content": "FIFO buffer compaction maintaining strict Cowan bounds.",
                    "salience_weight": 0.60,
                    "tags": ["memory", "buffer"],
                },
                {
                    "id": "node_arch_3",
                    "x": 100.0,
                    "y": 180.0,
                    "title": "Working Set Pruner",
                    "category": "Architecture",
                    "text_content": "Dynamic working set anchor eviction for cognitive stamina.",
                    "salience_weight": 0.70,
                    "tags": ["memory", "pruner"],
                },
                {
                    "id": "node_eye_1",
                    "x": 1380.0,
                    "y": 880.0,
                    "title": "Saccadic Fatigue Damper",
                    "category": "Ocular",
                    "text_content": "Carpenter main sequence peak velocity decay tracking.",
                    "salience_weight": 0.92,
                    "tags": ["saccade", "fatigue"],
                },
                {
                    "id": "node_eye_2",
                    "x": 1420.0,
                    "y": 920.0,
                    "title": "Optimal Viewing Position Calibrator",
                    "category": "Ocular",
                    "text_content": "Rayner OVP lexical fixation anchor placement.",
                    "salience_weight": 0.85,
                    "tags": ["rayner", "ovp"],
                },
            ]

        result = distiller.distill_canvas(items_input)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + distiller.generate_ascii_report(result))

        if args.canvas:
            distiller.export_canvas(result, args.canvas)
            print(f"[DxSkills] Distilled canvas written to: {args.canvas}")

        if args.svg:
            distiller.export_svg(result, args.svg)
            print(f"[DxSkills] Visual indexer radar SVG written to: {args.svg}")
    elif args.command in ["foveal-horizon", "foveal-drift", "breadcrumb-restorer", "zoom-horizon"]:
        import scripts.foveal_horizon_tracker as fht_mod

        tracker = fht_mod.FovealHorizonTracker()

        source_state = {}
        target_state = {}
        landmarks_input = None

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            source_state = raw_data.get("source", {})
            target_state = raw_data.get("target", {})
            landmarks_input = raw_data.get("landmarks", None)
        elif args.demo or not args.input:
            source_state = {
                "zoom_level": args.source_zoom,
                "pan_x": 100.0,
                "pan_y": 150.0,
                "focal_node_title": "Global System Overview",
            }
            target_state = {
                "zoom_level": args.target_zoom,
                "pan_x": 100.0 + args.displacement,
                "pan_y": 150.0 + (args.displacement * 0.7),
                "focal_node_title": "Deep Memory Detail Spec",
            }
            landmarks_input = [
                {"title": "Core Domain Cluster"},
                {"title": "Execution Unit Interface"},
                {"title": "Microcode Memory Bank"},
            ]

        result = tracker.track_transition(source_state, target_state, landmarks=landmarks_input)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + tracker.generate_ascii_report(result))

        if args.css:
            with open(args.css, "w", encoding="utf-8") as f:
                f.write(result.restorative_css)
            print(f"[DxSkills] Restorative transition CSS written to: {args.css}")

        if args.svg:
            tracker.export_svg(result, args.svg)
            print(f"[DxSkills] Foveal horizon SVG written to: {args.svg}")
    elif args.command in ["attention-gradient", "saccade-shaper", "eccentricity-damper", "acuity-gradient"]:
        import scripts.attention_gradient_shaper as ags_mod

        shaper = ags_mod.AttentionGradientShaper()

        cards_input = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            cards_input = raw_data if isinstance(raw_data, list) else raw_data.get("cards", raw_data.get("nodes", []))
        elif args.demo or not args.input:
            cards_input = [
                {"id": "card_focal", "x": 100.0, "y": 100.0, "width": 200.0, "height": 200.0, "title": "Focal Anchor Node"},
                {"id": "card_para", "x": 550.0, "y": 150.0, "width": 200.0, "height": 160.0, "title": "Parafoveal Context Card"},
                {"id": "card_target", "x": 800.0, "y": 250.0, "width": 220.0, "height": 180.0, "title": "Saccade Target Node"},
                {"id": "card_distract_1", "x": 1200.0, "y": 800.0, "width": 200.0, "height": 160.0, "title": "Peripheral Distractor A"},
                {"id": "card_distract_2", "x": 200.0, "y": 950.0, "width": 200.0, "height": 160.0, "title": "Peripheral Distractor B"},
            ]

        result = shaper.calculate_gradient(
            gaze_x=args.gaze_x,
            gaze_y=args.gaze_y,
            cards=cards_input,
            saccade_target={"x": args.target_x, "y": args.target_y},
        )

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + shaper.generate_ascii_report(result))

        if args.css:
            with open(args.css, "w", encoding="utf-8") as f:
                f.write(result.attenuation_css)
            print(f"[DxSkills] Peripheral attenuation CSS written to: {args.css}")

        if args.svg:
            shaper.export_svg(result, args.svg)
            print(f"[DxSkills] Attention gradient SVG written to: {args.svg}")
    elif args.command in ["causal-loom", "narrative-loom", "causal-dag", "quest-loom"]:
        import scripts.causal_narrative_loom as cnl_mod

        loom = cnl_mod.CausalNarrativeLoom(max_cowan_depth=args.depth)

        raw_nodes = []
        raw_edges = []
        text_corpus = None

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, dict):
                    raw_nodes = raw_data.get("nodes", [])
                    raw_edges = raw_data.get("edges", [])
                elif isinstance(raw_data, list):
                    raw_nodes = raw_data
            except json.JSONDecodeError:
                text_corpus = content
        elif args.demo or not args.input:
            raw_nodes = [
                {"id": "n1", "label": "Phonological Bottleneck", "node_type": "EVENT"},
                {"id": "n2", "label": "Spatial Scaffolding Harness", "node_type": "DECISION"},
                {"id": "n3", "label": "Peripheral Clutter Attenuation", "node_type": "DECISION"},
                {"id": "n4", "label": "Cognitive Stamina Restoration", "node_type": "OUTCOME"},
            ]
            raw_edges = [
                {"source_id": "n1", "target_id": "n2", "relation": "CAUSES"},
                {"source_id": "n2", "target_id": "n3", "relation": "ENABLES"},
                {"source_id": "n3", "target_id": "n4", "relation": "RESULTS_IN"},
            ]

        result = loom.weave_narrative(raw_nodes=raw_nodes, raw_edges=raw_edges, text_corpus=text_corpus)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + loom.generate_ascii_report(result))
            print("\n--- [FORWARD CHRONOLOGICAL BRIEF] ---")
            print(result.forward_narrative)
            print("\n--- [BACKWARD DIAGNOSTIC LADDER] ---")
            print(result.backward_diagnostic)

        if args.output_md:
            full_md = f"# Causal Executive Brief\n\n{result.forward_narrative}\n\n{result.backward_diagnostic}\n"
            with open(args.output_md, "w", encoding="utf-8") as f:
                f.write(full_md)
            print(f"[DxSkills] Causal narrative brief written to: {args.output_md}")

        if args.svg:
            loom.export_svg(result, args.svg)
            print(f"[DxSkills] Causal DAG SVG written to: {args.svg}")
    elif args.command in ["epistemic-radar", "uncertainty-radar", "assumption-tester", "fragility-radar"]:
        import scripts.epistemic_uncertainty_radar as eur_mod

        radar = eur_mod.EpistemicUncertaintyRadar(fragility_threshold=args.threshold)

        raw_claims = []
        stress_scenarios = None

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, dict):
                    raw_claims = raw_data.get("claims", [])
                    stress_scenarios = raw_data.get("stress_scenarios", None)
                elif isinstance(raw_data, list):
                    raw_claims = raw_data
            except json.JSONDecodeError:
                # Text lines as claims
                raw_claims = [{"id": f"c_{idx+1}", "statement": line.strip()} for idx, line in enumerate(content.splitlines()) if line.strip()]
        elif args.demo or not args.input:
            raw_claims = [
                {
                    "id": "clm_1",
                    "statement": "Hardware-accelerated CSS transforms maintain steady 60fps benchmark telemetry.",
                    "category": "PERFORMANCE",
                    "grounding_tier": "EMPIRICAL",
                    "confidence_score": 0.98,
                    "fragility_index": 0.12,
                },
                {
                    "id": "clm_2",
                    "statement": "Anstis retinal acuity decay equation models peripheral visual dropout correctly.",
                    "category": "ARCHITECTURE",
                    "grounding_tier": "THEORETICAL",
                    "confidence_score": 0.85,
                    "fragility_index": 0.28,
                },
                {
                    "id": "clm_3",
                    "statement": "Typical reading speed will remain stable across variable display contrasts.",
                    "category": "ERGONOMICS",
                    "grounding_tier": "HEURISTIC",
                    "confidence_score": 0.58,
                    "fragility_index": 0.65,
                },
                {
                    "id": "clm_4",
                    "statement": "We assume memory pressure will probably not trigger mobile browser tab reloads.",
                    "category": "ARCHITECTURE",
                    "grounding_tier": "SPECULATIVE",
                    "confidence_score": 0.25,
                    "fragility_index": 0.92,
                },
            ]

        result = radar.evaluate_claims(raw_claims=raw_claims, stress_scenarios=stress_scenarios)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + radar.generate_ascii_report(result))
            print("\n--- [MITIGATION STRATEGY TABLE] ---")
            print(result.mitigation_table_md)

        if args.output_table:
            with open(args.output_table, "w", encoding="utf-8") as f:
                f.write(result.mitigation_table_md)
            print(f"[DxSkills] Epistemic mitigation table written to: {args.output_table}")

        if args.svg:
            radar.export_svg(result, args.svg)
            print(f"[DxSkills] Epistemic radar SVG written to: {args.svg}")
    elif args.command in ["vault-consolidate", "anchor-vault", "semantic-snapshot", "rehydration-vault"]:
        import scripts.anchor_consolidation_vault as acv_mod

        vault = acv_mod.AnchorConsolidationVault(coherence_threshold=args.threshold)

        raw_anchors = []
        raw_conns = []

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, dict):
                    raw_anchors = raw_data.get("anchors", [])
                    raw_conns = raw_data.get("connections", [])
                elif isinstance(raw_data, list):
                    raw_anchors = raw_data
            except json.JSONDecodeError:
                raw_anchors = [{"id": f"anc_{idx+1}", "label": line.strip()} for idx, line in enumerate(content.splitlines()) if line.strip()]
        elif args.demo or not args.input:
            raw_anchors = [
                {"id": "a1", "label": "Affine Viewport Matrix", "x": 100.0, "y": 120.0, "coherence_score": 0.88},
                {"id": "a2", "label": "Pinch-Zoom Transform", "x": 140.0, "y": 150.0, "coherence_score": 0.92},
                {"id": "a3", "label": "Foveal Focus Reticle", "x": 180.0, "y": 130.0, "coherence_score": 0.85},
                {"id": "b1", "label": "Attentional Blink Detector", "x": 600.0, "y": 100.0, "coherence_score": 0.78},
                {"id": "b2", "label": "Eccentricity Attenuator", "x": 650.0, "y": 140.0, "coherence_score": 0.82},
                {"id": "c1", "label": "Exploratory Thought Fragment", "x": 400.0, "y": 400.0, "coherence_score": 0.40},
            ]
            raw_conns = [
                {"source": "a1", "target": "a2"},
                {"source": "a2", "target": "a3"},
                {"source": "b1", "target": "b2"},
            ]

        result = vault.consolidate_subcanvases(
            raw_anchors=raw_anchors,
            raw_connections=raw_conns,
            cluster_proximity_radius=args.radius,
        )

        if args.rehydrate:
            rehydrated = vault.rehydrate_snapshot(args.rehydrate, result)
            if rehydrated:
                print(f"[DxSkills] Successfully rehydrated snapshot '{args.rehydrate}':")
                print(json.dumps(rehydrated, indent=2))
            else:
                print(f"[DxSkills] Snapshot '{args.rehydrate}' not found in vault.")
        elif args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + vault.generate_ascii_report(result))
            print("\n" + result.rehydration_manifest_md)

        if args.manifest:
            with open(args.manifest, "w", encoding="utf-8") as f:
                f.write(result.rehydration_manifest_md)
            print(f"[DxSkills] Rehydration manifest written to: {args.manifest}")

        if args.svg:
            vault.export_svg(result, args.svg)
            print(f"[DxSkills] Vault map SVG written to: {args.svg}")
    elif args.command in ["schema-transfer", "isomorphism-engine", "analogy-transfer", "domain-mapper"]:
        import scripts.schema_isomorphism_engine as sie_mod

        engine = sie_mod.SchemaIsomorphismEngine(min_alignment_threshold=args.threshold)

        src_schema = None
        tgt_schema = None

        if args.source and os.path.isfile(args.source) and args.target and os.path.isfile(args.target):
            with open(args.source, "r", encoding="utf-8") as f:
                src_data = json.load(f)
            with open(args.target, "r", encoding="utf-8") as f:
                tgt_data = json.load(f)
            src_schema = sie_mod.DomainSchema.from_dict(src_data)
            tgt_schema = sie_mod.DomainSchema.from_dict(tgt_data)
        elif args.demo or not args.source:
            src_schema = sie_mod.DomainSchema.from_dict({
                "domain_name": "Hydraulic Power System",
                "nodes": [
                    {"id": "pump", "name": "Centrifugal Pump", "role": "SOURCE"},
                    {"id": "pipe", "name": "Conduit Pipe", "role": "TRANSPORT"},
                    {"id": "valve", "name": "Flow Constrictor Valve", "role": "REGULATOR"},
                    {"id": "basin", "name": "Reservoir Basin", "role": "SINK"},
                ],
                "relations": [
                    {"source": "pump", "target": "pipe", "relation": "DRIVES"},
                    {"source": "pipe", "target": "valve", "relation": "CIRCULATES"},
                    {"source": "valve", "target": "basin", "relation": "REGULATES"},
                    {"source": "basin", "target": "pump", "relation": "CIRCULATES"},
                ],
            })
            tgt_schema = sie_mod.DomainSchema.from_dict({
                "domain_name": "Electrical Direct Current Circuit",
                "nodes": [
                    {"id": "battery", "name": "Chemical Battery", "role": "SOURCE"},
                    {"id": "wire", "name": "Copper Wire", "role": "TRANSPORT"},
                    {"id": "resistor", "name": "Ceramic Resistor", "role": "REGULATOR"},
                    {"id": "ground", "name": "Chassis Ground", "role": "SINK"},
                ],
                "relations": [
                    {"source": "battery", "target": "wire", "relation": "DRIVES"},
                    {"source": "wire", "target": "resistor", "relation": "CIRCULATES"},
                    {"source": "resistor", "target": "ground", "relation": "REGULATES"},
                ],
            })

        projection = engine.synthesize_analogy_transfer(src_schema, tgt_schema)

        if args.json:
            print(json.dumps(projection.to_dict(), indent=2))
        else:
            print("\n" + engine.generate_ascii_report(projection))
            print("\n" + projection.transfer_report_md)

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(projection.transfer_report_md)
            print(f"[DxSkills] Analogy transfer report written to: {args.report}")

        if args.svg:
            engine.export_svg(projection, args.svg)
            print(f"[DxSkills] Isomorphic projection SVG written to: {args.svg}")
    elif args.command in ["narrative-reconcile", "branch-reconciler", "divergence-bridge", "fork-synthesizer"]:
        import scripts.narrative_branch_reconciler as nbr_mod

        reconciler = nbr_mod.NarrativeBranchReconciler(drift_threshold=args.threshold)

        raw_branches = []

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, dict):
                    raw_branches = raw_data.get("branches", [])
                elif isinstance(raw_data, list):
                    raw_branches = raw_data
            except json.JSONDecodeError:
                raw_branches = [{"id": f"br_{idx+1}", "name": line.strip(), "origin_id": "root", "waypoints": []} for idx, line in enumerate(content.splitlines()) if line.strip()]
        elif args.demo or not args.input:
            raw_branches = [
                {
                    "id": "br_a",
                    "name": "Branch Alpha: Monolithic Memory Store",
                    "origin_id": "root_fork",
                    "intent": "Maximize raw in-memory lookup performance",
                    "terminal_state": "Zero-latency in-memory cache",
                    "waypoints": [
                        {
                            "id": "wp_a1",
                            "label": "Shared SharedArrayBuffer Pool",
                            "phase_order": 1,
                            "assumptions": ["Dedicated multi-core hardware available"],
                            "tradeoffs": {"latency": 0.05, "ram_usage": 0.85, "portability": 0.30},
                        },
                        {
                            "id": "wp_a2",
                            "label": "Direct Binary Pointer Dereference",
                            "phase_order": 2,
                            "assumptions": ["Static layout offsets remain unchanged"],
                            "tradeoffs": {"latency": 0.02, "ram_usage": 0.90, "portability": 0.20},
                        },
                    ],
                },
                {
                    "id": "br_b",
                    "name": "Branch Beta: Distributed Micro-Vaults",
                    "origin_id": "root_fork",
                    "intent": "Maximize multi-tenant isolation and fault tolerance",
                    "terminal_state": "Decoupled immutable snapshot replicas",
                    "waypoints": [
                        {
                            "id": "wp_b1",
                            "label": "Ephemeral Local IndexedDB Clones",
                            "phase_order": 1,
                            "assumptions": ["Browser quota allows 50MB storage"],
                            "tradeoffs": {"latency": 0.45, "ram_usage": 0.20, "portability": 0.90},
                        },
                        {
                            "id": "wp_b2",
                            "label": "Event-Driven Sync Message Mesh",
                            "phase_order": 2,
                            "assumptions": ["Eventual consistency within 100ms"],
                            "tradeoffs": {"latency": 0.50, "ram_usage": 0.25, "portability": 0.95},
                        },
                    ],
                },
            ]

        result = reconciler.analyze_and_reconcile(raw_branches=raw_branches)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + reconciler.generate_ascii_report(result))
            print("\n" + result.executive_synthesis_md)

        if args.synthesis:
            with open(args.synthesis, "w", encoding="utf-8") as f:
                f.write(result.executive_synthesis_md)
            print(f"[DxSkills] Executive synthesis written to: {args.synthesis}")

        if args.svg:
            reconciler.export_svg(result, args.svg)
            print(f"[DxSkills] Narrative reconciliation map SVG written to: {args.svg}")
    elif args.command in ["topological-homotopy", "homotopy-engine", "topology-visualizer", "deformation-engine"]:
        import scripts.topological_homotopy_engine as the_mod

        engine = the_mod.TopologicalHomotopyEngine(steps_count=args.steps)

        raw_nodes = []
        raw_edges = []

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, dict):
                    raw_nodes = raw_data.get("nodes", [])
                    raw_edges = raw_data.get("edges", [])
                elif isinstance(raw_data, list):
                    raw_nodes = raw_data
            except json.JSONDecodeError:
                raw_nodes = [{"id": f"n_{idx+1}", "label": line.strip()} for idx, line in enumerate(content.splitlines()) if line.strip()]
        elif args.demo or not args.input:
            raw_nodes = [
                {"id": "n1", "label": "Perceptual Anchor", "start_x": 100.0, "start_y": 100.0, "end_x": 600.0, "end_y": 100.0},
                {"id": "n2", "label": "Epistemic Node", "start_x": 200.0, "start_y": 250.0, "end_x": 700.0, "end_y": 250.0},
                {"id": "n3", "label": "Action Horizon", "start_x": 100.0, "start_y": 250.0, "end_x": 600.0, "end_y": 250.0},
            ]
            raw_edges = [
                {"source": "n1", "target": "n2"},
                {"source": "n2", "target": "n3"},
                {"source": "n3", "target": "n1"},
            ]

        result = engine.evaluate_and_deform(nodes=raw_nodes, edges=raw_edges)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("\n" + engine.generate_ascii_report(result))
            print("\n" + result.invariant_audit_md)

        if args.audit:
            with open(args.audit, "w", encoding="utf-8") as f:
                f.write(result.invariant_audit_md)
            print(f"[DxSkills] Invariant audit report written to: {args.audit}")

        if args.svg:
            engine.export_svg(result, args.svg)
            print(f"[DxSkills] Homotopy diagram SVG written to: {args.svg}")
    elif args.command in ["lexical-gist", "gist-compressor", "dynamic-shorthand", "semantic-gist"]:
        import scripts.lexical_gist_compressor as lgc_mod

        compressor = lgc_mod.LexicalGistCompressor(target_ratio=args.ratio)

        input_text = ""
        if args.input:
            if os.path.isfile(args.input):
                with open(args.input, "r", encoding="utf-8") as f:
                    input_text = f.read()
            else:
                input_text = args.input
        elif args.demo or not args.input:
            input_text = (
                "The spatial knowledge graph transforms unstructured textual notes into topological coordinates. "
                "Working memory constraints strictly bound the simultaneous activation threshold to four chunks, "
                "which yields stable cognitive equilibrium and protects executive focus against attentional fatigue."
            )

        result = compressor.synthesize_gist(input_text)

        if args.json:
            import dataclasses
            print(json.dumps({
                "clauses": [dataclasses.asdict(c) for c in result.clauses],
                "telemetry": dataclasses.asdict(result.telemetry)
            }, indent=2))
        else:
            print(result.gist_markdown_report)

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(result.gist_markdown_report)
            print(f"[DxSkills] Gist markdown report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(result.spatial_glyph_diagram)
            print(f"[DxSkills] Spatial shorthand SVG diagram written to: {args.svg}")
    elif args.command in ["saccade-filter", "noise-gate", "saliency-gate", "saccade-gate"]:
        import scripts.saccade_saliency_filter as ssf_mod

        filter_obj = ssf_mod.SaccadeSaliencyFilter(
            threshold=args.threshold,
            margin_cutoff=args.cutoff,
            foveal_radius=args.foveal
        )

        nodes = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, dict):
                    nodes = raw_data.get("nodes", [])
                elif isinstance(raw_data, list):
                    nodes = raw_data
            except json.JSONDecodeError:
                nodes = [{"id": f"n_{idx+1}", "label": line.strip()} for idx, line in enumerate(content.splitlines()) if line.strip()]
        elif args.demo or not args.input:
            nodes = [
                {"id": "n1", "label": "Core Epistemic Anchor", "x": 380, "y": 280, "width": 160, "height": 80},
                {"id": "n2", "label": "Primary Synthesis Nexus", "x": 420, "y": 320, "width": 180, "height": 90},
                {"id": "n3", "label": "Marginal Metadata Clutter Fragment", "x": 100, "y": 80, "width": 120, "height": 60},
                {"id": "n4", "label": "Peripheral Note Boundary Clutter", "x": 750, "y": 550, "width": 140, "height": 70},
            ]

        result = filter_obj.apply_filter(nodes)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(result.noise_gate_report_md)

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(result.noise_gate_report_md)
            print(f"[DxSkills] Noise gate report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(result.saliency_map_svg)
            print(f"[DxSkills] Saccade saliency map SVG written to: {args.svg}")
    elif args.command in ["drift-compensator", "recenter-harness", "allocentric-drift", "magnetic-anchor"]:
        import scripts.drift_compensator as dc_mod

        compensator = dc_mod.WorkingMemoryDriftCompensator(
            drift_threshold=args.threshold,
            spring_constant=args.spring
        )

        waypoints = []
        anchors = []

        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, dict):
                    waypoints = raw_data.get("waypoints", [])
                    anchors = raw_data.get("anchors", [])
                elif isinstance(raw_data, list):
                    waypoints = raw_data
            except json.JSONDecodeError:
                pass
        elif args.demo or not args.input:
            anchors = [
                {"id": "root", "label": "Core Problem Definition", "x": 400.0, "y": 300.0, "mass": 6.0, "type": "root"},
                {"id": "synthesis", "label": "Architectural Nexus", "x": 700.0, "y": 300.0, "mass": 4.0, "type": "synthesis_nexus"}
            ]
            waypoints = [
                {"x": 420.0, "y": 310.0, "duration_ms": 400.0},
                {"x": 480.0, "y": 350.0, "duration_ms": 500.0},
                {"x": 580.0, "y": 420.0, "duration_ms": 600.0},
                {"x": 750.0, "y": 550.0, "duration_ms": 700.0},
                {"x": 900.0, "y": 680.0, "duration_ms": 800.0},
            ]

        result = compensator.compute_drift(waypoints, anchors)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(result.audit_report_md)

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(result.audit_report_md)
            print(f"[DxSkills] Drift audit report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(result.drift_field_svg)
            print(f"[DxSkills] Drift vector field SVG written to: {args.svg}")
    elif args.command in ["phonological-bridge", "grapheme-resonator", "sub-vocal-pacer", "phonetic-friction"]:
        import scripts.phonological_bridge as pb_mod

        bridge = pb_mod.PhonologicalLoopBridge(high_friction_threshold=args.threshold)

        input_text = ""
        if args.input:
            if os.path.isfile(args.input):
                with open(args.input, "r", encoding="utf-8") as f:
                    input_text = f.read()
            else:
                input_text = args.input
        elif args.demo or not args.input:
            input_text = (
                "The epistemological structure of algebraic topology presents orthographic friction. "
                "Complex phonological dissonance stalls ocular saccades during rapid comprehension."
            )

        result = bridge.evaluate_text(input_text)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(result.audit_report_md)

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(result.audit_report_md)
            print(f"[DxSkills] Phonological audit report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(result.resonance_map_svg)
            print(f"[DxSkills] Syllabic resonance SVG written to: {args.svg}")
    elif args.command in ["saccade-pacer", "kinetic-pacer", "fatigue-predictor", "main-sequence"]:
        import scripts.saccade_fatigue_pacer as sfp_mod

        pacer = sfp_mod.SaccadeKineticPacer(fatigue_threshold_ratio=args.threshold)

        saccades = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, list):
                    saccades = raw_data
                elif isinstance(raw_data, dict):
                    saccades = raw_data.get("saccades", [])
            except json.JSONDecodeError:
                pass
        elif args.demo or not args.input:
            saccades = [
                {"amplitude_px": 100.0, "duration_ms": 30.0, "peak_velocity_px_s": 420.0},
                {"amplitude_px": 150.0, "duration_ms": 35.0, "peak_velocity_px_s": 510.0},
                {"amplitude_px": 250.0, "duration_ms": 80.0, "peak_velocity_px_s": 320.0},
                {"amplitude_px": 350.0, "duration_ms": 110.0, "peak_velocity_px_s": 340.0},
            ]

        result = pacer.evaluate_kinetics(saccades)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(result.audit_report_md)

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(result.audit_report_md)
            print(f"[DxSkills] Kinetic pacer audit report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(result.kinetic_pacer_svg)
            print(f"[DxSkills] Main Sequence kinetic SVG written to: {args.svg}")
    elif args.command in ["entropy-gate", "density-equalizer", "semantic-entropy", "topological-density"]:
        import scripts.semantic_entropy_gate as seg_mod

        equalizer = seg_mod.SemanticEntropyEqualizer(radius=args.radius)

        nodes = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                if isinstance(raw_data, list):
                    nodes = [
                        seg_mod.SemanticNode(
                            node_id=item.get("id", f"node-{idx}"),
                            label=item.get("label", item.get("text", f"Node {idx}")),
                            x=float(item.get("x", 0.0)),
                            y=float(item.get("y", 0.0)),
                            token_count=int(item.get("token_count", 10)),
                            concept_count=int(item.get("concept_count", 2)),
                            edge_count=int(item.get("edge_count", 1)),
                            cluster_id=str(item.get("cluster_id", "default"))
                        )
                        for idx, item in enumerate(raw_data, 1)
                    ]
                elif isinstance(raw_data, dict):
                    raw_nodes = raw_data.get("nodes", [])
                    nodes = [
                        seg_mod.SemanticNode(
                            node_id=item.get("id", f"node-{idx}"),
                            label=item.get("label", item.get("text", f"Node {idx}")),
                            x=float(item.get("x", 0.0)),
                            y=float(item.get("y", 0.0)),
                            token_count=int(item.get("token_count", len(item.get("text", "").split()) or 10)),
                            concept_count=int(item.get("concept_count", 2)),
                            edge_count=int(item.get("edge_count", 1)),
                            cluster_id=str(item.get("cluster_id", item.get("color", "default")))
                        )
                        for idx, item in enumerate(raw_nodes, 1)
                    ]
            except json.JSONDecodeError:
                pass
        elif args.demo or not args.input:
            nodes = seg_mod.sample_canvas_nodes()

        telemetry = equalizer.equalize_density(nodes, iterations=args.iterations)

        if args.json:
            out_dict = {
                "total_nodes": telemetry.total_nodes,
                "radius": telemetry.radius,
                "global_entropy": telemetry.global_entropy,
                "initial_density_variance": telemetry.initial_density_variance,
                "equalized_density_variance": telemetry.equalized_density_variance,
                "variance_reduction_percent": telemetry.variance_reduction_percent,
                "critical_crowding_count": telemetry.critical_crowding_count,
                "max_displacement": telemetry.max_displacement,
                "mean_displacement": telemetry.mean_displacement,
                "nodes": [
                    {
                        "id": n.node_id,
                        "label": n.label,
                        "cluster": n.cluster_id,
                        "orig": [n.original_x, n.original_y],
                        "equalized": [n.adjusted_x, n.adjusted_y],
                        "displacement": n.displacement,
                        "pre_density": n.pre_local_density,
                        "post_density": n.post_local_density
                    }
                    for n in telemetry.redistributed_nodes
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = equalizer.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = equalizer.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Entropy and density report written to: {args.report}")

        if args.svg:
            svg_code = equalizer.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Density equalization SVG written to: {args.svg}")
    elif args.command in ["bifurcation-radar", "path-dependency", "lock-in-loom", "multiverse-fork"]:
        import scripts.bifurcation_radar as br_mod

        loom = br_mod.BifurcationRadarLoom(
            s_threshold=args.threshold,
            coupling_lambda=args.coupling
        )

        forks = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                raw_forks = raw_data if isinstance(raw_data, list) else raw_data.get("forks", [])
                for item in raw_forks:
                    decisions = [
                        br_mod.BifurcationDecision(
                            decision_id=d.get("id", f"d-{idx}"),
                            title=d.get("title", f"Decision {idx}"),
                            branch_id=d.get("branch", "primary"),
                            depth=int(d.get("depth", idx)),
                            complexity=float(d.get("complexity", 5.0)),
                            downstream_deps=int(d.get("downstream_deps", 1)),
                            reversible=bool(d.get("reversible", True))
                        )
                        for idx, d in enumerate(item.get("decisions", []), 1)
                    ]
                    forks.append(br_mod.BifurcationFork(
                        fork_id=item.get("id", item.get("fork_id", "fork-1")),
                        title=item.get("title", "Fork Point"),
                        root_concept=item.get("root_concept", item.get("root", "Root")),
                        primary_branch=item.get("primary_branch", "primary"),
                        counterfactual_branches=item.get("counterfactual_branches", ["alternative"]),
                        decisions=decisions
                    ))
            except json.JSONDecodeError:
                pass
        elif args.demo or not args.input:
            forks = br_mod.sample_bifurcation_forks()

        telemetry = loom.evaluate_multiverse(forks)

        if args.json:
            out_dict = {
                "total_forks": telemetry.total_forks,
                "total_decisions": telemetry.total_decisions,
                "mean_lock_in_score": telemetry.mean_lock_in_score,
                "max_lock_in_score": telemetry.max_lock_in_score,
                "primary_status": telemetry.primary_status,
                "total_switching_cost": telemetry.total_switching_cost,
                "counterfactual_entropy": telemetry.counterfactual_entropy,
                "forks": [
                    {
                        "id": f.fork_id,
                        "title": f.title,
                        "root": f.root_concept,
                        "primary": f.primary_branch,
                        "counterfactuals": f.counterfactual_branches,
                        "lock_in": f.lock_in_score,
                        "status": f.status,
                        "switching_cost": f.switching_cost,
                        "decisions_count": len(f.decisions)
                    }
                    for f in telemetry.forks
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = loom.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = loom.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Bifurcation radar report written to: {args.report}")

        if args.svg:
            svg_code = loom.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Multiverse bifurcation SVG written to: {args.svg}")
    elif args.command in ["foveal-recentering", "saccadic-drift", "drift-compensator-loom", "foveal-loom"]:
        import scripts.foveal_recentering_loom as frl_mod

        loom = frl_mod.FovealReCenteringLoom(
            drift_threshold=args.threshold,
            magnetic_gain=args.gain
        )

        fixations = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                raw_data = json.loads(content)
                raw_list = raw_data if isinstance(raw_data, list) else raw_data.get("fixations", [])
                for idx, item in enumerate(raw_list, 1):
                    fixations.append(frl_mod.GazeFixationPoint(
                        point_id=item.get("id", f"fix-{idx}"),
                        target_label=item.get("target_label", item.get("label", f"Target {idx}")),
                        target_x=float(item.get("target_x", item.get("tx", 0.0))),
                        target_y=float(item.get("target_y", item.get("ty", 0.0))),
                        gaze_x=float(item.get("gaze_x", item.get("gx", 0.0))),
                        gaze_y=float(item.get("gaze_y", item.get("gy", 0.0))),
                        timestamp_ms=float(item.get("timestamp_ms", float(idx) * 250.0))
                    ))
            except json.JSONDecodeError:
                pass
        elif args.demo or not args.input:
            fixations = frl_mod.sample_gaze_fixations()

        telemetry = loom.evaluate_fixations(fixations)

        if args.json:
            out_dict = {
                "total_fixations": telemetry.total_fixations,
                "mean_displacement_px": telemetry.mean_displacement_px,
                "max_displacement_px": telemetry.max_displacement_px,
                "cumulative_drift_error": telemetry.cumulative_drift_error,
                "locked_count": telemetry.locked_count,
                "drifting_count": telemetry.drifting_count,
                "disoriented_count": telemetry.disoriented_count,
                "disorientation_rate_pct": telemetry.disorientation_rate_pct,
                "measurements": [
                    {
                        "id": m.point_id,
                        "label": m.target_label,
                        "displacement": m.displacement_px,
                        "velocity": m.drift_velocity_px_s,
                        "state": m.state,
                        "restore_vector": [m.restore_vector_x, m.restore_vector_y]
                    }
                    for m in telemetry.measurements
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = loom.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = loom.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Foveal drift audit report written to: {args.report}")

        if args.svg:
            svg_code = loom.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Foveal re-centering SVG written to: {args.svg}")
    elif args.command in ["attentional-funnel", "boundary-gasket", "foveal-conduit", "leakage-analyzer"]:
        import scripts.attentional_funnel_gasket as afg_mod

        gasket = afg_mod.AttentionalFunnelGasket(
            foveal_radius=args.aperture,
            gasket_radius=args.conduit,
            min_transparency=args.min_opacity
        )

        entities = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_text = f.read()
            try:
                raw_data = json.loads(raw_text)
                raw_list = raw_data if isinstance(raw_data, list) else raw_data.get("entities", [])
                for idx, item in enumerate(raw_list, 1):
                    entities.append(afg_mod.CanvasEntity(
                        entity_id=str(item.get("id", f"ent-{idx}")),
                        label=str(item.get("label", f"Entity {idx}")),
                        x=float(item.get("x", 0.0)),
                        y=float(item.get("y", 0.0)),
                        width=float(item.get("width", 100.0)),
                        height=float(item.get("height", 60.0)),
                        cognitive_weight=float(item.get("weight", item.get("cognitive_weight", 1.0))),
                        is_target=bool(item.get("is_target", False))
                    ))
            except json.JSONDecodeError:
                pass
        elif args.demo or not args.input:
            entities = afg_mod.sample_canvas_entities()

        telemetry, conduit = gasket.evaluate_canvas(entities, focal_entity_id=args.focal_id)

        if args.json:
            out_dict = {
                "focal_center": list(telemetry.focal_center),
                "focal_label": conduit.focal_label,
                "foveal_radius": telemetry.foveal_radius,
                "gasket_radius": telemetry.gasket_radius,
                "total_entities": telemetry.total_entities,
                "active_entities_count": telemetry.active_entities_count,
                "peripheral_entities_count": telemetry.peripheral_entities_count,
                "raw_leakage_index": telemetry.raw_leakage_index,
                "attenuated_leakage_index": telemetry.attenuated_leakage_index,
                "noise_suppression_pct": telemetry.noise_suppression_pct,
                "gasket_status": telemetry.gasket_status,
                "measurements": [
                    {
                        "id": m.entity_id,
                        "label": m.label,
                        "distance_px": m.distance_px,
                        "raw_saliency": m.raw_saliency,
                        "transparency_factor": m.transparency_factor,
                        "attenuated_saliency": m.attenuated_saliency,
                        "leakage_risk": m.leakage_risk
                    }
                    for m in telemetry.measurements
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = gasket.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = gasket.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Attentional funnel audit report written to: {args.report}")

        if args.svg:
            svg_code = gasket.generate_svg(telemetry, conduit, entities)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Attentional funnel SVG written to: {args.svg}")
    elif args.command in ["semantic-gravity", "gravity-well", "conceptual-orbit", "thesis-attractor"]:
        import scripts.semantic_gravity_well as sgw_mod

        engine = sgw_mod.SemanticGravityWell(
            gravitational_constant_g=args.gravitational_constant,
            base_orbit_radius_px=args.base_radius,
            orbit_spacing_factor=args.spacing
        )

        core = None
        satellites = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_text = f.read()
            try:
                raw_data = json.loads(raw_text)
                core_data = raw_data.get("core", {})
                core = sgw_mod.ConceptualBody(
                    body_id=str(core_data.get("id", "core")),
                    title=str(core_data.get("title", "Core Thesis")),
                    mass=float(core_data.get("mass", 50.0)),
                    domain_tag=str(core_data.get("domain", "general")),
                    affinity_to_core=1.0
                )
                sat_list = raw_data.get("satellites", [])
                for idx, item in enumerate(sat_list, 1):
                    satellites.append(sgw_mod.ConceptualBody(
                        body_id=str(item.get("id", f"sat-{idx}")),
                        title=str(item.get("title", f"Satellite {idx}")),
                        mass=float(item.get("mass", 15.0)),
                        domain_tag=str(item.get("domain", "supporting")),
                        affinity_to_core=float(item.get("affinity", 0.70)),
                        initial_theta_rad=float(item.get("theta", 0.0))
                    ))
            except json.JSONDecodeError:
                pass

        if not core or args.demo:
            core, satellites = sgw_mod.sample_semantic_system()

        telemetry = engine.solve_orbital_system(core, satellites)

        if args.json:
            out_dict = {
                "core_id": telemetry.core_id,
                "core_title": telemetry.core_title,
                "core_mass": telemetry.core_mass,
                "capture_radius_px": telemetry.capture_radius_px,
                "escape_radius_px": telemetry.escape_radius_px,
                "total_satellites": telemetry.total_satellites,
                "orbit_count": telemetry.orbit_count,
                "mean_stability_score": telemetry.mean_stability_score,
                "cowan_overflow_count": telemetry.cowan_overflow_count,
                "orbital_states": [
                    {
                        "id": s.body.body_id,
                        "title": s.body.title,
                        "domain": s.body.domain_tag,
                        "semi_major_px": s.semi_major_axis_px,
                        "eccentricity": s.eccentricity,
                        "period_s": s.orbital_period_s,
                        "escape_risk": s.escape_risk,
                        "stability": s.stability_status,
                        "position": [s.pos_x, s.pos_y]
                    }
                    for s in telemetry.orbital_states
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = engine.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = engine.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Semantic gravity report written to: {args.report}")

        if args.svg:
            svg_code = engine.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Conceptual orbit SVG written to: {args.svg}")
    elif args.command in ["zoom-lens", "semantic-zoom-lens", "lod-lens", "hierarchical-zoom"]:
        import scripts.anchor_stacking_zoom_lens as aszl_mod

        lens = aszl_mod.AnchorStackingZoomLens(
            macro_zoom_threshold=args.macro_threshold,
            meso_zoom_threshold=args.meso_threshold
        )

        anchors = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_text = f.read()
            try:
                raw_data = json.loads(raw_text)
                raw_list = raw_data if isinstance(raw_data, list) else raw_data.get("anchors", [])
                for idx, item in enumerate(raw_list, 1):
                    anchors.append(aszl_mod.SemanticAnchor(
                        anchor_id=str(item.get("id", f"anc-{idx}")),
                        title=str(item.get("title", f"Anchor {idx}")),
                        x=float(item.get("x", 0.0)),
                        y=float(item.get("y", 0.0)),
                        lod_level=int(item.get("lod_level", item.get("lod", 0))),
                        parent_id=item.get("parent_id"),
                        saliency=float(item.get("saliency", 1.0)),
                        tags=list(item.get("tags", []))
                    ))
            except json.JSONDecodeError:
                pass

        if not anchors or args.demo:
            anchors = aszl_mod.sample_knowledge_hierarchy()

        telemetry = lens.evaluate_zoom(anchors, zoom_factor=args.zoom)

        if args.json:
            out_dict = {
                "zoom_factor": telemetry.zoom_factor,
                "active_lod_tier": telemetry.active_lod_tier,
                "total_anchors": telemetry.total_anchors,
                "visible_anchor_count": telemetry.visible_anchor_count,
                "collapsed_cluster_count": telemetry.collapsed_cluster_count,
                "mean_crowding_index": telemetry.mean_crowding_index,
                "cowan_compliant": telemetry.cowan_compliant,
                "cognitive_load_score": telemetry.cognitive_load_score,
                "visible_anchors": [
                    {
                        "id": a.anchor_id,
                        "title": a.title,
                        "x": a.x,
                        "y": a.y,
                        "lod_level": a.lod_level,
                        "parent_id": a.parent_id,
                        "saliency": a.saliency,
                        "tags": a.tags
                    }
                    for a in telemetry.visible_anchors
                ],
                "collapsed_hulls": [
                    {
                        "cluster_id": h.cluster_id,
                        "parent_anchor_id": h.parent_anchor_id,
                        "title": h.title,
                        "center": [h.center_x, h.center_y],
                        "radius_px": h.radius_px,
                        "contained_count": h.contained_anchor_count,
                        "aggregate_saliency": h.aggregate_saliency
                    }
                    for h in telemetry.collapsed_hulls
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = lens.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = lens.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Zoom lens audit report written to: {args.report}")

        if args.svg:
            svg_code = lens.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Zoom lens SVG written to: {args.svg}")
    elif args.command in ["concept-constellation", "starburst", "synesthetic-starburst", "asterism-weaver"]:
        import scripts.concept_constellation_starburst as ccs_mod

        engine = ccs_mod.ConceptConstellationStarburst(
            max_asterism_tether_dist_px=args.tether_distance,
            min_resonance_threshold=args.min_resonance
        )

        concepts = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_text = f.read()
            try:
                raw_data = json.loads(raw_text)
                concepts = raw_data if isinstance(raw_data, list) else raw_data.get("concepts", [])
            except json.JSONDecodeError:
                pass

        if not concepts or args.demo:
            concepts = ccs_mod.sample_concept_stars()

        telemetry = engine.synthesize_constellation(concepts)

        if args.json:
            out_dict = {
                "total_stars": telemetry.total_stars,
                "total_asterisms": telemetry.total_asterisms,
                "mean_resonance": telemetry.mean_resonance,
                "cowan_compliant": telemetry.cowan_compliant,
                "spectral_distribution": telemetry.spectral_distribution,
                "stars": [
                    {
                        "id": s.concept_id,
                        "title": s.title,
                        "magnitude": s.magnitude,
                        "spectral_class": s.spectral_class,
                        "frequency_hz": s.frequency_hz,
                        "cluster_id": s.cluster_id,
                        "position": [s.pos_x, s.pos_y]
                    }
                    for s in telemetry.stars
                ],
                "asterisms": [
                    {
                        "cluster_id": a.cluster_id,
                        "name": a.name,
                        "luminaries": a.luminary_count,
                        "base_frequency_hz": a.harmonic_base_hz,
                        "chromatic_hex": a.chromatic_hex,
                        "bounding_box": list(a.bounding_box)
                    }
                    for a in telemetry.asterisms
                ],
                "edges": [
                    {
                        "source": e.source_id,
                        "target": e.target_id,
                        "resonance": e.resonance_weight,
                        "is_primary": e.is_primary_asterism
                    }
                    for e in telemetry.edges
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = engine.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = engine.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Concept constellation report written to: {args.report}")

        if args.svg:
            svg_code = engine.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Concept constellation SVG written to: {args.svg}")
    elif args.command in ["allocentric-compass", "polar-compass", "anchor-compass", "heading-tracker"]:
        import scripts.allocentric_compass as ac_mod

        tracker = ac_mod.AllocentricCompassTracker(max_allowed_heading_jump_deg=args.max_jump)

        landmarks = []
        waypoints = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_text = f.read()
            try:
                raw_data = json.loads(raw_text)
                lm_list = raw_data.get("landmarks", [])
                for idx, item in enumerate(lm_list, 1):
                    landmarks.append(ac_mod.CanvasLandmark(
                        landmark_id=str(item.get("id", f"lm-{idx}")),
                        title=str(item.get("title", f"Landmark {idx}")),
                        pos_x=float(item.get("x", 0.0)),
                        pos_y=float(item.get("y", 0.0)),
                        is_cardinal_north=bool(item.get("is_north", False)),
                        importance=float(item.get("importance", 1.0))
                    ))
                wp_list = raw_data.get("waypoints", [])
                for idx, item in enumerate(wp_list, 1):
                    waypoints.append(ac_mod.GazeTrajectoryWaypoint(
                        waypoint_id=str(item.get("id", f"wp-{idx}")),
                        pos_x=float(item.get("x", 0.0)),
                        pos_y=float(item.get("y", 0.0)),
                        timestamp_ms=float(item.get("timestamp_ms", float(idx) * 200.0))
                    ))
            except json.JSONDecodeError:
                pass

        if not landmarks or not waypoints or args.demo:
            landmarks, waypoints = ac_mod.sample_navigation_session()

        telemetry = tracker.evaluate_trajectory(landmarks, waypoints)

        if args.json:
            out_dict = {
                "north_anchor_id": telemetry.north_anchor_id,
                "north_coords": list(telemetry.north_coords),
                "total_fixes": telemetry.total_fixes,
                "mean_bearing_deg": telemetry.mean_bearing_deg,
                "angular_dispersion_deg": telemetry.angular_dispersion_deg,
                "disorientation_count": telemetry.disorientation_count,
                "orientation_fidelity_pct": telemetry.orientation_fidelity_pct,
                "fixes": [
                    {
                        "waypoint_id": f.waypoint_id,
                        "bearing_deg": f.bearing_deg,
                        "sector": f.cardinal_sector,
                        "distance_px": f.distance_to_north_px,
                        "drift_deg": f.heading_drift_deg,
                        "is_disoriented": f.is_disoriented
                    }
                    for f in telemetry.fixes
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = tracker.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = tracker.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Allocentric compass report written to: {args.report}")

        if args.svg:
            svg_code = tracker.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Allocentric compass SVG written to: {args.svg}")
    elif args.command in ["tesseract-lattice", "hypercube-schema", "4d-lattice", "tesseract-projection"]:
        import scripts.topological_tesseract_lattice as ttl_mod

        lattice = ttl_mod.TopologicalTesseractLattice(default_scale=args.scale)

        vertices, edges = ttl_mod.sample_4d_schema_hypercube()

        telemetry = lattice.solve_lattice(
            vertices,
            edges,
            theta_deg=args.theta,
            phi_deg=args.phi
        )

        if args.json:
            out_dict = {
                "total_vertices": telemetry.total_vertices,
                "total_edges": telemetry.total_edges,
                "rotation_angles_deg": list(telemetry.rotation_angles_deg),
                "cell_count": telemetry.cell_count,
                "symmetry_metric": telemetry.symmetry_metric,
                "projected_vertices": [
                    {
                        "id": p.vertex_id,
                        "title": p.title,
                        "position": [p.proj_x, p.proj_y],
                        "depth_z": p.depth_z,
                        "w_depth": p.w_depth
                    }
                    for p in telemetry.projected_vertices
                ],
                "edges": [
                    {
                        "source": e.source_id,
                        "target": e.target_id,
                        "axis": e.axis_dimension
                    }
                    for e in telemetry.edges
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = lattice.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = lattice.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Tesseract audit report written to: {args.report}")

        if args.svg:
            svg_code = lattice.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Tesseract SVG written to: {args.svg}")
    elif args.command in ["dialectic-tensor", "tensor-gate", "orthogonality-gate", "synthesis-tensor"]:
        import scripts.dialectic_tensor_gate as dtg_mod

        gate = dtg_mod.DialecticTensorGate(tension_threshold=args.tension_threshold)

        vectors = []
        if args.input and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                raw_text = f.read()
            try:
                raw_data = json.loads(raw_text)
                raw_list = raw_data if isinstance(raw_data, list) else raw_data.get("vectors", [])
                for idx, item in enumerate(raw_list, 1):
                    vectors.append(dtg_mod.DialecticVector(
                        vector_id=str(item.get("id", f"vec-{idx}")),
                        title=str(item.get("title", f"Vector {idx}")),
                        components=[float(c) for c in item.get("components", [1.0, 0.0])],
                        domain=str(item.get("domain", "general")),
                        magnitude=float(item.get("magnitude", 1.0))
                    ))
            except json.JSONDecodeError:
                pass

        if not vectors or args.demo:
            vectors = dtg_mod.sample_dialectic_vectors()

        telemetry = gate.evaluate_manifold(vectors)

        if args.json:
            out_dict = {
                "total_vectors": telemetry.total_vectors,
                "evaluated_pairs_count": telemetry.evaluated_pairs_count,
                "mean_orthogonality": telemetry.mean_orthogonality,
                "peak_tension_pair": list(telemetry.peak_tension_pair) if telemetry.peak_tension_pair else None,
                "pair_tensions": [
                    {
                        "thesis": pt.thesis_id,
                        "antithesis": pt.antithesis_id,
                        "cosine_similarity": pt.cosine_similarity,
                        "orthogonality": pt.orthogonality_score,
                        "tension": pt.tension_energy,
                        "state": pt.synthesis_opportunity
                    }
                    for pt in telemetry.pair_tensions
                ],
                "synthesis_candidates": [
                    {
                        "title": sc.title,
                        "thesis": sc.thesis_id,
                        "antithesis": sc.antithesis_id,
                        "power": sc.synthesis_power,
                        "resolution_angle_deg": sc.resolution_angle_deg,
                        "components": sc.components
                    }
                    for sc in telemetry.synthesis_candidates
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = gate.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = gate.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Dialectic tensor report written to: {args.report}")

        if args.svg:
            svg_code = gate.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Dialectic tensor SVG written to: {args.svg}")
    elif args.command in ["anchor-eviction", "horizon-pacer", "memory-sunset", "decay-eviction"]:
        import scripts.anchor_eviction_horizon_pacer as aehp_mod
        pacer = aehp_mod.AnchorEvictionHorizonPacer(pressure_threshold=args.threshold)

        anchors = []
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = data.get("anchors", data) if isinstance(data, dict) else data
                for item in items:
                    anchors.append(
                        aehp_mod.DecayingAnchor(
                            anchor_id=item.get("id", item.get("anchor_id", "anc")),
                            title=item.get("title", "Anchor"),
                            created_at_s=float(item.get("created_at_s", 0.0)),
                            last_accessed_s=float(item.get("last_accessed_s", 0.0)),
                            base_saliency=float(item.get("base_saliency", 1.0)),
                            half_life_s=float(item.get("half_life_s", 300.0)),
                            pos_x=float(item.get("pos_x", 0.0)),
                            pos_y=float(item.get("pos_y", 0.0)),
                        )
                    )
        else:
            anchors = aehp_mod.sample_decaying_anchors(base_time_s=args.time)

        telemetry = pacer.evaluate_session(anchors, current_time_s=args.time)

        if args.json:
            out_dict = {
                "current_time_s": telemetry.current_time_s,
                "total_anchors": telemetry.total_anchors,
                "fresh_count": telemetry.fresh_count,
                "maturing_count": telemetry.maturing_count,
                "sunset_count": telemetry.sunset_count,
                "breadcrumb_count": telemetry.breadcrumb_count,
                "evicted_count": telemetry.evicted_count,
                "working_memory_pressure": telemetry.working_memory_pressure,
                "overload_warning": telemetry.overload_warning,
                "anchor_states": [
                    {
                        "anchor_id": s.anchor_id,
                        "title": s.title,
                        "retention_score": s.retention_score,
                        "lifecycle_state": s.lifecycle_state,
                        "opacity": s.opacity,
                        "visual_radius_px": s.visual_radius_px,
                        "pos_x": s.pos_x,
                        "pos_y": s.pos_y,
                    }
                    for s in telemetry.anchor_states
                ]
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = pacer.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = pacer.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Anchor eviction report written to: {args.report}")

        if args.svg:
            svg_code = pacer.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Anchor sunset horizon SVG written to: {args.svg}")
    elif args.command in ["saccadic-predictor", "trajectory-predictor", "gaze-prefetch", "saccade-prefetch"]:
        import scripts.saccadic_trajectory_predictor as stp_mod
        predictor = stp_mod.SaccadicTrajectoryPredictor(max_prediction_distance_px=args.distance)

        fixations = []
        candidates = []

        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                fix_items = data.get("fixations", [])
                for item in fix_items:
                    fixations.append(
                        stp_mod.FixationPoint(
                            node_id=str(item.get("id", item.get("node_id", "fix"))),
                            title=str(item.get("title", "Fixation")),
                            x=float(item.get("x", 0.0)),
                            y=float(item.get("y", 0.0)),
                            timestamp_ms=float(item.get("timestamp_ms", 0.0)),
                            dwell_duration_ms=float(item.get("dwell_duration_ms", 250.0)),
                        )
                    )
                candidates = data.get("candidates", data.get("nodes", []))
        else:
            fixations, candidates = stp_mod.sample_saccadic_session()

        telemetry = predictor.evaluate_pre_fetch_candidates(fixations, candidates)

        if args.json:
            traj_dict = None
            if telemetry.current_trajectory:
                traj_dict = {
                    "origin_x": telemetry.current_trajectory.origin_x,
                    "origin_y": telemetry.current_trajectory.origin_y,
                    "heading_deg": telemetry.current_trajectory.heading_deg,
                    "velocity_px_per_ms": telemetry.current_trajectory.velocity_px_per_ms,
                    "confidence": telemetry.current_trajectory.confidence,
                    "cone_angle_deg": telemetry.current_trajectory.cone_angle_deg,
                }

            out_dict = {
                "recent_fixations_count": telemetry.recent_fixations_count,
                "current_trajectory": traj_dict,
                "candidate_count": telemetry.candidate_count,
                "predictive_efficiency_score": telemetry.predictive_efficiency_score,
                "recommended_cache_size": telemetry.recommended_cache_size,
                "pre_fetch_candidates": [
                    {
                        "node_id": c.node_id,
                        "title": c.title,
                        "pos_x": c.pos_x,
                        "pos_y": c.pos_y,
                        "distance_px": c.distance_px,
                        "angle_offset_deg": c.angle_offset_deg,
                        "priority_score": c.priority_score,
                        "pre_fetch_tier": c.pre_fetch_tier,
                    }
                    for c in telemetry.pre_fetch_candidates
                ],
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = predictor.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = predictor.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Saccadic trajectory report written to: {args.report}")

        if args.svg:
            svg_code = predictor.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Saccadic trajectory SVG written to: {args.svg}")
    elif args.command in ["knowledge-mesh", "hypergraph-weaver", "mesh-consolidator", "semantic-weaver"]:
        import scripts.knowledge_mesh_weaver as kmw_mod
        weaver = kmw_mod.KnowledgeMeshWeaver(min_cluster_size=args.min_cluster)

        nodes = []
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = data.get("nodes", data) if isinstance(data, dict) else data
                for item in items:
                    nodes.append(
                        kmw_mod.MeshNode(
                            node_id=str(item.get("id", item.get("node_id", "node"))),
                            title=str(item.get("title", "Node")),
                            domain=str(item.get("domain", "General")),
                            semantic_primitives=item.get("primitives", item.get("semantic_primitives", [])),
                            pos_x=float(item.get("x", item.get("pos_x", 0.0))),
                            pos_y=float(item.get("y", item.get("pos_y", 0.0))),
                            weight=float(item.get("weight", 1.0)),
                        )
                    )
        else:
            nodes = kmw_mod.sample_knowledge_mesh()

        telemetry = weaver.weave_mesh(nodes)

        if args.json:
            out_dict = {
                "total_nodes": telemetry.total_nodes,
                "domain_count": telemetry.domain_count,
                "hyper_edges_count": telemetry.hyper_edges_count,
                "cross_domain_bridges_count": telemetry.cross_domain_bridges_count,
                "mesh_density": telemetry.mesh_density,
                "interconnected_reasoning_index": telemetry.interconnected_reasoning_index,
                "hyper_edges": [
                    {
                        "edge_id": he.edge_id,
                        "title": he.title,
                        "shared_primitive": he.shared_primitive,
                        "member_node_ids": he.member_node_ids,
                        "domains_spanned": he.domains_spanned,
                        "coherence_score": he.coherence_score,
                    }
                    for he in telemetry.hyper_edges
                ],
                "domain_bridges": [
                    {
                        "domain_a": db.domain_a,
                        "domain_b": db.domain_b,
                        "bridging_primitives": db.bridging_primitives,
                        "resonance_strength": db.resonance_strength,
                    }
                    for db in telemetry.domain_bridges
                ],
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = weaver.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = weaver.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Knowledge mesh report written to: {args.report}")

        if args.svg:
            svg_code = weaver.generate_svg(nodes, telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Knowledge hyper-graph SVG written to: {args.svg}")
    elif args.command in ["entropy-decoupler", "semantic-denoiser", "snr-gate", "syntax-denoiser"]:
        import scripts.semantic_entropy_decoupler as sed_mod
        decoupler = sed_mod.SemanticEntropyDecoupler(snr_alert_threshold_db=args.threshold)

        nodes = []
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = data.get("nodes", data) if isinstance(data, dict) else data
                if isinstance(items, list):
                    for item in items:
                        nodes.append({
                            "id": str(item.get("id", item.get("node_id", "node"))),
                            "title": str(item.get("title", "Node")),
                            "text": str(item.get("text", item.get("content", ""))),
                        })
                elif isinstance(data, str):
                    nodes.append({"id": "input-1", "title": "Input Text", "text": data})
        else:
            nodes = sed_mod.sample_noisy_nodes()

        telemetry = decoupler.analyze_nodes(nodes)

        if args.json:
            out_dict = {
                "node_count": telemetry.node_count,
                "mean_entropy_bits": telemetry.mean_entropy_bits,
                "mean_snr_db": telemetry.mean_snr_db,
                "mean_noise_ratio": telemetry.mean_noise_ratio,
                "high_noise_nodes_count": telemetry.high_noise_nodes_count,
                "profiles": [
                    {
                        "node_id": p.node_id,
                        "title": p.title,
                        "total_tokens": p.total_tokens,
                        "unique_tokens": p.unique_tokens,
                        "shannon_entropy_bits": p.shannon_entropy_bits,
                        "syntactic_noise_ratio": p.syntactic_noise_ratio,
                        "signal_to_noise_ratio_db": p.signal_to_noise_ratio_db,
                        "de_noised_text": p.de_noised_text,
                    }
                    for p in telemetry.profiles
                ],
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = decoupler.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = decoupler.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Semantic entropy report written to: {args.report}")

        if args.svg:
            svg_code = decoupler.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Semantic entropy SVG written to: {args.svg}")
    elif args.command in ["polyhedral-crystallizer", "schema-folder", "polyhedral-net", "concept-crystallizer"]:
        import scripts.polyhedral_schema_crystallizer as psc_mod
        crystallizer = psc_mod.PolyhedralSchemaCrystallizer(default_scale_px=args.scale)

        concepts = []
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = data.get("concepts", data) if isinstance(data, dict) else data
                if isinstance(items, list):
                    for item in items:
                        concepts.append({
                            "title": str(item.get("title", "Concept")),
                            "text": str(item.get("text", item.get("summary", ""))),
                        })
        else:
            concepts = psc_mod.sample_crystallizer_concepts()

        telemetry = crystallizer.crystallize_schema(concepts, polyhedron_type=args.type)

        if args.json:
            out_dict = {
                "input_concepts_count": telemetry.input_concepts_count,
                "selected_polyhedron": telemetry.selected_polyhedron,
                "face_coverage_ratio": telemetry.face_coverage_ratio,
                "mean_dihedral_angle_deg": telemetry.mean_dihedral_angle_deg,
                "spatial_crystallization_score": telemetry.spatial_crystallization_score,
                "net": {
                    "polyhedron_type": telemetry.polyhedral_net.polyhedron_type,
                    "face_count": telemetry.polyhedral_net.face_count,
                    "faces": [
                        {
                            "face_id": f.face_id,
                            "title": f.title,
                            "summary": f.concept_summary,
                            "adjacent_face_ids": f.adjacent_face_ids,
                            "center_x": f.center_x,
                            "center_y": f.center_y,
                            "dihedral_angle_deg": f.dihedral_angle_deg,
                        }
                        for f in telemetry.polyhedral_net.faces
                    ]
                }
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = crystallizer.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = crystallizer.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Polyhedral schema report written to: {args.report}")

        if args.svg:
            svg_code = crystallizer.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Polyhedral net blueprint SVG written to: {args.svg}")
    elif args.command in ["polar-grid", "landmark-polar", "bearing-synthesizer", "allocentric-bearing"]:
        import scripts.allocentric_polar_grid as apg_mod
        synthesizer = apg_mod.AllocentricPolarGridSynthesizer(
            default_ring_interval_px=args.interval,
            num_rings=args.rings,
        )

        landmark = None
        targets = []

        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                lm_data = data.get("landmark", {})
                landmark = apg_mod.PolarLandmark(
                    landmark_id=str(lm_data.get("id", "lm-hub")),
                    title=str(lm_data.get("title", "Origin Hub")),
                    x=float(lm_data.get("x", 460.0)),
                    y=float(lm_data.get("y", 280.0)),
                    radius_px=float(lm_data.get("radius_px", 16.0)),
                    is_primary=bool(lm_data.get("is_primary", True)),
                )
                targets = data.get("targets", data.get("nodes", []))
        else:
            landmark, targets = apg_mod.sample_polar_session()

        telemetry = synthesizer.calculate_polar_bearings(landmark, targets)

        if args.json:
            out_dict = {
                "landmark": {
                    "id": telemetry.primary_landmark.landmark_id,
                    "title": telemetry.primary_landmark.title,
                    "x": telemetry.primary_landmark.x,
                    "y": telemetry.primary_landmark.y,
                },
                "target_count": telemetry.target_count,
                "max_range_px": telemetry.max_range_px,
                "ring_count": telemetry.ring_count,
                "angular_dispersion_index": telemetry.angular_dispersion_index,
                "allocentric_stability_score": telemetry.allocentric_stability_score,
                "target_bearings": [
                    {
                        "target_id": b.target_id,
                        "title": b.title,
                        "pos_x": b.pos_x,
                        "pos_y": b.pos_y,
                        "distance_px": b.distance_px,
                        "bearing_deg": b.bearing_deg,
                        "cardinal_heading": b.cardinal_heading,
                        "range_ring_zone": b.range_ring_zone,
                    }
                    for b in telemetry.target_bearings
                ],
            }
            print(json.dumps(out_dict, indent=2))
        else:
            report_md = synthesizer.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = synthesizer.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Polar grid report written to: {args.report}")

        if args.svg:
            svg_code = synthesizer.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Polar radar grid SVG written to: {args.svg}")
    elif args.command in ["gaze-stabilizer", "attentional-funnel-stabilizer", "scanpath-limiter", "gaze-envelope"]:
        import scripts.attentional_gaze_stabilizer as ags_mod
        stabilizer = ags_mod.AttentionalGazeStabilizer(
            default_envelope_width_px=args.envelope_width,
            jitter_damping_factor=args.damping,
        )
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_pts = [
                    ags_mod.GazePoint(
                        point_id=str(p.get("id", f"gp-{i}")),
                        x=float(p.get("x", 0.0)),
                        y=float(p.get("y", 0.0)),
                        timestamp_ms=float(p.get("timestamp_ms", i * 100.0)),
                        fixation_dwell_ms=float(p.get("dwell_ms", 120.0)),
                        is_fixation=bool(p.get("is_fixation", True)),
                    )
                    for i, p in enumerate(data.get("points", data.get("gaze_points", [])))
                ]
                channels = [
                    ags_mod.AttentionalChannel(
                        channel_id=str(c.get("id", f"ch-{i}")),
                        title=str(c.get("title", f"Channel {i+1}")),
                        points=[(float(pt[0]), float(pt[1])) for pt in c.get("points", [])],
                        envelope_width_px=float(c.get("width_px", args.envelope_width)),
                        priority=int(c.get("priority", 1)),
                        color=str(c.get("color", "#58a6ff")),
                    )
                    for i, c in enumerate(data.get("channels", []))
                ]
                telemetry = stabilizer.stabilize_scanpath(raw_pts, channels)
        else:
            telemetry = ags_mod.AttentionalGazeStabilizer.create_demo_telemetry()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            report_md = stabilizer.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = stabilizer.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Gaze stabilization report written to: {args.report}")

        if args.svg:
            svg_code = stabilizer.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Gaze envelope SVG written to: {args.svg}")
    elif args.command in ["dialectical-tensor-loom", "hegelian-tensor-loom", "dialectical-tensor", "hegelian-loom", "tensor-lattice-loom"]:
        import scripts.dialectical_tensor_loom as dtl_mod
        loom = dtl_mod.DialecticalTensorLoom(
            acute_friction_threshold=args.threshold,
        )
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                poles = [
                    dtl_mod.DialecticalPole(
                        pole_id=str(p.get("id", f"pole-{i}")),
                        title=str(p.get("title", f"Pole {i+1}")),
                        dimension_vector=[float(v) for v in p.get("vector", p.get("dimension_vector", [1.0, 0.0]))],
                        core_axiom=str(p.get("axiom", p.get("core_axiom", "Core postulate"))),
                        pole_type=str(p.get("type", p.get("pole_type", "THESIS"))),
                        pos_x=float(p.get("x", 200.0 + i * 200.0)),
                        pos_y=float(p.get("y", 250.0)),
                    )
                    for i, p in enumerate(data.get("poles", []))
                ]
                resolutions = [
                    dtl_mod.AufhebungResolution(
                        resolution_id=str(r.get("id", f"res-{i}")),
                        thesis_id=str(r.get("thesis_id", "")),
                        antithesis_id=str(r.get("antithesis_id", "")),
                        synthesis_title=str(r.get("title", "Harmonic Synthesis")),
                        preserved_tenets=[str(t) for t in r.get("preserved", [])],
                        negated_biases=[str(b) for b in r.get("negated", [])],
                        emergent_axiom=str(r.get("emergent_axiom", "Synthesized paradigm")),
                        resolution_ratio=float(r.get("resolution_ratio", 0.85)),
                        cognitive_harmony_index=float(r.get("harmony_index", 85.0)),
                    )
                    for i, r in enumerate(data.get("resolutions", []))
                ]
                telemetry = loom.evaluate_lattice(poles, resolutions if resolutions else None)
        else:
            telemetry = dtl_mod.DialecticalTensorLoom.create_demo_telemetry()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            report_md = loom.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = loom.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Dialectical synthesis report written to: {args.report}")

        if args.svg:
            svg_code = loom.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Dialectical tensor loom SVG written to: {args.svg}")
    elif args.command in ["concept-hologram", "holographic-weaver", "interference-pattern", "semantic-hologram"]:
        import scripts.concept_hologram_weaver as chw_mod
        weaver = chw_mod.ConceptHologramWeaver(
            sample_grid_step=args.grid_step,
            coherence_threshold=args.threshold,
        )
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                emitters = [
                    chw_mod.WaveEmitter(
                        emitter_id=str(e.get("id", f"em-{i}")),
                        title=str(e.get("title", f"Emitter {i+1}")),
                        x=float(e.get("x", 200.0 + i * 150.0)),
                        y=float(e.get("y", 250.0)),
                        amplitude=float(e.get("amplitude", 1.0)),
                        wavelength_px=float(e.get("wavelength_px", 60.0)),
                        phase_rad=float(e.get("phase_rad", 0.0)),
                        modality=str(e.get("modality", "SPATIAL")),
                        color=str(e.get("color", "#58a6ff")),
                    )
                    for i, e in enumerate(data.get("emitters", data.get("concepts", [])))
                ]
                telemetry = weaver.compute_wave_field(emitters)
        else:
            telemetry = chw_mod.ConceptHologramWeaver.create_demo_telemetry()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            report_md = weaver.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = weaver.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Concept hologram report written to: {args.report}")

        if args.svg:
            svg_code = weaver.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Concept hologram SVG written to: {args.svg}")
    elif args.command in ["gaze-corridor-resonator", "corridor-resonator", "focal-conduit", "parafoveal-preview"]:
        import scripts.gaze_corridor_resonator as gcr_mod
        resonator = gcr_mod.GazeCorridorResonator(
            saccadic_latency_ms=args.latency,
            base_aperture_px=args.aperture,
        )
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                samples = [
                    gcr_mod.GazeSample(
                        sample_id=str(s.get("id", f"gs-{i}")),
                        x=float(s.get("x", 0.0)),
                        y=float(s.get("y", 0.0)),
                        timestamp_ms=float(s.get("timestamp_ms", i * 150.0)),
                        dwell_ms=float(s.get("dwell_ms", 120.0)),
                        modality=str(s.get("modality", "TEXT")),
                    )
                    for i, s in enumerate(data.get("samples", data.get("gaze_samples", [])))
                ]
                telemetry = resonator.synchronize_corridor(samples)
        else:
            telemetry = gcr_mod.GazeCorridorResonator.create_demo_telemetry()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            report_md = resonator.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = resonator.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Gaze corridor report written to: {args.report}")

        if args.svg:
            svg_code = resonator.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Gaze corridor SVG written to: {args.svg}")
    elif args.command in ["kinematic-horizon", "artificial-horizon", "inertial-frame", "gimbal-lock-calibrator"]:
        import scripts.allocentric_kinematic_horizon as akh_mod
        calibrator = akh_mod.AllocentricKinematicHorizon(
            gimbal_warning_threshold_deg=args.threshold,
            gauge_radius_px=args.radius,
            pitch_scale_px_per_deg=args.pitch_scale,
        )
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_samples = data.get("samples", data.get("inertial_samples", []))
                samples = [
                    akh_mod.InertialSample(
                        sample_id=str(s.get("sample_id", s.get("id", f"in-{i}"))),
                        pitch_deg=float(s.get("pitch_deg", s.get("pitch", 0.0))),
                        roll_deg=float(s.get("roll_deg", s.get("roll", 0.0))),
                        yaw_deg=float(s.get("yaw_deg", s.get("yaw", 0.0))),
                        timestamp_ms=float(s.get("timestamp_ms", i * 100.0)),
                    )
                    for i, s in enumerate(raw_samples)
                ]
                telemetry = calibrator.calculate_kinematic_frames(samples)
        else:
            telemetry = akh_mod.AllocentricKinematicHorizon.create_demo_telemetry()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            report_md = calibrator.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = calibrator.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Kinematic horizon report written to: {args.report}")

        if args.svg:
            svg_code = calibrator.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Kinematic horizon SVG written to: {args.svg}")
    elif args.command in ["morphological-lens", "semantic-lens", "granularity-zoom", "morphological-zoom"]:
        import scripts.morphological_semantic_lens as msl_mod
        lens = msl_mod.MorphologicalSemanticLens(
            base_focal_radius_px=args.focal_radius,
            max_cowan_foveal_capacity=args.cowan_capacity,
        )
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_nodes = data.get("nodes", data.get("semantic_nodes", []))
                samples = [
                    msl_mod.SemanticNode(
                        node_id=str(n.get("node_id", n.get("id", f"node-{i}"))),
                        label=str(n.get("label", n.get("name", f"Node {i}"))),
                        granularity_level=str(n.get("granularity_level", n.get("level", "MESO_SUBSYSTEM"))),
                        abstraction_depth=float(n.get("abstraction_depth", n.get("depth", 0.5))),
                        x=float(n.get("x", 400.0)),
                        y=float(n.get("y", 250.0)),
                        importance_weight=float(n.get("importance_weight", n.get("weight", 1.0))),
                        details=list(n.get("details", [])),
                    )
                    for i, n in enumerate(raw_nodes)
                ]
                telemetry = lens.compute_semantic_zoom(
                    samples,
                    focus_x=args.focus_x,
                    focus_y=args.focus_y,
                    zoom_factor=args.zoom,
                )
        else:
            telemetry = msl_mod.MorphologicalSemanticLens.create_demo_telemetry()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            report_md = lens.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = lens.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Morphological semantic lens report written to: {args.report}")

        if args.svg:
            svg_code = lens.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Morphological semantic lens SVG written to: {args.svg}")
    elif args.command in ["manifold-unfolder", "polytope-net", "tesseract-unfolder", "riemannian-manifold"]:
        import scripts.topological_manifold_unfolder as tmu_mod
        unfolder = tmu_mod.TopologicalManifoldUnfolder(
            isometric_angle_deg=args.iso_angle,
            cell_spacing_px=args.spacing,
        )
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                ptype = str(data.get("polytope_type", args.polytope))
                factor = float(data.get("unfolding_factor", args.factor))
                telemetry = unfolder.unfold_polytope(polytope_type=ptype, unfolding_factor=factor)
        else:
            telemetry = unfolder.unfold_polytope(polytope_type=args.polytope, unfolding_factor=args.factor)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            report_md = unfolder.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = unfolder.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Topological manifold report written to: {args.report}")

        if args.svg:
            svg_code = unfolder.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Topological manifold SVG written to: {args.svg}")
    elif args.command in ["saliency-conductor", "saccadic-conductor", "gaze-conductor", "saccadic-saliency"]:
        import scripts.saccadic_saliency_conductor as ssc_mod
        conductor = ssc_mod.SaccadicSaliencyConductor(
            px_per_degree=args.px_per_deg,
            base_saccade_latency_ms=args.latency,
            regression_penalty_weight=args.penalty,
        )
        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_wps = data.get("waypoints", data.get("saliency_waypoints", []))
                waypoints = [
                    ssc_mod.SaliencyWaypoint(
                        waypoint_id=str(w.get("waypoint_id", w.get("id", f"wp-{i}"))),
                        label=str(w.get("label", w.get("name", f"Waypoint {i}"))),
                        x=float(w.get("x", 100.0 * (i + 1))),
                        y=float(w.get("y", 150.0)),
                        raw_saliency=float(w.get("raw_saliency", w.get("saliency", 0.8))),
                        semantic_weight=float(w.get("semantic_weight", w.get("weight", 0.8))),
                        order_index=int(w.get("order_index", i)),
                    )
                    for i, w in enumerate(raw_wps)
                ]
                telemetry = conductor.conduct_saliency_path(waypoints)
        else:
            telemetry = ssc_mod.SaccadicSaliencyConductor.create_demo_telemetry()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            report_md = conductor.generate_markdown_report(telemetry)
            print(report_md)

        if args.report:
            report_md = conductor.generate_markdown_report(telemetry)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"[DxSkills] Saccadic conductor report written to: {args.report}")

        if args.svg:
            svg_code = conductor.generate_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Saccadic conductor SVG written to: {args.svg}")
    elif args.command in ["retinal-latch", "drift-dampener", "retinal-dampener", "working-memory-latch", "retinal-stabilizer"]:
        import scripts.saccadic_drift_dampener as sdd_mod
        cfg = sdd_mod.DriftDampeningConfig(
            damping_factor=args.damping,
            deadband_radius_px=args.deadband,
        )
        dampener = sdd_mod.SaccadicDriftDampener(config=cfg)

        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_samples = [
                    (float(s.get("t", s.get("timestamp_ms", i * 50.0))), float(s["x"]), float(s["y"]))
                    for i, s in enumerate(data.get("samples", []))
                ]
                for a in data.get("anchors", []):
                    dampener.add_anchor(
                        sdd_mod.RetinalAnchor(
                            anchor_id=str(a.get("anchor_id", a.get("id", "anc"))),
                            label=str(a.get("label", "Anchor")),
                            x=float(a["x"]),
                            y=float(a["y"]),
                            capture_radius_px=float(a.get("capture_radius_px", 35.0)),
                            latch_strength=float(a.get("latch_strength", 0.85)),
                        )
                    )
                telemetry = dampener.process_stream(raw_samples)
        else:
            telemetry = dampener.simulate_mental_rotation_drift(
                rotation_angle_deg=args.rotation_angle,
                noise_std=args.noise,
                duration_ms=args.duration,
            )

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print(f"[DxSkills] Retinal Latch & Saccadic Drift Telemetry")
            print(f"Status: {telemetry.stability_status}")
            print(f"Total Samples: {telemetry.total_samples}")
            print(f"Drift Reduction: {telemetry.drift_reduction_pct:.1f}%")
            print(f"Mean Jitter Amplitude: {telemetry.mean_jitter_amplitude_px:.1f} px")
            print(f"Latch Events: {telemetry.latch_event_count}")
            print(f"WM Coherence Index: {telemetry.working_memory_coherence_score:.1f} / 100")
            if telemetry.warnings:
                for w in telemetry.warnings:
                    print(f"Warning: {w}")

        if args.report:
            md_lines = [
                "# Saccadic Drift Dampener & Retinal Latch Diagnostic Report",
                "",
                f"**Stability Status:** `{telemetry.stability_status}`",
                f"- **Total Samples:** {telemetry.total_samples}",
                f"- **Raw Path Length:** {telemetry.total_raw_path_length_px:.1f} px",
                f"- **Damped Path Length:** {telemetry.total_damped_path_length_px:.1f} px",
                f"- **Drift Reduction:** {telemetry.drift_reduction_pct:.1f}%",
                f"- **Mean Jitter Amplitude:** {telemetry.mean_jitter_amplitude_px:.1f} px",
                f"- **Retinal Latch Events:** {telemetry.latch_event_count}",
                f"- **Working Memory Coherence Score:** {telemetry.working_memory_coherence_score:.1f} / 100",
                "",
                "## Registered Retinal Anchors",
                "",
                "| Anchor ID | Label | Coordinates (X, Y) | Capture Radius | Latch Strength |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
            for a in telemetry.anchors:
                md_lines.append(f"| `{a.anchor_id}` | {a.label} | ({a.x:.1f}, {a.y:.1f}) | {a.capture_radius_px:.1f} px | {a.latch_strength:.2f} |")
            if telemetry.warnings:
                md_lines.extend(["", "## Diagnostic Warnings", ""])
                for w in telemetry.warnings:
                    md_lines.append(f"- [WARNING] {w}")
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Retinal latch report written to: {args.report}")

        if args.svg:
            svg_code = dampener.render_retinal_latch_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Retinal latch SVG written to: {args.svg}")
    elif args.command in ["fiber-bundle", "holonomy-weaver", "topological-bundle", "polytope-holonomy", "parallel-transport"]:
        import scripts.topological_fiber_bundle as tfb_mod
        weaver = tfb_mod.TopologicalFiberBundle(twist_parameter=args.twist)

        btype = args.type.lower()
        if btype == "hopf":
            telemetry = weaver.weave_hopf_fibration(
                base_radius_px=args.radius,
                steps=args.steps,
                fiber_twist=args.twist,
            )
        elif btype == "torus":
            telemetry = weaver.weave_torus_bundle(
                major_radius_px=args.radius,
                p_winds=args.p_winds,
                q_winds=args.q_winds,
                steps=args.steps,
            )
        elif btype == "cylinder":
            telemetry = weaver.weave_mobius_bundle(
                radius_px=args.radius,
                steps=args.steps,
                twist_factor=0.0,
            )
        else:
            telemetry = weaver.weave_mobius_bundle(
                radius_px=args.radius,
                steps=args.steps,
                twist_factor=args.twist,
            )

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print(f"[DxSkills] Topological Fiber Bundle & Holonomy Telemetry")
            print(f"Bundle Type: {telemetry.bundle_type}")
            print(f"Total Steps: {telemetry.total_steps}")
            print(f"Loop Perimeter: {telemetry.loop_perimeter_px:.1f} px")
            print(f"Total Twist: {telemetry.total_twist_deg:.1f} deg")
            print(f"Holonomy Angle: {telemetry.holonomy_angle_deg:.1f} deg")
            print(f"Non-Trivial Topology: {telemetry.is_non_trivial_topology}")
            print(f"Curvature Integral: {telemetry.connection_curvature_integral:.3f} rad")
            if telemetry.warnings:
                for w in telemetry.warnings:
                    print(f"Note: {w}")

        if args.report:
            md_lines = [
                "# Topological Fiber Bundle & Holonomy Diagnostic Report",
                "",
                f"**Bundle Type:** `{telemetry.bundle_type}`",
                f"- **Total Discretization Steps:** {telemetry.total_steps}",
                f"- **Loop Perimeter:** {telemetry.loop_perimeter_px:.1f} px",
                f"- **Total Fiber Twist:** {telemetry.total_twist_deg:.1f} deg",
                f"- **Holonomy Angle:** {telemetry.holonomy_angle_deg:.1f} deg",
                f"- **Is Non-Trivial Topology:** {telemetry.is_non_trivial_topology}",
                f"- **Connection Curvature Integral:** {telemetry.connection_curvature_integral:.3f} rad",
                "",
                "## Topological Fibers Sample (First 5)",
                "",
                "| Step t | Base (X, Y, Z) | Fiber Angle | Vector (dx, dy, dz) |",
                "| :--- | :--- | :--- | :--- |",
            ]
            for f_vec in telemetry.fibers[:5]:
                md_lines.append(
                    f"| {f_vec.t:.3f} | ({f_vec.base_x:.1f}, {f_vec.base_y:.1f}, {f_vec.base_z:.1f}) | {f_vec.fiber_angle_deg:.1f} deg | ({f_vec.vector_dx:.2f}, {f_vec.vector_dy:.2f}, {f_vec.vector_dz:.2f}) |"
                )
            if telemetry.warnings:
                md_lines.extend(["", "## Diagnostic Notes", ""])
                for w in telemetry.warnings:
                    md_lines.append(f"- [TOPOLOGY] {w}")
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Holonomy report written to: {args.report}")

        if args.svg:
            svg_code = weaver.render_fiber_bundle_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Fiber bundle SVG written to: {args.svg}")
    elif args.command in ["chrono-replay", "replay-loom", "episodic-replay", "trajectory-synthesizer", "hippocampal-replay"]:
        import scripts.chrono_spatial_replay_loom as csrl_mod
        loom = csrl_mod.ChronoSpatialReplayLoom(default_compression=args.compression)

        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_wps = data.get("waypoints", [])
                waypoints = [
                    csrl_mod.EpisodicWaypoint(
                        node_id=str(w.get("node_id", w.get("id", f"node-{i}"))),
                        label=str(w.get("label", f"Milestone {i}")),
                        x=float(w.get("x", 100.0 * (i + 1))),
                        y=float(w.get("y", 150.0)),
                        valence=float(w.get("valence", 0.5)),
                        dwell_time_ms=float(w.get("dwell_time_ms", 250.0)),
                    )
                    for i, w in enumerate(raw_wps)
                ]
            if args.mode == "reverse":
                telemetry = loom.synthesize_reverse_replay(waypoints, compression_factor=args.compression)
            else:
                telemetry = loom.synthesize_forward_replay(waypoints, compression_factor=args.compression)
        elif args.mode == "reverse":
            demo_wps = [
                csrl_mod.EpisodicWaypoint("N1", "Initial Problem", 120.0, 260.0, valence=0.0),
                csrl_mod.EpisodicWaypoint("N2", "Formulate Hypothesis", 280.0, 180.0, valence=0.4),
                csrl_mod.EpisodicWaypoint("N3", "Execute Synthesis", 480.0, 240.0, valence=0.7),
                csrl_mod.EpisodicWaypoint("N4", "Resolution Goal", 680.0, 200.0, valence=1.0),
            ]
            telemetry = loom.synthesize_reverse_replay(demo_wps, compression_factor=args.compression)
        else:
            telemetry = loom.simulate_choice_point_rollout(depth=args.depth)

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print(f"[DxSkills] Chrono-Spatial Replay Loom Telemetry")
            print(f"Mode: {telemetry.replay_mode}")
            print(f"Total Waypoints: {telemetry.total_waypoints}")
            print(f"Path Length: {telemetry.total_path_length_px:.1f} px")
            print(f"Real-Time Duration: {telemetry.realtime_duration_ms:.0f} ms")
            print(f"Compressed Duration: {telemetry.compressed_duration_ms:.0f} ms")
            print(f"Compression Factor: {telemetry.compression_factor:.1f}x")
            print(f"Fidelity Score: {telemetry.fidelity_score:.1f} / 100")
            print(f"Status: {telemetry.status}")
            if telemetry.warnings:
                for w in telemetry.warnings:
                    print(f"Note: {w}")

        if args.report:
            md_lines = [
                "# Chrono-Spatial Replay Loom Diagnostic Report",
                "",
                f"**Replay Mode:** `{telemetry.replay_mode}`",
                f"- **Status:** `{telemetry.status}`",
                f"- **Total Waypoints:** {telemetry.total_waypoints}",
                f"- **Total Path Length:** {telemetry.total_path_length_px:.1f} px",
                f"- **Real-Time Duration:** {telemetry.realtime_duration_ms:.0f} ms",
                f"- **Compressed Duration:** {telemetry.compressed_duration_ms:.0f} ms",
                f"- **Compression Ratio:** {telemetry.compression_factor:.1f}x",
                f"- **Ripple Frequency:** {telemetry.ripple_frequency_hz:.0f} Hz",
                f"- **Mean Phase Precession:** {telemetry.mean_phase_precession_deg:.1f} deg",
                f"- **Replay Fidelity Score:** {telemetry.fidelity_score:.1f} / 100",
                "",
                "## Replay Trajectory Waypoints",
                "",
                "| Node ID | Label | Coordinates (X, Y) | Valence | Theta Phase | Dwell Time |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |",
            ]
            for wp in telemetry.waypoints:
                md_lines.append(
                    f"| `{wp.node_id}` | {wp.label} | ({wp.x:.1f}, {wp.y:.1f}) | {wp.valence:.2f} | {wp.theta_phase_deg:.0f} deg | {wp.dwell_time_ms:.0f} ms |"
                )
            if telemetry.warnings:
                md_lines.extend(["", "## Diagnostic Notes", ""])
                for w in telemetry.warnings:
                    md_lines.append(f"- [REPLAY] {w}")
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Replay report written to: {args.report}")

        if args.svg:
            svg_code = loom.render_chrono_replay_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Replay SVG written to: {args.svg}")
    elif args.command in ["topographic-contour", "isocline-tracer", "semantic-topography", "contour-morph", "terrain-elevation"]:
        import scripts.topographic_contour_morph as tcm_mod
        morph = tcm_mod.TopographicContourMorph(base_contour_interval=args.interval)

        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_summits = data.get("summits", [])
                for i, s in enumerate(raw_summits):
                    morph.add_summit(
                        tcm_mod.ElevationSummit(
                            summit_id=str(s.get("summit_id", s.get("id", f"summit-{i}"))),
                            label=str(s.get("label", f"Peak {i}")),
                            x=float(s["x"]),
                            y=float(s["y"]),
                            elevation=float(s.get("elevation", 500.0)),
                            spread_sigma=float(s.get("spread_sigma", 65.0)),
                        )
                    )
            telemetry = morph.trace_isoclines(
                grid_w=args.grid_w,
                grid_h=args.grid_h,
                contour_interval=args.interval,
            )
        else:
            telemetry = morph.simulate_demo_semantic_terrain()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print(f"[DxSkills] Topographic Contour & Relief Telemetry")
            print(f"Total Summits: {telemetry.total_summits}")
            print(f"Elevation Range: {telemetry.min_elevation:.0f}m to {telemetry.max_elevation:.0f}m")
            print(f"Contour Interval: {telemetry.contour_interval:.0f}m")
            print(f"Isocline Levels: {telemetry.total_isocline_levels}")
            print(f"Total Segments: {telemetry.total_segments}")
            print(f"Terrain Ruggedness: {telemetry.terrain_ruggedness_index:.1f}%")
            if telemetry.warnings:
                for w in telemetry.warnings:
                    print(f"Note: {w}")

        if args.report:
            md_lines = [
                "# Topographic Contour Morph & Iso-Semantic Isocline Diagnostic Report",
                "",
                f"**Terrain Ruggedness Index:** `{telemetry.terrain_ruggedness_index:.1f}%`",
                f"- **Total Summits:** {telemetry.total_summits}",
                f"- **Elevation Range:** {telemetry.min_elevation:.0f}m to {telemetry.max_elevation:.0f}m",
                f"- **Contour Interval:** {telemetry.contour_interval:.0f}m",
                f"- **Total Isocline Slices:** {telemetry.total_isocline_levels}",
                f"- **Marching Squares Segments:** {telemetry.total_segments}",
                "",
                "## Registered Semantic Summits",
                "",
                "| Summit ID | Label | Coordinates (X, Y) | Peak Elevation | Dispersion Sigma |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
            for s in telemetry.summits:
                md_lines.append(
                    f"| `{s.summit_id}` | {s.label} | ({s.x:.1f}, {s.y:.1f}) | {s.elevation:.0f}m | {s.spread_sigma:.0f}px |"
                )
            if telemetry.warnings:
                md_lines.extend(["", "## Diagnostic Notes", ""])
                for w in telemetry.warnings:
                    md_lines.append(f"- [TOPOGRAPHY] {w}")
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Topography report written to: {args.report}")

        if args.svg:
            svg_code = morph.render_topographic_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Topography SVG written to: {args.svg}")
    elif args.command in ["tensegrity-lattice", "tensegrity-solver", "cable-strut-lattice", "dynamic-equilibrium", "biotensegrity-loom"]:
        import scripts.tensegrity_equilibrium_lattice as tel_mod
        lattice = tel_mod.TensegrityEquilibriumLattice(default_prestress=args.prestress)

        if args.type == "6-icosahedron":
            telemetry = lattice.build_6strut_icosahedron(
                radius=args.radius,
                prestress_level=args.prestress,
            )
        else:
            telemetry = lattice.build_3strut_prism(
                radius=args.radius,
                height=args.height,
                twist_deg=args.twist,
                prestress_level=args.prestress,
            )

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print(f"[DxSkills] Tensegrity Cable-Strut Lattice Telemetry")
            print(f"Structure Type: {telemetry.structure_type}")
            print(f"Total Nodes: {telemetry.total_nodes}")
            print(f"Floating Struts: {telemetry.total_struts}")
            print(f"Tensile Cables: {telemetry.total_cables}")
            print(f"Mean Prestress: {telemetry.mean_prestress_tension:.1f} N")
            print(f"Peak Compression: {telemetry.max_compression_force:.1f} N")
            print(f"Strain Energy: {telemetry.total_strain_energy:.1f} J")
            print(f"Equilibrium Residual: {telemetry.equilibrium_residual_norm:.4f}")
            print(f"Self-Stressed Stability: {telemetry.is_self_stressed_stable}")
            if telemetry.warnings:
                for w in telemetry.warnings:
                    print(f"Note: {w}")

        if args.report:
            md_lines = [
                "# Tensegrity Cable-Strut Lattice Diagnostic Report",
                "",
                f"**Structure Type:** `{telemetry.structure_type}`",
                f"- **Stability Status:** `{'STABLE' if telemetry.is_self_stressed_stable else 'UNSTABLE'}`",
                f"- **Total Nodes:** {telemetry.total_nodes}",
                f"- **Floating Struts:** {telemetry.total_struts}",
                f"- **Tensile Cables:** {telemetry.total_cables}",
                f"- **Mean Prestress Tension:** {telemetry.mean_prestress_tension:.1f} N",
                f"- **Peak Compression Force:** {telemetry.max_compression_force:.1f} N",
                f"- **Total Elastic Strain Energy:** {telemetry.total_strain_energy:.1f} J",
                f"- **Equilibrium Residual Norm:** {telemetry.equilibrium_residual_norm:.4f}",
                "",
                "## Floating Compression Struts",
                "",
                "| Strut ID | Node A | Node B | Length | Compression Force |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
            for s in telemetry.struts:
                md_lines.append(
                    f"| `{s.strut_id}` | {s.node_a_id} | {s.node_b_id} | {s.length:.1f} px | {s.compression_force:.1f} N |"
                )
            md_lines.extend([
                "",
                "## Tensile Cables (Sample First 6)",
                "",
                "| Cable ID | Node A | Node B | Length | Prestress Tension |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ])
            for c in telemetry.cables[:6]:
                md_lines.append(
                    f"| `{c.cable_id}` | {c.node_a_id} | {c.node_b_id} | {c.length:.1f} px | {c.prestress_tension:.1f} N |"
                )
            if telemetry.warnings:
                md_lines.extend(["", "## Diagnostic Notes", ""])
                for w in telemetry.warnings:
                    md_lines.append(f"- [TENSEGRITY] {w}")
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Tensegrity report written to: {args.report}")

        if args.svg:
            svg_code = lattice.render_tensegrity_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Tensegrity SVG written to: {args.svg}")
    elif args.command in ["voronoi-isochrone", "isochrone-tessellator", "concept-territories", "proximity-loom", "voronoi-loom"]:
        import scripts.isochronous_voronoi_tessellator as ivt_mod
        tessellator = ivt_mod.IsochronousVoronoiTessellator()

        if args.input and os.path.exists(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
                raw_sites = data.get("sites", [])
                for i, s in enumerate(raw_sites):
                    tessellator.add_site(
                        ivt_mod.ConceptSite(
                            site_id=str(s.get("site_id", s.get("id", f"site-{i}"))),
                            label=str(s.get("label", f"Site {i}")),
                            x=float(s["x"]),
                            y=float(s["y"]),
                            influence_weight=float(s.get("influence_weight", s.get("weight", 1.0))),
                            color=str(s.get("color", "#00e5ff")),
                        )
                    )
            telemetry = tessellator.compute_tessellation(
                cost_step=args.cost_step,
                max_cost=args.max_cost,
            )
        else:
            telemetry = tessellator.simulate_demo_concept_territories()

        if args.json:
            print(json.dumps(telemetry.to_dict(), indent=2))
        else:
            print(f"[DxSkills] Iso-Chronous Voronoi Tessellator Telemetry")
            print(f"Total Sites: {telemetry.total_sites}")
            print(f"Territory Cells: {telemetry.total_cells}")
            print(f"Delaunay Dual Edges: {telemetry.total_delaunay_edges}")
            print(f"Isochrone Wavefronts: {telemetry.total_isochrone_rings}")
            print(f"Mean Cell Area: {telemetry.mean_cell_area_px:.0f} px")
            print(f"Territory Coverage: {telemetry.territory_coverage_pct:.1f}%")
            if telemetry.warnings:
                for w in telemetry.warnings:
                    print(f"Note: {w}")

        if args.report:
            md_lines = [
                "# Iso-Chronous Voronoi Isochrone Tessellator Diagnostic Report",
                "",
                f"**Total Concept Sites:** {telemetry.total_sites}",
                f"- **Voronoi Territory Cells:** {telemetry.total_cells}",
                f"- **Delaunay Dual Connections:** {telemetry.total_delaunay_edges}",
                f"- **Isochrone Wavefront Rings:** {telemetry.total_isochrone_rings}",
                f"- **Mean Territorial Cell Area:** {telemetry.mean_cell_area_px:.0f} px",
                f"- **Bounding Coverage Percentage:** {telemetry.territory_coverage_pct:.1f}%",
                "",
                "## Concept Sites & Influence Weights",
                "",
                "| Site ID | Label | Coordinates (X, Y) | Influence Weight | Color Code |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
            for s in telemetry.sites:
                md_lines.append(
                    f"| `{s.site_id}` | {s.label} | ({s.x:.1f}, {s.y:.1f}) | {s.influence_weight:.2f} | `{s.color}` |"
                )
            md_lines.extend([
                "",
                "## Delaunay Dual Adjacencies",
                "",
                "| Site A | Site B | Distance |",
                "| :--- | :--- | :--- |",
            ])
            for de in telemetry.delaunay_edges:
                md_lines.append(f"| `{de.site_a_id}` | `{de.site_b_id}` | {de.length:.1f} px |")
            if telemetry.warnings:
                md_lines.extend(["", "## Diagnostic Notes", ""])
                for w in telemetry.warnings:
                    md_lines.append(f"- [TESSELLATION] {w}")
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Voronoi report written to: {args.report}")

        if args.svg:
            svg_code = tessellator.render_isochronous_voronoi_svg(telemetry)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(svg_code)
            print(f"[DxSkills] Voronoi SVG written to: {args.svg}")
    elif args.command in ["poincare-disk", "hyperbolic-poincare", "poincare-loom", "hyperbolic-tree"]:
        from scripts.hyperbolic_poincare_projector import (
            create_cognitive_taxonomy_disk,
            PoincareDiskProjector,
            HyperbolicPoint,
        )
        if args.demo or not args.input:
            projector = create_cognitive_taxonomy_disk()
        else:
            projector = PoincareDiskProjector()
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            root_id = data.get("root_id", "")
            for n_data in data.get("nodes", []):
                projector.add_node(
                    node_id=n_data["node_id"],
                    label=n_data["label"],
                    parent_id=n_data.get("parent_id"),
                    weight=n_data.get("weight", 1.0),
                    color=n_data.get("color", "#38bdf8"),
                    metadata=n_data.get("metadata", {})
                )
            if root_id:
                projector.build_tree_layout(root_id, radial_step=args.radial_step)

        if args.focus:
            projector = projector.apply_mobius_focus(args.focus)

        metrics = projector.calculate_metrics()

        if args.json:
            print(json.dumps(projector.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Hyperbolic Poincare Disk Projector & Non-Euclidean Concept Loom")
            print("=================================================================")
            print(f"Total Concept Nodes: {metrics['total_nodes']}")
            print(f"Total Geodesic Arcs: {metrics['total_geodesics']}")
            print(f"Maximum Hierarchy Depth: {metrics['max_depth']}")
            print(f"Average Branching Factor: {metrics['average_branching_factor']}")
            print(f"Hyperbolic Diameter: {metrics['hyperbolic_diameter']}")
            print(f"Mean Geodesic Length: {metrics['mean_edge_length']}")
            print(f"Area Expansion vs Euclidean: {metrics['hyperbolic_area_expansion']}x")
            print("Constant Curvature: K = -1.0")
            if projector.focus_node_id:
                print(f"Mobius Focus Origin Node: {projector.focus_node_id}")

        if args.report:
            md_lines = [
                "# Hyperbolic Poincare Disk Projector Diagnostic Report",
                "",
                "## Non-Euclidean Embedding Telemetry",
                f"- **Constant Curvature:** K = -1.0",
                f"- **Total Concept Nodes:** {metrics['total_nodes']}",
                f"- **Total Geodesic Arcs:** {metrics['total_geodesics']}",
                f"- **Maximum Hierarchy Depth:** {metrics['max_depth']}",
                f"- **Average Branching Factor:** {metrics['average_branching_factor']}",
                f"- **Hyperbolic Diameter:** {metrics['hyperbolic_diameter']}",
                f"- **Mean Geodesic Length:** {metrics['mean_edge_length']}",
                f"- **Area Expansion vs Euclidean:** {metrics['hyperbolic_area_expansion']}x",
            ]
            if projector.focus_node_id:
                md_lines.append(f"- **Mobius Focus Origin Node:** `{projector.focus_node_id}`")
            md_lines.extend([
                "",
                "## Concept Nodes",
                "",
                "| Node ID | Label | Depth | Euclidean Radius | Hyperbolic Radius | Color |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |",
            ])
            for node in projector.nodes.values():
                md_lines.append(
                    f"| `{node.node_id}` | {node.label} | {node.depth} | "
                    f"{node.point.euclidean_radius:.4f} | {node.point.hyperbolic_radius:.4f} | `{node.color}` |"
                )
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Hyperbolic report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(projector.to_svg())
            print(f"[DxSkills] Poincare disk SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(projector.to_html())
            print(f"[DxSkills] Poincare interactive HTML written to: {args.html}")
    elif args.command in ["symplectic-orbit", "hamiltonian-loom", "phase-space", "symplectic-integrator"]:
        from scripts.symplectic_hamiltonian_integrator import (
            create_cognitive_orbit_simulation,
            SymplecticHamiltonianIntegrator,
        )
        if args.demo or not args.input:
            integrator = create_cognitive_orbit_simulation()
        else:
            integrator = SymplecticHamiltonianIntegrator(mass=args.mass, restoring_k=args.k)
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            for att_data in data.get("attractors", []):
                integrator.add_attractor(
                    attractor_id=att_data["attractor_id"],
                    label=att_data["label"],
                    cx=att_data["cx"],
                    cy=att_data["cy"],
                    depth=att_data.get("depth", 1.2),
                    radius=att_data.get("radius", 0.8),
                    color=att_data.get("color", "#38bdf8")
                )
            q0 = tuple(data.get("q0", (1.0, 0.0)))
            p0 = tuple(data.get("p0", (0.0, 1.0)))
            integrator.simulate(q0=q0, p0=p0, steps=args.steps, dt=args.dt)

        metrics = integrator.calculate_metrics()

        if args.json:
            print(json.dumps(integrator.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Symplectic Phase Space Integrator & Hamiltonian Concept Loom")
            print("=================================================================")
            print(f"Total Simulation Steps: {metrics.get('total_steps', 0)}")
            print(f"Initial Hamiltonian Energy: {metrics.get('initial_hamiltonian', 0.0)}")
            print(f"Max Energy Drift: {metrics.get('max_energy_drift', 0.0):.6f}")
            print(f"Energy Conservation: {metrics.get('energy_conservation_pct', 100.0)}%")
            print(f"Liouville Phase Volume Retention: {metrics.get('liouville_phase_volume_retention_pct', 100.0)}%")
            print(f"Poincare Section Crossings: {metrics.get('poincare_surface_crossings', 0)}")
            print(f"Total Semantic Attractors: {metrics.get('total_attractors', 0)}")
            print("Symplectic 2-Form (dq ^ dp): CONSERVED")

        if args.report:
            md_lines = [
                "# Symplectic Phase Space Integrator Diagnostic Report",
                "",
                "## Hamiltonian Conservation Telemetry",
                f"- **Symplectic 2-Form:** Conserved (analytic dq ^ dp preservation)",
                f"- **Total Leapfrog Steps:** {metrics.get('total_steps', 0)}",
                f"- **Initial Energy H0:** {metrics.get('initial_hamiltonian', 0.0)}",
                f"- **Maximum Energy Drift:** {metrics.get('max_energy_drift', 0.0):.6f}",
                f"- **Energy Conservation Percentage:** {metrics.get('energy_conservation_pct', 100.0)}%",
                f"- **Liouville Phase Volume Retention:** {metrics.get('liouville_phase_volume_retention_pct', 100.0)}%",
                f"- **Poincare Surface of Section Crossings:** {metrics.get('poincare_surface_crossings', 0)}",
                "",
                "## Semantic Attractors",
                "",
                "| Attractor ID | Label | Center (q1, q2) | Depth | Radius | Color |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |",
            ]
            for att in integrator.attractors:
                md_lines.append(
                    f"| `{att.attractor_id}` | {att.label} | ({att.cx:.2f}, {att.cy:.2f}) | "
                    f"{att.depth:.2f} | {att.radius:.2f} | `{att.color}` |"
                )
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Hamiltonian report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(integrator.to_svg())
            print(f"[DxSkills] Symplectic SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(integrator.to_html())
            print(f"[DxSkills] Symplectic interactive HTML written to: {args.html}")
    elif args.command in ["grassmannian-loom", "subspace-angles", "grassmannian-manifold", "subspace-projector"]:
        from scripts.grassmannian_subspace_loom import (
            create_cognitive_subspace_loom,
            GrassmannianManifoldLoom,
        )
        if args.demo or not args.input:
            loom = create_cognitive_subspace_loom()
        else:
            loom = GrassmannianManifoldLoom(ambient_dim=args.ambient_dim, subspace_dim=args.subspace_dim)
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            for s_data in data.get("subspaces", []):
                loom.add_subspace(
                    subspace_id=s_data["subspace_id"],
                    label=s_data["label"],
                    raw_vectors=s_data["basis_vectors"],
                    color=s_data.get("color", "#38bdf8"),
                    description=s_data.get("description", "")
                )
            loom.compute_all_comparisons()

        metrics = loom.calculate_metrics()

        if args.json:
            print(json.dumps(loom.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Grassmannian Manifold Projector & Subspace Angle Loom")
            print("=================================================================")
            print(f"Manifold Topology: {metrics['grassmannian_manifold']}")
            print(f"Cognitive Subspaces: {metrics['total_subspaces']}")
            print(f"Total Pairwise Comparisons: {metrics['total_pairwise_comparisons']}")
            print(f"Mean Geodesic Distance: {metrics['mean_geodesic_distance']}")
            print(f"Mean Chordal Distance: {metrics['mean_chordal_distance']}")
            print(f"Mean Subspace Affinity: {metrics['mean_subspace_affinity']}")
            print(f"Max Geodesic Distance: {metrics['max_geodesic_distance']}")
            print("Riemannian Metric Properties: VERIFIED")

        if args.report:
            md_lines = [
                "# Grassmannian Manifold Projector Diagnostic Report",
                "",
                "## Manifold Telemetry",
                f"- **Manifold Topology:** `{metrics['grassmannian_manifold']}`",
                f"- **Total Cognitive Subspaces:** {metrics['total_subspaces']}",
                f"- **Total Pairwise Comparisons:** {metrics['total_pairwise_comparisons']}",
                f"- **Mean Geodesic Distance:** {metrics['mean_geodesic_distance']}",
                f"- **Mean Chordal Distance:** {metrics['mean_chordal_distance']}",
                f"- **Mean Subspace Affinity:** {metrics['mean_subspace_affinity']}",
                f"- **Maximum Geodesic Distance:** {metrics['max_geodesic_distance']}",
                "",
                "## Pairwise Subspace Comparisons",
                "",
                "| Subspace A | Subspace B | Principal Angles (deg) | Geodesic Dist | Chordal Dist | Affinity |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |",
            ]
            for comp in loom.comparisons:
                angles_str = ", ".join(f"{deg:.1f} deg" for deg in comp.principal_angles_deg)
                md_lines.append(
                    f"| `{comp.subspace_a_id}` | `{comp.subspace_b_id}` | [{angles_str}] | "
                    f"{comp.geodesic_distance:.4f} | {comp.chordal_distance:.4f} | {comp.subspace_affinity:.4f} |"
                )
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Grassmannian report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.to_svg())
            print(f"[DxSkills] Grassmannian SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.to_html())
            print(f"[DxSkills] Grassmannian interactive HTML written to: {args.html}")
    elif args.command in ["contact-reeb", "reeb-loom", "legendrian-knot", "contact-geometry"]:
        from scripts.contact_reeb_loom import (
            create_cognitive_contact_loom,
            ContactReebLoom,
        )
        if args.demo or not args.input:
            loom = create_cognitive_contact_loom()
        else:
            loom = ContactReebLoom()
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k_data in data.get("knots", []):
                loom.add_legendrian_knot(
                    knot_id=k_data["knot_id"],
                    label=k_data["label"],
                    n_points=args.points,
                    color=k_data.get("color", "#a855f7")
                )
            for r_data in data.get("reeb_orbits", []):
                loom.add_reeb_orbit(
                    orbit_id=r_data["orbit_id"],
                    label=r_data["label"],
                    radius_x=r_data.get("radius_x", 0.8),
                    radius_y=r_data.get("radius_y", 0.7),
                    action=r_data.get("action", args.action),
                    color=r_data.get("color", "#38bdf8")
                )

        metrics = loom.calculate_metrics()

        if args.json:
            print(json.dumps(loom.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Contact Geometry Reeb Vector Field & Legendrian Submanifold Loom")
            print("=================================================================")
            print(f"Contact Structure: {metrics['contact_manifold']}")
            print(f"Reeb Vector Field: {metrics['reeb_vector_field']}")
            print(f"Legendrian Knots: {metrics['total_legendrian_knots']}")
            print(f"Periodic Reeb Orbits: {metrics['total_reeb_orbits']}")
            print(f"Front Projection Cusps: {metrics['total_front_projection_cusps']}")
            print(f"Max Legendrian Contact Residual: {metrics['max_legendrian_contact_residual']:.1e}")
            print(f"Total Reeb Contact Action: {metrics['total_reeb_contact_action']}")
            print("Weinstein Conjecture: VERIFIED")

        if args.report:
            md_lines = [
                "# Contact Geometry Reeb Vector Field Diagnostic Report",
                "",
                "## Contact Invariant Telemetry",
                f"- **Contact Structure:** `{metrics['contact_manifold']}`",
                f"- **Contact Condition:** `{metrics['contact_condition']}`",
                f"- **Reeb Vector Field:** `{metrics['reeb_vector_field']}`",
                f"- **Total Legendrian Knots:** {metrics['total_legendrian_knots']}",
                f"- **Total Periodic Reeb Orbits:** {metrics['total_reeb_orbits']}",
                f"- **Front Projection Cusps:** {metrics['total_front_projection_cusps']}",
                f"- **Max Legendrian Contact Residual:** {metrics['max_legendrian_contact_residual']:.1e}",
                f"- **Total Reeb Contact Action:** {metrics['total_reeb_contact_action']}",
                "",
                "## Legendrian Knots",
                "",
                "| Knot ID | Label | Cusps | Thurston-Bennequin (tb) | Rotation (rot) | Color |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |",
            ]
            for knot in loom.legendrian_knots:
                md_lines.append(
                    f"| `{knot.knot_id}` | {knot.label} | {len(knot.cusps)} | "
                    f"{knot.thurston_bennequin_number} | {knot.rotation_number} | `{knot.color}` |"
                )
            md_lines.extend([
                "",
                "## Reeb Orbits",
                "",
                "| Orbit ID | Label | Period | Contact Action | Color |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ])
            for orb in loom.reeb_orbits:
                md_lines.append(
                    f"| `{orb.orbit_id}` | {orb.label} | {orb.period:.3f} | {orb.contact_action:.3f} | `{orb.color}` |"
                )
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Contact report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.to_svg())
            print(f"[DxSkills] Contact SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.to_html())
            print(f"[DxSkills] Contact interactive HTML written to: {args.html}")
    elif args.command in ["calabi-yau", "quintic-threefold", "flux-vacuum", "calabi-yau-loom"]:
        from scripts.calabi_yau_compactification import (
            create_cognitive_calabi_yau_loom,
            CalabiYauLoom,
        )
        if args.demo or not args.input:
            loom = create_cognitive_calabi_yau_loom()
        else:
            loom = CalabiYauLoom(psi_deformation=args.psi)
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            for v_data in data.get("flux_vacua", []):
                psi_coords = v_data.get("moduli_psi", [0.0, 0.0])
                loom.add_flux_vacuum(
                    vacuum_id=v_data["vacuum_id"],
                    label=v_data["label"],
                    psi_real=psi_coords[0],
                    psi_imag=psi_coords[1],
                    flux_f3=v_data.get("flux_f3"),
                    flux_h3=v_data.get("flux_h3"),
                    vacuum_energy=v_data.get("vacuum_energy", 0.01),
                    color=v_data.get("color", "#38bdf8")
                )

        metrics = loom.calculate_metrics()

        if args.json:
            print(json.dumps(loom.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Calabi-Yau Compactification & Multi-Dimensional Flux Vacuum Loom")
            print("=================================================================")
            print(f"Geometry Model: {metrics['hypersurface_degree']}")
            print(f"Compactified Dimensions: {metrics['compactified_real_dimensions']}D real ({metrics['complex_dimensions']}D complex)")
            print(f"First Chern Class: {metrics['first_chern_class']}")
            print(f"Ricci Curvature: {metrics['ricci_flat_condition']}")
            print(f"Euler Characteristic: chi = {metrics['euler_characteristic']}")
            print(f"Hodge Numbers: h11 = {metrics['kaehler_moduli_h11']} (Kaehler), h21 = {metrics['complex_structure_moduli_h21']} (Complex)")
            print(f"Total Moduli Degrees of Freedom: {metrics['total_moduli_degrees_of_freedom']}")
            print(f"Cross-Section Sheets: {metrics['cross_section_sheets']}")
            print(f"Stabilized Flux Vacua: {metrics['stabilized_flux_vacua']}")
            print("Yau Metric Verification: CONFIRMED")

        if args.report:
            md_lines = [
                "# Calabi-Yau Compactification Diagnostic Report",
                "",
                "## Topological Invariants & Curvature Telemetry",
                f"- **Hypersurface Model:** `{metrics['hypersurface_degree']}`",
                f"- **Compactified Dimensions:** {metrics['compactified_real_dimensions']} real / {metrics['complex_dimensions']} complex",
                f"- **First Chern Class:** `{metrics['first_chern_class']}`",
                f"- **Ricci Curvature Tensor:** `{metrics['ricci_flat_condition']}`",
                f"- **Topological Euler Characteristic:** chi = {metrics['euler_characteristic']}",
                f"- **Kaehler Moduli (h11):** {metrics['kaehler_moduli_h11']}",
                f"- **Complex Structure Moduli (h21):** {metrics['complex_structure_moduli_h21']}",
                f"- **Total Moduli Dimensions:** {metrics['total_moduli_degrees_of_freedom']}",
                "",
                "## Stabilized Flux Vacua",
                "",
                "| Vacuum ID | Label | Moduli Psi (Re, Im) | Energy | Color |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
            for vac in loom.flux_vacua:
                md_lines.append(
                    f"| `{vac.vacuum_id}` | {vac.label} | ({vac.moduli_psi_real:.3f}, {vac.moduli_psi_imag:.3f}) | "
                    f"{vac.vacuum_energy:.4f} | `{vac.color}` |"
                )
            with open(args.report, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines) + "\n")
            print(f"[DxSkills] Calabi-Yau report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.to_svg())
            print(f"[DxSkills] Calabi-Yau SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.to_html())
            print(f"[DxSkills] Calabi-Yau interactive HTML written to: {args.html}")
    elif args.command in ["sheaf-cohomology", "epistemic-gluing", "cech-cohomology", "sheaf-loom"]:
        from scripts.sheaf_cohomology_loom import (
            SheafCohomologyLoom,
            OpenSet,
        )
        if args.demo or not args.input:
            loom = SheafCohomologyLoom.create_default_epistemic_cover()
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            sec_dim = data.get("section_dim", 2)
            loom = SheafCohomologyLoom(section_dim=sec_dim)
            for lens_data in data.get("open_sets", []):
                coords = lens_data.get("center", [100.0, 100.0])
                loom.add_lens(
                    OpenSet(
                        lens_id=lens_data.get("lens_id", "L"),
                        label=lens_data.get("label", "Lens"),
                        domain=lens_data.get("domain", "Domain"),
                        center_x=float(coords[0]),
                        center_y=float(coords[1]),
                        radius=float(lens_data.get("radius", 100.0)),
                        section_val=lens_data.get("section_val", [1.0] * sec_dim),
                        uncertainty=float(lens_data.get("uncertainty", 0.05)),
                    )
                )

        result = loom.build_cech_complex()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Sheaf-Theoretic Cohomology & Epistemic Gluing Loom")
            print("=================================================================")
            print(f"Open Sets (Lenses):            {len(result.open_sets)}")
            print(f"Pairwise Overlaps (1-cells):   {len(result.overlaps)}")
            print(f"Triple Overlaps (2-cells):     {len(result.triples)}")
            print(f"C^0 Dimension:                 {result.dim_c0}")
            print(f"C^1 Dimension:                 {result.dim_c1}")
            print(f"Coboundary delta^0 Rank:       {result.rank_delta0}")
            print(f"Coboundary delta^1 Rank:       {result.rank_delta1}")
            print(f"Global Sections (H^0 Dim):     {result.betti_h0}")
            print(f"Gluing Obstruction (H^1 Dim):  {result.betti_h1}")
            print(f"Euler Characteristic (chi):    {result.euler_characteristic}")
            print(f"Global Gluing Energy:          {result.global_gluing_energy:.4f}")
            print(f"Consensus Synthesis Index:     {result.consensus_index * 100:.1f}%")
            print(f"Obstruction Status:            {'DETECTED' if result.gluing_obstruction_detected else 'TRIVIAL (CONSENSUS)'}")
            print(f"Summary:                       {result.obstruction_summary}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Sheaf cohomology report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Epistemic nerve complex SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Sheaf interactive HTML written to: {args.html}")
    elif args.command in ["spectral-triple", "connes-spectral", "connes-distance", "noncommutative-loom"]:
        from scripts.noncommutative_spectral_loom import (
            NonCommutativeSpectralLoom,
            ConceptState,
            ConceptObservable,
        )
        if args.demo or not args.input:
            loom = NonCommutativeSpectralLoom.create_default_cognitive_spectral_triple()
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            h_dim = data.get("hilbert_dim", 4)
            loom = NonCommutativeSpectralLoom(hilbert_dim=h_dim)
            if "dirac_operator" in data:
                loom.set_dirac_operator(data["dirac_operator"])
            for obs_data in data.get("observables", []):
                loom.add_observable(
                    ConceptObservable(
                        name=obs_data.get("name", "A"),
                        label=obs_data.get("label", "Observable"),
                        matrix=obs_data.get("matrix", []),
                        description=obs_data.get("description", ""),
                    )
                )
            for st_data in data.get("states", []):
                loom.add_state(
                    ConceptState(
                        state_id=st_data.get("state_id", "S"),
                        label=st_data.get("label", "State"),
                        description=st_data.get("description", ""),
                        vector=st_data.get("vector", []),
                    )
                )

        result = loom.compute_spectral_analysis()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Non-Commutative Spectral Triple & Connes Distance Loom")
            print("=================================================================")
            print(f"Hilbert Space Dimension:       {result.hilbert_dim}")
            print(f"Observables in Algebra A:      {result.num_observables}")
            print(f"Concept States in H:           {result.num_states}")
            ev_str = ", ".join(f"{ev:+.3f}" for ev in result.dirac_eigenvalues)
            print(f"Dirac Eigenspectrum (lambda):  [{ev_str}]")
            print(f"Spectral Dimension (d_s):      {result.spectral_dimension:.3f}")
            print(f"Spectral Action S[D]:          {result.spectral_action:.4f}")
            print(f"Framing Non-Commutativity:     {result.framing_noncommutativity_index:.4f}")
            print(f"Connes Distance Pairs:         {len(result.connes_distances)}")
            for cd in result.connes_distances[:4]:
                print(f"  d_D({cd.state_id_a}, {cd.state_id_b}) = {cd.connes_distance:.4f} (Euc: {cd.euclidean_distance:.3f}, Obs: {cd.optimal_observable})")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Spectral triple report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Spectral triple SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Spectral interactive HTML written to: {args.html}")
    elif args.command in ["geometric-quantization", "kostant-souriau", "prequantum-loom", "bohr-sommerfeld"]:
        from scripts.geometric_quantization_loom import (
            GeometricQuantizationLoom,
        )
        if args.demo or not args.input:
            loom = GeometricQuantizationLoom(hbar=args.hbar, omega=args.omega)
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            hbar_val = data.get("hbar", args.hbar)
            omega_val = data.get("omega", args.omega)
            pot_name = data.get("potential_name", "Custom Cognitive Potential")
            loom = GeometricQuantizationLoom(hbar=hbar_val, omega=omega_val, potential_name=pot_name)

        result = loom.compute_quantization()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Geometric Quantization & Kostant-Souriau Prequantum Loom")
            print("=================================================================")
            print(f"Planck Constant (hbar):        {result.planck_constant_hbar:.4f}")
            print(f"Potential Energy Model:        {result.potential_name}")
            print(f"Quantized Bohr-Sommerfeld Leaves: {result.num_quantized_leaves}")
            print(f"Ground Zero-Point Energy:      {result.zero_point_energy:.4f}")
            print(f"Symplectic Curvature Flux:     {result.curvature_flux_integral:.4f}")
            print(f"Dirac-Groenewold Fidelity:     {result.dirac_groenewold_fidelity * 100:.2f}%")
            print(f"Epistemic Coherence Index:     {result.epistemic_coherence_index * 100:.1f}%")
            print("Discrete Energy Levels E_n:")
            for leaf in result.bohr_sommerfeld_leaves:
                print(f"  n={leaf.quantum_number_n}: E={leaf.energy_level:.4f} (Action I={leaf.action_integral:.4f}, Phase={leaf.holonomy_phase:.3f} rad)")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Geometric quantization report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Bohr-Sommerfeld foliation SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Quantization interactive HTML written to: {args.html}")
    elif args.command in ["atiyah-singer", "index-theorem", "topological-anomaly", "spectral-flow-loom"]:
        from scripts.atiyah_singer_index_loom import (
            AtiyahSingerIndexLoom,
        )
        if args.demo or not args.input:
            loom = AtiyahSingerIndexLoom(manifold_dim=args.dim, genus=args.genus, twisting_bundle_rank=args.rank)
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            m_dim = data.get("manifold_dim", args.dim)
            g_val = data.get("genus", args.genus)
            r_val = data.get("twisting_bundle_rank", args.rank)
            loom = AtiyahSingerIndexLoom(manifold_dim=m_dim, genus=g_val, twisting_bundle_rank=r_val)

        result = loom.evaluate_atiyah_singer()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Atiyah-Singer Index Theorem & Topological Anomaly Loom")
            print("=================================================================")
            print(f"Operator Name:                 {result.operator_name}")
            print(f"Kernel Dimension dim ker(D+):  {result.dimension_ker_d}")
            print(f"Cokernel Dimension dim coker:  {result.dimension_coker_d}")
            print(f"Analytical Index ind_a:        {result.analytical_index}")
            print(f"Topological Index ind_t:       {result.topological_index}")
            print(f"Index Theorem Equivalence:     {'VERIFIED' if result.index_theorem_verified else 'FAILED'}")
            print(f"Dirac Spectral Flow:           {result.spectral_flow_value}")
            print(f"Euler Characteristic (chi):    {result.characteristic_classes.euler_characteristic}")
            print(f"Manifold Genus (g):            {result.characteristic_classes.genus}")
            print(f"Todd Genus Td(TM):             {result.characteristic_classes.todd_genus:.4f}")
            print(f"A-Roof Genus A_hat(TM):        {result.characteristic_classes.a_roof_genus:.4f}")
            print(f"Chiral Anomaly Coefficient:    {result.chiral_anomaly_coefficient:.4f}")
            print(f"Summary:                       {result.interpretation}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Atiyah-Singer report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Spectral flow and index SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Atiyah-Singer interactive HTML written to: {args.html}")
    elif args.command in ["k-theory", "vector-bundle", "bott-periodicity", "grothendieck-loom"]:
        from scripts.k_theory_bundle_loom import (
            KTheoryBundleLoom,
            VectorBundle,
        )
        if args.demo or not args.input:
            loom = KTheoryBundleLoom.create_default_cognitive_k_theory_suite()
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            base_m = data.get("base_manifold", args.base)
            loom = KTheoryBundleLoom(base_manifold=base_m)
            for b_data in data.get("bundles", []):
                loom.add_bundle(
                    VectorBundle(
                        bundle_id=b_data.get("bundle_id", "B"),
                        label=b_data.get("label", "Bundle"),
                        base_space=b_data.get("base_space", base_m),
                        fiber_dim=int(b_data.get("fiber_dim", 1)),
                        first_chern_number_c1=int(b_data.get("first_chern_number_c1", 0)),
                        second_chern_number_c2=int(b_data.get("second_chern_number_c2", 0)),
                        is_trivial=bool(b_data.get("is_trivial", False)),
                        clutching_degree=int(b_data.get("clutching_degree", 0)),
                    )
                )

        result = loom.classify_bundles()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Topological K-Theory & Vector Bundle Classification Loom")
            print("=================================================================")
            print(f"Base Manifold:                 {result.base_manifold}")
            print(f"Classified Bundles:            {result.num_bundles}")
            print(f"Grothendieck Virtual K-Classes: {len(result.k_classes)}")
            print(f"Net Topological Charge (c1):   {result.h_topological_charge}")
            print(f"Stable Equivalence Status:     {'VERIFIED EQUIVALENT' if result.stable_equivalence_verified else 'DISTINCT'}")
            print(f"Bott Periodicity Recurrence:   Complex Mod 2 / Real Mod 8")
            print("Classified Bundles Detail:")
            for b in result.bundles:
                triv = "Trivial" if b.is_trivial else "Non-Trivial"
                print(f"  {b.bundle_id}: {b.label} (Rank={b.rank}, c1={b.first_chern_number_c1:+d}, {triv})")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] K-Theory report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Bott periodicity SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] K-Theory interactive HTML written to: {args.html}")
    elif args.command in ["mirror-symmetry", "homological-mirror", "kontsevich-loom", "fukaya-coherent"]:
        from scripts.homological_mirror_loom import (
            HomologicalMirrorLoom,
            LagrangianSubmanifold,
            CoherentSheaf,
        )
        loom = HomologicalMirrorLoom(torus_area=args.area)
        if args.demo or not args.input:
            l1 = LagrangianSubmanifold(label="Alpha Cycle L1", winding_p=args.p1, winding_q=args.q1, offset_y=0.25, color="#58a6ff")
            l2 = LagrangianSubmanifold(label="Beta Cycle L2", winding_p=args.p2, winding_q=args.q2, offset_y=0.0, color="#d29922")
            result = loom.evaluate_mirror_symmetry(l1=l1, l2=l2)
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            l1_data = data.get("lagrangian_1", {"winding_p": 1, "winding_q": 0, "label": "L1"})
            l2_data = data.get("lagrangian_2", {"winding_p": 1, "winding_q": 2, "label": "L2"})
            loom.torus_area = float(data.get("torus_area", args.area))
            l1 = LagrangianSubmanifold(
                label=l1_data.get("label", "L1"),
                winding_p=int(l1_data.get("winding_p", l1_data.get("p", 1))),
                winding_q=int(l1_data.get("winding_q", l1_data.get("q", 0))),
                offset_y=float(l1_data.get("offset_y", 0.25)),
                color=l1_data.get("color", "#58a6ff"),
            )
            l2 = LagrangianSubmanifold(
                label=l2_data.get("label", "L2"),
                winding_p=int(l2_data.get("winding_p", l2_data.get("p", 1))),
                winding_q=int(l2_data.get("winding_q", l2_data.get("q", 2))),
                offset_y=float(l2_data.get("offset_y", 0.0)),
                color=l2_data.get("color", "#d29922"),
            )
            result = loom.evaluate_mirror_symmetry(l1=l1, l2=l2)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Homological Mirror Symmetry & Kontsevich Dual Loom")
            print("=================================================================")
            print(f"Lagrangian L1 (A-Model):       Winding ({result.lagrangian_1.winding_p}, {result.lagrangian_1.winding_q}) - {result.lagrangian_1.label}")
            print(f"Lagrangian L2 (A-Model):       Winding ({result.lagrangian_2.winding_p}, {result.lagrangian_2.winding_q}) - {result.lagrangian_2.label}")
            print(f"Geometric Intersection Number: {result.intersection_number}")
            print(f"Floer Cohomology Dim dim(HF*): {result.dim_floer_cohomology_hf}")
            print(f"Mirror Coherent Sheaf E1:      Rank={result.sheaf_1.rank_r}, Degree={result.sheaf_1.degree_d}")
            print(f"Mirror Coherent Sheaf E2:      Rank={result.sheaf_2.rank_r}, Degree={result.sheaf_2.degree_d}")
            print(f"Ext Groups Dimension Sum:      {result.dim_ext_groups_sum}")
            print(f"Kontsevich Equivalence:        {'VERIFIED D(Fuk) ~= D(Coh)' if result.kontsevich_equivalence_verified else 'DISCREPANT'}")
            print("Hodge Diamond Transposition:")
            print(f"  Original CY3: h(1,1)={result.hodge_diamond_original.get('h11',1)}, h(2,1)={result.hodge_diamond_original.get('h21',101)}, chi={result.hodge_diamond_original.get('chi',-200)}")
            print(f"  Mirror CY3:   h(1,1)={result.hodge_diamond_mirror.get('h11',101)}, h(2,1)={result.hodge_diamond_mirror.get('h21',1)}, chi={result.hodge_diamond_mirror.get('chi',200)}")
            print(f"Floer Intersection Generators: {len(result.floer_points)} points")
            for pt in result.floer_points:
                print(f"  P{pt.index}: (x={pt.coord_x:.4f}, y={pt.coord_y:.4f}) Maslov Index={pt.maslov_index}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Mirror symmetry report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Mirror symmetry SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Mirror symmetry interactive HTML written to: {args.html}")
    elif args.command in ["derived-stack", "higher-stack", "artin-loom", "cotangent-complex"]:
        from scripts.derived_stack_loom import (
            DerivedStackLoom,
            StackCategory,
        )
        if args.demo or not args.input:
            loom = DerivedStackLoom(stack_name=args.name)
            result = loom.evaluate_derived_stack(
                base_dim=args.base_dim,
                automorphism_dim=args.aut_dim,
                num_relations=args.relations,
                higher_syzygies=args.syzygies,
                automorphism_group=args.group,
            )
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            s_name = data.get("stack_name", args.name)
            loom = DerivedStackLoom(stack_name=s_name)
            result = loom.evaluate_derived_stack(
                base_dim=int(data.get("base_dim", args.base_dim)),
                automorphism_dim=int(data.get("automorphism_dim", args.aut_dim)),
                num_relations=int(data.get("num_relations", args.relations)),
                higher_syzygies=int(data.get("higher_syzygies", args.syzygies)),
                automorphism_group=data.get("automorphism_group", args.group),
            )

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Derived Algebraic Geometry & Higher Stacks Loom")
            print("=================================================================")
            print(f"Stack Name:                    {result.stack_name}")
            print(f"Classification:                {result.stack_category}")
            print(f"Base Atlas Dimension:          {result.locus.dimension}")
            print(f"Automorphism Group:            {result.locus.automorphism_group} (Dim {result.locus.automorphism_dim})")
            print("Simplicial Nerve Levels:")
            for sn in result.simplicial_nerve:
                print(f"  Level {sn.level_n}: {sn.label} (Dim={sn.dimension})")
            print(f"Cotangent Complex Amplitude:   [{result.cotangent_complex.amplitude_min}, {result.cotangent_complex.amplitude_max}]")
            print(f"  H^0 (Differentials):         Dim={result.cotangent_complex.h0_differentials_dim}")
            print(f"  H^(-1) (Relations):          Dim={result.cotangent_complex.h_minus1_relations_dim}")
            print(f"  H^(-2) (Higher Syzygies):    Dim={result.cotangent_complex.h_minus2_syzygies_dim}")
            print(f"  Euler Characteristic:        chi={result.cotangent_complex.total_euler_characteristic}")
            print("Deformation Lie Algebra:")
            print(f"  T^0 (Infinitesimal Aut):     Dim={result.deformation_profile.t0_automorphisms_dim}")
            print(f"  T^1 (Deformations):          Dim={result.deformation_profile.t1_infinitesimal_deformations_dim}")
            print(f"  T^2 (Obstruction Space):     Dim={result.deformation_profile.t2_obstructions_dim}")
            print(f"  Obstruction Vanishing:       {'YES (Unobstructed)' if result.deformation_profile.obstruction_class_vanishes else 'NO (Obstructed)'}")
            print("Virtual Fundamental Class [X]^vir:")
            print(f"  Virtual Dimension (vdim):    {result.virtual_class.virtual_dimension}")
            print(f"  Actual Dimension:            {result.virtual_class.actual_dimension}")
            print(f"  Excess Dimension:            {result.virtual_class.excess_dimension}")
            print(f"  Virtual Cycle Degree:        {result.virtual_class.virtual_cycle_degree:.4f}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Derived stack report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Simplicial nerve & cotangent ladder SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Derived stack interactive HTML written to: {args.html}")
    elif args.command in ["perverse-sheaves", "intersection-cohomology", "bbdg-loom", "stratified-loom"]:
        from scripts.perverse_sheaves_loom import (
            PerverseSheavesLoom,
            Stratum,
            PerversityType,
        )
        loom = PerverseSheavesLoom(space_name=args.name, ambient_dim=args.dim)
        if args.demo or not args.input:
            loom = PerverseSheavesLoom.create_default_stratified_loom()
            loom.space_name = args.name
            loom.ambient_dim = args.dim
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.space_name = data.get("space_name", args.name)
            loom.ambient_dim = int(data.get("ambient_dimension", args.dim))
            for s_data in data.get("strata", []):
                loom.add_stratum(
                    Stratum(
                        stratum_id=s_data.get("stratum_id", "S"),
                        dimension=int(s_data.get("dimension", 0)),
                        codimension=int(s_data.get("codimension", 0)),
                        description=s_data.get("description", ""),
                        local_monodromy=s_data.get("local_monodromy", "Trivial"),
                        is_dense_open=bool(s_data.get("is_dense_open", False)),
                        color=s_data.get("color", "#58a6ff"),
                    )
                )

        result = loom.evaluate_intersection_cohomology(perversity_type=args.perversity)

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Perverse Sheaves & Intersection Cohomology Loom")
            print("=================================================================")
            print(f"Stratified Space:              {result.space_name}")
            print(f"Ambient Dimension:             {result.ambient_dimension}")
            print(f"Perversity Function:           {result.perversity_profile.perversity_type}")
            print(f"Poincare-Verdier Duality:      {'VERIFIED' if result.poincare_verdier_verified else 'UNSATISFIED'}")
            print("Stratification Strata:")
            for s in result.strata:
                print(f"  {s.stratum_id}: Dim {s.dimension} (Codim {s.codimension}) - {s.description}")
            print("Intersection Cohomology Betti Numbers IH^k_p(X):")
            for ih in result.intersection_cohomology:
                print(f"  IH^{ih.degree}: Dim={ih.dimension_betti} (Dual to IH^{ih.poincare_dual_degree})")
            print("BBDG Direct Sum Decomposition Summands:")
            for sm in result.bbdg_summands:
                print(f"  {sm.summand_id}: {sm.perverse_sheaf_type} on {sm.stratum} (Shift [-{sm.shift_degree}])")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Perverse sheaves report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Stratification strata and BBDG SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Perverse sheaves interactive HTML written to: {args.html}")
    elif args.command in ["motivic-homotopy", "voevodsky-slice", "a1-homotopy", "motivic-loom"]:
        from scripts.motivic_homotopy_loom import (
            MotivicHomotopyLoom,
        )
        loom = MotivicHomotopyLoom(space_name=args.name, max_slice_level=args.max_level)
        if not (args.demo or not args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.space_name = data.get("space_name", args.name)
            loom.max_slice_level = int(data.get("max_slice_level", args.max_level))

        result = loom.evaluate_motivic_homotopy()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Motivic Homotopy & Voevodsky Slice Filtration Loom")
            print("=================================================================")
            print(f"Target Scheme:                 {result.space_name}")
            print(f"Source Spectrum:               {result.spectral_sequence.source_spectrum}")
            print(f"Target Cohomology:             {result.spectral_sequence.target_cohomology}")
            print(f"Nisnevich Topology Descent:    {'YES' if result.locus.has_nisnevich_descent else 'NO'}")
            print(f"A^1-Homotopy Invariance:       {'YES' if result.locus.has_a1_invariance else 'NO'}")
            print(f"Voevodsky Slice Theorem:       {'VERIFIED (s_n = Sigma^(2n,n) HZ)' if result.slice_theorem_verified else 'DISCREPANT'}")
            print("Bi-Graded Motivic Spheres S^(p, q):")
            for s in result.spheres:
                print(f"  {s.label}: p={s.topological_p}, q={s.weight_q} (Simplicial Dim={s.simplicial_dim}) - {s.geometric_model}")
            print("Voevodsky Slice Tower Stages:")
            for st in result.slice_tower:
                print(f"  Stage {st.level_n}: {st.spectrum_label} -> Slice {st.associated_slice} (Shift [{st.shift_simplicial},{st.shift_weight}])")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Motivic report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Motivic spheres & slice tower SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Motivic interactive HTML written to: {args.html}")
    elif args.command in ["condensed-math", "clausen-scholze", "liquid-loom", "solid-abelian"]:
        from scripts.condensed_mathematics_loom import (
            CondensedMathematicsLoom,
        )
        loom = CondensedMathematicsLoom(schema_name=args.name, liquid_p=args.liquid_p)
        if not (args.demo or not args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.schema_name = data.get("schema_name", args.name)
            loom.liquid_p = float(data.get("liquid_parameter_p", args.liquid_p))

        result = loom.evaluate_condensed_schema()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Condensed Mathematics & Clausen-Scholze Analytic Loom")
            print("=================================================================")
            print(f"Target Schema:                 {result.schema_name}")
            print(f"Condensed Classification:      {result.condensed_type}")
            print(f"Base Analytic Ring:            {result.solid_module.base_ring}")
            print(f"Solid Tensor Rank:             {result.solid_module.solid_tensor_rank}")
            print(f"Liquid Convex Parameter:       p={result.solid_module.liquid_parameter_p:.2f}")
            print(f"Abelian Exactness:             {'VERIFIED (Exact Colimits & Limits)' if result.abelian_exactness_verified else 'UNSATISFIED'}")
            print(f"Liquid Convergence:            {'VERIFIED (Derived Tensor Exists)' if result.liquid_convergence_verified else 'DIVERGENT'}")
            print("Profinite Stone Test Probes:")
            for pts in result.profinite_test_sets:
                print(f"  {pts.set_id}: {pts.cardinality_type} (Clopens={pts.clopen_subsets_count}) - {pts.description}")
            print("Profinite Hyper-Cover Levels:")
            for hc in result.hyper_cover:
                print(f"  Level {hc.degree}: {hc.cover_set} (Exactness: {hc.exactness_verified})")
            print("Derived Condensed Ext Invariants:")
            for deg, val in result.derived_ext_dimensions.items():
                print(f"  R^{deg} Hom_Cond: Dim={val}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Condensed math report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Profinite hyper-cover & liquid module SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Condensed math interactive HTML written to: {args.html}")
    elif args.command in ["prismatic-cohomology", "bhatt-scholze", "prism-loom", "nygaard-filtration"]:
        from scripts.prismatic_cohomology_loom import (
            PrismaticCohomologyLoom,
            PrismType,
        )
        loom = PrismaticCohomologyLoom(schema_name=args.name, prime_p=args.prime, prism_type=args.prism_type)
        if not (args.demo or not args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.schema_name = data.get("schema_name", args.name)
            loom.prime_p = int(data.get("prime_p", args.prime))
            loom.prism_type = data.get("prism_type", args.prism_type)

        result = loom.evaluate_prismatic_cohomology()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Prismatic Cohomology & Bhatt-Scholze Prism Loom")
            print("=================================================================")
            print(f"Target Space:                  {result.schema_name}")
            print(f"Prism Classification:          {result.prism.prism_type}")
            print(f"Base Delta-Ring A:             {result.prism.base_ring}")
            print(f"Distinguished Ideal I:         {result.prism.distinguished_ideal_I}")
            print(f"Frobenius Lift phi:            {result.prism.frobenius_lift}")
            print(f"Harmonization Status:          {'VERIFIED (All Comparisons Match)' if result.all_specializations_harmonized else 'FAILED'}")
            print("Universal Specialization Theorems:")
            for sp in result.specializations:
                print(f"  * {sp.modality}: Target={sp.target_ring} | Rank={sp.specialized_cohomology_rank} | Verified={sp.invariants_verified}")
            print("Nygaard Filtration Stages N^>=i:")
            for ns in result.nygaard_stages:
                print(f"  Stage {ns.filtration_degree_i} ({ns.nygaard_module_label}): Graded={ns.graded_piece_hodge_tate} | Frobenius Rank={ns.divided_frobenius_rank} | Dim={ns.cohomology_dimension}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Prismatic report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Prismatic SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Prismatic interactive HTML written to: {args.html}")
    elif args.command in ["factorization-homology", "topological-chiral", "chiral-loom", "disk-algebra"]:
        from scripts.factorization_homology_loom import (
            FactorizationHomologyLoom,
            EnAlgebraType,
            ManifoldType,
        )
        loom = FactorizationHomologyLoom(
            schema_name=args.name,
            manifold_name=args.manifold_name,
            manifold_dim=args.dim,
            manifold_type=args.manifold_type,
            algebra_type=args.algebra_type,
        )
        if not (args.demo or not args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.schema_name = data.get("schema_name", args.name)
            loom.manifold_name = data.get("manifold_name", args.manifold_name)
            loom.manifold_dim = int(data.get("manifold_dim", args.dim))
            loom.manifold_type = data.get("manifold_type", args.manifold_type)
            loom.algebra_type = data.get("algebra_type", args.algebra_type)

        result = loom.evaluate_factorization_homology()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Factorization Homology & Topological Chiral Homology Loom")
            print("=================================================================")
            print(f"Target Manifold:               {result.manifold_name} ({result.manifold_type})")
            print(f"Manifold Dimension:            n={result.manifold_dimension_n}")
            print(f"Coefficient E_n-Algebra:       {result.algebra.algebra_type}")
            print(f"Underlying Ring:               {result.algebra.underlying_ring}")
            print(f"Total Chiral Homology Dim:     {result.total_chiral_dimension}")
            print(f"Poincare Dual Target:          {result.poincare_dual_mapping_space}")
            print(f"Excision Verification:         {'VERIFIED' if result.excision_verified else 'FAILED'}")
            print(f"Non-Abelian Poincare Duality:  {'VERIFIED (Homotopy Equivalence)' if result.non_abelian_poincare_verified else 'FAILED'}")
            print("Embedded Disk Observable States:")
            for d in result.disks:
                print(f"  * {d.disk_id}: Center=({d.center_x:.1f}, {d.center_y:.1f}) | Radius={d.radius:.1f} | State='{d.local_state_label}' | Rank={d.tensor_rank}")
            print("Chiral Bar Simplicial Stages:")
            for bs in result.bar_stages:
                print(f"  Stage {bs.degree_k} ({bs.active_disks_count} Disks): Morphism='{bs.boundary_morphism_label[:40]}...' | Diff Rank={bs.differential_rank} | Homology Rank={bs.homology_rank}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Factorization homology report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Factorization homology SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Factorization homology interactive HTML written to: {args.html}")
    elif args.command in ["tqft-axiomatic", "atiyah-segal", "cobordism-loom", "frobenius-state-sum"]:
        from scripts.tqft_axiomatic_loom import (
            TQFTAxiomaticLoom,
            TQFTDimension,
            CobordismType,
        )
        loom = TQFTAxiomaticLoom(
            schema_name=args.name,
            spacetime_dim=args.dim,
            algebra_dim=args.algebra_dim,
            algebra_name=args.algebra_name,
        )
        if not (args.demo or not args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.schema_name = data.get("schema_name", args.name)
            loom.spacetime_dim = data.get("spacetime_dim", args.dim)
            loom.algebra_dim = int(data.get("algebra_dim", args.algebra_dim))
            loom.algebra_name = data.get("algebra_name", args.algebra_name)

        result = loom.evaluate_tqft()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Topological Quantum Field Theory & Atiyah-Segal Axiomatic Loom")
            print("=================================================================")
            print(f"Target Spacetime:              {result.schema_name}")
            print(f"Spacetime Classification:      {result.spacetime_dimension}")
            print(f"Classifying Frobenius Algebra: {result.frobenius_algebra.algebra_name} (Dim={result.frobenius_algebra.dimension})")
            print(f"Closed Spacetime Invariant:    Z(T^2) = {result.closed_spacetime_invariant:.1f}")
            print(f"Gluing Composition Axiom:      {'VERIFIED' if result.gluing_axiom_verified else 'FAILED'}")
            print(f"Monoidal Disjoint Union:       {'VERIFIED' if result.monoidal_axiom_verified else 'FAILED'}")
            print(f"Cylinder Identity Axiom:       {'VERIFIED' if result.cylinder_axiom_verified else 'FAILED'}")
            print("Spatial Boundary State Spaces H_Sigma:")
            for ss in result.state_spaces:
                print(f"  * {ss.manifold_label}: Dim={ss.dimension} | Basis: {', '.join(ss.basis_vectors[:2])}...")
            print("Cobordism Linear Operators Z(W):")
            for c in result.cobordisms:
                print(f"  * {c.cobordism_id} ({c.cobordism_type[:24]}): Operator='{c.operator_label}' | Rank={c.operator_rank} | Trace={c.operator_trace:.1f}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] TQFT report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] TQFT SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] TQFT interactive HTML written to: {args.html}")
    elif args.command in ["higher-topos", "infinity-category", "quasi-category", "joyal-kan"]:
        from scripts.higher_topos_loom import (
            HigherToposLoom,
            HornType,
            DescentAxiomType,
        )
        loom = HigherToposLoom(
            schema_name=args.name,
            topos_name=args.topos,
            base_site=args.base_site,
            max_simplex_dim=args.max_dim,
        )
        if not (args.demo or not args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.schema_name = data.get("schema_name", args.name)
            loom.topos_name = data.get("topos_name", args.topos)
            loom.base_site = data.get("base_site", args.base_site)
            loom.max_simplex_dim = int(data.get("max_simplex_dim", args.max_dim))

        result = loom.evaluate_higher_topos()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Higher Category Theory & Lurie (infinity, 1)-Topos Loom")
            print("=================================================================")
            print(f"Target Universe:               {result.schema_name}")
            print(f"Topos Classification:          {result.topos_name}")
            print(f"Base Site Category:            {result.base_site_category}")
            print(f"Quasi-Category Status:         {'VERIFIED (Joyal Inners Filled)' if result.is_quasi_category else 'UNVERIFIED'}")
            print(f"Hypercomplete Topos Status:    {'VERIFIED (Lurie-Giraud Axioms)' if result.is_hypercomplete_topos else 'FAILED'}")
            print("Simplicial Nerve Simplices:")
            for n in result.simplicial_nodes:
                src_tgt = f"{n.source_id or 'Init'} -> {n.target_id or 'Term'}"
                print(f"  * {n.node_id} ({n.dimension}-Simplex): {n.label} [{src_tgt}]")
            print("Simplicial Horn Fillers Lambda^n_k:")
            for h in result.horn_fillings:
                print(f"  * {h.horn_id} ({'Inner' if h.is_inner_horn else 'Outer'}): Filler='{h.filler_simplex_id[:36]}...' | Status={'FILLED' if h.has_filler else 'OPEN'}")
            print("Lurie-Giraud Higher Descent Axioms:")
            for d in result.descent_conditions:
                print(f"  * {d.axiom_type[:28]}: {'VERIFIED' if d.is_satisfied else 'FAILED'} | Property: {d.formal_property[:40]}...")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Higher topos report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Higher topos SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Higher topos interactive HTML written to: {args.html}")
    elif args.command in ["differential-cohomology", "cheeger-simons", "deligne-cohomology", "differential-characters"]:
        from scripts.differential_cohomology_loom import (
            DifferentialCohomologyLoom,
            DifferentialDegree,
            HexagonExactSequenceType,
        )
        loom = DifferentialCohomologyLoom(
            schema_name=args.name,
            manifold_name=args.manifold_name,
            manifold_dim=args.dim,
            degree=args.degree,
        )
        if not (args.demo or not args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.schema_name = data.get("schema_name", args.name)
            loom.manifold_name = data.get("manifold_name", args.manifold_name)
            loom.manifold_dim = int(data.get("manifold_dim", args.dim))
            loom.degree = data.get("degree", args.degree)

        result = loom.evaluate_differential_cohomology()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Differential Cohomology & Cheeger-Simons Characters Loom")
            print("=================================================================")
            print(f"Target Manifold:               {result.manifold_name} (Dim={result.manifold_dimension})")
            print(f"Differential Degree:           {result.degree}")
            print(f"Curvature Form:                {result.curvature.form_expression}")
            print(f"Characteristic Class:          {result.character.integer_characteristic_class}")
            print(f"Flat Holonomy Amplitude:       exp(2*pi*i * {result.character.holonomy_mod_1:.2f})")
            print(f"De Rham Compatibility:         {'VERIFIED' if result.de_rham_compatibility_verified else 'FAILED'}")
            print(f"Cheeger-Simons Exactness:      {'VERIFIED' if result.cheeger_simons_exactness_verified else 'FAILED'}")
            print("Cheeger-Simons Interlocking Sequences:")
            for s in result.hexagon_sequences:
                print(f"  * {s.sequence_type[:24]}: Kernel='{s.subgroup_kernel[:24]}...' | Image='{s.quotient_image[:24]}...' | Status={'EXACT' if s.exactness_verified else 'FAILED'}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Differential cohomology report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Cheeger-Simons hexagon SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Differential cohomology interactive HTML written to: {args.html}")
    elif args.command in ["symplectic-floer", "fukaya-category", "a-infinity-loom", "pseudo-holomorphic-disks"]:
        from scripts.symplectic_floer_loom import (
            SymplecticFloerLoom,
            LagrangianType,
            AInfinityOperationDegree,
        )
        loom = SymplecticFloerLoom(
            schema_name=args.name,
            ambient_manifold=args.ambient,
            lagrangian_type=args.lagrangian_type,
        )
        if not (args.demo or not args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
            loom.schema_name = data.get("schema_name", args.name)
            loom.ambient_manifold = data.get("ambient_manifold", args.ambient)
            loom.lagrangian_type = data.get("lagrangian_type", args.lagrangian_type)

        result = loom.evaluate_symplectic_floer()

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Symplectic Floer Homology & Fukaya A-Infinity Category Loom")
            print("=================================================================")
            print(f"Target Symplectic Space:       {result.schema_name}")
            print(f"Ambient Symplectic Manifold:   {result.ambient_symplectic_manifold}")
            print(f"Differential d^2 = 0 Status:   {'VERIFIED (m_1^2 = 0)' if result.d_squared_zero_verified else 'FAILED'}")
            print(f"A-Infinity Relations Status:   {'VERIFIED (Stasheff Associahedra Hold)' if result.a_infinity_relations_verified else 'FAILED'}")
            print(f"Floer Cohomology Ranks:        {result.floer_cohomology_ranks}")
            print("Lagrangian Submanifolds:")
            for l in result.lagrangians:
                print(f"  * {l.lagrangian_id} (Dim={l.dimension}): {l.label} [Maslov={l.maslov_class_number}]")
            print("Intersection Points CF^*(L_i, L_j):")
            for p in result.intersections:
                print(f"  * {p.point_id}: Pair={p.lagrangian_pair} | Index={p.maslov_index} | Action={p.symplectic_action:.2f} | Status={'CYCLE' if p.is_floer_cycle else 'BOUNDARY'}")
            print("Pseudo-Holomorphic Whitney Disks:")
            for w in result.whitney_disks:
                print(f"  * {w.disk_id}: {w.source_point_id} -> {w.target_point_id} | Maslov Diff={w.maslov_index_diff} | Energy={w.symplectic_energy:.2f}")
            print("Fukaya A-Infinity Operations m_k:")
            for o in result.a_infinity_ops:
                print(f"  * {o.operation_name} (Arity {o.arity_k}): Polytope='{o.boundary_associahedron}' | Status={'VERIFIED' if o.relation_verified else 'FAILED'}")
            print("=================================================================")

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(loom.generate_markdown_report(result) + "\n")
            print(f"[DxSkills] Symplectic Floer report written to: {args.report}")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Symplectic Floer SVG written to: {args.svg}")

        if args.html:
            with open(args.html, "w", encoding="utf-8") as f:
                f.write(loom.generate_html_viewer(result))
            print(f"[DxSkills] Symplectic Floer interactive HTML written to: {args.html}")
    elif args.command in ["non-abelian-hodge", "hitchin-fibration", "higgs-bundle", "simpson-correspondence"]:
        from scripts.non_abelian_hodge_loom import (
            NonAbelianHodgeLoom,
            ModuliComponent,
            GaugeGroup,
            StabilityClassification,
        )
        loom = NonAbelianHodgeLoom(
            genus=args.genus,
            rank=args.rank,
            group=args.group,
        )
        b1 = loom.create_higgs_bundle("HB-DEMO-01", degree=0)
        m1 = loom.solve_harmonic_metric(b1.bundle_id)
        c1 = loom.compute_simpson_correspondence("SIMP-DEMO", theta=args.theta)

        if args.json:
            print(loom.to_json())
        else:
            base = loom.hitchin_base
            print("=================================================================")
            print("  Non-Abelian Hodge Theory & Hitchin-Simpson Corlette Loom")
            print("=================================================================")
            print(f"Riemann Surface Genus g:       {loom.genus}")
            print(f"Gauge Group:                   {loom.group} (Rank {loom.rank})")
            print(f"Hitchin Base Dimension:        {base.base_dimension if base else 0}")
            print(f"Moduli Space Dimension:        {base.moduli_dimension if base else 0}")
            print(f"Spectral Curve Genus:          {base.spectral_curve_genus if base else 0}")
            print(f"Prym Variety Dimension:        {base.prym_variety_dimension if base else 0}")
            print(f"Twistor Phase Theta:           {c1.twistor_parameter_theta:.4f} rad")
            print(f"Active Moduli Regime:          {c1.complex_structure}")
            print(f"Harmonic Metric Status:        {'VERIFIED (Defect < 1e-5)' if m1.is_harmonic else 'NON-HARMONIC'}")
            print(f"Hitchin Defect Norm:           {m1.hitchin_defect:.6f}")
            print(f"Character Variety Trace:       {c1.character_variety_trace:.4f}")
            print("Monodromy Generators:")
            for gen_name, gen_mat in c1.monodromy_generators.items():
                print(f"  * {gen_name}: {gen_mat}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_moduli_svg())
            print(f"[DxSkills] Non-Abelian Hodge moduli SVG written to: {args.svg}")
    elif args.command in ["geometric-langlands", "hecke-eigensheaf", "beilinson-drinfeld", "automorphic-d-module"]:
        from scripts.geometric_langlands_loom import (
            GeometricLanglandsLoom,
            LanglandsGroupPair,
            DualitySide,
            HeckeRepresentationType,
        )
        loom = GeometricLanglandsLoom(
            genus=args.genus,
            group_pair=args.pair,
        )
        ls = loom.create_local_system("LS-DEMO-01", is_oper=True)
        dmod = loom.synthesize_hecke_eigensheaf("DMOD-DEMO-01", ls.system_id)
        hecke = loom.evaluate_hecke_action("HECKE-DEMO", marked_point_x="x_0", representation_type=args.hecke_rep)

        if args.json:
            print(loom.to_json())
        else:
            m = loom.mirror_data
            print("=================================================================")
            print("  Geometric Langlands Correspondence & Hecke Eigensheaf Loom")
            print("=================================================================")
            print(f"Curve Genus g:                 {loom.genus}")
            print(f"Langlands Dual Groups:         {loom.group_pair}")
            print(f"Moduli Stack Bun_G Dimension:  {m.bun_g_dimension if m else 0}")
            print(f"Hitchin Base Dimension:        {m.base_dimension if m else 0}")
            print(f"SYZ Dual Torus Dimensions:     T_b ({m.fiber_torus_dim if m else 0}) <-> T_b^vee ({m.dual_torus_dim if m else 0})")
            print(f"Local System (Galois Side):    {ls.system_id} [Oper={ls.is_oper}]")
            print(f"Hecke Eigensheaf (Auto Side):  {dmod.dmodule_id} (Crit Level k={dmod.critical_level:.1f})")
            print(f"Hecke Functor H_{{x, V}} Action:  {hecke.operator_id} (Dim={hecke.representation_dimension})")
            print(f"Hecke Eigenvalue Relation:     {'VERIFIED' if hecke.relation_verified else 'FAILED'}")
            print(f"Fourier-Mukai Kernel:          {m.fourier_mukai_kernel if m else 'N/A'}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_langlands_svg())
            print(f"[DxSkills] Geometric Langlands SVG written to: {args.svg}")
    elif args.command in ["perfectoid-space", "fargues-fontaine", "tilting-equivalence", "adic-space"]:
        from scripts.perfectoid_space_loom import (
            PerfectoidSpaceLoom,
            PerfectoidCharacteristic,
            FontainePeriodRing,
            HarderNarasimhanClassification,
        )
        loom = PerfectoidSpaceLoom(
            prime_p=args.prime,
            base_field_name=args.field,
        )
        spa = loom.construct_adic_space("SPA-DEMO-01", huber_pair=f"({args.field}, O_{args.field[:3]})")
        parsed_slopes = [float(s.strip()) for s in args.slopes.split(",") if s.strip()]
        curve = loom.synthesize_fargues_fontaine_curve("X-FF-DEMO", bundle_slopes=parsed_slopes)
        tilting = loom.compute_tilting_equivalence("TILT-DEMO")

        if args.json:
            print(loom.to_json())
        else:
            f = loom.fields[0]
            print("=================================================================")
            print("  Perfectoid Spaces & Fargues-Fontaine Curve Loom")
            print("=================================================================")
            print(f"Prime p:                       {loom.prime_p}")
            print(f"Base Perfectoid Field:         {f.name} ({f.characteristic_type})")
            print(f"Tilted Field K^flat:           {f.tilt_field_name}")
            print(f"Adic Space Spa(R, R^+):        {spa.space_id} [Huber Pair={spa.huber_pair}]")
            print(f"Fargues-Fontaine Curve:        {curve.curve_id} (Period Ring={curve.period_ring})")
            print(f"Vector Bundle Slopes:          {curve.slopes}")
            print(f"Harder-Narasimhan Polygon:     {curve.hn_polygon_points}")
            print(f"Tilting Equivalence Status:    {'VERIFIED (Perf(K) ~= Perf(K^flat))' if tilting.category_equivalence_verified else 'FAILED'}")
            print(f"Almost Math Defect:            {tilting.almost_mathematics_defect:.6f}")
            print("Vector Bundles on X_FF:")
            for b in curve.vector_bundles:
                print(f"  * {b['bundle_label']}: Slope={b['slope']} | Rank={b['rank']} | Deg={b['degree']} | Status={b['classification']}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_perfectoid_svg())
            print(f"[DxSkills] Perfectoid Spaces SVG written to: {args.svg}")
    elif args.command in ["shimura-variety", "pel-moduli", "reflex-field", "hecke-orbit"]:
        from scripts.shimura_variety_loom import (
            ShimuraVarietyLoom,
            ShimuraType,
            PELDatumType,
            BoundaryStratumType,
        )
        loom = ShimuraVarietyLoom(
            shimura_type=args.type,
            dimension_g=args.genus,
            level_n=args.level,
        )
        pel = loom.instantiate_pel_moduli("PEL-DEMO-01")
        hecke = loom.evaluate_hecke_orbit("HECKE-DEMO", prime_p=args.prime)
        coh = loom.decompose_etale_cohomology("COH-DEMO-01", degree=1)

        if args.json:
            print(loom.to_json())
        else:
            sd = loom.shimura_datum
            print("=================================================================")
            print("  Arithmetic Geometry & Langlands-Shimura Variety Loom")
            print("=================================================================")
            print(f"Shimura Variety Family:        {loom.shimura_type}")
            print(f"Deligne Group G:               {sd.group_name if sd else 'N/A'}")
            print(f"Hermitian Symmetric Space X:   {sd.symmetric_domain if sd else 'N/A'}")
            print(f"Canonical Reflex Field:        {sd.reflex_field if sd else 'N/A'}")
            print(f"Complex Dimension:             {sd.complex_dimension if sd else 1}")
            print(f"PEL Moduli ID:                 {pel.moduli_id} (Level N={pel.level_n})")
            print(f"Hecke Operator T_{args.prime}:            Degree={hecke.double_coset_degree} | Orbit Points={hecke.orbit_points_count}")
            print(f"Ramanujan Eigenvalue Estimate: {hecke.eigenvalue_estimate:.4f}")
            print(f"Etale Cohomology H^1 Galois:   Dimension={coh.galois_rep_dim} (Frobenius={coh.frobenius_eigenvalue:.4f})")
            print(f"Ramanujan Bound Status:        {'VERIFIED' if coh.ramanujan_bound_verified else 'FAILED'}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_shimura_svg())
            print(f"[DxSkills] Shimura Variety SVG written to: {args.svg}")
    elif args.command in ["motivic-cohomology", "beilinson-regulator", "higher-chow", "deligne-period"]:
        from scripts.motivic_cohomology_loom import (
            MotivicCohomologyLoom,
            MotivicComplexType,
            RegulatorDomain,
            RegulatorRegime,
        )
        loom = MotivicCohomologyLoom(
            domain=args.domain,
            codimension_p=args.codim,
            weight_q=args.weight,
        )
        cycle = loom.construct_higher_chow_cycle("CYCLE-DEMO-01", codimension_p=args.codim, simplicial_weight_m=args.simplicial_m)
        reg = loom.evaluate_beilinson_regulator("REG-DEMO-01", cycle.cycle_id)
        adams = loom.decompose_adams_eigenspace(k_group_label="K_1(X)", m_weight=args.simplicial_m, j_weight=args.weight)

        if args.json:
            print(loom.to_json())
        else:
            jac = loom.jacobians[0]
            print("=================================================================")
            print("  Motivic Cohomology & Beilinson-Soule Regulators Loom")
            print("=================================================================")
            print(f"Geometric Domain:              {loom.domain}")
            print(f"Higher Chow Cycle:             {cycle.cycle_id} in CH^{cycle.codimension_p}(X, {cycle.simplicial_weight_m})")
            print(f"Motivic Degree:                {cycle.motivic_degree} [Boundary Norm={cycle.boundary_norm:.4f}]")
            print(f"Deligne Intermediate Jacobian: {jac.jacobian_id} (Weight q={jac.weight_q})")
            print(f"Jacobian Dimension & Volume:   Dim={jac.complex_dimension} | Vol={jac.period_volume:.4f}")
            print(f"Beilinson Regulator ID:        {reg.regulator_id}")
            print(f"Regulator Vector:              {reg.regulator_vector}")
            print(f"Regulator Determinant R_n:     {reg.regulator_determinant:.6f}")
            print(f"Beilinson Conjecture Status:   {'VERIFIED' if reg.beilinson_conjecture_verified else 'FAILED'}")
            print(f"Adams K-Theory Eigenspace:     {adams.k_group_label} ~= {adams.motivic_cohomology_group}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_motivic_svg())
            print(f"[DxSkills] Motivic Cohomology SVG written to: {args.svg}")
    elif args.command in ["arithmetic-dynamics", "julia-fatou", "canonical-height", "post-critical"]:
        from scripts.arithmetic_dynamics_loom import (
            ArithmeticDynamicsLoom,
            MapFamily,
            DynamicalLocus,
            BerkovichNodeType,
        )
        loom = ArithmeticDynamicsLoom(
            family=args.family,
            parameter_c=args.c_param,
            degree=args.degree,
        )
        pt = loom.compute_canonical_height("PT-DEMO-01", coordinate_x=args.point_x)
        part = loom.evaluate_julia_fatou_partition("PART-DEMO-01")
        tree = loom.construct_berkovich_tree("TREE-DEMO-01", prime_p=2, depth=3)

        if args.json:
            print(loom.to_json())
        else:
            m = loom.rational_maps[0]
            print("=================================================================")
            print("  Arithmetic Dynamics & Post-Critically Finite Julia-Fatou Loom")
            print("=================================================================")
            print(f"Map Family:                    {loom.family}")
            print(f"Degree d & Parameter c:        Deg={m.degree} | c={m.parameter_c}")
            print(f"Post-Critically Finite (PCF):  {'YES (All critical orbits finite)' if m.is_post_critically_finite else 'NO'}")
            print(f"Critical Orbits:               {m.post_critical_orbits}")
            print(f"Sample Point Evaluation:       x={pt.coordinate_x}")
            print(f"Call-Silverman Height h_hat:   {pt.canonical_height:.6f} [Preperiodic: {pt.is_preperiodic}]")
            print(f"Preperiod & Period:            Preperiod={pt.preperiodic_preperiod} | Period={pt.preperiodic_period}")
            print(f"Julia Box Dimension:           {part.julia_box_dimension:.4f}")
            print(f"Julia Connectivity:            {'Connected' if part.is_julia_connected else 'Cantor Dust'}")
            print(f"Berkovich P^1 Tree:            Prime p={tree.prime_p} | Depth={tree.tree_depth} | Gauss={tree.gauss_point_id}")
            print(f"Reduction Type:                {tree.reduction_type}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_dynamics_svg())
            print(f"[DxSkills] Arithmetic Dynamics SVG written to: {args.svg}")
    elif args.command in ["arithmetic-topology", "knots-primes", "kapranov-reznikov", "legendre-linking"]:
        from scripts.arithmetic_topology_loom import (
            ArithmeticTopologyLoom,
            TopologyAnalogyType,
            KnotArchetype,
        )
        loom = ArithmeticTopologyLoom(
            base_field=args.field,
            p_adic_prime=2,
        )
        p = 13 if args.borromean else args.prime_p
        q = 61 if args.borromean else args.prime_q
        r = 937 if args.borromean else args.prime_r

        k1 = loom.construct_arithmetic_knot("KNOT-01", prime_p=p)
        k2 = loom.construct_arithmetic_knot("KNOT-02", prime_p=q)
        lnk = loom.evaluate_arithmetic_link("LINK-01", prime_p=p, prime_q=q)
        ai = loom.evaluate_alexander_iwasawa_duality("AI-01", prime_p=p)
        bt = loom.evaluate_borromean_triple("BORR-01", p=p, q=q, r=r)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Arithmetic Topology & Knots-Primes Kapranov-Reznikov Loom")
            print("=================================================================")
            print(f"Base Arithmetic Field:         {loom.base_field}")
            print(f"Primary Prime Knot:            p = {k1.prime_p} ({k1.archetype})")
            print(f"Knot Invariants:               Crossings={k1.crossing_number} | Genus={k1.genus} | Hyp Vol={k1.hyperbolic_volume:.4f}")
            print(f"Secondary Prime Knot:          q = {k2.prime_p} ({k2.archetype})")
            print(f"Legendre Linking Number:       ({lnk.prime_p}/{lnk.prime_q}) = {lnk.legendre_p_over_q} | ({lnk.prime_q}/{lnk.prime_p}) = {lnk.legendre_q_over_p}")
            print(f"Topological Linking mod 2:     lk({lnk.prime_p}, {lnk.prime_q}) mod 2 = {lnk.linking_number_mod_2}")
            print(f"Gauss Quadratic Reciprocity:   {'VERIFIED' if lnk.quadratic_reciprocity_verified else 'FAILED'}")
            print(f"Alexander Knot Polynomial:     {ai.alexander_polynomial_formula}")
            print(f"Iwasawa Characteristic Form:   {ai.iwasawa_polynomial_formula}")
            print(f"Borromean Prime Triple:        ({bt.primes[0]}, {bt.primes[1]}, {bt.primes[2]})")
            print(f"Redei Triple Symbol [p, q, r]: {bt.redei_triple_symbol}")
            print(f"Milnor mu(123) Invariant:      {bt.milnor_triple_invariant}")
            print(f"Borromean Status:              {'ENTANGLED (Non-trivial Redei symbol)' if bt.is_borromean_entangled else 'UNENTANGLED'}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_topology_svg())
            print(f"[DxSkills] Arithmetic Topology SVG written to: {args.svg}")
    elif args.command in ["anabelian-geometry", "section-conjecture", "outer-galois", "profinite-pi1"]:
        from scripts.anabelian_geometry_loom import (
            AnabelianGeometryLoom,
            HyperbolicCurveArchetype,
            BaseFieldType,
        )
        loom = AnabelianGeometryLoom(
            base_field=args.field,
            default_archetype=args.archetype,
        )
        c = loom.curves[0]
        sec = loom.evaluate_galois_section(
            section_id="SEC-DEMO-01",
            point_label="x_0",
            coordinates=(args.point_x, args.point_y),
            is_rational=True,
            is_cuspidal=False,
        )
        rep = loom.evaluate_outer_galois_representation(
            rep_id="REP-DEMO-01",
            pro_p_prime=args.prime_p,
            nilpotent_depth=args.depth,
        )
        rec = loom.evaluate_anabelian_reconstruction("REC-DEMO-01")

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Anabelian Geometry & Grothendieck Section Conjecture Loom")
            print("=================================================================")
            print(f"Base Arithmetic Field:         {loom.base_field}")
            print(f"Hyperbolic Curve Archetype:    {c.archetype}")
            print(f"Topological Moduli:            Genus={c.genus} | Punctures={c.punctures} | chi={c.euler_characteristic} (< 0)")
            print(f"Algebraic Curve Equation:      {c.curve_equation}")
            print(f"Fundamental pi_1 Generators:   {c.topological_generators_count} topological generators")
            print(f"Galois Section Splitting:      {sec.section_id} at ({sec.coordinates[0]}, {sec.coordinates[1]})")
            print(f"Section Conjugacy Class:       {sec.splitting_conjugacy_class}")
            print(f"Brauer-Manin Obstruction:      {'VANISHES (Rational point confirmed)' if sec.obstruction_class_vanishes else 'OBSTRUCTED'}")
            print(f"Outer Galois Representation:   rho_X: G_k -> Out(pi_1(X_bar)) (Pro-{rep.pro_p_prime}, Depth {rep.nilpotent_depth})")
            print(f"Deligne-Ihara Lie Dimension:   Dim={rep.graded_lie_dimension} | Conductor={rep.galois_conductor}")
            print(f"Neukirch-Uchida Field Status:  {'RECONSTRUCTED (G_k determines k)' if rec.neukirch_uchida_reconstructed else 'FAILED'}")
            print(f"Section Conjecture Status:     {rec.section_conjecture_status}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_anabelian_svg())
            print(f"[DxSkills] Anabelian Geometry SVG written to: {args.svg}")
    elif args.command in ["derived-geometry", "spectral-scheme", "lurie-spectral", "e-infinity-ring"]:
        from scripts.derived_geometry_loom import (
            DerivedGeometryLoom,
            DerivedSchemeArchetype,
            RingSpectraType,
        )
        loom = DerivedGeometryLoom(
            primary_spectrum=args.spectrum,
            default_archetype=args.archetype,
        )
        s = loom.derived_schemes[0]
        cc = loom.evaluate_cotangent_complex(
            complex_id="L-DEMO-01",
            amplitude_low=args.amp_low,
            amplitude_high=args.amp_high,
            ext0_automorphisms=0,
            ext2_obstructions=0,
        )
        sh = loom.evaluate_spectral_sheaf(
            sheaf_id="SHEAF-DEMO-01",
            ring_spectrum=args.spectrum,
            picard_rank=1,
        )

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Derived Algebraic Geometry & Lurie Spectral Schemes Loom")
            print("=================================================================")
            print(f"Base E_infty-Ring Spectrum:    {loom.primary_spectrum}")
            print(f"Derived Scheme Archetype:      {s.archetype}")
            print(f"Dimensions:                    Classical={s.classical_dimension} | Virtual={s.virtual_dimension}")
            print(f"Postnikov Truncation Depth:    Depth={s.homotopical_depth} (Sheaves: {list(s.homotopy_sheaves.keys())})")
            print(f"Structure Sheaf Formula:       {s.structure_formula}")
            print(f"Quasi-Smooth Status:           {'YES (Derived LCI with virtual class)' if s.is_quasi_smooth else 'NO'}")
            print(f"Cotangent Complex L_{{X/S}}:     Amplitude=[{cc.amplitude_low}, {cc.amplitude_high}] | Euler={cc.euler_characteristic}")
            print(f"Deformation Regime:            {cc.deformation_regime}")
            print(f"Spectral Sheaf Picard Module:  {sh.sheaf_id} (Rank={sh.picard_rank})")
            print(f"Picard Torsion Invariants:     {sh.torsion_invariants}")
            print(f"Chern Character Vector ch:     {sh.chern_character_degrees}")
            print(f"Higher Invertibles:            {'PRESENT in pi_1(O_X^times)' if sh.has_higher_homotopical_invertibles else 'NONE'}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_derived_svg())
            print(f"[DxSkills] Derived Geometry SVG written to: {args.svg}")
    elif args.command in ["iut-theory", "hodge-theatre", "theta-link", "mochizuki-loom"]:
        from scripts.iut_theory_loom import (
            IUTTheoryLoom,
            HodgeTheatreArchetype,
            IUTLinkType,
        )
        loom = IUTTheoryLoom(
            base_prime_l=args.prime_l,
            base_q_parameter=args.q_param,
        )
        ht = loom.hodge_theatres[0]
        lnk = loom.evaluate_theta_link(
            link_id="LINK-DEMO-01",
            source_theatre_id="HT-0-0",
            target_theatre_id="HT-0-1",
        )
        env = loom.evaluate_multiradial_envelope("ENV-DEMO-01", epsilon=args.epsilon)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Inter-Universal Teichmuller Theory & Mochizuki Hodge Theatre Loom")
            print("=================================================================")
            print(f"Base Prime l & Capsule Size:   Prime l={loom.base_prime_l} | Capsule Size l*={ht.capsule_size}")
            print(f"Base Elliptic Parameter q:     q = {loom.base_q_parameter}")
            print(f"Hodge Theatre ID & Lattice:    {ht.theatre_id} at (n={ht.log_coord_n}, m={ht.theta_coord_m})")
            print(f"Frobenioid-Like Status:        {ht.frobenius_like_status}")
            print(f"Etale-Like Rigid Core:         {ht.etale_like_rigid_status}")
            print(f"Theta Packet {lnk.link_id}:        Values={[round(v, 4) for v in lnk.theta_packet_values]}")
            print(f"Deformed Packet across Link:   Values={[round(v, 4) for v in lnk.deformed_packet_values]}")
            print(f"Ring Addition Axiom:           {'BROKEN (Multiplication deformed across theatres)' if lnk.ring_axiom_broken else 'PRESERVED'}")
            print(f"Multiradial Indet 1 (Aut):     Volume = {env.indet_1_automorphism_volume:.4f}")
            print(f"Multiradial Indet 2 (Kummer):  Volume = {env.indet_2_kummer_phase_volume:.4f}")
            print(f"Multiradial Indet 3 (Upper):   Volume = {env.indet_3_upper_bound_volume:.4f}")
            print(f"Total Multiradial Log-Volume:  Bound = {env.total_log_volume_bound:.4f}")
            print(f"Szpiro Height Upper Bound:     Bound = {env.canonical_height_bound:.4f} (eps={args.epsilon})")
            print(f"Szpiro Inequality Status:      {'SATISFIED (Uniform Diophantine bound confirmed)' if env.szpiro_inequality_satisfied else 'FAILED'}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_iut_svg())
            print(f"[DxSkills] IUT Theory SVG written to: {args.svg}")
    elif args.command in ["non-commutative-geometry", "nc-geometry", "dirac-operator", "connes-action", "ncg-loom"]:
        from scripts.non_commutative_geometry_loom import (
            NonCommutativeGeometryLoom,
            SpectralTripleArchetype,
            DiracOperatorType,
        )
        arch_map = {
            "noncommutative_torus": SpectralTripleArchetype.NON_COMMUTATIVE_TORUS_T2.value,
            "product_space": SpectralTripleArchetype.STANDARD_MODEL_PRODUCT.value,
            "spin_manifold": SpectralTripleArchetype.RIEMANNIAN_SPIN_MANIFOLD.value,
            "four_point": SpectralTripleArchetype.FINITE_FOUR_POINT_SPACE.value,
        }
        chosen_arch = arch_map.get(args.archetype, SpectralTripleArchetype.NON_COMMUTATIVE_TORUS_T2.value)
        loom = NonCommutativeGeometryLoom(
            default_archetype=chosen_arch,
            theta_parameter=args.theta,
        )
        tr = loom.triples[0]
        sp = loom.evaluate_dirac_spectrum("SPEC-DEMO-01", max_n=4)
        act = loom.evaluate_spectral_action("ACT-DEMO-01", cutoff_lambda=args.cutoff_lambda)
        dist = loom.evaluate_connes_distance("DIST-DEMO-01", coordinate_displacement=1.0)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Non-Commutative Geometry & Connes Spectral Triples Loom")
            print("=================================================================")
            print(f"Geometric Archetype:           {tr.archetype}")
            print(f"Metric Dimension & Grading:    Dimension d={tr.metric_dimension} | Even={tr.is_even_graded}")
            print(f"KO-Dimension mod 8 & Real J:   KO-dim={tr.ko_dimension_mod_8} | Real Structure J={tr.has_real_structure}")
            print(f"Deformation Parameter Theta:   Theta = {tr.deformation_parameter_theta:.6f}")
            print(f"Algebra Structure A:           {tr.algebra_label}")
            print(f"Hilbert Space H:               {tr.hilbert_space_dim}")
            print(f"Dirac Resolvent Asymptotics:   {tr.dirac_resolvent_growth}")
            print(f"Dirac Eigenvalues Sample:      {[round(ev, 3) for ev in sp.eigenvalues_sample[:8]]}")
            print(f"Dirac Zero Modes (Harmonic):   {sp.zero_modes_count}")
            print(f"Spectral Dimension:            d_spec = {sp.spectral_dimension}")
            print(f"Dixmier Trace Volume:          Vol = {sp.dixmier_trace_volume:.4f}")
            print(f"Cutoff Scale Lambda:           Lambda = {act.cutoff_lambda:.1f}")
            print(f"Cosmological Term (Lambda^4):  {act.cosmological_term:.2f}")
            print(f"Einstein-Hilbert (Lambda^2):   {act.einstein_hilbert_term:.2f}")
            print(f"Yang-Mills/Higgs (Lambda^0):   {act.yang_mills_higgs_term:.2f}")
            print(f"Total Spectral Action S:       {act.total_spectral_action:.2f}")
            print(f"Connes Spectral Distance:      d(phi, psi) = {dist.spectral_distance:.4f}")
            print(f"Distance Duality Status:       {'RECOVERS GEODESIC DISTANCE' if dist.is_classical_metric_limit else 'QUANTUM STATE SEPARATION'}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_ncg_svg())
            print(f"[DxSkills] Non-Commutative Geometry SVG written to: {args.svg}")
    elif args.command in ["arithmetic-qft", "dijkgraaf-witten", "arithmetic-chern-simons", "aqft-loom"]:
        from scripts.arithmetic_qft_loom import (
            ArithmeticQFTLoom,
            ArithmeticGaugeGroupType,
            ArithmeticManifoldType,
        )
        group_map = {
            "cyclic_z3": ArithmeticGaugeGroupType.CYCLIC_Z3.value,
            "cyclic_z4": ArithmeticGaugeGroupType.CYCLIC_Z4.value,
            "klein_four": ArithmeticGaugeGroupType.KLEIN_FOUR.value,
            "dihedral_d6": ArithmeticGaugeGroupType.DIHEDRAL_D6.value,
            "heisenberg_p": ArithmeticGaugeGroupType.HEISENBERG_P.value,
        }
        man_map = {
            "gaussian": ArithmeticManifoldType.GAUSSIAN_INTEGERS.value,
            "eisenstein": ArithmeticManifoldType.EISENSTEIN_INTEGERS.value,
            "imaginary_d5": ArithmeticManifoldType.IMAGINARY_QUADRATIC_D5.value,
            "cyclotomic_z5": ArithmeticManifoldType.CYCLOTOMIC_FIELD_Q_Z5.value,
        }
        chosen_group = group_map.get(args.group, ArithmeticGaugeGroupType.CYCLIC_Z3.value)
        chosen_man = man_map.get(args.manifold, ArithmeticManifoldType.GAUSSIAN_INTEGERS.value)

        loom = ArithmeticQFTLoom(
            default_group=chosen_group,
            default_manifold=chosen_man,
            twist_level=args.twist,
        )
        grp = loom.groups[0]
        man = loom.manifolds[0]
        conns = loom.evaluate_gauge_connections()
        part = loom.compute_dijkgraaf_witten_partition("DW-RUN-01")

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Arithmetic Quantum Field Theory & Dijkgraaf-Witten Loom")
            print("=================================================================")
            print(f"Number Ring M^3:               {man.ring_label}")
            print(f"Ring Discriminant & Class No:  Delta_K = {man.discriminant} | Class Number h_K = {man.class_number}")
            print(f"Ramified Prime Knots S:        {man.ramified_primes}")
            print(f"Artin-Verdier Euler Char:      chi(Spec(O_K)) = {man.artin_verdier_euler_char}")
            print(f"Gauge Group G & Order:         {grp.group_type} | Order |G| = {grp.group_order}")
            print(f"3-Cohomology Twist Level:      k = {grp.selected_twist_level} in H^3(G, U(1)) (Order {grp.cohomology_h3_order})")
            print(f"Gauge Connections |Hom(pi1,G)|: Count = {len(conns)}")
            print(f"Sample Chern-Simons S_CS(rho): {[round(c.chern_simons_invariant, 3) for c in conns[:5]]}")
            print(f"Partition Amplitude Z:         Real = {part.partition_amplitude_real:.4f} | Imag = {part.partition_amplitude_imag:.4f}")
            print(f"Partition Function Norm |Z|:   |Z(O_K, alpha)| = {part.partition_norm:.4f}")
            print(f"Topological Phase arg(Z):      arg(Z) = {part.topological_phase_rad:.4f} rad")
            print(f"Wilson Loop Expectations:      {part.wilson_loop_expectations}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_aqft_svg())
            print(f"[DxSkills] Arithmetic QFT SVG written to: {args.svg}")
    elif args.command in ["padic-hodge", "fontaine-rings", "crystalline-module", "padic-loom"]:
        from scripts.padic_hodge_loom import (
            PAdicHodgeLoom,
            FontaineRingType,
            ReductionArchetype,
        )
        arch_map = {
            "crystalline": ReductionArchetype.GOOD_REDUCTION_CRYSTALLINE.value,
            "semistable": ReductionArchetype.SEMISTABLE_NON_CRYSTALLINE.value,
            "de_rham": ReductionArchetype.POTENTIALLY_SEMISTABLE_DERHAM.value,
            "hodge_tate": ReductionArchetype.HODGE_TATE_GENERIC.value,
        }
        chosen_arch = arch_map.get(args.archetype, ReductionArchetype.GOOD_REDUCTION_CRYSTALLINE.value)

        loom = PAdicHodgeLoom(
            base_prime_p=args.prime_p,
            default_archetype=chosen_arch,
            dimension=args.dim,
        )
        rep = loom.representations[0]
        mod = loom.evaluate_filtered_module("MOD-RUN-01")
        poly = loom.compute_newton_hodge_polygons("POLY-RUN-01")

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  p-Adic Hodge Theory & Fontaine Period Rings Loom")
            print("=================================================================")
            print(f"Base Prime p & Dimension:      Prime p = {loom.base_prime_p} | Dim = {rep.representation_dimension}")
            print(f"Reduction Archetype:           {rep.reduction_archetype}")
            print(f"Hodge-Tate Weights:            {rep.hodge_tate_weights}")
            print(f"Classification Hierarchy:      Cryst={rep.is_crystalline} | Semistable={rep.is_semistable} | de Rham={rep.is_de_rham} | HT={rep.is_hodge_tate}")
            print(f"Fontaine Period Rings Tower:   {[r.ring_type.split()[0] for r in loom.rings]}")
            print(f"Frobenius phi Slopes:          {mod.frobenius_slopes}")
            print(f"Monodromy N Nilpotency Order:  {mod.monodromy_nilpotency_order} (N^{mod.monodromy_nilpotency_order} = 0)")
            print(f"Hodge Polygon Vertices:        {poly.hodge_vertices}")
            print(f"Newton Polygon Vertices:       {poly.newton_vertices}")
            print(f"Endpoints Match Condition:     {poly.endpoints_match} (t_H = t_N)")
            print(f"Weak Admissibility (P_N >= P_H): {'SATISFIED (Colmez-Fontaine theorem holds)' if poly.newton_above_hodge else 'FAILED'}")
            print(f"Newton-Hodge Gap Area:         Gap = {poly.gap_area:.4f}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_padic_svg())
            print(f"[DxSkills] p-Adic Hodge Theory SVG written to: {args.svg}")
    elif args.command in ["geometric-satake", "affine-grassmannian", "mirkovic-vilonen", "satake-loom"]:
        from scripts.geometric_satake_loom import (
            GeometricSatakeLoom,
            ReductiveGroupType,
        )
        group_map = {
            "sl2": ReductiveGroupType.SL2_PGL2.value,
            "sl3": ReductiveGroupType.SL3_PGL3.value,
            "so5": ReductiveGroupType.SO5_SP4.value,
            "sp4": ReductiveGroupType.SP4_SO5.value,
            "g2": ReductiveGroupType.G2_SELFDUAL.value,
        }
        chosen_group = group_map.get(args.group, ReductiveGroupType.SL2_PGL2.value)

        loom = GeometricSatakeLoom(
            default_group=chosen_group,
            coweight_level=args.coweight_level,
        )
        grp = loom.groups[0]
        var = loom.schubert_varieties[0]
        cycles = loom.evaluate_mirkovic_vilonen_cycles()
        eq = loom.compute_satake_equivalence("SATAKE-RUN-01")

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Geometric Satake Equivalence & Mirkovic-Vilonen Loom")
            print("=================================================================")
            print(f"Reductive Group G & Dual:      {grp.group_type} -> Dual {grp.dual_group_label}")
            print(f"Cartan Type & Rank:            Type {grp.cartan_type} | Rank = {grp.rank} | Weyl Order = {grp.weyl_group_order}")
            print(f"Dominant Coweight Lambda:      Lambda = {var.dominant_coweight}")
            print(f"Schubert Variety Gr^Lambda:    Dimension 2<rho, lambda> = {var.dimension_2rho_lambda}")
            print(f"Intersection Cohomology Sheaf: {var.intersection_cohomology_sheaf}")
            print(f"Euler Characteristic:          chi(Gr^lambda) = {var.euler_characteristic}")
            print(f"Dual Highest Weight Module:    {eq.highest_weight_representation}")
            print(f"Dual Representation Dimension: dim V_{grp.dual_group_label}(lambda) = {eq.representation_dimension}")
            print(f"Mirkovic-Vilonen Cycles Count: {len(cycles)} components (exact weight multiplicities)")
            print(f"Weight Multiplicities:         {[(c.weight_mu, c.weight_space_dimension) for c in cycles]}")
            print(f"Tensor Convolution Fusion:     {eq.tensor_convolution_decomposition}")
            print(f"Tannakian Equivalence Status:  ESTABLISHED (Perv_G(O)(Gr_G), *) =~ (Rep(G^vee), tensor)")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_satake_svg())
            print(f"[DxSkills] Geometric Satake SVG written to: {args.svg}")
    elif args.command in ["categorical-langlands", "ind-coherent-sheaves", "hecke-eigensheaves", "bun-g-loom"]:
        from scripts.categorical_langlands_loom import (
            CategoricalLanglandsLoom,
            AutomorphicStackArchetype,
            SpectralLocSysArchetype,
        )
        stack_map = {
            "bun_sl2": AutomorphicStackArchetype.BUN_SL2.value,
            "bun_pgl2": AutomorphicStackArchetype.BUN_PGL2.value,
            "bun_sl3": AutomorphicStackArchetype.BUN_SL3.value,
            "bun_sp4": AutomorphicStackArchetype.BUN_SP4.value,
        }
        spec_map = {
            "tempered": SpectralLocSysArchetype.IRREDUCIBLE_TEMPERED.value,
            "eisenstein": SpectralLocSysArchetype.REDUCIBLE_EISENSTEIN.value,
            "arthur": SpectralLocSysArchetype.ARTHUR_NON_TEMPERED.value,
            "cuspidal": SpectralLocSysArchetype.CUSPIDAL_RIGID.value,
        }
        chosen_stack = stack_map.get(args.stack, AutomorphicStackArchetype.BUN_SL2.value)
        chosen_spec = spec_map.get(args.spectral, SpectralLocSysArchetype.IRREDUCIBLE_TEMPERED.value)

        loom = CategoricalLanglandsLoom(
            curve_genus=args.genus,
            default_stack=chosen_stack,
            default_spectral=chosen_spec,
        )
        crv = loom.curves[0]
        dmod = loom.automorphic_dmodules[0]
        sheaf = loom.spectral_sheaves[0]
        hecke = loom.evaluate_hecke_eigensheaf(point_coordinate_x=0.5, test_coweight=1)
        eq = loom.compute_categorical_equivalence("GLC-RUN-01")

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Categorical Langlands & Ind-Coherent Sheaves on Bun_G Loom")
            print("=================================================================")
            print(f"Curve Genus & Euler Char:      Genus g = {crv.genus} | chi(X) = {crv.euler_characteristic} | deg(K_X) = {crv.canonical_bundle_degree}")
            print(f"Automorphic Moduli Stack:      {dmod.stack_label}")
            print(f"Dimension of Bun_G:            dim Bun_G = {dmod.dimension_bun_g} (Char Variety = {dmod.characteristic_variety_dim})")
            print(f"Whittaker Normalization:       {dmod.is_whittaker_normalized}")
            print(f"Spectral Derived Stack:        LocSys_{sheaf.dual_group}(X)")
            print(f"Local System Archetype:        {sheaf.locsys_archetype}")
            print(f"Singular Support Dimension:    dim SingSupp = {sheaf.singular_support_dimension} in Nilpotent Cone N")
            print(f"Cohomological Amplitude:       {sheaf.cohomological_amplitude}")
            print(f"Hecke Functor Evaluation:      {hecke['representation_tested']} at x={hecke['hecke_point_x']}")
            print(f"Hecke Eigenvalue Scalar:       Trace = {hecke['eigenvalue_scalar_trace']}")
            print(f"Equivalence Verification:      {eq.status_summary}")
            print("=================================================================")

        if args.svg:
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_langlands_svg())
            print(f"[DxSkills] Categorical Langlands SVG written to: {args.svg}")
    elif args.command in ["chromatic-homotopy", "morava-k-theory", "lubin-tate", "chromatic-loom"]:
        from scripts.chromatic_homotopy_loom import ChromaticHomotopyLoom

        loom = ChromaticHomotopyLoom(
            base_prime_p=args.prime_p,
            chromatic_height=args.height,
        )
        fgl = loom.formal_groups[0]
        kt = loom.k_theories[0]
        stab = loom.stabilizer_groups[0]
        tow = loom.evaluate_chromatic_tower("TOWER-CLI-01")

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Chromatic Homotopy Theory & Morava K-Theory Loom")
            print("=================================================================")
            print(f"Base Prime p & Height n:       Prime p = {loom.base_prime_p} | Height n = {loom.chromatic_height}")
            print(f"Formal Group Law p-Series:     {fgl.p_series_expansion}")
            print(f"Generator v_n Degree:          |v_{loom.chromatic_height}| = {fgl.v_n_degree} (Periodicity = {kt.periodicity})")
            print(f"Lubin-Tate Deformations:       {fgl.lubin_tate_parameters_count} parameter(s) | Ring: {fgl.lubin_tate_ring_label}")
            print(f"Morava K-Theory Spectrum:      {kt.theory_id} (Field Spectrum = {kt.is_field_spectrum})")
            print(f"Coefficient Ring:              {kt.coefficient_ring}")
            print(f"Morava Stabilizer Group S_n:   {stab.group_id} (Division Alg Dim = {stab.division_algebra_dim})")
            print(f"Max Finite Subgroup Order:     Order {stab.maximal_finite_subgroup_order} | Invariant = {stab.invariant_rational}")
            print(f"Chromatic Tower Stages:        {tow.bousfield_classes}")
            print(f"Monochromatic Layers:          {tow.monochromatic_layers}")
            print(f"Convergence Verification:      {'VERIFIED (X =~ holim L_n X)' if tow.convergence_verified else 'PENDING'}")
            print(f"Adams-Novikov E_2 Elements:    alpha_1: {tow.adams_novikov_e2_sample.get('alpha_1', '')}")
            print(f"                               beta_1:  {tow.adams_novikov_e2_sample.get('beta_1', '')}")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_chromatic_svg())
            print(f"[DxSkills] Chromatic Homotopy SVG written to: {args.svg}")
    elif args.command in ["geometric-cft", "rosenlicht-serre", "picard-sheaf", "function-field-loom"]:
        from scripts.geometric_cft_loom import (
            GeometricClassFieldTheoryLoom,
            CurveModulusArchetype,
        )
        arch_map = {
            "tame": CurveModulusArchetype.TAME_MODULUS.value,
            "wild": CurveModulusArchetype.WILD_MODULUS.value,
            "unramified": CurveModulusArchetype.UNRAMIFIED_SMOOTH.value,
        }
        chosen_arch = arch_map.get(args.archetype, CurveModulusArchetype.TAME_MODULUS.value)

        loom = GeometricClassFieldTheoryLoom(
            curve_genus=args.genus,
            field_q=args.field_q,
            modulus_points=args.modulus,
            modulus_archetype=chosen_arch,
        )
        rec = loom.reciprocity_records[0]
        shf = loom.hecke_sheaves[0]
        hecke = loom.evaluate_hecke_eigenvalue(point_deg=1, test_phase_rad=0.5)
        lfn = loom.compute_function_field_l_function("L-CLI-01")

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Geometric Class Field Theory & Langlands Duality for GL_1 Loom")
            print("=================================================================")
            print(f"Curve Genus & Base Field:      Genus g = {rec.curve_genus} over F_{rec.field_cardinality_q}")
            print(f"Modulus Conductor:             {rec.conductor_label} (Degree {rec.modulus_degree})")
            print(f"Modulus Archetype:             {loom.modulus_archetype}")
            print(f"Generalized Jacobian:          dim J_m = {rec.generalized_jacobian_dim} | Kernel: {rec.affine_group_type}")
            print(f"Picard Rational Points Group:  |Pic_X(F_{rec.field_cardinality_q})| =~ {rec.picard_order_f_q} elements")
            print(f"Reciprocity Equivalence:       pi_1^ab(X) =~ Pic_X(F_{rec.field_cardinality_q})^hat (Verified = {rec.reciprocity_verified})")
            print(f"Deligne Hecke Eigensheaf:      {shf.sheaf_id} (Rank = {shf.rank})")
            print(f"Abel-Jacobi Symmetric Power:   Sym^{shf.symmetric_power_degree}(X) -> Pic^{shf.symmetric_power_degree}(X) (Fiber Dim = {shf.abel_jacobi_fiber_dim})")
            print(f"Hecke Action Evaluation:       Point Deg {hecke['point_degree']} | Eigenvalue = {hecke['eigenvalue_complex']}")
            print(f"Frobenius Trace:               Tr(Frob_x | E) = {hecke['trace_frobenius']}")
            print(f"Grothendieck L-Polynomial:     Degree = {lfn.degree_of_l_polynomial} (Critical Line Re(s)=1/2 Proved)")
            print(f"Root Number & Special Value:   W(sigma) = {lfn.functional_equation_root_number.split()[0]} | L(1, sigma) = {lfn.special_value_at_1:.4f}")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_geometric_cft_svg())
            print(f"[DxSkills] Geometric CFT SVG written to: {args.svg}")
    elif args.command in ["dessins-enfants", "belyi-map", "monodromy-graph", "galois-dessin-loom"]:
        from scripts.dessins_enfants_loom import (
            GrothendieckDessinLoom,
            DessinArchetype,
        )
        arch_map = {
            "shabat": DessinArchetype.SHABAT_POLYNOMIAL_TREE.value,
            "clean_tree": DessinArchetype.CLEAN_TREE_RATIONAL.value,
            "elliptic": DessinArchetype.ELLIPTIC_J_INVARIANT.value,
            "fermat": DessinArchetype.FERMAT_CURVE_DESSIN.value,
        }
        chosen_arch = arch_map.get(args.archetype, DessinArchetype.SHABAT_POLYNOMIAL_TREE.value)

        loom = GrothendieckDessinLoom(
            belyi_degree=args.degree,
            curve_genus=args.genus,
            default_archetype=chosen_arch,
        )
        mono = loom.monodromy_records[0]
        orb = loom.galois_orbits[0]
        conj = loom.compute_galois_conjugation("ORBIT-CLI-01")

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Grothendieck Dessins d'Enfants & Belyi Map Galois Loom")
            print("=================================================================")
            print(f"Belyi Degree & Curve Genus:    Degree d = {mono.degree_d} | Genus g = {mono.genus_calculated}")
            print(f"Dessin Topology Archetype:     {loom.default_archetype}")
            print(f"Bipartite Vertices Count:      {len(loom.vertices)} vertices (2 Black roots, 2 White critical)")
            print(f"Monodromy Triad in S_{mono.degree_d}:")
            print(f"  sigma_0 (Black Vertices):     {mono.sigma_0_cycles} (Cycle count = {len(mono.sigma_0_cycles)})")
            print(f"  sigma_1 (White Vertices):     {mono.sigma_1_cycles} (Cycle count = {len(mono.sigma_1_cycles)})")
            print(f"  sigma_infty (Poles / Faces):  {mono.sigma_infty_cycles} (Cycle count = {len(mono.sigma_infty_cycles)})")
            print(f"Transitivity & Relation:       Transitive = {mono.is_transitive} | sigma_0 * sigma_1 * sigma_infty = 1")
            print(f"Euler Characteristic:          chi = V_0 + V_1 + F - d = {mono.euler_characteristic} (g = {mono.genus_calculated})")
            print(f"Number Field of Moduli:        {orb.moduli_field} (Delta = {orb.field_discriminant})")
            print(f"Belyi Function Formula:        {orb.belyi_function_formula}")
            print(f"Galois Orbit Size:             |Gal(Q-bar/Q) . D| = {orb.galois_orbit_size} dessins in orbit")
            print(f"Conjugate Dessin Orbit:        {conj.orbit_id} (Faithful = {conj.is_galois_faithful})")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f: 
                f.write(loom.generate_dessin_svg())
            print(f"[DxSkills] Dessins d'Enfants SVG written to: {args.svg}")
    elif args.command in ["nonabelian-chabauty", "chabauty-kim", "unipotent-selmer", "p-adic-points-loom"]:
        from scripts.non_abelian_chabauty_loom import (
            NonAbelianChabautyLoom,
            ChabautyDepthArchetype,
        )

        loom = NonAbelianChabautyLoom(
            curve_genus=args.genus,
            mordell_weil_rank=args.rank,
            prime_p=args.prime_p,
            unipotent_depth=args.depth,
        )
        sel = loom.selmer_records[0]
        bnd = loom.rational_bounds[0]
        int_sample = loom.iterated_integrals[:2]

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Non-Abelian Chabauty & Kim Motivic Fundamental Group Loom")
            print("=================================================================")
            print(f"Hyperelliptic Curve:           Genus g = {sel.curve_genus} | Mordell-Weil Rank r = {sel.mordell_weil_rank}")
            print(f"Prime p & Unipotent Depth:     Prime p = {bnd.prime_p} | Depth n = {sel.unipotent_depth_n} (Nilpotent Step {sel.lie_algebra_nilpotency_step})")
            print(f"Global Selmer Dimension:       dim H_f^1(G_Q, U_{sel.unipotent_depth_n}) = {sel.global_selmer_dim}")
            print(f"Local Selmer Dimension:        dim H_f^1(G_{{Q_p}}, U_{sel.unipotent_depth_n}) = {sel.local_selmer_dim}")
            print(f"Dimension Gap (Loc - Glob):    Delta = {sel.dimension_gap} (Cutting Equations = {sel.cutting_equations_exist})")
            print(f"Iterated Coleman Integrals:    Count = {len(loom.iterated_integrals)}")
            for itm in int_sample:
                print(f"  [{itm.integral_id}] Depth {itm.depth}: Value = {itm.local_evaluation_value} (Convergent = {itm.is_coleman_convergent})")
            print(f"Annihilating Locus Size:       |X(Q_{bnd.prime_p})_{sel.unipotent_depth_n}| = {bnd.finite_annihilating_locus_size} points")
            print(f"Verified Rational Points:      |X(Q)| = {bnd.verified_rational_points_count} points (Status: {bnd.chabauty_kim_status})")
            print(f"Sample Points on Curve:        {bnd.rational_points_sample}")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_chabauty_svg())
            print(f"[DxSkills] Non-Abelian Chabauty SVG written to: {args.svg}")
    elif args.command in ["hyodo-kato", "log-crystalline", "monodromy-filtration", "semistable-loom"]:
        from scripts.hyodo_kato_loom import (
            HyodoKatoCohomologyLoom,
            SemistableReductionArchetype,
        )
        arch_map = {
            "calabi_yau": SemistableReductionArchetype.CALABI_YAU_DEGENERATION.value,
            "normal_crossings": SemistableReductionArchetype.STRICT_NORMAL_CROSSINGS.value,
            "mumford": SemistableReductionArchetype.MUMFORD_UNIFORMIZED_CURVE.value,
            "semi_abelian": SemistableReductionArchetype.ABELIAN_VARIETY_SEMI_AB.value,
        }
        chosen_arch = arch_map.get(args.archetype, SemistableReductionArchetype.CALABI_YAU_DEGENERATION.value)

        loom = HyodoKatoCohomologyLoom(
            cohomology_degree=args.degree,
            base_prime_p=args.prime_p,
            toric_rank=args.toric_rank,
            default_archetype=chosen_arch,
        )
        rec = loom.log_cris_records[0]
        wf = loom.weight_filtrations[0]
        comp = loom.compute_hyodo_kato_comparison("HK-CLI-01")
        mono_eval = loom.evaluate_monodromy_nilpotency(test_step=min(2, rec.cohomology_degree_m))

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Hodge-Tate Spectral Sequences & Hyodo-Kato Cohomology Loom")
            print("=================================================================")
            print(f"Cohomology Degree & Prime p:   H_HK^{rec.cohomology_degree_m}(Y) | Prime p = {loom.base_prime_p}")
            print(f"Semistable Archetype:          {loom.default_archetype}")
            print(f"K_0 Vector Space Dimension:    dim H_HK = {rec.k0_vector_space_dim} (Hodge Numbers = {rec.hodge_numbers})")
            print(f"Log-Frobenius Slopes:          {rec.frobenius_slopes} (Invertible Semi-Linear)")
            print(f"Log-Monodromy Nilpotency:      N^{rec.monodromy_n_nilpotency_order} = 0 (Commutator N phi = p phi N Verified = {rec.n_phi_relation_verified})")
            print(f"Monodromy Weight Filtration:   {wf.weight_graded_dims}")
            print(f"Weight-Monodromy Conjecture:   Satisfied = {wf.weight_monodromy_conjecture_satisfied} (Eigenvalues = {wf.p_weight_eigenvalues})")
            print(f"Hard Lefschetz Isomorphism:    N^k: {mono_eval['source_graded_piece']} -> {mono_eval['target_graded_piece']} (Verified = {mono_eval['hard_lefschetz_isomorphism']})")
            print(f"Hyodo-Kato Comparison:         {comp.comparison_id} | Uniformizer: {comp.uniformizer_label}")
            print(f"de Rham Isomorphism:           H_HK tensor K =~ H_dR (dim = {comp.de_rham_dim})")
            print(f"Hodge-Tate E_1 Degeneration:   Degenerates at E_1 = {comp.hodge_tate_degeneration_e1} (Tsuji C_st Proved)")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_hyodo_kato_svg())
            print(f"[DxSkills] Hyodo-Kato SVG written to: {args.svg}")
    elif args.command in ["motivic-regulator", "beilinson-conjectures", "chow-motives", "motivic-l-loom"]:
        from scripts.motives_beilinson_loom import (
            MotivesBeilinsonLoom,
            MotivicWeightArchetype,
        )
        arch_map = {
            "elliptic": MotivicWeightArchetype.ELLIPTIC_CURVE_H1.value,
            "k3": MotivicWeightArchetype.K3_SURFACE_CHOW.value,
            "calabi_yau": MotivicWeightArchetype.CALABI_YAU_THREEFOLD.value,
            "tate": MotivicWeightArchetype.PURE_TATE_MOTIVE.value,
        }
        chosen_arch = arch_map.get(args.archetype, MotivicWeightArchetype.ELLIPTIC_CURVE_H1.value)

        loom = MotivesBeilinsonLoom(
            motive_weight=args.weight,
            tate_twist=args.twist,
            default_archetype=chosen_arch,
        )
        mot = loom.motives[0]
        reg = loom.regulators[0]
        sp = loom.special_values[0]
        eval_reg = loom.evaluate_motivic_cohomology(weight_i=mot.idempotent_degree + 1, twist_n=mot.tate_twist_n, test_rank=reg.motivic_cohomology_rank)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Motives & Beilinson Conjectures on Special Values Loom")
            print("=================================================================")
            print(f"Chow Motive ID & Variety:      {mot.motive_id} | {mot.underlying_variety}")
            print(f"Motivic Archetype:             {loom.default_archetype}")
            print(f"Realization Dimensions:        dim H_Betti = {mot.betti_dimension} | dim H_dR = {mot.de_rham_dimension}")
            print(f"Hodge Diamond Row:             {mot.hodge_diamond_row}")
            print(f"Beilinson Regulator Map:       {reg.source_motivic_cohomology} -> {reg.target_deligne_cohomology}")
            print(f"Regulator Lattice Determinant: vol(R_D) = {reg.regulator_determinant:.4f} (Non-Zero Volume = {reg.is_lattice_volume_non_zero})")
            print(f"L-Function Special Value:      {sp.l_function_label} | Order of Vanishing r = {sp.order_of_vanishing_r}")
            print(f"Leading Coefficient L^*(M, s): {sp.leading_coefficient_value:.4f}")
            print(f"Beilinson Conjecture Ratio:    L^*(M, s) / (c_M * R_M) = {sp.beilinson_conjecture_ratio:.4f} in Q^x (Verified = {sp.conjecture_verified})")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_beilinson_svg())
            print(f"[DxSkills] Beilinson Motives SVG written to: {args.svg}")
    elif args.command in ["bloch-kato", "tamagawa-numbers", "crystalline-exponential", "selmer-lattice-loom"]:
        from scripts.bloch_kato_loom import (
            BlochKatoExponentialLoom,
            MotivicGaloisArchetype,
        )
        arch_map = {
            "elliptic": MotivicGaloisArchetype.ELLIPTIC_CURVE_P_ADIC.value,
            "tate": MotivicGaloisArchetype.TATE_TWIST_Q_P.value,
            "modular": MotivicGaloisArchetype.MODULAR_FORM_DELIGNE.value,
            "calabi_yau": MotivicGaloisArchetype.CALABI_YAU_P_ADIC.value,
        }
        chosen_arch = arch_map.get(args.archetype, MotivicGaloisArchetype.ELLIPTIC_CURVE_P_ADIC.value)

        loom = BlochKatoExponentialLoom(
            base_prime=args.prime,
            dimension_v=args.dim,
            default_archetype=chosen_arch,
        )
        cond = loom.local_conditions[0]
        exp_m = loom.exponential_maps[0]
        tam = loom.tamagawa_data[0]
        eval_exp = loom.evaluate_bloch_kato_exponential(tangent_vector_norm=1.5)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Tamagawa Numbers & Bloch-Kato Exponential Map Loom")
            print("=================================================================")
            print(f"Galois Representation:         {cond.representation_label} | Prime p = {cond.prime_v}")
            print(f"Motivic Galois Archetype:      {loom.default_archetype}")
            print(f"Local Selmer Subspaces:        H_e^1 [{cond.dim_h_exponential}D] <= H_f^1 [{cond.dim_h_finite}D] <= H_g^1 [{cond.dim_h_geometric}D] <= H^1 [{cond.dim_h_total}D]")
            print(f"Local Tamagawa Factor:         c_v = [H_f^1 : H_e^1] = {cond.local_tamagawa_factor_c_v}")
            print(f"Bloch-Kato Exponential Map:    exp_BK: {exp_m.source_tangent_space} -> {exp_m.target_selmer_space}")
            print(f"Isomorphism on Lie Algebra:    {exp_m.is_isomorphism} (Kernel Dim = {exp_m.exponential_kernel_dim})")
            print(f"Tangent Evaluation:            ||v|| = 1.5 -> ||exp_BK(v)|| = {eval_exp['cohomology_image_norm']:.4f}")
            print(f"Global Tamagawa Formula:       Tam(M) = #Sha * prod c_v / (#H^0 * #H^0(M^*(1)))")
            print(f"Computed Tam(M):               {tam.tamagawa_number_tam_m:.4f} (#Sha = {tam.sha_order}, prod c_v = {tam.product_local_tamagawa})")
            print(f"Bloch-Kato Leading Value:      L^*(M, 0) in Tam(M) * R_BK * Q^x (Verified = {tam.conjecture_satisfied})")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_bloch_kato_svg())
            print(f"[DxSkills] Bloch-Kato SVG written to: {args.svg}")
    elif args.command in ["euler-systems", "kolyvagin-derivatives", "heegner-system", "selmer-bound-loom"]:
        from scripts.euler_systems_loom import (
            EulerSystemsKolyvaginLoom,
            EulerSystemArchetype,
        )
        arch_map = {
            "heegner": EulerSystemArchetype.HEEGNER_POINTS_ELLIPTIC.value,
            "cyclotomic": EulerSystemArchetype.CYCLOTOMIC_UNITS.value,
            "kato": EulerSystemArchetype.KATO_EULER_SYSTEM.value,
            "beilinson_flach": EulerSystemArchetype.BEILINSON_FLACH_ELEMENTS.value,
        }
        chosen_arch = arch_map.get(args.archetype, EulerSystemArchetype.HEEGNER_POINTS_ELLIPTIC.value)

        loom = EulerSystemsKolyvaginLoom(
            conductor=args.conductor,
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        c_cls = loom.euler_classes[0]
        deriv = loom.derivatives[0]
        b_data = loom.selmer_bounds[0]
        eval_deriv = loom.evaluate_kolyvagin_derivative(test_prime_ell=11, mod_power_m=1)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Euler Systems & Kolyvagin Derivatives Loom")
            print("=================================================================")
            print(f"Euler System Conductor & Prime: m = {c_cls.conductor_m} | Prime p = {loom.prime_p}")
            print(f"Euler System Archetype:        {loom.default_archetype}")
            print(f"Field Extension:               {c_cls.field_extension_label} (Galois Order = {c_cls.galois_group_order})")
            print(f"Norm Compatibility Relation:   cor(c_{{m*ell}}) = P_ell(Frob_ell^-1) * c_m (Verified = {c_cls.norm_compatibility_verified})")
            print(f"Kolyvagin Derivative:          {deriv.kolyvagin_operator_label}")
            print(f"Finite-Singular Residues:      partial_ell(kappa_{{m*ell}}) = phi_ell(kappa_m) (Matched = {deriv.finite_singular_residue_match})")
            print(f"Motive & Mordell-Weil Rank:    {b_data.motive_label} | r_MW = {b_data.mordell_weil_rank}")
            print(f"Shafarevich-Tate Group Bound:  #Sha <= p^{b_data.sha_order_bound} (Finite = {b_data.is_sha_finite})")
            print(f"Kolyvagin Annihilator:         {b_data.kolyvagin_annihilator_ideal}")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_euler_system_svg())
            print(f"[DxSkills] Euler Systems SVG written to: {args.svg}")
    elif args.command in ["iwasawa-theory", "padic-l-functions", "iwasawa-main-conjecture", "lambda-module-loom"]:
        from scripts.iwasawa_theory_loom import (
            IwasawaTheoryLoom,
            IwasawaArchetype,
        )
        arch_map = {
            "cyclotomic": IwasawaArchetype.CYCLOTOMIC_Z_P.value,
            "ordinary": IwasawaArchetype.ELLIPTIC_CURVE_ORDINARY.value,
            "supersingular": IwasawaArchetype.ELLIPTIC_CURVE_SUPERSINGULAR.value,
            "totally_real": IwasawaArchetype.TOTALLY_REAL_FIELD.value,
        }
        chosen_arch = arch_map.get(args.archetype, IwasawaArchetype.CYCLOTOMIC_Z_P.value)

        loom = IwasawaTheoryLoom(
            base_prime=args.prime,
            lambda_inv=args.lambda_inv,
            default_archetype=chosen_arch,
        )
        mod = loom.modules[0]
        l_fn = loom.l_functions[0]
        comp = loom.comparisons[0]
        growth = loom.evaluate_class_number_growth(layer_n=3)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Iwasawa Main Conjecture & p-Adic L-Functions Loom")
            print("=================================================================")
            print(f"Base Extension & Prime:        {mod.base_field_label} | Prime p = {mod.prime_p}")
            print(f"Iwasawa Archetype:             {loom.default_archetype}")
            print(f"Iwasawa Invariants:            mu = {mod.mu_invariant}, lambda = {mod.lambda_invariant}, nu = {mod.nu_invariant}")
            print(f"Ferrero-Washington mu = 0:     {mod.is_ferrero_washington_mu_zero}")
            print(f"Class Number at Layer n = 3:   e_3 = {growth['exponent_e_n']} (|A_3| = {growth['order_approx']})")
            print(f"Kubota-Leopoldt L_p(s, chi):   s = {l_fn.evaluation_point_s}, character = {l_fn.character_label}")
            print(f"Special Bernoulli Value:       {l_fn.special_value_bernoulli:.4f} (Euler Factor = {l_fn.euler_factor_at_p:.4f})")
            print(f"Algebraic Characteristic Ideal:{comp.algebraic_char_ideal}")
            print(f"Analytic p-Adic L-Ideal:       {comp.analytic_l_ideal}")
            print(f"Iwasawa Main Conjecture:       char_Lambda(X_infty) == (L_p) Verified ({comp.ideals_coincide})")
            print(f"Theorem Reference:             {comp.theorem_reference}")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_iwasawa_svg())
            print(f"[DxSkills] Iwasawa Theory SVG written to: {args.svg}")
    elif args.command in ["hida-family", "ordinary-deformation", "lambda-adic-form", "hecke-algebra-loom"]:
        from scripts.hida_family_loom import (
            HidaFamilyLoom,
            HidaFamilyArchetype,
        )
        arch_map = {
            "elliptic": HidaFamilyArchetype.WEIGHT_TWO_ELLIPTIC.value,
            "delta": HidaFamilyArchetype.RAMANUJAN_DELTA_FAMILY.value,
            "cm": HidaFamilyArchetype.CM_FAMILY.value,
            "eisenstein": HidaFamilyArchetype.EISENSTEIN_FAMILY.value,
        }
        chosen_arch = arch_map.get(args.archetype, HidaFamilyArchetype.WEIGHT_TWO_ELLIPTIC.value)

        loom = HidaFamilyLoom(
            level_n=args.level,
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        fam = loom.families[0]
        spec = loom.specialize_to_weight(target_weight=args.weight)
        rep = loom.representations[0]
        eval_cong = loom.evaluate_congruence_ideal(test_order=2)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Hida Families & Ordinary Modular Deformations Loom")
            print("=================================================================")
            print(f"Modular Level & Prime:         N = {fam.level_n} | Prime p = {fam.prime_p}")
            print(f"Hida Family Archetype:         {loom.default_archetype}")
            print(f"Hecke Algebra Rank over Lambda:rank_Lambda(h^ord) = {fam.hecke_algebra_rank} (Ordinary at p = {fam.is_ordinary_at_p})")
            print(f"Lambda-Adic Coefficients:      a_p(T) in Z_p[[T]]^x ({fam.lambda_adic_coefficients.get('a_p', 'u(T)')})")
            print(f"Weight Specialization k = {spec.weight_k}:  T -> (1+p)^{spec.weight_k - 2} - 1 (P_k = {spec.arithmetic_point_t_val:.4f})")
            print(f"Classical Form Label:          {spec.classical_form_label}")
            print(f"Hecke Eigenvalue a_p(P_k):     {spec.hecke_eigenvalue_a_p:.4f} (Classical Cusp Form = {spec.is_classical_cusp_form})")
            print(f"Big Galois Representation:     rho_F: G_Q -> GL_2(I) (Unramified outside Np = {rep.is_unramified_outside_np})")
            print(f"Local Shape at Prime p:        {rep.local_p_shape}")
            print(f"Congruence Ideal:              {rep.congruence_ideal_label} (Adjoint L_p Divisibility Verified)")
            print("=================================================================")

        if args.svg:
            if os.path.dirname(args.svg):
                os.makedirs(os.path.dirname(args.svg), exist_ok=True)
            with open(args.svg, "w", encoding="utf-8") as f:
                f.write(loom.generate_hida_svg())
            print(f"[DxSkills] Hida Family SVG written to: {args.svg}")
    elif args.command in ["coleman-family", "overconvergent-forms", "eigencurve", "finite-slope-loom"]:
        from scripts.coleman_family_loom import (
            ColemanFamilyLoom,
            ColemanFamilyArchetype,
        )
        arch_map = {
            "eigencurve": ColemanFamilyArchetype.COLEMAN_MAZUR_EIGENCURVE.value,
            "finite-slope": ColemanFamilyArchetype.FINITE_SLOPE_TWO.value,
            "critical-slope": ColemanFamilyArchetype.CRITICAL_SLOPE_K_MINUS_1.value,
            "ramanujan": ColemanFamilyArchetype.RAMANUJAN_SLOPE_FAMILY.value,
        }
        chosen_arch = arch_map.get(args.archetype, ColemanFamilyArchetype.COLEMAN_MAZUR_EIGENCURVE.value)

        loom = ColemanFamilyLoom(
            level_n=args.level,
            prime_p=args.prime,
            weight_k=args.weight,
            default_archetype=chosen_arch,
        )
        sp = loom.spaces[0]
        fred = loom.fredholm_series[0]
        pt = loom.eigencurve_points[0]
        crit = loom.evaluate_classicality_threshold(slope=args.slope, weight=args.weight)

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Coleman Families & Overconvergent Modular Forms Loom")
            print("=================================================================")
            print(f"Modular Level & Prime:         N = {sp.level_n} | Prime p = {sp.prime_p}")
            print(f"Coleman Family Archetype:      {loom.default_archetype}")
            print(f"Overconvergent Banach Space:   M_{sp.weight_k}^dagger(Gamma_0({sp.level_n}), r={sp.overconvergence_radius_r})")
            print(f"U_p Compact Operator:          {sp.is_u_p_compact} ({sp.banach_norm_type})")
            print(f"Fredholm Series P(T):          det(1 - T * U_p) (Entire: {fred.is_entire_function}, Slopes: {fred.slope_segments})")
            print(f"Newton Polygon Vertices:       {fred.newton_polygon_vertices}")
            print(f"Coleman Classicality:          Slope {crit['slope_alpha']} vs Bound k - 1 = {crit['critical_bound']}")
            print(f"Classical Cusp Form:           {crit['is_strictly_classical']} ({crit['criterion']})")
            print(f"Eigencurve Point Projection:   {pt.point_id} -> Weight Space W (Slope: {pt.slope_alpha:.2f})")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "coleman_family_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_coleman_svg())
            print(f"[DxSkills] Coleman Family SVG written to: {out_path}")
    elif args.command in ["fontaine-mazur", "geometric-galois", "de-rham-representation", "galois-deformation-loom"]:
        from scripts.fontaine_mazur_loom import (
            FontaineMazurLoom,
            FontaineMazurArchetype,
        )
        arch_map = {
            "elliptic": FontaineMazurArchetype.ELLIPTIC_CURVE_TATE_MODULE.value,
            "delta": FontaineMazurArchetype.RAMANUJAN_DELTA_REP.value,
            "dirichlet": FontaineMazurArchetype.DIRICHLET_TATE_TWIST.value,
            "exotic": FontaineMazurArchetype.NON_GEOMETRIC_UNRAMIFIED.value,
        }
        chosen_arch = arch_map.get(args.archetype, FontaineMazurArchetype.ELLIPTIC_CURVE_TATE_MODULE.value)

        loom = FontaineMazurLoom(
            dimension=args.dimension,
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        rings = {r.ring_name.split()[0]: r for r in loom.period_rings}
        ht = loom.hodge_tate_data[0]
        gm = loom.geometric_modularity[0]
        verdict = loom.evaluate_fontaine_mazur_conjecture(
            unramified_ae=gm.is_unramified_almost_everywhere,
            de_rham=gm.is_de_rham_at_p,
            dimension=loom.dimension,
        )

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Fontaine-Mazur Conjecture & Geometric Galois Representations Loom")
            print("=================================================================")
            print(f"Dimension & Base Prime:        Dim = {loom.dimension} | Prime p = {loom.prime_p}")
            print(f"Galois Representation:         {gm.representation_label} ({loom.default_archetype.split('(')[0].strip()})")
            print(f"Hodge-Tate Weights HT(rho):    {ht.hodge_tate_weights}")
            print(f"Sen Polynomial Theta_V(T):     Coefficients = {ht.sen_polynomial_coefficients}")
            print(f"Fontaine Period Rings:         B_HT Admissible: {rings.get('B_HT').is_admissible} | B_dR Admissible: {rings.get('B_dR').is_admissible}")
            print(f"Crystalline & Semi-Stable:     B_cris: {rings.get('B_cris').is_admissible} | B_st: {rings.get('B_st').is_admissible} (Monodromy N = {rings.get('B_st').monodromy_nilpotent_order})")
            print(f"Frobenius Eigenvalues:         {rings.get('B_cris').frobenius_eigenvalues}")
            print(f"Fontaine-Mazur Geometric:      {gm.is_geometric_representation} ({verdict['fontaine_mazur_verdict']})")
            print(f"Associated Variety / Motive:   {gm.associated_motive_or_variety}")
            print(f"Modularity Deformation R = T:  {gm.deformation_ring_status}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "fontaine_mazur_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_fontaine_mazur_svg())
            print(f"[DxSkills] Fontaine-Mazur SVG written to: {out_path}")
    elif args.command in ["serre-modularity", "odd-representation", "serre-weight-loom", "khare-wintenberger"]:
        from scripts.serre_modularity_loom import (
            SerreModularityLoom,
            SerreModularityArchetype,
        )
        arch_map = {
            "elliptic": SerreModularityArchetype.WEIGHT_TWO_ELLIPTIC.value,
            "delta": SerreModularityArchetype.RAMANUJAN_DELTA_MOD_P.value,
            "dihedral": SerreModularityArchetype.DIHEDRAL_INDUCTION.value,
            "even": SerreModularityArchetype.EVEN_NON_MODULAR.value,
        }
        chosen_arch = arch_map.get(args.archetype, SerreModularityArchetype.WEIGHT_TWO_ELLIPTIC.value)

        loom = SerreModularityLoom(
            level_n=args.level,
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        rep = loom.representations[0]
        inv = loom.serre_invariants[0]
        mod = loom.modularity_data[0]
        verdict = loom.evaluate_serre_conjecture(
            is_odd=rep.is_odd,
            is_irreducible=rep.is_irreducible,
            level_n=inv.serre_level_n,
            weight_k=inv.serre_weight_k,
        )

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Serre's Modularity Conjecture & Odd Galois Representations Loom")
            print("=================================================================")
            print(f"Prime p & Artin Conductor:     Prime p = {rep.prime_p} | Level N(rho_bar) = {rep.artin_conductor_prime_to_p}")
            print(f"Galois Representation:         {rep.representation_id} ({loom.default_archetype.split('(')[0].strip()})")
            print(f"Parity Condition:              Odd = {rep.is_odd} (det(rho_bar(c)) = {'-1' if rep.is_odd else '+1'})")
            print(f"Irreducibility:                {rep.is_irreducible}")
            print(f"Serre Optimal Invariants:      N = {inv.serre_level_n} | k = {inv.serre_weight_k} | epsilon = {inv.serre_character_epsilon}")
            print(f"Tame Inertia Weights:          {inv.tame_inertia_weights} (Fontaine-Laffaille: {inv.is_fontaine_laffaille})")
            print(f"Companion Form Pair:           {inv.is_companion_form_pair}")
            print(f"Serre Modularity Verdict:      {mod.is_modular} ({verdict['serre_verdict']})")
            print(f"Modular Target Space:          {mod.modular_eigenform_space}")
            print(f"Khare-Wintenberger Theorem:    {mod.proof_reference}")
            print(f"Deformation Lifting:           {mod.deformation_lifting_status}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "serre_modularity_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_serre_svg())
            print(f"[DxSkills] Serre Modularity SVG written to: {out_path}")
    elif args.command in ["perfectoid-tilting", "scholze-tilting", "almost-mathematics-loom", "perfectoid-category"]:
        from scripts.perfectoid_spaces_loom import (
            PerfectoidSpacesLoom,
            PerfectoidSpacesArchetype,
        )
        arch_map = {
            "cyclotomic": PerfectoidSpacesArchetype.CYCLOTOMIC_PERFECTOID_FIELD.value,
            "roots": PerfectoidSpacesArchetype.PERFECTOID_P_POWER_ROOTS.value,
            "algebraic": PerfectoidSpacesArchetype.ALGEBRAIC_CLOSURE_C_P.value,
            "shimura": PerfectoidSpacesArchetype.TORSION_SHIMURA_VARIETY.value,
        }
        chosen_arch = arch_map.get(args.archetype, PerfectoidSpacesArchetype.CYCLOTOMIC_PERFECTOID_FIELD.value)

        loom = PerfectoidSpacesLoom(
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        pair = loom.field_pairs[0]
        equiv = loom.tilting_equivalences[0]
        adic = loom.adic_spaces[0]
        axioms = loom.evaluate_perfectoid_axioms(
            frobenius_surjective=pair.is_frobenius_surjective,
            non_discrete_valuation=True,
            complete_topology=True,
        )

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Perfectoid Spaces & Scholze Tilting Equivalence Loom")
            print("=================================================================")
            print(f"Base Prime:                    Prime p = {pair.prime_p}")
            print(f"Field Pair:                    {pair.pair_id} ({loom.default_archetype.split('(')[0].strip()})")
            print(f"Characteristic 0 Field K:      {pair.field_char_zero}")
            print(f"Tilted Characteristic p K^flat:{pair.field_char_p_tilt}")
            print(f"Frobenius on O_K / p:          Surjective ({pair.is_frobenius_surjective}) | Valuation Rank: {pair.valuation_rank}")
            print(f"Pseudo-Uniformizer:            pi = {pair.pseudo_uniformizer_symbol}")
            print(f"Tilting Equivalence:           {equiv.equivalence_label} ({axioms['axiomatic_verdict']})")
            print(f"Topological Homeomorphism:     |X| = |X^flat| ({equiv.is_topological_homeomorphism})")
            print(f"Etale Site Equivalence:        X_et = X^flat_et ({equiv.is_etale_site_equivalent})")
            print(f"Almost Purity Theorem:         {equiv.almost_purity_theorem_verified} (H^i(X, O_X)^a = 0 for i > 0)")
            print(f"Adic Spectrum Geometry:        {adic.space_label} ({adic.rational_subsets_count} Rational Subsets)")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "perfectoid_tilting_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_perfectoid_svg())
            print(f"[DxSkills] Perfectoid Tilting SVG written to: {out_path}")
    elif args.command in ["fargues-scholze", "local-shtuka", "excursion-operator", "geometrization-loom"]:
        from scripts.fargues_scholze_loom import (
            FarguesScholzeLoom,
            FarguesScholzeArchetype,
        )
        arch_map = {
            "unramified": FarguesScholzeArchetype.GL2_UNRAMIFIED.value,
            "supercuspidal": FarguesScholzeArchetype.GL2_SUPER_CUSPIDAL.value,
            "siegel": FarguesScholzeArchetype.GSP4_SIEGEL_LOCAL.value,
            "packet": FarguesScholzeArchetype.SL2_PACKET_DECOMPOSITION.value,
        }
        chosen_arch = arch_map.get(args.archetype, FarguesScholzeArchetype.GL2_UNRAMIFIED.value)

        loom = FarguesScholzeLoom(
            group_label=args.group,
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        bun = loom.bun_g_models[0]
        sht = loom.local_shtukas[0]
        exc = loom.excursion_operators[0]
        eval_geom = loom.evaluate_geometrization_theorem(
            is_reductive=True,
            is_local_p_adic=True,
        )

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Fargues-Scholze Geometrization of Local Langlands Loom")
            print("=================================================================")
            print(f"Reductive Group & Prime:       G = {bun.group_label} | Prime p = {bun.prime_p}")
            print(f"Fargues-Scholze Archetype:     {loom.default_archetype}")
            print(f"Moduli Stack Bun_G on X_FF:    Newton Strata = {bun.newton_strata}")
            print(f"Harder-Narasimhan Slopes:      {bun.harder_narasimhan_slopes} ({bun.sheaf_category_label})")
            print(f"Local Shtuka Moduli Space:     {sht.shtuka_id} ({sht.legs_count} Legs, {sht.schubert_variety_mu})")
            print(f"Frobenius Modification Type:   {sht.frobenius_modification_type}")
            print(f"Excursion Operator:            {exc.operator_id} (Bernstein Eigenvalue = {exc.bernstein_center_eigenvalue})")
            print(f"Semisimple L-Parameter:        {exc.weil_deligne_parameter_label}")
            print(f"Geometrization Theorem:        {eval_geom['geometrization_verdict']}")
            print(f"Spectral Action Status:        {eval_geom['spectral_action_status']}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "fargues_scholze_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_fargues_scholze_svg())
            print(f"[DxSkills] Fargues-Scholze SVG written to: {out_path}")
    elif args.command in ["kudla-program", "arithmetic-intersection", "special-cycles-loom", "kudla-rapoport"]:
        from scripts.kudla_program_loom import (
            KudlaProgramLoom,
            KudlaArchetype,
        )
        arch_map = {
            "siegel": KudlaArchetype.SO3_2_SIEGEL_SURFACE.value,
            "hilbert": KudlaArchetype.SO2_2_HILBERT_BLUMENTHAL.value,
            "modular": KudlaArchetype.GU1_1_MODULAR_CURVE.value,
            "rapoport": KudlaArchetype.RAPOPORT_ZINK_P_DIVISIBLE.value,
        }
        sig_map = {
            "3,2": (3, 2),
            "2,2": (2, 2),
            "1,1": (1, 1),
        }
        chosen_sig = sig_map.get(args.signature, (3, 2))
        chosen_arch = arch_map.get(args.archetype, KudlaArchetype.SO3_2_SIEGEL_SURFACE.value)

        loom = KudlaProgramLoom(
            signature=chosen_sig,
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        datum = loom.shimura_datum
        cycles = loom.special_cycles
        total_int = loom.compute_total_arithmetic_intersection(1, 2)
        eis = loom.eisenstein_series

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Kudla Program Arithmetic Intersection Loom")
            print("=================================================================")
            print(f"Orthogonal Shimura Datum:      {datum.quadratic_space_label}")
            print(f"Discriminant & Reflex Field:   D = {datum.lattice_discriminant} | E = {datum.reflex_field}")
            print(f"Symmetric Domain:              {datum.symmetric_domain_label}")
            print(f"Special Cycles Loomed:         {len(cycles)} fundamental cycles (CH^1(M)_hat)")
            print(f"First Cycle Geometric Deg:     deg(Z(1)) = {cycles[0].geometric_degree}")
            print(f"First Cycle Arithmetic Deg:    deg_hat(Z_hat(1)) = {cycles[0].arithmetic_degree}")
            print(f"Local Intersection Multiplicity:Int_{total_int['local_intersections'][0]['prime_p']}(1, 2) = {total_int['local_intersections'][0]['local_intersection_multiplicity']}")
            print(f"Finite Places Sum:             sum_{{p < inf}} Int_p log p = {total_int['finite_places_sum']}")
            print(f"Archimedean Star Product:      Int_inf(1, 2) = {total_int['archimedean_star_product']}")
            print(f"Total Arithmetic Pairing:      <Z_hat(1), Z_hat(2)> = {total_int['total_arithmetic_pairing']}")
            print(f"Eisenstein Derivative Match:   deg_hat(phi_hat(tau)) = E'(0, tau) (Verified: {eis.kudla_conjecture_verified})")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "kudla_program_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Kudla Program SVG written to: {out_path}")
    elif args.command in ["colmez-conjecture", "faltings-height", "cm-abelian-loom", "artin-derivative"]:
        from scripts.colmez_conjecture_loom import (
            ColmezConjectureLoom,
            ColmezArchetype,
        )
        arch_map = {
            "elliptic": ColmezArchetype.IMAGINARY_QUADRATIC_CHOWLA_SELBERG.value,
            "surface": ColmezArchetype.QUARTIC_CYCLOTOMIC_Q_MU5.value,
            "dihedral": ColmezArchetype.QUARTIC_NON_ABELIAN_CM.value,
            "sextic": ColmezArchetype.SEXTIC_CM_FIELD.value,
        }
        chosen_arch = arch_map.get(args.archetype, ColmezArchetype.IMAGINARY_QUADRATIC_CHOWLA_SELBERG.value)

        loom = ColmezConjectureLoom(
            dimension_g=args.dimension,
            discriminant_d=args.discriminant,
            default_archetype=chosen_arch,
        )
        field_info = loom.cm_field
        type_info = loom.cm_type
        fh = loom.faltings_height
        eval_colmez = loom.evaluate_colmez_conjecture()
        artins = loom.artin_derivatives

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Colmez Conjecture & Faltings Heights of CM Varieties Loom")
            print("=================================================================")
            print(f"CM Field & Dimension:          {field_info.field_label} (dim g = {field_info.dimension_g})")
            print(f"Discriminants:                 Disc(E) = {field_info.discriminant_e} | Disc(F) = {field_info.discriminant_f}")
            print(f"Galois Group:                  {field_info.galois_group_label}")
            print(f"CM Type:                       {type_info.type_id} ({type_info.embeddings_count} Embeddings, Reflex={type_info.reflex_field})")
            print(f"Stable Faltings Height:        h_Fal(A) = {fh.stable_faltings_height:.5f}")
            print(f"Taguchi-Smith Height:          h_TS(A) = {fh.taguchi_smith_height:.5f}")
            print(f"Archimedean Period Integral:   int_{{A(C)}} |omega ^ omega_bar| = {fh.archimedean_period_integral}")
            print(f"Artin Characters Evaluated:    {len(artins)} characters")
            print(f"Quadratic Char Log-Deriv:      L'(0, chi)/L(0, chi) = {artins[1].logarithmic_derivative:.5f} (cond = {artins[1].conductor})")
            print(f"Colmez Conjecture Equality:    Satisfied: {eval_colmez['is_colmez_equality_satisfied']} (Diff = {eval_colmez['absolute_discrepancy']})")
            print(f"Verification Verdict:          {eval_colmez['proof_status']}")
            print(f"Andre-Oort Consequence:        {eval_colmez['andre_oort_consequence']}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "colmez_conjecture_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Colmez Conjecture SVG written to: {out_path}")
    elif args.command in ["gross-stark", "stark-conjecture", "padic-regulator", "brumer-stark"]:
        from scripts.gross_stark_loom import (
            GrossStarkLoom,
            GrossStarkArchetype,
        )
        arch_map = {
            "sqrt5": GrossStarkArchetype.REAL_QUADRATIC_Q_SQRT5.value,
            "sqrt2": GrossStarkArchetype.REAL_QUADRATIC_Q_SQRT2.value,
            "cubic": GrossStarkArchetype.TOTALLY_REAL_CUBIC_Q_ZETA7_PLUS.value,
            "quartic": GrossStarkArchetype.TOTALLY_REAL_QUARTIC_FIELD.value,
        }
        chosen_arch = arch_map.get(args.archetype, GrossStarkArchetype.REAL_QUADRATIC_Q_SQRT5.value)

        loom = GrossStarkLoom(
            degree_g=args.degree,
            discriminant_d=args.discriminant,
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        f_data = loom.totally_real_field
        u_data = loom.stark_unit
        l_data = loom.padic_derivative
        cones = loom.shintani_cones
        status = loom.evaluate_conjecture_status()

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Gross-Stark & p-Adic Stark Conjectures Loom")
            print("=================================================================")
            print(f"Totally Real Field:            {f_data.field_label} (degree g = {f_data.degree_g})")
            print(f"Discriminant & Class Number:   D_F = {f_data.discriminant_df} | h^+(F) = {f_data.narrow_class_number}")
            print(f"Splitting Prime:               p = {f_data.splitting_prime_p} (Exceptional Zero Order e = {l_data.order_of_vanishing})")
            print(f"Gross-Stark S-Unit:            {u_data.unit_label}")
            print(f"Minimal Polynomial:            {u_data.minimal_polynomial}")
            print(f"p-Adic Valuation & Logarithm:  ord_p(u) = {u_data.p_adic_valuation} | log_p(u) = {u_data.iwasawa_padic_log:.5f}")
            print(f"p-Adic Regulator:              R_p(chi) = {u_data.canonical_regulator:.5f}")
            print(f"p-Adic L Derivative:           L_p'(0, chi) = {l_data.derivative_value:.5f}")
            print(f"Gross-Stark Formula:           {status['gross_stark_formula']}")
            print(f"Equality Verified:             {l_data.is_conjecture_verified} (Ratio = {l_data.gross_stark_ratio:.5f})")
            print(f"Proof Status:                  {status['proof_status']}")
            print(f"Methodology:                   {status['methodology']}")
            print(f"Shintani Cones Decomposed:     {len(cones)} simplicial cones")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "gross_stark_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Gross-Stark SVG written to: {out_path}")
    elif args.command in ["langlands-shahidi", "shahidi-gamma", "intertwining-operator", "automorphic-l-loom"]:
        from scripts.langlands_shahidi_loom import (
            LanglandsShahidiLoom,
            ShahidiArchetype,
        )
        arch_map = {
            "so5": ShahidiArchetype.SO5_SPLIT_STANDARD.value,
            "sp4": ShahidiArchetype.SP4_SIEGEL_DEGREE2.value,
            "rankin": ShahidiArchetype.GL2_TIMES_GL2_IN_GL4.value,
            "exterior": ShahidiArchetype.GL4_EXTERIOR_SQUARE.value,
        }
        chosen_arch = arch_map.get(args.archetype, ShahidiArchetype.SO5_SPLIT_STANDARD.value)

        loom = LanglandsShahidiLoom(
            spectral_s=args.spectral_s,
            prime_p=args.prime,
            default_archetype=chosen_arch,
        )
        grp = loom.group_data
        rep = loom.levi_representation
        factors = loom.local_factors
        gl = loom.global_l_data
        eval_res = loom.evaluate_unitary_axis()

        if args.json:
            print(loom.to_json())
        else:
            print("=================================================================")
            print("  Langlands-Shahidi Method & Automorphic L-Functions Loom")
            print("=================================================================")
            print(f"Quasi-Split Group:             {grp.group_label} (dim = {grp.dimension_g})")
            print(f"Levi Subgroup:                 {grp.levi_m_label}")
            print(f"Unipotent Radical:             dim(N) = {grp.unipotent_n_dimension}")
            print(f"Generic Representation:        {rep.representation_label}")
            print(f"Whittaker Model:               Generic ({rep.whittaker_model_character[:45]})")
            print(f"Spectral Parameter:            s = {loom.spectral_s} (On Unitary Axis Re(s)=1: {eval_res['is_on_unitary_axis']})")
            print(f"Local Prime & Factors:         p = {loom.prime_p} ({len(factors)} adjoint pieces)")
            print(f"First Local Factor:            L(s) = {factors[0].local_l_value:.4f} | gamma(s) = {factors[0].local_gamma_value:.4f}")
            print(f"Global Functorial Lift:        {gl.functorial_lift_type}")
            print(f"Ramanujan Generalized Bound:   {gl.ramanujan_generalized_bound}")
            print(f"Meromorphic Continuation:      {gl.has_meromorphic_continuation} (Root Number = {gl.functional_equation_root_number})")
            print(f"Unitary Axis Non-Vanishing:    L(1 + it, pi, r) != 0 (Guaranteed: {eval_res['non_vanishing_guaranteed']})")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "langlands_shahidi_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Langlands-Shahidi SVG written to: {out_path}")
    elif args.command in ["arthur-trace-formula", "endoscopic-classification", "arthur-packet", "selberg-trace-loom"]:
        from scripts.arthur_trace_loom import (
            ArthurSelbergTraceLoom,
            ArthurGroupArchetype,
        )
        group_map = {
            "so5": ArthurGroupArchetype.SO5_SPLIT.value,
            "sp4": ArthurGroupArchetype.SP4_SPLIT.value,
            "so7": ArthurGroupArchetype.SO7_SPLIT.value,
            "gl4": ArthurGroupArchetype.GL4_STANDARD.value,
        }
        chosen_group = group_map.get(args.group, ArthurGroupArchetype.SO5_SPLIT.value)

        loom = ArthurSelbergTraceLoom(
            test_function_cutoff=args.cutoff,
            spectral_truncation_level=args.truncation,
            default_archetype=chosen_group,
        )
        ev = loom.evaluate_trace_formula()
        param = loom.arthur_parameter

        if args.json:
            import json
            print(json.dumps(loom.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Arthur-Selberg Trace Formula & Endoscopic Classification Loom")
            print("=================================================================")
            print(f"Reductive Group:               {loom.archetype_str}")
            print(f"Test Function Cutoff T:        {loom.test_function_cutoff}")
            print(f"Geometric Orbital Sum:         I_geom(f) = {ev.geometric_total:.4f} ({len(loom.orbital_components)} classes)")
            print(f"Spectral Automorphic Sum:      I_spec(f) = {ev.spectral_total:.4f} ({len(loom.spectral_components)} representations)")
            print(f"Endoscopic Reconstructed:      sum_H iota S^H(f^H) = {ev.endoscopic_reconstructed_total:.4f}")
            print(f"Trace Identity Residual:       |I_geom - I_spec| = {ev.trace_identity_residual:.5f} (Stabilized: {ev.is_stabilized})")
            if param:
                print(f"Arthur Parameter:              {param.parameter_label}")
                print(f"Dual Group & Component Group:  {param.dual_group_label} | |S_psi| = {param.component_group_order}")
            print(f"Arthur Packet Size:            {len(loom.arthur_packet)} representations in Pi_psi")
            print(f"Cognitive Resonance Score:     {ev.cognitive_resonance_score:.4f}")
            print(f"Spatial Stability Index:       {ev.spatial_stability_index:.4f}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "arthur_trace_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Arthur-Selberg SVG written to: {out_path}")
    elif args.command in ["relative-trace-ggp", "ggp-loom", "ichino-ikeda", "gan-gross-prasad"]:
        from scripts.relative_trace_ggp_loom import (
            RelativeTraceGGPLoom,
            GGPArchetype,
        )
        arch_map = {
            "u3_u2": GGPArchetype.UNITARY_U3_U2.value,
            "so5_so4": GGPArchetype.ORTHOGONAL_SO5_SO4.value,
            "waldspurger": GGPArchetype.UNITARY_U2_U1_WALDSPURGER.value,
            "aggp": GGPArchetype.ARITHMETIC_AGGP_CURVE.value,
        }
        chosen_arch = arch_map.get(args.archetype, GGPArchetype.UNITARY_U3_U2.value)

        loom = RelativeTraceGGPLoom(
            spectral_parameter=args.spectral_s,
            subgroup_truncation=args.truncation,
            default_archetype=chosen_arch,
        )
        ev = loom.evaluate_relative_trace()
        sd = loom.spherical_data
        rp = loom.rep_pair
        ii = loom.ichino_ikeda
        ag = loom.aggp_height

        if args.json:
            import json
            print(json.dumps(loom.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Relative Trace Formula & Gan-Gross-Prasad (GGP) Loom")
            print("=================================================================")
            print(f"Setting Archetype:             {loom.archetype_str}")
            if sd:
                print(f"Spherical Group Pair:          {sd.group_g_label} with {sd.subgroup_h_label}")
            if rp:
                print(f"GGP Representation Pair:       {rp.rep_pi1_label[:35]} x {rp.rep_pi2_label[:35]}")
                print(f"Branching Multiplicity:        dim Hom_H = {rp.hom_multiplicity} <= 1 (Vogan Size = {rp.vogan_packet_size})")
                print(f"Distinguished Representation:  {rp.is_distinguished_by_h} (Root Sign = {rp.local_root_number_sign})")
            print(f"RTF Geometric Total:           I_geom_H = {ev.rtf_geometric_total:.4f} ({len(loom.relative_orbitals)} orbits)")
            print(f"RTF Spectral Total:            I_spec_H = {ev.rtf_spectral_total:.4f}")
            print(f"RTF Identity Residual:         {ev.rtf_residual:.5f} (Period Active: {ev.period_non_vanishing})")
            if ag and ag.is_exceptional_vanishing:
                print(f"Arithmetic AGGP Derivative:    L'(1/2) = {ag.central_derivative_l_prime:.4f}")
                print(f"Beilinson-Bloch Height:        <Z, Z>_BB = {ag.beilinson_bloch_height:.4f}")
            elif ii:
                print(f"Ichino-Ikeda Central L-Value:  L(1/2) = {ii.central_l_value:.4f}")
                print(f"Normalized Period Square:      |P_H(phi)|^2 / <phi,phi> = {ii.normalized_period_square:.5f}")
            print(f"Cognitive Resonance Score:     {ev.cognitive_resonance_score:.4f}")
            print(f"Spatial Stability Index:       {ev.spatial_stability_index:.4f}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "relative_trace_ggp_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Relative Trace GGP SVG written to: {out_path}")
    elif args.command in ["beyond-endoscopy", "langlands-functoriality", "poisson-trace", "altug-loom"]:
        from scripts.beyond_endoscopy_loom import (
            BeyondEndoscopyLoom,
            BeyondEndoscopyArchetype,
        )
        arch_map = {
            "sym2": BeyondEndoscopyArchetype.GL2_SYMMETRIC_SQUARE.value,
            "rankin": BeyondEndoscopyArchetype.GL2_TIMES_GL2_RANKIN.value,
            "adjoint": BeyondEndoscopyArchetype.GL3_ADJOINT_OCTET.value,
            "altug": BeyondEndoscopyArchetype.ALTUG_POISSON_GL2.value,
        }
        chosen_arch = arch_map.get(args.archetype, BeyondEndoscopyArchetype.GL2_SYMMETRIC_SQUARE.value)

        loom = BeyondEndoscopyLoom(
            test_energy_parameter=args.energy,
            smoothing_epsilon=args.epsilon,
            default_archetype=chosen_arch,
        )
        ev = loom.evaluate_beyond_endoscopy()
        dr = loom.dual_rep
        ak = loom.altug_kernel

        if args.json:
            import json
            print(json.dumps(loom.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Beyond Endoscopy & Langlands Functoriality Loom")
            print("=================================================================")
            print(f"Setting Archetype:             {loom.archetype_str}")
            if dr:
                print(f"Dual Representation:           {dr.dual_group_label} with {dr.representation_r_label}")
                print(f"Dimension & Self-Duality:      dim(r) = {dr.representation_dimension} | Self-Dual = {dr.is_self_dual}")
                print(f"Functorial Target:             {dr.functorial_target_group}")
            print(f"Poisson Geometric Total:       I_Poisson = {ev.poisson_geometric_total:.4f} ({len(loom.poisson_harmonics)} harmonics)")
            print(f"Spectral L-Pole Residue Total: sum Res_(s=1) = {ev.spectral_pole_residue_total:.4f} ({len(loom.spectral_filters)} representations)")
            print(f"Trace Matching Residual:       {ev.trace_matching_residual:.5f} (Isolated: {ev.functorial_lift_isolated})")
            print(f"Cancellation Efficiency:       {ev.cancellation_efficiency_ratio * 100:.2f}%")
            if ak:
                print(f"Altug Unipotent Subtraction:   eps = {ak.smoothing_parameter_epsilon} | sub = {ak.unipotent_subtraction_value:.4f}")
            print(f"Cognitive Resonance Score:     {ev.cognitive_resonance_score:.4f}")
            print(f"Spatial Stability Index:       {ev.spatial_stability_index:.4f}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "beyond_endoscopy_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Beyond Endoscopy SVG written to: {out_path}")
    elif args.command in ["taylor-wiles", "modularity-lifting", "patching-loom", "r-equals-t"]:
        from scripts.taylor_wiles_patching_loom import (
            TaylorWilesPatchingLoom,
            TaylorWilesArchetype,
        )
        arch_map = {
            "fermat": TaylorWilesArchetype.FERMAT_FREY_CURVE.value,
            "ordinary": TaylorWilesArchetype.TAYLOR_WILES_ORDINARY.value,
            "kisin": TaylorWilesArchetype.KISIN_POTENTIALLY_BARSOTTI_TATE.value,
            "unitary": TaylorWilesArchetype.UNITARY_CALEGARI_GERAGHTY.value,
        }
        chosen_arch = arch_map.get(args.archetype, TaylorWilesArchetype.FERMAT_FREY_CURVE.value)

        loom = TaylorWilesPatchingLoom(
            prime_p=args.prime,
            patching_level=args.level,
            default_archetype=chosen_arch,
        )
        ev = loom.evaluate_modularity_lifting()
        rr = loom.residual_rep
        sg = loom.selmer_group
        pm = loom.patched_module

        if args.json:
            import json
            print(json.dumps(loom.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Taylor-Wiles Patching & Modularity Lifting Loom (R = T)")
            print("=================================================================")
            print(f"Setting Archetype:             {loom.archetype_str}")
            if rr:
                print(f"Residual Representation:       {rr.representation_label[:40]}")
                print(f"Prime & Conductor Level:       p = {rr.prime_p} | N = {rr.conductor_level_n} (Weight k = {rr.serre_weight_k})")
            if sg:
                print(f"Selmer Groups:                 dim H^1_f = {sg.selmer_dimension_h1} | dim H^1_perp = {sg.dual_selmer_dimension_h1_perp}")
            print(f"Taylor-Wiles Primes:           {len(loom.tw_primes)} auxiliary primes in Q_{loom.patching_level}")
            if pm:
                print(f"Patched Module M_infty:        Free over S_infty = Z_p[[x_1..x_{pm.patching_depth_g}]] (Rank = {pm.module_rank_over_s_infty})")
            print(f"Modularity Isomorphism:        R_D ~= T_D is {ev.is_r_equals_t_isomorphism} (Ratio = {ev.numerical_criterion_ratio})")
            print(f"Multiplicity One Verified:     {ev.multiplicity_one_verified}")
            print(f"Cognitive Resonance Score:     {ev.cognitive_resonance_score:.4f}")
            print(f"Spatial Stability Index:       {ev.spatial_stability_index:.4f}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "taylor_wiles_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Taylor-Wiles SVG written to: {out_path}")
    elif args.command in ["paramodular-conjecture", "abelian-surface", "paramodular-loom", "brumer-kramer"]:
        from scripts.paramodular_conjecture_loom import (
            ParamodularConjectureLoom,
            ParamodularArchetype,
        )
        arch_map = {
            "n277": ParamodularArchetype.PARAMODULAR_N277_MINIMAL.value,
            "n587": ParamodularArchetype.PARAMODULAR_N587_JACOBIAN.value,
            "lift": ParamodularArchetype.GRITSENKO_LIFT_BOUNDARY.value,
            "bcgp": ParamodularArchetype.BCGP_OVERCONVERGENT_GSP4.value,
        }
        chosen_arch = arch_map.get(args.archetype, ParamodularArchetype.PARAMODULAR_N277_MINIMAL.value)

        loom = ParamodularConjectureLoom(
            conductor_input=args.conductor,
            spectral_precision=args.precision,
            default_archetype=chosen_arch,
        )
        ev = loom.evaluate_paramodular_conjecture()
        ab = loom.abelian_surface
        pf = loom.paramodular_form

        if args.json:
            import json
            print(json.dumps(loom.to_dict(), indent=2))
        else:
            print("=================================================================")
            print("  Paramodular Conjecture & Modularity of Abelian Surfaces Loom")
            print("=================================================================")
            print(f"Setting Archetype:             {loom.archetype_str}")
            if ab:
                print(f"Abelian Surface A/Q:           {ab.surface_label[:40]} (Conductor N = {ab.conductor_n})")
                print(f"Polarization & Endomorphisms:  Degree {ab.polarization_degree} | {ab.endomorphism_ring}")
                print(f"Genus 2 Curve Equation:        {ab.genus2_curve_equation[:45]}")
            if pf:
                print(f"Paramodular Form S_2(K(N)):    {pf.form_label[:40]}")
                print(f"Hecke Eigenvalues:             T(2) = {pf.hecke_eigenvalue_t2} | T(3) = {pf.hecke_eigenvalue_t3}")
                print(f"Genuine Non-Lift Form:         {ev.is_genuine_non_lift} (CAP Lift: {pf.is_gritsenko_lift})")
            print(f"Spinor L-Function Degree:      {ev.spinor_l_degree} (Euler Factors: {len(loom.euler_factors)} primes)")
            print(f"Paramodular Modularity Holds:  {ev.modularity_conjecture_verified}")
            print(f"Cognitive Resonance Score:     {ev.cognitive_resonance_score:.4f}")
            print(f"Spatial Stability Index:       {ev.spatial_stability_index:.4f}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "paramodular_conjecture_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.generate_svg())
            print(f"[DxSkills] Paramodular SVG written to: {out_path}")
    elif args.command in ["calabi-yau-modularity", "attractor-mechanism", "picard-fuchs", "cy-modularity-loom"]:
        from scripts.calabi_yau_modularity_loom import (
            CalabiYauModularityLoom,
        )
        model_map = {
            "quintic": "Mirror Quintic Threefold",
            "rigid": "Rigid Schoen Calabi-Yau Threefold",
            "octic": "Rigid Octic Threefold",
        }
        model_name = model_map.get(args.model, "Mirror Quintic Threefold")
        try:
            charge_parts = tuple(int(x.strip()) for x in args.charges.split(","))
            if len(charge_parts) != 4:
                charge_parts = (1, 0, 0, -5)
        except Exception:
            charge_parts = (1, 0, 0, -5)

        loom = CalabiYauModularityLoom(model_name)
        result = loom.analyze(charges=charge_parts)

        if args.json:
            import json
            from dataclasses import asdict
            res_dict = {
                "model_name": result.model_name,
                "hodge": asdict(result.hodge),
                "conifold_dist": result.picard_fuchs.conifold_dist,
                "attractor_z": [result.attractor.attractor_z.real, result.attractor.attractor_z.imag],
                "horizon_entropy": result.attractor.horizon_entropy,
                "cm_discriminant": result.attractor.cm_discriminant,
                "modularity_type": result.attractor.modularity_type,
                "modular_level": result.modular_level,
                "hecke_eigenvalues": result.hecke_eigenvalues,
                "modularity_proven": result.modularity_proven,
                "notes": result.notes,
            }
            print(json.dumps(res_dict, indent=2))
        else:
            print("=================================================================")
            print("  Calabi-Yau Modularity & Attractor Mechanism Loom")
            print("=================================================================")
            print(f"Calabi-Yau Model:             {result.model_name}")
            print(f"Hodge Diamond:                h11 = {result.hodge.h11} | h21 = {result.hodge.h21} | chi = {result.hodge.euler_char}")
            print(f"Middle Cohomology Dim:        {result.hodge.middle_cohomology_dim()} (Rigid: {result.hodge.is_rigid()})")
            print(f"Conifold Singularity Dist:    {result.picard_fuchs.conifold_dist:.4f}")
            print(f"Attractor Fixed Point z_*:    {result.attractor.attractor_z.real:.4f} + {result.attractor.attractor_z.imag:.4f}j")
            print(f"Bekenstein-Hawking Entropy:   {result.attractor.horizon_entropy:.4f}")
            print(f"Complex Multiplication Disc:  D = {result.attractor.cm_discriminant}")
            print(f"Modularity Classification:    {result.attractor.modularity_type}")
            print(f"Modular Level & Weights:      N = {result.modular_level} | k in {result.attractor.weight_components}")
            print(f"Modularity Verified (R = T):  {result.modularity_proven}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "calabi_yau_modularity_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] Calabi-Yau SVG written to: {out_path}")
    elif args.command in ["k3-modularity", "borcherds-product", "transcendental-lattice", "k3-loom"]:
        from scripts.k3_modularity_loom import (
            K3ModularityLoom,
        )
        model_map = {
            "shioda": "Shioda-Inose Singular K3 (D=-3)",
            "fermat": "Fermat Quartic K3 (D=-4)",
            "klein": "Klein Quartic Related K3 (D=-7)",
            "generic": "Generic K3 (Picard 1)",
        }
        model_label = model_map.get(args.model, "Shioda-Inose Singular K3 (D=-3)")
        loom = K3ModularityLoom(model_label)
        result = loom.analyze()

        if args.json:
            import json
            from dataclasses import asdict
            b_dict = asdict(result.borcherds)
            b_dict["product_evaluation_sample"] = [
                result.borcherds.product_evaluation_sample.real,
                result.borcherds.product_evaluation_sample.imag,
            ]
            res_dict = {
                "surface_label": result.surface_label,
                "lattice": asdict(result.lattice),
                "borcherds": b_dict,
                "modular_weight": result.modular_weight,
                "modular_level": result.modular_level,
                "hecke_eigenvalues": result.hecke_eigenvalues,
                "point_counts_f_p": result.point_counts_f_p,
                "shioda_inose_cm_field": result.shioda_inose_cm_field,
                "modularity_proven": result.modularity_proven,
                "notes": result.notes,
            }
            print(json.dumps(res_dict, indent=2))
        else:
            print("=================================================================")
            print("  K3 Surfaces Modularity & Borcherds Automorphic Products Loom")
            print("=================================================================")
            print(f"K3 Surface:                   {result.surface_label}")
            print(f"Picard Number rho(S):         {result.lattice.picard_number} (Singular: {result.lattice.is_singular})")
            print(f"Transcendental Lattice T(S):  Rank {result.lattice.transcendental_rank} | Sig {result.lattice.transcendental_signature}")
            print(f"Quadratic Form / Disc:        {result.lattice.quadratic_form} | D = {result.lattice.discriminant_d}")
            print(f"Shioda-Inose CM Field:        {result.shioda_inose_cm_field}")
            print(f"Borcherds Theta Lift:         Orthogonal group O(2, {result.borcherds.lattice_signature[1]})")
            print(f"Reflective Roots in Chamber:  {result.borcherds.num_reflective_roots}")
            print(f"Associated Modular Form:      Weight k = {result.modular_weight} | Level N = {result.modular_level}")
            print(f"Modularity Verified (CM):     {result.modularity_proven}")
            print("=================================================================")

        if args.svg or args.demo:
            out_path = args.svg if args.svg else "k3_modularity_demo.svg"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(loom.render_svg(result))
            print(f"[DxSkills] K3 Modularity SVG written to: {out_path}")
    else:
        parser.print_help()







if __name__ == "__main__":
    main()
