"""
Semantic Entropy Gate & Topological Density Equalizer
Grounding: Shannon-Wiener information entropy, Cowan working memory limits (N <= 4),
Itti-Koch visual conspicuity models, and topological density redistribution.
Strict rule: Zero em dashes across all code, comments, docstrings, and outputs.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import json


@dataclass
class SemanticNode:
    """Represents a spatial canvas node with coordinate and semantic payload."""
    node_id: str
    label: str
    x: float
    y: float
    token_count: int = 10
    concept_count: int = 2
    edge_count: int = 1
    cluster_id: str = "default"

    @property
    def semantic_mass(self) -> float:
        """Computes weighted semantic mass based on tokens, concepts, and relational degree."""
        return max(1.0, float(self.token_count) * 0.2 + float(self.concept_count) * 1.5 + float(self.edge_count) * 0.8)


@dataclass
class LocalEntropyMeasurement:
    """Localized Shannon-Wiener entropy and spatial crowding metrics."""
    node_id: str
    neighbor_count: int
    local_semantic_mass: float
    shannon_entropy: float
    normalized_entropy: float
    local_density: float
    crowding_level: str  # "optimal", "moderate", "critical"


@dataclass
class RedistributedNode:
    """Represents a node after spatial topological density equalization."""
    node_id: str
    label: str
    cluster_id: str
    original_x: float
    original_y: float
    adjusted_x: float
    adjusted_y: float
    displacement: float
    pre_local_density: float
    post_local_density: float


@dataclass
class DensityEqualizerTelemetry:
    """Aggregated telemetry from entropy evaluation and density redistribution."""
    total_nodes: int
    radius: float
    global_entropy: float
    initial_density_variance: float
    equalized_density_variance: float
    variance_reduction_percent: float
    critical_crowding_count: int
    max_displacement: float
    mean_displacement: float
    redistributed_nodes: List[RedistributedNode] = field(default_factory=list)
    measurements: List[LocalEntropyMeasurement] = field(default_factory=list)


class SemanticEntropyEqualizer:
    """
    Evaluates Shannon-Wiener entropy on spatial canvases and redistributes
    topological cluster density to protect Cowan working memory bounds.
    """

    def __init__(self, radius: float = 120.0, alpha: float = 0.2, beta: float = 1.5, gamma: float = 0.8):
        self.radius = max(10.0, float(radius))
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def calculate_distance(self, n1: SemanticNode, n2: SemanticNode) -> float:
        """Euclidean distance between two nodes."""
        dx = n1.x - n2.x
        dy = n1.y - n2.y
        return math.sqrt(dx * dx + dy * dy)

    def calculate_coord_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Euclidean distance between coordinates."""
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx * dx + dy * dy)

    def measure_local_entropy(self, nodes: List[SemanticNode]) -> List[LocalEntropyMeasurement]:
        """
        Calculates localized Shannon-Wiener entropy and density for every node.
        """
        if not nodes:
            return []

        area = math.pi * (self.radius ** 2)
        measurements: List[LocalEntropyMeasurement] = []

        for target in nodes:
            neighbors: List[SemanticNode] = []
            for candidate in nodes:
                dist = self.calculate_distance(target, candidate)
                if dist <= self.radius:
                    neighbors.append(candidate)

            neighbor_count = len(neighbors)
            total_mass = sum(n.semantic_mass for n in neighbors)

            # Shannon-Wiener entropy calculation
            shannon_h = 0.0
            if total_mass > 0.0 and neighbor_count > 1:
                for n in neighbors:
                    p = n.semantic_mass / total_mass
                    if p > 0.0:
                        shannon_h -= p * math.log2(p)

            max_h = math.log2(float(neighbor_count)) if neighbor_count > 1 else 1.0
            normalized_h = shannon_h / max_h if max_h > 0.0 else 0.0

            # Local density (mass per 10k pixels squared)
            local_density = (total_mass / area) * 10000.0

            if local_density > 15.0 or (neighbor_count > 4 and normalized_h > 0.85):
                crowding = "critical"
            elif local_density > 8.0 or neighbor_count > 3:
                crowding = "moderate"
            else:
                crowding = "optimal"

            measurements.append(LocalEntropyMeasurement(
                node_id=target.node_id,
                neighbor_count=neighbor_count,
                local_semantic_mass=round(total_mass, 2),
                shannon_entropy=round(shannon_h, 3),
                normalized_entropy=round(normalized_h, 3),
                local_density=round(local_density, 3),
                crowding_level=crowding
            ))

        return measurements

    def equalize_density(
        self,
        nodes: List[SemanticNode],
        iterations: int = 40,
        repulsion_scale: float = 800.0,
        cluster_cohesion: float = 0.05,
        bounds: Optional[Tuple[float, float, float, float]] = None
    ) -> DensityEqualizerTelemetry:
        """
        Executes repulsive harmonic relaxation on high-density nodes to disperse
        cognitive crowding while preserving semantic cluster topology.
        """
        if not nodes:
            return DensityEqualizerTelemetry(
                total_nodes=0,
                radius=self.radius,
                global_entropy=0.0,
                initial_density_variance=0.0,
                equalized_density_variance=0.0,
                variance_reduction_percent=0.0,
                critical_crowding_count=0,
                max_displacement=0.0,
                mean_displacement=0.0
            )

        pre_measurements = self.measure_local_entropy(nodes)
        pre_densities = [m.local_density for m in pre_measurements]
        pre_mean_d = sum(pre_densities) / len(pre_densities)
        pre_variance = sum((d - pre_mean_d) ** 2 for d in pre_densities) / len(pre_densities)

        # Cluster centroids for cluster cohesion
        cluster_centroids: Dict[str, Tuple[float, float, int]] = {}
        for n in nodes:
            cx, cy, count = cluster_centroids.get(n.cluster_id, (0.0, 0.0, 0))
            cluster_centroids[n.cluster_id] = (cx + n.x, cy + n.y, count + 1)

        centroids: Dict[str, Tuple[float, float]] = {
            cid: (cx / float(cnt), cy / float(cnt))
            for cid, (cx, cy, cnt) in cluster_centroids.items() if cnt > 0
        }

        # Simulation positions (working copies)
        positions: Dict[str, List[float]] = {n.node_id: [float(n.x), float(n.y)] for n in nodes}
        masses: Dict[str, float] = {n.node_id: n.semantic_mass for n in nodes}
        clusters: Dict[str, str] = {n.node_id: n.cluster_id for n in nodes}

        # Iterative force-directed relaxation
        for _ in range(iterations):
            forces: Dict[str, List[float]] = {n.node_id: [0.0, 0.0] for n in nodes}

            # Pairwise repulsion when distance < radius
            for i in range(len(nodes)):
                n1 = nodes[i]
                p1 = positions[n1.node_id]
                for j in range(i + 1, len(nodes)):
                    n2 = nodes[j]
                    p2 = positions[n2.node_id]

                    dx = p1[0] - p2[0]
                    dy = p1[1] - p2[1]
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < 0.001:
                        dist = 0.001
                        dx = 0.001

                    if dist < self.radius:
                        # Repulsion inversely proportional to distance
                        factor = (repulsion_scale * (masses[n1.node_id] * masses[n2.node_id]) ** 0.5) / (dist * dist + 10.0)
                        fx = (dx / dist) * factor
                        fy = (dy / dist) * factor
                        forces[n1.node_id][0] += fx
                        forces[n1.node_id][1] += fy
                        forces[n2.node_id][0] -= fx
                        forces[n2.node_id][1] -= fy

            # Cluster cohesion pulling back toward cluster centroid
            for n in nodes:
                cid = clusters[n.node_id]
                if cid in centroids:
                    cx, cy = centroids[cid]
                    px, py = positions[n.node_id]
                    forces[n.node_id][0] += (cx - px) * cluster_cohesion
                    forces[n.node_id][1] += (cy - py) * cluster_cohesion

            # Update positions with damping
            damping = 0.15
            for n in nodes:
                nid = n.node_id
                fx, fy = forces[nid]
                # Clamp displacement per iteration to 15.0 px
                step = math.sqrt(fx * fx + fy * fy)
                if step > 15.0:
                    fx = (fx / step) * 15.0
                    fy = (fy / step) * 15.0
                positions[nid][0] += fx * damping
                positions[nid][1] += fy * damping

                # Optional canvas bounding (min_x, min_y, max_x, max_y)
                if bounds:
                    positions[nid][0] = max(bounds[0], min(bounds[2], positions[nid][0]))
                    positions[nid][1] = max(bounds[1], min(bounds[3], positions[nid][1]))

        # Create equalized node objects to measure post-distribution density
        equalized_nodes = [
            SemanticNode(
                node_id=n.node_id,
                label=n.label,
                x=positions[n.node_id][0],
                y=positions[n.node_id][1],
                token_count=n.token_count,
                concept_count=n.concept_count,
                edge_count=n.edge_count,
                cluster_id=n.cluster_id
            )
            for n in nodes
        ]

        post_measurements = self.measure_local_entropy(equalized_nodes)
        post_densities = [m.local_density for m in post_measurements]
        post_mean_d = sum(post_densities) / len(post_densities)
        post_variance = sum((d - post_mean_d) ** 2 for d in post_densities) / len(post_densities)

        reduction_pct = 0.0
        if pre_variance > 0.0:
            reduction_pct = max(0.0, ((pre_variance - post_variance) / pre_variance) * 100.0)

        displacements: List[float] = []
        redistributed_nodes: List[RedistributedNode] = []

        pre_map = {m.node_id: m for m in pre_measurements}
        post_map = {m.node_id: m for m in post_measurements}

        for n in nodes:
            nid = n.node_id
            ax, ay = positions[nid]
            disp = self.calculate_coord_distance(n.x, n.y, ax, ay)
            displacements.append(disp)

            redistributed_nodes.append(RedistributedNode(
                node_id=nid,
                label=n.label,
                cluster_id=n.cluster_id,
                original_x=round(n.x, 2),
                original_y=round(n.y, 2),
                adjusted_x=round(ax, 2),
                adjusted_y=round(ay, 2),
                displacement=round(disp, 2),
                pre_local_density=pre_map[nid].local_density,
                post_local_density=post_map[nid].local_density
            ))

        total_mass_all = sum(n.semantic_mass for n in nodes)
        global_h = 0.0
        if total_mass_all > 0.0 and len(nodes) > 1:
            for n in nodes:
                p = n.semantic_mass / total_mass_all
                if p > 0.0:
                    global_h -= p * math.log2(p)

        critical_count = sum(1 for m in pre_measurements if m.crowding_level == "critical")

        return DensityEqualizerTelemetry(
            total_nodes=len(nodes),
            radius=self.radius,
            global_entropy=round(global_h, 3),
            initial_density_variance=round(pre_variance, 3),
            equalized_density_variance=round(post_variance, 3),
            variance_reduction_percent=round(reduction_pct, 1),
            critical_crowding_count=critical_count,
            max_displacement=round(max(displacements) if displacements else 0.0, 2),
            mean_displacement=round(sum(displacements) / len(displacements) if displacements else 0.0, 2),
            redistributed_nodes=redistributed_nodes,
            measurements=post_measurements
        )

    def generate_svg(self, telemetry: DensityEqualizerTelemetry, width: int = 900, height: int = 560) -> str:
        """
        Generates dark titanium SVG diagram visualizing original positions,
        displacement trajectory vectors, and equalized node boundaries.
        """
        nodes = telemetry.redistributed_nodes
        if not nodes:
            return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <rect width="100%" height="100%" fill="#09090b"/>
  <text x="50%" y="50%" fill="#71717a" font-family="system-ui, sans-serif" font-size="14" text-anchor="middle">No nodes to visualize</text>
</svg>'''

        min_x = min(min(n.original_x for n in nodes), min(n.adjusted_x for n in nodes))
        max_x = max(max(n.original_x for n in nodes), max(n.adjusted_x for n in nodes))
        min_y = min(min(n.original_y for n in nodes), min(n.adjusted_y for n in nodes))
        max_y = max(max(n.original_y for n in nodes), max(n.adjusted_y for n in nodes))

        pad = 60.0
        data_w = max(1.0, max_x - min_x)
        data_h = max(1.0, max_y - min_y)
        draw_w = float(width) - pad * 2.0
        draw_h = float(height) - pad * 2.0 - 50.0  # leave header room

        def scale_x(val: float) -> float:
            return pad + ((val - min_x) / data_w) * draw_w

        def scale_y(val: float) -> float:
            return 80.0 + ((val - min_y) / data_h) * draw_h

        svg_parts: List[str] = [
            f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <radialGradient id="cardGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="vectorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.9"/>
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#10b981"/>
    </marker>
  </defs>

  <!-- Background Base Canvas -->
  <rect width="100%" height="100%" fill="#09090b" rx="14"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" fill="none" stroke="#27272a" stroke-width="1.5" rx="13"/>

  <!-- Header Section -->
  <text x="32" y="38" fill="#fafafa" font-family="system-ui, sans-serif" font-size="16" font-weight="700">Topological Density Equalizer and Semantic Entropy Gate</text>
  <text x="32" y="58" fill="#71717a" font-family="system-ui, sans-serif" font-size="12">Shannon Entropy: {telemetry.global_entropy} bits | Variance Reduced: {telemetry.variance_reduction_percent}% | Max Shift: {telemetry.max_displacement}px</text>

  <!-- Status Badges -->
  <g transform="translate({width - 280}, 24)">
    <rect width="120" height="24" rx="6" fill="#18181b" stroke="#27272a"/>
    <circle cx="14" cy="12" r="4" fill="#f59e0b"/>
    <text x="26" y="16" fill="#a1a1aa" font-family="system-ui, sans-serif" font-size="10">Original Ghost</text>

    <rect x="130" width="130" height="24" rx="6" fill="#18181b" stroke="#27272a"/>
    <circle cx="144" cy="12" r="4" fill="#10b981"/>
    <text x="156" y="16" fill="#a1a1aa" font-family="system-ui, sans-serif" font-size="10">Equalized Node</text>
  </g>
'''
        ]

        # Render displacement vectors
        for n in nodes:
            ox = scale_x(n.original_x)
            oy = scale_y(n.original_y)
            ax = scale_x(n.adjusted_x)
            ay = scale_y(n.adjusted_y)

            if n.displacement > 2.0:
                svg_parts.append(
                    f'  <line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="url(#vectorGrad)" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arrow)"/>'
                )

        # Render original ghost positions
        for n in nodes:
            ox = scale_x(n.original_x)
            oy = scale_y(n.original_y)
            svg_parts.append(
                f'  <circle cx="{ox:.1f}" cy="{oy:.1f}" r="5" fill="none" stroke="#f59e0b" stroke-width="1.2" opacity="0.4"/>'
            )

        # Render equalized adjusted nodes
        for n in nodes:
            ax = scale_x(n.adjusted_x)
            ay = scale_y(n.adjusted_y)

            # Density indicator color
            if n.post_local_density > 12.0:
                node_color = "#ef4444"
            elif n.post_local_density > 7.0:
                node_color = "#38bdf8"
            else:
                node_color = "#10b981"

            svg_parts.append(f'''  <g transform="translate({ax:.1f}, {ay:.1f})">
    <circle r="16" fill="url(#cardGlow)"/>
    <circle r="7" fill="#18181b" stroke="{node_color}" stroke-width="2"/>
    <text x="12" y="4" fill="#e4e4e7" font-family="system-ui, sans-serif" font-size="10" font-weight="500">{n.label}</text>
  </g>''')

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def generate_markdown_report(self, telemetry: DensityEqualizerTelemetry) -> str:
        """
        Synthesizes a publication-ready markdown compliance audit for spatial density.
        """
        lines: List[str] = [
            "# Topological Density Equalizer and Semantic Entropy Audit",
            "",
            "## 1. Executive Telemetry Overview",
            f"- **Total Monitored Nodes:** {telemetry.total_nodes}",
            f"- **Perceptual Interaction Radius:** {telemetry.radius} px",
            f"- **Global Shannon Entropy:** {telemetry.global_entropy} bits",
            f"- **Initial Density Variance:** {telemetry.initial_density_variance}",
            f"- **Equalized Density Variance:** {telemetry.equalized_density_variance}",
            f"- **Variance Reduction:** {telemetry.variance_reduction_percent}%",
            f"- **Critical Crowded Nodes (Pre-Equalization):** {telemetry.critical_crowding_count}",
            f"- **Mean Topological Shift:** {telemetry.mean_displacement} px",
            f"- **Maximum Topological Shift:** {telemetry.max_displacement} px",
            "",
            "## 2. Theoretical Grounding",
            "- **Shannon-Wiener Information Entropy:** Local spatial entropy quantifies informational variety across localized foveal glance windows.",
            "- **Cowan Capacity Bounds (N <= 4):** Dense clusters exceeding 4 high-mass concepts within a glance window trigger visual crowding and attentional decay.",
            "- **Harmonic Repulsive Relaxation:** Topological relaxation equalizes spatial density while preserving relative cluster neighborhood boundaries.",
            "",
            "## 3. Node-by-Node Spatial Telemetry",
            "| Node ID | Label | Cluster | Orig (X, Y) | Equalized (X, Y) | Shift (px) | Pre-Density | Post-Density |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for n in telemetry.redistributed_nodes:
            lines.append(
                f"| `{n.node_id}` | {n.label} | `{n.cluster_id}` | ({n.original_x}, {n.original_y}) | ({n.adjusted_x}, {n.adjusted_y}) | {n.displacement} | {n.pre_local_density} | {n.post_local_density} |"
            )

        lines.extend([
            "",
            "## 4. Operational Recommendations",
            "- Nodes exhibiting Post-Density > 10.0 should be nested into hierarchical sub-canvas portals.",
            "- High-displacement nodes have been moved outward along density gradient lines to balance foveal fixation flow.",
            "- Maintain consistent card breathing room to prevent cognitive fatigue during prolonged analysis."
        ])

        return "\n".join(lines)


def sample_canvas_nodes() -> List[SemanticNode]:
    """Generates an illustrative spatial canvas with two dense clusters and scattered satellites."""
    return [
        # Cluster 1: Architecture Core (Crowded)
        SemanticNode("core-1", "Authentication Gateway", 200.0, 200.0, token_count=18, concept_count=4, edge_count=3, cluster_id="auth"),
        SemanticNode("core-2", "OAuth Token Vault", 215.0, 210.0, token_count=14, concept_count=3, edge_count=4, cluster_id="auth"),
        SemanticNode("core-3", "Session Cache", 205.0, 225.0, token_count=12, concept_count=2, edge_count=2, cluster_id="auth"),
        SemanticNode("core-4", "JWT Verifier", 220.0, 195.0, token_count=15, concept_count=3, edge_count=3, cluster_id="auth"),
        SemanticNode("core-5", "Rate Limiter", 195.0, 215.0, token_count=10, concept_count=2, edge_count=2, cluster_id="auth"),

        # Cluster 2: Data Pipeline (Moderate)
        SemanticNode("data-1", "Ingestion Kafka Queue", 550.0, 320.0, token_count=22, concept_count=4, edge_count=5, cluster_id="data"),
        SemanticNode("data-2", "Stream Filter", 570.0, 335.0, token_count=16, concept_count=3, edge_count=3, cluster_id="data"),
        SemanticNode("data-3", "Parquet Sink", 540.0, 345.0, token_count=19, concept_count=3, edge_count=2, cluster_id="data"),

        # Satellites (Optimal)
        SemanticNode("sat-1", "Metrics Prometheus", 750.0, 140.0, token_count=8, concept_count=1, edge_count=1, cluster_id="ops"),
        SemanticNode("sat-2", "Alertmanager Webhook", 120.0, 420.0, token_count=9, concept_count=2, edge_count=1, cluster_id="ops"),
    ]
