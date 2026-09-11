"""
Saccadic Drift Dampener & Retinal Latch Engine
Autonomous cognitive spatial module stabilizing gaze fixations and visuospatial working memory
during rapid mental rotations and allocentric navigation transformations.
Grounded in Shepard-Metzler mental rotation dynamics, Rucci fixational drift models,
and Baddeley visuospatial sketchpad retention mechanics.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json


@dataclass
class RetinalAnchor:
    """Stable spatial reference landmark that captures and latches gaze during mental transformations."""
    anchor_id: str
    label: str
    x: float
    y: float
    capture_radius_px: float = 35.0
    latch_strength: float = 0.85
    retention_decay_rate: float = 0.15
    active_latch: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "label": self.label,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "capture_radius_px": round(self.capture_radius_px, 1),
            "latch_strength": round(self.latch_strength, 2),
            "retention_decay_rate": round(self.retention_decay_rate, 2),
            "active_latch": self.active_latch,
        }


@dataclass
class DriftDampeningConfig:
    """Operational parameters for the low-pass drift filter and retinal latch mechanism."""
    deadband_radius_px: float = 10.0
    damping_factor: float = 0.68
    hysteresis_threshold_px: float = 24.0
    working_memory_span_ms: float = 2400.0
    rotation_drift_compensation: bool = True
    max_fixational_jitter_px: float = 18.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "deadband_radius_px": self.deadband_radius_px,
            "damping_factor": self.damping_factor,
            "hysteresis_threshold_px": self.hysteresis_threshold_px,
            "working_memory_span_ms": self.working_memory_span_ms,
            "rotation_drift_compensation": self.rotation_drift_compensation,
            "max_fixational_jitter_px": self.max_fixational_jitter_px,
        }


@dataclass
class DriftCorrectionStep:
    """Detailed temporal sample recording raw vs damped ocular coordinates."""
    timestamp_ms: float
    raw_x: float
    raw_y: float
    filtered_x: float
    filtered_y: float
    drift_magnitude_px: float
    is_latched: bool
    latched_anchor_id: Optional[str]
    rotation_angle_deg: float
    wm_stability_index: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp_ms": round(self.timestamp_ms, 1),
            "raw_x": round(self.raw_x, 1),
            "raw_y": round(self.raw_y, 1),
            "filtered_x": round(self.filtered_x, 1),
            "filtered_y": round(self.filtered_y, 1),
            "drift_magnitude_px": round(self.drift_magnitude_px, 2),
            "is_latched": self.is_latched,
            "latched_anchor_id": self.latched_anchor_id,
            "rotation_angle_deg": round(self.rotation_angle_deg, 1),
            "wm_stability_index": round(self.wm_stability_index, 3),
        }


@dataclass
class RetinalLatchTelemetry:
    """Comprehensive summary of ocular drift dampening and working memory stabilization."""
    total_samples: int
    total_raw_path_length_px: float
    total_damped_path_length_px: float
    drift_reduction_pct: float
    mean_jitter_amplitude_px: float
    latch_event_count: int
    working_memory_coherence_score: float
    stability_status: str
    anchors: List[RetinalAnchor]
    corrections: List[DriftCorrectionStep]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_samples": self.total_samples,
            "total_raw_path_length_px": round(self.total_raw_path_length_px, 1),
            "total_damped_path_length_px": round(self.total_damped_path_length_px, 1),
            "drift_reduction_pct": round(self.drift_reduction_pct, 1),
            "mean_jitter_amplitude_px": round(self.mean_jitter_amplitude_px, 2),
            "latch_event_count": self.latch_event_count,
            "working_memory_coherence_score": round(self.working_memory_coherence_score, 1),
            "stability_status": self.stability_status,
            "anchors": [a.to_dict() for a in self.anchors],
            "corrections_count": len(self.corrections),
            "warnings": self.warnings,
        }


class SaccadicDriftDampener:
    """
    Stabilizes gaze trajectories and preserves visuospatial anchors
    against micro-saccadic fixational tremor and mental rotation drift.
    """

    def __init__(self, config: Optional[DriftDampeningConfig] = None):
        self.config = config or DriftDampeningConfig()
        self.anchors: List[RetinalAnchor] = []

    def add_anchor(self, anchor: RetinalAnchor) -> None:
        """Register a stable spatial landmark for retinal latching."""
        self.anchors.append(anchor)

    def clear_anchors(self) -> None:
        """Remove all registered anchors."""
        self.anchors.clear()

    def find_nearest_anchor(self, x: float, y: float) -> Optional[Tuple[RetinalAnchor, float]]:
        """Identify closest spatial anchor and its Euclidean distance in pixels."""
        if not self.anchors:
            return None
        closest = None
        min_dist = float("inf")
        for anchor in self.anchors:
            dist = math.hypot(x - anchor.x, y - anchor.y)
            if dist < min_dist:
                min_dist = dist
                closest = anchor
        return (closest, min_dist) if closest else None

    def process_stream(
        self,
        raw_samples: List[Tuple[float, float, float]],
        rotation_rate_dps: float = 0.0,
        initial_rotation_deg: float = 0.0
    ) -> RetinalLatchTelemetry:
        """
        Process a sequential stream of ocular samples (timestamp_ms, x, y).
        Applies low-pass damping, deadband suppression, and retinal latching.
        """
        if not raw_samples:
            return RetinalLatchTelemetry(
                total_samples=0,
                total_raw_path_length_px=0.0,
                total_damped_path_length_px=0.0,
                drift_reduction_pct=0.0,
                mean_jitter_amplitude_px=0.0,
                latch_event_count=0,
                working_memory_coherence_score=0.0,
                stability_status="EMPTY_STREAM",
                anchors=[a for a in self.anchors],
                corrections=[],
                warnings=["No raw gaze samples supplied for drift processing."],
            )

        corrections: List[DriftCorrectionStep] = []
        total_raw_dist = 0.0
        total_damped_dist = 0.0
        jitter_accum = 0.0
        latch_count = 0
        currently_latched_id: Optional[str] = None

        prev_raw_x = raw_samples[0][1]
        prev_raw_y = raw_samples[0][2]
        prev_filtered_x = prev_raw_x
        prev_filtered_y = prev_raw_y

        first_t = raw_samples[0][0]

        for idx, (t_ms, rx, ry) in enumerate(raw_samples):
            # Calculate raw movement distance
            step_raw_dist = math.hypot(rx - prev_raw_x, ry - prev_raw_y)
            total_raw_dist += step_raw_dist

            elapsed_sec = (t_ms - first_t) / 1000.0
            cur_rot_deg = (initial_rotation_deg + rotation_rate_dps * elapsed_sec) % 360.0

            # Find nearest spatial anchor
            nearest = self.find_nearest_anchor(rx, ry)
            is_latched = False
            latched_id = None

            filtered_x = rx
            filtered_y = ry

            if nearest:
                anchor, dist = nearest
                # Check hysteresis if previously latched
                if currently_latched_id == anchor.anchor_id:
                    if dist <= self.config.hysteresis_threshold_px:
                        is_latched = True
                        latched_id = anchor.anchor_id
                    else:
                        currently_latched_id = None
                elif dist <= anchor.capture_radius_px:
                    is_latched = True
                    latched_id = anchor.anchor_id
                    currently_latched_id = anchor.anchor_id
                    latch_count += 1

                if is_latched:
                    # Pull coordinates towards anchor based on latch strength
                    pull = anchor.latch_strength
                    filtered_x = (1.0 - pull) * rx + pull * anchor.x
                    filtered_y = (1.0 - pull) * ry + pull * anchor.y

            if not is_latched:
                # Apply low-pass exponential damping filter
                deadband = self.config.deadband_radius_px
                dist_from_prev = math.hypot(rx - prev_filtered_x, ry - prev_filtered_y)

                if dist_from_prev < deadband:
                    # Suppress micro-tremor within deadband
                    filtered_x = prev_filtered_x
                    filtered_y = prev_filtered_y
                else:
                    alpha = 1.0 - self.config.damping_factor
                    filtered_x = prev_filtered_x + alpha * (rx - prev_filtered_x)
                    filtered_y = prev_filtered_y + alpha * (ry - prev_filtered_y)

            # Rotation drift compensation if active
            if self.config.rotation_drift_compensation and rotation_rate_dps > 0.0:
                rad = math.radians(cur_rot_deg)
                comp_x = -0.05 * math.sin(rad) * (dist_from_prev if not is_latched else 0.0)
                comp_y = 0.05 * math.cos(rad) * (dist_from_prev if not is_latched else 0.0)
                filtered_x += comp_x
                filtered_y += comp_y

            # Measure damped step distance
            step_damped_dist = math.hypot(filtered_x - prev_filtered_x, filtered_y - prev_filtered_y)
            total_damped_dist += step_damped_dist

            drift_mag = math.hypot(rx - filtered_x, ry - filtered_y)
            jitter_accum += drift_mag

            # Compute working memory stability index
            # High latching and low drift preserve visuospatial sketchpad representation
            stability_decay = max(0.1, 1.0 - (elapsed_sec / (self.config.working_memory_span_ms / 1000.0)))
            wm_stability = 1.0 if is_latched else max(0.2, (1.0 - min(1.0, drift_mag / 30.0)) * stability_decay)

            corrections.append(
                DriftCorrectionStep(
                    timestamp_ms=t_ms,
                    raw_x=rx,
                    raw_y=ry,
                    filtered_x=filtered_x,
                    filtered_y=filtered_y,
                    drift_magnitude_px=drift_mag,
                    is_latched=is_latched,
                    latched_anchor_id=latched_id,
                    rotation_angle_deg=cur_rot_deg,
                    wm_stability_index=wm_stability,
                )
            )

            prev_raw_x = rx
            prev_raw_y = ry
            prev_filtered_x = filtered_x
            prev_filtered_y = filtered_y

        n_samples = len(raw_samples)
        mean_jitter = jitter_accum / n_samples if n_samples > 0 else 0.0
        reduction_pct = (
            ((total_raw_dist - total_damped_dist) / total_raw_dist * 100.0)
            if total_raw_dist > 0.0
            else 0.0
        )
        reduction_pct = max(0.0, min(100.0, reduction_pct))

        # Coherence score based on jitter reduction and stability
        mean_stability = sum(c.wm_stability_index for c in corrections) / n_samples if n_samples > 0 else 0.0
        coherence_score = max(0.0, min(100.0, (mean_stability * 60.0) + (reduction_pct * 0.4)))

        warnings = []
        if mean_jitter > self.config.max_fixational_jitter_px:
            warnings.append(
                f"Elevated ocular tremor detected: mean drift {mean_jitter:.1f}px exceeds nominal tolerance."
            )
        if rotation_rate_dps > 90.0:
            warnings.append(
                f"High mental rotation velocity ({rotation_rate_dps:.1f} deg/s) induces severe vestibular-cognitive slip."
            )

        if coherence_score >= 75.0:
            status = "LATCHED_STABLE"
        elif coherence_score >= 45.0:
            status = "DRIFT_DAMPED"
        else:
            status = "JITTER_COMPROMISED"

        return RetinalLatchTelemetry(
            total_samples=n_samples,
            total_raw_path_length_px=total_raw_dist,
            total_damped_path_length_px=total_damped_dist,
            drift_reduction_pct=reduction_pct,
            mean_jitter_amplitude_px=mean_jitter,
            latch_event_count=latch_count,
            working_memory_coherence_score=coherence_score,
            stability_status=status,
            anchors=[a for a in self.anchors],
            corrections=corrections,
            warnings=warnings,
        )

    def simulate_mental_rotation_drift(
        self,
        base_anchors: Optional[List[Tuple[str, float, float]]] = None,
        rotation_angle_deg: float = 180.0,
        noise_std: float = 9.5,
        duration_ms: float = 2400.0,
        step_ms: float = 50.0,
        center_x: float = 450.0,
        center_y: float = 260.0,
        radius_px: float = 140.0
    ) -> RetinalLatchTelemetry:
        """
        Synthesize simulated ocular drift during mental rotation of a 2D/3D polygon.
        Generates noisy gaze path orbiting anchors and demonstrates latching stabilization.
        """
        self.clear_anchors()
        if base_anchors:
            for aid, ax, ay in base_anchors:
                self.add_anchor(RetinalAnchor(anchor_id=aid, label=aid, x=ax, y=ay))
        else:
            # Default equilateral triangle of spatial anchors
            for i in range(3):
                theta = math.radians(i * 120.0 - 90.0)
                ax = center_x + radius_px * math.cos(theta)
                ay = center_y + radius_px * math.sin(theta)
                self.add_anchor(
                    RetinalAnchor(
                        anchor_id=f"ANC_{i+1}",
                        label=f"Vertex {i+1}",
                        x=ax,
                        y=ay,
                        capture_radius_px=40.0,
                        latch_strength=0.88,
                    )
                )

        total_steps = int(duration_ms / step_ms)
        rotation_rate_dps = (rotation_angle_deg / (duration_ms / 1000.0)) if duration_ms > 0 else 0.0

        raw_samples: List[Tuple[float, float, float]] = []
        for step in range(total_steps):
            t = step * step_ms
            # Target path orbits around center while jumping between anchors
            progress = step / max(1, total_steps - 1)
            active_anchor_idx = int(progress * len(self.anchors)) % len(self.anchors)
            target_anchor = self.anchors[active_anchor_idx]

            # Involuntary tremor / drift noise
            noise_x = math.sin(step * 0.45) * noise_std + (math.cos(step * 1.3) * (noise_std * 0.5))
            noise_y = math.cos(step * 0.40) * noise_std + (math.sin(step * 1.1) * (noise_std * 0.5))

            # Additional drift caused by rotational motion
            rot_rad = math.radians(rotation_rate_dps * (t / 1000.0))
            drift_x = math.cos(rot_rad) * (noise_std * 0.75)
            drift_y = math.sin(rot_rad) * (noise_std * 0.75)

            gx = target_anchor.x + noise_x + drift_x
            gy = target_anchor.y + noise_y + drift_y
            raw_samples.append((t, gx, gy))

        return self.process_stream(
            raw_samples=raw_samples,
            rotation_rate_dps=rotation_rate_dps,
            initial_rotation_deg=0.0
        )

    def render_retinal_latch_svg(
        self,
        telemetry: RetinalLatchTelemetry,
        width: int = 920,
        height: int = 560
    ) -> str:
        """
        Render an interactive, publication-grade dark titanium SVG diagram
        visualizing raw vs damped gaze paths, retinal latch anchor rings, and working memory metrics.
        """
        bg_color = "#0b0f14"
        card_color = "#121820"
        border_color = "#1f2937"
        raw_path_color = "#ff5252"      # Coral/red for jittery raw gaze
        damped_path_color = "#00e5ff"   # Glowing neon cyan for damped stabilized gaze
        anchor_color = "#00e676"        # Emerald green for anchors
        text_primary = "#f3f4f6"
        text_muted = "#9ca3af"
        accent_purple = "#7c4dff"

        status_badge_color = {
            "LATCHED_STABLE": "#00e676",
            "DRIFT_DAMPED": "#ffab00",
            "JITTER_COMPROMISED": "#ff5252",
            "EMPTY_STREAM": "#6b7280",
        }.get(telemetry.stability_status, "#00e5ff")

        # Build raw and damped path strings
        raw_pts = []
        damped_pts = []
        for c in telemetry.corrections:
            raw_pts.append(f"{c.raw_x:.1f},{c.raw_y:.1f}")
            damped_pts.append(f"{c.filtered_x:.1f},{c.filtered_y:.1f}")

        raw_polyline = " ".join(raw_pts)
        damped_polyline = " ".join(damped_pts)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: {bg_color}; '
            'font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.9"/>',
            '    <stop offset="100%" stop-color="#7c4dff" stop-opacity="0.9"/>',
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
            '<!-- Background Grid -->',
            '<g opacity="0.08" stroke="#ffffff" stroke-width="1">',
        ]

        # Subtle Cartesian background grid
        for gx in range(0, width, 40):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" />')
        for gy in range(0, height, 40):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" />')
        svg_parts.append('</g>')

        # Top Header & Status Card
        svg_parts.extend([
            f'<rect x="24" y="20" width="{width - 48}" height="70" rx="8" fill="{card_color}" stroke="{border_color}" stroke-width="1.2"/>',
            '<text x="44" y="50" fill="url(#headerGrad)" font-size="18" font-weight="700" letter-spacing="0.5">SACCADIC DRIFT DAMPENER &amp; RETINAL LATCH</text>',
            '<text x="44" y="72" fill="#9ca3af" font-size="12">Visuospatial Sketchpad Retention &amp; Mental Rotation Stabilizer</text>',
            f'<rect x="{width - 240}" y="36" width="196" height="36" rx="6" fill="#1e293b" stroke="{status_badge_color}" stroke-width="1.2"/>',
            f'<circle cx="{width - 222}" cy="54" r="5" fill="{status_badge_color}"/>',
            f'<text x="{width - 208}" y="59" fill="{text_primary}" font-size="12" font-weight="600">{telemetry.stability_status}</text>',
        ])

        # Main Visualization Canvas Box
        canvas_y = 105
        canvas_h = height - canvas_y - 85
        svg_parts.extend([
            f'<rect x="24" y="{canvas_y}" width="{width - 48}" height="{canvas_h}" rx="8" fill="#0d131a" stroke="{border_color}" stroke-width="1.2"/>',
            f'<text x="44" y="{canvas_y + 24}" fill="{text_muted}" font-size="11" font-weight="600" letter-spacing="1">OCULAR DRIFT &amp; RETINAL ANCHOR MESH</text>',
        ])

        # Draw Raw Gaze Path (Red/Coral, semi-transparent dashed or thin)
        if raw_polyline:
            svg_parts.append(
                f'<polyline points="{raw_polyline}" fill="none" stroke="{raw_path_color}" stroke-width="1.4" opacity="0.45" stroke-dasharray="3,3" />'
            )

        # Draw Damped Gaze Path (Glowing Neon Cyan)
        if damped_polyline:
            svg_parts.append(
                f'<polyline points="{damped_polyline}" fill="none" stroke="{damped_path_color}" stroke-width="2.6" filter="url(#glowCyan)" opacity="0.95" />'
            )

        # Draw Retinal Anchors
        for anc in telemetry.anchors:
            rad = anc.capture_radius_px
            svg_parts.extend([
                f'<circle cx="{anc.x:.1f}" cy="{anc.y:.1f}" r="{rad:.1f}" fill="{anchor_color}" fill-opacity="0.06" stroke="{anchor_color}" stroke-width="1.2" stroke-dasharray="4,4" />',
                f'<circle cx="{anc.x:.1f}" cy="{anc.y:.1f}" r="7" fill="{anchor_color}" filter="url(#glowGreen)"/>',
                f'<circle cx="{anc.x:.1f}" cy="{anc.y:.1f}" r="2.5" fill="#ffffff" />',
                f'<text x="{anc.x + 12:.1f}" y="{anc.y + 4:.1f}" fill="{text_primary}" font-size="11" font-weight="600">{html.escape(anc.label)}</text>',
                f'<text x="{anc.x + 12:.1f}" y="{anc.y + 17:.1f}" fill="{accent_purple}" font-size="9.5">R={rad:.0f}px | L={anc.latch_strength:.2f}</text>',
            ])

        # Bottom Metrics Cards (4 Columns)
        bottom_y = height - 72
        card_w = (width - 48 - 36) / 4

        metrics = [
            ("Drift Suppression", f"{telemetry.drift_reduction_pct:.1f}%", damped_path_color),
            ("Mean Jitter Amplitude", f"{telemetry.mean_jitter_amplitude_px:.1f} px", "#ffab00"),
            ("Retinal Latch Events", f"{telemetry.latch_event_count}", anchor_color),
            ("WM Coherence Index", f"{telemetry.working_memory_coherence_score:.1f} / 100", accent_purple),
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

    def export_telemetry_json(self, telemetry: RetinalLatchTelemetry) -> str:
        """Export serialized telemetry data to JSON format."""
        return json.dumps(telemetry.to_dict(), indent=2)
