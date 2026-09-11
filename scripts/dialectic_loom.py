"""
dialectic_loom.py - Autonomous Cognitive Spatial Multi-Perspective Dialectic Reification & Synthesis Loom

Part of the DxSkills cognitive scaffolding suite (Phase 97, Cycle 93).
Grounded in Eide & Eide Interconnected Reasoning (I-strength), Hegelian
Aufhebung logic (sublation without shallow compromise), and Cowan 4-chunk
working memory constraints.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ArgumentCard:
    """Represents an input argument or architectural proposition card."""
    card_id: str
    title: str
    statement: str
    perspective: str = "neutral"  # thesis, antithesis, or neutral
    domain: str = "architecture"
    core_values: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TensionVector:
    """Structural divergence vector between two opposing architectural poles."""
    tension_id: str
    axis_name: str
    thesis_card_id: str
    antithesis_card_id: str
    intensity: float  # 0.0 to 1.0
    divergence_rationale: str
    underlying_tradeoff: str
    is_critical_path: bool = False


@dataclass
class AufhebungBridge:
    """Emergent architectural synthesis transcending binary polarization."""
    bridge_id: str
    title: str
    synthesis_paradigm: str
    thesis_preserved_strength: str
    antithesis_preserved_strength: str
    eliminated_failure_modes: List[str]
    concrete_implementation_pattern: str
    invariant_guarantees: List[str]
    reification_fidelity: float  # 0.0 to 1.0
    target_tension_ids: List[str] = field(default_factory=list)


@dataclass
class LoomTelemetry:
    """Cognitive telemetry and structural balance metrics for the dialectic loom."""
    total_cards_processed: int
    theses_count: int
    antitheses_count: int
    structural_tensions_identified: int
    critical_tensions_count: int
    mean_tension_intensity: float
    dialectic_entropy: float  # 0.0 (fully resolved) to 1.0 (chaotic polarization)
    resolution_ratio: float
    cowan_bounded: bool  # True if synthesized working set <= 4 chunks
    cognitive_load_saved_pct: float


@dataclass
class DialecticLoomResult:
    """Master result bundle produced by the Dialectic Loom."""
    cards: List[ArgumentCard]
    tensions: List[TensionVector]
    bridges: List[AufhebungBridge]
    telemetry: LoomTelemetry

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cards": [asdict(c) for c in self.cards],
            "tensions": [asdict(t) for t in self.tensions],
            "bridges": [asdict(b) for b in self.bridges],
            "telemetry": asdict(self.telemetry),
        }


class DialecticLoom:
    """
    Autonomous Cognitive Spatial Multi-Perspective Dialectic Reification & Synthesis Loom.

    Identifies antithetical polarities in multi-card architectural arguments,
    maps structural tension vectors, and synthesizes concrete Aufhebung bridges
    grounded in Eide & Eide Interconnected reasoning.
    """

    KNOWN_POLARITY_PAIRS: List[Tuple[str, str, str, str]] = [
        ("autonomy", "coherence", "Independent service boundary vs unified system governance", "Decoupled micro-cells with schema-checked contracts"),
        ("consistency", "availability", "Strict linearizability vs partition resilience (CAP)", "Local-first CRDT stores with deterministic merge"),
        ("velocity", "stability", "Rapid iteration deployment vs rigorous formal verification", "Automated shadow pipelines with progressive rollouts"),
        ("monolith", "microservices", "Unified shared-memory binary vs distributed RPC topology", "Modular monolith with strict interface boundaries"),
        ("immutability", "efficiency", "Pure functional state trees vs zero-copy in-place mutation", "Append-only write-ahead log with in-memory materialized views"),
        ("centralized", "decentralized", "Single coordinator bottleneck vs gossip protocol convergence", "Hierarchical raft clusters with autonomous edge zones"),
        ("flexibility", "rigor", "Dynamic unconstrained typing vs strict static contracts", "Gradual typing with compile-time schema validation"),
        ("synchronous", "asynchronous", "Immediate blocking feedback vs decoupled event-driven queues", "CQRS command bus with read-optimized optimistic responses"),
    ]

    def __init__(self, max_working_memory_chunks: int = 4) -> None:
        self.max_working_memory_chunks = max_working_memory_chunks

    def load_cards(self, data: Any) -> List[ArgumentCard]:
        """Loads and normalizes argument cards from list, dict, or canvas structure."""
        cards: List[ArgumentCard] = []

        if isinstance(data, list):
            for idx, item in enumerate(data):
                if isinstance(item, dict):
                    cid = str(item.get("id") or item.get("card_id") or f"card_{idx+1}")
                    title = str(item.get("title") or item.get("text", "")[:30] or f"Card {idx+1}")
                    statement = str(item.get("statement") or item.get("text") or item.get("description") or title)
                    persp = str(item.get("perspective", "neutral")).lower()
                    values = list(item.get("core_values") or item.get("values") or [])
                    failures = list(item.get("failure_modes") or item.get("risks") or [])
                    tags = list(item.get("tags") or [])
                    cards.append(ArgumentCard(
                        card_id=cid,
                        title=title,
                        statement=statement,
                        perspective=persp,
                        domain=str(item.get("domain", "architecture")),
                        core_values=values,
                        failure_modes=failures,
                        tags=tags,
                        metadata=item.get("metadata", {}),
                    ))
        elif isinstance(data, dict):
            # Check Obsidian canvas format
            nodes = data.get("nodes")
            if isinstance(nodes, list):
                for idx, node in enumerate(nodes):
                    nid = str(node.get("id") or f"node_{idx+1}")
                    text = str(node.get("text") or "")
                    lines = text.splitlines()
                    title = lines[0].lstrip("# ").strip() if lines else f"Node {idx+1}"
                    statement = "\n".join(lines[1:]).strip() if len(lines) > 1 else text
                    cards.append(ArgumentCard(
                        card_id=nid,
                        title=title,
                        statement=statement or title,
                        perspective="neutral",
                        metadata=node,
                    ))
            elif isinstance(nodes, dict):
                for nid, n_data in nodes.items():
                    if isinstance(n_data, dict):
                        title = str(n_data.get("title") or n_data.get("text", "")[:30] or nid)
                        stmt = str(n_data.get("statement") or n_data.get("text") or title)
                        cards.append(ArgumentCard(
                            card_id=str(nid),
                            title=title,
                            statement=stmt,
                            perspective=str(n_data.get("perspective", "neutral")).lower(),
                            metadata=n_data,
                        ))
            elif "cards" in data and isinstance(data["cards"], list):
                return self.load_cards(data["cards"])

        return cards

    def analyze(self, raw_data: Any) -> DialecticLoomResult:
        """Executes end-to-end structural tension mapping and Aufhebung synthesis."""
        cards = self.load_cards(raw_data)
        if not cards:
            return DialecticLoomResult(
                cards=[],
                tensions=[],
                bridges=[],
                telemetry=LoomTelemetry(
                    total_cards_processed=0,
                    theses_count=0,
                    antitheses_count=0,
                    structural_tensions_identified=0,
                    critical_tensions_count=0,
                    mean_tension_intensity=0.0,
                    dialectic_entropy=0.0,
                    resolution_ratio=1.0,
                    cowan_bounded=True,
                    cognitive_load_saved_pct=0.0,
                ),
            )

        # 1. Classify perspectives if neutral
        theses: List[ArgumentCard] = []
        antitheses: List[ArgumentCard] = []
        neutrals: List[ArgumentCard] = []

        for card in cards:
            classified_persp = self._classify_perspective(card)
            card.perspective = classified_persp
            if classified_persp == "thesis":
                theses.append(card)
            elif classified_persp == "antithesis":
                antitheses.append(card)
            else:
                neutrals.append(card)

        # If unbalanced, partition based on polarity heuristics
        if not theses and antitheses:
            theses.append(antitheses.pop(0))
            theses[0].perspective = "thesis"
        elif not antitheses and theses:
            antitheses.append(theses.pop(-1))
            antitheses[0].perspective = "antithesis"
        elif not theses and not antitheses and len(cards) >= 2:
            theses.append(cards[0])
            cards[0].perspective = "thesis"
            antitheses.append(cards[1])
            cards[1].perspective = "antithesis"

        # 2. Structural Tension Mapping (Task 97.1)
        tensions = self._map_structural_tensions(theses, antitheses)

        # 3. Aufhebung Bridge Weaving (Task 97.2)
        bridges = self._weave_aufhebung_bridges(theses, antitheses, tensions)

        # 4. Telemetry and cognitive load estimation
        mean_intensity = (
            sum(t.intensity for t in tensions) / len(tensions) if tensions else 0.0
        )
        critical_count = sum(1 for t in tensions if t.is_critical_path)
        resolved_tensions_set = set()
        for b in bridges:
            resolved_tensions_set.update(b.target_tension_ids)

        resolution_ratio = (
            len(resolved_tensions_set) / len(tensions) if tensions else 1.0
        )
        # Dialectic entropy: high if many un-resolved high-intensity tensions
        unresolved_weight = sum(
            t.intensity for t in tensions if t.tension_id not in resolved_tensions_set
        )
        raw_entropy = unresolved_weight / max(1, len(tensions))
        dialectic_entropy = round(min(1.0, raw_entropy), 3)

        # Cowan chunk bounding (target working set: active bridges + focal poles <= 4)
        active_chunks = len(bridges) + min(len(theses), 2)
        cowan_bounded = active_chunks <= self.max_working_memory_chunks

        # Load reduction: organizing polarized sprawl into 1-2 Aufhebung nodes
        unscaffolded_chunks = len(cards) + len(tensions)
        saved_pct = round(
            max(0.0, min(85.0, (1.0 - (active_chunks / max(1, unscaffolded_chunks))) * 100.0)),
            1,
        )

        telemetry = LoomTelemetry(
            total_cards_processed=len(cards),
            theses_count=len(theses),
            antitheses_count=len(antitheses),
            structural_tensions_identified=len(tensions),
            critical_tensions_count=critical_count,
            mean_tension_intensity=round(mean_intensity, 3),
            dialectic_entropy=dialectic_entropy,
            resolution_ratio=round(resolution_ratio, 3),
            cowan_bounded=cowan_bounded,
            cognitive_load_saved_pct=saved_pct,
        )

        return DialecticLoomResult(
            cards=cards,
            tensions=tensions,
            bridges=bridges,
            telemetry=telemetry,
        )

    def _classify_perspective(self, card: ArgumentCard) -> str:
        """Determines if card acts as thesis or antithesis via textual markers."""
        if card.perspective in ("thesis", "antithesis"):
            return card.perspective

        full_text = f"{card.title} {card.statement} {' '.join(card.tags)}".lower()

        thesis_keywords = [
            "decouple", "autonomy", "microservice", "eventual", "asynchronous",
            "distributed", "flexibility", "immutability", "local-first", "thesis",
            "speed", "velocity", "modular", "dynamic"
        ]
        antithesis_keywords = [
            "monolith", "centralized", "linearizable", "consistency", "strict",
            "governance", "synchronous", "shared state", "antithesis", "formal",
            "stability", "auditability", "uniform", "in-place"
        ]

        t_score = sum(1 for kw in thesis_keywords if kw in full_text)
        a_score = sum(1 for kw in antithesis_keywords if kw in full_text)

        if t_score > a_score:
            return "thesis"
        elif a_score > t_score:
            return "antithesis"
        return "neutral"

    def _map_structural_tensions(
        self, theses: List[ArgumentCard], antitheses: List[ArgumentCard]
    ) -> List[TensionVector]:
        """Task 97.1: Maps structural tension vectors between opposing poles."""
        tensions: List[TensionVector] = []
        counter = 1

        for t_card in theses:
            t_text = f"{t_card.title} {t_card.statement}".lower()
            for a_card in antitheses:
                a_text = f"{a_card.title} {a_card.statement}".lower()

                # Check known architectural polarity matches
                matched_polarity = None
                for p_thesis, p_antithesis, rationale, _ in self.KNOWN_POLARITY_PAIRS:
                    if (p_thesis in t_text and p_antithesis in a_text) or (
                        p_antithesis in t_text and p_thesis in a_text
                    ):
                        matched_polarity = (p_thesis, p_antithesis, rationale)
                        break

                if matched_polarity:
                    axis = f"{matched_polarity[0].capitalize()} vs {matched_polarity[1].capitalize()}"
                    rationale = matched_polarity[2]
                    intensity = 0.85
                    is_critical = True
                else:
                    # Generic divergence detection
                    axis = "Architectural Coupling vs Autonomy"
                    rationale = f"Structural polarity between '{t_card.title}' and '{a_card.title}'"
                    intensity = 0.65
                    is_critical = counter == 1

                tensions.append(
                    TensionVector(
                        tension_id=f"ten_{counter:02d}",
                        axis_name=axis,
                        thesis_card_id=t_card.card_id,
                        antithesis_card_id=a_card.card_id,
                        intensity=round(intensity, 2),
                        divergence_rationale=rationale,
                        underlying_tradeoff=f"Balancing {t_card.title} against {a_card.title}",
                        is_critical_path=is_critical,
                    )
                )
                counter += 1

        # Fallback if empty
        if not tensions and (theses or antitheses):
            t_id = theses[0].card_id if theses else "card_t"
            a_id = antitheses[0].card_id if antitheses else "card_a"
            tensions.append(
                TensionVector(
                    tension_id="ten_01",
                    axis_name="Global Coherence vs Local Velocity",
                    thesis_card_id=t_id,
                    antithesis_card_id=a_id,
                    intensity=0.70,
                    divergence_rationale="Latent system-level friction between independent sub-canvases",
                    underlying_tradeoff="Balancing local agility against overall systemic integration",
                    is_critical_path=True,
                )
            )

        return tensions

    def _weave_aufhebung_bridges(
        self,
        theses: List[ArgumentCard],
        antitheses: List[ArgumentCard],
        tensions: List[TensionVector],
    ) -> List[AufhebungBridge]:
        """Task 97.2: Synthesizes concrete Aufhebung bridges resolving structural tensions."""
        bridges: List[AufhebungBridge] = []
        if not tensions:
            return bridges

        # Cluster tensions by axis or group into unified syntheses
        # For Cowan working memory bounds, synthesize into 1 or 2 high-level bridges
        bridge_idx = 1

        # Check if known polarity pair applies
        primary_tension = tensions[0]
        found_pattern = None
        for p_thesis, p_antithesis, _, pattern in self.KNOWN_POLARITY_PAIRS:
            if (
                p_thesis in primary_tension.axis_name.lower()
                or p_antithesis in primary_tension.axis_name.lower()
            ):
                found_pattern = pattern
                break

        t_card = next((c for c in theses if c.card_id == primary_tension.thesis_card_id), None)
        a_card = next((c for c in antitheses if c.card_id == primary_tension.antithesis_card_id), None)

        t_title = t_card.title if t_card else "Thesis Core"
        a_title = a_card.title if a_card else "Antithesis Core"

        if not found_pattern:
            found_pattern = "Dual-Plane Coordination Layer with Formal Contract Gateway"

        bridge = AufhebungBridge(
            bridge_id=f"aufhebung_{bridge_idx:02d}",
            title=f"Aufhebung Synthesis: {t_title} & {a_title}",
            synthesis_paradigm="Emergent Sublation (Higher-Order Architectural Synthesis)",
            thesis_preserved_strength=f"Preserves primary advantages of {t_title} without unconstrained drift",
            antithesis_preserved_strength=f"Retains foundational guarantees of {a_title} without global bottleneck",
            eliminated_failure_modes=[
                f"Eliminates cascade failures from pure {t_title}",
                f"Eliminates rigid throughput ceilings from pure {a_title}",
            ],
            concrete_implementation_pattern=found_pattern,
            invariant_guarantees=[
                "Deterministic boundary contracts verified at build time",
                "Sub-system isolation preserved under partition conditions",
                "Non-blocking local state transitions with convergence audit log",
            ],
            reification_fidelity=0.92,
            target_tension_ids=[t.tension_id for t in tensions[:3]],
        )
        bridges.append(bridge)

        # If more than 3 tensions exist, create a second specialized bridge
        if len(tensions) > 3:
            bridge_idx += 1
            secondary_tension = tensions[3]
            bridges.append(
                AufhebungBridge(
                    bridge_id=f"aufhebung_{bridge_idx:02d}",
                    title=f"Secondary Aufhebung: Adaptive Operational Boundary",
                    synthesis_paradigm="Dynamic Runtime Mediation Engine",
                    thesis_preserved_strength="Local execution autonomy under standard workload envelopes",
                    antithesis_preserved_strength="Centralized fallback orchestration during boundary violations",
                    eliminated_failure_modes=[
                        "Unmonitored state drift across autonomous worker nodes",
                        "Single point of failure lockup under heavy load spikes",
                    ],
                    concrete_implementation_pattern="Hierarchical Event Bus with Supervised Circuit Breakers",
                    invariant_guarantees=[
                        "Zero unmonitored divergence across cluster boundaries",
                        "Graceful degradation to local snapshot stores during outages",
                    ],
                    reification_fidelity=0.88,
                    target_tension_ids=[t.tension_id for t in tensions[3:]],
                )
            )

        return bridges

    def export_canvas(self, result: DialecticLoomResult, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Exports dialectic triad and Aufhebung bridges as an Obsidian Canvas JSON structure.
        Layout:
          - Left column: Theses (Cyan)
          - Right column: Antitheses (Crimson/Amber)
          - Center/Top: Aufhebung Synthesis Bridges (Emerald Green / Purple)
          - Tension and synthesis edges connecting the nodes.
        """
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []

        # Color codes: 4 = cyan, 1 = red/crimson, 3 = green, 5 = purple
        COLOR_THESIS = "4"
        COLOR_ANTITHESIS = "1"
        COLOR_AUFHEBUNG = "3"

        # Theses on Left (x = -400)
        y_pos = 100
        for card in [c for c in result.cards if c.perspective == "thesis"]:
            nodes.append({
                "id": card.card_id,
                "type": "text",
                "text": f"### [Thesis] {card.title}\n\n{card.statement}\n\n*Core Values:* {', '.join(card.core_values) or 'Autonomy, Agility'}",
                "x": -450,
                "y": y_pos,
                "width": 320,
                "height": 220,
                "color": COLOR_THESIS,
            })
            y_pos += 260

        # Antitheses on Right (x = 450)
        y_pos = 100
        for card in [c for c in result.cards if c.perspective == "antithesis"]:
            nodes.append({
                "id": card.card_id,
                "type": "text",
                "text": f"### [Antithesis] {card.title}\n\n{card.statement}\n\n*Core Values:* {', '.join(card.core_values) or 'Integrity, Coherence'}",
                "x": 450,
                "y": y_pos,
                "width": 320,
                "height": 220,
                "color": COLOR_ANTITHESIS,
            })
            y_pos += 260

        # Aufhebung Bridges in Center (x = 0, y = -250)
        b_x = 0
        for bridge in result.bridges:
            b_text = (
                f"## 🏛️ {bridge.title}\n\n"
                f"**Paradigm:** {bridge.synthesis_paradigm}\n\n"
                f"**Implementation:** `{bridge.concrete_implementation_pattern}`\n\n"
                f"**Preserved Thesis:** {bridge.thesis_preserved_strength}\n\n"
                f"**Preserved Antithesis:** {bridge.antithesis_preserved_strength}\n\n"
                f"**Eliminated Pathologies:**\n- " + "\n- ".join(bridge.eliminated_failure_modes)
            )
            nodes.append({
                "id": bridge.bridge_id,
                "type": "text",
                "text": b_text,
                "x": b_x,
                "y": -280,
                "width": 460,
                "height": 340,
                "color": COLOR_AUFHEBUNG,
            })
            b_x += 500

        # Add edges: Tension lines between opposing cards
        edge_id_counter = 1
        for tension in result.tensions:
            edges.append({
                "id": f"edge_ten_{edge_id_counter}",
                "fromNode": tension.thesis_card_id,
                "toNode": tension.antithesis_card_id,
                "label": f"⚡ Tension: {tension.axis_name} ({tension.intensity:.2f})",
                "color": "1",
            })
            edge_id_counter += 1

        # Add edges: Synthesis connections from thesis & antithesis to Aufhebung bridge
        for bridge in result.bridges:
            for tension in result.tensions:
                if tension.tension_id in bridge.target_tension_ids:
                    edges.append({
                        "id": f"edge_syn_{edge_id_counter}",
                        "fromNode": tension.thesis_card_id,
                        "toNode": bridge.bridge_id,
                        "label": "sublated into",
                        "color": "3",
                    })
                    edge_id_counter += 1
                    edges.append({
                        "id": f"edge_syn_{edge_id_counter}",
                        "fromNode": tension.antithesis_card_id,
                        "toNode": bridge.bridge_id,
                        "label": "sublated into",
                        "color": "3",
                    })
                    edge_id_counter += 1

        canvas_dict = {"nodes": nodes, "edges": edges}

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(canvas_dict, f, indent=2)

        return canvas_dict

    def export_svg(self, result: DialecticLoomResult, output_path: Optional[str] = None) -> str:
        """
        Exports a dark titanium visual SVG diagram depicting the Dialectic Triad:
        Thesis (Left Cyan), Antithesis (Right Crimson), Tension Axis (Dashed Red),
        and Aufhebung Bridge (Center Emerald Green).
        """
        w, h = 900, 540
        primary_bridge = result.bridges[0] if result.bridges else None
        b_title = primary_bridge.title if primary_bridge else "Aufhebung Bridge"
        b_pattern = primary_bridge.concrete_implementation_pattern if primary_bridge else "Synthesis"
        saved_pct = result.telemetry.cognitive_load_saved_pct

        theses = [c for c in result.cards if c.perspective == "thesis"]
        antitheses = [c for c in result.cards if c.perspective == "antithesis"]
        t_name = theses[0].title if theses else "Thesis"
        a_name = antitheses[0].title if antitheses else "Antithesis"

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '  <defs>',
            '    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#0a0e17"/>',
            '      <stop offset="100%" stop-color="#141c2e"/>',
            '    </linearGradient>',
            '    <linearGradient id="thesisGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.25"/>',
            '      <stop offset="100%" stop-color="#0ea5e9" stop-opacity="0.10"/>',
            '    </linearGradient>',
            '    <linearGradient id="antiGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#e11d48" stop-opacity="0.25"/>',
            '      <stop offset="100%" stop-color="#f43f5e" stop-opacity="0.10"/>',
            '    </linearGradient>',
            '    <linearGradient id="aufGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#059669" stop-opacity="0.30"/>',
            '      <stop offset="100%" stop-color="#10b981" stop-opacity="0.15"/>',
            '    </linearGradient>',
            '  </defs>',
            '  <rect width="100%" height="100%" fill="url(#bg)"/>',
            '  <!-- Header -->',
            '  <text x="40" y="46" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Dialectic Reification &amp; Synthesis Loom</text>',
            f'  <text x="40" y="70" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#94a3b8">Hegelian Aufhebung &bull; Cognitive Load Saved: {saved_pct}% &bull; Cowan Bounded: {result.telemetry.cowan_bounded}</text>',
            '  <!-- Tension Axis Line -->',
            '  <line x1="240" y1="360" x2="660" y2="360" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,6" opacity="0.7"/>',
            '  <rect x="400" y="344" width="100" height="26" rx="13" fill="#1e1b4b" stroke="#6366f1" stroke-width="1.5"/>',
            '  <text x="450" y="361" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#c7d2fe" text-anchor="middle">⚡ TENSION AXIS</text>',
            '  <!-- Synthesis Uplift Vectors -->',
            '  <path d="M 220 300 Q 320 220 420 180" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,4" opacity="0.8"/>',
            '  <path d="M 680 300 Q 580 220 480 180" fill="none" stroke="#fb7185" stroke-width="2" stroke-dasharray="4,4" opacity="0.8"/>',
            '  <!-- Card 1: Thesis -->',
            '  <rect x="60" y="270" width="260" height="170" rx="12" fill="url(#thesisGrad)" stroke="#0ea5e9" stroke-width="1.5"/>',
            '  <rect x="76" y="286" width="70" height="20" rx="6" fill="#0369a1"/>',
            '  <text x="111" y="300" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">THESIS</text>',
            f'  <text x="76" y="330" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="700" fill="#f0f9ff">{t_name[:24]}</text>',
            '  <text x="76" y="356" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#bae6fd">Primary drive: Autonomy &amp; Speed</text>',
            '  <text x="76" y="380" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#7dd3fc">Risk: System fragmentation</text>',
            '  <!-- Card 2: Antithesis -->',
            '  <rect x="580" y="270" width="260" height="170" rx="12" fill="url(#antiGrad)" stroke="#f43f5e" stroke-width="1.5"/>',
            '  <rect x="596" y="286" width="90" height="20" rx="6" fill="#be123c"/>',
            '  <text x="641" y="300" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">ANTITHESIS</text>',
            f'  <text x="596" y="330" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="700" fill="#fff1f2">{a_name[:24]}</text>',
            '  <text x="596" y="356" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#fecdd3">Primary drive: Coherence &amp; Guardrails</text>',
            '  <text x="596" y="380" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#fda4af">Risk: Central coordinator stall</text>',
            '  <!-- Center Top: Aufhebung Bridge -->',
            '  <rect x="250" y="90" width="400" height="150" rx="14" fill="url(#aufGrad)" stroke="#10b981" stroke-width="2"/>',
            '  <rect x="270" y="106" width="160" height="22" rx="6" fill="#047857"/>',
            '  <text x="350" y="121" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">AUFHEBUNG SYNTHESIS</text>',
            f'  <text x="270" y="152" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#ecfdf5">{b_title[:38]}</text>',
            f'  <text x="270" y="176" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" fill="#6ee7b7">Pattern: {b_pattern[:40]}</text>',
            '  <text x="270" y="198" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#a7f3d0">&bull; Cancels mutual pathologies without shallow compromise</text>',
            '  <text x="270" y="216" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#a7f3d0">&bull; Preserves invariant boundaries under high load</text>',
            '  <!-- Footer Telemetry Badges -->',
            f'  <text x="40" y="500" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#64748b">Cards: {result.telemetry.total_cards_processed} | Tensions: {result.telemetry.structural_tensions_identified} | Dialectic Entropy: {result.telemetry.dialectic_entropy} | Resolution: {int(result.telemetry.resolution_ratio * 100)}%</text>',
            '</svg>',
        ]

        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def generate_ascii_report(self, result: DialecticLoomResult) -> str:
        """Generates a clean terminal ASCII table summarizing the dialectic analysis."""
        lines = [
            "================================================================================",
            "   DIALECTIC REIFICATION & SYNTHESIS LOOM (PHASE 97 / CYCLE 93)",
            "================================================================================",
            f" Cards Analyzed       : {result.telemetry.total_cards_processed} (Thesis: {result.telemetry.theses_count}, Antithesis: {result.telemetry.antitheses_count})",
            f" Structural Tensions  : {result.telemetry.structural_tensions_identified} (Critical Path: {result.telemetry.critical_tensions_count})",
            f" Dialectic Entropy    : {result.telemetry.dialectic_entropy:.3f} (0.0=Resolved, 1.0=Polarized)",
            f" Resolution Ratio     : {result.telemetry.resolution_ratio * 100:.1f}%",
            f" Cowan Bounded (<=4)  : {'Yes [OPTIMAL]' if result.telemetry.cowan_bounded else 'No [EXCEEDS CHUNK LIMIT]'}",
            f" Working Memory Saved : {result.telemetry.cognitive_load_saved_pct:.1f}%",
            "--------------------------------------------------------------------------------",
            " IDENTIFIED STRUCTURAL TENSIONS",
            "--------------------------------------------------------------------------------",
        ]

        if not result.tensions:
            lines.append(" (No structural tensions identified)")
        else:
            for t in result.tensions:
                crit = "[CRITICAL]" if t.is_critical_path else "[SECONDARY]"
                lines.append(f" {t.tension_id.upper()} {crit:<11} | Intensity: {t.intensity:.2f} | Axis: {t.axis_name}")
                lines.append(f"   Trade-off : {t.underlying_tradeoff}")
                lines.append(f"   Rationale : {t.divergence_rationale}")

        lines.extend([
            "--------------------------------------------------------------------------------",
            " EMERGENT AUFHEBUNG BRIDGES (SUBLATION WITHOUT COMPROMISE)",
            "--------------------------------------------------------------------------------",
        ])

        if not result.bridges:
            lines.append(" (No Aufhebung bridges synthesized)")
        else:
            for b in result.bridges:
                lines.append(f" [AUFHEBUNG] {b.bridge_id.upper()}: {b.title}")
                lines.append(f"    Paradigm   : {b.synthesis_paradigm}")
                lines.append(f"    Pattern    : {b.concrete_implementation_pattern}")
                lines.append(f"    Preserved  : {b.thesis_preserved_strength}")
                lines.append(f"               : {b.antithesis_preserved_strength}")
                lines.append(f"    Cancelled  : {', '.join(b.eliminated_failure_modes)}")
                lines.append("    Guarantees :")
                for g in b.invariant_guarantees:
                    lines.append(f"      - {g}")

        lines.append("================================================================================")
        return "\n".join(lines)
