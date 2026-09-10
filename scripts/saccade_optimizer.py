#!/usr/bin/env python3
"""
Autonomous Cognitive Spatial Working Memory Saccade & Visual Glance Path Optimizer
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Simulates ocular glance trajectories, saccadic jump amplitudes, and visual
crowding across 2D Obsidian Canvas node graphs. Repositions node topologies
into smooth, low-friction ocular pathways that eliminate visual crowding,
minimize high-amplitude eye fatigue, and preserve cognitive working memory.

Core Principles:
- Saccadic Amplitude Minimization: Reduces wide erratic eye jumps across canvas whitespace.
- Visual Crowding Alleviation: Eliminates overlapping node interference and optical clutter.
- Serpentine Flow Harmony: Establishes predictable left-to-right cognitive sweep vectors.
"""

import os
import re
import math
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


@dataclass
class FixationNode:
    """Represents a spatial visual target or canvas node."""
    node_id: str
    x: int
    y: int
    width: int
    height: int
    text: str = ""
    color: str = "1"
    center_x: float = field(init=False)
    center_y: float = field(init=False)

    def __post_init__(self):
        self.center_x = self.x + (self.width / 2.0)
        self.center_y = self.y + (self.height / 2.0)


@dataclass
class SaccadeMetrics:
    """Quantifies ocular jump distance, direction changes, and cognitive fatigue."""
    total_path_distance: float
    avg_jump_distance: float
    max_jump_distance: float
    angular_deviation_deg: float
    regression_count: int
    crowding_violations: int
    cognitive_fatigue_score: float  # 0 to 100 scale (lower is better)


class SaccadeGlancePathOptimizer:
    """Simulates eye-tracking scanpaths and optimizes canvas layouts for ocular comfort."""

    def __init__(self):
        self.nodes: Dict[str, FixationNode] = {}
        self.edges: List[Dict[str, Any]] = []

    def load_canvas_data(self, canvas_data: Dict[str, Any]):
        """Load nodes and edges from Obsidian .canvas JSON structure."""
        self.nodes = {}
        self.edges = canvas_data.get("edges", [])
        for n in canvas_data.get("nodes", []):
            if n.get("type") == "text" or "text" in n:
                f_node = FixationNode(
                    node_id=n.get("id", f"node_{len(self.nodes)}"),
                    x=int(n.get("x", 0)),
                    y=int(n.get("y", 0)),
                    width=int(n.get("width", 260)),
                    height=int(n.get("height", 160)),
                    text=n.get("text", ""),
                    color=str(n.get("color", "1"))
                )
                self.nodes[f_node.node_id] = f_node

    def compute_scanpath(self, nodes: Optional[Dict[str, FixationNode]] = None) -> List[FixationNode]:
        """
        Simulate human gaze reading trajectory across the 2D layout.
        Uses topological edge flow where available, falling back to top-down,
        left-to-right reading order (hierarchical sweep).
        """
        target_nodes = nodes or self.nodes
        if not target_nodes:
            return []

        # Build in-degree map from edges
        in_degree: Dict[str, int] = {nid: 0 for nid in target_nodes}
        adjacency: Dict[str, List[str]] = {nid: [] for nid in target_nodes}

        for edge in self.edges:
            src = edge.get("fromNode")
            dst = edge.get("toNode")
            if src in target_nodes and dst in target_nodes:
                adjacency[src].append(dst)
                in_degree[dst] += 1

        # If directed graph has clear roots, use topological breadth-first traversal
        roots = [nid for nid, deg in in_degree.items() if deg == 0]
        if roots and len(roots) < len(target_nodes):
            # Sort roots spatially by y then x
            roots.sort(key=lambda nid: (target_nodes[nid].y, target_nodes[nid].x))
            visited: Set[str] = set()
            scanpath: List[FixationNode] = []
            queue = list(roots)

            for r in queue:
                if r not in visited:
                    visited.add(r)
                    scanpath.append(target_nodes[r])
                    for child in adjacency[r]:
                        if child not in visited:
                            queue.append(child)

            # Append any unconnected nodes in spatial order
            remaining = [target_nodes[nid] for nid in target_nodes if nid not in visited]
            remaining.sort(key=lambda n: (n.y, n.x))
            scanpath.extend(remaining)
            return scanpath

        # Natural reading sweep: sort primarily by vertical band (y // 150), then by x
        sorted_nodes = sorted(
            target_nodes.values(),
            key=lambda n: (round(n.center_y / 160.0), n.center_x)
        )
        return sorted_nodes

    def evaluate_metrics(self, scanpath: List[FixationNode]) -> SaccadeMetrics:
        """Calculate ocular jump distances, angular churn, regressions, and fatigue score."""
        if len(scanpath) < 2:
            return SaccadeMetrics(
                total_path_distance=0.0,
                avg_jump_distance=0.0,
                max_jump_distance=0.0,
                angular_deviation_deg=0.0,
                regression_count=0,
                crowding_violations=0,
                cognitive_fatigue_score=10.0
            )

        total_dist = 0.0
        max_dist = 0.0
        vectors: List[Tuple[float, float]] = []
        regressions = 0

        for i in range(len(scanpath) - 1):
            curr = scanpath[i]
            nxt = scanpath[i + 1]

            dx = nxt.center_x - curr.center_x
            dy = nxt.center_y - curr.center_y
            dist = math.hypot(dx, dy)

            total_dist += dist
            if dist > max_dist:
                max_dist = dist

            vectors.append((dx, dy))

            # Backward regression: jump backwards horizontally on same or earlier vertical band
            if dx < -80 and dy <= 40:
                regressions += 1

        avg_dist = total_dist / max(len(scanpath) - 1, 1)

        # Angular churn: sum of directional angle changes between successive saccades
        angular_churn = 0.0
        for i in range(len(vectors) - 1):
            v1 = vectors[i]
            v2 = vectors[i + 1]
            mag1 = math.hypot(v1[0], v1[1])
            mag2 = math.hypot(v2[0], v2[1])
            if mag1 > 0 and mag2 > 0:
                dot = (v1[0] * v2[0] + v1[1] * v2[1]) / (mag1 * mag2)
                dot_clamped = max(-1.0, min(1.0, dot))
                angle_rad = math.acos(dot_clamped)
                angular_churn += math.degrees(angle_rad)

        avg_angle_dev = angular_churn / max(len(vectors) - 1, 1) if len(vectors) > 1 else 0.0

        # Visual crowding check: count node pairs spaced closer than 30px (optical interference)
        crowding = 0
        node_list = list(scanpath)
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                na = node_list[i]
                nb = node_list[j]
                # Horizontal and vertical overlaps with small margin
                h_overlap = (na.x < nb.x + nb.width + 30) and (na.x + na.width + 30 > nb.x)
                v_overlap = (na.y < nb.y + nb.height + 30) and (na.y + na.height + 30 > nb.y)
                if h_overlap and v_overlap:
                    crowding += 1

        # Cognitive Fatigue Score (0 to 100):
        # Weighted combination of average jump distance (comfortable range 200-400px),
        # angular deviation (higher churn = more ocular disorientation),
        # regression count, and crowding penalty.
        jump_penalty = min(40.0, (avg_dist / 600.0) * 40.0)
        angle_penalty = min(30.0, (avg_angle_dev / 180.0) * 30.0)
        regr_penalty = min(20.0, regressions * 8.0)
        crowd_penalty = min(10.0, crowding * 5.0)

        fatigue_score = round(min(100.0, jump_penalty + angle_penalty + regr_penalty + crowd_penalty), 1)

        return SaccadeMetrics(
            total_path_distance=round(total_dist, 1),
            avg_jump_distance=round(avg_dist, 1),
            max_jump_distance=round(max_dist, 1),
            angular_deviation_deg=round(avg_angle_dev, 1),
            regression_count=regressions,
            crowding_violations=crowding,
            cognitive_fatigue_score=fatigue_score
        )

    def optimize_layout(self, cols: int = 3, gutter_x: int = 60, gutter_y: int = 80) -> Dict[str, FixationNode]:
        """
        Repack and reposition nodes into a low-fatigue serpentine grid layout.
        Nodes alternate directions between rows (serpentine sweep) so ocular return
        jumps are smooth and continuous rather than jumping all the way back.
        """
        scanpath = self.compute_scanpath()
        if not scanpath:
            return {}

        optimized_nodes: Dict[str, FixationNode] = {}
        total_items = len(scanpath)

        for idx, node in enumerate(scanpath):
            row = idx // cols
            col = idx % cols

            # Serpentine alignment: even rows left-to-right, odd rows right-to-left
            if row % 2 == 1:
                effective_col = (cols - 1) - col
            else:
                effective_col = col

            new_x = effective_col * (node.width + gutter_x)
            new_y = row * (node.height + gutter_y)

            opt_node = FixationNode(
                node_id=node.node_id,
                x=new_x,
                y=new_y,
                width=node.width,
                height=node.height,
                text=node.text,
                color=node.color
            )
            optimized_nodes[opt_node.node_id] = opt_node

        return optimized_nodes

    def export_canvas(self, optimized_nodes: Dict[str, FixationNode]) -> Dict[str, Any]:
        """Export optimized nodes into standard Obsidian .canvas JSON format."""
        canvas_nodes = []
        for n in optimized_nodes.values():
            canvas_nodes.append({
                "id": n.node_id,
                "type": "text",
                "text": n.text,
                "x": n.x,
                "y": n.y,
                "width": n.width,
                "height": n.height,
                "color": n.color
            })
        return {
            "nodes": canvas_nodes,
            "edges": self.edges
        }

    def export_scanpath_svg(self, scanpath: List[FixationNode], width: int = 1000, height: int = 650) -> str:
        """Generate a visual ocular scanpath overlay SVG showing glance order and jumps."""
        if not scanpath:
            return '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50"></svg>'

        # Determine bounding box
        min_x = min(n.x for n in scanpath)
        min_y = min(n.y for n in scanpath)
        max_x = max(n.x + n.width for n in scanpath)
        max_y = max(n.y + n.height for n in scanpath)

        view_w = max(max_x - min_x + 120, 800)
        view_h = max(max_y - min_y + 120, 500)
        offset_x = -min_x + 60
        offset_y = -min_y + 60

        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" width="100%" height="100%">',
            f'  <defs>',
            f'    <marker id="saccade-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
            f'      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />',
            f'    </marker>',
            f'  </defs>',
            f'  <rect width="{view_w}" height="{view_h}" fill="#09090b" rx="16" />',
            f'  <!-- Canvas Target Nodes -->',
        ]

        # Draw nodes
        for n in scanpath:
            nx = n.x + offset_x
            ny = n.y + offset_y
            safe_text = n.text.split("\n")[0][:22].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg_lines.append(f'  <rect x="{nx}" y="{ny}" width="{n.width}" height="{n.height}" rx="8" fill="#18181b" stroke="#27272a" stroke-width="1.5" />')
            svg_lines.append(f'  <text x="{nx + 14}" y="{ny + 30}" fill="#f4f4f5" font-size="12" font-weight="600" font-family="sans-serif">{safe_text}</text>')

        # Draw saccadic glance vectors
        svg_lines.append(f'  <!-- Saccadic Eye Scanpath Trajectory -->')
        for i in range(len(scanpath) - 1):
            curr = scanpath[i]
            nxt = scanpath[i + 1]
            x1 = curr.center_x + offset_x
            y1 = curr.center_y + offset_y
            x2 = nxt.center_x + offset_x
            y2 = nxt.center_y + offset_y
            svg_lines.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#saccade-arrow)" />')

        # Draw fixation numbered badges
        for idx, n in enumerate(scanpath, 1):
            cx = n.center_x + offset_x
            cy = n.center_y + offset_y
            svg_lines.append(f'  <circle cx="{cx}" cy="{cy}" r="16" fill="#0284c7" stroke="#ffffff" stroke-width="2" />')
            svg_lines.append(f'  <text x="{cx}" y="{cy + 4}" fill="#ffffff" font-size="11" font-weight="800" font-family="sans-serif" text-anchor="middle">{idx}</text>')

        svg_lines.append('</svg>')
        return "\n".join(svg_lines)

    @classmethod
    def export_audit_summary(cls, orig: SaccadeMetrics, opt: SaccadeMetrics) -> str:
        """Export comparative markdown audit summary of saccadic optimization."""
        dist_change = round(((orig.total_path_distance - opt.total_path_distance) / max(orig.total_path_distance, 1.0)) * 100, 1)
        fatigue_reduction = round(((orig.cognitive_fatigue_score - opt.cognitive_fatigue_score) / max(orig.cognitive_fatigue_score, 0.1)) * 100, 1)

        return (
            f"# Saccadic Eye-Tracking & Glance Path Optimization Audit\n\n"
            f"**Cognitive Fatigue Reduction:** {fatigue_reduction}% improvement\n"
            f"**Total Ocular Travel Distance Reduction:** {dist_change}%\n\n"
            f"| Metric | Original Layout | Optimized Serpentine Layout | Delta |\n"
            f"| :--- | :--- | :--- | :--- |\n"
            f"| **Cognitive Fatigue Score** | `{orig.cognitive_fatigue_score}/100` | `{opt.cognitive_fatigue_score}/100` | **-{fatigue_reduction}%** |\n"
            f"| **Total Ocular Travel** | `{orig.total_path_distance} px` | `{opt.total_path_distance} px` | **-{dist_change}%** |\n"
            f"| **Average Jump Amplitude** | `{orig.avg_jump_distance} px` | `{opt.avg_jump_distance} px` | `{round(opt.avg_jump_distance - orig.avg_jump_distance, 1)} px` |\n"
            f"| **Max Saccade Leap** | `{orig.max_jump_distance} px` | `{opt.max_jump_distance} px` | `{round(opt.max_jump_distance - orig.max_jump_distance, 1)} px` |\n"
            f"| **Angular Churn Deviation** | `{orig.angular_deviation_deg}°` | `{opt.angular_deviation_deg}°` | `{round(opt.angular_deviation_deg - orig.angular_deviation_deg, 1)}°` |\n"
            f"| **Backward Regressions** | `{orig.regression_count}` | `{opt.regression_count}` | **{opt.regression_count - orig.regression_count}** |\n"
            f"| **Crowding Collisions** | `{orig.crowding_violations}` | `{opt.crowding_violations}` | **{opt.crowding_violations - orig.crowding_violations}** |\n"
        )


def main():
    """Quick CLI tester."""
    print("SaccadeGlancePathOptimizer Loaded.")


if __name__ == "__main__":
    main()
