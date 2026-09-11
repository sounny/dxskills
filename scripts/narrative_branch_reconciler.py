"""
narrative_branch_reconciler.py - Autonomous Cognitive Spatial Multiscale Narrative Branching & Divergence Reconciler

Part of the DxSkills cognitive scaffolding suite (Phase 109, Cycle 105).
Grounded in Eide & Eide (2011) Narrative Reasoning in spatial cognition, Arthur (1989) path dependence,
and Cowan (2001) bounded cognitive capacity (N<=4).

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class NarrativeWaypoint:
    """Individual decision milestone or state waypoint along a narrative branch."""
    waypoint_id: str
    label: str
    branch_id: str
    phase_order: int
    assumptions: List[str] = field(default_factory=list)
    tradeoffs: Dict[str, float] = field(default_factory=dict)
    coordinates: Tuple[float, float] = (100.0, 100.0)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NarrativeBranch:
    """Directed sequence of waypoints representing an architectural strategy or story trajectory."""
    branch_id: str
    name: str
    origin_waypoint_id: str
    waypoints: List[NarrativeWaypoint]
    thematic_intent: str
    terminal_state: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "branch_id": self.branch_id,
            "name": self.name,
            "origin_waypoint_id": self.origin_waypoint_id,
            "thematic_intent": self.thematic_intent,
            "terminal_state": self.terminal_state,
            "waypoints": [w.to_dict() for w in self.waypoints],
        }


@dataclass
class DivergencePoint:
    """Bifurcation point where narrative pathways splinter into conflicting trajectories."""
    fork_id: str
    bifurcation_origin_id: str
    divergent_branch_ids: List[str]
    thematic_drift_distance: float  # 0.0 (aligned) to 1.0 (polar opposite)
    divergence_severity: str  # LOW, MODERATE, CRITICAL
    conflicting_assumptions: List[Tuple[str, str]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReconciliationBridge:
    """Synthesized unifying architectural bridge resolving conflicting narrative paths."""
    bridge_id: str
    source_branch_id: str
    target_branch_id: str
    synthesis_waypoint_label: str
    unifying_strategy: str
    tradeoff_consensus_score: float  # 0.0 to 1.0 Pareto efficiency
    reconciled_assumptions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReconciliationTelemetry:
    """Cognitive telemetry measuring narrative divergence, convergence ratio, and Cowan headroom."""
    total_branches_tracked: int
    total_waypoints_analyzed: int
    divergence_forks_detected: int
    reconciliation_bridges_synthesized: int
    mean_drift_distance: float
    systemic_convergence_ratio: float
    cowan_bounded: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BranchReconcilerResult:
    """Master result bundle containing branches, divergence forks, unifying bridges, and SVG map."""
    branches: List[NarrativeBranch]
    divergences: List[DivergencePoint]
    bridges: List[ReconciliationBridge]
    telemetry: ReconciliationTelemetry
    svg_reconciliation_map: str
    executive_synthesis_md: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telemetry": self.telemetry.to_dict(),
            "branches": [b.to_dict() for b in self.branches],
            "divergences": [d.to_dict() for d in self.divergences],
            "bridges": [br.to_dict() for br in self.bridges],
            "svg_reconciliation_map": self.svg_reconciliation_map,
            "executive_synthesis_md": self.executive_synthesis_md,
        }


class NarrativeBranchReconciler:
    """
    Autonomous Cognitive Spatial Multiscale Narrative Branching & Divergence Reconciler.

    Detects non-linear thematic bifurcation points across divergent spatial sub-canvases
    and synthesizes unifying architectural bridges reconciling conflicting strategic paths.
    """

    def __init__(self, drift_threshold: float = 0.35, max_active_branches: int = 4) -> None:
        self.drift_threshold = drift_threshold
        self.max_active_branches = max_active_branches

    def analyze_and_reconcile(self, raw_branches: List[Dict[str, Any]]) -> BranchReconcilerResult:
        """
        Task 109.1 & 109.2: Tracks narrative bifurcation points and synthesizes
        unifying architectural bridges to restore systemic coherence.
        """
        if not raw_branches:
            empty_telemetry = ReconciliationTelemetry(
                total_branches_tracked=0,
                total_waypoints_analyzed=0,
                divergence_forks_detected=0,
                reconciliation_bridges_synthesized=0,
                mean_drift_distance=0.0,
                systemic_convergence_ratio=1.0,
                cowan_bounded=True,
            )
            return BranchReconcilerResult(
                branches=[],
                divergences=[],
                bridges=[],
                telemetry=empty_telemetry,
                svg_reconciliation_map="",
                executive_synthesis_md="",
            )

        # Parse branches and waypoints
        branches: List[NarrativeBranch] = []
        total_wps = 0

        for b_idx, b_item in enumerate(raw_branches):
            bid = str(b_item.get("id") or b_item.get("branch_id") or f"br_{b_idx+1}")
            bname = str(b_item.get("name") or b_item.get("title") or f"Narrative Path {chr(65+b_idx)}")
            origin_id = str(b_item.get("origin_id") or b_item.get("fork_from") or "root")
            intent = str(b_item.get("intent") or b_item.get("thematic_intent") or "Exploratory Architecture")
            term = str(b_item.get("terminal_state") or "Resolved Milestone")

            raw_wps = b_item.get("waypoints", [])
            wps: List[NarrativeWaypoint] = []
            for w_idx, w_item in enumerate(raw_wps):
                wid = str(w_item.get("id") or f"{bid}_wp{w_idx+1}")
                lbl = str(w_item.get("label") or w_item.get("name") or f"Step {w_idx+1}")
                order = int(w_item.get("phase_order", w_idx + 1))
                assumps = list(w_item.get("assumptions", []))
                tradeoffs = dict(w_item.get("tradeoffs", {}))
                coords = tuple(w_item.get("coordinates", (150.0 + w_idx * 160.0, 120.0 + b_idx * 120.0)))
                wps.append(NarrativeWaypoint(
                    waypoint_id=wid,
                    label=lbl,
                    branch_id=bid,
                    phase_order=order,
                    assumptions=assumps,
                    tradeoffs=tradeoffs,
                    coordinates=coords,
                ))

            total_wps += len(wps)
            branches.append(NarrativeBranch(
                branch_id=bid,
                name=bname,
                origin_waypoint_id=origin_id,
                waypoints=wps,
                thematic_intent=intent,
                terminal_state=term,
            ))

        # Detect divergence points (Task 109.1)
        divergences: List[DivergencePoint] = []
        origin_groups: Dict[str, List[NarrativeBranch]] = {}
        for b in branches:
            origin_groups.setdefault(b.origin_waypoint_id, []).append(b)

        total_drift = 0.0
        drift_comparisons = 0

        for origin, group in origin_groups.items():
            if len(group) >= 2:
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        b1 = group[i]
                        b2 = group[j]

                        # Calculate thematic drift distance based on tradeoff disparities and assumption collisions
                        conflicts: List[Tuple[str, str]] = []
                        drift = 0.40  # baseline fork drift

                        # Compare tradeoffs
                        t1 = b1.waypoints[-1].tradeoffs if b1.waypoints else {}
                        t2 = b2.waypoints[-1].tradeoffs if b2.waypoints else {}
                        common_keys = set(t1.keys()).intersection(set(t2.keys()))
                        if common_keys:
                            diff_sum = sum(abs(t1[k] - t2[k]) for k in common_keys)
                            drift = min(1.0, 0.20 + (diff_sum / max(1, len(common_keys))))

                        # Compare terminal assumptions
                        a1 = b1.waypoints[-1].assumptions if b1.waypoints else []
                        a2 = b2.waypoints[-1].assumptions if b2.waypoints else []
                        for asm1 in a1[:2]:
                            for asm2 in a2[:2]:
                                if asm1.lower() != asm2.lower():
                                    conflicts.append((asm1, asm2))

                        drift = round(max(0.10, min(1.0, drift)), 2)
                        total_drift += drift
                        drift_comparisons += 1

                        if drift < 0.35:
                            sev = "LOW"
                        elif drift < 0.70:
                            sev = "MODERATE"
                        else:
                            sev = "CRITICAL"

                        divergences.append(DivergencePoint(
                            fork_id=f"fork_{len(divergences)+1}",
                            bifurcation_origin_id=origin,
                            divergent_branch_ids=[b1.branch_id, b2.branch_id],
                            thematic_drift_distance=drift,
                            divergence_severity=sev,
                            conflicting_assumptions=conflicts,
                        ))

        # Synthesize unifying reconciliation bridges (Task 109.2)
        bridges: List[ReconciliationBridge] = []
        for d in divergences:
            if d.thematic_drift_distance >= self.drift_threshold:
                b1_id, b2_id = d.divergent_branch_ids[0], d.divergent_branch_ids[1]
                b1 = next(b for b in branches if b.branch_id == b1_id)
                b2 = next(b for b in branches if b.branch_id == b2_id)

                # Formulate synthesis bridge
                bridge_id = f"bridge_{len(bridges)+1}"
                synth_label = f"Synthesized Unified Horizon ({b1.name.split(':')[0]} + {b2.name.split(':')[0]})"
                strat = f"Pareto-optimal integration balancing {b1.thematic_intent} with {b2.thematic_intent}."
                consensus_score = round(max(0.65, min(0.95, 1.0 - (d.thematic_drift_distance * 0.40))), 2)

                reconciled = [
                    f"Harmonized tradeoff equilibrium across {b1.name} and {b2.name}",
                    "Continuous telemetry feedback preventing branch divergence relapse",
                ]

                bridges.append(ReconciliationBridge(
                    bridge_id=bridge_id,
                    source_branch_id=b1_id,
                    target_branch_id=b2_id,
                    synthesis_waypoint_label=synth_label,
                    unifying_strategy=strat,
                    tradeoff_consensus_score=consensus_score,
                    reconciled_assumptions=reconciled,
                ))

        mean_drift = round(total_drift / max(1, drift_comparisons), 2)
        conv_ratio = round(len(bridges) / max(1, len(divergences)), 2)
        cowan_bounded = len(branches) <= self.max_active_branches

        telemetry = ReconciliationTelemetry(
            total_branches_tracked=len(branches),
            total_waypoints_analyzed=total_wps,
            divergence_forks_detected=len(divergences),
            reconciliation_bridges_synthesized=len(bridges),
            mean_drift_distance=mean_drift,
            systemic_convergence_ratio=conv_ratio,
            cowan_bounded=cowan_bounded,
        )

        # Build Executive Synthesis Markdown
        md_lines = [
            "# Multiscale Narrative Branching & Divergence Reconciliation",
            "",
            f"**Total Tracked Branches:** {telemetry.total_branches_tracked} | **Analyzed Waypoints:** {telemetry.total_waypoints_analyzed}",
            f"**Bifurcation Forks Detected:** {telemetry.divergence_forks_detected} | **Synthesized Bridges:** {telemetry.reconciliation_bridges_synthesized}",
            f"**Mean Thematic Drift:** {telemetry.mean_drift_distance:.2f} | **Convergence Ratio:** {telemetry.systemic_convergence_ratio * 100:.0f}%",
            f"**Cowan Bounded (N<=4):** {'Yes [OPTIMAL]' if telemetry.cowan_bounded else 'No [EXCESS BRANCHING]'}  ",
            "",
            "## Synthesized Architectural Bridges",
            "",
            "| Bridge ID | Conjoined Branches | Consensus Score | Unifying Strategic Vector |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for br in bridges:
            md_lines.append(
                f"| `{br.bridge_id}` | `{br.source_branch_id}` &bull; `{br.target_branch_id}` | "
                f"{br.tradeoff_consensus_score * 100:.0f}% | {br.unifying_strategy} |"
            )

        md_lines.append("")
        md_lines.append("## Identified Divergence Points & Conflict Vectors")
        md_lines.append("")
        for d in divergences:
            md_lines.append(
                f"- **{d.fork_id} (Origin: `{d.bifurcation_origin_id}`):** Drift Distance: {d.thematic_drift_distance:.2f} "
                f"[{d.divergence_severity}]. Branches: {d.divergent_branch_ids}"
            )

        synthesis_md = "\n".join(md_lines)

        svg_map = self._render_reconciliation_svg(
            branches=branches,
            divergences=divergences,
            bridges=bridges,
            telemetry=telemetry,
        )

        return BranchReconcilerResult(
            branches=branches,
            divergences=divergences,
            bridges=bridges,
            telemetry=telemetry,
            svg_reconciliation_map=svg_map,
            executive_synthesis_md=synthesis_md,
        )

    def _render_reconciliation_svg(
        self,
        branches: List[NarrativeBranch],
        divergences: List[DivergencePoint],
        bridges: List[ReconciliationBridge],
        telemetry: ReconciliationTelemetry,
    ) -> str:
        """Renders dark titanium branching tree with converging synthesis bridge arcs."""
        w, h = 920, 520
        t = telemetry

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '  <defs>',
            '    <linearGradient id="nbrBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#080c14"/>',
            '      <stop offset="100%" stop-color="#0f172a"/>',
            '    </linearGradient>',
            '    <linearGradient id="bridgeArc" x1="0%" y1="0%" x2="100%" y2="0%">',
            '      <stop offset="0%" stop-color="#38bdf8"/>',
            '      <stop offset="50%" stop-color="#10b981"/>',
            '      <stop offset="100%" stop-color="#a855f7"/>',
            '    </linearGradient>',
            '  </defs>',
            '  <rect width="100%" height="100%" fill="url(#nbrBg)"/>',
            '  <!-- Header -->',
            '  <text x="40" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Multiscale Narrative Branching &amp; Divergence Reconciler</text>',
            f'  <text x="40" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#94a3b8">Arthur Path Dependence &bull; Branches: {t.total_branches_tracked} &bull; Bridges: {t.reconciliation_bridges_synthesized} &bull; Convergence: {t.systemic_convergence_ratio * 100:.0f}% &bull; Cowan: {t.cowan_bounded}</text>',
            '  <!-- Main Branching Canvas -->',
            '  <g transform="translate(40, 95)">',
            '    <rect x="0" y="0" width="840" height="270" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
        ]

        # Draw Root Origin Node
        svg_parts.extend([
            '    <!-- Origin Root Node -->',
            '    <circle cx="60" cy="135" r="12" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>',
            '    <text x="60" y="139" font-family="monospace" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">ROOT</text>',
            '    <text x="60" y="165" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Fork Anchor</text>',
        ])

        # Draw Branch Lines & Waypoints
        branch_colors = ["#38bdf8", "#a855f7", "#f59e0b", "#10b981"]
        for b_idx, b in enumerate(branches[:4]):
            col = branch_colors[b_idx % len(branch_colors)]
            target_y = 65 + (b_idx * 50)

            # Curved branch line from root
            svg_parts.extend([
                f'    <!-- Branch {b.branch_id} path -->',
                f'    <path d="M 72 135 C 140 135, 140 {target_y}, 200 {target_y}" fill="none" stroke="{col}" stroke-width="2"/>',
            ])

            # Draw Waypoints along the branch
            prev_x = 200
            for w_idx, wp in enumerate(b.waypoints):
                cur_x = 200 + (w_idx * 160)
                if w_idx > 0:
                    svg_parts.append(f'    <line x1="{prev_x}" y1="{target_y}" x2="{cur_x}" y2="{target_y}" stroke="{col}" stroke-width="2"/>')
                svg_parts.extend([
                    f'    <!-- Waypoint {wp.waypoint_id} -->',
                    f'    <circle cx="{cur_x}" cy="{target_y}" r="8" fill="#0f172a" stroke="{col}" stroke-width="2.5"/>',
                    f'    <text x="{cur_x}" y="{target_y - 14}" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#f8fafc" text-anchor="middle">{wp.label}</text>',
                ])
                prev_x = cur_x

        # Draw Reconciliation Bridge Arcs (Task 109.2)
        if len(branches) >= 2:
            svg_parts.extend([
                '    <!-- Reconciling Bridge Arc -->',
                '    <path d="M 680 65 C 760 65, 760 115, 680 115" fill="none" stroke="url(#bridgeArc)" stroke-width="2.5" stroke-dasharray="4,4"/>',
                '    <rect x="700" y="80" width="125" height="24" rx="6" fill="#065f46" stroke="#10b981" stroke-width="1"/>',
                '    <text x="762" y="96" font-family="monospace" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">SYNTHESIS BRIDGE</text>',
            ])

        svg_parts.append('  </g>')

        # Bottom Cards: Telemetry
        svg_parts.extend([
            '  <!-- Bottom Cards: Telemetry Badges -->',
            '  <g transform="translate(40, 390)">',
            '    <rect x="0" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="20" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Bifurcation Convergence</text>',
            f'    <text x="20" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#10b981">{t.systemic_convergence_ratio * 100:.0f}%</text>',
            f'    <text x="20" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">{t.reconciliation_bridges_synthesized} unifying bridges built</text>',
            '    <rect x="290" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="310" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Mean Thematic Drift</text>',
            f'    <text x="310" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#38bdf8">{t.mean_drift_distance:.2f}</text>',
            f'    <text x="310" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">{t.divergence_forks_detected} divergence forks monitored</text>',
            '    <rect x="580" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="600" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Active Branch Capacity</text>',
            f'    <text x="600" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#a855f7">{t.total_branches_tracked} / {self.max_active_branches}</text>',
            f'    <text x="600" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Cowan bounded: {t.cowan_bounded}</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg_parts)

    def export_svg(self, result: BranchReconcilerResult, output_path: Optional[str] = None) -> str:
        """Exports SVG diagram to file or returns XML string."""
        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(result.svg_reconciliation_map)
        return result.svg_reconciliation_map

    def generate_ascii_report(self, result: BranchReconcilerResult) -> str:
        """Generates terminal ASCII summary table of narrative branching and divergence metrics."""
        t = result.telemetry
        lines = [
            "================================================================================",
            "   MULTISCALE NARRATIVE BRANCHING & RECONCILER (PHASE 109 / CYCLE 105)",
            "================================================================================",
            f" Active Branches       : {t.total_branches_tracked} trajectories",
            f" Analyzed Waypoints    : {t.total_waypoints_analyzed} milestones",
            f" Divergence Forks      : {t.divergence_forks_detected} bifurcation points",
            f" Unifying Bridges      : {t.reconciliation_bridges_synthesized} synthesized horizons",
            f" Mean Thematic Drift   : {t.mean_drift_distance:.2f} (0.0=Parallel, 1.0=Polar Opposite)",
            f" Convergence Ratio     : {t.systemic_convergence_ratio * 100:.0f}%",
            f" Cowan Bounded (N<=4)  : {'Yes [OPTIMAL]' if t.cowan_bounded else 'No [COGNITIVE OVERFLOW]'}",
            "--------------------------------------------------------------------------------",
            " TRACKED NARRATIVE BRANCHES",
            "--------------------------------------------------------------------------------",
        ]

        if not result.branches:
            lines.append(" (No branches tracked; empty trajectory input)")
        else:
            for b in result.branches:
                lines.append(f" [BRANCH] {b.branch_id}: '{b.name}' (Origin: `{b.origin_waypoint_id}`)")
                lines.append(f"          Intent: {b.thematic_intent} | Terminal: {b.terminal_state}")
                wp_seq = " -> ".join([f"[{w.label}]" for w in b.waypoints])
                lines.append(f"          Path: {wp_seq}")

        lines.append("--------------------------------------------------------------------------------")
        lines.append(" RECONCILED ARCHITECTURAL BRIDGES")
        lines.append("--------------------------------------------------------------------------------")
        if not result.bridges:
            lines.append(" (No bridges required; branches are coherent or under drift threshold)")
        else:
            for br in result.bridges:
                lines.append(f" [BRIDGE] {br.bridge_id}: '{br.synthesis_waypoint_label}' (Consensus: {br.tradeoff_consensus_score * 100:.0f}%)")
                lines.append(f"          Connecting: `{br.source_branch_id}` <====> `{br.target_branch_id}`")
                lines.append(f"          Strategy  : {br.unifying_strategy}")

        lines.append("================================================================================")
        return "\n".join(lines)
