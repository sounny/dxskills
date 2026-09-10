#!/usr/bin/env python3
"""
Autonomous Cognitive Spatial Schema Morphing & Associative Bridge Weaver
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Translates complex abstract mental models across computational, mechanical, biological,
and spatial architectural paradigms. Generates isomorphic cross-domain metaphor bridges
to accelerate non-linear conceptual comprehension and eliminate phonological fatigue.

Core Principles:
- N-Connection Analogical Reasoning: Leverages cross-domain analogies to decode abstract architectures.
- M-Reasoning Physical Grounding: Ground non-physical systems into tactile mechanical and biological loops.
- Isomorphic Structural Mapping: Preserves relational dynamics and failure modes across domains.
- Zero Jargon Friction: Explains high-dimensional technical dynamics through intuitive physical metaphors.
"""

import os
import re
import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


VALID_DOMAINS = {"computational", "mechanical", "biological", "spatial"}

DOMAIN_METADATA = {
    "computational": {"label": "Computational System", "color": "5", "theme": "#38bdf8", "icon": "cpu"},
    "mechanical": {"label": "Mechanical Physical System", "color": "2", "theme": "#f59e0b", "icon": "cog"},
    "biological": {"label": "Biological Organism Loop", "color": "4", "theme": "#10b981", "icon": "activity"},
    "spatial": {"label": "Spatial Architectural Fabric", "color": "6", "theme": "#a855f7", "icon": "building"}
}


@dataclass
class DomainConcept:
    """An instantiated manifestation of a system dynamic within a specific domain."""
    name: str
    domain: str  # computational, mechanical, biological, spatial
    role: str    # buffer, governor, distributor, filter, failsafe, resonator
    description: str
    dynamics: str
    failure_mode: str


@dataclass
class IsomorphicBridge:
    """An analogical bridge connecting two disparate domains with relational parity."""
    bridge_id: str
    source_domain: str
    target_domain: str
    source_concept: str
    target_concept: str
    structural_isomorphism: str
    analogical_strength: float  # 0.0 to 1.0
    cognitive_takeaway: str


@dataclass
class MorphedSchema:
    """A cross-domain multi-perspective conceptual matrix."""
    schema_id: str
    title: str
    primary_role: str
    computational: DomainConcept
    mechanical: DomainConcept
    biological: DomainConcept
    spatial: DomainConcept
    bridges: List[IsomorphicBridge]
    cognitive_takeaway: str


class SpatialSchemaMorpher:
    """Weaves cross-domain analogies and generates multi-perspective spatial canvases."""

    def __init__(self):
        self.library: Dict[str, MorphedSchema] = {}
        self._next_id = 1
        self._load_standard_catalog()

    def _load_standard_catalog(self):
        """Populate baseline library of canonical architectural paradigms."""
        # 1. Backpressure and Flow Regulation
        self.register_schema(
            title="Reactive Backpressure and Flow Regulation",
            primary_role="governor",
            cognitive_takeaway="Upstream producers must throttle flow when downstream buffers saturate, preventing catastrophic rupture.",
            computational=DomainConcept(
                name="Reactive Stream Backpressure (RSocket / Reactive Streams)",
                domain="computational",
                role="governor",
                description="Downstream subscriber signals request(N) credit tokens to upstream publisher to prevent memory exhaustion.",
                dynamics="Signal-based flow credits bound heap allocation during burst traffic.",
                failure_mode="Out of Memory (OOM) heap panic or dropped TCP packet buffers under unmitigated load."
            ),
            mechanical=DomainConcept(
                name="Centrifugal Flyball Governor & Spring Pressure Relief Valve",
                domain="mechanical",
                role="governor",
                description="Rotating flyweights lift under excess rotational speed, throttling the steam intake valve.",
                dynamics="Centrifugal kinetic force mechanically chokes incoming energy when downstream resistance spikes.",
                failure_mode="Boiler rupture or flyweight fracture under uncontrolled runaway pressure."
            ),
            biological=DomainConcept(
                name="Enzymatic Allosteric Feedback Inhibition",
                domain="biological",
                role="governor",
                description="Abundant end-product molecules bind to the regulatory site of the initial pathway enzyme, halting production.",
                dynamics="Concentration gradient conformational shift down-regulates catalytic reaction rate.",
                failure_mode="Metabolic toxicity or substrate depletion leading to cellular necrosis."
            ),
            spatial=DomainConcept(
                name="Canal Lock Sluice & Spillway Retention Basin",
                domain="spatial",
                role="governor",
                description="Sequential stepped canal gates and bypass reservoirs absorbing surge headwaters.",
                dynamics="Gravity head hydrostatic redistribution across tiered weir channels.",
                failure_mode="Overtopping dam breach or flash flooding in downriver urban districts."
            )
        )

        # 2. Resilient Redundancy and Consensus
        self.register_schema(
            title="Quorum Consensus and Fault-Tolerant State Ledger",
            primary_role="failsafe",
            cognitive_takeaway="A distributed system maintains truth through majority agreement across independent witnesses.",
            computational=DomainConcept(
                name="Raft / Paxos Distributed Consensus Protocol",
                domain="computational",
                role="failsafe",
                description="Replicated write-ahead log requiring acknowledgement from (N/2 + 1) nodes before commit.",
                dynamics="Heartbeat leases and randomized election timeouts maintain consistent cluster state.",
                failure_mode="Split-brain partition or leader election liveloop under asymmetric network splits."
            ),
            mechanical=DomainConcept(
                name="Epicyclic Differential Gearbox with Limited Slip",
                domain="mechanical",
                role="failsafe",
                description="Planet gears distributing mechanical torque equally between axles while accommodating speed divergence.",
                dynamics="Mechanical gear tooth interlock prevents single wheel spinning from stalling vehicle momentum.",
                failure_mode="Axle shear or gear tooth stripping when differential lock fails under severe impact."
            ),
            biological=DomainConcept(
                name="Adaptive Immune Clonal Selection & Polyclonal B-Cell Verification",
                domain="biological",
                role="failsafe",
                description="Multiple independent T-helper cells and B-cells must cross-verify antigen presentation before releasing antibodies.",
                dynamics="Receptor affinity thresholding prevents catastrophic autoimmune self-destruction.",
                failure_mode="Autoimmune disorder or pathogen evasion when co-stimulatory checkpoints fail."
            ),
            spatial=DomainConcept(
                name="Flying Buttress and Ribbed Vault Distribution Arch",
                domain="spatial",
                role="failsafe",
                description="Interconnected diagonal masonry struts transferring lateral roof thrust outward to exterior buttress piers.",
                dynamics="Triangulated compressive stone vectors resolve outward ceiling gravity loads into bedrock.",
                failure_mode="Cathedral vault collapse if exterior abutments shift or mortar delaminates."
            )
        )

        # 3. Cache Decoupling and Working Memory Buffering
        self.register_schema(
            title="Temporal Caching and Working Memory Buffering",
            primary_role="buffer",
            cognitive_takeaway="High-frequency short-term access prevents repetitive high-latency roundtrips to deep cold storage.",
            computational=DomainConcept(
                name="Multi-Tier LRU L1/L2 Cache with Write-Through Invalidation",
                domain="computational",
                role="buffer",
                description="Ultra-fast local SRAM holding frequently dereferenced memory addresses ahead of cold DRAM and NVMe.",
                dynamics="Spatial and temporal locality heuristics deliver sub-nanosecond cache hits.",
                failure_mode="Cache thrashing, cold-start stampedes, or stale cache inconsistency."
            ),
            mechanical=DomainConcept(
                name="High-Inertia Heavy Cast-Iron Flywheel",
                domain="mechanical",
                role="buffer",
                description="Heavy rotating mass that stores kinetic energy during power strokes and delivers it smoothly between strokes.",
                dynamics="Rotational inertia smoothing out intermittent reciprocating engine torque spikes.",
                failure_mode="Rotational burst explosion if angular velocity exceeds tensile burst threshold."
            ),
            biological=DomainConcept(
                name="Hepatic Glycogen Reserves and Blood Glucose Homeostasis",
                domain="biological",
                role="buffer",
                description="Liver hepatocytes storing surplus blood glucose as glycogen polymers, releasing it during acute exertion.",
                dynamics="Glucagon and insulin hormonal toggles rapidly balance systemic energy availability.",
                failure_mode="Hypoglycemic shock or ketoacidosis during glycogen depletion."
            ),
            spatial=DomainConcept(
                name="Thermal Mass Adobe Trombe Wall and Shaded Courtyard",
                domain="spatial",
                role="buffer",
                description="Dense rammed-earth walls absorbing peak midday desert solar heat, releasing it into living quarters at night.",
                dynamics="Diurnal thermal damping phase-shifting heat flux by 8 to 12 hours.",
                failure_mode="Internal overheating during multi-day continuous heatwaves without night cooling."
            )
        )

    def register_schema(
        self,
        title: str,
        primary_role: str,
        cognitive_takeaway: str,
        computational: DomainConcept,
        mechanical: DomainConcept,
        biological: DomainConcept,
        spatial: DomainConcept,
        schema_id: Optional[str] = None
    ) -> MorphedSchema:
        """Register a 4-domain isomorphic schema."""
        sid = schema_id or f"schema-{self._next_id}"
        self._next_id += 1

        bridges = self._build_isomorphic_bridges(
            computational, mechanical, biological, spatial
        )

        schema = MorphedSchema(
            schema_id=sid,
            title=title.strip(),
            primary_role=primary_role.strip().lower(),
            computational=computational,
            mechanical=mechanical,
            biological=biological,
            spatial=spatial,
            bridges=bridges,
            cognitive_takeaway=cognitive_takeaway.strip()
        )
        self.library[sid] = schema
        return schema

    def _build_isomorphic_bridges(
        self,
        comp: DomainConcept,
        mech: DomainConcept,
        bio: DomainConcept,
        spat: DomainConcept
    ) -> List[IsomorphicBridge]:
        """Construct relational bridges pairing the computational concept to each physical domain."""
        bridges = []

        # Computational <-> Mechanical Bridge
        bridges.append(IsomorphicBridge(
            bridge_id="bridge-comp-mech",
            source_domain="computational",
            target_domain="mechanical",
            source_concept=comp.name,
            target_concept=mech.name,
            structural_isomorphism=(
                f"Both regulate system equilibrium through physical or programmatic resistance: "
                f"{comp.role.title()} dynamic matches mechanical kinetic regulation."
            ),
            analogical_strength=0.94,
            cognitive_takeaway=(
                f"Visualize {comp.name} not as code, but as a physical {mech.name}. "
                f"When buffers saturate, think of pressure valves lifting."
            )
        ))

        # Computational <-> Biological Bridge
        bridges.append(IsomorphicBridge(
            bridge_id="bridge-comp-bio",
            source_domain="computational",
            target_domain="biological",
            source_concept=comp.name,
            target_concept=bio.name,
            structural_isomorphism=(
                f"Both rely on organic feedback loops to preserve self-stabilizing homeostasis: "
                f"Token limits mimic biochemical concentration gradient signals."
            ),
            analogical_strength=0.91,
            cognitive_takeaway=(
                f"Think of {comp.name} as {bio.name}. "
                f"Self-regulation occurs through local cellular signals rather than central command."
            )
        ))

        # Computational <-> Spatial Bridge
        bridges.append(IsomorphicBridge(
            bridge_id="bridge-comp-spat",
            source_domain="computational",
            target_domain="spatial",
            source_concept=comp.name,
            target_concept=spat.name,
            structural_isomorphism=(
                f"Both absorb and dissipate physical or informational surge stress through spatial geometry: "
                f"Decoupled queues match spillway retention and masonry load transfer."
            ),
            analogical_strength=0.88,
            cognitive_takeaway=(
                f"Architectural structural containment: {spat.name} provides physical intuition "
                f"for how {comp.name} handles sudden shock loads."
            )
        ))

        return bridges

    def morph_concept(
        self,
        concept_name: str,
        role: str = "buffer",
        description: str = ""
    ) -> MorphedSchema:
        """
        Dynamically synthesize a 4-domain morphed schema for a user-specified concept.
        Matches against catalog heuristics or generates bespoke cross-domain analogies.
        """
        clean_role = role.strip().lower()
        if clean_role not in {"buffer", "governor", "failsafe", "distributor", "filter", "resonator"}:
            clean_role = "buffer"

        # Check existing schemas for title or concept name match
        for s in self.library.values():
            if concept_name.lower() in s.title.lower() or concept_name.lower() in s.computational.name.lower():
                return s

        # Synthesize dynamic bespoke schema
        sid = f"schema-{self._next_id}"
        self._next_id += 1

        comp_concept = DomainConcept(
            name=concept_name.strip(),
            domain="computational",
            role=clean_role,
            description=description.strip() or f"Computational architecture component performing {clean_role}.",
            dynamics=f"Orchestrates discrete logical events to maintain {clean_role} efficiency.",
            failure_mode=f"Throughput stalling, memory leak, or synchronization deadlock."
        )

        # Dynamic physical analogies based on role
        if clean_role == "governor":
            mech_name = "Flyweight Throttle & Spring Escapement"
            mech_dyn = "Restricting kinetic throughput proportionally to input velocity."
            bio_name = "Hormonal Glucagon-Insulin Pancreatic Circuit"
            bio_dyn = "Chemical feedback loop stabilizing systemic blood sugar levels."
            spat_name = "Tide Gates and Coastal Surge Breakwaters"
            spat_dyn = "Hydrodynamic deflection of incoming tidal energy surges."
        elif clean_role == "failsafe":
            mech_name = "Shear Pin & Counterweight Brake Assembly"
            mech_dyn = "Sacrificial physical disconnection preventing catastrophic motor burnout."
            bio_name = "Apoptosis (Programmed Cellular Self-Destruction)"
            bio_dyn = "Controlled cellular disassembly preventing malignant tumor proliferation."
            spat_name = "Firewall Compartmentalization & Egress Air-Locks"
            spat_dyn = "Physical airtight isolation of burning zones from escape corridors."
        else:  # buffer
            mech_name = "Hydraulic Accumulator & Torsion Spring Reservoir"
            mech_dyn = "Storing fluid volume under gas pressure to deliver instantaneous burst power."
            bio_name = "Capillary Venous Reservoir and Spleen Erythrocyte Buffer"
            bio_dyn = "Contractile pooling of blood cells released during sudden circulatory shock."
            spat_name = "Sunken Atrium & Diurnal Thermal Trombe Mass"
            spat_dyn = "Atmospheric and thermal shock damping via subterranean geometry."

        mech_concept = DomainConcept(
            name=mech_name,
            domain="mechanical",
            role=clean_role,
            description=f"Mechanical physical manifestation of a {clean_role}.",
            dynamics=mech_dyn,
            failure_mode="Metal fatigue or structural rupture under continuous cycle stress."
        )
        bio_concept = DomainConcept(
            name=bio_name,
            domain="biological",
            role=clean_role,
            description=f"Biological physiological manifestation of a {clean_role}.",
            dynamics=bio_dyn,
            failure_mode="Metabolic collapse when homeostatic reserve is exhausted."
        )
        spat_concept = DomainConcept(
            name=spat_name,
            domain="spatial",
            role=clean_role,
            description=f"Spatial architectural manifestation of a {clean_role}.",
            dynamics=spat_dyn,
            failure_mode="Material degradation or localized structural shear failure."
        )

        return self.register_schema(
            title=f"{concept_name} Cross-Domain Schema",
            primary_role=clean_role,
            cognitive_takeaway=f"Understand {concept_name} through the tangible dynamics of {mech_name} and {bio_name}.",
            computational=comp_concept,
            mechanical=mech_concept,
            biological=bio_concept,
            spatial=spat_concept,
            schema_id=sid
        )

    def export_canvas(self, schemas: List[MorphedSchema]) -> Dict[str, Any]:
        """
        Generate Obsidian .canvas file mapping cross-domain pillars in 2D space.
        Arranges Computational (top-left), Mechanical (top-right), Biological (bottom-left),
        and Spatial (bottom-right), linked with color-coded isomorphic bridge edges.
        """
        canvas_nodes = []
        canvas_edges = []
        edge_counter = 1

        base_x = 100
        base_y = 100

        for s_idx, schema in enumerate(schemas):
            # Center HUD card for schema title
            hud_id = f"node-hud-{schema.schema_id}"
            hud_text = (
                f"## {schema.title}\n"
                f"> **Primary Dynamic:** {schema.primary_role.upper()}\n\n"
                f"**Cognitive Takeaway:**\n{schema.cognitive_takeaway}\n\n"
                f"- **Computational:** {schema.computational.name}\n"
                f"- **Mechanical:** {schema.mechanical.name}\n"
                f"- **Biological:** {schema.biological.name}\n"
                f"- **Spatial:** {schema.spatial.name}"
            )
            canvas_nodes.append({
                "id": hud_id,
                "type": "text",
                "text": hud_text,
                "x": base_x + 320,
                "y": base_y + 180,
                "width": 380,
                "height": 220,
                "color": "1"  # Center anchor
            })

            # Domain Pillar Positions: (x_offset, y_offset, DomainConcept, color)
            pillars = [
                ("comp", 0, 0, schema.computational, DOMAIN_METADATA["computational"]["color"]),
                ("mech", 760, 0, schema.mechanical, DOMAIN_METADATA["mechanical"]["color"]),
                ("bio", 0, 440, schema.biological, DOMAIN_METADATA["biological"]["color"]),
                ("spat", 760, 440, schema.spatial, DOMAIN_METADATA["spatial"]["color"]),
            ]

            node_ids = {}
            for tag, px, py, concept, col in pillars:
                nid = f"node-{schema.schema_id}-{tag}"
                node_ids[tag] = nid
                card_text = (
                    f"### [{DOMAIN_METADATA[concept.domain]['label']}]\n"
                    f"#### {concept.name}\n\n"
                    f"{concept.description}\n\n"
                    f"- **Physical Dynamics:** {concept.dynamics}\n"
                    f"- **Failure Mode:** {concept.failure_mode}"
                )
                canvas_nodes.append({
                    "id": nid,
                    "type": "text",
                    "text": card_text,
                    "x": base_x + px,
                    "y": base_y + py,
                    "width": 300,
                    "height": 200,
                    "color": col
                })

                # Connect each pillar to center HUD
                canvas_edges.append({
                    "id": f"edge-hud-{edge_counter}",
                    "fromNode": nid,
                    "toNode": hud_id,
                    "toEnd": "arrow",
                    "label": "Homeostasis",
                    "color": col
                })
                edge_counter += 1

            # Connect Computational to the other three via Isomorphic Bridges
            for bridge in schema.bridges:
                tgt_tag = "mech" if bridge.target_domain == "mechanical" else (
                    "bio" if bridge.target_domain == "biological" else "spat"
                )
                canvas_edges.append({
                    "id": f"edge-bridge-{edge_counter}",
                    "fromNode": node_ids["comp"],
                    "toNode": node_ids[tgt_tag],
                    "toEnd": "arrow",
                    "label": f"Isomorphism ({int(bridge.analogical_strength * 100)}%)",
                    "color": "5"
                })
                edge_counter += 1

            base_y += 720

        return {
            "nodes": canvas_nodes,
            "edges": canvas_edges
        }

    def export_svg_morph(self, schema: MorphedSchema, width: int = 760, height: int = 540) -> str:
        """
        Generate vector SVG visualizing 4-domain isomorphic cross-connections,
        metaphor bridge trajectories, and dynamic failure modes.
        """
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0f172a; '
            f'font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">',
            '<defs>',
            '  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur" />',
            '    <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>',
            '  </filter>',
            '  <linearGradient id="compGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#38bdf8"/>',
            '    <stop offset="100%" stop-color="#0284c7"/>',
            '  </linearGradient>',
            '  <linearGradient id="mechGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#f59e0b"/>',
            '    <stop offset="100%" stop-color="#d97706"/>',
            '  </linearGradient>',
            '  <linearGradient id="bioGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#10b981"/>',
            '    <stop offset="100%" stop-color="#059669"/>',
            '  </linearGradient>',
            '  <linearGradient id="spatGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#a855f7"/>',
            '    <stop offset="100%" stop-color="#7e22ce"/>',
            '  </linearGradient>',
            '</defs>',
            '<!-- Title Header -->',
            f'<text x="28" y="34" fill="#f8fafc" font-size="16" font-weight="700">{schema.title}</text>',
            f'<text x="28" y="52" fill="#94a3b8" font-size="11.5">{schema.cognitive_takeaway[:85]}...</text>',
            '<!-- Central Hub Diamond -->',
        ]

        cx = width / 2.0
        cy = height / 2.0 + 16.0

        # Draw cross connecting curved bridges
        # Coordinates for 4 quadrant cards
        card_w = 230
        card_h = 135
        p_comp = (32, 75)
        p_mech = (width - card_w - 32, 75)
        p_bio = (32, height - card_h - 25)
        p_spat = (width - card_w - 32, height - card_h - 25)

        centers = [
            (p_comp[0] + card_w, p_comp[1] + card_h / 2.0),
            (p_mech[0], p_mech[1] + card_h / 2.0),
            (p_bio[0] + card_w, p_bio[1] + card_h / 2.0),
            (p_spat[0], p_spat[1] + card_h / 2.0)
        ]

        # Draw connecting arcs between cards through center
        svg_parts.append(
            f'<path d="M {centers[0][0]} {centers[0][1]} Q {cx} {cy} {centers[1][0]} {centers[1][1]}" '
            f'fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4,4" opacity="0.8"/>'
        )
        svg_parts.append(
            f'<path d="M {centers[0][0]} {centers[0][1]} Q {cx} {cy} {centers[2][0]} {centers[2][1]}" '
            f'fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4,4" opacity="0.8"/>'
        )
        svg_parts.append(
            f'<path d="M {centers[0][0]} {centers[0][1]} Q {cx} {cy} {centers[3][0]} {centers[3][1]}" '
            f'fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4,4" opacity="0.8"/>'
        )

        # Draw Central Core Badge
        svg_parts.append(
            f'<polygon points="{cx},{cy - 44} {cx + 60},{cy} {cx},{cy + 44} {cx - 60},{cy}" '
            f'fill="#1e293b" stroke="#38bdf8" stroke-width="2" filter="url(#glow)"/>'
        )
        svg_parts.append(
            f'<text x="{cx}" y="{cy - 8}" fill="#38bdf8" font-size="10.5" font-weight="800" text-anchor="middle">ISOMORPHISM</text>'
        )
        svg_parts.append(
            f'<text x="{cx}" y="{cy + 10}" fill="#f8fafc" font-size="12" font-weight="700" text-anchor="middle">{schema.primary_role.upper()}</text>'
        )
        svg_parts.append(
            f'<text x="{cx}" y="{cy + 24}" fill="#94a3b8" font-size="9" text-anchor="middle">Structural Parity</text>'
        )

        # Draw 4 Domain Pillar Cards
        domain_cards = [
            (p_comp, schema.computational, "#38bdf8", "url(#compGrad)", "COMPUTATIONAL"),
            (p_mech, schema.mechanical, "#f59e0b", "url(#mechGrad)", "MECHANICAL"),
            (p_bio, schema.biological, "#10b981", "url(#bioGrad)", "BIOLOGICAL"),
            (p_spat, schema.spatial, "#a855f7", "url(#spatGrad)", "SPATIAL")
        ]

        for (bx, by), concept, stroke_c, header_grad, dom_tag in domain_cards:
            svg_parts.append(f'<g transform="translate({bx}, {by})">')
            svg_parts.append(
                f'  <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="8" fill="#1e293b" stroke="{stroke_c}" stroke-width="1.5"/>'
            )
            svg_parts.append(
                f'  <rect x="0" y="0" width="{card_w}" height="24" rx="8" fill="{header_grad}" fill-opacity="0.25"/>'
            )
            svg_parts.append(
                f'  <text x="12" y="16" fill="{stroke_c}" font-size="10.5" font-weight="700">{dom_tag}</text>'
            )
            svg_parts.append(
                f'  <text x="12" y="42" fill="#f8fafc" font-size="11.5" font-weight="600">{concept.name[:27]}</text>'
            )
            svg_parts.append(
                f'  <text x="12" y="62" fill="#94a3b8" font-size="9.5">Dynamics: {concept.dynamics[:36]}...</text>'
            )
            svg_parts.append(
                f'  <text x="12" y="80" fill="#94a3b8" font-size="9.5">Failure: {concept.failure_mode[:36]}...</text>'
            )

            # Mini strength pill
            svg_parts.append(
                f'  <rect x="12" y="{card_h - 26}" width="{card_w - 24}" height="16" rx="4" fill="#0f172a"/>'
            )
            svg_parts.append(
                f'  <text x="18" y="{card_h - 14}" fill="{stroke_c}" font-size="9" font-weight="600">Cognitive Anchor Match: 90%+</text>'
            )
            svg_parts.append('</g>')

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def export_summary_markdown(self, schemas: List[MorphedSchema]) -> str:
        """Generate an executive markdown report mapping cross-domain physical schemas."""
        lines = [
            "# Cross-Domain Schema Morphing & Associative Bridge Weaver Report",
            "",
            "## Executive Overview",
            "This cognitive synthesis maps abstract computational architectures into tangible",
            "mechanical, biological, and spatial structural systems to offload working memory",
            "and build deep physical intuition.",
            ""
        ]

        for s in schemas:
            lines.append(f"## {s.title} (`{s.schema_id}`)")
            lines.append(f"> **Core Directive:** {s.cognitive_takeaway}")
            lines.append("")
            lines.append("| Domain | Manifestation | Dynamic Equilibrium | Failure Mode |")
            lines.append("| :--- | :--- | :--- | :--- |")
            lines.append(f"| **Computational** | `{s.computational.name}` | {s.computational.dynamics} | {s.computational.failure_mode} |")
            lines.append(f"| **Mechanical** | `{s.mechanical.name}` | {s.mechanical.dynamics} | {s.mechanical.failure_mode} |")
            lines.append(f"| **Biological** | `{s.biological.name}` | {s.biological.dynamics} | {s.biological.failure_mode} |")
            lines.append(f"| **Spatial** | `{s.spatial.name}` | {s.spatial.dynamics} | {s.spatial.failure_mode} |")
            lines.append("")

            lines.append("### Associative Metaphor Bridges")
            for b in s.bridges:
                pct = int(b.analogical_strength * 100)
                lines.append(f"- **{b.source_domain.title()} -> {b.target_domain.title()} (Match: `{pct}%`):** {b.cognitive_takeaway}")
            lines.append("")

        return "\n".join(lines)


def create_sample_schema_morpher() -> Tuple[SpatialSchemaMorpher, List[MorphedSchema]]:
    """Create sample schema morpher loaded with the 3 canonical schemas."""
    morpher = SpatialSchemaMorpher()
    schemas = list(morpher.library.values())
    return morpher, schemas


if __name__ == "__main__":
    morpher, schemas = create_sample_schema_morpher()
    print(morpher.export_summary_markdown(schemas))
