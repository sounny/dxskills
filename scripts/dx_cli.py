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
    else:
        parser.print_help()







if __name__ == "__main__":
    main()
