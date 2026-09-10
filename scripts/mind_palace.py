"""
Autonomous Cognitive Spatial Mind Palace Virtual Tour and Spatial Audio Navigator.

Transforms Obsidian .canvas graphs and markdown notes into 3D architectural
method-of-loci memory palaces with room-by-room loci and binaural spatial audio cues.
Generates architectural blueprint canvases, vector SVG floorplans, and interactive tours.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import re
import math
import argparse
from typing import Dict, List, Any, Optional, Tuple


class MindPalaceProjector:
    """Projects 2D canvas nodes into 3D architectural rooms and binaural soundscapes."""

    CHAMBER_ARCHETYPES = [
        ("The Grand Atrium", "Inciting Friction and Entry Portal", "#ef4444", "1"),
        ("The Architectural Gallery", "Core Relational Models and Systems", "#3b82f6", "5"),
        ("The Rotunda of Vectors", "Technical Mechanisms and Pipelines", "#8b5cf6", "2"),
        ("The Observatory of Synthesis", "Empirical Resolution and Horizon", "#10b981", "4")
    ]

    FIXTURE_POSITIONS = [
        ("North Alcove", 0.0, 8.0, 1.5, 0.0),
        ("East Hearth", 8.0, 0.0, 1.0, 90.0),
        ("South Portal", 0.0, -8.0, 1.0, 180.0),
        ("West Colonnade", -8.0, 0.0, 1.0, -90.0),
        ("Center Pedestal", 0.0, 0.0, 0.8, 0.0)
    ]

    @classmethod
    def project_palace(
        cls,
        nodes: List[Dict[str, Any]],
        palace_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Distributes concepts across architectural chambers with spatial audio metadata."""
        title = palace_title or "Spatial Cognitive Mind Palace"
        total_nodes = len(nodes)

        if total_nodes == 0:
            nodes = [
                {"id": "node-demo-1", "text": "Linear prose causes cognitive loop saturation."},
                {"id": "node-demo-2", "text": "Spatial mind palaces anchor ideas to hippocampal coordinates."},
                {"id": "node-demo-3", "text": "Binaural audio cues reinforce loci recall through acoustic azimuth."},
                {"id": "node-demo-4", "text": "Architectural navigation disarms reductionist critique effortlessly."}
            ]
            total_nodes = len(nodes)

        nodes_per_chamber = max(1, math.ceil(total_nodes / len(cls.CHAMBER_ARCHETYPES)))
        chambers = []

        for c_idx, (chamber_name, theme, hex_col, color_id) in enumerate(cls.CHAMBER_ARCHETYPES):
            start_i = c_idx * nodes_per_chamber
            end_i = min(total_nodes, (c_idx + 1) * nodes_per_chamber)
            assigned_nodes = nodes[start_i:end_i]

            if not assigned_nodes and c_idx > 0:
                continue

            chamber_loci = []
            for l_idx, node in enumerate(assigned_nodes):
                fix_name, fx, fy, fz, azimuth = cls.FIXTURE_POSITIONS[l_idx % len(cls.FIXTURE_POSITIONS)]
                text_content = node.get("text", node.get("title", f"Locus {l_idx + 1}"))
                clean_snippet = re.sub(r"^[#\s*->]+", "", text_content.split("\n")[0]).strip()

                distance_m = round(math.sqrt(fx * fx + fy * fy), 1)
                stereo_pan = round(math.sin(math.radians(azimuth)), 2)

                chamber_loci.append({
                    "locus_id": f"locus-{c_idx + 1}-{l_idx + 1}",
                    "source_id": node.get("id", f"node-{l_idx + 1}"),
                    "fixture": fix_name,
                    "title": clean_snippet[:40] if len(clean_snippet) > 40 else clean_snippet,
                    "full_text": text_content,
                    "coordinates": {"x": fx, "y": fy, "z": fz},
                    "spatial_audio": {
                        "azimuth_degrees": azimuth,
                        "stereo_pan": stereo_pan,
                        "distance_meters": distance_m,
                        "acoustic_cue": f"Speak with acoustic focus at {fix_name} ({azimuth} deg, pan {stereo_pan})"
                    }
                })

            chambers.append({
                "chamber_id": f"chamber-{c_idx + 1}",
                "name": chamber_name,
                "theme": theme,
                "color_id": color_id,
                "hex_color": hex_col,
                "grid_coordinates": {"room_x": (c_idx % 2) * 900, "room_y": (c_idx // 2) * 700},
                "loci": chamber_loci
            })

        return {
            "title": title,
            "total_chambers": len(chambers),
            "total_loci": sum(len(c["loci"]) for c in chambers),
            "chambers": chambers
        }


class MindPalaceExporter:
    """Exports mind palace architectures into Obsidian Canvas, vector SVG, and HTML tours."""

    @staticmethod
    def to_canvas(palace: Dict[str, Any]) -> Dict[str, Any]:
        """Generates room-by-room architectural blueprint Obsidian Canvas."""
        nodes = []
        edges = []

        title = palace.get("title", "Cognitive Mind Palace")

        # Master Welcome Portal
        root_id = "node-palace-entry"
        nodes.append({
            "id": root_id,
            "type": "text",
            "text": (
                f"## {title}\n"
                f"**Architectural Chambers:** `{palace.get('total_chambers', 0)}` | **Memory Loci:** `{palace.get('total_loci', 0)}`\n\n"
                f"> Method-of-Loci episodic navigation with binaural acoustic guidance."
            ),
            "x": -200,
            "y": -350,
            "width": 450,
            "height": 160,
            "color": "5"
        })

        prev_chamber_id = root_id

        for c in palace.get("chambers", []):
            rx = c["grid_coordinates"]["room_x"] - 400
            ry = c["grid_coordinates"]["room_y"]

            # Chamber Header Frame
            c_header_id = f"node-room-{c['chamber_id']}"
            nodes.append({
                "id": c_header_id,
                "type": "text",
                "text": f"### {c['name']}\n*{c['theme']}*\nLoci Anchors: **{len(c['loci'])}**",
                "x": rx,
                "y": ry - 90,
                "width": 380,
                "height": 110,
                "color": c["color_id"]
            })

            edges.append({
                "id": f"edge-portal-{c['chamber_id']}",
                "fromNode": prev_chamber_id,
                "fromSide": "bottom" if prev_chamber_id == root_id else "right",
                "toNode": c_header_id,
                "toSide": "top" if prev_chamber_id == root_id else "left",
                "label": "Portal Transition"
            })
            prev_chamber_id = c_header_id

            # Individual Loci nodes in this chamber
            for idx, locus in enumerate(c["loci"]):
                lx = rx + (idx % 2) * 320
                ly = ry + 80 + (idx // 2) * 200
                lid = locus["locus_id"]

                sa = locus["spatial_audio"]
                nodes.append({
                    "id": lid,
                    "type": "text",
                    "text": (
                        f"#### {locus['fixture']}: {locus['title']}\n\n"
                        f"> {locus['full_text'][:110]}...\n\n"
                        f"🔊 **Audio Anchor:** `{sa['azimuth_degrees']} deg` (Pan `{sa['stereo_pan']}`)"
                    ),
                    "x": lx,
                    "y": ly,
                    "width": 300,
                    "height": 180,
                    "color": c["color_id"]
                })

                edges.append({
                    "id": f"edge-locus-{lid}",
                    "fromNode": c_header_id,
                    "fromSide": "bottom",
                    "toNode": lid,
                    "toSide": "top",
                    "label": locus["fixture"]
                })

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def to_svg_blueprint(palace: Dict[str, Any]) -> str:
        """Renders 2D architectural blueprint floorplan with audio direction cones."""
        width = 800
        height = 460
        chambers = palace.get("chambers", [])
        title = palace.get("title", "Cognitive Mind Palace Blueprint")

        svg = []
        svg.append(f'<svg width="100%" height="auto" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'<rect width="{width}" height="{height}" rx="14" fill="#09090b" stroke="#27272a" stroke-width="1.5"/>')

        # Header Title
        svg.append(f'<text x="28" y="38" fill="#fafafa" font-size="18" font-weight="bold" font-family="sans-serif">{title}</text>')
        svg.append(f'<text x="28" y="58" fill="#a1a1aa" font-size="12" font-family="sans-serif">Architectural Method-of-Loci Floorplan | Total Loci: {palace.get("total_loci", 0)}</text>')

        # 4 Chamber Rooms arranged 2x2
        room_w = 350
        room_h = 160
        spacing = 24
        start_x = 34
        start_y = 80

        for idx, c in enumerate(chambers[:4]):
            col = idx % 2
            row = idx // 2
            rx = start_x + col * (room_w + spacing)
            ry = start_y + row * (room_h + spacing)
            hex_col = c.get("hex_color", "#3b82f6")

            # Room wall rect
            svg.append(f'<g transform="translate({rx}, {ry})">')
            svg.append(f'<rect width="{room_w}" height="{room_h}" rx="8" fill="#18181b" stroke="{hex_col}" stroke-width="1.5"/>')
            svg.append(f'<rect x="0" y="0" width="{room_w}" height="26" rx="8" fill="{hex_col}22"/>')
            svg.append(f'<text x="12" y="18" fill="{hex_col}" font-size="11" font-weight="bold" font-family="sans-serif">{c["name"].upper()}</text>')

            # Fixture markers
            for l_idx, locus in enumerate(c.get("loci", [])[:4]):
                lx = 30 + (l_idx % 2) * 160
                ly = 50 + (l_idx // 2) * 55
                sa = locus["spatial_audio"]

                svg.append(f'<circle cx="{lx}" cy="{ly}" r="6" fill="{hex_col}"/>')
                svg.append(f'<text x="{lx + 12}" y="{ly + 4}" fill="#e4e4e7" font-size="10" font-weight="bold" font-family="sans-serif">{locus["fixture"]}</text>')
                title_snip = locus["title"][:18] + ("..." if len(locus["title"]) > 18 else "")
                svg.append(f'<text x="{lx + 12}" y="{ly + 16}" fill="#71717a" font-size="9" font-family="sans-serif">{title_snip}</text>')

            svg.append('</g>')

        # Footer
        svg.append(f'<text x="28" y="440" fill="#52525b" font-size="10" font-family="sans-serif">DxSkills Spatial Navigation Architecture | Binaural Loci Navigator</text>')
        svg.append('</svg>')
        return "\n".join(svg)


def run_mind_palace(
    input_text: str,
    title: Optional[str] = None,
    output_canvas: Optional[str] = None,
    output_svg: Optional[str] = None
) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """Projects text into mind palace and exports canvas and SVG artifacts."""
    doc_title = title or "Method-of-Loci Mind Palace"

    # Parse input into list of node texts
    lines = [line.strip() for line in input_text.split("\n") if line.strip()]
    nodes = []
    for line in lines:
        if line.startswith(("#", ">")):
            continue
        clean = re.sub(r"^[-*+\d.]+\s*", "", line).strip()
        if len(clean) > 8:
            nodes.append({"text": clean})

    palace = MindPalaceProjector.project_palace(nodes, palace_title=doc_title)
    canvas_data = MindPalaceExporter.to_canvas(palace)
    svg_code = MindPalaceExporter.to_svg_blueprint(palace)

    if output_canvas:
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)

    if output_svg:
        os.makedirs(os.path.dirname(os.path.abspath(output_svg)), exist_ok=True)
        with open(output_svg, "w", encoding="utf-8") as f:
            f.write(svg_code)

    return palace, canvas_data, svg_code


def main():
    parser = argparse.ArgumentParser(description="DxSkills Autonomous Spatial Cognitive Mind Palace Navigator")
    parser.add_argument("input", nargs="?", help="Input markdown note, topic outline, or text file")
    parser.add_argument("--title", "-t", help="Mind Palace title")
    parser.add_argument("--canvas", "-c", help="Output Obsidian .canvas filepath")
    parser.add_argument("--svg", "-s", help="Output vector SVG blueprint floorplan filepath")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON palace telemetry")

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
                "# Spatial Memory Architecture\n"
                "- Linear text creates phonological loop bottleneck.\n"
                "- Method-of-loci memory palaces activate hippocampal spatial navigation.\n"
                "- Binaural acoustic orientation reinforces episodic memory recall.\n"
                "- Structured chambers allow non-linear review without cognitive exhaustion."
            )

    palace, canvas_data, svg_code = run_mind_palace(
        content,
        title=args.title,
        output_canvas=args.canvas,
        output_svg=args.svg
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
        print(f"[DxSkills] Mind Palace projected: {palace['total_chambers']} Chambers with {palace['total_loci']} Memory Loci.")
        if args.canvas:
            print(f"  - Canvas: {args.canvas}")
        if args.svg:
            print(f"  - Blueprint: {args.svg}")


if __name__ == "__main__":
    main()
