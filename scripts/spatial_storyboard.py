"""
Autonomous Multi-Modal Spatial Audio-Visual Storyboarder for DxSkills.

Decomposes narrative scripts, venture pitches, and architectural proposals
into 3-act visual beats with camera framing, audio cues, and vector animatics.
Generates Obsidian .canvas storyboards and interactive SVG animatic strips.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple


class StoryboardSequencer:
    """Parses text scripts into a 3-act cinematic storyboard."""

    CAMERA_FRAMINGS = [
        "Overhead Spatial Map (OSM)",
        "Extreme Wide Shot (EWS)",
        "Wide Establishing Shot (WES)",
        "Medium System Shot (MSS)",
        "Close-Up Focus (CU)",
        "Macro Synthesis Vista (MSV)"
    ]

    @classmethod
    def sequence_script(cls, script_text: str) -> Dict[str, Any]:
        raw_shots = cls._extract_shot_units(script_text)
        total_shots = len(raw_shots)

        acts = {"Act I": [], "Act II": [], "Act III": []}
        shot_models = []

        total_duration = 0

        for idx, shot in enumerate(raw_shots, 1):
            # Assign Act based on position
            if idx <= max(1, round(total_shots * 0.25)):
                act_name = "Act I"
                act_title = "The Status Quo and Inciting Friction"
                color = "1"  # Red
            elif idx <= max(2, round(total_shots * 0.75)):
                act_name = "Act II"
                act_title = "The Architectural Confrontation"
                color = "5"  # Blue
            else:
                act_name = "Act III"
                act_title = "The Resolution and Transformation"
                color = "4"  # Green

            framing = cls.CAMERA_FRAMINGS[(idx - 1) % len(cls.CAMERA_FRAMINGS)]
            duration_sec = max(3, min(12, round(len(shot.split()) * 0.4)))
            total_duration += duration_sec

            shot_data = {
                "shot_index": idx,
                "act": act_name,
                "act_title": act_title,
                "color": color,
                "title": f"Shot {idx}: {shot[:32]}..." if len(shot) > 32 else f"Shot {idx}: {shot}",
                "framing": framing,
                "duration_seconds": duration_sec,
                "action": shot,
                "audio_cue": f"Acoustic Beat {idx}: Speak with deliberate pace ({duration_sec}s runtime)"
            }

            acts[act_name].append(shot_data)
            shot_models.append(shot_data)

        return {
            "total_shots": len(shot_models),
            "total_duration_seconds": total_duration,
            "acts": acts,
            "shots": shot_models
        }

    @classmethod
    def _extract_shot_units(cls, text: str) -> List[str]:
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        shots = []

        for line in lines:
            if line.startswith(("#", ">")):
                continue
            if line.startswith(("-", "*")) or re.match(r"^\d+\.\s+", line):
                clean = re.sub(r"^[-*+\d.]+\s*", "", line).strip()
                if len(clean) > 8:
                    shots.append(clean)
            else:
                sentences = re.split(r"(?<=[.!?])\s+", line)
                for s in sentences:
                    clean = s.strip()
                    if len(clean) > 12:
                        shots.append(clean)

        if not shots:
            # Default demonstrative 3-act pitch storyboard
            shots = [
                "Establish the friction: Linear text walls overload phonological working memory in traditional documentation.",
                "Inciting shift: Non-linear thinkers struggle to communicate complex holistic architectures through sequential slides.",
                "Core exploration: The DxSkills cognitive engine decouples spatial mental models from linear output streams.",
                "Technical deep dive: High-dimensional vector similarity clusters ideas into constellation topologies.",
                "Multi-vault bridge: Cross-repository synchronizers identify dangling wikilinks and orphan nodes in real time.",
                "Resolution vista: The user presents a hardened spatial canvas that disarms reductionist critics instantly."
            ]

        return shots


class StoryboardExporter:
    """Exports storyboards into Obsidian Canvas and vector SVG animatics."""

    @staticmethod
    def to_canvas(storyboard: Dict[str, Any], title: str = "Narrative Storyboard") -> Dict[str, Any]:
        nodes = []
        edges = []

        shots = storyboard.get("shots", [])

        # Header root
        header_id = "node-storyboard-header"
        nodes.append({
            "id": header_id,
            "type": "text",
            "text": f"## {title}\nTotal Shots: **{len(shots)}** | Runtime: **{storyboard.get('total_duration_seconds', 0)}s**\n3-Act Spatial Cinematics Active",
            "x": 0,
            "y": -280,
            "width": 380,
            "height": 140,
            "color": "1"
        })

        x_pos = -600
        y_pos = 0

        prev_node_id = header_id

        for s in shots:
            sid = f"shot-node-{s['shot_index']}"
            act = s["act"]

            # Layout by acts: horizontally staggered
            node_text = (
                f"### {s['title']}\n"
                f"**Act:** `{act}` | **Framing:** `{s['framing']}`\n\n"
                f"> **Action:** {s['action']}\n\n"
                f"⏱ **Duration:** `{s['duration_seconds']}s` | 🔊 `{s['audio_cue']}`"
            )

            nodes.append({
                "id": sid,
                "type": "text",
                "text": node_text,
                "x": x_pos,
                "y": y_pos,
                "width": 360,
                "height": 220,
                "color": s["color"]
            })

            edges.append({
                "id": f"edge-seq-{s['shot_index']}",
                "fromNode": prev_node_id,
                "fromSide": "right" if prev_node_id != header_id else "bottom",
                "toNode": sid,
                "toSide": "left" if prev_node_id != header_id else "top",
                "label": f"+{s['duration_seconds']}s"
            })

            prev_node_id = sid
            x_pos += 420
            if s["shot_index"] % 3 == 0:
                y_pos += 120  # Organic downward stagger per act

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def to_svg_animatic(storyboard: Dict[str, Any], title: str = "Spatial Storyboard Strip") -> str:
        shots = storyboard.get("shots", [])
        if not shots:
            return '<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg"><text x="20" y="40" fill="#fff">No shots sequenced</text></svg>'

        panel_w = 280
        panel_h = 160
        spacing = 24
        total_w = len(shots) * (panel_w + spacing) + spacing
        total_h = panel_h + 160

        svg = []
        svg.append(f'<svg width="100%" height="auto" viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'<rect width="{total_w}" height="{total_h}" rx="12" fill="#09090b" stroke="#27272a" stroke-width="1"/>')

        svg.append(f'<text x="24" y="36" fill="#fafafa" font-size="18" font-weight="bold" font-family="sans-serif">{title}</text>')
        svg.append(f'<text x="24" y="58" fill="#a1a1aa" font-size="12" font-family="sans-serif">3-Act Narrative Animatic Strip | Total Runtime: {storyboard.get("total_duration_seconds", 0)}s</text>')

        cur_x = spacing
        panel_y = 80

        colors = {"1": "#ef4444", "4": "#10b981", "5": "#3b82f6"}

        for s in shots:
            c = colors.get(s["color"], "#3b82f6")
            action_snippet = re.sub(r"[<>&]", "", s["action"])[:36] + "..."

            svg.append(f'<g transform="translate({cur_x}, {panel_y})">')
            # 16:9 panel box
            svg.append(f'<rect width="{panel_w}" height="{panel_h}" rx="8" fill="#18181b" stroke="{c}" stroke-width="2"/>')
            # Camera framing rule-of-thirds guides
            svg.append(f'<line x1="{panel_w / 3}" y1="0" x2="{panel_w / 3}" y2="{panel_h}" stroke="#27272a" stroke-width="1" stroke-dasharray="2 2"/>')
            svg.append(f'<line x1="{2 * panel_w / 3}" y1="0" x2="{2 * panel_w / 3}" y2="{panel_h}" stroke="#27272a" stroke-width="1" stroke-dasharray="2 2"/>')
            svg.append(f'<line x1="0" y1="{panel_h / 3}" x2="{panel_w}" y2="{panel_h / 3}" stroke="#27272a" stroke-width="1" stroke-dasharray="2 2"/>')
            svg.append(f'<line x1="0" y1="{2 * panel_h / 3}" x2="{panel_w}" y2="{2 * panel_h / 3}" stroke="#27272a" stroke-width="1" stroke-dasharray="2 2"/>')

            # Shot labels
            svg.append(f'<rect x="8" y="8" width="54" height="20" rx="4" fill="{c}22" stroke="{c}"/>')
            svg.append(f'<text x="35" y="22" fill="{c}" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">SHOT {s["shot_index"]}</text>')

            svg.append(f'<rect x="{panel_w - 60}" y="8" width="52" height="20" rx="4" fill="#27272a"/>')
            svg.append(f'<text x="{panel_w - 34}" y="22" fill="#fafafa" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">{s["duration_seconds"]}s</text>')

            # Framing
            svg.append(f'<text x="12" y="70" fill="#38bdf8" font-size="11" font-weight="600" font-family="sans-serif">{s["framing"]}</text>')
            # Action text
            svg.append(f'<text x="12" y="96" fill="#e4e4e7" font-size="11" font-family="sans-serif">{action_snippet}</text>')
            # Act indicator
            svg.append(f'<text x="12" y="{panel_h - 14}" fill="#71717a" font-size="10" font-family="sans-serif">{s["act"]} ({s["act_title"].split()[0]})</text>')

            svg.append('</g>')
            cur_x += panel_w + spacing

        svg.append('</svg>')
        return "\n".join(svg)


def run_storyboard(
    script_text: str,
    title: Optional[str] = None,
    output_canvas: Optional[str] = None,
    output_svg: Optional[str] = None
) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """Sequences script into storyboard and exports outputs."""
    seq_title = title or "3-Act Narrative Storyboard"
    storyboard = StoryboardSequencer.sequence_script(script_text)

    canvas_data = StoryboardExporter.to_canvas(storyboard, title=seq_title)
    svg_code = StoryboardExporter.to_svg_animatic(storyboard, title=seq_title)

    if output_canvas:
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)

    if output_svg:
        os.makedirs(os.path.dirname(os.path.abspath(output_svg)), exist_ok=True)
        with open(output_svg, "w", encoding="utf-8") as f:
            f.write(svg_code)

    return storyboard, canvas_data, svg_code


def main():
    parser = argparse.ArgumentParser(description="DxSkills Autonomous Multi-Modal Spatial Audio-Visual Storyboarder")
    parser.add_argument("input", nargs="?", help="Input narrative script, pitch markdown, or text file")
    parser.add_argument("--title", "-t", help="Storyboard title")
    parser.add_argument("--canvas", "-c", help="Output Obsidian .canvas filepath")
    parser.add_argument("--svg", "-s", help="Output vector SVG animatic strip filepath")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON storyboard telemetry")

    args = parser.parse_args()

    content = ""
    if args.input:
        if os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = args.input
    else:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            content = (
                "Establish the friction: Linear text walls overload phonological working memory.\n"
                "Inciting shift: Non-linear thinkers struggle to communicate complex holistic architectures through sequential slides.\n"
                "Core exploration: The DxSkills cognitive engine decouples spatial mental models from linear output streams.\n"
                "Technical deep dive: High-dimensional vector similarity clusters ideas into constellation topologies.\n"
                "Multi-vault bridge: Cross-repository synchronizers identify dangling wikilinks and orphan nodes in real time.\n"
                "Resolution vista: The user presents a hardened spatial canvas that disarms reductionist critics instantly."
            )

    storyboard, canvas_data, svg_code = run_storyboard(
        content,
        title=args.title,
        output_canvas=args.canvas,
        output_svg=args.svg
    )

    if args.json:
        print(json.dumps(storyboard, indent=2))
    elif not (args.canvas or args.svg):
        print(f"\n=== [DxSkills: 3-Act Spatial Storyboard ({storyboard['total_shots']} Shots | {storyboard['total_duration_seconds']}s)] ===")
        for s in storyboard["shots"]:
            print(f"[{s['act']}] Shot {s['shot_index']} ({s['framing']}, {s['duration_seconds']}s): {s['action']}")
    else:
        print(f"[DxSkills] Sequenced {storyboard['total_shots']} shots across 3 acts ({storyboard['total_duration_seconds']}s total).")
        if args.canvas:
            print(f"  - Canvas: {args.canvas}")
        if args.svg:
            print(f"  - SVG: {args.svg}")


if __name__ == "__main__":
    main()
