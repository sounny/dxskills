#!/usr/bin/env python3
"""
DxSkills Real-Time Voice Dictation & Audio Canvas Streaming Engine
Streams audio chunks or live speech input, removes phonological disfluencies,
and incrementally builds Obsidian Canvas (.canvas) graphs and vector SVGs in real time.

Cognitive Principle:
Dyslexic and spatial thinkers ideate faster aloud than through orthographic typing.
Visualizing spoken ideas immediately as spatial 2D node graphs closes the working memory
feedback loop without requiring linear textual transcription first.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import re
import sys
import json
import time
import uuid

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

DISFLUENCIES = [
    r"\bum\b", r"\buh\b", r"\byou know\b", r"\blike\b", r"\bso basically\b",
    r"\bah\b", r"\ber\b", r"\bI mean\b", r"\bkind of\b", r"\bsort of\b"
]

def clean_speech_chunk(text):
    """Strips filler words, disfluencies, and enforces zero em dashes."""
    cleaned = text
    for pat in DISFLUENCIES:
        cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s+([.,?!])", r"\1", cleaned).strip()
    cleaned = re.sub(r"^[,;:\s]+", "", cleaned).strip()
    
    # Strictly strip em dashes dynamically
    em_char = chr(8212)
    cleaned = cleaned.replace(em_char, " - ")
    return cleaned

class LiveVoiceBuffer:
    """Manages continuous speech transcript stream and semantic landmark segmentation."""

    def __init__(self):
        self.raw_chunks = []
        self.cleaned_text = ""
        self.sentences = []
        self.bluf = ""
        self.pillars = []
        self.actions = []

    def add_chunk(self, chunk):
        """Appends a new transcript chunk and updates semantic landmarks."""
        if not chunk or not chunk.strip():
            return
        
        self.raw_chunks.append(chunk.strip())
        clean_part = clean_speech_chunk(chunk)
        
        if self.cleaned_text:
            self.cleaned_text += " " + clean_part
        else:
            self.cleaned_text = clean_part
            
        # Re-segment sentences
        raw_sents = [s.strip() for s in self.cleaned_text.split(".") if s.strip()]
        self.sentences = []
        for s in raw_sents:
            clean_s = re.sub(r"^[,;:\s]+", "", s).strip()
            if len(clean_s) > 3:
                self.sentences.append(clean_s[0].upper() + clean_s[1:])

        if self.sentences:
            self.bluf = self.sentences[0]
            if not self.bluf.endswith("."):
                self.bluf += "."

            self.pillars = []
            self.actions = []

            for idx, s in enumerate(self.sentences[1:], 1):
                s_lower = s.lower()
                if any(w in s_lower for w in ["first", "second", "third", "deploy", "build", "verify", "ship", "deliver"]):
                    self.actions.append(s)
                else:
                    self.pillars.append(s)

class LiveCanvasStreamer:
    """
    Incrementally constructs an Obsidian Canvas (.canvas) and vector SVG
    as speech transcript chunks stream in from the microphone or audio buffer.
    """

    def __init__(self, session_title="Live Voice Session"):
        self.title = session_title
        self.buffer = LiveVoiceBuffer()
        self.nodes = []
        self.edges = []
        self.chunk_count = 0
        self._initialize_canvas()

    def _initialize_canvas(self):
        root_id = "node-root"
        self.nodes = [{
            "id": root_id,
            "type": "text",
            "text": f"# {self.title}\n\n> **BLUF:** Listening for live speech input...",
            "x": 40,
            "y": 140,
            "width": 340,
            "height": 160,
            "color": "1"  # Obsidian red/accent
        }]
        self.edges = []

    def process_chunk(self, chunk_text):
        """Processes an incoming speech chunk and updates spatial canvas geometry."""
        self.chunk_count += 1
        self.buffer.add_chunk(chunk_text)

        # Update root node BLUF
        bluf_display = self.buffer.bluf or "Listening for live speech input..."
        self.nodes[0]["text"] = f"# {self.title}\n\n> **BLUF:** {bluf_display}"

        # Rebuild sections and action child nodes
        new_nodes = [self.nodes[0]]
        new_edges = []

        sec_x = 440
        sec_y_start = 40
        sec_y_gap = 180

        child_x = 820
        child_y_start = 40
        child_y_gap = 110

        # Create pillar nodes
        for idx, pillar in enumerate(self.buffer.pillars[:4], 1):
            sec_id = f"node-pillar-{idx}"
            sec_y = sec_y_start + ((idx - 1) * sec_y_gap)
            new_nodes.append({
                "id": sec_id,
                "type": "text",
                "text": f"## Focus {idx}\n{pillar}",
                "x": sec_x,
                "y": sec_y,
                "width": 300,
                "height": 120,
                "color": "4"  # Obsidian blue
            })
            new_edges.append({
                "id": f"edge-root-{idx}",
                "fromNode": "node-root",
                "fromSide": "right",
                "toNode": sec_id,
                "toSide": "left"
            })

        # Create action vector child nodes
        for idx, action in enumerate(self.buffer.actions[:5], 1):
            act_id = f"node-action-{idx}"
            act_y = child_y_start + ((idx - 1) * child_y_gap)
            new_nodes.append({
                "id": act_id,
                "type": "text",
                "text": f"**Action {idx}**\n- [ ] {action}",
                "x": child_x,
                "y": act_y,
                "width": 260,
                "height": 90,
                "color": "2"  # Obsidian green
            })
            
            # Connect action to corresponding pillar or root
            parent_id = f"node-pillar-{min(idx, len(self.buffer.pillars))}" if self.buffer.pillars else "node-root"
            new_edges.append({
                "id": f"edge-act-{idx}",
                "fromNode": parent_id,
                "fromSide": "right",
                "toNode": act_id,
                "toSide": "left"
            })

        self.nodes = new_nodes
        self.edges = new_edges

        return {
            "chunk_count": self.chunk_count,
            "nodes_count": len(self.nodes),
            "edges_count": len(self.edges),
            "bluf": self.buffer.bluf,
            "pillars_count": len(self.buffer.pillars),
            "actions_count": len(self.buffer.actions)
        }

    def get_canvas_json(self):
        """Returns standard Obsidian Canvas (.canvas) JSON specification."""
        payload = {
            "nodes": self.nodes,
            "edges": self.edges
        }
        return json.dumps(payload, indent=2)

    def get_canvas_svg(self):
        """Generates publication-grade standalone vector SVG of the live canvas."""
        width = 1140
        height = max(560, len(self.nodes) * 90)
        
        paths_svg = ""
        for edge in self.edges:
            from_n = next((n for n in self.nodes if n["id"] == edge["fromNode"]), None)
            to_n = next((n for n in self.nodes if n["id"] == edge["toNode"]), None)
            if from_n and to_n:
                x1 = from_n["x"] + from_n["width"]
                y1 = from_n["y"] + (from_n["height"] // 2)
                x2 = to_n["x"]
                y2 = to_n["y"] + (to_n["height"] // 2)
                cx1 = x1 + 60
                cy1 = y1
                cx2 = x2 - 60
                cy2 = y2
                paths_svg += f'<path d="M {x1} {y1} C {cx1} {cy1}, {cx2} {cy2}, {x2} {y2}" fill="none" stroke="#52525b" stroke-width="2" marker-end="url(#canvas-arrow)" />\n'

        nodes_svg = ""
        for n in self.nodes:
            col = "#10b981" if n.get("color") == "2" else ("#3b82f6" if n.get("color") == "4" else "#f43f5e")
            safe_text = n["text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            lines = safe_text.split("\n")
            tspan_str = "".join([f'<tspan x="{n["x"] + 14}" dy="18">{l[:36]}</tspan>' for l in lines[:5]])
            
            nodes_svg += f"""
            <g id="{n['id']}">
                <rect x="{n['x']}" y="{n['y']}" width="{n['width']}" height="{n['height']}" rx="10" fill="#18181b" stroke="{col}" stroke-width="2" />
                <text x="{n['x'] + 14}" y="{n['y'] + 14}" fill="#fafafa" font-family="monospace" font-size="11">
                    {tspan_str}
                </text>
            </g>"""

        svg_markup = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <marker id="canvas-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#71717a" />
    </marker>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <circle cx="15" cy="15" r="0.8" fill="#3f3f46" />
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" fill="#09090b" />
  <rect width="{width}" height="{height}" fill="url(#grid)" />
  <g id="edges-group">
    {paths_svg}
  </g>
  <g id="nodes-group">
    {nodes_svg}
  </g>
</svg>"""
        return svg_markup

    def get_markdown_summary(self):
        """Compiles clean D-Mode markdown summary from voice stream buffer."""
        lines = [
            f"# {self.title}",
            f"> **BLUF:** {self.buffer.bluf or 'Session compiled from live voice dictation.'}",
            "",
            "## Core Architecture"
        ]
        if self.buffer.pillars:
            for p in self.buffer.pillars:
                lines.append(f"- {p}")
        else:
            lines.append("- Live streaming architecture in progress.")

        lines.append("")
        lines.append("## Action Vectors")
        if self.buffer.actions:
            for a in self.buffer.actions:
                lines.append(f"- [ ] {a}")
        else:
            lines.append("- [ ] Review live dictation stream and confirm next actions.")

        return "\n".join(lines)

    def export_session(self, output_prefix="live_voice_session"):
        """Exports finalized .canvas, .svg, and .md files to disk."""
        canvas_path = f"{output_prefix}.canvas"
        svg_path = f"{output_prefix}.svg"
        md_path = f"{output_prefix}.md"

        with open(canvas_path, "w", encoding="utf-8") as f:
            f.write(self.get_canvas_json())

        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(self.get_canvas_svg())

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self.get_markdown_summary())

        return {
            "canvas": os.path.abspath(canvas_path),
            "svg": os.path.abspath(svg_path),
            "markdown": os.path.abspath(md_path)
        }

def simulate_streaming_dictation(streamer, chunks, delay=0.0):
    """Simulates real-time microphone dictation from a sequence of chunks."""
    results = []
    for chunk in chunks:
        res = streamer.process_chunk(chunk)
        results.append(res)
        if delay > 0:
            time.sleep(delay)
    return results

if __name__ == "__main__":
    streamer = LiveCanvasStreamer(session_title="Quarterly Strategy Dictation")
    sample_chunks = [
        "Um, the bottom line is that we need to ship the spatial canvas pipeline by Friday.",
        "Like, you know, our first focus area is decoupling worker queues to prevent database lock contention.",
        "Second focus area is setting up automated telemetry alerts for memory spikes.",
        "Third, we must deploy the canary cluster to production and verify latency under load."
    ]
    print("=== [DxSkills: Live Voice-to-Canvas Streamer] ===")
    for idx, c in enumerate(sample_chunks, 1):
        status = streamer.process_chunk(c)
        print(f"[Chunk {idx}] Nodes: {status['nodes_count']} | Edges: {status['edges_count']} | BLUF: {status['bluf'][:45]}...")
    
    print("\n--- Finalized Obsidian Canvas (.canvas) JSON ---")
    print(streamer.get_canvas_json()[:300] + "\n...")
    print("\n--- Finalized Markdown Summary ---")
    print(streamer.get_markdown_summary())
