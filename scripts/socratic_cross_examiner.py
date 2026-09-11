"""
Autonomous Cognitive Multi-Perspective Architectural Socratic Cross-Examiner for DxSkills.

Grounded in:
- Eide and Eide M-I-N-D spatial framework (stress-testing structural interconnectedness)
- Popperian Falsifiability and Socratic Elenchus (refuting ungrounded design claims)
- Sweller Cognitive Load Theory (exposing hidden operational friction in complex architectures)
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SocraticProbe:
    """Targeted adversarial interrogation probe examining architectural vulnerability."""
    dimension: str
    target_component: str
    forcing_question: str
    failure_mode_exposed: str
    severity_weight: float  # 1.0 to 10.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExaminationScorecard:
    """Comprehensive evaluation of architectural rigor, falsifiability, and resilience."""
    system_title: str
    architectural_rigor_score: float  # 0.0 to 100.0
    boundary_invariance_score: float  # 0.0 to 10.0
    falsifiability_score: float      # 0.0 to 10.0
    coupling_resilience_score: float  # 0.0 to 10.0
    failure_mode_score: float        # 0.0 to 10.0
    cognitive_ergonomics_score: float # 0.0 to 10.0
    verdict: str
    fragility_hotspots: List[str]
    probes: List[SocraticProbe]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SocraticCrossExaminer:
    """
    Submits spatial architectures and system specifications to relentless Socratic inquiry,
    identifying unverified boundaries, unfalsifiable claims, and operational blindspots.
    """

    def __init__(self) -> None:
        pass

    def cross_examine_architecture(
        self,
        system_title: str,
        components: List[Dict[str, Any]],
    ) -> ExaminationScorecard:
        """
        Cross-examine architecture across 5 foundational dimensions of systemic rigor.
        """
        if not components:
            return ExaminationScorecard(
                system_title=system_title,
                architectural_rigor_score=25.0,
                boundary_invariance_score=3.0,
                falsifiability_score=2.0,
                coupling_resilience_score=3.0,
                failure_mode_score=2.0,
                cognitive_ergonomics_score=2.5,
                verdict="Deficient (Empty Specification)",
                fragility_hotspots=["No concrete architectural components or interfaces declared."],
                probes=self._generate_default_probes(system_title),
            )

        total_comp = len(components)
        has_tests = sum(1 for c in components if c.get("has_tests", False))
        has_failover = sum(1 for c in components if c.get("has_failover", False))
        is_stateless = sum(1 for c in components if c.get("is_stateless", False))

        # Calculate dimension scores (0.0 to 10.0)
        falsifiability = round(min(10.0, max(1.0, (has_tests / total_comp) * 10.0)), 1)
        failure_mode = round(min(10.0, max(1.0, (has_failover / total_comp) * 10.0)), 1)
        coupling = round(min(10.0, max(2.0, (is_stateless / total_comp) * 8.0 + 2.0)), 1)
        boundary = round(min(10.0, max(2.0, (falsifiability + failure_mode) / 2.0)), 1)
        # Ergonomics penalizes excessive component sprawl without abstraction tiers
        ergo_penalty = max(0.0, (total_comp - 6) * 0.4)
        ergonomics = round(max(2.0, min(10.0, 9.0 - ergo_penalty)), 1)

        raw_rigor = (
            boundary * 2.0 +
            falsifiability * 2.5 +
            coupling * 2.0 +
            failure_mode * 2.0 +
            ergonomics * 1.5
        )
        rigor_score = round(max(10.0, min(100.0, raw_rigor)), 1)

        hotspots = []
        if falsifiability < 6.0:
            hotspots.append("Unfalsifiable core: Critical components lack explicit validation gates.")
        if failure_mode < 6.0:
            hotspots.append("Single point of failure vulnerability: Inadequate failover clustering.")
        if coupling < 5.0:
            hotspots.append("Tight state coupling: State mutation leaks across interface boundaries.")
        if total_comp > 8:
            hotspots.append(f"Cognitive sprawl: High component count ({total_comp}) degrades on-call triaging.")

        if rigor_score >= 80.0:
            verdict = "Hardened (Socratically Robust)"
        elif rigor_score >= 60.0:
            verdict = "Defensible (Minor Boundary Gaps)"
        elif rigor_score >= 40.0:
            verdict = "Fragile (Significant Blindspots)"
        else:
            verdict = "Vulnerable (Critical Architectural Failure)"

        probes = self._generate_component_probes(components)

        return ExaminationScorecard(
            system_title=system_title,
            architectural_rigor_score=rigor_score,
            boundary_invariance_score=boundary,
            falsifiability_score=falsifiability,
            coupling_resilience_score=coupling,
            failure_mode_score=failure_mode,
            cognitive_ergonomics_score=ergonomics,
            verdict=verdict,
            fragility_hotspots=hotspots,
            probes=probes,
        )

    def _generate_default_probes(self, title: str) -> List[SocraticProbe]:
        return [
            SocraticProbe(
                dimension="Boundary Invariance",
                target_component=title,
                forcing_question="Under 100x traffic surge or complete network split, what exact invariant prevents corruption?",
                failure_mode_exposed="Cascading silent failure under unexpected volume.",
                severity_weight=8.5,
            ),
            SocraticProbe(
                dimension="Falsifiability",
                target_component=title,
                forcing_question="What empirical telemetry proves this system is malfunctioning before users submit tickets?",
                failure_mode_exposed="Undetected semantic drift and dark debt.",
                severity_weight=9.0,
            ),
        ]

    def _generate_component_probes(self, components: List[Dict[str, Any]]) -> List[SocraticProbe]:
        probes = []
        for c in components:
            name = c.get("name", "Component")
            if not c.get("has_failover", False):
                probes.append(SocraticProbe(
                    dimension="Failure Mode",
                    target_component=name,
                    forcing_question=f"If node hosting '{name}' crashes at fsync barrier, how is zero data loss verified?",
                    failure_mode_exposed=f"Unrecoverable state loss in {name}.",
                    severity_weight=9.0,
                ))
            if not c.get("has_tests", False):
                probes.append(SocraticProbe(
                    dimension="Falsifiability",
                    target_component=name,
                    forcing_question=f"How can an adversarial engineer falsify the correctness of '{name}' in production?",
                    failure_mode_exposed=f"Unchecked logical divergence inside {name}.",
                    severity_weight=8.0,
                ))
        if not probes:
            probes.append(SocraticProbe(
                dimension="Cognitive Ergonomics",
                target_component="System Topology",
                forcing_question="Can a junior engineer diagnose a cascading timeout across these boundaries at 3 AM in under 5 minutes?",
                failure_mode_exposed="Excessive MTTR caused by opaque architectural boundaries.",
                severity_weight=7.5,
            ))
        return probes[:5]

    def export_canvas(
        self,
        scorecard: ExaminationScorecard,
        output_path: str = "socratic_examination.canvas",
    ) -> Dict[str, Any]:
        """
        Export Socratic examination topology into Obsidian .canvas JSON format.
        """
        nodes = []
        edges = []

        # Central System Rigor Hub Node
        hub_id = "node-socratic-hub"
        nodes.append({
            "id": hub_id,
            "x": 0,
            "y": 0,
            "width": 380,
            "height": 200,
            "type": "text",
            "text": (
                f"### [Socratic Scorecard] {scorecard.system_title}\n\n"
                f"- **Verdict:** {scorecard.verdict}\n"
                f"- **Architectural Rigor:** {scorecard.architectural_rigor_score}/100\n"
                f"- **Falsifiability:** {scorecard.falsifiability_score}/10\n"
                f"- **Failure Modes:** {scorecard.failure_mode_score}/10\n"
                f"- **Coupling Resilience:** {scorecard.coupling_resilience_score}/10"
            ),
            "color": "1" if scorecard.architectural_rigor_score < 60 else "4",
        })

        # Arrange Socratic Probes around the hub
        positions = [
            (-440, -180, "left", "bottom"),
            (440, -180, "right", "bottom"),
            (-440, 180, "left", "top"),
            (440, 180, "right", "top"),
            (0, 260, "bottom", "top"),
        ]

        for i, probe in enumerate(scorecard.probes):
            pid = f"node-probe-{i + 1}"
            px, py, from_side, to_side = positions[i % len(positions)]
            nodes.append({
                "id": pid,
                "x": px,
                "y": py,
                "width": 340,
                "height": 160,
                "type": "text",
                "text": (
                    f"### Probe #{i + 1}: {probe.dimension}\n\n"
                    f"**Target:** {probe.target_component}\n"
                    f"**Question:** {probe.forcing_question}\n\n"
                    f"*Risk: {probe.failure_mode_exposed}*"
                ),
                "color": "2",
            })
            edges.append({
                "id": f"edge-hub-probe-{i + 1}",
                "fromNode": hub_id,
                "fromSide": from_side,
                "toNode": pid,
                "toSide": to_side,
                "label": f"Interrogation #{i + 1}",
            })

        canvas_data = {"nodes": nodes, "edges": edges}

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)

        return canvas_data

    def export_svg_radar(
        self,
        scorecard: ExaminationScorecard,
        width: int = 560,
        height: int = 380,
    ) -> str:
        """
        Export 5-axis pentagonal radar visualization of architectural rigor.
        """
        cx, cy, r = 160, 190, 100
        dims = [
            ("Boundary", scorecard.boundary_invariance_score),
            ("Falsify", scorecard.falsifiability_score),
            ("Coupling", scorecard.coupling_resilience_score),
            ("Failure", scorecard.failure_mode_score),
            ("Ergo", scorecard.cognitive_ergonomics_score),
        ]

        # Compute 5 radar vertices
        points = []
        for idx, (_, val) in enumerate(dims):
            angle = (2.0 * math.pi * idx / 5.0) - (math.pi / 2.0)
            norm_r = (val / 10.0) * r
            px = cx + int(norm_r * math.cos(angle))
            py = cy + int(norm_r * math.sin(angle))
            points.append(f"{px},{py}")

        polygon_pts = " ".join(points)

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
            '  <defs>',
            '    <linearGradient id="bgGradSocratic" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#080e1a" />',
            '      <stop offset="100%" stop-color="#141f33" />',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" rx="14" fill="url(#bgGradSocratic)" stroke="#334155" stroke-width="1.5" />',
            f'  <text x="24" y="36" fill="#f8fafc" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="bold">Socratic Cross-Examiner: {scorecard.system_title}</text>',
            f'  <text x="24" y="58" fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif" font-size="12">Verdict: {scorecard.verdict} | Rigor Score: {scorecard.architectural_rigor_score}/100</text>',
            '  <!-- 5-Axis Spider Radar Background Grid -->',
            f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#334155" stroke-dasharray="3,3" />',
            f'  <circle cx="{cx}" cy="{cy}" r="{int(r * 0.6)}" fill="none" stroke="#334155" stroke-dasharray="2,2" />',
            f'  <circle cx="{cx}" cy="{cy}" r="{int(r * 0.3)}" fill="none" stroke="#334155" stroke-dasharray="2,2" />',
        ]

        # Draw axis spokes
        for idx, (label, _) in enumerate(dims):
            angle = (2.0 * math.pi * idx / 5.0) - (math.pi / 2.0)
            ax = cx + int((r + 18) * math.cos(angle))
            ay = cy + int((r + 18) * math.sin(angle))
            svg.append(f'  <line x1="{cx}" y1="{cy}" x2="{cx + int(r * math.cos(angle))}" y2="{cy + int(r * math.sin(angle))}" stroke="#334155" stroke-width="1" />')
            svg.append(f'  <text x="{ax}" y="{ay + 4}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle">{label}</text>')

        # Radar Polygon
        svg.extend([
            f'  <polygon points="{polygon_pts}" fill="#38bdf8" fill-opacity="0.35" stroke="#38bdf8" stroke-width="2" />',
            '  <!-- Dimension Score Cards Side Panel -->',
            '  <g transform="translate(320, 95)">',
            f'    <text x="0" y="0" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Dimension Breakdown (0-10):</text>',
            f'    <text x="0" y="24" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="12">1. Boundary Invariance: {scorecard.boundary_invariance_score}/10</text>',
            f'    <text x="0" y="48" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="12">2. Falsifiability Gates: {scorecard.falsifiability_score}/10</text>',
            f'    <text x="0" y="72" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="12">3. Coupling Resilience: {scorecard.coupling_resilience_score}/10</text>',
            f'    <text x="0" y="96" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="12">4. Failure Mode Defense: {scorecard.failure_mode_score}/10</text>',
            f'    <text x="0" y="120" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="12">5. Cognitive Ergonomics: {scorecard.cognitive_ergonomics_score}/10</text>',
            '    <line x1="0" y1="140" x2="210" y2="140" stroke="#334155" stroke-width="1" />',
            f'    <text x="0" y="162" fill="#f43f5e" font-family="system-ui, sans-serif" font-size="11">Active Socratic Probes: {len(scorecard.probes)} items</text>',
            f'    <text x="0" y="182" fill="#a78bfa" font-family="system-ui, sans-serif" font-size="11">Falsification Gate: Rigor {scorecard.architectural_rigor_score}%</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg)

    def export_summary_markdown(self, scorecard: ExaminationScorecard) -> str:
        """
        Generate executive Socratic examination audit in Markdown with zero em dashes.
        """
        lines = [
            f"# Socratic Architectural Cross-Examination: {scorecard.system_title}",
            "",
            f"**Verdict:** {scorecard.verdict}",
            f"**Architectural Rigor Score:** {scorecard.architectural_rigor_score} / 100.0",
            f"**Falsifiability Gates:** {scorecard.falsifiability_score} / 10.0",
            f"**Failure Mode Defense:** {scorecard.failure_mode_score} / 10.0",
            f"**Coupling Resilience:** {scorecard.coupling_resilience_score} / 10.0",
            f"**Cognitive Ergonomics:** {scorecard.cognitive_ergonomics_score} / 10.0",
            "",
            "## 1. Fragility Hotspots",
            "",
        ]

        if not scorecard.fragility_hotspots:
            lines.append("*Zero immediate fragility hotspots identified. Architecture is well-hardened.*")
        else:
            for h in scorecard.fragility_hotspots:
                lines.append(f"- {h}")

        lines.extend([
            "",
            "## 2. Active Socratic Interrogation Probes",
            "",
        ])

        for i, probe in enumerate(scorecard.probes):
            lines.extend([
                f"### Probe #{i + 1}: {probe.dimension} ({probe.target_component})",
                f"- **Forcing Question:** {probe.forcing_question}",
                f"- **Exposed Vulnerability:** {probe.failure_mode_exposed}",
                f"- **Severity Weight:** {probe.severity_weight} / 10.0",
                "",
            ])

        lines.extend([
            "---",
            "*Generated by DxSkills SocraticCrossExaminer. Zero phonological friction, zero em dashes.*",
        ])

        return "\n".join(lines)
