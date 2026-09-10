#!/usr/bin/env python3
"""
Autonomous Cognitive Non-Linear Narrative Branching Simulator & Plot Mesh
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Provides non-linear storyline dependency graph parsing, causal plot branch tracking,
narrative pacing telemetry, and 2D Obsidian Canvas timeline visualization for
spatial, screenwriting, and game design thinkers.

Core Principles:
- Eide & Eide I-Strength & N-Strength: Interconnected causality and narrative reasoning.
- Spatial-First Plot Topologies: Disentangles complex timelines across visual axes.
- Zero Phonological Friction: Replaces linear outline lock-in with dynamic causal nodes.
"""

import os
import re
import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


@dataclass
class NarrativeBeat:
    """Individual narrative beat, scene, or plot milestone."""
    id: str
    title: str
    character: str
    tension_level: float  # 0.0 to 100.0
    act: str  # e.g. "Act 1", "Act 2", "Act 3"
    description: str = ""
    tags: List[str] = field(default_factory=list)
    timeline_col: int = 0
    branch_row: int = 0
    is_terminal: bool = False


@dataclass
class PlotBranch:
    """Causal consequence or decision edge connecting narrative beats."""
    branch_id: str
    source_id: str
    target_id: str
    condition: str = ""
    consequence: str = ""
    is_canonical: bool = True


@dataclass
class NarrativeAudit:
    """Telemetry describing narrative pacing, agency, and plot cohesion."""
    total_beats: int
    total_branches: int
    characters_count: int
    dangling_threads_count: int
    pacing_bottlenecks_count: int
    narrative_agency_score: float  # 0.0 to 100.0 (branching diversity)
    average_tension: float


class NarrativeBranchingSimulator:
    """Parses, simulates, and visualizes non-linear narrative plot meshes."""

    # Color palette mapped to narrative acts for Obsidian canvas
    ACT_COLORS = {
        "Act 1": "4",       # Obsidian green/emerald
        "Act 2": "2",       # Obsidian yellow/amber
        "Act 3": "1",       # Obsidian red/rose
        "Epilogue": "5",    # Obsidian cyan/blue
        "Prologue": "6",    # Obsidian purple
        "Alternative": "3"  # Obsidian orange
    }

    def __init__(self):
        self.beats: Dict[str, NarrativeBeat] = {}
        self.branches: List[PlotBranch] = []
        self._next_beat_idx = 1
        self._next_branch_idx = 1

    def add_beat(
        self,
        title: str,
        character: str = "Protagonist",
        tension_level: float = 50.0,
        act: str = "Act 1",
        description: str = "",
        tags: Optional[List[str]] = None,
        beat_id: Optional[str] = None,
        is_terminal: bool = False
    ) -> NarrativeBeat:
        """Add a narrative beat to the plot mesh."""
        bid = beat_id or f"beat-{self._next_beat_idx}"
        self._next_beat_idx += 1
        clamped_tension = max(0.0, min(100.0, float(tension_level)))
        beat = NarrativeBeat(
            id=bid,
            title=title.strip(),
            character=character.strip() or "Protagonist",
            tension_level=clamped_tension,
            act=act.strip() or "Act 1",
            description=description.strip(),
            tags=tags or [],
            is_terminal=is_terminal
        )
        self.beats[bid] = beat
        return beat

    def add_branch(
        self,
        source_id: str,
        target_id: str,
        condition: str = "",
        consequence: str = "",
        is_canonical: bool = True
    ) -> PlotBranch:
        """Add a causal plot branch between two narrative beats."""
        brid = f"branch-{self._next_branch_idx}"
        self._next_branch_idx += 1
        branch = PlotBranch(
            branch_id=brid,
            source_id=source_id,
            target_id=target_id,
            condition=condition.strip(),
            consequence=consequence.strip(),
            is_canonical=is_canonical
        )
        self.branches.append(branch)
        return branch

    def parse_markdown_storyline(self, text: str) -> None:
        """
        Parse non-linear storylines from structured markdown text.
        Supports beat headers and branch arrows:
        ### Beat: Inception
        - Character: Dr. Elena Vance
        - Tension: 65
        - Act: Act 1
        - Description: Discovery of deep spatial anomaly.
        - Leads To: Confrontation | Condition: If sensor calibrated | Consequence: Telemetry locked
        """
        current_beat: Optional[NarrativeBeat] = None
        pending_branches: List[Tuple[str, str, str, str]] = []  # (src_id, target_title, cond, cons)

        lines = text.splitlines()
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            # Beat declaration: ### Beat: Title OR [Beat: Title]
            beat_match = re.match(r'^(?:#{1,4}\s*Beat:\s*|\[Beat:\s*)([^\]\n]+)\]?', line, re.IGNORECASE)
            if beat_match:
                title = beat_match.group(1).strip()
                current_beat = self.add_beat(title=title)
                continue

            if current_beat:
                # Character attribute
                char_match = re.match(r'^[-\*]\s*Character:\s*(.+)$', line, re.IGNORECASE)
                if char_match:
                    current_beat.character = char_match.group(1).strip()
                    continue

                # Tension attribute
                tension_match = re.match(r'^[-\*]\s*Tension:\s*(\d+(?:\.\d+)?)$', line, re.IGNORECASE)
                if tension_match:
                    current_beat.tension_level = max(0.0, min(100.0, float(tension_match.group(1))))
                    continue

                # Act attribute
                act_match = re.match(r'^[-\*]\s*Act:\s*(.+)$', line, re.IGNORECASE)
                if act_match:
                    current_beat.act = act_match.group(1).strip()
                    continue

                # Description attribute
                desc_match = re.match(r'^[-\*]\s*Description:\s*(.+)$', line, re.IGNORECASE)
                if desc_match:
                    current_beat.description = desc_match.group(1).strip()
                    continue

                # Terminal flag
                if re.match(r'^[-\*]\s*(?:Terminal|End|Resolution):\s*(?:true|yes)', line, re.IGNORECASE):
                    current_beat.is_terminal = True
                    continue

                # Branch declaration: Leads To: Target Title | Condition: X | Consequence: Y
                branch_match = re.match(r'^[-\*]\s*(?:Leads\s*To|->|Branch):\s*([^\|]+)(?:\|\s*Condition:\s*([^\|]+))?(?:\|\s*Consequence:\s*(.+))?$', line, re.IGNORECASE)
                if branch_match:
                    target_title = branch_match.group(1).strip()
                    cond = (branch_match.group(2) or "").strip()
                    cons = (branch_match.group(3) or "").strip()
                    pending_branches.append((current_beat.id, target_title, cond, cons))
                    continue

        # Resolve branch targets by beat title or ID
        title_to_id = {b.title.lower(): b.id for b in self.beats.values()}
        for src_id, target_title, cond, cons in pending_branches:
            target_key = target_title.lower()
            if target_key in title_to_id:
                self.add_branch(src_id, title_to_id[target_key], condition=cond, consequence=cons)
            elif target_title in self.beats:
                self.add_branch(src_id, target_title, condition=cond, consequence=cons)

    def audit_narrative(self) -> NarrativeAudit:
        """Perform comprehensive pacing, branch connectivity, and narrative agency audit."""
        total_beats = len(self.beats)
        total_branches = len(self.branches)
        if total_beats == 0:
            return NarrativeAudit(0, 0, 0, 0, 0, 0.0, 0.0)

        characters = {b.character for b in self.beats.values()}

        # Identify source and target connection counts
        outgoing_counts: Dict[str, int] = {bid: 0 for bid in self.beats}
        incoming_counts: Dict[str, int] = {bid: 0 for bid in self.beats}
        for br in self.branches:
            if br.source_id in outgoing_counts:
                outgoing_counts[br.source_id] += 1
            if br.target_id in incoming_counts:
                incoming_counts[br.target_id] += 1

        # Dangling threads: non-terminal beats with 0 outgoing branches
        dangling = sum(
            1 for bid, beat in self.beats.items()
            if not beat.is_terminal and outgoing_counts.get(bid, 0) == 0
        )

        # Pacing bottlenecks: beats with excessive convergence (>= 3 incoming) or stagnant tension
        bottlenecks = sum(
            1 for bid, inc in incoming_counts.items()
            if inc >= 3
        )

        # Average tension level
        tensions = [b.tension_level for b in self.beats.values()]
        avg_tension = sum(tensions) / float(total_beats)

        # Narrative Agency Score: measures branch choice density vs total beats (up to 100.0)
        # Ratio of branch choices per beat, penalized by dangling threads
        branch_ratio = (total_branches / float(max(1, total_beats)))
        agency = min(100.0, max(10.0, (branch_ratio * 45.0) + (len(characters) * 8.0) - (dangling * 5.0)))

        return NarrativeAudit(
            total_beats=total_beats,
            total_branches=total_branches,
            characters_count=len(characters),
            dangling_threads_count=dangling,
            pacing_bottlenecks_count=bottlenecks,
            narrative_agency_score=round(agency, 1),
            average_tension=round(avg_tension, 1)
        )

    def _compute_topological_layout(self) -> None:
        """Assign 2D spatial grid coordinates (col = timeline step, row = character/branch line)."""
        if not self.beats:
            return

        # Simple topological layering using longest path from root nodes
        incoming_counts: Dict[str, int] = {bid: 0 for bid in self.beats}
        outgoing_map: Dict[str, List[str]] = {bid: [] for bid in self.beats}
        for br in self.branches:
            if br.target_id in incoming_counts:
                incoming_counts[br.target_id] += 1
            if br.source_id in outgoing_map:
                outgoing_map[br.source_id].append(br.target_id)

        # Root beats have 0 incoming edges
        roots = [bid for bid, count in incoming_counts.items() if count == 0]
        if not roots:
            roots = list(self.beats.keys())[:1]

        # BFS / Layering
        levels: Dict[str, int] = {}
        for r in roots:
            levels[r] = 0

        queue = list(roots)
        while queue:
            curr = queue.pop(0)
            curr_lvl = levels.get(curr, 0)
            for nxt in outgoing_map.get(curr, []):
                if nxt not in levels or levels[nxt] < curr_lvl + 1:
                    levels[nxt] = curr_lvl + 1
                    queue.append(nxt)

        # For disconnected nodes, assign progressive levels
        max_lvl = max(levels.values()) if levels else 0
        for bid in self.beats:
            if bid not in levels:
                max_lvl += 1
                levels[bid] = max_lvl

        # Assign rows based on distinct characters or parallel branches
        char_rows: Dict[str, int] = {}
        row_counter = 0
        for b in self.beats.values():
            if b.character not in char_rows:
                char_rows[b.character] = row_counter
                row_counter += 1

        # Save coordinates to beats
        for bid, beat in self.beats.items():
            beat.timeline_col = levels.get(bid, 0)
            beat.branch_row = char_rows.get(beat.character, 0)

    def export_canvas(self) -> Dict[str, Any]:
        """Export narrative plot mesh into Obsidian .canvas JSON topology."""
        self._compute_topological_layout()

        node_width = 320
        node_height = 200
        col_spacing = 420
        row_spacing = 300
        origin_x = 100
        origin_y = 100

        nodes = []
        for bid, beat in self.beats.items():
            x = origin_x + (beat.timeline_col * col_spacing)
            y = origin_y + (beat.branch_row * row_spacing)

            act_clean = beat.act.split(":")[0].strip()
            color = self.ACT_COLORS.get(act_clean, "3")

            tags_str = " ".join([f"#{t}" for t in beat.tags]) if beat.tags else ""
            tension_bar = "[" + "=" * int(beat.tension_level // 10) + " " * (10 - int(beat.tension_level // 10)) + "]"

            text_lines = [
                f"### {beat.title}",
                f"**Character:** {beat.character} | **Act:** {beat.act}",
                f"**Tension:** {beat.tension_level}% `{tension_bar}`",
                f"",
                f"{beat.description if beat.description else 'Story beat milestone.'}",
            ]
            if tags_str:
                text_lines.append(f"\n{tags_str}")
            if beat.is_terminal:
                text_lines.append("\n**Status:** [Storyline Resolution]")

            nodes.append({
                "id": bid,
                "type": "text",
                "text": "\n".join(text_lines),
                "x": x,
                "y": y,
                "width": node_width,
                "height": node_height,
                "color": color
            })

        edges = []
        for br in self.branches:
            label_parts = []
            if br.condition:
                label_parts.append(f"If: {br.condition}")
            if br.consequence:
                label_parts.append(f"-> {br.consequence}")
            edge_label = " | ".join(label_parts)

            edge_data: Dict[str, Any] = {
                "id": br.branch_id,
                "fromNode": br.source_id,
                "fromSide": "right",
                "toNode": br.target_id,
                "toSide": "left"
            }
            if edge_label:
                edge_data["label"] = edge_label
            if not br.is_canonical:
                edge_data["color"] = "3"  # Distinct color for alternative reality branch

            edges.append(edge_data)

        return {
            "nodes": nodes,
            "edges": edges
        }

    def export_svg(self, width: int = 1100, height: int = 650) -> str:
        """Export 2D interactive narrative plot mesh vector SVG visualization."""
        self._compute_topological_layout()
        audit = self.audit_narrative()

        def safe_xml(s: str) -> str:
            return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            f'  <rect width="{width}" height="{height}" fill="#09090b" rx="16" />',
            f'  <!-- Header -->',
            f'  <text x="30" y="40" fill="#ffffff" font-size="16" font-weight="700" font-family="sans-serif">Non-Linear Narrative Branching Simulator &amp; Plot Mesh</text>',
            f'  <text x="30" y="60" fill="#a1a1aa" font-size="11" font-family="sans-serif">Beats: {audit.total_beats} | Branches: {audit.total_branches} | Agency Score: {audit.narrative_agency_score}/100 | Dangling Threads: {audit.dangling_threads_count}</text>',
            f'  <!-- Tension Waveform Background -->',
            f'  <rect x="30" y="80" width="{width - 60}" height="100" rx="10" fill="#18181b" stroke="#27272a" stroke-width="1" />',
            f'  <text x="45" y="100" fill="#71717a" font-size="10" font-weight="700" font-family="sans-serif">DRAMATIC TENSION PROFILE (AVERAGE: {audit.average_tension}%)</text>'
        ]

        # Draw tension curve
        sorted_beats = sorted(self.beats.values(), key=lambda b: (b.timeline_col, b.branch_row))
        if sorted_beats:
            step_x = (width - 120) / float(max(1, len(sorted_beats) - 1))
            points = []
            for idx, b in enumerate(sorted_beats):
                px = 60 + (idx * step_x)
                py = 160 - (b.tension_level * 0.6)
                points.append(f"{px:.1f},{py:.1f}")
                # Dot
                svg.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#38bdf8" />')
                svg.append(f'  <text x="{px:.1f}" y="{py - 8:.1f}" fill="#94a3b8" font-size="8" text-anchor="middle" font-family="sans-serif">{int(b.tension_level)}%</text>')

            if len(points) > 1:
                poly_str = " ".join(points)
                svg.append(f'  <polyline points="{poly_str}" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,2" />')

        # Draw Narrative Beat Cards
        card_start_y = 200
        cols = max(1, max((b.timeline_col for b in self.beats.values()), default=0) + 1)
        rows = max(1, max((b.branch_row for b in self.beats.values()), default=0) + 1)

        c_w = min(220, int((width - 120) / max(1, cols)))
        c_h = min(110, int((height - card_start_y - 60) / max(1, rows)))
        gap_x = int((width - 80 - (cols * c_w)) / max(1, cols))
        gap_y = 30

        pos_map: Dict[str, Tuple[int, int]] = {}
        for bid, b in self.beats.items():
            bx = 40 + (b.timeline_col * (c_w + max(20, gap_x)))
            by = card_start_y + (b.branch_row * (c_h + gap_y))
            pos_map[bid] = (bx + (c_w // 2), by + (c_h // 2))

            card_stroke = "#ef4444" if b.is_terminal else "#10b981" if b.act.startswith("Act 1") else "#f59e0b"
            svg.append(f'  <!-- Beat: {safe_xml(b.title)} -->')
            svg.append(f'  <rect x="{bx}" y="{by}" width="{c_w}" height="{c_h}" rx="8" fill="#18181b" stroke="{card_stroke}" stroke-width="1.5" />')
            svg.append(f'  <text x="{bx + 12}" y="{by + 24}" fill="#ffffff" font-size="12" font-weight="700" font-family="sans-serif">{safe_xml(b.title[:22])}</text>')
            svg.append(f'  <text x="{bx + 12}" y="{by + 42}" fill="#a1a1aa" font-size="9" font-family="sans-serif">Role: {safe_xml(b.character[:18])}</text>')
            svg.append(f'  <text x="{bx + 12}" y="{by + 58}" fill="#71717a" font-size="9" font-family="sans-serif">{safe_xml(b.act[:16])} | Tension: {int(b.tension_level)}%</text>')
            if b.description:
                svg.append(f'  <text x="{bx + 12}" y="{by + 78}" fill="#94a3b8" font-size="8" font-family="sans-serif">{safe_xml(b.description[:32])}...</text>')

        # Draw Connecting Branch Lines
        for br in self.branches:
            if br.source_id in pos_map and br.target_id in pos_map:
                x1, y1 = pos_map[br.source_id]
                x2, y2 = pos_map[br.target_id]
                line_color = "#38bdf8" if br.is_canonical else "#f43f5e"
                dash = 'stroke-dasharray="3,3"' if not br.is_canonical else ""
                svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{line_color}" stroke-width="1.5" {dash} opacity="0.6" />')

        # Footer
        svg.append(f'  <text x="{width // 2}" y="{height - 20}" fill="#71717a" font-size="10" text-anchor="middle" font-family="sans-serif">Spatial Non-Linear Plot Mesh | Green: Beginning, Amber: Middle, Red: Climax / Resolution</text>')
        svg.append('</svg>')
        return "\n".join(svg)

    @classmethod
    def export_summary(cls, audit: NarrativeAudit, beats_sample: List[NarrativeBeat]) -> str:
        """Generate executive markdown summary of non-linear storyline topology."""
        beats_table = "\n".join([
            f"| `{b.id}` | **{b.title}** | {b.character} | `{b.act}` | `{b.tension_level}%` | {'Terminal' if b.is_terminal else 'Open'} |"
            for b in beats_sample[:10]
        ])

        return (
            f"# Non-Linear Narrative Branching Simulator & Plot Mesh\n\n"
            f"**Narrative Agency Score:** `{audit.narrative_agency_score}/100` (Branching diversity and causal impact)\n"
            f"**Total Narrative Beats:** `{audit.total_beats}` | **Plot Branches:** `{audit.total_branches}`\n"
            f"**Characters Tracked:** `{audit.characters_count}` | **Dangling Threads:** `{audit.dangling_threads_count}`\n"
            f"**Pacing Bottlenecks:** `{audit.pacing_bottlenecks_count}` | **Average Dramatic Tension:** `{audit.average_tension}%`\n\n"
            f"### Narrative Beats Topography\n\n"
            f"| Beat ID | Title | Character | Act | Tension | Status |\n"
            f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            f"{beats_table}\n\n"
            f"### Cognitive Diagnostic Recommendations\n"
            f"- **Dangling Threads Resolution:** {'All narrative threads converge to designated resolutions.' if audit.dangling_threads_count == 0 else f'Flagged {audit.dangling_threads_count} unresolved leaf nodes needing definitive consequences or terminal endings.'}\n"
            f"- **Pacing Bottlenecks:** {'Smooth narrative flow without excessive nodal convergence.' if audit.pacing_bottlenecks_count == 0 else f'Identified {audit.pacing_bottlenecks_count} plot nodes where 3+ branches converge, risking cognitive plot overload.'}\n"
            f"- **Spatial Layout Leverage:** Multi-track 2D timeline separates parallel character storylines, preventing narrative chronological entanglement.\n"
        )


def main():
    """Quick CLI runner."""
    print("NarrativeBranchingSimulator Loaded.")


if __name__ == "__main__":
    main()
