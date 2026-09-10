#!/usr/bin/env python3
"""
DxSkills Unified CLI Tool (Zero External Dependencies)
Provides direct terminal access to the DxSkills cognitive scaffolding suite.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys
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
        import json
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
        import json
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
        import json
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
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
