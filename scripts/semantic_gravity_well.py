"""
Semantic Gravity Well & Conceptual Orbit Engine
Autonomous cognitive spatial module for anchoring subordinate arguments
and conceptual satellites around core thesis pillars using stable Keplerian
orbital mechanics and gravitational potential wells. Grounded in Eide & Eide
M-I-N-D framework, Cowan working memory bounds, and spatial schema stabilization.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import html


@dataclass
class ConceptualBody:
    """Represents a conceptual entity within a semantic gravity system."""
    body_id: str
    title: str
    mass: float  # Centrality/significance weight (e.g., 5.0 to 100.0)
    domain_tag: str
    affinity_to_core: float  # 0.0 to 1.0 semantic proximity
    initial_theta_rad: float = 0.0


@dataclass
class OrbitalBodyState:
    """Calculated Keplerian orbital state of a subordinate concept."""
    body: ConceptualBody
    orbit_index: int
    semi_major_axis_px: float
    semi_minor_axis_px: float
    eccentricity: float
    orbital_period_s: float
    current_theta_rad: float
    pos_x: float
    pos_y: float
    escape_risk: float
    stability_status: str  # locked, resonant, metastable, divergent


@dataclass
class GravityWellTelemetry:
    """Comprehensive telemetry report for a semantic gravity system."""
    core_id: str
    core_title: str
    core_mass: float
    capture_radius_px: float
    escape_radius_px: float
    total_satellites: int
    orbit_count: int
    mean_stability_score: float
    cowan_overflow_count: int
    orbital_states: List[OrbitalBodyState] = field(default_factory=list)


class SemanticGravityWell:
    """
    Autonomous engine that positions conceptual satellites into stable
    multi-body orbital trajectories around a central thesis attractor.
    Eliminates graph clutter and force-directed jitter by providing deterministic,
    harmonic Keplerian ellipses.
    """

    def __init__(
        self,
        gravitational_constant_g: float = 15000.0,
        base_orbit_radius_px: float = 95.0,
        orbit_spacing_factor: float = 1.42,
        max_eccentricity: float = 0.40,
    ):
        self.g = max(100.0, float(gravitational_constant_g))
        self.base_radius = max(30.0, float(base_orbit_radius_px))
        self.spacing_factor = max(1.1, float(orbit_spacing_factor))
        self.max_eccentricity = min(0.8, max(0.0, float(max_eccentricity)))

    def calculate_capture_radius(self, core_mass: float) -> float:
        """Calculate effective gravitational capture perimeter in pixels."""
        return math.sqrt(self.g * max(1.0, core_mass)) * 1.8

    def calculate_escape_velocity(self, core_mass: float, radius_px: float) -> float:
        """Calculate local escape velocity threshold."""
        r = max(10.0, radius_px)
        return math.sqrt(2.0 * self.g * max(1.0, core_mass) / r)

    def solve_orbital_system(
        self,
        core: ConceptualBody,
        satellites: List[ConceptualBody],
        time_offset_s: float = 0.0,
        center_x: float = 460.0,
        center_y: float = 280.0,
    ) -> GravityWellTelemetry:
        """
        Calculates harmonic orbital planes, eccentricities, and coordinates
        for all subordinate concepts orbiting the central core thesis.
        """
        capture_radius = self.calculate_capture_radius(core.mass)
        escape_radius = capture_radius * 1.65

        # Sort satellites by descending affinity (closest affinity -> innermost orbit)
        sorted_satellites = sorted(
            satellites,
            key=lambda s: (s.affinity_to_core, s.mass),
            reverse=True,
        )

        orbital_states: List[OrbitalBodyState] = []
        cowan_overflow = max(0, len(satellites) - 4)

        for idx, sat in enumerate(sorted_satellites):
            orbit_idx = idx + 1
            # Harmonic radius scaling
            semi_major = self.base_radius * math.pow(self.spacing_factor, float(idx) * 0.75)
            
            # Eccentricity scales inversely with affinity (high affinity = circular, low = elongated)
            raw_ecc = (1.0 - min(1.0, max(0.0, sat.affinity_to_core))) * self.max_eccentricity
            eccentricity = round(raw_ecc, 3)
            semi_minor = semi_major * math.sqrt(max(0.01, 1.0 - eccentricity * eccentricity))

            # Kepler Third Law: T^2 proportional to a^3
            # Period in simulated seconds
            period_s = max(4.0, 2.0 * math.pi * math.sqrt(math.pow(semi_major, 3) / (self.g * core.mass)))
            
            # Angular velocity
            omega = 2.0 * math.pi / period_s
            theta = (sat.initial_theta_rad + omega * time_offset_s + (idx * 1.35)) % (2.0 * math.pi)

            # Elliptical coordinates centered at focal point (center_x, center_y)
            # Distance from center to ellipse focus = c = a * e
            focus_c = semi_major * eccentricity
            pos_x = center_x + semi_major * math.cos(theta) - focus_c
            pos_y = center_y + semi_minor * math.sin(theta)

            # Escape risk metric
            effective_dist = math.hypot(pos_x - center_x, pos_y - center_y)
            escape_risk = min(1.0, max(0.0, (effective_dist - capture_radius * 0.7) / (escape_radius - capture_radius * 0.7 + 1e-5)))

            if escape_risk > 0.75:
                stability = "divergent"
            elif escape_risk > 0.45:
                stability = "metastable"
            elif eccentricity > 0.25:
                stability = "resonant"
            else:
                stability = "locked"

            orbital_states.append(
                OrbitalBodyState(
                    body=sat,
                    orbit_index=orbit_idx,
                    semi_major_axis_px=round(semi_major, 2),
                    semi_minor_axis_px=round(semi_minor, 2),
                    eccentricity=eccentricity,
                    orbital_period_s=round(period_s, 2),
                    current_theta_rad=round(theta, 3),
                    pos_x=round(pos_x, 2),
                    pos_y=round(pos_y, 2),
                    escape_risk=round(escape_risk, 3),
                    stability_status=stability,
                )
            )

        mean_stability = (
            sum(1.0 - s.escape_risk for s in orbital_states) / len(orbital_states)
            if orbital_states
            else 1.0
        )

        return GravityWellTelemetry(
            core_id=core.body_id,
            core_title=core.title,
            core_mass=core.mass,
            capture_radius_px=round(capture_radius, 2),
            escape_radius_px=round(escape_radius, 2),
            total_satellites=len(orbital_states),
            orbit_count=len(orbital_states),
            mean_stability_score=round(mean_stability, 3),
            cowan_overflow_count=cowan_overflow,
            orbital_states=orbital_states,
        )

    def generate_markdown_report(self, telemetry: GravityWellTelemetry) -> str:
        """Generates a structured markdown audit report with zero em dashes."""
        lines = [
            "# Semantic Gravity Well and Conceptual Orbit Telemetry",
            "",
            "## 1. Core Thesis Attractor Overview",
            f"- **Core Concept ID:** `{telemetry.core_id}`",
            f"- **Core Concept Title:** {telemetry.core_title}",
            f"- **Central Attractor Mass:** {telemetry.core_mass} units",
            f"- **Gravitational Capture Perimeter:** {telemetry.capture_radius_px} px",
            f"- **Escape Threshold Horizon:** {telemetry.escape_radius_px} px",
            f"- **Active Satellites:** {telemetry.total_satellites}",
            f"- **Mean System Stability:** {round(telemetry.mean_stability_score * 100.0, 1)}%",
            f"- **Cowan Capacity Bound (N <= 4):** {'OPTIMAL' if telemetry.cowan_overflow_count == 0 else f'WARNING ({telemetry.cowan_overflow_count} satellites overflow)'}",
            "",
            "## 2. Theoretical Grounding",
            "- **Keplerian Harmonic Distribution:** Elliptical orbits prevent cognitive collision and visual spaghetti.",
            "- **Cowan Memory Bound:** Constraining immediate core orbits to 4 active bodies minimizes executive cognitive load.",
            "- **Gravitational Escape Risk:** High eccentricity or distance flags concepts drifting into unrelated tangents.",
            "",
            "## 3. Subordinate Concept Orbital Breakdown",
            "| ID | Title | Domain | Semi-Major (px) | Eccentricity | Period (s) | Escape Risk | State |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for s in telemetry.orbital_states:
            lines.append(
                f"| `{s.body.body_id}` | {s.body.title} | {s.body.domain_tag} | {s.semi_major_axis_px} | {s.eccentricity} | {s.orbital_period_s} | {round(s.escape_risk * 100.0, 1)}% | `{s.stability_status}` |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Guidance",
            "- Satellites marked as 'divergent' should be split into independent gravity wells or pruned.",
            "- Satellites in 'resonant' orbits provide optimal dialectical counter-arguments with balanced tension.",
            "- Maintain negative spatial margins between concentric orbital tracks to eliminate reading fatigue.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: GravityWellTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates a publication-grade dark titanium SVG diagram of the semantic gravity system."""
        center_x = width // 2
        center_y = height // 2

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d16; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9"/>',
            '    <stop offset="40%" stop-color="#0284c7" stop-opacity="0.5"/>',
            '    <stop offset="100%" stop-color="#0284c7" stop-opacity="0"/>',
            '  </radialGradient>',
            '  <radialGradient id="captureGlow" cx="50%" cy="50%" r="50%">',
            '    <stop offset="0%" stop-color="#0284c7" stop-opacity="0.08"/>',
            '    <stop offset="85%" stop-color="#38bdf8" stop-opacity="0.03"/>',
            '    <stop offset="100%" stop-color="#090d16" stop-opacity="0"/>',
            '  </radialGradient>',
            '  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity="0.6"/>',
            '  </filter>',
            '</defs>',
            '<!-- Background Grid -->',
            '<g opacity="0.15">',
        ]

        # Grid lines
        for gx in range(40, width, 60):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#334155" stroke-width="0.5" stroke-dasharray="2,4"/>')
        for gy in range(40, height, 60):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#334155" stroke-width="0.5" stroke-dasharray="2,4"/>')
        svg_parts.append('</g>')

        # Capture perimeter
        svg_parts.append(
            f'<circle cx="{center_x}" cy="{center_y}" r="{telemetry.capture_radius_px}" fill="url(#captureGlow)" stroke="#0284c7" stroke-width="1.2" stroke-dasharray="4,6" opacity="0.5"/>'
        )

        # Concentric Keplerian orbits
        for state in telemetry.orbital_states:
            focus_c = state.semi_major_axis_px * state.eccentricity
            ellipse_cx = center_x - focus_c
            svg_parts.append(
                f'<ellipse cx="{ellipse_cx}" cy="{center_y}" rx="{state.semi_major_axis_px}" ry="{state.semi_minor_axis_px}" fill="none" stroke="#475569" stroke-width="1.0" stroke-dasharray="3,5" opacity="0.6"/>'
            )

        # Tether lines from core to satellites
        for state in telemetry.orbital_states:
            tether_color = "#38bdf8" if state.stability_status in ["locked", "resonant"] else "#f59e0b"
            if state.stability_status == "divergent":
                tether_color = "#ef4444"
            svg_parts.append(
                f'<line x1="{center_x}" y1="{center_y}" x2="{state.pos_x}" y2="{state.pos_y}" stroke="{tether_color}" stroke-width="0.8" stroke-dasharray="2,3" opacity="0.4"/>'
            )

        # Core Thesis Well
        core_r = max(18.0, min(36.0, math.sqrt(telemetry.core_mass) * 3.2))
        svg_parts.append(
            f'<circle cx="{center_x}" cy="{center_y}" r="{core_r * 2.2}" fill="url(#coreGlow)"/>'
        )
        svg_parts.append(
            f'<circle cx="{center_x}" cy="{center_y}" r="{core_r}" fill="#0284c7" stroke="#38bdf8" stroke-width="2.5" filter="url(#shadow)"/>'
        )
        svg_parts.append(
            f'<text x="{center_x}" y="{center_y + 4}" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">{html.escape(telemetry.core_title[:18])}</text>'
        )

        # Orbiting Satellites
        for state in telemetry.orbital_states:
            node_r = max(9.0, min(18.0, math.sqrt(state.body.mass) * 3.0))
            if state.stability_status == "locked":
                fill_col = "#0ea5e9"
                stroke_col = "#38bdf8"
            elif state.stability_status == "resonant":
                fill_col = "#10b981"
                stroke_col = "#34d399"
            elif state.stability_status == "metastable":
                fill_col = "#d97706"
                stroke_col = "#fbbf24"
            else:
                fill_col = "#dc2626"
                stroke_col = "#f87171"

            svg_parts.append(
                f'<circle cx="{state.pos_x}" cy="{state.pos_y}" r="{node_r}" fill="{fill_col}" stroke="{stroke_col}" stroke-width="1.8" filter="url(#shadow)"/>'
            )
            # Label
            label_y = state.pos_y + node_r + 13
            svg_parts.append(
                f'<text x="{state.pos_x}" y="{label_y}" font-size="10" font-weight="600" fill="#e2e8f0" text-anchor="middle">{html.escape(state.body.title)}</text>'
            )
            # Sub-badge (status and period)
            badge_y = label_y + 11
            svg_parts.append(
                f'<text x="{state.pos_x}" y="{badge_y}" font-size="8" fill="#94a3b8" text-anchor="middle">T={state.orbital_period_s}s ({state.stability_status})</text>'
            )

        # Telemetry Header HUD
        svg_parts.append(
            f'<rect x="20" y="16" width="310" height="74" rx="8" fill="#0f172a" fill-opacity="0.85" stroke="#1e293b" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="32" y="36" font-size="11" font-weight="700" fill="#38bdf8">SEMANTIC GRAVITY WELL ENGINE</text>'
        )
        svg_parts.append(
            f'<text x="32" y="52" font-size="9" fill="#94a3b8">Core Mass: {telemetry.core_mass} | Satellites: {telemetry.total_satellites}</text>'
        )
        svg_parts.append(
            f'<text x="32" y="68" font-size="9" fill="#94a3b8">Stability Score: {round(telemetry.mean_stability_score * 100.0, 1)}% | Cowan Bound: {telemetry.cowan_overflow_count} overflow</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_semantic_system() -> Tuple[ConceptualBody, List[ConceptualBody]]:
    """Provides demonstration conceptual hierarchy for spatial architecture."""
    core = ConceptualBody(
        body_id="core-thesis",
        title="Spatial Schemas",
        mass=64.0,
        domain_tag="cognitive_architecture",
        affinity_to_core=1.0,
    )

    satellites = [
        ConceptualBody(
            body_id="sat-1",
            title="Nonlinear Synthesis",
            mass=25.0,
            domain_tag="epistemology",
            affinity_to_core=0.92,
            initial_theta_rad=0.3,
        ),
        ConceptualBody(
            body_id="sat-2",
            title="Saccadic Pacing",
            mass=18.0,
            domain_tag="ocular_ergonomics",
            affinity_to_core=0.85,
            initial_theta_rad=1.8,
        ),
        ConceptualBody(
            body_id="sat-3",
            title="Working Memory Shield",
            mass=16.0,
            domain_tag="cognitive_bandwidth",
            affinity_to_core=0.74,
            initial_theta_rad=3.5,
        ),
        ConceptualBody(
            body_id="sat-4",
            title="Dialectic Resolution",
            mass=12.0,
            domain_tag="reasoning_loom",
            affinity_to_core=0.62,
            initial_theta_rad=4.9,
        ),
        ConceptualBody(
            body_id="sat-5",
            title="Edge Case Divergence",
            mass=8.0,
            domain_tag="multiverse_branching",
            affinity_to_core=0.28,
            initial_theta_rad=0.9,
        ),
    ]

    return core, satellites
