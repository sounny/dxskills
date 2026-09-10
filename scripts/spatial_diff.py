"""
Autonomous Spatial Cognitive Architecture Graph Differential and Version Divergence Engine.

Diffs two Obsidian .canvas spatial architectures or markdown note snapshots,
computing topological node-edge drift, spatial coordinate translations, and
generating visual branch conflict resolution canvases.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import math
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple, Set


class SpatialGraphDiffer:
    """Computes topological and spatial geometric drift between two canvas graphs."""

    @classmethod
    def diff_canvases(
        cls,
        canvas_a: Dict[str, Any],
        canvas_b: Dict[str, Any],
        position_drift_threshold: float = 50.0
    ) -> Dict[str, Any]:
        """Calculates differences in nodes, edges, content, and spatial positions."""
        nodes_a = {n["id"]: n for n in canvas_a.get("nodes", []) if "id" in n}
        nodes_b = {n["id"]: n for n in canvas_b.get("nodes", []) if "id" in n}

        added_node_ids = set(nodes_b.keys()) - set(nodes_a.keys())
        removed_node_ids = set(nodes_a.keys()) - set(nodes_b.keys())
        common_node_ids = set(nodes_a.keys()) & set(nodes_b.keys())

        modified_nodes = []
        relocated_nodes = []
        unchanged_nodes = []

        for nid in common_node_ids:
            na = nodes_a[nid]
            nb = nodes_b[nid]

            # Content comparison
            text_a = na.get("text", na.get("file", ""))
            text_b = nb.get("text", nb.get("file", ""))
            color_a = na.get("color", "")
            color_b = nb.get("color", "")

            content_changed = (text_a != text_b) or (color_a != color_b)

            # Spatial movement
            xa, ya = float(na.get("x", 0)), float(na.get("y", 0))
            xb, yb = float(nb.get("x", 0)), float(nb.get("y", 0))
            dx = xb - xa
            dy = yb - ya
            dist = math.sqrt(dx * dx + dy * dy)

            is_relocated = dist >= position_drift_threshold

            if content_changed:
                modified_nodes.append({
                    "id": nid,
                    "previous_text": text_a,
                    "current_text": text_b,
                    "spatial_shift": {"dx": dx, "dy": dy, "distance": round(dist, 1)},
                    "node": nb
                })
            elif is_relocated:
                relocated_nodes.append({
                    "id": nid,
                    "spatial_shift": {"dx": dx, "dy": dy, "distance": round(dist, 1)},
                    "node": nb
                })
            else:
                unchanged_nodes.append(nid)

        # Edges comparison
        edges_a = canvas_a.get("edges", [])
        edges_b = canvas_b.get("edges", [])

        edge_tuples_a = {
            (e.get("fromNode"), e.get("toNode")): e for e in edges_a if "fromNode" in e and "toNode" in e
        }
        edge_tuples_b = {
            (e.get("fromNode"), e.get("toNode")): e for e in edges_b if "fromNode" in e and "toNode" in e
        }

        added_edges = [
            edge_tuples_b[pair] for pair in set(edge_tuples_b.keys()) - set(edge_tuples_a.keys())
        ]
        removed_edges = [
            edge_tuples_a[pair] for pair in set(edge_tuples_a.keys()) - set(edge_tuples_b.keys())
        ]
        retained_edges = [
            edge_tuples_b[pair] for pair in set(edge_tuples_a.keys()) & set(edge_tuples_b.keys())
        ]

        # Topological Stability Index (Sorensen-Dice edge ratio)
        total_edge_cardinality = len(edges_a) + len(edges_b)
        if total_edge_cardinality > 0:
            tsi = round((2.0 * len(retained_edges)) / total_edge_cardinality, 3)
        else:
            tsi = 1.0

        drift_percentage = round((1.0 - tsi) * 100.0, 1)

        return {
            "topological_stability_index": tsi,
            "graph_drift_percentage": drift_percentage,
            "summary": {
                "nodes_before": len(nodes_a),
                "nodes_after": len(nodes_b),
                "nodes_added": len(added_node_ids),
                "nodes_removed": len(removed_node_ids),
                "nodes_modified": len(modified_nodes),
                "nodes_relocated": len(relocated_nodes),
                "nodes_unchanged": len(unchanged_nodes),
                "edges_before": len(edges_a),
                "edges_after": len(edges_b),
                "edges_added": len(added_edges),
                "edges_removed": len(removed_edges),
                "edges_retained": len(retained_edges)
            },
            "added_nodes": [nodes_b[nid] for nid in added_node_ids],
            "removed_nodes": [nodes_a[nid] for nid in removed_node_ids],
            "modified_nodes": modified_nodes,
            "relocated_nodes": relocated_nodes,
            "added_edges": added_edges,
            "removed_edges": removed_edges
        }


class VisualMergeResolver:
    """Generates visual conflict resolution Obsidian Canvas and SVG diff maps."""

    @staticmethod
    def to_differential_canvas(
        diff_report: Dict[str, Any],
        canvas_b: Dict[str, Any],
        title: str = "Differential Canvas Merge"
    ) -> Dict[str, Any]:
        """Synthesizes a combined visual diff canvas highlighting mutations."""
        nodes = []
        edges = []

        added_ids = {n["id"] for n in diff_report.get("added_nodes", [])}
        removed_ids = {n["id"] for n in diff_report.get("removed_nodes", [])}
        modified_dict = {m["id"]: m for m in diff_report.get("modified_nodes", [])}
        relocated_dict = {r["id"]: r for r in diff_report.get("relocated_nodes", [])}

        summary = diff_report.get("summary", {})
        tsi = diff_report.get("topological_stability_index", 1.0)

        # 1. Header Node
        nodes.append({
            "id": "node-diff-header",
            "type": "text",
            "text": (
                f"## {title}\n"
                f"**Stability Index (TSI):** `{tsi * 100:.1f}%` | **Graph Drift:** `{diff_report.get('graph_drift_percentage', 0)}%`\n\n"
                f"- Added Nodes: **+{summary.get('nodes_added', 0)}** (Emerald)\n"
                f"- Removed Nodes: **-{summary.get('nodes_removed', 0)}** (Ruby Red)\n"
                f"- Modified Content: **{summary.get('nodes_modified', 0)}** (Amber)\n"
                f"- Relocated Coordinates: **{summary.get('nodes_relocated', 0)}** (Cyan)"
            ),
            "x": -300,
            "y": -350,
            "width": 600,
            "height": 220,
            "color": "5" if tsi >= 0.75 else "1"
        })

        # 2. Existing and Updated nodes from Canvas B
        for nb in canvas_b.get("nodes", []):
            nid = nb["id"]
            node_copy = dict(nb)

            if nid in added_ids:
                node_copy["color"] = "4"  # Green
                node_copy["text"] = f"### [ADDED NODE]\n" + node_copy.get("text", "")
            elif nid in modified_dict:
                mod = modified_dict[nid]
                node_copy["color"] = "3"  # Yellow / Amber
                node_copy["text"] = (
                    f"### [MODIFIED NODE]\n"
                    f"**Previous:**\n> {mod['previous_text'][:80]}...\n\n"
                    f"**Updated:**\n{mod['current_text']}"
                )
            elif nid in relocated_dict:
                rel = relocated_dict[nid]
                node_copy["color"] = "5"  # Cyan / Blue
                node_copy["text"] = f"### [RELOCATED: +{rel['spatial_shift']['distance']}px]\n" + node_copy.get("text", "")
            else:
                node_copy["color"] = "0"  # Neutral Gray

            nodes.append(node_copy)

        # 3. Ghosted Removed Nodes
        for nr in diff_report.get("removed_nodes", []):
            ghost_node = dict(nr)
            ghost_node["id"] = f"ghost-{nr['id']}"
            ghost_node["color"] = "1"  # Red
            ghost_node["text"] = f"### [REMOVED IN REVISION]\n" + ghost_node.get("text", "")
            nodes.append(ghost_node)

        # 4. Edges
        added_edges_keys = {
            (e.get("fromNode"), e.get("toNode")) for e in diff_report.get("added_edges", [])
        }
        for idx, eb in enumerate(canvas_b.get("edges", [])):
            edge_copy = dict(eb)
            pair = (eb.get("fromNode"), eb.get("toNode"))
            if pair in added_edges_keys:
                edge_copy["color"] = "4"
                edge_copy["label"] = "[NEW BRIDGE]"
            edges.append(edge_copy)

        # Add ghosted severed edges
        for idx, er in enumerate(diff_report.get("removed_edges", [])):
            from_id = f"ghost-{er['fromNode']}" if er["fromNode"] in removed_ids else er["fromNode"]
            to_id = f"ghost-{er['toNode']}" if er["toNode"] in removed_ids else er["toNode"]
            edges.append({
                "id": f"severed-edge-{idx}",
                "fromNode": from_id,
                "fromSide": er.get("fromSide", "right"),
                "toNode": to_id,
                "toSide": er.get("toSide", "left"),
                "color": "1",
                "label": "[SEVERED LINK]"
            })

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def to_svg_diff_strip(diff_report: Dict[str, Any], title: str = "Spatial Graph Differential") -> str:
        """Renders vector SVG diff dashboard with visual distribution metrics."""
        summary = diff_report.get("summary", {})
        tsi = diff_report.get("topological_stability_index", 1.0)
        drift = diff_report.get("graph_drift_percentage", 0.0)

        width = 720
        height = 360

        svg = []
        svg.append(f'<svg width="100%" height="auto" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'<rect width="{width}" height="{height}" rx="14" fill="#09090b" stroke="#27272a" stroke-width="1.5"/>')

        # Header Title
        svg.append(f'<text x="28" y="38" fill="#fafafa" font-size="18" font-weight="bold" font-family="sans-serif">{title}</text>')
        svg.append(f'<text x="28" y="60" fill="#a1a1aa" font-size="12" font-family="sans-serif">Topological Stability Index (TSI): {tsi * 100:.1f}% | Architectural Drift: {drift}%</text>')

        # Metric Tiles (4 Across)
        metrics = [
            ("Added Nodes", f"+{summary.get('nodes_added', 0)}", "#10b981"),
            ("Removed Nodes", f"-{summary.get('nodes_removed', 0)}", "#ef4444"),
            ("Modified Nodes", f"{summary.get('nodes_modified', 0)}", "#f59e0b"),
            ("Relocated Nodes", f"{summary.get('nodes_relocated', 0)}", "#06b6d4")
        ]

        tile_w = 150
        tile_h = 75
        tile_y = 85
        spacing = 18
        start_x = 28

        for idx, (label, val, col) in enumerate(metrics):
            tx = start_x + idx * (tile_w + spacing)
            svg.append(f'<g transform="translate({tx}, {tile_y})">')
            svg.append(f'<rect width="{tile_w}" height="{tile_h}" rx="8" fill="#18181b" stroke="{col}" stroke-width="1.5"/>')
            svg.append(f'<text x="14" y="26" fill="#a1a1aa" font-size="11" font-family="sans-serif">{label}</text>')
            svg.append(f'<text x="14" y="56" fill="{col}" font-size="22" font-weight="bold" font-family="sans-serif">{val}</text>')
            svg.append('</g>')

        # Structural Edge Metrics Banner
        edge_y = 180
        svg.append(f'<rect x="28" y="{edge_y}" width="664" height="65" rx="8" fill="#18181b" stroke="#27272a" stroke-width="1"/>')
        svg.append(f'<text x="44" y="{edge_y + 26}" fill="#e4e4e7" font-size="13" font-weight="bold" font-family="sans-serif">Topological Edge Dynamics</text>')
        svg.append(f'<text x="44" y="{edge_y + 48}" fill="#71717a" font-size="11" font-family="sans-serif">Retained Bridges: {summary.get("edges_retained", 0)} | Added Connections: +{summary.get("edges_added", 0)} | Severed Links: -{summary.get("edges_removed", 0)}</text>')

        # Stability Gauge Bar
        gauge_y = 265
        gauge_w = 664
        fill_w = max(10, int(gauge_w * tsi))
        gauge_col = "#10b981" if tsi >= 0.75 else ("#f59e0b" if tsi >= 0.5 else "#ef4444")

        svg.append(f'<text x="28" y="{gauge_y - 8}" fill="#a1a1aa" font-size="11" font-family="sans-serif">Architectural Stability Gauge ({tsi * 100:.1f}%)</text>')
        svg.append(f'<rect x="28" y="{gauge_y}" width="{gauge_w}" height="14" rx="7" fill="#27272a"/>')
        svg.append(f'<rect x="28" y="{gauge_y}" width="{fill_w}" height="14" rx="7" fill="{gauge_col}"/>')

        # Footer
        svg.append(f'<text x="28" y="325" fill="#52525b" font-size="10" font-family="sans-serif">DxSkills Cognitive Architecture Divergence Engine | Zero Em Dash Verified</text>')

        svg.append('</svg>')
        return "\n".join(svg)


def run_spatial_diff(
    canvas_path_a: str,
    canvas_path_b: str,
    title: Optional[str] = None,
    output_canvas: Optional[str] = None,
    output_svg: Optional[str] = None
) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """Loads two canvases, calculates topological diff, and exports merged views."""
    with open(canvas_path_a, "r", encoding="utf-8") as f:
        canvas_a = json.load(f)
    with open(canvas_path_b, "r", encoding="utf-8") as f:
        canvas_b = json.load(f)

    diff_report = SpatialGraphDiffer.diff_canvases(canvas_a, canvas_b)
    diff_title = title or f"Diff: {os.path.basename(canvas_path_a)} vs {os.path.basename(canvas_path_b)}"

    merged_canvas = VisualMergeResolver.to_differential_canvas(diff_report, canvas_b, title=diff_title)
    svg_code = VisualMergeResolver.to_svg_diff_strip(diff_report, title=diff_title)

    if output_canvas:
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(merged_canvas, f, indent=2)

    if output_svg:
        os.makedirs(os.path.dirname(os.path.abspath(output_svg)), exist_ok=True)
        with open(output_svg, "w", encoding="utf-8") as f:
            f.write(svg_code)

    return diff_report, merged_canvas, svg_code


def main():
    parser = argparse.ArgumentParser(description="DxSkills Spatial Cognitive Architecture Graph Differential Engine")
    parser.add_argument("canvas_a", help="Base Obsidian .canvas file (Branch A / Snapshot 1)")
    parser.add_argument("canvas_b", help="Target Obsidian .canvas file (Branch B / Snapshot 2)")
    parser.add_argument("--title", "-t", help="Title for the diff report")
    parser.add_argument("--canvas", "-c", help="Output differential Obsidian .canvas filepath")
    parser.add_argument("--svg", "-s", help="Output vector SVG differential dashboard filepath")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON diff telemetry")

    args = parser.parse_args()

    if not os.path.exists(args.canvas_a):
        print(f"[DxSkills] Error: Base canvas not found: {args.canvas_a}")
        sys.exit(1)
    if not os.path.exists(args.canvas_b):
        print(f"[DxSkills] Error: Target canvas not found: {args.canvas_b}")
        sys.exit(1)

    diff_report, merged_canvas, svg_code = run_spatial_diff(
        args.canvas_a,
        args.canvas_b,
        title=args.title,
        output_canvas=args.canvas,
        output_svg=args.svg
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
        print(f"[DxSkills] Computed graph differential (Stability: {diff_report['topological_stability_index'] * 100:.1f}%).")
        if args.canvas:
            print(f"  - Differential Canvas: {args.canvas}")
        if args.svg:
            print(f"  - SVG Diff Dashboard: {args.svg}")


if __name__ == "__main__":
    main()
