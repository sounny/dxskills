"""
Chrono-Spatial Replay Loom & Episodic Trajectory Synthesizer
Autonomous cognitive spatial module synthesizing forward mental rollouts and reverse credit assignment.
Grounded in hippocampal sharp-wave ripples (SWRs), theta phase precession,
and episodic memory trajectory compression for non-linear strategic planning.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json


@dataclass
class EpisodicWaypoint:
    """Represents a spatial or conceptual milestone in an episodic trajectory."""
    node_id: str
    label: str
    x: float
    y: float
    valence: float = 0.5            # -1.0 (aversive) to +1.0 (rewarding / focal goal)
    dwell_time_ms: float = 250.0    # Real-time inspection dwell duration
    theta_phase_deg: float = 0.0    # Spiking phase relative to local field theta cycle

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "label": self.label,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "valence": round(self.valence, 2),
            "dwell_time_ms": round(self.dwell_time_ms, 1),
            "theta_phase_deg": round(self.theta_phase_deg, 1),
        }


@dataclass
class ChronoReplayTelemetry:
    """Synthesized telemetry summarizing compressed episodic trajectory rollout."""
    replay_mode: str              # FORWARD_PLANNING, REVERSE_CREDIT, CHOICE_POINT_ROLLOUT
    total_waypoints: int
    total_path_length_px: float
    realtime_duration_ms: float
    compressed_duration_ms: float
    compression_factor: float
    ripple_frequency_hz: float
    mean_phase_precession_deg: float
    fidelity_score: float         # 0.0 to 100.0
    status: str
    waypoints: List[EpisodicWaypoint]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "replay_mode": self.replay_mode,
            "total_waypoints": self.total_waypoints,
            "total_path_length_px": round(self.total_path_length_px, 1),
            "realtime_duration_ms": round(self.realtime_duration_ms, 1),
            "compressed_duration_ms": round(self.compressed_duration_ms, 1),
            "compression_factor": round(self.compression_factor, 1),
            "ripple_frequency_hz": round(self.ripple_frequency_hz, 1),
            "mean_phase_precession_deg": round(self.mean_phase_precession_deg, 1),
            "fidelity_score": round(self.fidelity_score, 1),
            "status": self.status,
            "waypoints": [w.to_dict() for w in self.waypoints],
            "warnings": self.warnings,
        }


class ChronoSpatialReplayLoom:
    """
    Synthesizes compressed forward and reverse episodic trajectory sweeps,
    allowing spatial thinkers to evaluate multi-step conceptual decisions.
    """

    def __init__(self, default_compression: float = 14.0, ripple_freq_hz: float = 165.0):
        self.default_compression = default_compression
        self.ripple_freq_hz = ripple_freq_hz
        self.waypoints: List[EpisodicWaypoint] = []

    def add_waypoint(self, waypoint: EpisodicWaypoint) -> None:
        """Register a sequential episodic waypoint."""
        self.waypoints.append(waypoint)

    def clear_waypoints(self) -> None:
        """Clear registered trajectory waypoints."""
        self.waypoints.clear()

    def synthesize_forward_replay(
        self,
        waypoints: Optional[List[EpisodicWaypoint]] = None,
        compression_factor: Optional[float] = None,
    ) -> ChronoReplayTelemetry:
        """
        Synthesize a predictive forward trajectory rollout simulating hippocampal planning sweeps.
        Phase precession steadily advances from late to early theta phases (330 deg to 30 deg).
        """
        active_wps = waypoints if waypoints is not None else self.waypoints
        comp = compression_factor or self.default_compression

        if not active_wps:
            return ChronoReplayTelemetry(
                replay_mode="FORWARD_PLANNING",
                total_waypoints=0,
                total_path_length_px=0.0,
                realtime_duration_ms=0.0,
                compressed_duration_ms=0.0,
                compression_factor=comp,
                ripple_frequency_hz=self.ripple_freq_hz,
                mean_phase_precession_deg=0.0,
                fidelity_score=0.0,
                status="EMPTY_TRAJECTORY",
                waypoints=[],
                warnings=["No waypoints available for forward replay synthesis."],
            )

        n = len(active_wps)
        processed: List[EpisodicWaypoint] = []
        total_dist = 0.0
        total_real_ms = 0.0

        for i, wp in enumerate(active_wps):
            if i > 0:
                prev = active_wps[i - 1]
                dist = math.hypot(wp.x - prev.x, wp.y - prev.y)
                total_dist += dist
                # Real-time traversal estimated at 250 px/s + dwell time
                travel_time_ms = (dist / 250.0) * 1000.0
                total_real_ms += travel_time_ms

            total_real_ms += wp.dwell_time_ms

            # Phase precession: earlier phase as animal moves through trajectory
            # Progression from 320 deg down to 40 deg
            frac = i / max(1, n - 1)
            phase = 320.0 - frac * 280.0

            processed.append(
                EpisodicWaypoint(
                    node_id=wp.node_id,
                    label=wp.label,
                    x=wp.x,
                    y=wp.y,
                    valence=wp.valence,
                    dwell_time_ms=wp.dwell_time_ms,
                    theta_phase_deg=phase,
                )
            )

        compressed_ms = total_real_ms / comp if comp > 0 else total_real_ms
        mean_phase = sum(w.theta_phase_deg for w in processed) / n if n > 0 else 0.0
        fidelity = max(20.0, min(100.0, 95.0 - (comp / 50.0) * 10.0))

        warnings = []
        if comp > 25.0:
            warnings.append(
                f"Elevated compression factor ({comp:.1f}x) risks temporal aliasing across sharp-wave ripples."
            )

        return ChronoReplayTelemetry(
            replay_mode="FORWARD_PLANNING",
            total_waypoints=n,
            total_path_length_px=total_dist,
            realtime_duration_ms=total_real_ms,
            compressed_duration_ms=compressed_ms,
            compression_factor=comp,
            ripple_frequency_hz=self.ripple_freq_hz,
            mean_phase_precession_deg=mean_phase,
            fidelity_score=fidelity,
            status="REPLAY_SYNTHESIZED",
            waypoints=processed,
            warnings=warnings,
        )

    def synthesize_reverse_replay(
        self,
        waypoints: Optional[List[EpisodicWaypoint]] = None,
        compression_factor: Optional[float] = None,
    ) -> ChronoReplayTelemetry:
        """
        Synthesize a retrospective reverse replay sweep from goal state back to initial state.
        Reinforces high-reward nodes and credits causal antecedents.
        """
        active_wps = waypoints if waypoints is not None else self.waypoints
        comp = compression_factor or (self.default_compression * 1.15)

        if not active_wps:
            return ChronoReplayTelemetry(
                replay_mode="REVERSE_CREDIT",
                total_waypoints=0,
                total_path_length_px=0.0,
                realtime_duration_ms=0.0,
                compressed_duration_ms=0.0,
                compression_factor=comp,
                ripple_frequency_hz=self.ripple_freq_hz,
                mean_phase_precession_deg=0.0,
                fidelity_score=0.0,
                status="EMPTY_TRAJECTORY",
                waypoints=[],
                warnings=["No waypoints available for reverse replay synthesis."],
            )

        # Reverse the sequence for retrospective sweep
        reversed_wps = list(reversed(active_wps))
        n = len(reversed_wps)
        processed: List[EpisodicWaypoint] = []
        total_dist = 0.0
        total_real_ms = 0.0

        for i, wp in enumerate(reversed_wps):
            if i > 0:
                prev = reversed_wps[i - 1]
                dist = math.hypot(wp.x - prev.x, wp.y - prev.y)
                total_dist += dist
                travel_time_ms = (dist / 250.0) * 1000.0
                total_real_ms += travel_time_ms

            total_real_ms += wp.dwell_time_ms
            frac = i / max(1, n - 1)
            # Reverse phase sequence (40 deg up to 320 deg)
            phase = 40.0 + frac * 280.0

            processed.append(
                EpisodicWaypoint(
                    node_id=wp.node_id,
                    label=wp.label,
                    x=wp.x,
                    y=wp.y,
                    valence=wp.valence,
                    dwell_time_ms=wp.dwell_time_ms,
                    theta_phase_deg=phase,
                )
            )

        compressed_ms = total_real_ms / comp if comp > 0 else total_real_ms
        mean_phase = sum(w.theta_phase_deg for w in processed) / n if n > 0 else 0.0
        fidelity = max(20.0, min(100.0, 92.0 - (comp / 50.0) * 8.0))

        return ChronoReplayTelemetry(
            replay_mode="REVERSE_CREDIT",
            total_waypoints=n,
            total_path_length_px=total_dist,
            realtime_duration_ms=total_real_ms,
            compressed_duration_ms=compressed_ms,
            compression_factor=comp,
            ripple_frequency_hz=self.ripple_freq_hz,
            mean_phase_precession_deg=mean_phase,
            fidelity_score=fidelity,
            status="REPLAY_SYNTHESIZED",
            waypoints=processed,
            warnings=["Retrospective credit assignment sweep completed from target node to origin."],
        )

    def simulate_choice_point_rollout(
        self,
        center_x: float = 160.0,
        center_y: float = 260.0,
        branch_count: int = 3,
        depth: int = 4,
        step_len_px: float = 120.0,
    ) -> ChronoReplayTelemetry:
        """
        Generate a multi-step episodic trajectory through a choice-point decision lattice.
        """
        wps: List[EpisodicWaypoint] = [
            EpisodicWaypoint(
                node_id="ROOT",
                label="Decision Origin",
                x=center_x,
                y=center_y,
                valence=0.0,
                dwell_time_ms=300.0,
            )
        ]

        curr_x = center_x
        curr_y = center_y

        for step in range(1, depth + 1):
            angle = -0.3 + (step * 0.18)
            curr_x += step_len_px * math.cos(angle)
            curr_y += (step_len_px * 0.7) * math.sin(angle)
            valence = 0.2 + (step / float(depth)) * 0.75

            wps.append(
                EpisodicWaypoint(
                    node_id=f"STEP_{step}",
                    label=f"Action Node {step}",
                    x=curr_x,
                    y=curr_y,
                    valence=valence,
                    dwell_time_ms=220.0,
                )
            )

        return self.synthesize_forward_replay(wps, compression_factor=14.5)

    def render_chrono_replay_svg(
        self,
        telemetry: ChronoReplayTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """
        Render a publication-grade dark titanium SVG diagram showing the episodic trajectory rollout,
        hippocampal ripple burst waves, theta phase markers, and compression gauges.
        """
        bg_color = "#0b0f14"
        card_color = "#121820"
        border_color = "#1f2937"
        text_primary = "#f3f4f6"
        text_muted = "#9ca3af"
        accent_cyan = "#00e5ff"
        accent_purple = "#7c4dff"
        accent_green = "#00e676"
        accent_amber = "#ffab00"

        # Build trajectory polyline
        pts = [f"{w.x:.1f},{w.y:.1f}" for w in telemetry.waypoints]
        polyline_str = " ".join(pts)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: {bg_color}; '
            'font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <linearGradient id="replayGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.95"/>',
            '    <stop offset="100%" stop-color="#7c4dff" stop-opacity="0.95"/>',
            '  </linearGradient>',
            '  <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            '  </filter>',
            '  <filter id="glowGreen" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="2.5" result="blur" />',
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

        # Top Header Bar
        svg_parts.extend([
            f'<rect x="24" y="20" width="{width - 48}" height="70" rx="8" fill="{card_color}" stroke="{border_color}" stroke-width="1.2"/>',
            '<text x="44" y="50" fill="url(#replayGrad)" font-size="18" font-weight="700" letter-spacing="0.5">CHRONO-SPATIAL REPLAY LOOM</text>',
            '<text x="44" y="72" fill="#9ca3af" font-size="12">Hippocampal Sharp-Wave Ripple Compression &amp; Theta Phase Precession</text>',
            f'<rect x="{width - 240}" y="36" width="196" height="36" rx="6" fill="#1e293b" stroke="{accent_cyan}" stroke-width="1.2"/>',
            f'<circle cx="{width - 222}" cy="54" r="5" fill="{accent_cyan}"/>',
            f'<text x="{width - 208}" y="59" fill="{text_primary}" font-size="12" font-weight="600">{telemetry.replay_mode}</text>',
        ])

        # Main Trajectory Viewport
        view_y = 105
        view_h = height - view_y - 85
        svg_parts.extend([
            f'<rect x="24" y="{view_y}" width="{width - 48}" height="{view_h}" rx="8" fill="#0d131a" stroke="{border_color}" stroke-width="1.2"/>',
            f'<text x="44" y="{view_y + 24}" fill="{text_muted}" font-size="11" font-weight="600" letter-spacing="1">EPISODIC TRAJECTORY ROLLOUT</text>',
        ])

        # Draw trajectory connector line
        if polyline_str:
            line_col = accent_cyan if telemetry.replay_mode == "FORWARD_PLANNING" else accent_purple
            svg_parts.append(
                f'<polyline points="{polyline_str}" fill="none" stroke="{line_col}" stroke-width="2.8" filter="url(#glowCyan)" opacity="0.9" />'
            )

        # Draw waypoints with valence and theta phase indicators
        for i, wp in enumerate(telemetry.waypoints):
            # Valence mapped color: positive = green, neutral = cyan, negative = amber/coral
            val_col = accent_green if wp.valence > 0.4 else (accent_amber if wp.valence < 0.0 else accent_cyan)
            svg_parts.extend([
                # Outer ripple ring
                f'<circle cx="{wp.x:.1f}" cy="{wp.y:.1f}" r="14" fill="none" stroke="{val_col}" stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>',
                # Core node
                f'<circle cx="{wp.x:.1f}" cy="{wp.y:.1f}" r="7" fill="{val_col}" filter="url(#glowGreen)"/>',
                f'<circle cx="{wp.x:.1f}" cy="{wp.y:.1f}" r="2.5" fill="#ffffff"/>',
                # Labels
                f'<text x="{wp.x + 16:.1f}" y="{wp.y + 4:.1f}" fill="{text_primary}" font-size="11" font-weight="600">{html.escape(wp.label)}</text>',
                f'<text x="{wp.x + 16:.1f}" y="{wp.y + 17:.1f}" fill="{accent_purple}" font-size="9.5">Phase: {wp.theta_phase_deg:.0f} deg | V={wp.valence:.2f}</text>',
            ])

        # Bottom Metrics Cards
        bottom_y = height - 72
        card_w = (width - 48 - 36) / 4

        metrics = [
            ("Compression Ratio", f"{telemetry.compression_factor:.1f}x", accent_cyan),
            ("Rollout Time", f"{telemetry.compressed_duration_ms:.0f} ms", accent_purple),
            ("Ripple Frequency", f"{telemetry.ripple_frequency_hz:.0f} Hz", accent_amber),
            ("Fidelity Score", f"{telemetry.fidelity_score:.1f} / 100", accent_green),
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

    def export_telemetry_json(self, telemetry: ChronoReplayTelemetry) -> str:
        """Export serialized telemetry to JSON format."""
        return json.dumps(telemetry.to_dict(), indent=2)
