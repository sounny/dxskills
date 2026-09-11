"""
Topological Fiber Bundle & Polytope Holonomy Weaver
Autonomous cognitive spatial module modeling non-trivial conceptual manifolds,
parallel transport, and geometric phase holonomy across closed cognitive loops.
Grounded in differential geometry, fiber bundle topology (E, B, pi, F),
and Berry-Pancharatnam geometric phase mechanics for high-dimensional spatial reasoning.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json


@dataclass
class FiberVector:
    """Represents a directional perspective vector transported along a base concept manifold."""
    t: float
    base_x: float
    base_y: float
    base_z: float
    fiber_angle_deg: float
    vector_dx: float
    vector_dy: float
    vector_dz: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "t": round(self.t, 3),
            "base_x": round(self.base_x, 2),
            "base_y": round(self.base_y, 2),
            "base_z": round(self.base_z, 2),
            "fiber_angle_deg": round(self.fiber_angle_deg, 2),
            "vector_dx": round(self.vector_dx, 3),
            "vector_dy": round(self.vector_dy, 3),
            "vector_dz": round(self.vector_dz, 3),
        }


@dataclass
class HolonomyTelemetry:
    """Synthesized telemetry summarizing fiber bundle parallel transport and geometric phase."""
    bundle_type: str                  # MOBIUS_STRIP, HOPF_FIBRATION, TORUS_KNOT, CYLINDER_TRIVIAL
    total_steps: int
    loop_perimeter_px: float
    total_twist_deg: float
    holonomy_angle_deg: float
    is_non_trivial_topology: bool
    connection_curvature_integral: float
    fibers: List[FiberVector]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bundle_type": self.bundle_type,
            "total_steps": self.total_steps,
            "loop_perimeter_px": round(self.loop_perimeter_px, 1),
            "total_twist_deg": round(self.total_twist_deg, 2),
            "holonomy_angle_deg": round(self.holonomy_angle_deg, 2),
            "is_non_trivial_topology": self.is_non_trivial_topology,
            "connection_curvature_integral": round(self.connection_curvature_integral, 3),
            "fiber_count": len(self.fibers),
            "warnings": self.warnings,
        }


class TopologicalFiberBundle:
    """
    Simulates non-trivial topological fiber bundles and computes parallel transport
    holonomy along closed cognitive loops to support non-linear conceptual navigation.
    """

    def __init__(self, twist_parameter: float = 1.0):
        self.twist_parameter = twist_parameter

    def weave_mobius_bundle(
        self,
        radius_px: float = 160.0,
        fiber_length_px: float = 55.0,
        steps: int = 64,
        center_x: float = 450.0,
        center_y: float = 260.0,
        twist_factor: float = 1.0,
    ) -> HolonomyTelemetry:
        """
        Weave a non-trivial Mobius fiber bundle over a circular base manifold S^1 with fiber [-1, 1].
        A twist factor of 1.0 produces a 180-degree holonomy shift upon full loop traversal.
        """
        fibers: List[FiberVector] = []
        total_perimeter = 2.0 * math.pi * radius_px
        total_twist_deg = 180.0 * twist_factor

        for i in range(steps):
            t = i / float(steps)
            theta = 2.0 * math.pi * t
            # Base manifold circle S^1
            bx = center_x + radius_px * math.cos(theta)
            by = center_y + radius_px * math.sin(theta)
            bz = 0.0

            # Fiber orientation angle with half-integer twist
            phi = (theta * 0.5) * twist_factor
            phi_deg = math.degrees(phi) % 360.0

            # Vector component along fiber direction
            v_dx = math.cos(phi) * (fiber_length_px * 0.5)
            v_dy = math.sin(phi) * (fiber_length_px * 0.5)
            v_dz = math.sin(theta) * 15.0

            fibers.append(
                FiberVector(
                    t=t,
                    base_x=bx,
                    base_y=by,
                    base_z=bz,
                    fiber_angle_deg=phi_deg,
                    vector_dx=v_dx,
                    vector_dy=v_dy,
                    vector_dz=v_dz,
                )
            )

        # Holonomy is net angular difference between start and end vectors
        holonomy_deg = total_twist_deg % 360.0
        is_non_trivial = abs(holonomy_deg - 0.0) > 1e-4

        warnings = []
        if is_non_trivial:
            warnings.append(
                f"Non-trivial holonomy detected: {holonomy_deg:.1f} deg phase rotation upon loop closure."
            )

        return HolonomyTelemetry(
            bundle_type="MOBIUS_STRIP",
            total_steps=steps,
            loop_perimeter_px=total_perimeter,
            total_twist_deg=total_twist_deg,
            holonomy_angle_deg=holonomy_deg,
            is_non_trivial_topology=is_non_trivial,
            connection_curvature_integral=math.pi * twist_factor,
            fibers=fibers,
            warnings=warnings,
        )

    def weave_hopf_fibration(
        self,
        base_radius_px: float = 140.0,
        fiber_circle_radius_px: float = 38.0,
        steps: int = 48,
        center_x: float = 450.0,
        center_y: float = 260.0,
        fiber_twist: float = 1.0,
    ) -> HolonomyTelemetry:
        """
        Weave a discrete Hopf fibration projection (S^3 -> S^2 with S^1 fibers).
        Maps points on base 2-sphere to nested circular fibers with linked topological winding.
        """
        fibers: List[FiberVector] = []
        total_perimeter = 2.0 * math.pi * base_radius_px

        for i in range(steps):
            t = i / float(steps)
            theta = 2.0 * math.pi * t
            # Base manifold on S^2 projection
            bx = center_x + base_radius_px * math.cos(theta)
            by = center_y + (base_radius_px * 0.65) * math.sin(theta)
            bz = base_radius_px * 0.35 * math.cos(2.0 * theta)

            # Hopf linking fiber angle
            fiber_angle = (theta * fiber_twist)
            fiber_deg = math.degrees(fiber_angle) % 360.0

            v_dx = fiber_circle_radius_px * math.cos(fiber_angle)
            v_dy = fiber_circle_radius_px * math.sin(fiber_angle)
            v_dz = fiber_circle_radius_px * 0.5 * math.sin(2.0 * fiber_angle)

            fibers.append(
                FiberVector(
                    t=t,
                    base_x=bx,
                    base_y=by,
                    base_z=bz,
                    fiber_angle_deg=fiber_deg,
                    vector_dx=v_dx,
                    vector_dy=v_dy,
                    vector_dz=v_dz,
                )
            )

        holonomy_deg = (360.0 * fiber_twist) % 360.0
        return HolonomyTelemetry(
            bundle_type="HOPF_FIBRATION",
            total_steps=steps,
            loop_perimeter_px=total_perimeter,
            total_twist_deg=360.0 * fiber_twist,
            holonomy_angle_deg=holonomy_deg,
            is_non_trivial_topology=True,
            connection_curvature_integral=2.0 * math.pi * fiber_twist,
            fibers=fibers,
            warnings=["Hopf invariant linking number Q=1 confirms non-trivial bundle topology."],
        )

    def weave_torus_bundle(
        self,
        major_radius_px: float = 170.0,
        minor_radius_px: float = 50.0,
        p_winds: int = 2,
        q_winds: int = 3,
        steps: int = 72,
        center_x: float = 450.0,
        center_y: float = 260.0,
    ) -> HolonomyTelemetry:
        """
        Weave a (p, q) torus knot bundle where fiber directions rotate around toroidal coordinates.
        """
        fibers: List[FiberVector] = []
        total_len = 0.0
        prev_x, prev_y = None, None

        for i in range(steps):
            t = i / float(steps)
            phi = 2.0 * math.pi * p_winds * t
            theta = 2.0 * math.pi * q_winds * t

            r = major_radius_px + minor_radius_px * math.cos(theta)
            bx = center_x + r * math.cos(phi)
            by = center_y + (r * 0.65) * math.sin(phi) + minor_radius_px * 0.5 * math.sin(theta)
            bz = minor_radius_px * math.sin(theta)

            if prev_x is not None and prev_y is not None:
                total_len += math.hypot(bx - prev_x, by - prev_y)
            prev_x, prev_y = bx, by

            fiber_angle = theta
            fiber_deg = math.degrees(fiber_angle) % 360.0

            v_dx = 25.0 * math.cos(fiber_angle)
            v_dy = 25.0 * math.sin(fiber_angle)
            v_dz = 15.0 * math.cos(phi)

            fibers.append(
                FiberVector(
                    t=t,
                    base_x=bx,
                    base_y=by,
                    base_z=bz,
                    fiber_angle_deg=fiber_deg,
                    vector_dx=v_dx,
                    vector_dy=v_dy,
                    vector_dz=v_dz,
                )
            )

        holonomy_deg = (360.0 * (q_winds / float(p_winds))) % 360.0
        return HolonomyTelemetry(
            bundle_type="TORUS_KNOT",
            total_steps=steps,
            loop_perimeter_px=total_len,
            total_twist_deg=360.0 * q_winds,
            holonomy_angle_deg=holonomy_deg,
            is_non_trivial_topology=True,
            connection_curvature_integral=2.0 * math.pi * q_winds,
            fibers=fibers,
            warnings=[f"Torus knot ({p_winds}, {q_winds}) produces non-trivial fundamental group winding."],
        )

    def render_fiber_bundle_svg(
        self,
        telemetry: HolonomyTelemetry,
        width: int = 920,
        height: int = 560
    ) -> str:
        """
        Render publication-grade dark titanium SVG diagram showing the base loop manifold,
        parallel transported fiber vectors, ribbon surfaces, and holonomy gauge meters.
        """
        bg_color = "#0b0f14"
        card_color = "#121820"
        border_color = "#1f2937"
        text_primary = "#f3f4f6"
        text_muted = "#9ca3af"
        accent_cyan = "#00e5ff"
        accent_purple = "#7c4dff"
        accent_amber = "#ffab00"
        accent_green = "#00e676"

        # Construct base loop polyline
        base_pts = [f"{f.base_x:.1f},{f.base_y:.1f}" for f in telemetry.fibers]
        if base_pts:
            base_pts.append(base_pts[0])  # Close loop
        base_polyline = " ".join(base_pts)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: {bg_color}; '
            'font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <linearGradient id="fiberGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.9"/>',
            '    <stop offset="100%" stop-color="#7c4dff" stop-opacity="0.9"/>',
            '  </linearGradient>',
            '  <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="2.5" result="blur" />',
            '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            '  </filter>',
            '  <filter id="glowPurple" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            '  </filter>',
            '</defs>',
            '<!-- Subtle background coordinate grid -->',
            '<g opacity="0.07" stroke="#ffffff" stroke-width="1">',
        ]

        for gx in range(0, width, 40):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" />')
        for gy in range(0, height, 40):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" />')
        svg_parts.append('</g>')

        # Header bar
        svg_parts.extend([
            f'<rect x="24" y="20" width="{width - 48}" height="70" rx="8" fill="{card_color}" stroke="{border_color}" stroke-width="1.2"/>',
            '<text x="44" y="50" fill="url(#fiberGrad)" font-size="18" font-weight="700" letter-spacing="0.5">TOPOLOGICAL FIBER BUNDLE &amp; HOLONOMY WEAVER</text>',
            '<text x="44" y="72" fill="#9ca3af" font-size="12">Differential Geometry &amp; Geometric Phase Holonomy across Closed Cognitive Loops</text>',
            f'<rect x="{width - 240}" y="36" width="196" height="36" rx="6" fill="#1e293b" stroke="{accent_cyan}" stroke-width="1.2"/>',
            f'<circle cx="{width - 222}" cy="54" r="5" fill="{accent_cyan}"/>',
            f'<text x="{width - 208}" y="59" fill="{text_primary}" font-size="12" font-weight="600">{telemetry.bundle_type}</text>',
        ])

        # Main viewport
        view_y = 105
        view_h = height - view_y - 85
        svg_parts.extend([
            f'<rect x="24" y="{view_y}" width="{width - 48}" height="{view_h}" rx="8" fill="#0d131a" stroke="{border_color}" stroke-width="1.2"/>',
            f'<text x="44" y="{view_y + 24}" fill="{text_muted}" font-size="11" font-weight="600" letter-spacing="1">PARALLEL TRANSPORT &amp; FIBER SURFACE</text>',
        ])

        # Draw base loop manifold
        if base_polyline:
            svg_parts.append(
                f'<polyline points="{base_polyline}" fill="none" stroke="#2a3b4c" stroke-width="3.5" opacity="0.6" stroke-dasharray="4,4" />'
            )

        # Draw fiber segments and ribbons connecting consecutive fibers
        n_fibers = len(telemetry.fibers)
        for i in range(n_fibers):
            curr = telemetry.fibers[i]
            nxt = telemetry.fibers[(i + 1) % n_fibers]

            # Current fiber endpoints
            p1_x = curr.base_x + curr.vector_dx
            p1_y = curr.base_y + curr.vector_dy
            p2_x = curr.base_x - curr.vector_dx
            p2_y = curr.base_y - curr.vector_dy

            # Next fiber endpoints
            q1_x = nxt.base_x + nxt.vector_dx
            q1_y = nxt.base_y + nxt.vector_dy
            q2_x = nxt.base_x - nxt.vector_dx
            q2_y = nxt.base_y - nxt.vector_dy

            # Render ribbon quad facet with gradient opacity
            quad_pts = f"{p1_x:.1f},{p1_y:.1f} {q1_x:.1f},{q1_y:.1f} {q2_x:.1f},{q2_y:.1f} {p2_x:.1f},{p2_y:.1f}"
            svg_parts.append(
                f'<polygon points="{quad_pts}" fill="{accent_purple}" fill-opacity="0.12" stroke="{accent_purple}" stroke-opacity="0.3" stroke-width="0.8" />'
            )

            # Fiber needle line
            svg_parts.append(
                f'<line x1="{p2_x:.1f}" y1="{p2_y:.1f}" x2="{p1_x:.1f}" y2="{p1_y:.1f}" stroke="{accent_cyan}" stroke-width="1.8" opacity="0.85" />'
            )
            # Base anchor node
            svg_parts.append(
                f'<circle cx="{curr.base_x:.1f}" cy="{curr.base_y:.1f}" r="2.5" fill="{accent_green}" />'
            )

        # Bottom metrics cards
        bottom_y = height - 72
        card_w = (width - 48 - 36) / 4

        metrics = [
            ("Holonomy Angle", f"{telemetry.holonomy_angle_deg:.1f} deg", accent_cyan),
            ("Total Fiber Twist", f"{telemetry.total_twist_deg:.1f} deg", accent_purple),
            ("Curvature Integral", f"{telemetry.connection_curvature_integral:.2f} rad", accent_amber),
            ("Bundle Topology", "Non-Trivial" if telemetry.is_non_trivial_topology else "Trivial", accent_green),
        ]

        for i, (m_label, m_val, m_col) in enumerate(metrics):
            cx = 24 + i * (card_w + 12)
            svg_parts.extend([
                f'<rect x="{cx:.1f}" y="{bottom_y}" width="{card_w:.1f}" height="56" rx="6" fill="{card_color}" stroke="{border_color}" stroke-width="1.2"/>',
                f'<text x="{cx + 12:.1f}" y="{bottom_y + 20}" fill="{text_muted}" font-size="10.5">{m_label}</text>',
                f'<text x="{cx + 12:.1f}" y="{bottom_y + 44}" fill="{m_col}" font-size="16" font-weight="700">{m_val}</text>',
            ])

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def export_telemetry_json(self, telemetry: HolonomyTelemetry) -> str:
        """Export serialized telemetry to JSON format."""
        return json.dumps(telemetry.to_dict(), indent=2)
