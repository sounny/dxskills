"""Autonomous Cognitive Spatial Associative Multi-Perspective Dialectic Synthesizer & Synthesis Mesh.

Theoretical Foundation:
- Hegelian Triadic Dialectics & Spatial Synthesis (Thesis, Antithesis, Synthesis):
  Non-linear and dyslexic minds naturally perceive systemic multi-directional
  polarities. When faced with apparent architectural contradictions, traditional
  linear thinking forces false zero-sum trade-offs. Spatial dialectic synthesis
  externalizes tension vectors into 2D triads, discovering emergent third-way
  solutions (Aufhebung) that transcend the compromise.
- Polarity Management (Johnson, 1992):
  Distinguishes solvable problems from interdependent polarities that must be managed
  dynamically. Identifies chronic oscillation traps where systems swing wildly between
  opposing poles (e.g., centralized governance vs local agility).
- Architectural Third-Way Resolution Patterns:
  Generates verified decoupling strategies including Temporal Decoupling, Hierarchical
  Tiering, Orthogonal Abstraction, Dual-Plane Isolation, and Adaptive Equilibrium.
- Spatial Canvas Synthesis Mesh & Dark Titanium SVG Export:
  Enriches Obsidian .canvas graphs with integrated triad clusters and renders
  publication-grade SVG vector polarity radar diagrams.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class ResolutionStrategy(str, enum.Enum):
    """Architectural pattern employed to achieve third-way dialectic synthesis."""

    TEMPORAL_DECOUPLING = "temporal_decoupling"
    HIERARCHICAL_TIERING = "hierarchical_tiering"
    ORTHOGONAL_ABSTRACTION = "orthogonal_abstraction"
    DUAL_PLANE_ISOLATION = "dual_plane_isolation"
    ADAPTIVE_EQUILIBRIUM = "adaptive_equilibrium"


@dataclass
class PolarityPole:
    """One side of a structural or conceptual architectural polarity."""

    pole_id: str
    name: str
    core_values: List[str]
    strengths: List[str]
    overuse_vulnerabilities: List[str]
    node_references: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert pole to serializable dictionary."""
        return {
            "pole_id": self.pole_id,
            "name": self.name,
            "core_values": sorted(self.core_values),
            "strengths": sorted(self.strengths),
            "overuse_vulnerabilities": sorted(self.overuse_vulnerabilities),
            "node_references": sorted(self.node_references),
        }


@dataclass
class DialecticTension:
    """Identified structural tension between two opposing architectural poles."""

    tension_id: str
    thesis: PolarityPole
    antithesis: PolarityPole
    tension_intensity: float  # 0.0 to 1.0
    competing_attributes: List[str]
    shared_invariants: List[str]
    oscillation_risk: float  # 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert tension to serializable dictionary."""
        return {
            "tension_id": self.tension_id,
            "thesis": self.thesis.to_dict(),
            "antithesis": self.antithesis.to_dict(),
            "tension_intensity": round(self.tension_intensity, 2),
            "competing_attributes": sorted(self.competing_attributes),
            "shared_invariants": sorted(self.shared_invariants),
            "oscillation_risk": round(self.oscillation_risk, 2),
        }


@dataclass
class SyntheticResolution:
    """Emergent third-way integrative architecture transcending the binary tension."""

    synthesis_id: str
    tension_id: str
    title: str
    strategy: ResolutionStrategy
    mechanisms: List[str]
    retained_thesis_strengths: List[str]
    retained_antithesis_strengths: List[str]
    synthesis_rigor_score: float  # 0.0 to 1.0
    integrative_insight: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert resolution to serializable dictionary."""
        return {
            "synthesis_id": self.synthesis_id,
            "tension_id": self.tension_id,
            "title": self.title,
            "strategy": self.strategy.value,
            "mechanisms": sorted(self.mechanisms),
            "retained_thesis_strengths": sorted(self.retained_thesis_strengths),
            "retained_antithesis_strengths": sorted(self.retained_antithesis_strengths),
            "synthesis_rigor_score": round(self.synthesis_rigor_score, 2),
            "integrative_insight": self.integrative_insight,
        }


@dataclass
class SynthesisMeshTelemetry:
    """Telemetry capturing multi-perspective dialectic synthesis across spatial schemas."""

    total_poles: int
    tensions_detected: int
    syntheses_generated: int
    avg_tension_intensity: float
    top_synthesis_rigor: float
    dialectical_harmony_score: float
    tensions: List[DialecticTension] = field(default_factory=list)
    syntheses: List[SyntheticResolution] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_poles": self.total_poles,
            "tensions_detected": self.tensions_detected,
            "syntheses_generated": self.syntheses_generated,
            "avg_tension_intensity": round(self.avg_tension_intensity, 2),
            "top_synthesis_rigor": round(self.top_synthesis_rigor, 2),
            "dialectical_harmony_score": round(self.dialectical_harmony_score, 2),
            "tensions": [t.to_dict() for t in self.tensions],
            "syntheses": [s.to_dict() for s in self.syntheses],
        }


class DialecticSynthesizer:
    """Multi-perspective dialectic tension detector and third-way resolution engine."""

    def __init__(self, min_tension_threshold: float = 0.35) -> None:
        self.min_tension_threshold = min_tension_threshold
        self.poles: Dict[str, PolarityPole] = {}
        self.explicit_tensions: List[Tuple[str, str]] = []

    def load_dict(self, polarity_data: Dict[str, Any]) -> None:
        """Load polarity poles and explicit tensions from dictionary."""
        self.poles.clear()
        self.explicit_tensions.clear()

        poles_raw = polarity_data.get("poles", {})
        for p_id, p_info in poles_raw.items():
            self.poles[p_id] = PolarityPole(
                pole_id=p_id,
                name=p_info.get("name", p_id),
                core_values=list(p_info.get("core_values", [])),
                strengths=list(p_info.get("strengths", [])),
                overuse_vulnerabilities=list(p_info.get("overuse_vulnerabilities", [])),
                node_references=list(p_info.get("node_references", [])),
            )

        pairs = polarity_data.get("tensions", [])
        for pair in pairs:
            if len(pair) == 2:
                self.explicit_tensions.append((pair[0], pair[1]))

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract polarity poles and tension edges from an Obsidian .canvas structure."""
        self.poles.clear()
        self.explicit_tensions.clear()

        nodes = canvas_data.get("nodes", [])
        edges = canvas_data.get("edges", [])

        for node in nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            name = lines[0].lstrip("#").strip() if lines else n_id

            tags = re.findall(r"#([a-zA-Z0-9_\-]+)", text)
            words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
            stop_words = {"this", "that", "with", "from", "have", "were", "node", "canvas"}
            meaningful = [w for w in words if w not in stop_words]

            self.poles[n_id] = PolarityPole(
                pole_id=n_id,
                name=name,
                core_values=tags if tags else meaningful[:3],
                strengths=meaningful[3:6] if len(meaningful) > 3 else ["stability"],
                overuse_vulnerabilities=["rigidity" if "static" in text.lower() else "volatility"],
                node_references=[n_id],
            )

        # Detect conflict or trade-off edges
        for edge in edges:
            label = str(edge.get("label", "")).lower()
            from_n = str(edge.get("fromNode", ""))
            to_n = str(edge.get("toNode", ""))
            if any(k in label for k in ["vs", "conflict", "opposes", "tension", "tradeoff"]):
                self.explicit_tensions.append((from_n, to_n))

    def analyze_mesh(self) -> Tuple[List[DialecticTension], List[SyntheticResolution], SynthesisMeshTelemetry]:
        """Detect dialectic tensions and generate third-way synthetic resolutions."""
        if not self.poles:
            empty_telemetry = SynthesisMeshTelemetry(
                total_poles=0,
                tensions_detected=0,
                syntheses_generated=0,
                avg_tension_intensity=0.0,
                top_synthesis_rigor=0.0,
                dialectical_harmony_score=1.0,
            )
            return [], [], empty_telemetry

        # 1. Identify dialectic tension pairs
        tension_pairs: List[Tuple[PolarityPole, PolarityPole]] = []

        if self.explicit_tensions:
            for p1_id, p2_id in self.explicit_tensions:
                if p1_id in self.poles and p2_id in self.poles:
                    tension_pairs.append((self.poles[p1_id], self.poles[p2_id]))
        else:
            # Pairwise heuristics based on value divergence
            pole_list = list(self.poles.values())
            for i in range(len(pole_list)):
                for j in range(i + 1, len(pole_list)):
                    p1 = pole_list[i]
                    p2 = pole_list[j]
                    tension_pairs.append((p1, p2))

        tensions: List[DialecticTension] = []
        for idx, (p1, p2) in enumerate(tension_pairs, 1):
            t_id = f"tension_{idx}"
            v1 = set(p1.core_values)
            v2 = set(p2.core_values)
            shared = v1.intersection(v2)
            competing = v1.symmetric_difference(v2)

            # Tension intensity: high competing values and distinct overuse modes
            divergence = len(competing) / max(1, len(v1.union(v2)))
            intensity = min(1.0, max(0.2, (divergence * 0.6) + 0.3))

            # Oscillation risk: high if strengths are mutually exclusive
            osc_risk = round(min(1.0, intensity * 0.85 + 0.1), 2)

            tensions.append(
                DialecticTension(
                    tension_id=t_id,
                    thesis=p1,
                    antithesis=p2,
                    tension_intensity=intensity,
                    competing_attributes=sorted(list(competing)) if competing else ["scope_variance"],
                    shared_invariants=sorted(list(shared)) if shared else ["system_resilience"],
                    oscillation_risk=osc_risk,
                )
            )

        # Filter by threshold
        filtered_tensions = [t for t in tensions if t.tension_intensity >= self.min_tension_threshold]
        if not filtered_tensions and tensions:
            filtered_tensions = [tensions[0]]

        # 2. Generate Third-Way Synthetic Resolutions
        syntheses: List[SyntheticResolution] = []
        for idx, t in enumerate(filtered_tensions, 1):
            s_id = f"synth_{idx}"
            strategy, mechanisms, insight = self._derive_synthesis_strategy(t)

            # Compute synthesis rigor score
            rigor = round(min(1.0, 0.70 + (len(mechanisms) * 0.08) + (len(t.shared_invariants) * 0.05)), 2)

            syntheses.append(
                SyntheticResolution(
                    synthesis_id=s_id,
                    tension_id=t.tension_id,
                    title=f"Triadic Synthesis: {t.thesis.name} & {t.antithesis.name}",
                    strategy=strategy,
                    mechanisms=mechanisms,
                    retained_thesis_strengths=t.thesis.strengths[:2],
                    retained_antithesis_strengths=t.antithesis.strengths[:2],
                    synthesis_rigor_score=rigor,
                    integrative_insight=insight,
                )
            )

        avg_tension = sum(t.tension_intensity for t in filtered_tensions) / max(1, len(filtered_tensions))
        top_rigor = max([s.synthesis_rigor_score for s in syntheses]) if syntheses else 0.0
        harmony = round(min(1.0, top_rigor * (1.0 - (avg_tension * 0.25))), 2)

        telemetry = SynthesisMeshTelemetry(
            total_poles=len(self.poles),
            tensions_detected=len(filtered_tensions),
            syntheses_generated=len(syntheses),
            avg_tension_intensity=avg_tension,
            top_synthesis_rigor=top_rigor,
            dialectical_harmony_score=harmony,
            tensions=filtered_tensions,
            syntheses=syntheses,
        )

        return filtered_tensions, syntheses, telemetry

    def _derive_synthesis_strategy(
        self,
        tension: DialecticTension,
    ) -> Tuple[ResolutionStrategy, List[str], str]:
        """Select optimal resolution strategy and mechanisms based on pole semantics."""
        name_t = (tension.thesis.name + " " + " ".join(tension.thesis.core_values)).lower()
        name_a = (tension.antithesis.name + " " + " ".join(tension.antithesis.core_values)).lower()
        combined = name_t + " " + name_a

        if any(w in combined for w in ["speed", "latency", "throughput", "batch", "stream"]):
            return (
                ResolutionStrategy.TEMPORAL_DECOUPLING,
                ["Fast-path synchronous pipeline", "Asynchronous background reconciliation", "Dual-clock message bus"],
                "Decouples write-path velocity from heavy processing via asynchronous eventual consistency.",
            )
        elif any(w in combined for w in ["security", "isolation", "trust", "privacy", "access"]):
            return (
                ResolutionStrategy.DUAL_PLANE_ISOLATION,
                ["Separated control and data planes", "Cryptographic verifiable enclave", "Role-attenuated gateway"],
                "Enforces strict boundaries at the perimeter while maintaining friction-free internal data flow.",
            )
        elif any(w in combined for w in ["modular", "monolith", "central", "distributed", "local"]):
            return (
                ResolutionStrategy.HIERARCHICAL_TIERING,
                ["Tiered federated consensus", "Local autonomy micro-kernels", "Global invariant synchronization"],
                "Permits independent edge execution while preserving central structural coherence.",
            )
        elif any(w in combined for w in ["dynamic", "static", "flex", "strict", "adapt"]):
            return (
                ResolutionStrategy.ADAPTIVE_EQUILIBRIUM,
                ["Feedback-driven rate damping", "Dynamic headroom expansion", "Graceful degradation breakers"],
                "Maintains system stability by automatically modulating strictness relative to current stress.",
            )
        else:
            return (
                ResolutionStrategy.ORTHOGONAL_ABSTRACTION,
                ["Aspect-oriented abstraction layer", "Canonical intermediary representation", "Decoupled domain adapters"],
                "Synthesizes both concerns by factoring competing dimensions into orthogonal axes of variation.",
            )

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Dialectic Synthesis Mesh",
    ) -> Dict[str, Any]:
        """Export dialectic triads (Thesis, Antithesis, Synthesis) to Obsidian .canvas format."""
        tensions, syntheses, telemetry = self.analyze_mesh()

        canvas_nodes: List[Dict[str, Any]] = []
        canvas_edges: List[Dict[str, Any]] = []

        base_x = 100
        base_y = 100
        cluster_spacing_y = 480

        for idx, (t, s) in enumerate(zip(tensions, syntheses)):
            cy = base_y + idx * cluster_spacing_y

            # Thesis Node (Color 1: Red/Coral)
            thesis_id = f"node_{t.thesis.pole_id}"
            canvas_nodes.append({
                "id": thesis_id,
                "x": base_x,
                "y": cy,
                "width": 300,
                "height": 180,
                "type": "text",
                "text": f"### THESIS: {t.thesis.name}\n**Values:** {', '.join(t.thesis.core_values)}\n\n**Strengths:**\n- " + "\n- ".join(t.thesis.strengths[:2]),
                "color": "1",
            })

            # Antithesis Node (Color 5: Blue/Purple)
            antithesis_id = f"node_{t.antithesis.pole_id}"
            canvas_nodes.append({
                "id": antithesis_id,
                "x": base_x + 720,
                "y": cy,
                "width": 300,
                "height": 180,
                "type": "text",
                "text": f"### ANTITHESIS: {t.antithesis.name}\n**Values:** {', '.join(t.antithesis.core_values)}\n\n**Strengths:**\n- " + "\n- ".join(t.antithesis.strengths[:2]),
                "color": "5",
            })

            # Synthesis Node (Color 4: Green / Emergent Resolution)
            synth_node_id = f"node_{s.synthesis_id}"
            canvas_nodes.append({
                "id": synth_node_id,
                "x": base_x + 360,
                "y": cy + 180,
                "width": 320,
                "height": 220,
                "type": "text",
                "text": f"### SYNTHESIS: {s.title}\n**Strategy:** `{s.strategy.value}` (Rigor: {s.synthesis_rigor_score:.0%})\n\n**Integrative Insight:**\n{s.integrative_insight}\n\n**Mechanisms:**\n- " + "\n- ".join(s.mechanisms[:2]),
                "color": "4",
            })

            # Edges: Conflict edge between Thesis and Antithesis
            canvas_edges.append({
                "id": f"edge_tension_{idx}",
                "fromNode": thesis_id,
                "fromSide": "right",
                "toNode": antithesis_id,
                "toSide": "left",
                "label": f"Tension: {t.tension_intensity:.2f} (Oscillation: {t.oscillation_risk:.0%})",
                "color": "1",
            })

            # Edges: Converging into Synthesis
            canvas_edges.append({
                "id": f"edge_synth_t_{idx}",
                "fromNode": thesis_id,
                "fromSide": "bottom",
                "toNode": synth_node_id,
                "toSide": "top",
                "label": "Transcended",
                "color": "4",
            })
            canvas_edges.append({
                "id": f"edge_synth_a_{idx}",
                "fromNode": antithesis_id,
                "fromSide": "bottom",
                "toNode": synth_node_id,
                "toSide": "top",
                "label": "Integrated",
                "color": "4",
            })

        canvas_json = {
            "title": canvas_title,
            "nodes": canvas_nodes,
            "edges": canvas_edges,
        }

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(canvas_json, f, indent=2)

        return canvas_json

    def to_svg(
        self,
        output_path: Optional[str] = None,
        width: int = 1200,
        height: int = 750,
    ) -> str:
        """Render publication-grade SVG triadic dialectic synthesis diagram."""
        tensions, syntheses, telemetry = self.analyze_mesh()

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <linearGradient id="thesisGrad" x1="0" y1="0" x2="1" y2="1">',
            '    <stop offset="0%" stop-color="#EF4444" stop-opacity="0.2"/>',
            '    <stop offset="100%" stop-color="#B91C1C" stop-opacity="0.05"/>',
            '  </linearGradient>',
            '  <linearGradient id="antithesisGrad" x1="0" y1="0" x2="1" y2="1">',
            '    <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.2"/>',
            '    <stop offset="100%" stop-color="#1D4ED8" stop-opacity="0.05"/>',
            '  </linearGradient>',
            '  <linearGradient id="synthGrad" x1="0" y1="0" x2="0" y2="1">',
            '    <stop offset="0%" stop-color="#10B981" stop-opacity="0.25"/>',
            '    <stop offset="100%" stop-color="#047857" stop-opacity="0.08"/>',
            '  </linearGradient>',
            '  <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">',
            '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.5"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Multi-Perspective Dialectic Synthesizer &amp; Synthesis Mesh</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Hegelian Triads: {telemetry.tensions_detected} Tensions | {telemetry.syntheses_generated} Resolutions | Dialectical Harmony: {telemetry.dialectical_harmony_score:.2f}</text>',
        ]

        # Draw first tension triad prominently
        if tensions and syntheses:
            t = tensions[0]
            s = syntheses[0]

            tx, ty = 240, 200
            ax, ay = 800, 200
            sx, sy = 520, 480

            # Tension vector spring (dashed red line)
            svg_parts.append('<!-- Tension Vector -->')
            svg_parts.append(
                f'<line x1="{tx + 120}" y1="{ty + 50}" x2="{ax - 120}" y2="{ay + 50}" '
                f'stroke="#EF4444" stroke-width="2.5" stroke-dasharray="8,5" opacity="0.8"/>'
            )
            svg_parts.append(
                f'<rect x="460" y="190" width="120" height="24" rx="4" fill="#450A0A" stroke="#EF4444" stroke-width="1"/>'
            )
            svg_parts.append(
                f'<text x="520" y="206" font-size="11" font-weight="700" fill="#FCA5A5" text-anchor="middle">Tension: {t.tension_intensity:.2f}</text>'
            )

            # Converging resolution lines (green)
            svg_parts.append('<!-- Synthetic Integration Bridges -->')
            svg_parts.append(
                f'<path d="M {tx} {ty + 90} Q {tx} {sy} {sx - 140} {sy + 40}" fill="none" stroke="#10B981" stroke-width="2.5"/>'
            )
            svg_parts.append(
                f'<path d="M {ax} {ay + 90} Q {ax} {sy} {sx + 140} {sy + 40}" fill="none" stroke="#10B981" stroke-width="2.5"/>'
            )

            # Thesis Card
            svg_parts.append(
                f'<g transform="translate({tx - 120}, {ty})" filter="url(#shadow)">'
                f'  <rect width="240" height="110" rx="8" fill="#1E293B" stroke="#EF4444" stroke-width="2"/>'
                f'  <text x="16" y="26" font-size="12" font-weight="700" fill="#FCA5A5">THESIS: {t.thesis.name[:18]}</text>'
                f'  <text x="16" y="50" font-size="10" fill="#94A3B8">Values: <tspan fill="#F8FAFC">{", ".join(t.thesis.core_values[:2])}</tspan></text>'
                f'  <text x="16" y="72" font-size="10" fill="#94A3B8">Strength: <tspan fill="#38BDF8">{t.thesis.strengths[0] if t.thesis.strengths else "Focus"}</tspan></text>'
                f'  <text x="16" y="94" font-size="9" fill="#EF4444">Risk: {t.thesis.overuse_vulnerabilities[0] if t.thesis.overuse_vulnerabilities else "Rigidity"}</text>'
                f'</g>'
            )

            # Antithesis Card
            svg_parts.append(
                f'<g transform="translate({ax - 120}, {ay})" filter="url(#shadow)">'
                f'  <rect width="240" height="110" rx="8" fill="#1E293B" stroke="#3B82F6" stroke-width="2"/>'
                f'  <text x="16" y="26" font-size="12" font-weight="700" fill="#93C5FD">ANTITHESIS: {t.antithesis.name[:18]}</text>'
                f'  <text x="16" y="50" font-size="10" fill="#94A3B8">Values: <tspan fill="#F8FAFC">{", ".join(t.antithesis.core_values[:2])}</tspan></text>'
                f'  <text x="16" y="72" font-size="10" fill="#94A3B8">Strength: <tspan fill="#38BDF8">{t.antithesis.strengths[0] if t.antithesis.strengths else "Speed"}</tspan></text>'
                f'  <text x="16" y="94" font-size="9" fill="#3B82F6">Risk: {t.antithesis.overuse_vulnerabilities[0] if t.antithesis.overuse_vulnerabilities else "Volatility"}</text>'
                f'</g>'
            )

            # Synthesis Node
            svg_parts.append(
                f'<g transform="translate({sx - 150}, {sy})" filter="url(#shadow)">'
                f'  <rect width="300" height="130" rx="10" fill="#064E3B" stroke="#10B981" stroke-width="2.5"/>'
                f'  <text x="20" y="28" font-size="13" font-weight="700" fill="#ECFDF5">SYNTHESIS (Aufhebung)</text>'
                f'  <text x="20" y="50" font-size="10" font-weight="600" fill="#A7F3D0">Strategy: {s.strategy.value}</text>'
                f'  <text x="20" y="70" font-size="9" fill="#D1FAE5">{s.integrative_insight[:42]}...</text>'
                f'  <text x="20" y="92" font-size="9" fill="#6EE7B7">1. {s.mechanisms[0] if s.mechanisms else "Decoupled plane"}</text>'
                f'  <text x="20" y="110" font-size="9" fill="#6EE7B7">2. {s.mechanisms[1] if len(s.mechanisms) > 1 else "Eventual convergence"}</text>'
                f'</g>'
            )

        # Telemetry Legend
        legend_x = width - 260
        legend_y = height - 145
        svg_parts.append('<!-- Telemetry Legend -->')
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="230" height="115" rx="6" '
            f'fill="#0F172A" stroke="#1E293B" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Dialectic Synthesis Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Tension Intensity: <tspan fill="#EF4444">{telemetry.avg_tension_intensity:.2f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Synthesis Rigor: <tspan fill="#10B981">{telemetry.top_synthesis_rigor:.2f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Dialectical Harmony: <tspan fill="#38BDF8">{telemetry.dialectical_harmony_score:.2f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">Johnson Polarity Management</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_mesh(self, telemetry: SynthesisMeshTelemetry) -> str:
        """Format an accessible ASCII dialectic synthesis report for the terminal."""
        lines = [
            "=" * 68,
            "  Dialectic Synthesis Mesh & Third-Way Resolution Report",
            "=" * 68,
            f"  Total Architectural Poles:  {telemetry.total_poles}",
            f"  Dialectic Tensions:         {telemetry.tensions_detected}",
            f"  Synthetic Resolutions:      {telemetry.syntheses_generated}",
            f"  Average Tension Intensity:  {telemetry.avg_tension_intensity:.2f}",
            f"  Top Synthesis Rigor Score:  {telemetry.top_synthesis_rigor:.2f}",
            f"  Dialectical Harmony Score:  {telemetry.dialectical_harmony_score:.2f}",
            "-" * 68,
            "  [DIALECTIC TRIADS & RESOLUTIONS]:",
        ]

        for idx, (t, s) in enumerate(zip(telemetry.tensions, telemetry.syntheses), 1):
            lines.append(f"  Triad #{idx}:")
            lines.append(f"    THESIS:     {t.thesis.name} (Core: {', '.join(t.thesis.core_values[:2])})")
            lines.append(f"    ANTITHESIS: {t.antithesis.name} (Core: {', '.join(t.antithesis.core_values[:2])})")
            lines.append(f"    TENSION:    Intensity: {t.tension_intensity:.2f} | Oscillation Risk: {t.oscillation_risk:.0%}")
            lines.append(f"    SYNTHESIS:  {s.title}")
            lines.append(f"      Strategy: {s.strategy.value} (Rigor: {s.synthesis_rigor_score:.0%})")
            lines.append(f"      Insight:  {s.integrative_insight}")
            lines.append(f"      Decoupling Mechanisms:")
            for m in s.mechanisms[:2]:
                lines.append(f"        * {m}")
            if idx < len(telemetry.tensions):
                lines.append("-" * 68)

        lines.append("=" * 68)
        return "\n".join(lines)
