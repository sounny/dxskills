"""
Anchor Eviction & Graceful Horizon Pacer Engine
Autonomous cognitive spatial module for working memory anchor decay modeling,
Ebbinghaus retention half-life tracking, graceful sunset fading, and subliminal
peripheral breadcrumb maintenance. Grounded in Cowan working memory capacity bounds,
Ebbinghaus forgetting curves, and Burgess allocentric memory persistence.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import html


@dataclass
class DecayingAnchor:
    """Represents a working memory anchor subject to cognitive decay."""
    anchor_id: str
    title: str
    created_at_s: float
    last_accessed_s: float
    base_saliency: float = 1.0  # 0.5 to 5.0
    half_life_s: float = 300.0  # Half-life in seconds (default 5 minutes)
    pos_x: float = 0.0
    pos_y: float = 0.0


@dataclass
class EvictionState:
    """Calculated lifecycle state and visual attributes of an anchor."""
    anchor_id: str
    title: str
    retention_score: float  # 0.0 to 1.0
    lifecycle_state: str  # fresh, maturing, sunset, breadcrumb, evicted
    opacity: float
    visual_radius_px: float
    pos_x: float
    pos_y: float


@dataclass
class AnchorEvictionTelemetry:
    """Comprehensive telemetry report for working memory anchor eviction."""
    current_time_s: float
    total_anchors: int
    fresh_count: int
    maturing_count: int
    sunset_count: int
    breadcrumb_count: int
    evicted_count: int
    working_memory_pressure: float
    overload_warning: bool
    anchor_states: List[EvictionState] = field(default_factory=list)


class AnchorEvictionHorizonPacer:
    """
    Autonomous engine that paces anchor eviction from working memory.
    Prevents abrupt disappears and visual disorientation by gracefully
    transitioning stale anchors into sunset fading and peripheral breadcrumbs.
    """

    def __init__(self, pressure_threshold: float = 4.5):
        self.pressure_threshold = float(pressure_threshold)

    @staticmethod
    def calculate_retention(anchor: DecayingAnchor, current_time_s: float) -> float:
        """Calculates Ebbinghaus retention score based on time elapsed and half-life."""
        elapsed = max(0.0, current_time_s - anchor.last_accessed_s)
        half_life = max(10.0, anchor.half_life_s * (0.8 + 0.2 * anchor.base_saliency))
        decay_constant = math.log(2.0) / half_life
        retention = math.exp(-decay_constant * elapsed)
        return max(0.0, min(1.0, retention))

    def evaluate_session(
        self,
        anchors: List[DecayingAnchor],
        current_time_s: float,
    ) -> AnchorEvictionTelemetry:
        """
        Evaluates current retention profiles for all anchors and determines
        lifecycle transitions, working memory pressure, and overload states.
        """
        if not anchors:
            return AnchorEvictionTelemetry(
                current_time_s=current_time_s,
                total_anchors=0,
                fresh_count=0,
                maturing_count=0,
                sunset_count=0,
                breadcrumb_count=0,
                evicted_count=0,
                working_memory_pressure=0.0,
                overload_warning=False,
                anchor_states=[],
            )

        states: List[EvictionState] = []
        fresh = 0
        maturing = 0
        sunset = 0
        breadcrumb = 0
        evicted = 0
        total_pressure = 0.0

        for a in anchors:
            ret = self.calculate_retention(a, current_time_s)

            # Classify lifecycle state
            if ret >= 0.85:
                state_label = "fresh"
                opacity = 1.0
                radius = 16.0
                fresh += 1
                total_pressure += 1.0 * a.base_saliency
            elif ret >= 0.50:
                state_label = "maturing"
                opacity = 0.85
                radius = 14.0
                maturing += 1
                total_pressure += 0.75 * a.base_saliency
            elif ret >= 0.20:
                state_label = "sunset"
                opacity = 0.55
                radius = 10.0
                sunset += 1
                total_pressure += 0.35 * a.base_saliency
            elif ret >= 0.05:
                state_label = "breadcrumb"
                opacity = 0.25
                radius = 5.0
                breadcrumb += 1
                total_pressure += 0.10 * a.base_saliency
            else:
                state_label = "evicted"
                opacity = 0.0
                radius = 0.0
                evicted += 1

            states.append(
                EvictionState(
                    anchor_id=a.anchor_id,
                    title=a.title,
                    retention_score=round(ret, 3),
                    lifecycle_state=state_label,
                    opacity=opacity,
                    visual_radius_px=radius,
                    pos_x=a.pos_x,
                    pos_y=a.pos_y,
                )
            )

        overload = total_pressure > self.pressure_threshold

        return AnchorEvictionTelemetry(
            current_time_s=round(current_time_s, 1),
            total_anchors=len(anchors),
            fresh_count=fresh,
            maturing_count=maturing,
            sunset_count=sunset,
            breadcrumb_count=breadcrumb,
            evicted_count=evicted,
            working_memory_pressure=round(total_pressure, 2),
            overload_warning=overload,
            anchor_states=states,
        )

    def generate_markdown_report(self, telemetry: AnchorEvictionTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lines = [
            "# Working Memory Anchor Eviction and Horizon Pacer Telemetry",
            "",
            "## 1. Executive Memory Pressure Overview",
            f"- **Session Timestamp:** {telemetry.current_time_s}s",
            f"- **Total Monitored Anchors:** {telemetry.total_anchors}",
            f"- **Active Working Memory Pressure:** {telemetry.working_memory_pressure} units (Threshold: {self.pressure_threshold})",
            f"- **Cowan Capacity Bound Status:** {'OPTIMAL' if not telemetry.overload_warning else 'OVERLOAD WARNING'}",
            f"- **Anchor Breakdown:** {telemetry.fresh_count} Fresh, {telemetry.maturing_count} Maturing, {telemetry.sunset_count} Sunset, {telemetry.breadcrumb_count} Breadcrumb, {telemetry.evicted_count} Evicted",
            "",
            "## 2. Theoretical Grounding",
            "- **Ebbinghaus Forgetting Model:** Anchors decay exponentially without active rehearsal.",
            "- **Graceful Horizon Sunset:** Fading stale anchors gradually preserves allocentric landmark orientation.",
            "- **Subliminal Breadcrumbs:** 5px micro-dots maintain spatial context without consuming focal foveal bandwidth.",
            "",
            "## 3. Anchor Lifecycle Catalog",
            "| ID | Title | Retention Score | State | Opacity | Radius (px) | Position (x, y) |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for s in telemetry.anchor_states:
            lines.append(
                f"| `{s.anchor_id}` | {s.title} | {s.retention_score} | `{s.lifecycle_state}` | {s.opacity} | {s.visual_radius_px} | ({s.pos_x}, {s.pos_y}) |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Guidance",
            "- Anchors transitioning to 'sunset' are prime candidates for consolidation into macro schemas.",
            "- When Working Memory Pressure exceeds 4.5, trigger micro-rest or batch-flush non-critical pins.",
            "- Peripheral breadcrumbs can be re-activated with a single ocular fixation touchpoint.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: AnchorEvictionTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium sunset horizon SVG."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d18; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <linearGradient id="sunsetSky" x1="0%" y1="0%" x2="0%" y2="100%">',
            '    <stop offset="0%" stop-color="#0f172a"/>',
            '    <stop offset="60%" stop-color="#1e293b"/>',
            '    <stop offset="90%" stop-color="#312e81" stop-opacity="0.6"/>',
            '    <stop offset="100%" stop-color="#431407" stop-opacity="0.4"/>',
            '  </linearGradient>',
            '  <filter id="anchorShadow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.8"/>',
            '  </filter>',
            '</defs>',
            '<!-- Sky Atmosphere -->',
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="url(#sunsetSky)"/>',
            '<!-- Horizon Reference Line -->',
            f'<line x1="40" y1="{height - 80}" x2="{width - 40}" y2="{height - 80}" stroke="#475569" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.6"/>',
            f'<text x="{width - 50}" y="{height - 86}" font-size="9" fill="#94a3b8" text-anchor="end">MEMORY HORIZON</text>',
        ]

        # Draw Anchors by State
        for s in telemetry.anchor_states:
            if s.lifecycle_state == "evicted":
                continue

            if s.lifecycle_state == "fresh":
                fill_c = "#38bdf8"
                stroke_c = "#ffffff"
            elif s.lifecycle_state == "maturing":
                fill_c = "#0284c7"
                stroke_c = "#38bdf8"
            elif s.lifecycle_state == "sunset":
                fill_c = "#f97316"
                stroke_c = "#fdba74"
            else:  # breadcrumb
                fill_c = "#94a3b8"
                stroke_c = "#cbd5e1"

            svg_parts.append(
                f'<circle cx="{s.pos_x}" cy="{s.pos_y}" r="{s.visual_radius_px}" fill="{fill_c}" fill-opacity="{s.opacity}" stroke="{stroke_c}" stroke-width="1.5" stroke-opacity="{s.opacity}" filter="url(#anchorShadow)"/>'
            )

            if s.lifecycle_state != "breadcrumb":
                svg_parts.append(
                    f'<text x="{s.pos_x}" y="{s.pos_y + s.visual_radius_px + 13}" font-size="9" font-weight="600" fill="#ffffff" fill-opacity="{s.opacity}" text-anchor="middle">{html.escape(s.title)}</text>'
                )
                svg_parts.append(
                    f'<text x="{s.pos_x}" y="{s.pos_y + s.visual_radius_px + 23}" font-size="7" fill="#94a3b8" fill-opacity="{s.opacity}" text-anchor="middle">R={s.retention_score}</text>'
                )

        # HUD Overlay Box
        hud_border = "#ef4444" if telemetry.overload_warning else "#1e293b"
        svg_parts.append(
            f'<rect x="20" y="16" width="350" height="74" rx="8" fill="#0f172a" fill-opacity="0.88" stroke="{hud_border}" stroke-width="1.2"/>'
        )
        svg_parts.append(
            f'<text x="32" y="36" font-size="11" font-weight="700" fill="#38bdf8">ANCHOR HORIZON PACER HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="52" font-size="9" fill="#94a3b8">Active Pressure: {telemetry.working_memory_pressure}/{self.pressure_threshold} | Fresh: {telemetry.fresh_count} | Maturing: {telemetry.maturing_count}</text>'
        )
        svg_parts.append(
            f'<text x="32" y="68" font-size="9" fill="#94a3b8">Sunset: {telemetry.sunset_count} | Breadcrumbs: {telemetry.breadcrumb_count} | Evicted: {telemetry.evicted_count}</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_decaying_anchors(base_time_s: float = 1000.0) -> List[DecayingAnchor]:
    """Generates demonstration decaying working memory anchor session."""
    return [
        DecayingAnchor("anc-1", "Authentication Token", 800.0, 980.0, 1.2, 300.0, 220.0, 180.0),   # 20s ago -> Fresh
        DecayingAnchor("anc-2", "Query Cache Hook", 700.0, 920.0, 1.0, 300.0, 380.0, 190.0),        # 80s ago -> Fresh
        DecayingAnchor("anc-3", "Database Connection", 500.0, 750.0, 1.5, 300.0, 540.0, 220.0),      # 250s ago -> Maturing
        DecayingAnchor("anc-4", "User Preference Reducer", 300.0, 500.0, 0.8, 300.0, 700.0, 260.0), # 500s ago -> Sunset
        DecayingAnchor("anc-5", "Legacy CSS Variable", 100.0, 200.0, 0.6, 250.0, 300.0, 360.0),      # 800s ago -> Breadcrumb
        DecayingAnchor("anc-6", "Deprecating Modal Event", 50.0, 80.0, 0.5, 200.0, 600.0, 400.0),    # 920s ago -> Evicted
    ]
