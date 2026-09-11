"""Autonomous Cognitive Spatial Associative Resonance & Concept Lattice Compiler.

Theoretical Foundation:
- Eide & Eide M-I-N-D Framework (Interconnected Reasoning / I-Strength):
  Dyslexic cognition excels at detecting non-obvious relationships, structural
  isomorphisms, and cross-domain metaphors between disparate disciplines. However,
  without explicit spatial externalization, multi-branch associative leaps can
  saturate working memory.
- Formal Concept Analysis (FCA) & Galois Connections (Wille & Ganter):
  Maps objects and attributes into a formal context (G, M, I). Galois derivation
  operators compute closed concept pairs (Extent, Intent) forming a complete
  mathematical lattice ordered by subconcept-superconcept specialization.
- Associative Resonance Index (R_assoc):
  Quantifies the cognitive synergy between distant concept nodes based on latent
  attribute overlap, domain divergence, and structural bridge novelty, identifying
  breakthrough intuitive leaps across spatial clusters.
- Spatial Canvas & Vector Compilation:
  Compiles Galois lattices directly into Obsidian .canvas files and publication-grade
  vector SVG diagrams with dark titanium aesthetic and explicit resonance pathways.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class LeapCategory(str, enum.Enum):
    """Categorization of associative cognitive leaps across concept clusters."""

    CROSS_DOMAIN_ISOMORPHISM = "cross_domain_isomorphism"
    ANALOGICAL_BRIDGE = "analogical_bridge"
    EMERGENT_INTEGRATION = "emergent_integration"
    METAPHORIC_SYNTHESIS = "metaphoric_synthesis"


@dataclass
class FormalConcept:
    """A formal concept defined by closed extent (objects) and intent (attributes)."""

    concept_id: str
    extent: List[str]
    intent: List[str]
    support: float
    depth: int = 0
    layer_index: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Return serializable dictionary representation."""
        return {
            "concept_id": self.concept_id,
            "extent": sorted(self.extent),
            "intent": sorted(self.intent),
            "support": round(self.support, 3),
            "depth": self.depth,
            "layer_index": self.layer_index,
        }


@dataclass
class LatticeEdge:
    """Directed Hasse edge representing a direct subconcept-superconcept cover relation."""

    child_id: str
    parent_id: str
    attribute_delta: List[str] = field(default_factory=list)
    object_delta: List[str] = field(default_factory=list)


@dataclass
class AssociativeLeap:
    """An intuitive conceptual leap bridging distant non-hierarchical concepts."""

    source_id: str
    target_id: str
    source_extent: List[str]
    target_extent: List[str]
    shared_intent: List[str]
    resonance_score: float
    category: LeapCategory
    bridge_metaphor: str
    hueristic_novelty: float

    def to_dict(self) -> Dict[str, Any]:
        """Return serializable dictionary representation."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "source_extent": sorted(self.source_extent),
            "target_extent": sorted(self.target_extent),
            "shared_intent": sorted(self.shared_intent),
            "resonance_score": round(self.resonance_score, 3),
            "category": self.category.value,
            "bridge_metaphor": self.bridge_metaphor,
            "hueristic_novelty": round(self.hueristic_novelty, 3),
        }


@dataclass
class LatticeTelemetry:
    """Telemetry metrics capturing Galois lattice structure and associative resonance."""

    total_objects: int
    total_attributes: int
    total_concepts: int
    total_hasse_edges: int
    max_lattice_depth: int
    associative_leaps_count: int
    top_resonance_score: float
    galois_connectivity_index: float
    concepts: List[FormalConcept] = field(default_factory=list)
    leaps: List[AssociativeLeap] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_objects": self.total_objects,
            "total_attributes": self.total_attributes,
            "total_concepts": self.total_concepts,
            "total_hasse_edges": self.total_hasse_edges,
            "max_lattice_depth": self.max_lattice_depth,
            "associative_leaps_count": self.associative_leaps_count,
            "top_resonance_score": round(self.top_resonance_score, 3),
            "galois_connectivity_index": round(self.galois_connectivity_index, 3),
            "concepts": [c.to_dict() for c in self.concepts],
            "leaps": [l.to_dict() for l in self.leaps],
        }


class ConceptLatticeCompiler:
    """Compiler executing Formal Concept Analysis and associative resonance indexing."""

    def __init__(
        self,
        min_resonance: float = 0.35,
        max_overlap_for_leap: float = 0.5,
    ) -> None:
        self.min_resonance = min_resonance
        self.max_overlap_for_leap = max_overlap_for_leap
        self.context: Dict[str, Set[str]] = {}
        self.all_objects: List[str] = []
        self.all_attributes: List[str] = []

    def load_context(self, context_data: Dict[str, List[str]]) -> None:
        """Load formal context from object-to-attributes mapping."""
        self.context = {obj: set(attrs) for obj, attrs in context_data.items()}
        self.all_objects = sorted(list(self.context.keys()))
        attrs_set: Set[str] = set()
        for a_set in self.context.values():
            attrs_set.update(a_set)
        self.all_attributes = sorted(list(attrs_set))

    def load_from_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract objects and attributes from an Obsidian .canvas structure."""
        nodes = canvas_data.get("nodes", [])
        context_data: Dict[str, List[str]] = {}

        for node in nodes:
            node_id = str(node.get("id", ""))
            text = str(node.get("text", ""))
            title = node_id
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            if lines and not lines[0].startswith("#"):
                title = lines[0]
            elif lines and lines[0].startswith("#"):
                title = lines[0].lstrip("#").strip()

            tags = re.findall(r"#([a-zA-Z0-9_\-]+)", text)
            words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
            stop_words = {
                "this", "that", "with", "from", "have", "were", "node",
                "card", "text", "canvas", "file", "title", "then", "into"
            }
            meaningful_words = [w for w in words if w not in stop_words]
            combined_attrs = list(set(tags + meaningful_words[:8]))
            if not combined_attrs:
                combined_attrs = ["general_concept"]
            context_data[title] = combined_attrs

        self.load_context(context_data)

    def _prime_objects(self, obj_subset: Set[str]) -> Set[str]:
        """Galois derivation operator: Intent of an object subset (A')."""
        if not obj_subset:
            return set(self.all_attributes)
        common_attrs: Optional[Set[str]] = None
        for obj in obj_subset:
            attrs = self.context.get(obj, set())
            if common_attrs is None:
                common_attrs = set(attrs)
            else:
                common_attrs = common_attrs.intersection(attrs)
        return common_attrs if common_attrs is not None else set()

    def _prime_attributes(self, attr_subset: Set[str]) -> Set[str]:
        """Galois derivation operator: Extent of an attribute subset (B')."""
        if not attr_subset:
            return set(self.all_objects)
        matching_objects: Set[str] = set()
        for obj, attrs in self.context.items():
            if attr_subset.issubset(attrs):
                matching_objects.add(obj)
        return matching_objects

    def compute_lattice(self) -> Tuple[List[FormalConcept], List[LatticeEdge], List[AssociativeLeap], LatticeTelemetry]:
        """Compute complete formal concept lattice, Hasse diagram, and associative leaps."""
        if not self.context:
            empty_telemetry = LatticeTelemetry(
                total_objects=0,
                total_attributes=0,
                total_concepts=0,
                total_hasse_edges=0,
                max_lattice_depth=0,
                associative_leaps_count=0,
                top_resonance_score=0.0,
                galois_connectivity_index=0.0,
            )
            return [], [], [], empty_telemetry

        # 1. Compute all closed concept extents using intersection closure
        extents_set: Set[frozenset[str]] = {frozenset(self.all_objects)}
        for obj in self.all_objects:
            obj_intent = self._prime_objects({obj})
            obj_closure = self._prime_attributes(obj_intent)
            extents_set.add(frozenset(obj_closure))

        extent_list = list(extents_set)
        expanded = True
        while expanded:
            expanded = False
            new_extents = []
            for i in range(len(extent_list)):
                for j in range(i + 1, len(extent_list)):
                    intersection = extent_list[i].intersection(extent_list[j])
                    if intersection not in extents_set and intersection not in new_extents:
                        new_extents.append(intersection)
                        expanded = True
            if new_extents:
                extents_set.update(new_extents)
                extent_list.extend(new_extents)

        # 2. Build formal concepts
        raw_concepts: List[Tuple[Set[str], Set[str]]] = []
        for ext in extents_set:
            intent = self._prime_objects(set(ext))
            raw_concepts.append((set(ext), intent))

        # Sort concepts by extent size descending, then intent size ascending
        raw_concepts.sort(key=lambda item: (len(item[0]), -len(item[1])), reverse=True)

        formal_concepts: List[FormalConcept] = []
        total_obj_count = max(1, len(self.all_objects))
        for idx, (ext, intent) in enumerate(raw_concepts):
            c_id = f"c_{idx}"
            support = len(ext) / total_obj_count
            formal_concepts.append(
                FormalConcept(
                    concept_id=c_id,
                    extent=sorted(list(ext)),
                    intent=sorted(list(intent)),
                    support=support,
                )
            )

        # 3. Transitive reduction to compute direct Hasse cover edges
        hasse_edges: List[LatticeEdge] = []
        for i, c_sub in enumerate(formal_concepts):
            ext_sub = set(c_sub.extent)
            for j, c_sup in enumerate(formal_concepts):
                if i == j:
                    continue
                ext_sup = set(c_sup.extent)
                # In concept lattice: subconcept has smaller extent and larger intent
                if ext_sub < ext_sup:
                    # Check for intermediate concept
                    is_direct = True
                    for k, c_mid in enumerate(formal_concepts):
                        if k == i or k == j:
                            continue
                        ext_mid = set(c_mid.extent)
                        if ext_sub < ext_mid and ext_mid < ext_sup:
                            is_direct = False
                            break
                    if is_direct:
                        attr_delta = sorted(list(set(c_sub.intent) - set(c_sup.intent)))
                        obj_delta = sorted(list(ext_sup - ext_sub))
                        hasse_edges.append(
                            LatticeEdge(
                                child_id=c_sub.concept_id,
                                parent_id=c_sup.concept_id,
                                attribute_delta=attr_delta,
                                object_delta=obj_delta,
                            )
                        )

        # 4. Compute topological depth and layer indices for visualization
        self._assign_lattice_layers(formal_concepts, hasse_edges)

        # 5. Compute Associative Resonance and detect intuitive leaps
        associative_leaps = self._detect_associative_leaps(formal_concepts, hasse_edges)

        max_depth = max([c.depth for c in formal_concepts]) if formal_concepts else 0
        top_resonance = max([l.resonance_score for l in associative_leaps]) if associative_leaps else 0.0

        edge_ratio = len(hasse_edges) / max(1, len(formal_concepts))
        galois_connectivity = min(1.0, edge_ratio / 2.5)

        telemetry = LatticeTelemetry(
            total_objects=len(self.all_objects),
            total_attributes=len(self.all_attributes),
            total_concepts=len(formal_concepts),
            total_hasse_edges=len(hasse_edges),
            max_lattice_depth=max_depth,
            associative_leaps_count=len(associative_leaps),
            top_resonance_score=top_resonance,
            galois_connectivity_index=galois_connectivity,
            concepts=formal_concepts,
            leaps=associative_leaps,
        )

        return formal_concepts, hasse_edges, associative_leaps, telemetry

    def _assign_lattice_layers(
        self,
        concepts: List[FormalConcept],
        edges: List[LatticeEdge],
    ) -> None:
        """Assign topological depth layers to concepts from top to bottom."""
        # Top concept has full extent (or maximal extent)
        concept_map = {c.concept_id: c for c in concepts}
        # Find parents of each node
        parents_map: Dict[str, List[str]] = {c.concept_id: [] for c in concepts}
        children_map: Dict[str, List[str]] = {c.concept_id: [] for c in concepts}
        for e in edges:
            parents_map[e.child_id].append(e.parent_id)
            children_map[e.parent_id].append(e.child_id)

        # Root nodes have no parents
        roots = [c.concept_id for c in concepts if not parents_map[c.concept_id]]
        for r_id in roots:
            concept_map[r_id].depth = 0

        queue = list(roots)
        visited: Set[str] = set(roots)
        while queue:
            curr = queue.pop(0)
            curr_depth = concept_map[curr].depth
            for child_id in children_map[curr]:
                child = concept_map[child_id]
                child.depth = max(child.depth, curr_depth + 1)
                if child_id not in visited:
                    visited.add(child_id)
                    queue.append(child_id)

        # Assign layer_index (horizontal ordering within layer)
        layer_buckets: Dict[int, List[FormalConcept]] = {}
        for c in concepts:
            layer_buckets.setdefault(c.depth, []).append(c)

        for depth, bucket in layer_buckets.items():
            for idx, c in enumerate(bucket):
                c.layer_index = idx

    def _detect_associative_leaps(
        self,
        concepts: List[FormalConcept],
        edges: List[LatticeEdge],
    ) -> List[AssociativeLeap]:
        """Identify non-hierarchical conceptual leaps with high associative resonance."""
        leaps: List[AssociativeLeap] = []
        direct_pairs: Set[Tuple[str, str]] = set()
        for e in edges:
            direct_pairs.add((e.child_id, e.parent_id))
            direct_pairs.add((e.parent_id, e.child_id))

        # Evaluate all concept pairs
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                c1 = concepts[i]
                c2 = concepts[j]

                # Skip direct Hasse cover relationships
                if (c1.concept_id, c2.concept_id) in direct_pairs:
                    continue

                ext1 = set(c1.extent)
                ext2 = set(c2.extent)
                int1 = set(c1.intent)
                int2 = set(c2.intent)

                # Skip empty concepts or universal covers
                if not ext1 or not ext2 or not int1 or not int2:
                    continue

                # Skip subset relations (ancestors/descendants)
                if ext1.issubset(ext2) or ext2.issubset(ext1):
                    continue

                shared_intent = int1.intersection(int2)
                if not shared_intent:
                    continue

                # Jaccard extent overlap (how distinct the object domains are)
                union_ext = ext1.union(ext2)
                inter_ext = ext1.intersection(ext2)
                overlap_ratio = len(inter_ext) / max(1, len(union_ext))

                # If extents are too identical, it is an incremental refinement rather than a leap
                if overlap_ratio > self.max_overlap_for_leap:
                    continue

                # Intent synergy: ratio of shared attributes relative to smaller intent
                synergy = len(shared_intent) / min(len(int1), len(int2))

                # Extent divergence factor: reward bridging across distinct object clusters
                divergence = 1.0 - overlap_ratio

                # Depth parity: leaps between similar abstractions vs cross-scale
                depth_factor = 1.0 / (1.0 + abs(c1.depth - c2.depth) * 0.25)

                # Novelty weight
                novelty = round(divergence * 0.6 + depth_factor * 0.4, 3)

                resonance = (synergy * 0.45) + (divergence * 0.35) + (min(1.0, len(shared_intent) / 3.0) * 0.20)
                resonance = min(1.0, max(0.0, resonance))

                if resonance >= self.min_resonance:
                    # Determine leap category
                    if divergence >= 0.9 and synergy >= 0.5:
                        cat = LeapCategory.CROSS_DOMAIN_ISOMORPHISM
                    elif synergy >= 0.4 and len(shared_intent) >= 2:
                        cat = LeapCategory.ANALOGICAL_BRIDGE
                    elif len(union_ext) >= 4 and synergy >= 0.3:
                        cat = LeapCategory.EMERGENT_INTEGRATION
                    else:
                        cat = LeapCategory.METAPHORIC_SYNTHESIS

                    metaphor = f"Shared invariants: ({', '.join(sorted(list(shared_intent)))})"

                    leaps.append(
                        AssociativeLeap(
                            source_id=c1.concept_id,
                            target_id=c2.concept_id,
                            source_extent=c1.extent,
                            target_extent=c2.extent,
                            shared_intent=sorted(list(shared_intent)),
                            resonance_score=resonance,
                            category=cat,
                            bridge_metaphor=metaphor,
                            hueristic_novelty=novelty,
                        )
                    )

        # Sort leaps by resonance score descending
        leaps.sort(key=lambda l: l.resonance_score, reverse=True)
        return leaps

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Concept Lattice",
    ) -> Dict[str, Any]:
        """Export concept lattice and associative leaps to Obsidian .canvas format."""
        concepts, edges, leaps, _ = self.compute_lattice()

        nodes: List[Dict[str, Any]] = []
        canvas_edges: List[Dict[str, Any]] = []

        # Layer spacing parameters
        x_spacing = 380
        y_spacing = 280
        base_x = 100
        base_y = 100

        # Group by depth for positioning
        depth_map: Dict[int, List[FormalConcept]] = {}
        for c in concepts:
            depth_map.setdefault(c.depth, []).append(c)

        max_nodes_in_layer = max([len(bucket) for bucket in depth_map.values()]) if depth_map else 1
        total_width = max_nodes_in_layer * x_spacing

        node_coords: Dict[str, Tuple[int, int]] = {}

        for depth, bucket in depth_map.items():
            layer_width = len(bucket) * x_spacing
            start_x = base_x + (total_width - layer_width) // 2
            y = base_y + depth * y_spacing

            for idx, c in enumerate(bucket):
                x = start_x + idx * x_spacing
                node_coords[c.concept_id] = (x, y)

                ext_str = ", ".join(c.extent) if c.extent else "(empty)"
                if len(ext_str) > 60:
                    ext_str = ext_str[:57] + "..."
                int_str = ", ".join(c.intent) if c.intent else "(universal)"
                if len(int_str) > 60:
                    int_str = int_str[:57] + "..."

                # Visual styling: color 6 (purple) for root, color 4 (green) for leaves, 2 (orange) for internal
                if c.depth == 0:
                    color = "6"
                elif not c.extent:
                    color = "1"
                elif c.support >= 0.5:
                    color = "4"
                else:
                    color = "2"

                content = (
                    f"### Concept {c.concept_id.upper()}\n"
                    f"**Support:** {c.support:.0%}\n\n"
                    f"**Extent (Objects):**\n`{ext_str}`\n\n"
                    f"**Intent (Attributes):**\n`{int_str}`"
                )

                nodes.append({
                    "id": c.concept_id,
                    "x": x,
                    "y": y,
                    "width": 320,
                    "height": 220,
                    "type": "text",
                    "text": content,
                    "color": color,
                })

        # Hasse cover edges (solid arrows)
        edge_idx = 1
        for e in edges:
            delta_label = f"+{', '.join(e.attribute_delta[:2])}" if e.attribute_delta else ""
            canvas_edges.append({
                "id": f"edge_hasse_{edge_idx}",
                "fromNode": e.parent_id,
                "fromSide": "bottom",
                "toNode": e.child_id,
                "toSide": "top",
                "label": delta_label,
            })
            edge_idx += 1

        # Associative leap bridge edges (highlighted)
        leap_idx = 1
        for l in leaps[:10]:
            canvas_edges.append({
                "id": f"edge_leap_{leap_idx}",
                "fromNode": l.source_id,
                "fromSide": "right",
                "toNode": l.target_id,
                "toSide": "left",
                "label": f"Leap: {l.resonance_score:.2f} ({l.category.value})",
                "color": "5",
            })
            leap_idx += 1

        canvas_json = {
            "title": canvas_title,
            "nodes": nodes,
            "edges": canvas_edges,
        }

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(canvas_json, f, indent=2)

        return canvas_json

    def to_svg(
        self,
        output_path: Optional[str] = None,
        width: int = 1200,
        height: int = 850,
    ) -> str:
        """Render publication-grade SVG concept lattice with dark titanium aesthetic."""
        concepts, edges, leaps, telemetry = self.compute_lattice()

        # Canvas boundaries
        padding = 80
        depth_map: Dict[int, List[FormalConcept]] = {}
        for c in concepts:
            depth_map.setdefault(c.depth, []).append(c)

        max_depth = max(depth_map.keys()) if depth_map else 0
        v_spacing = (height - 2 * padding) / max(1, max_depth) if max_depth > 0 else 100

        pos: Dict[str, Tuple[float, float]] = {}
        for depth, bucket in depth_map.items():
            y = padding + depth * v_spacing
            h_spacing = (width - 2 * padding) / max(1, len(bucket) + 1)
            for idx, c in enumerate(bucket):
                x = padding + (idx + 1) * h_spacing
                pos[c.concept_id] = (x, y)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">',
            '    <stop offset="0%" stop-color="#1E293B" stop-opacity="0.9"/>',
            '    <stop offset="100%" stop-color="#0F172A" stop-opacity="0.9"/>',
            '  </linearGradient>',
            '  <linearGradient id="leapGrad" x1="0" y1="0" x2="1" y2="1">',
            '    <stop offset="0%" stop-color="#EC4899"/>',
            '    <stop offset="100%" stop-color="#8B5CF6"/>',
            '  </linearGradient>',
            '  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748B"/>',
            '  </marker>',
            '  <marker id="leapArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#EC4899"/>',
            '  </marker>',
            '  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur stdDeviation="3" result="blur"/>',
            '    <feComposite in="SourceGraphic" in2="blur" operator="over"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="{padding}" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Formal Concept Lattice &amp; Associative Resonance</text>',
            f'<text x="{padding}" y="65" font-size="12" fill="#94A3B8">Galois Connections: {telemetry.total_concepts} Concepts | {telemetry.total_hasse_edges} Covers | {telemetry.associative_leaps_count} Associative Leaps</text>',
            '<!-- Hasse Edges -->',
        ]

        # Draw Hasse edges
        for e in edges:
            if e.parent_id in pos and e.child_id in pos:
                x1, y1 = pos[e.parent_id]
                x2, y2 = pos[e.child_id]
                svg_parts.append(
                    f'<line x1="{x1:.1f}" y1="{y1 + 25:.1f}" x2="{x2:.1f}" y2="{y2 - 25:.1f}" '
                    f'stroke="#334155" stroke-width="2" marker-end="url(#arrow)"/>'
                )

        # Draw Associative Leap Bridges (curved magenta paths)
        svg_parts.append('<!-- Associative Leaps -->')
        for l in leaps[:8]:
            if l.source_id in pos and l.target_id in pos:
                x1, y1 = pos[l.source_id]
                x2, y2 = pos[l.target_id]
                mx = (x1 + x2) / 2.0
                my = (y1 + y2) / 2.0 - 50.0
                svg_parts.append(
                    f'<path d="M {x1:.1f} {y1:.1f} Q {mx:.1f} {my:.1f} {x2:.1f} {y2:.1f}" '
                    f'fill="none" stroke="url(#leapGrad)" stroke-width="2.5" stroke-dasharray="6,4" '
                    f'filter="url(#glow)" marker-end="url(#leapArrow)"/>'
                )
                svg_parts.append(
                    f'<rect x="{mx - 45:.1f}" y="{my - 12:.1f}" width="90" height="20" rx="4" fill="#1E1B4B" stroke="#818CF8" stroke-width="1"/>'
                )
                svg_parts.append(
                    f'<text x="{mx:.1f}" y="{my + 2:.1f}" font-size="10" font-weight="600" fill="#E0E7FF" text-anchor="middle">Leap {l.resonance_score:.2f}</text>'
                )

        # Draw Concept Nodes
        svg_parts.append('<!-- Concept Cards -->')
        card_w = 170
        card_h = 75
        for c in concepts:
            if c.concept_id in pos:
                cx, cy = pos[c.concept_id]
                rx = cx - card_w / 2
                ry = cy - card_h / 2

                stroke_col = "#38BDF8" if c.depth == 0 else "#6366F1" if c.support > 0.4 else "#334155"

                ext_text = ", ".join(c.extent[:2]) + ("..." if len(c.extent) > 2 else "") if c.extent else "(empty)"
                int_text = ", ".join(c.intent[:2]) + ("..." if len(c.intent) > 2 else "") if c.intent else "(all)"

                svg_parts.append(
                    f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{card_w}" height="{card_h}" rx="8" '
                    f'fill="url(#cardGrad)" stroke="{stroke_col}" stroke-width="1.5"/>'
                )
                svg_parts.append(
                    f'<text x="{rx + 10:.1f}" y="{ry + 20:.1f}" font-size="12" font-weight="700" fill="#F1F5F9">{c.concept_id.upper()} ({c.support:.0%})</text>'
                )
                svg_parts.append(
                    f'<text x="{rx + 10:.1f}" y="{ry + 40:.1f}" font-size="10" fill="#94A3B8">Ext: <tspan fill="#38BDF8">{ext_text}</tspan></text>'
                )
                svg_parts.append(
                    f'<text x="{rx + 10:.1f}" y="{ry + 58:.1f}" font-size="10" fill="#94A3B8">Int: <tspan fill="#A78BFA">{int_text}</tspan></text>'
                )

        # Legend / Telemetry Box
        legend_x = width - 260
        legend_y = height - 140
        svg_parts.append('<!-- Telemetry Legend -->')
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="230" height="110" rx="6" '
            f'fill="#0F172A" stroke="#1E293B" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">M-I-N-D Lattice Metrics</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Max Depth: <tspan fill="#F8FAFC">{telemetry.max_lattice_depth}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Top Resonance: <tspan fill="#EC4899">{telemetry.top_resonance_score:.3f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Galois Connectivity: <tspan fill="#38BDF8">{telemetry.galois_connectivity_index:.3f}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 96}" font-size="9" fill="#475569">Eide &amp; Eide Interconnected Reasoning</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content
