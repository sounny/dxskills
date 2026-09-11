"""
Saccadic Trajectory Predictor and Predictive Pre-Fetcher Engine
Autonomous cognitive spatial module modeling Carpenter LATER saccade dynamics,
Rayner parafoveal preview envelopes, and forward trajectory vector extrapolation.
Predicts subsequent ocular fixation targets and pre-fetches high-priority canvas
nodes to eliminate visual lag during non-linear analytical exploration.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html


@dataclass
class FixationPoint:
    """Represents a recorded ocular fixation point with spatial and temporal coordinates."""
    node_id: str
    title: str
    x: float
    y: float
    timestamp_ms: float
    dwell_duration_ms: float = 250.0


@dataclass
class TrajectoryVector:
    """Extrapolated ballistic saccade vector with heading, velocity, and cone aperture."""
    origin_x: float
    origin_y: float
    heading_deg: float
    velocity_px_per_ms: float
    confidence: float  # 0.0 to 1.0
    cone_angle_deg: float = 40.0


@dataclass
class PreFetchCandidate:
    """A prospective canvas target node scored for pre-fetching priority."""
    node_id: str
    title: str
    pos_x: float
    pos_y: float
    distance_px: float
    angle_offset_deg: float
    priority_score: float  # 0.0 to 1.0
    pre_fetch_tier: str  # focal, parafoveal, peripheral


@dataclass
class SaccadicPredictionTelemetry:
    """Comprehensive telemetry report for predictive saccadic pre-fetching."""
    recent_fixations_count: int
    current_trajectory: Optional[TrajectoryVector]
    candidate_count: int
    pre_fetch_candidates: List[PreFetchCandidate] = field(default_factory=list)
    predictive_efficiency_score: float = 0.0
    recommended_cache_size: int = 3


class SaccadicTrajectoryPredictor:
    """
    Autonomous engine that extrapolates eye movement trajectories and computes
    pre-fetch priority for peripheral nodes ahead of ballistic saccades.
    """

    def __init__(self, max_prediction_distance_px: float = 600.0):
        self.max_prediction_distance_px = float(max_prediction_distance_px)

    def predict_trajectory(self, fixations: List[FixationPoint]) -> Optional[TrajectoryVector]:
        """
        Extrapolates forward velocity and angular heading from the most recent fixations.
        Requires at least two fixation points.
        """
        if not fixations or len(fixations) < 2:
            return None

        # Take last two fixations
        p1 = fixations[-2]
        p2 = fixations[-1]

        dx = p2.x - p1.x
        dy = p2.y - p1.y
        dist = math.hypot(dx, dy)

        dt = max(1.0, p2.timestamp_ms - (p1.timestamp_ms + p1.dwell_duration_ms))
        velocity = dist / dt

        angle_rad = math.atan2(dy, dx)
        angle_deg = (math.degrees(angle_rad) + 360.0) % 360.0

        # Confidence is higher if velocity is within realistic ballistic range (0.3 to 2.5 px/ms)
        if 0.2 <= velocity <= 3.0:
            confidence = 0.90
        elif velocity < 0.2:
            confidence = 0.50  # Slow drift / fixational jitter
        else:
            confidence = 0.65  # Extremely rapid jump

        # If there are 3+ points, check heading consistency
        if len(fixations) >= 3:
            p0 = fixations[-3]
            dx0 = p1.x - p0.x
            dy0 = p1.y - p0.y
            angle0_deg = (math.degrees(math.atan2(dy0, dx0)) + 360.0) % 360.0
            angular_diff = abs((angle_deg - angle0_deg + 180.0) % 360.0 - 180.0)
            if angular_diff < 30.0:
                confidence = min(0.98, confidence + 0.10)
            elif angular_diff > 90.0:
                confidence = max(0.35, confidence - 0.25)

        return TrajectoryVector(
            origin_x=round(p2.x, 1),
            origin_y=round(p2.y, 1),
            heading_deg=round(angle_deg, 1),
            velocity_px_per_ms=round(velocity, 3),
            confidence=round(confidence, 2),
            cone_angle_deg=40.0,
        )

    def evaluate_pre_fetch_candidates(
        self,
        fixations: List[FixationPoint],
        candidate_nodes: List[Dict[str, Any]],
    ) -> SaccadicPredictionTelemetry:
        """
        Evaluates potential target nodes against extrapolated trajectory vector.
        Classifies targets into focal, parafoveal, and peripheral pre-fetch tiers.
        """
        traj = self.predict_trajectory(fixations)
        if not traj or not candidate_nodes:
            return SaccadicPredictionTelemetry(
                recent_fixations_count=len(fixations),
                current_trajectory=traj,
                candidate_count=0,
                pre_fetch_candidates=[],
                predictive_efficiency_score=0.0,
                recommended_cache_size=1,
            )

        scored_candidates: List[PreFetchCandidate] = []
        heading_rad = math.radians(traj.heading_deg)

        for node in candidate_nodes:
            n_id = str(node.get("id", node.get("node_id", "node")))
            title = str(node.get("title", "Node"))
            nx = float(node.get("x", node.get("pos_x", 0.0)))
            ny = float(node.get("y", node.get("pos_y", 0.0)))

            dx = nx - traj.origin_x
            dy = ny - traj.origin_y
            dist = math.hypot(dx, dy)

            # Skip the origin point itself or overly distant nodes
            if dist < 15.0 or dist > self.max_prediction_distance_px * 1.5:
                continue

            node_angle_rad = math.atan2(dy, dx)
            node_angle_deg = (math.degrees(node_angle_rad) + 360.0) % 360.0
            angle_diff = abs((node_angle_deg - traj.heading_deg + 180.0) % 360.0 - 180.0)

            # Angular penalty: nodes within cone get higher priority
            half_cone = traj.cone_angle_deg / 2.0
            if angle_diff <= half_cone:
                angle_score = 1.0 - (angle_diff / half_cone) * 0.4
            else:
                angle_score = max(0.05, 0.6 - (angle_diff - half_cone) / 90.0)

            # Distance score: optimal distance matches expected saccade distance (150-400px)
            if 100.0 <= dist <= 450.0:
                dist_score = 1.0 - abs(dist - 250.0) / 350.0
            elif dist < 100.0:
                dist_score = 0.75
            else:
                dist_score = max(0.1, 1.0 - (dist - 450.0) / 450.0)

            # Semantic weight (if provided)
            weight = float(node.get("weight", node.get("saliency", 1.0)))
            raw_priority = (0.55 * angle_score + 0.35 * dist_score + 0.10 * (weight / 2.0)) * traj.confidence
            priority = max(0.0, min(1.0, raw_priority))

            # Tier classification
            if priority >= 0.70:
                tier = "focal"
            elif priority >= 0.40:
                tier = "parafoveal"
            else:
                tier = "peripheral"

            scored_candidates.append(
                PreFetchCandidate(
                    node_id=n_id,
                    title=title,
                    pos_x=round(nx, 1),
                    pos_y=round(ny, 1),
                    distance_px=round(dist, 1),
                    angle_offset_deg=round(angle_diff, 1),
                    priority_score=round(priority, 3),
                    pre_fetch_tier=tier,
                )
            )

        # Sort by priority descending
        scored_candidates.sort(key=lambda c: c.priority_score, reverse=True)

        # Efficiency calculation
        top_candidates = scored_candidates[:4]
        mean_top = (
            sum(c.priority_score for c in top_candidates) / len(top_candidates)
            if top_candidates
            else 0.0
        )
        efficiency = round(mean_top * traj.confidence, 3)

        rec_cache = min(6, max(2, len([c for c in scored_candidates if c.priority_score >= 0.50])))

        return SaccadicPredictionTelemetry(
            recent_fixations_count=len(fixations),
            current_trajectory=traj,
            candidate_count=len(scored_candidates),
            pre_fetch_candidates=scored_candidates,
            predictive_efficiency_score=efficiency,
            recommended_cache_size=rec_cache,
        )

    def generate_markdown_report(self, telemetry: SaccadicPredictionTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        traj = telemetry.current_trajectory
        lines = [
            "# Saccadic Trajectory Predictor and Predictive Pre-Fetcher Report",
            "",
            "## 1. Ocular Kinetic Trajectory Overview",
            f"- **Recorded Fixations in Window:** {telemetry.recent_fixations_count}",
        ]

        if traj:
            lines.extend([
                f"- **Current Extrapolated Origin:** ({traj.origin_x}, {traj.origin_y}) px",
                f"- **Heading Vector:** {traj.heading_deg} deg (Velocity: {traj.velocity_px_per_ms} px/ms)",
                f"- **Prediction Confidence:** {int(traj.confidence * 100)}%",
                f"- **Aperture Cone:** {traj.cone_angle_deg} deg",
            ])
        else:
            lines.append("- **Current Extrapolated Origin:** Insufficient fixations for trajectory calculation")

        lines.extend([
            f"- **Predictive Pre-Fetch Efficiency:** {telemetry.predictive_efficiency_score}",
            f"- **Recommended GPU/DOM Pre-Fetch Cache:** {telemetry.recommended_cache_size} nodes",
            "",
            "## 2. Neuro-Cognitive Theoretical Basis",
            "- **Carpenter LATER Model:** Ballistic saccade launch follows linear accumulation to decision thresholds.",
            "- **Rayner Parafoveal Preview:** Previewing tokens 3-5 degrees from fovea accelerates visual assimilation.",
            "- **Zero-Latency Spatial Hopping:** Pre-rendering prospective fixation targets avoids UI re-layout stutters.",
            "",
            "## 3. Prioritized Pre-Fetch Candidate Hierarchy",
            "| Node ID | Title | Distance (px) | Angle Offset | Priority Score | Tier | Position |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for c in telemetry.pre_fetch_candidates[:8]:
            lines.append(
                f"| `{c.node_id}` | {c.title} | {c.distance_px} | {c.angle_offset_deg} deg | {c.priority_score} | `{c.pre_fetch_tier}` | ({c.pos_x}, {c.pos_y}) |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Recommendations",
            "- Allocate high-resolution textures and expanded AST branches to 'focal' tier nodes.",
            "- Parafoveal tier nodes should receive skeleton wireframes and title metadata.",
            "- Peripheral tier nodes remain in low-density representation to conserve DOM memory.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: SaccadicPredictionTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium saccadic trajectory HUD SVG."""
        traj = telemetry.current_trajectory
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d18; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <linearGradient id="coneGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.35"/>',
            '    <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.02"/>',
            '  </linearGradient>',
            '  <filter id="nodeGlow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur"/>',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over"/>',
            '  </filter>',
            '</defs>',
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#090d18"/>',
            '<!-- Background Grid -->',
        ]

        # Subtle grid
        for gx in range(0, width, 60):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#1e293b" stroke-width="0.7" opacity="0.4"/>')
        for gy in range(0, height, 60):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#1e293b" stroke-width="0.7" opacity="0.4"/>')

        if traj:
            # Draw trajectory cone
            ox, oy = traj.origin_x, traj.origin_y
            cone_dist = min(self.max_prediction_distance_px, 450.0)
            h_rad = math.radians(traj.heading_deg)
            half_c = math.radians(traj.cone_angle_deg / 2.0)

            left_rad = h_rad - half_c
            right_rad = h_rad + half_c

            lx = ox + cone_dist * math.cos(left_rad)
            ly = oy + cone_dist * math.sin(left_rad)
            rx = ox + cone_dist * math.cos(right_rad)
            ry = oy + cone_dist * math.sin(right_rad)

            # Cone polygon
            svg_parts.append(
                f'<path d="M {ox} {oy} L {lx} {ly} A {cone_dist} {cone_dist} 0 0 1 {rx} {ry} Z" fill="url(#coneGrad)" stroke="#0284c7" stroke-width="1.2" stroke-dasharray="3,3"/>'
            )

            # Central heading arrow
            ax = ox + (cone_dist * 0.85) * math.cos(h_rad)
            ay = oy + (cone_dist * 0.85) * math.sin(h_rad)
            svg_parts.append(
                f'<line x1="{ox}" y1="{oy}" x2="{ax}" y2="{ay}" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>'
            )
            svg_parts.append(
                f'<circle cx="{ax}" cy="{ay}" r="4" fill="#38bdf8"/>'
            )

            # Origin Fixation Point
            svg_parts.append(
                f'<circle cx="{ox}" cy="{oy}" r="9" fill="#0284c7" stroke="#ffffff" stroke-width="2" filter="url(#nodeGlow)"/>'
            )
            svg_parts.append(
                f'<text x="{ox}" y="{oy - 14}" font-size="10" font-weight="700" fill="#38bdf8" text-anchor="middle">ACTIVE FOVEAL FIXATION</text>'
            )

        # Draw Candidate Nodes
        for c in telemetry.pre_fetch_candidates:
            if c.pre_fetch_tier == "focal":
                fill_c = "#22c55e"
                stroke_c = "#86efac"
                radius = 12.0
            elif c.pre_fetch_tier == "parafoveal":
                fill_c = "#eab308"
                stroke_c = "#fde047"
                radius = 9.0
            else:
                fill_c = "#64748b"
                stroke_c = "#94a3b8"
                radius = 6.0

            svg_parts.append(
                f'<circle cx="{c.pos_x}" cy="{c.pos_y}" r="{radius}" fill="{fill_c}" stroke="{stroke_c}" stroke-width="1.5"/>'
            )
            svg_parts.append(
                f'<text x="{c.pos_x}" y="{c.pos_y + radius + 12}" font-size="9" font-weight="600" fill="#f8fafc" text-anchor="middle">{html.escape(c.title)}</text>'
            )
            svg_parts.append(
                f'<text x="{c.pos_x}" y="{c.pos_y + radius + 22}" font-size="7.5" fill="#94a3b8" text-anchor="middle">P={c.priority_score}</text>'
            )

        # HUD Card Box
        svg_parts.append(
            f'<rect x="20" y="20" width="370" height="76" rx="8" fill="#0f172a" fill-opacity="0.9" stroke="#38bdf8" stroke-width="1.2"/>'
        )
        svg_parts.append(
            '<text x="32" y="40" font-size="11" font-weight="700" fill="#38bdf8">SACCADIC TRAJECTORY PREDICTOR HUD</text>'
        )
        if traj:
            svg_parts.append(
                f'<text x="32" y="56" font-size="9" fill="#94a3b8">Heading: {traj.heading_deg} deg | Vel: {traj.velocity_px_per_ms} px/ms | Conf: {int(traj.confidence * 100)}%</text>'
            )
            svg_parts.append(
                f'<text x="32" y="72" font-size="9" fill="#94a3b8">Candidates: {telemetry.candidate_count} | Pre-Fetch Efficiency: {telemetry.predictive_efficiency_score} | Cache: {telemetry.recommended_cache_size}</text>'
            )
        else:
            svg_parts.append(
                '<text x="32" y="58" font-size="9" fill="#94a3b8">Status: Calibrating gaze fixation path...</text>'
            )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_saccadic_session() -> Tuple[List[FixationPoint], List[Dict[str, Any]]]:
    """Generates demonstration ocular fixation path and candidate target nodes."""
    fixations = [
        FixationPoint("fix-0", "Canvas Origin", 150.0, 200.0, 100.0, 250.0),
        FixationPoint("fix-1", "Authentication Hub", 260.0, 220.0, 400.0, 220.0),
        FixationPoint("fix-2", "Token Validator", 420.0, 250.0, 700.0, 240.0),
    ]

    candidates = [
        {"id": "cand-1", "title": "Session Cache", "x": 620.0, "y": 280.0, "weight": 1.4},     # Directly ahead in cone -> Focal
        {"id": "cand-2", "title": "Database Pool", "x": 580.0, "y": 380.0, "weight": 1.1},     # Parafoveal
        {"id": "cand-3", "title": "User Profile", "x": 520.0, "y": 140.0, "weight": 0.9},      # Parafoveal upper
        {"id": "cand-4", "title": "Logging Conduit", "x": 780.0, "y": 310.0, "weight": 0.7},   # Far forward
        {"id": "cand-5", "title": "Legacy Stylesheet", "x": 200.0, "y": 450.0, "weight": 0.5}, # Behind/lateral -> Peripheral
        {"id": "cand-6", "title": "Analytics Tracker", "x": 180.0, "y": 100.0, "weight": 0.6}, # Backward
    ]

    return fixations, candidates
