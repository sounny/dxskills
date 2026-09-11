"""
schema_isomorphism_engine.py - Autonomous Cognitive Spatial Schema Isomorphism & Analogy Transfer Engine

Part of the DxSkills cognitive scaffolding suite (Phase 108, Cycle 104).
Grounded in Gentner (1983) Structure-Mapping Theory, Holyoak & Thagard (1989) Multiconstraint Theory,
and Eide & Eide (2011) Interconnected Reasoning in spatial cognition.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class SchemaNode:
    """Relational node representing an entity, concept, or component within a domain."""
    node_id: str
    label: str
    role: str  # SOURCE, TRANSFORMER, SINK, REGULATOR, BUFFER, TRANSPORT
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SchemaRelation:
    """Directed relational link connecting two schema nodes."""
    source_id: str
    target_id: str
    relation_type: str  # DRIVES, INHIBITS, CIRCULATES, STORES, AMPLIFIES, TRANSFORMS
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DomainSchema:
    """Topological schema graph representing relational structures within a knowledge domain."""
    domain_name: str
    nodes: List[SchemaNode]
    relations: List[SchemaRelation]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain_name": self.domain_name,
            "nodes": [n.to_dict() for n in self.nodes],
            "relations": [r.to_dict() for r in self.relations],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainSchema:
        dname = str(data.get("domain_name") or "Generic Domain")
        raw_nodes = data.get("nodes", [])
        raw_rels = data.get("relations", [])

        nodes = [
            SchemaNode(
                node_id=str(n.get("id") or n.get("node_id") or f"n_{idx+1}"),
                label=str(n.get("label") or n.get("name") or f"Node {idx+1}"),
                role=str(n.get("role") or "TRANSFORMER").upper(),
                attributes=dict(n.get("attributes", {})),
            )
            for idx, n in enumerate(raw_nodes)
        ]

        relations = [
            SchemaRelation(
                source_id=str(r.get("source") or r.get("source_id") or ""),
                target_id=str(r.get("target") or r.get("target_id") or ""),
                relation_type=str(r.get("relation") or r.get("relation_type") or "DRIVES").upper(),
                weight=float(r.get("weight", 1.0)),
            )
            for r in raw_rels
            if (r.get("source") or r.get("source_id")) and (r.get("target") or r.get("target_id"))
        ]

        return cls(domain_name=dname, nodes=nodes, relations=relations)


@dataclass
class NodeMapping:
    """1-to-1 structural correspondence between a source node and target node."""
    source_node_id: str
    target_node_id: str
    source_label: str
    target_label: str
    role_congruence: float  # 0.0 to 1.0 role similarity
    structural_degree_similarity: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IsomorphismResult:
    """Structural alignment metrics evaluating graph homomorphism fidelity."""
    isomorphism_score: float  # 0.0 to 1.0
    systematicity_index: float  # Gentner systematicity: preservation of relational systems
    node_mappings: List[NodeMapping]
    preserved_relations_count: int
    unmapped_relations_count: int
    is_valid_homomorphism: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "isomorphism_score": self.isomorphism_score,
            "systematicity_index": self.systematicity_index,
            "node_mappings": [m.to_dict() for m in self.node_mappings],
            "preserved_relations_count": self.preserved_relations_count,
            "unmapped_relations_count": self.unmapped_relations_count,
            "is_valid_homomorphism": self.is_valid_homomorphism,
        }


@dataclass
class IsomorphismTelemetry:
    """Telemetry capturing cognitive scale, bandwidth, and transfer strength."""
    source_nodes_count: int
    target_nodes_count: int
    mapped_nodes_count: int
    isomorphism_score: float
    systematicity_index: float
    inferences_projected_count: int
    cognitive_leap_magnitude: str  # CONCRETE, DOMAIN_ADJACENT, RADICAL_CROSS_DOMAIN
    cowan_bounded: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AnalogyTransferProjection:
    """Master result bundle containing structural mappings, generated inferences, and visual assets."""
    source_domain: str
    target_domain: str
    isomorphism: IsomorphismResult
    transferred_inferences: List[str]
    telemetry: IsomorphismTelemetry
    svg_projection_map: str
    transfer_report_md: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_domain": self.source_domain,
            "target_domain": self.target_domain,
            "isomorphism": self.isomorphism.to_dict(),
            "transferred_inferences": self.transferred_inferences,
            "telemetry": self.telemetry.to_dict(),
            "svg_projection_map": self.svg_projection_map,
            "transfer_report_md": self.transfer_report_md,
        }


class SchemaIsomorphismEngine:
    """
    Autonomous Cognitive Spatial Schema Isomorphism & Analogy Transfer Engine.

    Evaluates structural graph homomorphisms between disparate knowledge domains,
    computes Gentner systematicity preservation, and synthesizes novel inferences
    projecting causal solutions into destination conceptual spaces.
    """

    ROLE_COMPATIBILITY: Dict[str, Set[str]] = {
        "SOURCE": {"SOURCE", "REGULATOR", "TRANSPORT"},
        "TRANSFORMER": {"TRANSFORMER", "REGULATOR", "BUFFER"},
        "SINK": {"SINK", "BUFFER"},
        "REGULATOR": {"REGULATOR", "TRANSFORMER", "SOURCE"},
        "BUFFER": {"BUFFER", "SINK", "TRANSFORMER"},
        "TRANSPORT": {"TRANSPORT", "SOURCE"},
    }

    def __init__(self, min_alignment_threshold: float = 0.55) -> None:
        self.min_alignment_threshold = min_alignment_threshold

    def evaluate_isomorphism(
        self,
        source: DomainSchema,
        target: DomainSchema,
    ) -> IsomorphismResult:
        """Task 108.1: Structural schema isomorphism evaluator computing graph homomorphisms."""
        if not source.nodes or not target.nodes:
            return IsomorphismResult(
                isomorphism_score=0.0,
                systematicity_index=0.0,
                node_mappings=[],
                preserved_relations_count=0,
                unmapped_relations_count=len(source.relations),
                is_valid_homomorphism=False,
            )

        # Compute degree profiles for structural alignment
        src_out: Dict[str, int] = {}
        src_in: Dict[str, int] = {}
        for r in source.relations:
            src_out[r.source_id] = src_out.get(r.source_id, 0) + 1
            src_in[r.target_id] = src_in.get(r.target_id, 0) + 1

        tgt_out: Dict[str, int] = {}
        tgt_in: Dict[str, int] = {}
        for r in target.relations:
            tgt_out[r.source_id] = tgt_out.get(r.source_id, 0) + 1
            tgt_in[r.target_id] = tgt_in.get(r.target_id, 0) + 1

        # Greedy bipartite structural matching based on role congruence and degree similarity
        available_tgt = list(target.nodes)
        mappings: List[NodeMapping] = []

        for s_node in source.nodes:
            s_deg = src_out.get(s_node.node_id, 0) + src_in.get(s_node.node_id, 0)
            best_match: Optional[SchemaNode] = None
            best_sim = -1.0
            best_role_congruence = 0.0

            for t_node in available_tgt:
                t_deg = tgt_out.get(t_node.node_id, 0) + tgt_in.get(t_node.node_id, 0)

                # Role congruence with weighted priority
                if s_node.role == t_node.role:
                    role_cong = 1.0
                    role_weight = 0.85
                elif t_node.role in self.ROLE_COMPATIBILITY.get(s_node.role, set()):
                    role_cong = 0.60
                    role_weight = 0.65
                else:
                    role_cong = 0.20
                    role_weight = 0.50

                # Degree similarity (0 to 1)
                max_deg = max(1, max(s_deg, t_deg))
                deg_sim = 1.0 - (abs(s_deg - t_deg) / max_deg)

                combined = (role_cong * role_weight) + (deg_sim * (1.0 - role_weight))
                if combined > best_sim:
                    best_sim = combined
                    best_match = t_node
                    best_role_congruence = role_cong

            if best_match and best_sim >= 0.45:
                mappings.append(NodeMapping(
                    source_node_id=s_node.node_id,
                    target_node_id=best_match.node_id,
                    source_label=s_node.label,
                    target_label=best_match.label,
                    role_congruence=round(best_role_congruence, 2),
                    structural_degree_similarity=round(best_sim, 2),
                ))
                available_tgt.remove(best_match)

        # Evaluate preserved relational edges under mapping
        s2t = {m.source_node_id: m.target_node_id for m in mappings}
        target_edges: Set[Tuple[str, str]] = {(r.source_id, r.target_id) for r in target.relations}

        preserved_count = 0
        unmapped_count = 0

        for r in source.relations:
            mapped_src = s2t.get(r.source_id)
            mapped_tgt = s2t.get(r.target_id)
            if mapped_src and mapped_tgt and (mapped_src, mapped_tgt) in target_edges:
                preserved_count += 1
            else:
                unmapped_count += 1

        total_source_rels = max(1, len(source.relations))
        rel_preservation_ratio = preserved_count / total_source_rels
        node_mapping_ratio = len(mappings) / max(1, len(source.nodes))

        # Overall isomorphism score
        iso_score = round((node_mapping_ratio * 0.45) + (rel_preservation_ratio * 0.55), 2)

        # Gentner systematicity index: higher order relational density preservation
        systematicity = round(rel_preservation_ratio * (1.0 if preserved_count >= 2 else 0.75), 2)

        is_valid = iso_score >= self.min_alignment_threshold

        return IsomorphismResult(
            isomorphism_score=iso_score,
            systematicity_index=systematicity,
            node_mappings=mappings,
            preserved_relations_count=preserved_count,
            unmapped_relations_count=unmapped_count,
            is_valid_homomorphism=is_valid,
        )

    def synthesize_analogy_transfer(
        self,
        source: DomainSchema,
        target: DomainSchema,
    ) -> AnalogyTransferProjection:
        """Task 108.2: Cross-domain analogy transfer synthesizer projecting verified patterns."""
        iso = self.evaluate_isomorphism(source, target)

        s2t = {m.source_node_id: m.target_node_id for m in iso.node_mappings}
        target_labels = {n.node_id: n.label for n in target.nodes}
        source_labels = {n.node_id: n.label for n in source.nodes}
        target_edges: Set[Tuple[str, str]] = {(r.source_id, r.target_id) for r in target.relations}

        inferences: List[str] = []

        # Project inferences for unmapped source relations where nodes are mapped
        for r in source.relations:
            msrc = s2t.get(r.source_id)
            mtgt = s2t.get(r.target_id)
            if msrc and mtgt and (msrc, mtgt) not in target_edges:
                tl_src = target_labels.get(msrc, msrc)
                tl_tgt = target_labels.get(mtgt, mtgt)
                sl_src = source_labels.get(r.source_id, r.source_id)
                sl_tgt = source_labels.get(r.target_id, r.target_id)
                inferences.append(
                    f"Projected Relational Hypothesis: In {source.domain_name}, [{sl_src}] {r.relation_type} [{sl_tgt}]. "
                    f"Analogously in {target.domain_name}, [{tl_src}] should {r.relation_type.lower()} [{tl_tgt}] to stabilize systemic throughput."
                )

        # If all relations were already mapped or no direct projection was triggered
        if not inferences:
            inferences.append(
                f"Symmetric Structural Balance: All high-order relations in {source.domain_name} map directly into {target.domain_name} "
                "with full topological preservation. No missing systemic linkages detected."
            )

        # Cognitive leap magnitude categorization
        if iso.isomorphism_score >= 0.85:
            magnitude = "DOMAIN_ADJACENT"
        elif iso.isomorphism_score >= 0.60:
            magnitude = "RADICAL_CROSS_DOMAIN"
        else:
            magnitude = "CONCRETE"

        cowan_bounded = len(iso.node_mappings) <= 4

        telemetry = IsomorphismTelemetry(
            source_nodes_count=len(source.nodes),
            target_nodes_count=len(target.nodes),
            mapped_nodes_count=len(iso.node_mappings),
            isomorphism_score=iso.isomorphism_score,
            systematicity_index=iso.systematicity_index,
            inferences_projected_count=len(inferences),
            cognitive_leap_magnitude=magnitude,
            cowan_bounded=cowan_bounded,
        )

        # Generate Markdown Report
        md_lines = [
            f"# Cross-Domain Schema Isomorphism & Analogy Transfer Report",
            f"",
            f"**Source Domain:** {source.domain_name}  ",
            f"**Target Destination:** {target.domain_name}  ",
            f"**Isomorphism Score:** {telemetry.isomorphism_score:.2f} | **Systematicity Index:** {telemetry.systematicity_index:.2f}  ",
            f"**Cognitive Leap Magnitude:** [{telemetry.cognitive_leap_magnitude}]  ",
            f"",
            f"## Structural Node Correspondences",
            f"",
            f"| Source Node (`{source.domain_name}`) | Target Node (`{target.domain_name}`) | Role Congruence | Structural Alignment |",
            f"| :--- | :--- | :--- | :--- |",
        ]
        for m in iso.node_mappings:
            md_lines.append(
                f"| `{m.source_label}` | `{m.target_label}` | {m.role_congruence:.2f} | {m.structural_degree_similarity:.2f} |"
            )

        md_lines.append("")
        md_lines.append("## Projected Cross-Domain Inferences")
        md_lines.append("")
        for idx, inf in enumerate(inferences, 1):
            md_lines.append(f"{idx}. {inf}")

        report_md = "\n".join(md_lines)

        svg_map = self._render_projection_svg(
            source=source,
            target=target,
            iso=iso,
            telemetry=telemetry,
        )

        return AnalogyTransferProjection(
            source_domain=source.domain_name,
            target_domain=target.domain_name,
            isomorphism=iso,
            transferred_inferences=inferences,
            telemetry=telemetry,
            svg_projection_map=svg_map,
            transfer_report_md=report_md,
        )

    def _render_projection_svg(
        self,
        source: DomainSchema,
        target: DomainSchema,
        iso: IsomorphismResult,
        telemetry: IsomorphismTelemetry,
    ) -> str:
        """Renders dark titanium dual-domain isomorphic projection diagram."""
        w, h = 920, 520
        t = telemetry

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '  <defs>',
            '    <linearGradient id="isoBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#080c14"/>',
            '      <stop offset="100%" stop-color="#0f172a"/>',
            '    </linearGradient>',
            '    <linearGradient id="srcPill" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.2"/>',
            '      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.05"/>',
            '    </linearGradient>',
            '    <linearGradient id="tgtPill" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.2"/>',
            '      <stop offset="100%" stop-color="#7e22ce" stop-opacity="0.05"/>',
            '    </linearGradient>',
            '  </defs>',
            '  <rect width="100%" height="100%" fill="url(#isoBg)"/>',
            '  <!-- Header -->',
            '  <text x="40" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Schema Isomorphism &amp; Analogy Transfer Engine</text>',
            f'  <text x="40" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#94a3b8">Gentner Structure-Mapping &bull; Score: {t.isomorphism_score:.2f} &bull; Systematicity: {t.systematicity_index:.2f} &bull; Leap: [{t.cognitive_leap_magnitude}]</text>',
            '  <!-- Dual Column Mapping Area -->',
            '  <g transform="translate(40, 95)">',
            '    <!-- Source Box -->',
            '    <rect x="0" y="0" width="340" height="270" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            f'    <text x="20" y="32" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="700" fill="#38bdf8">SOURCE: {source.domain_name}</text>',
            '    <!-- Target Box -->',
            '    <rect x="500" y="0" width="340" height="270" rx="12" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            f'    <text x="520" y="32" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="700" fill="#c084fc">TARGET: {target.domain_name}</text>',
        ]

        # Draw Node Pairs and Cross-Domain Bridge Connectors
        y_offset = 60
        for idx, m in enumerate(iso.node_mappings[:5]):
            cur_y = y_offset + (idx * 40)
            svg_parts.extend([
                f'    <!-- Mapping {idx+1} -->',
                f'    <rect x="15" y="{cur_y}" width="310" height="30" rx="6" fill="url(#srcPill)" stroke="#38bdf8" stroke-width="1"/>',
                f'    <text x="25" y="{cur_y + 19}" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" fill="#f8fafc">{m.source_label}</text>',
                f'    <rect x="515" y="{cur_y}" width="310" height="30" rx="6" fill="url(#tgtPill)" stroke="#a855f7" stroke-width="1"/>',
                f'    <text x="525" y="{cur_y + 19}" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" fill="#f8fafc">{m.target_label}</text>',
                f'    <!-- Isomorphic Bridge Line -->',
                f'    <line x1="325" y1="{cur_y + 15}" x2="515" y2="{cur_y + 15}" stroke="#10b981" stroke-width="1.8" stroke-dasharray="3,3"/>',
                f'    <circle cx="420" cy="{cur_y + 15}" r="3" fill="#10b981"/>',
            ])

        svg_parts.append('  </g>')

        # Bottom Cards: Telemetry
        svg_parts.extend([
            '  <!-- Bottom Cards: Telemetry Badges -->',
            '  <g transform="translate(40, 390)">',
            '    <rect x="0" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="20" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Isomorphism Alignment</text>',
            f'    <text x="20" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#10b981">{t.isomorphism_score * 100:.0f}%</text>',
            f'    <text x="20" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Systematicity index: {t.systematicity_index:.2f}</text>',
            '    <rect x="290" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="310" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Transferred Hypotheses</text>',
            f'    <text x="310" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="800" fill="#38bdf8">{t.inferences_projected_count} Inferences</text>',
            f'    <text x="310" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">{iso.preserved_relations_count} preserved relations</text>',
            '    <rect x="580" y="0" width="260" height="85" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="600" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Cognitive Leap</text>',
            f'    <text x="600" y="56" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="800" fill="#a855f7">[{t.cognitive_leap_magnitude}]</text>',
            f'    <text x="600" y="74" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Cowan bounded: {t.cowan_bounded}</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg_parts)

    def export_svg(self, projection: AnalogyTransferProjection, output_path: Optional[str] = None) -> str:
        """Exports SVG diagram to file or returns XML string."""
        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(projection.svg_projection_map)
        return projection.svg_projection_map

    def generate_ascii_report(self, projection: AnalogyTransferProjection) -> str:
        """Generates terminal ASCII summary table of analogy transfer metrics."""
        t = projection.telemetry
        iso = projection.isomorphism
        lines = [
            "================================================================================",
            "   SCHEMA ISOMORPHISM & ANALOGY TRANSFER ENGINE (PHASE 108 / CYCLE 104)",
            "================================================================================",
            f" Source Domain         : {projection.source_domain}",
            f" Target Destination    : {projection.target_domain}",
            f" Isomorphism Score     : {t.isomorphism_score:.2f} (0.0 to 1.0 structural homomorphism)",
            f" Systematicity Index   : {t.systematicity_index:.2f} (Gentner relational preservation)",
            f" Mapped Node Entities  : {t.mapped_nodes_count} / {t.source_nodes_count} nodes",
            f" Relational Ties       : {iso.preserved_relations_count} preserved | {iso.unmapped_relations_count} unmapped",
            f" Cognitive Leap        : [{t.cognitive_leap_magnitude}]",
            f" Cowan Bounded (N<=4)  : {'Yes [OPTIMAL]' if t.cowan_bounded else 'No [HIGH COMPLEXITY]'}",
            "--------------------------------------------------------------------------------",
            " STRUCTURAL NODE CORRESPONDENCES",
            "--------------------------------------------------------------------------------",
        ]

        if not iso.node_mappings:
            lines.append(" (No structural node correspondences found)")
        else:
            for m in iso.node_mappings:
                lines.append(f" [MAP] '{m.source_label}' <====> '{m.target_label}'")
                lines.append(f"       Role Congruence: {m.role_congruence:.2f} | Degree Sim: {m.structural_degree_similarity:.2f}")

        lines.append("--------------------------------------------------------------------------------")
        lines.append(" PROJECTED CROSS-DOMAIN INFERENCES")
        lines.append("--------------------------------------------------------------------------------")
        for idx, inf in enumerate(projection.transferred_inferences, 1):
            lines.append(f" [{idx}] {inf}")

        lines.append("================================================================================")
        return "\n".join(lines)
