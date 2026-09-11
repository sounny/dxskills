"""
Knowledge Mesh Consolidator & Semantic Hyper-Graph Weaver Engine
Autonomous cognitive spatial module synthesizing cross-domain knowledge meshes,
tri-directional relational hyper-edges, and shared semantic primitive linking.
Grounded in Eide & Eide Interconnected Reasoning (I-strengths) and hyper-graph theory.
Connects disparate knowledge silos into cohesive multi-domain cognitive tapestries.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set, Optional, Any
import itertools
import math
import html


@dataclass
class MeshNode:
    """A conceptual node anchored within a specific knowledge domain."""
    node_id: str
    title: str
    domain: str
    semantic_primitives: List[str]
    pos_x: float = 0.0
    pos_y: float = 0.0
    weight: float = 1.0


@dataclass
class HyperEdge:
    """A multi-node hyper-edge binding conceptual nodes through a shared semantic primitive."""
    edge_id: str
    title: str
    shared_primitive: str
    member_node_ids: List[str]
    domains_spanned: List[str]
    coherence_score: float  # 0.0 to 1.0
    color_hex: str = "#38bdf8"


@dataclass
class DomainBridge:
    """A cross-domain resonance conduit connecting two knowledge spheres."""
    domain_a: str
    domain_b: str
    bridging_primitives: List[str]
    resonance_strength: float  # 0.0 to 1.0


@dataclass
class KnowledgeMeshTelemetry:
    """Comprehensive telemetry report for consolidated knowledge hyper-graphs."""
    total_nodes: int
    domain_count: int
    hyper_edges_count: int
    cross_domain_bridges_count: int
    hyper_edges: List[HyperEdge] = field(default_factory=list)
    domain_bridges: List[DomainBridge] = field(default_factory=list)
    mesh_density: float = 0.0
    interconnected_reasoning_index: float = 0.0


PALETTE = [
    "#38bdf8", "#818cf8", "#c084fc", "#f472b6",
    "#fb7185", "#fb923c", "#facc15", "#4ade80",
    "#2dd4bf", "#22d3ee"
]


class KnowledgeMeshWeaver:
    """
    Autonomous engine that discovers cross-domain isomorphisms and weaves
    multi-node hyper-edges into consolidated knowledge webs.
    """

    def __init__(self, min_cluster_size: int = 2):
        self.min_cluster_size = max(2, int(min_cluster_size))

    def weave_mesh(self, nodes: List[MeshNode]) -> KnowledgeMeshTelemetry:
        """
        Maps shared semantic primitives across nodes to form hyper-edges
        and computes inter-domain resonance bridges.
        """
        if not nodes:
            return KnowledgeMeshTelemetry(
                total_nodes=0,
                domain_count=0,
                hyper_edges_count=0,
                cross_domain_bridges_count=0,
                hyper_edges=[],
                domain_bridges=[],
                mesh_density=0.0,
                interconnected_reasoning_index=0.0,
            )

        unique_domains = sorted(list({n.domain for n in nodes}))

        # Invert index: primitive -> list of nodes
        primitive_map: Dict[str, List[MeshNode]] = {}
        for n in nodes:
            for p in n.semantic_primitives:
                p_norm = p.strip().lower()
                primitive_map.setdefault(p_norm, []).append(n)

        hyper_edges: List[HyperEdge] = []
        edge_idx = 1

        for prim, member_nodes in sorted(primitive_map.items()):
            if len(member_nodes) >= self.min_cluster_size:
                spanned_domains = sorted(list({m.domain for m in member_nodes}))
                # Coherence increases if multiple distinct domains are unified
                domain_diversity = len(spanned_domains) / max(1, len(unique_domains))
                coherence = min(1.0, 0.5 + 0.5 * domain_diversity)

                color = PALETTE[(edge_idx - 1) % len(PALETTE)]
                hyper_edges.append(
                    HyperEdge(
                        edge_id=f"he-{edge_idx:02d}",
                        title=f"Primitive: {prim.title()}",
                        shared_primitive=prim,
                        member_node_ids=[m.node_id for m in member_nodes],
                        domains_spanned=spanned_domains,
                        coherence_score=round(coherence, 2),
                        color_hex=color,
                    )
                )
                edge_idx += 1

        # Calculate cross-domain bridges
        domain_bridges: List[DomainBridge] = []
        domain_pairs = list(itertools.combinations(unique_domains, 2))

        for da, db in domain_pairs:
            nodes_a = [n for n in nodes if n.domain == da]
            nodes_b = [n for n in nodes if n.domain == db]

            prims_a = {p.strip().lower() for n in nodes_a for p in n.semantic_primitives}
            prims_b = {p.strip().lower() for n in nodes_b for p in n.semantic_primitives}

            shared = sorted(list(prims_a.intersection(prims_b)))
            if shared:
                union_len = max(1, len(prims_a.union(prims_b)))
                jaccard = len(shared) / union_len
                strength = min(1.0, 0.4 + 0.6 * jaccard)
                domain_bridges.append(
                    DomainBridge(
                        domain_a=da,
                        domain_b=db,
                        bridging_primitives=shared,
                        resonance_strength=round(strength, 2),
                    )
                )

        # Interconnected reasoning index
        total_possible_edges = max(1, len(nodes) * (len(nodes) - 1) // 2)
        mesh_density = round(len(hyper_edges) / max(1, len(nodes)), 2)

        mean_coherence = (
            sum(he.coherence_score for he in hyper_edges) / len(hyper_edges)
            if hyper_edges
            else 0.0
        )
        cross_domain_ratio = (
            len(domain_bridges) / max(1, len(domain_pairs))
            if domain_pairs
            else 0.0
        )
        iri = round(0.5 * mean_coherence + 0.5 * cross_domain_ratio, 3)

        return KnowledgeMeshTelemetry(
            total_nodes=len(nodes),
            domain_count=len(unique_domains),
            hyper_edges_count=len(hyper_edges),
            cross_domain_bridges_count=len(domain_bridges),
            hyper_edges=hyper_edges,
            domain_bridges=domain_bridges,
            mesh_density=mesh_density,
            interconnected_reasoning_index=iri,
        )

    def generate_markdown_report(self, telemetry: KnowledgeMeshTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lines = [
            "# Knowledge Mesh Consolidator and Semantic Hyper-Graph Weaver Report",
            "",
            "## 1. Interconnected Mesh Architecture Overview",
            f"- **Total Knowledge Nodes:** {telemetry.total_nodes}",
            f"- **Distinct Domains Spanned:** {telemetry.domain_count}",
            f"- **Consolidated Hyper-Edges:** {telemetry.hyper_edges_count}",
            f"- **Cross-Domain Isomorphic Bridges:** {telemetry.cross_domain_bridges_count}",
            f"- **Mesh Connectivity Density:** {telemetry.mesh_density} edges/node",
            f"- **Interconnected Reasoning Index (IRI):** {telemetry.interconnected_reasoning_index} (Scale: 0.0 to 1.0)",
            "",
            "## 2. Neuro-Cognitive Grounding (Eide & Eide I-Strengths)",
            "- **Cross-Disciplinary Isomorphism:** Dyslexic thinkers identify common structural primitives across silos.",
            "- **Hyper-Edge Unification:** Grouping multiple nodes under a single primitive avoids pairwise edge clutter.",
            "- **Resonance Bridges:** Quantifying shared primitive density unlocks non-linear analogy transfer.",
            "",
            "## 3. Discovered Hyper-Edge Envelopes",
            "| Edge ID | Primitive Title | Member Nodes | Spanned Domains | Coherence |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        for he in telemetry.hyper_edges:
            nodes_str = ", ".join(f"`{nid}`" for nid in he.member_node_ids)
            doms_str = ", ".join(he.domains_spanned)
            lines.append(
                f"| `{he.edge_id}` | {he.title} | {nodes_str} | {doms_str} | {he.coherence_score} |"
            )

        lines.extend([
            "",
            "## 4. Cross-Domain Resonance Bridges",
            "| Domain A | Domain B | Shared Primitives | Resonance Strength |",
            "| :--- | :--- | :--- | :--- |",
        ])

        for db in telemetry.domain_bridges:
            prims_str = ", ".join(f"`{p}`" for p in db.bridging_primitives)
            lines.append(
                f"| {db.domain_a} | {db.domain_b} | {prims_str} | {db.resonance_strength} |"
            )

        lines.extend([
            "",
            "## 5. Architectural Guidance",
            "- High-coherence hyper-edges should be rendered with shared translucent hull polygons.",
            "- Use resonant primitives as universal search indices across personal and institutional vaults.",
            "- Avoid duplicate implementation of buffering and queuing primitives across isolated subsystems.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        nodes: List[MeshNode],
        telemetry: KnowledgeMeshTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium knowledge hyper-graph SVG."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d18; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <filter id="meshGlow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur"/>',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over"/>',
            '  </filter>',
            '</defs>',
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#090d18"/>',
            '<!-- Subtle Matrix Grid -->',
        ]

        for gx in range(0, width, 50):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#1e293b" stroke-width="0.6" opacity="0.3"/>')
        for gy in range(0, height, 50):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#1e293b" stroke-width="0.6" opacity="0.3"/>')

        node_dict = {n.node_id: n for n in nodes}

        # Draw Hyper-Edge Hulls / Connecting Polygons
        for he in telemetry.hyper_edges:
            member_pts = [node_dict[nid] for nid in he.member_node_ids if nid in node_dict]
            if len(member_pts) >= 3:
                # Hull polygon
                pts_str = " ".join(f"{n.pos_x},{n.pos_y}" for n in member_pts)
                svg_parts.append(
                    f'<polygon points="{pts_str}" fill="{he.color_hex}" fill-opacity="0.08" stroke="{he.color_hex}" stroke-width="1.2" stroke-dasharray="4,4"/>'
                )
            elif len(member_pts) == 2:
                n1, n2 = member_pts
                svg_parts.append(
                    f'<line x1="{n1.pos_x}" y1="{n1.pos_y}" x2="{n2.pos_x}" y2="{n2.pos_y}" stroke="{he.color_hex}" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.6"/>'
                )

        # Draw Nodes
        for n in nodes:
            svg_parts.append(
                f'<circle cx="{n.pos_x}" cy="{n.pos_y}" r="11" fill="#1e293b" stroke="#38bdf8" stroke-width="1.8" filter="url(#meshGlow)"/>'
            )
            svg_parts.append(
                f'<text x="{n.pos_x}" y="{n.pos_y + 22}" font-size="9" font-weight="600" fill="#ffffff" text-anchor="middle">{html.escape(n.title)}</text>'
            )
            svg_parts.append(
                f'<text x="{n.pos_x}" y="{n.pos_y + 32}" font-size="7.5" fill="#94a3b8" text-anchor="middle">[{html.escape(n.domain)}]</text>'
            )

        # HUD Box
        svg_parts.append(
            f'<rect x="20" y="20" width="380" height="74" rx="8" fill="#0f172a" fill-opacity="0.9" stroke="#38bdf8" stroke-width="1.2"/>'
        )
        svg_parts.append(
            '<text x="32" y="38" font-size="11" font-weight="700" fill="#38bdf8">KNOWLEDGE MESH HYPER-GRAPH HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="54" font-size="9" fill="#94a3b8">Nodes: {telemetry.total_nodes} | Domains: {telemetry.domain_count} | Hyper-Edges: {telemetry.hyper_edges_count}</text>'
        )
        svg_parts.append(
            f'<text x="32" y="70" font-size="9" fill="#94a3b8">Cross-Bridges: {telemetry.cross_domain_bridges_count} | IRI: {telemetry.interconnected_reasoning_index} | Density: {telemetry.mesh_density}</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_knowledge_mesh() -> List[MeshNode]:
    """Generates demonstration multi-domain knowledge mesh nodes."""
    return [
        MeshNode("bio-1", "Cell Membrane Osmosis", "Biology", ["semi-permeable", "gradient", "buffering"], 180.0, 180.0),
        MeshNode("bio-2", "Immune Antigens", "Biology", ["pattern-matching", "signature", "adaptation"], 240.0, 320.0),
        MeshNode("sys-1", "Rate Limiter Gateway", "Distributed Systems", ["semi-permeable", "buffering", "backpressure"], 420.0, 160.0),
        MeshNode("sys-2", "Intrusion Detection", "Distributed Systems", ["pattern-matching", "signature", "anomaly"], 480.0, 340.0),
        MeshNode("urb-1", "Sponge City Swales", "Urbanism", ["buffering", "gradient", "retention"], 680.0, 200.0),
        MeshNode("urb-2", "Cordon Pricing Toll", "Urbanism", ["semi-permeable", "congestion", "backpressure"], 720.0, 350.0),
    ]
