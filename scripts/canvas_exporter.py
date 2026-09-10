#!/usr/bin/env python3
"""
DxSkills Spatial Mindmap & Obsidian Canvas (.canvas) Exporter
Converts structured markdown deliverables, executive briefs, and pitch trees into
infinite spatial canvases with calculated 2D coordinates, hierarchical branches, and edges.

Cognitive Principle:
Spatial thinkers process relational networks faster than linear syntax trees.
Mapping deliverables onto 2D canvases reduces phonological working memory overload.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import re
import sys
import json
import uuid

def parse_markdown_to_spatial_graph(markdown_text, title=None):
    """
    Decomposes markdown deliverable into a hierarchical spatial node graph.
    Returns nodes (with x, y, width, height, text, color) and directional edges.
    """
    lines = [l.strip() for l in markdown_text.strip().splitlines() if l.strip()]

    root_title = title or "Spatial Specification"
    bluf = ""
    sections = []
    current_section = None

    for line in lines:
        if not title and line.startswith("# ") and root_title == "Spatial Specification":
            root_title = line.lstrip("# ").strip()
        elif line.startswith("> ") and not bluf:
            clean_q = line.lstrip("> ").strip()
            if any(k in clean_q for k in ["BLUF", "Decision Requested", "Core Value", "Summary"]):
                bluf = clean_q.replace("**", "").replace("*", "")
        elif line.startswith("## "):
            sec_title = line.lstrip("## ").strip()
            current_section = {"title": sec_title, "items": []}
            sections.append(current_section)
        elif current_section and (line.startswith("- ") or line.startswith("* ") or re.match(r"^\d+\.\s", line)):
            clean_item = re.sub(r"^\d+\.\s+", "", line).lstrip("-* ").strip()
            if clean_item and len(current_section["items"]) < 3:
                current_section["items"].append(clean_item)

    # Fallback sections if none parsed
    if not sections:
        sections = [
            {"title": "Core Architecture", "items": ["Modular pipeline", "Zero latency"]},
            {"title": "Execution Milestones", "items": ["Phase 1 delivery", "Production sign-off"]}
        ]

    nodes = []
    edges = []

    # Calculate spatial geometry
    root_id = "node-root-" + str(uuid.uuid4())[:8]
    root_text = f"# {root_title}\n\n" + (f"> **BLUF:** {bluf}" if bluf else "Spatial Central Anchor")
    nodes.append({
        "id": root_id,
        "type": "text",
        "text": root_text,
        "x": 40,
        "y": 140,
        "width": 340,
        "height": 180,
        "color": "1"  # Obsidian red/accent
    })

    sec_y_start = 40
    sec_y_gap = 200
    sec_x = 460
    child_x = 860

    child_node_idx = 1
    for sec_idx, sec in enumerate(sections[:4]):
        sec_id = f"node-sec-{sec_idx + 1}"
        sec_y = sec_y_start + (sec_idx * sec_y_gap)
        
        sec_text = f"## {sec['title']}"
        nodes.append({
            "id": sec_id,
            "type": "text",
            "text": sec_text,
            "x": sec_x,
            "y": sec_y,
            "width": 300,
            "height": 120,
            "color": "4"  # Obsidian blue
        })

        # Connect Root -> Section
        edges.append({
            "id": f"edge-root-{sec_idx + 1}",
            "fromNode": root_id,
            "fromSide": "right",
            "toNode": sec_id,
            "toSide": "left",
            "label": "Section"
        })

        # Child items
        for item_idx, item in enumerate(sec["items"]):
            child_id = f"node-item-{child_node_idx}"
            child_node_idx += 1
            child_y = sec_y - 20 + (item_idx * 90)

            nodes.append({
                "id": child_id,
                "type": "text",
                "text": f"• {item}",
                "x": child_x,
                "y": child_y,
                "width": 280,
                "height": 75,
                "color": "6"  # Obsidian purple/green
            })

            # Connect Section -> Item
            edges.append({
                "id": f"edge-sec-{sec_idx + 1}-item-{item_idx + 1}",
                "fromNode": sec_id,
                "fromSide": "right",
                "toNode": child_id,
                "toSide": "left"
            })

    return {"nodes": nodes, "edges": edges}

def generate_obsidian_canvas(markdown_text, title=None):
    """
    Exports deliverable to an official Obsidian Canvas (.canvas) JSON document.
    """
    graph = parse_markdown_to_spatial_graph(markdown_text, title=title)
    return json.dumps(graph, indent=2)

def generate_svg_canvas(graph, width=1200, height=800):
    """
    Renders the spatial graph into a standalone publication-grade vector SVG.
    Includes connecting cubic bezier splines, node cards, and typographic hierarchy.
    """
    nodes = graph["nodes"]
    edges = graph["edges"]

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#09090b; font-family:ui-monospace,SFMono-Regular,Menlo,monospace;">',
        '  <defs>',
        '    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '      <path d="M 0 1 L 10 5 L 0 9 z" fill="#71717a" />',
        '    </marker>',
        '    <linearGradient id="root-grad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#18181b"/>',
        '      <stop offset="100%" stop-color="#27272a"/>',
        '    </linearGradient>',
        '  </defs>',
        '  <!-- Background Grid -->',
        '  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">',
        '    <circle cx="2" cy="2" r="1" fill="#27272a" />',
        '  </pattern>',
        f'  <rect width="{width}" height="{height}" fill="url(#grid)" />'
    ]

    # Node lookup for edges
    node_map = {n["id"]: n for n in nodes}

    # Render Edges
    svg_parts.append('  <!-- Edges -->')
    for edge in edges:
        from_node = node_map.get(edge["fromNode"])
        to_node = node_map.get(edge["toNode"])
        if from_node and to_node:
            x1 = from_node["x"] + from_node["width"]
            y1 = from_node["y"] + (from_node["height"] / 2)
            x2 = to_node["x"]
            y2 = to_node["y"] + (to_node["height"] / 2)
            cx1 = x1 + (x2 - x1) * 0.5
            cy1 = y1
            cx2 = x1 + (x2 - x1) * 0.5
            cy2 = y2
            svg_parts.append(f'  <path d="M {x1} {y1} C {cx1} {cy1}, {cx2} {cy2}, {x2} {y2}" fill="none" stroke="#52525b" stroke-width="2" marker-end="url(#arrow)" />')

    # Render Nodes
    svg_parts.append('  <!-- Nodes -->')
    for n in nodes:
        nx = n["x"]
        ny = n["y"]
        nw = n["width"]
        nh = n["height"]
        color = n.get("color", "1")
        border_color = "#e4e4e7" if color == "1" else ("#38bdf8" if color == "4" else "#a855f7")

        raw_text = n["text"]
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        header_text = lines[0].replace("# ", "").replace("## ", "") if lines else ""
        body_text = lines[1] if len(lines) > 1 else ""

        svg_parts.append(f'  <g id="{n["id"]}">')
        svg_parts.append(f'    <rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="12" fill="#18181b" stroke="{border_color}" stroke-width="1.5" />')
        svg_parts.append(f'    <text x="{nx + 16}" y="{ny + 30}" fill="#f4f4f5" font-size="13" font-weight="bold">{header_text}</text>')
        if body_text:
            cleaned_body = body_text.replace("> **BLUF:**", "BLUF:").replace("•", "").strip()[:42]
            svg_parts.append(f'    <text x="{nx + 16}" y="{ny + 58}" fill="#a1a1aa" font-size="11">{cleaned_body}</text>')
        svg_parts.append('  </g>')

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)

if __name__ == "__main__":
    sample = (
        "# Space Logistics Architecture\n"
        "> **BLUF:** Deploy autonomous orbital depot by 2028.\n\n"
        "## Propellant Transfer\n"
        "- Cryogenic zero-boil-off insulation\n"
        "- Automated docking coupler\n\n"
        "## Orbital Dynamics\n"
        "- Low Earth orbit staging\n"
        "- Lunar gateway transfer orbit\n"
    )
    canvas_json = generate_obsidian_canvas(sample, title="Orbital Depot")
    print("Obsidian Canvas JSON generated with length:", len(canvas_json))
    svg = generate_svg_canvas(parse_markdown_to_spatial_graph(sample))
    print("SVG generated with length:", len(svg))
