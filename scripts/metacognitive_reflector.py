"""
Autonomous Cognitive Multi-Perspective Metacognitive Reflector and Bias Breaker for DxSkills.

Grounded in:
- Eide and Eide M-I-N-D spatial framework (interconnected reasoning without cognitive fixation)
- Sweller Cognitive Load Theory (mitigating confirmation bias and narrow schema entrenchment)
- Baddeley Working Memory Model (executive metacognitive monitoring and dialectic perspective pivoting)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PerspectiveLens:
    """Dialectical reframing lens for challenging cognitive blindspots."""
    name: str
    lens_type: str
    provocation: str
    countervailing_hypothesis: str
    resilience_impact: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BlindspotAssessment:
    """Quantitative evaluation of cognitive fixation traps and assumption fragility."""
    thesis_title: str
    total_assumptions: int
    unvalidated_count: int
    fixation_risk_score: float
    confirmation_trap_index: float
    dialectical_resilience_score: float
    status: str
    vulnerabilities: List[str]
    lenses: List[PerspectiveLens]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MetacognitiveReflector:
    """
    Scans mental models and strategic theses for cognitive blindspots,
    anchoring bias, and confirmation traps, then synthesizes countervailing hypotheses.
    """

    def __init__(self) -> None:
        pass

    def assess_thesis(
        self,
        thesis_title: str,
        assumptions: List[Dict[str, Any]],
        perspective_breadth: int = 1,
    ) -> BlindspotAssessment:
        """
        Assess assumptions for fixation risk, unvalidated dependencies, and single-perspective fragility.
        """
        total = len(assumptions)
        if total == 0:
            return BlindspotAssessment(
                thesis_title=thesis_title,
                total_assumptions=0,
                unvalidated_count=0,
                fixation_risk_score=20.0,
                confirmation_trap_index=0.20,
                dialectical_resilience_score=80.0,
                status="Balanced (Low Complexity)",
                vulnerabilities=["No explicit assumptions detected. Risk of unconscious default framing."],
                lenses=self._generate_default_lenses(thesis_title),
            )

        unvalidated = sum(1 for a in assumptions if not a.get("validated", False))
        unvalidated_ratio = unvalidated / total

        # High reliance on single perspective amplifies confirmation traps
        perspective_penalty = max(0.0, (4 - perspective_breadth) * 12.0)
        unvalidated_penalty = unvalidated_ratio * 55.0
        depth_penalty = min(20.0, total * 2.0)

        fixation_risk = round(min(100.0, max(5.0, unvalidated_penalty + perspective_penalty + depth_penalty)), 1)
        trap_index = round(min(1.0, max(0.05, (unvalidated_ratio * 0.7) + ((4 - min(4, perspective_breadth)) * 0.1))), 2)
        resilience = round(max(0.0, min(100.0, 100.0 - (fixation_risk * 0.85))), 1)

        if fixation_risk < 35.0:
            status = "Low Risk (Dialectically Grounded)"
        elif fixation_risk < 60.0:
            status = "Moderate Strain (Unvalidated Anchors)"
        elif fixation_risk < 80.0:
            status = "High Fixation (Confirmation Trap)"
        else:
            status = "Critical Fragility (Dogmatic Clustering)"

        vulnerabilities = []
        for a in assumptions:
            if not a.get("validated", False):
                label = a.get("label", "Key Assumption")
                vulnerabilities.append(f"Unvalidated anchor: '{label}' lacks empirical corroboration.")

        if perspective_breadth <= 1:
            vulnerabilities.append("Monolithic viewpoint: Analysis lacks cross-functional red teaming.")

        lenses = self._synthesize_lenses(thesis_title, assumptions)

        return BlindspotAssessment(
            thesis_title=thesis_title,
            total_assumptions=total,
            unvalidated_count=unvalidated,
            fixation_risk_score=fixation_risk,
            confirmation_trap_index=trap_index,
            dialectical_resilience_score=resilience,
            status=status,
            vulnerabilities=vulnerabilities,
            lenses=lenses,
        )

    def _generate_default_lenses(self, title: str) -> List[PerspectiveLens]:
        return [
            PerspectiveLens(
                name="Inversion Lens",
                lens_type="inversion",
                provocation=f"What if the foundational premise of '{title}' is fundamentally reversed?",
                countervailing_hypothesis="Opposite environmental dynamics may yield superior efficiency.",
                resilience_impact=25.0,
            ),
            PerspectiveLens(
                name="Adversarial Red Team",
                lens_type="adversarial",
                provocation="Where will hostile competition or extreme black-swan conditions exploit this design?",
                countervailing_hypothesis="Resource starvation could cripple monolithic dependencies.",
                resilience_impact=30.0,
            ),
        ]

    def _synthesize_lenses(
        self,
        title: str,
        assumptions: List[Dict[str, Any]],
    ) -> List[PerspectiveLens]:
        first_claim = assumptions[0].get("label", "Primary Thesis") if assumptions else title

        return [
            PerspectiveLens(
                name="Inversion Lens (Munger / Nietzsche)",
                lens_type="inversion",
                provocation=f"Assume '{first_claim}' fails catastrophically on launch. What caused it?",
                countervailing_hypothesis="Decoupled fail-safe pathways must precede optimization efforts.",
                resilience_impact=28.0,
            ),
            PerspectiveLens(
                name="Constraint Multiplier (TRIZ Principle)",
                lens_type="constraint",
                provocation="If primary computing or capital resources were slashed by 80%, what architecture survives?",
                countervailing_hypothesis="Lightweight, asynchronous edge protocols outperform heavy central nodes.",
                resilience_impact=22.0,
            ),
            PerspectiveLens(
                name="Adversarial Red Team (Pre-Mortem)",
                lens_type="adversarial",
                provocation="How does an intelligent adversary exploit the unverified anchors in this model?",
                countervailing_hypothesis="Adversaries will target downstream coordination latencies.",
                resilience_impact=25.0,
            ),
            PerspectiveLens(
                name="Decoupling Perspective (Systems Dynamics)",
                lens_type="decoupling",
                provocation="Which two tightly coupled variables can be structurally severed?",
                countervailing_hypothesis="Isolating state storage from compute execution eliminates cascading stalls.",
                resilience_impact=25.0,
            ),
        ]

    def export_canvas(self, assessment: BlindspotAssessment, output_path: str = "metacognitive_bias.canvas") -> Dict[str, Any]:
        """
        Export dialectic perspective map to Obsidian .canvas JSON format.
        """
        nodes = []
        edges = []

        # Central Root Node
        root_id = "node-thesis"
        nodes.append({
            "id": root_id,
            "x": 0,
            "y": 0,
            "width": 380,
            "height": 180,
            "type": "text",
            "text": (
                f"### [Core Thesis] {assessment.thesis_title}\n\n"
                f"- **Fixation Risk:** {assessment.fixation_risk_score} / 100\n"
                f"- **Status:** {assessment.status}\n"
                f"- **Resilience Index:** {assessment.dialectical_resilience_score}%\n"
                f"- **Unvalidated Anchors:** {assessment.unvalidated_count} of {assessment.total_assumptions}"
            ),
            "color": "1" if assessment.fixation_risk_score > 60 else "4",
        })

        # Peripheral Dialectical Lenses
        positions = [
            (-460, -220, "left", "bottom"),
            (460, -220, "right", "bottom"),
            (-460, 220, "left", "top"),
            (460, 220, "right", "top"),
        ]

        for i, lens in enumerate(assessment.lenses):
            lens_id = f"node-lens-{i + 1}"
            px, py, from_side, to_side = positions[i % len(positions)]
            nodes.append({
                "id": lens_id,
                "x": px,
                "y": py,
                "width": 360,
                "height": 170,
                "type": "text",
                "text": (
                    f"### {lens.name}\n\n"
                    f"**Provocation:** {lens.provocation}\n\n"
                    f"**Counter-Thesis:** {lens.countervailing_hypothesis}\n"
                    f"*Resilience Lift: +{lens.resilience_impact}%*"
                ),
                "color": "5",
            })
            edges.append({
                "id": f"edge-thesis-lens-{i + 1}",
                "fromNode": root_id,
                "fromSide": from_side,
                "toNode": lens_id,
                "toSide": to_side,
                "label": f"Challenge #{i + 1}",
            })

        canvas_data = {"nodes": nodes, "edges": edges}

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(canvas_data, f, indent=2)

        return canvas_data

    def export_svg_radar(self, assessment: BlindspotAssessment, width: int = 560, height: int = 360) -> str:
        """
        Export a modern vector SVG radar and dialectic tension visualizer.
        """
        fix = assessment.fixation_risk_score
        res = assessment.dialectical_resilience_score
        trap_pct = int(assessment.confirmation_trap_index * 100)

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
            '  <defs>',
            '    <linearGradient id="bgGradReflect" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#090d16" />',
            '      <stop offset="100%" stop-color="#131d2e" />',
            '    </linearGradient>',
            '    <linearGradient id="barGradRisk" x1="0%" y1="0%" x2="100%" y2="0%">',
            '      <stop offset="0%" stop-color="#38bdf8" />',
            '      <stop offset="100%" stop-color="#f43f5e" />',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" rx="14" fill="url(#bgGradReflect)" stroke="#1e293b" stroke-width="1.5" />',
            f'  <text x="28" y="38" fill="#f8fafc" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="bold">Metacognitive Reflector: {assessment.thesis_title}</text>',
            f'  <text x="28" y="60" fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif" font-size="12">Status: {assessment.status} | Fixation: {fix}/100 | Resilience: {res}%</text>',
            '  <!-- Dialectic Tension Polar Visualizer -->',
            '  <g transform="translate(140, 200)">',
            '    <circle cx="0" cy="0" r="90" fill="none" stroke="#334155" stroke-dasharray="4,4" stroke-width="1" />',
            '    <circle cx="0" cy="0" r="60" fill="none" stroke="#334155" stroke-dasharray="3,3" stroke-width="1" />',
            '    <circle cx="0" cy="0" r="30" fill="none" stroke="#334155" stroke-dasharray="2,2" stroke-width="1" />',
            '    <line x1="-90" y1="0" x2="90" y2="0" stroke="#334155" stroke-width="1" />',
            '    <line x1="0" y1="-90" x2="0" y2="90" stroke="#334155" stroke-width="1" />',
            f'    <circle cx="0" cy="0" r="{max(12, int(fix * 0.8))}" fill="#f43f5e" opacity="0.4" />',
            f'    <circle cx="0" cy="0" r="{max(8, int(res * 0.8))}" fill="#38bdf8" opacity="0.35" />',
            '    <text x="0" y="-98" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle">Inversion</text>',
            '    <text x="102" y="4" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" text-anchor="start">Decoupling</text>',
            '    <text x="0" y="110" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" text-anchor="middle">Constraint</text>',
            '    <text x="-102" y="4" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" text-anchor="end">Adversarial</text>',
            '  </g>',
            '  <!-- Telemetry Metrics & Dialectic Countermeasures -->',
            '  <g transform="translate(280, 95)">',
            f'    <text x="0" y="20" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Confirmation Trap Index: {trap_pct}%</text>',
            '    <rect x="0" y="30" width="240" height="8" rx="4" fill="#1e293b" />',
            f'    <rect x="0" y="30" width="{int(trap_pct * 2.4)}" height="8" rx="4" fill="url(#barGradRisk)" />',
            f'    <text x="0" y="65" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Dialectical Resilience: {res}%</text>',
            '    <rect x="0" y="75" width="240" height="8" rx="4" fill="#1e293b" />',
            f'    <rect x="0" y="75" width="{int(res * 2.4)}" height="8" rx="4" fill="#38bdf8" />',
            '    <line x1="0" y1="105" x2="240" y2="105" stroke="#334155" stroke-width="1" />',
            '    <text x="0" y="130" fill="#a78bfa" font-family="system-ui, sans-serif" font-size="12" font-weight="bold">Countervailing Lenses Deployed:</text>',
            '    <text x="0" y="152" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">1. Inversion (Premise Catastrophe Failure)</text>',
            '    <text x="0" y="172" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">2. Constraint Multiplier (Resource Slashes)</text>',
            '    <text x="0" y="192" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">3. Adversarial Red Team (Attack Vectors)</text>',
            '    <text x="0" y="212" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">4. Decoupling (Structural Severance)</text>',
            '  </g>',
            '</svg>',
        ]
        return "\n".join(svg)

    def export_summary_markdown(self, assessment: BlindspotAssessment) -> str:
        """
        Generate executive markdown audit report with zero em dashes.
        """
        lines = [
            f"# Metacognitive Reflector and Bias Audit: {assessment.thesis_title}",
            "",
            f"**Audit Verdict:** {assessment.status}",
            f"**Fixation Risk Score:** {assessment.fixation_risk_score} / 100.0",
            f"**Confirmation Trap Index:** {assessment.confirmation_trap_index} (0.0 to 1.0)",
            f"**Dialectical Resilience:** {assessment.dialectical_resilience_score}%",
            "",
            "## 1. Assumption Vulnerability Assessment",
            "",
            f"- Total Stated Assumptions: {assessment.total_assumptions}",
            f"- Unvalidated Hypotheses: {assessment.unvalidated_count}",
        ]

        if assessment.vulnerabilities:
            lines.append("")
            for v in assessment.vulnerabilities:
                lines.append(f"- {v}")

        lines.extend([
            "",
            "## 2. Dialectical Counter-Perspectives (Pivoting Lenses)",
            "",
        ])

        for i, lens in enumerate(assessment.lenses):
            lines.extend([
                f"### {i + 1}. {lens.name}",
                f"- **Provocation:** {lens.provocation}",
                f"- **Counter-Thesis:** {lens.countervailing_hypothesis}",
                f"- **Expected Resilience Gain:** +{lens.resilience_impact}%",
                "",
            ])

        lines.extend([
            "---",
            "*Generated by DxSkills Metacognitive Reflector. Zero phonological friction, zero em dashes.*",
        ])

        return "\n".join(lines)
