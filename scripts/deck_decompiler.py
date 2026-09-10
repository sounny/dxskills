"""
Autonomous Multimodal Spatial Lecture and Deck Decompiler for DxSkills.

Decompiles sequential slide decks, lecture notes, and presentations into
interconnected 2D spatial canvas topologies with narrative spines,
deep-dive satellite branches, and conceptual bridge edges.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple


class SlideDeckParser:
    """Parses linear slide decks into structured slide models."""

    SLIDE_SEPARATORS = [
        re.compile(r"^<!--\s*slide\s*-->$", re.MULTILINE | re.IGNORECASE),
        re.compile(r"^---\s*$", re.MULTILINE),
        re.compile(r"^\*\*\*\s*$", re.MULTILINE),
        re.compile(r"^#+\s+(?:Slide\s+\d+|Lecture\s+\d+)", re.MULTILINE | re.IGNORECASE)
    ]

    def __init__(self, raw_content: str):
        self.raw_content = raw_content.strip()

    def parse(self) -> List[Dict[str, Any]]:
        raw_slides = self._split_slides(self.raw_content)
        parsed_slides = []

        for idx, block in enumerate(raw_slides, 1):
            slide_data = self._analyze_slide(block, idx)
            if slide_data:
                parsed_slides.append(slide_data)

        return parsed_slides

    def _split_slides(self, content: str) -> List[str]:
        # Try HTML section tags first
        if "<section" in content and "</section>" in content:
            sections = re.findall(r"<section[^>]*>(.*?)</section>", content, re.DOTALL | re.IGNORECASE)
            if len(sections) > 1:
                return [s.strip() for s in sections if s.strip()]

        # Try markdown slide separators
        for pattern in self.SLIDE_SEPARATORS:
            parts = pattern.split(content)
            clean_parts = [p.strip() for p in parts if p.strip()]
            if len(clean_parts) > 1:
                return clean_parts

        # Fallback: split on markdown H1 or H2 headers
        parts = re.split(r"(?=^#{1,2}\s+)", content, flags=re.MULTILINE)
        clean_parts = [p.strip() for p in parts if p.strip()]
        if len(clean_parts) > 1:
            return clean_parts

        # Single slide fallback
        return [content] if content else []

    @staticmethod
    def _analyze_slide(block: str, index: int) -> Dict[str, Any]:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            return {}

        title = f"Slide {index}"
        bullets = []
        body_lines = []

        # Check for HTML headers first
        html_header_match = re.search(r"<h[1-3][^>]*>(.*?)</h[1-3]>", block, re.IGNORECASE)
        if html_header_match:
            title = re.sub(r"<[^>]+>", "", html_header_match.group(1)).strip()
        else:
            # Find title from first header or first line
            for line in lines:
                if line.startswith("#"):
                    title = re.sub(r"^#+\s*", "", line).strip()
                    break
            if title == f"Slide {index}" and lines:
                first_line = re.sub(r"<[^>]+>", "", lines[0]).strip()
                if len(first_line) < 80 and not first_line.startswith(("-", "*", "1", "2")):
                    title = first_line

        # Extract bullets and text
        html_lis = re.findall(r"<li[^>]*>(.*?)</li>", block, re.IGNORECASE)
        if html_lis:
            for li in html_lis:
                clean_li = re.sub(r"<[^>]+>", "", li).strip()
                if clean_li:
                    bullets.append(clean_li)

        for line in lines:
            if line.startswith("#") and title in line:
                continue
            if line.startswith(("-", "*", "+")) or re.match(r"^\d+\.\s+", line):
                clean_bullet = re.sub(r"^[-*+\d.]+\s*", "", line).strip()
                if clean_bullet:
                    bullets.append(clean_bullet)
            else:
                clean_line = re.sub(r"<[^>]+>", "", line).strip()
                if clean_line and clean_line != title:
                    body_lines.append(clean_line)

        # Infer slide category / role
        t_lower = title.lower()
        if any(w in t_lower for w in ["agenda", "overview", "intro", "welcome", "objective", "roadmap"]):
            category = "Overview"
            color = "4"  # Green
        elif any(w in t_lower for w in ["architecture", "core", "foundation", "pipeline", "system", "engine"]):
            category = "Architecture"
            color = "5"  # Blue
        elif any(w in t_lower for w in ["detail", "deep dive", "benchmark", "evaluation", "telemetry", "algorithm"]):
            category = "Deep Dive"
            color = "6"  # Purple
        elif any(w in t_lower for w in ["milestone", "action", "next step", "rollout", "deploy"]):
            category = "Action"
            color = "2"  # Orange
        elif any(w in t_lower for w in ["summary", "conclusion", "takeaway", "q&a", "wrap"]):
            category = "Summary"
            color = "3"  # Yellow
        else:
            category = "Core Narrative"
            color = "5"  # Blue

        # Extract primary keywords for cross-linking
        words = re.findall(r"\b[A-Za-z0-9_\-]{4,}\b", block.lower())
        stopwords = {"this", "that", "with", "from", "have", "more", "will", "slide", "into", "their"}
        keywords = list(set(w for w in words if w not in stopwords))[:8]

        bluf = bullets[0] if bullets else (body_lines[0] if body_lines else title)
        if len(bluf) > 120:
            bluf = bluf[:117] + "..."

        return {
            "index": index,
            "title": title,
            "category": category,
            "color": color,
            "bluf": bluf,
            "bullets": bullets,
            "body": " ".join(body_lines),
            "keywords": keywords
        }


class SpatialTopologyDecompiler:
    """Arranges linear slides into 2D visual canvas topology with spine and branches."""

    @classmethod
    def decompile_to_canvas(cls, slides: List[Dict[str, Any]], deck_title: str = "Presentation") -> Dict[str, Any]:
        nodes = []
        edges = []

        if not slides:
            return {"nodes": [], "edges": []}

        # Header node
        header_id = "node-deck-header"
        nodes.append({
            "id": header_id,
            "type": "text",
            "text": f"## {deck_title}\nTotal Slides Decompiled: **{len(slides)}**\nSpatial Architecture Active",
            "x": 0,
            "y": -220,
            "width": 380,
            "height": 130,
            "color": "1"  # Red
        })

        spine_x = 0
        spine_y = 0
        prev_spine_node_id = header_id

        # Arrange: Narrative Spine (Horizontal), Deep Dives (Vertical Satellites)
        for slide in slides:
            idx = slide["index"]
            nid = f"slide-{idx}"
            is_deep_dive = slide["category"] == "Deep Dive"

            bullets_text = "\n".join(f"- {b}" for b in slide["bullets"][:4])
            node_text = (
                f"### {slide['index']}. {slide['title']}\n"
                f"> **BLUF:** {slide['bluf']}\n\n"
                f"{bullets_text}"
            ).strip()

            if is_deep_dive:
                # Vertical branch below current spine node
                x_pos = spine_x - 420
                y_pos = spine_y + 320
                width = 360
                height = 220
                from_side = "bottom"
                to_side = "top"
                from_nid = prev_spine_node_id
            else:
                # Horizontal narrative spine
                x_pos = spine_x
                y_pos = spine_y
                width = 380
                height = 240
                from_side = "right" if prev_spine_node_id != header_id else "bottom"
                to_side = "left" if prev_spine_node_id != header_id else "top"
                from_nid = prev_spine_node_id

                prev_spine_node_id = nid
                spine_x += 440

            nodes.append({
                "id": nid,
                "type": "text",
                "text": node_text,
                "x": x_pos,
                "y": y_pos,
                "width": width,
                "height": height,
                "color": slide["color"]
            })

            # Sequential / Branch Edge
            edges.append({
                "id": f"edge-seq-{idx}",
                "fromNode": from_nid,
                "fromSide": from_side,
                "toNode": nid,
                "toSide": to_side,
                "label": "narrative flow" if not is_deep_dive else "technical branch"
            })

        # Add conceptual bridge edges across disparate slides sharing keywords
        edge_count = 0
        for i in range(len(slides)):
            for j in range(i + 2, len(slides)):
                s1 = slides[i]
                s2 = slides[j]
                common_kw = set(s1["keywords"]).intersection(set(s2["keywords"]))
                if len(common_kw) >= 2 and edge_count < 10:
                    edges.append({
                        "id": f"edge-bridge-{s1['index']}-{s2['index']}",
                        "fromNode": f"slide-{s1['index']}",
                        "fromSide": "bottom",
                        "toNode": f"slide-{s2['index']}",
                        "toSide": "bottom",
                        "label": f"shares: {', '.join(list(common_kw)[:2])}",
                        "color": "6"
                    })
                    edge_count += 1

        return {"nodes": nodes, "edges": edges}


class DeckSummaryExporter:
    """Exports structured spatial briefing and vector SVG representations."""

    @staticmethod
    def to_markdown(slides: List[Dict[str, Any]], deck_title: str) -> str:
        lines = []
        lines.append(f"# Spatial Deck Decompilation: {deck_title}")
        lines.append("")
        lines.append(f"> **Decompiled Slides:** `{len(slides)}` | **Architecture:** Non-linear narrative spine with satellite deep dives")
        lines.append("")
        lines.append("## Conceptual Spine & Milestones")
        lines.append("")
        lines.append("| # | Slide Title | Category | BLUF / Core Takeaway | Key Topics |")
        lines.append("|:--|:------------|:---------|:---------------------|:-----------|")

        for s in slides:
            kw_str = ", ".join(s["keywords"][:4])
            lines.append(f"| **{s['index']}** | {s['title']} | `{s['category']}` | {s['bluf']} | `{kw_str}` |")

        lines.append("")
        lines.append("## Modular Spatial Nodes")
        lines.append("")
        for s in slides:
            lines.append(f"### Node {s['index']}: {s['title']}")
            lines.append(f"- **Category:** {s['category']}")
            lines.append(f"- **BLUF:** {s['bluf']}")
            if s["bullets"]:
                lines.append("- **Key Points:**")
                for b in s["bullets"]:
                    lines.append(f"  - {b}")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def to_svg(canvas_data: Dict[str, Any]) -> str:
        nodes = canvas_data.get("nodes", [])
        if not nodes:
            return '<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg"><text x="20" y="50" fill="#fff">No slides decompiled</text></svg>'

        min_x = min(n["x"] for n in nodes)
        max_x = max(n["x"] + n["width"] for n in nodes)
        min_y = min(n["y"] for n in nodes)
        max_y = max(n["y"] + n["height"] for n in nodes)

        padding = 60
        view_w = (max_x - min_x) + (padding * 2)
        view_h = (max_y - min_y) + (padding * 2)

        color_hex = {
            "1": "#ef4444",
            "2": "#f59e0b",
            "3": "#eab308",
            "4": "#10b981",
            "5": "#3b82f6",
            "6": "#8b5cf6"
        }

        svg_parts = [
            f'<svg width="100%" height="auto" viewBox="{min_x - padding} {min_y - padding} {view_w} {view_h}" xmlns="http://www.w3.org/2000/svg">',
            '<rect width="100%" height="100%" fill="#09090b"/>'
        ]

        # Draw edges
        node_map = {n["id"]: n for n in nodes}
        for edge in canvas_data.get("edges", []):
            fn = node_map.get(edge["fromNode"])
            tn = node_map.get(edge["toNode"])
            if fn and tn:
                fx = fn["x"] + fn["width"] / 2
                fy = fn["y"] + fn["height"] / 2
                tx = tn["x"] + tn["width"] / 2
                ty = tn["y"] + tn["height"] / 2
                svg_parts.append(
                    f'<line x1="{fx}" y1="{fy}" x2="{tx}" y2="{ty}" stroke="#3f3f46" stroke-width="2" stroke-dasharray="4 4"/>'
                )

        # Draw nodes
        for n in nodes:
            border_c = color_hex.get(n.get("color", "5"), "#3b82f6")
            first_line = n["text"].split("\n")[0].lstrip("#*-> ").strip()
            first_line_clean = re.sub(r"[<>&]", "", first_line)[:28]
            svg_parts.append(
                f'<g transform="translate({n["x"]}, {n["y"]})">'
                f'<rect width="{n["width"]}" height="{n["height"]}" rx="8" fill="#18181b" stroke="{border_c}" stroke-width="2"/>'
                f'<text x="16" y="32" fill="#fafafa" font-size="14" font-weight="bold" font-family="sans-serif">{first_line_clean}</text>'
                f'</g>'
            )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def decompile_deck(
    content: str,
    deck_title: Optional[str] = None,
    output_canvas: Optional[str] = None,
    output_svg: Optional[str] = None,
    output_markdown: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], str]:
    """Orchestrates slide parsing, spatial topology mapping, and export."""
    parser = SlideDeckParser(content)
    slides = parser.parse()

    title = deck_title
    if not title:
        title = slides[0]["title"] if slides else "Executive Slide Deck"

    canvas_data = SpatialTopologyDecompiler.decompile_to_canvas(slides, deck_title=title)
    md_summary = DeckSummaryExporter.to_markdown(slides, deck_title=title)

    if output_canvas:
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)

    if output_svg:
        os.makedirs(os.path.dirname(os.path.abspath(output_svg)), exist_ok=True)
        svg_code = DeckSummaryExporter.to_svg(canvas_data)
        with open(output_svg, "w", encoding="utf-8") as f:
            f.write(svg_code)

    if output_markdown:
        os.makedirs(os.path.dirname(os.path.abspath(output_markdown)), exist_ok=True)
        with open(output_markdown, "w", encoding="utf-8") as f:
            f.write(md_summary)

    return slides, canvas_data, md_summary


def main():
    parser = argparse.ArgumentParser(description="DxSkills Autonomous Multimodal Spatial Lecture & Deck Decompiler")
    parser.add_argument("input", nargs="?", help="Input deck markdown, HTML, or transcript file")
    parser.add_argument("--title", "-t", help="Explicit presentation title")
    parser.add_argument("--canvas", "-c", help="Output Obsidian .canvas filepath")
    parser.add_argument("--svg", "-s", help="Output vector .svg filepath")
    parser.add_argument("--markdown", "-m", help="Output markdown summary filepath")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON topology")

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
            # Default demonstrative sample deck
            content = (
                "# Slide 1: Executive Mission Overview\n"
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

    slides, canvas_data, md_summary = decompile_deck(
        content,
        deck_title=args.title,
        output_canvas=args.canvas,
        output_svg=args.svg,
        output_markdown=args.markdown
    )

    if args.json:
        print(json.dumps({"slides_count": len(slides), "canvas": canvas_data}, indent=2))
    elif not (args.canvas or args.svg or args.markdown):
        print(md_summary)
    else:
        print(f"[DxSkills] Decompiled {len(slides)} slides into spatial architecture.")
        if args.canvas:
            print(f"  - Canvas: {args.canvas}")
        if args.svg:
            print(f"  - SVG: {args.svg}")
        if args.markdown:
            print(f"  - Markdown: {args.markdown}")


if __name__ == "__main__":
    main()
