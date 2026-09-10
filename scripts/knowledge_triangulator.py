#!/usr/bin/env python3
"""
Autonomous Cognitive Multimodal Knowledge Synthesis & Triangulation Radar
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Cross-triangulates claims and concepts across four modalities (Text, Code, Audio, Visual),
calculating multi-source consensus confidence scores and identifying uncorroborated
single-source assumptions across knowledge vaults.

Core Principles:
- Multi-Sensory Triangulation: Synthesizes text notes, code ASTs, audio recordings, and diagrams.
- Epistemic Grounding: Flags single-source claims lacking multi-modal corroboration.
- Spatial Radar Topologies: Visualizes cross-modal confidence on a 4-axis polar mesh.
"""

import os
import re
import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


VALID_MODALITIES = {"text", "code", "audio", "visual"}


@dataclass
class MultimodalSource:
    """Individual evidence artifact supporting a claim."""
    source_id: str
    modality: str  # "text", "code", "audio", "visual"
    label: str
    reference: str
    excerpt: str = ""


@dataclass
class TriangulatedClaim:
    """Core proposition verified across multimodal evidence channels."""
    claim_id: str
    statement: str
    sources: List[MultimodalSource] = field(default_factory=list)
    modalities_present: Set[str] = field(default_factory=set)
    confidence_score: float = 0.0
    is_corroborated: bool = False
    recommendation: str = ""


@dataclass
class TriangulationAudit:
    """Synthesis telemetry describing multi-modal coherence and verification health."""
    total_claims: int
    corroborated_claims_count: int
    uncorroborated_claims_count: int
    modality_distribution: Dict[str, int]
    overall_synthesis_confidence: float  # 0 to 100


class MultimodalKnowledgeTriangulator:
    """Evaluates cross-modal coherence across text, code, audio, and visual nodes."""

    MODALITY_COLORS = {
        "text": "4",     # Emerald (Obsidian canvas green)
        "code": "5",     # Cyan/Blue
        "audio": "6",    # Purple
        "visual": "2"    # Amber
    }

    def __init__(self):
        self.claims: Dict[str, TriangulatedClaim] = {}
        self._next_claim_idx = 1
        self._next_source_idx = 1

    def add_claim(self, statement: str, claim_id: Optional[str] = None) -> TriangulatedClaim:
        """Register a core conceptual claim or thesis proposition."""
        cid = claim_id or f"claim-{self._next_claim_idx}"
        self._next_claim_idx += 1

        claim = TriangulatedClaim(
            claim_id=cid,
            statement=statement.strip()
        )
        self.claims[cid] = claim
        return claim

    def attach_evidence(
        self,
        claim_id: str,
        modality: str,
        label: str,
        reference: str,
        excerpt: str = ""
    ) -> MultimodalSource:
        """Attach a supporting evidence piece to an existing claim."""
        if claim_id not in self.claims:
            raise KeyError(f"Claim ID '{claim_id}' not found.")

        mod_clean = modality.strip().lower()
        if mod_clean not in VALID_MODALITIES:
            mod_clean = "text"

        sid = f"src-{self._next_source_idx}"
        self._next_source_idx += 1

        source = MultimodalSource(
            source_id=sid,
            modality=mod_clean,
            label=label.strip(),
            reference=reference.strip(),
            excerpt=excerpt.strip()
        )

        claim = self.claims[claim_id]
        claim.sources.append(source)
        claim.modalities_present.add(mod_clean)
        self._recalculate_claim_confidence(claim)
        return source

    def _recalculate_claim_confidence(self, claim: TriangulatedClaim) -> None:
        """Calculate confidence percentage based on multimodal coverage."""
        mod_count = len(claim.modalities_present)
        # Score calculation: 25% per distinct modality (1=25%, 2=50%, 3=75%, 4=100%)
        # Slight bonus for multi-evidence depth (up to +10% max)
        depth_bonus = min(10.0, max(0.0, (len(claim.sources) - mod_count) * 2.5))
        base_score = mod_count * 25.0
        final_score = min(100.0, base_score + depth_bonus)

        claim.confidence_score = round(final_score, 1)
        claim.is_corroborated = (mod_count >= 2)

        if mod_count >= 4:
            claim.recommendation = "Fully Triangulated: Rock-solid multimodal empirical consensus."
        elif mod_count == 3:
            missing = (VALID_MODALITIES - claim.modalities_present).pop()
            claim.recommendation = f"High Confidence: Corroborated across 3 modalities. Missing {missing.title()} anchor."
        elif mod_count == 2:
            claim.recommendation = "Emerging Synthesis: Corroborated by 2 modalities. Add code or audio anchors."
        else:
            claim.recommendation = "Uncorroborated Single-Source: High risk of isolation or drift. Needs multi-modal verification."

    def parse_markdown_evidence(self, text: str) -> None:
        """
        Parse claims and multimodal evidence from structured markdown blocks:
        ### Claim: Zero-Copy Serialization Minimizes Latency
        - Text: Architectural specification section 3.1 | Ref: docs/spec.md | Excerpt: Zero-copy avoids kernel copies.
        - Code: fn serialize_zero_copy() | Ref: src/codec.rs:L85
        - Audio: Architecture Sync Podcast 18:20 | Ref: audio/sync_ep4.mp3
        - Visual: Dataflow diagram | Ref: diagrams/flow.svg
        """
        lines = text.splitlines()
        current_claim: Optional[TriangulatedClaim] = None

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            claim_match = re.match(r'^(?:#{1,4}\s*Claim:\s*|\[Claim:\s*)([^\]\n]+)\]?', line, re.IGNORECASE)
            if claim_match:
                statement = claim_match.group(1).strip()
                current_claim = self.add_claim(statement)
                continue

            if current_claim:
                ev_match = re.match(r'^[-\*]\s*(Text|Code|Audio|Visual):\s*([^\|]+)(?:\|\s*Ref:\s*([^\|]+))?(?:\|\s*Excerpt:\s*(.+))?$', line, re.IGNORECASE)
                if ev_match:
                    modality = ev_match.group(1).strip().lower()
                    label = ev_match.group(2).strip()
                    ref = (ev_match.group(3) or "").strip()
                    excerpt = (ev_match.group(4) or "").strip()
                    self.attach_evidence(current_claim.claim_id, modality, label, ref, excerpt)

    def audit_synthesis(self) -> TriangulationAudit:
        """Compute holistic audit telemetry across all registered claims."""
        total = len(self.claims)
        if total == 0:
            return TriangulationAudit(0, 0, 0, {m: 0 for m in VALID_MODALITIES}, 0.0)

        corroborated = sum(1 for c in self.claims.values() if c.is_corroborated)
        uncorroborated = total - corroborated

        mod_counts = {m: 0 for m in VALID_MODALITIES}
        for c in self.claims.values():
            for m in c.modalities_present:
                mod_counts[m] += 1

        avg_conf = sum(c.confidence_score for c in self.claims.values()) / float(total)

        return TriangulationAudit(
            total_claims=total,
            corroborated_claims_count=corroborated,
            uncorroborated_claims_count=uncorroborated,
            modality_distribution=mod_counts,
            overall_synthesis_confidence=round(avg_conf, 1)
        )

    def export_canvas(self) -> Dict[str, Any]:
        """Export claims and multimodal evidence into Obsidian .canvas layout."""
        nodes = []
        edges = []
        edge_idx = 1

        col_spacing = 450
        row_spacing = 320
        origin_x = 100
        origin_y = 100

        for c_idx, claim in enumerate(self.claims.values()):
            cx = origin_x + (c_idx * col_spacing)
            cy = origin_y

            # Claim Parent Node
            conf_bar = "[" + "=" * int(claim.confidence_score // 10) + " " * (10 - int(claim.confidence_score // 10)) + "]"
            claim_text = [
                f"### {claim.statement}",
                f"**Confidence:** `{claim.confidence_score}%` {conf_bar}",
                f"**Corroboration:** {'Corroborated' if claim.is_corroborated else 'Single-Source Warning'}",
                f"**Coverage:** {', '.join([m.title() for m in claim.modalities_present])}",
                f"\n> {claim.recommendation}"
            ]
            claim_node_id = claim.claim_id
            nodes.append({
                "id": claim_node_id,
                "type": "text",
                "text": "\n".join(claim_text),
                "x": cx,
                "y": cy,
                "width": 380,
                "height": 220,
                "color": "1" if not claim.is_corroborated else "4"
            })

            # Radial Satellite Evidences
            sat_dist = 280
            for s_idx, src in enumerate(claim.sources[:4]):
                angle = (s_idx * (2 * math.pi / max(1, len(claim.sources[:4]))))
                sx = int(cx + (sat_dist * math.cos(angle)))
                sy = int(cy + 260 + (sat_dist * math.sin(angle) * 0.5))

                src_text = [
                    f"#### [{src.modality.upper()}] {src.label}",
                    f"**Ref:** `{src.reference}`"
                ]
                if src.excerpt:
                    src_text.append(f"\n> {src.excerpt[:100]}...")

                nodes.append({
                    "id": src.source_id,
                    "type": "text",
                    "text": "\n".join(src_text),
                    "x": sx,
                    "y": sy,
                    "width": 260,
                    "height": 140,
                    "color": self.MODALITY_COLORS.get(src.modality, "2")
                })

                edges.append({
                    "id": f"edge-tri-{edge_idx}",
                    "fromNode": claim_node_id,
                    "toNode": src.source_id,
                    "label": src.modality.title(),
                    "color": self.MODALITY_COLORS.get(src.modality, "2")
                })
                edge_idx += 1

        return {
            "nodes": nodes,
            "edges": edges
        }

    def export_svg(self, width: int = 1100, height: int = 650) -> str:
        """Export 4-axis polar radar chart showing multimodal synthesis coverage."""
        audit = self.audit_synthesis()

        def safe_xml(s: str) -> str:
            return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            f'  <rect width="{width}" height="{height}" fill="#09090b" rx="16" />',
            f'  <!-- Header -->',
            f'  <text x="30" y="40" fill="#ffffff" font-size="16" font-weight="700" font-family="sans-serif">Multimodal Knowledge Synthesis &amp; Triangulation Radar</text>',
            f'  <text x="30" y="60" fill="#a1a1aa" font-size="11" font-family="sans-serif">Synthesis Confidence: {audit.overall_synthesis_confidence}% | Corroborated: {audit.corroborated_claims_count}/{audit.total_claims} | Uncorroborated: {audit.uncorroborated_claims_count}</text>'
        ]

        # Polar Radar Geometry (Center at x=340, y=360, radius=180)
        rx, ry, rad = 320, 360, 180
        axes = [
            ("Text", 0, -rad, 0, -rad - 15, "middle"),           # Top: Text (0 deg)
            ("Code", rad, 0, rad + 15, 5, "start"),             # Right: Code (90 deg)
            ("Audio", 0, rad, 0, rad + 20, "middle"),           # Bottom: Audio (180 deg)
            ("Visual", -rad, 0, -rad - 15, 5, "end")            # Left: Visual (270 deg)
        ]

        # Radar concentric rings
        for ring in [0.25, 0.5, 0.75, 1.0]:
            r_val = rad * ring
            svg.append(f'  <circle cx="{rx}" cy="{ry}" r="{r_val}" fill="none" stroke="#27272a" stroke-width="1" stroke-dasharray="3,3" />')
            svg.append(f'  <text x="{rx + 8}" y="{ry - r_val + 12}" fill="#52525b" font-size="8" font-family="sans-serif">{int(ring * 100)}%</text>')

        # Radar crosshairs
        svg.append(f'  <line x1="{rx - rad}" y1="{ry}" x2="{rx + rad}" y2="{ry}" stroke="#3f3f46" stroke-width="1.2" />')
        svg.append(f'  <line x1="{rx}" y1="{ry - rad}" x2="{rx}" y2="{ry + rad}" stroke="#3f3f46" stroke-width="1.2" />')

        for name, ax, ay, tx, ty, anchor in axes:
            svg.append(f'  <text x="{rx + tx}" y="{ry + ty}" fill="#38bdf8" font-size="12" font-weight="700" text-anchor="{anchor}" font-family="sans-serif">{name}</text>')

        # Compute average coverage on 4 axes
        max_c = max(1, audit.total_claims)
        norm_text = audit.modality_distribution["text"] / max_c
        norm_code = audit.modality_distribution["code"] / max_c
        norm_audio = audit.modality_distribution["audio"] / max_c
        norm_vis = audit.modality_distribution["visual"] / max_c

        # Polygon points
        p_top = (rx, ry - (rad * norm_text))
        p_right = (rx + (rad * norm_code), ry)
        p_bottom = (rx, ry + (rad * norm_audio))
        p_left = (rx - (rad * norm_vis), ry)

        poly_pts = f"{p_top[0]},{p_top[1]} {p_right[0]},{p_right[1]} {p_bottom[0]},{p_bottom[1]} {p_left[0]},{p_left[1]}"
        svg.append(f'  <!-- Synthesis Polygon -->')
        svg.append(f'  <polygon points="{poly_pts}" fill="#38bdf8" fill-opacity="0.25" stroke="#38bdf8" stroke-width="2" />')
        for pt in [p_top, p_right, p_bottom, p_left]:
            svg.append(f'  <circle cx="{pt[0]}" cy="{pt[1]}" r="4" fill="#38bdf8" />')

        # Right Side Claims Cards List
        card_start_x = 580
        card_start_y = 110
        c_w = 480
        c_h = 100
        gap_y = 18

        for idx, claim in enumerate(list(self.claims.values())[:4]):
            cy = card_start_y + (idx * (c_h + gap_y))
            border_color = "#10b981" if claim.is_corroborated else "#ef4444"

            svg.append(f'  <!-- Claim Card #{idx + 1} -->')
            svg.append(f'  <rect x="{card_start_x}" y="{cy}" width="{c_w}" height="{c_h}" rx="10" fill="#18181b" stroke="{border_color}" stroke-width="1.5" />')
            svg.append(f'  <text x="{card_start_x + 16}" y="{cy + 24}" fill="#ffffff" font-size="12" font-weight="700" font-family="sans-serif">{safe_xml(claim.statement[:48])}...</text>')
            svg.append(f'  <text x="{card_start_x + 16}" y="{cy + 42}" fill="#a1a1aa" font-size="9" font-family="sans-serif">Confidence: {claim.confidence_score}% | Coverage: {", ".join([m.title() for m in claim.modalities_present])}</text>')
            svg.append(f'  <text x="{card_start_x + 16}" y="{cy + 62}" fill="{border_color}" font-size="9" font-weight="600" font-family="sans-serif">{safe_xml(claim.recommendation[:64])}...</text>')
            svg.append(f'  <text x="{card_start_x + 16}" y="{cy + 82}" fill="#71717a" font-size="8" font-family="sans-serif">Evidence items attached: {len(claim.sources)}</text>')

        # Footer
        svg.append(f'  <text x="{width // 2}" y="{height - 20}" fill="#71717a" font-size="10" text-anchor="middle" font-family="sans-serif">Green: Corroborated Multi-Modal Consensus | Red: Uncorroborated Single-Source Claim</text>')
        svg.append('</svg>')
        return "\n".join(svg)

    @classmethod
    def export_summary(cls, audit: TriangulationAudit, claims_sample: List[TriangulatedClaim]) -> str:
        """Generate executive markdown summary of multimodal triangulation."""
        claims_rows = "\n".join([
            f"| `{c.claim_id}` | **{c.statement[:45]}...** | `{c.confidence_score}%` | {', '.join([m.title() for m in c.modalities_present])} | {'Corroborated' if c.is_corroborated else 'Single-Source'} |"
            for c in claims_sample[:8]
        ])

        return (
            f"# Multimodal Knowledge Synthesis & Triangulation Radar\n\n"
            f"**Overall Synthesis Confidence:** `{audit.overall_synthesis_confidence}%`\n"
            f"**Total Claims Evaluated:** `{audit.total_claims}` | **Corroborated:** `{audit.corroborated_claims_count}`\n"
            f"**Uncorroborated Single-Source Claims:** `{audit.uncorroborated_claims_count}`\n\n"
            f"### Modality Distribution Breakdown\n"
            f"- **Textual Notes:** `{audit.modality_distribution.get('text', 0)} claims`\n"
            f"- **Code AST / Symbols:** `{audit.modality_distribution.get('code', 0)} claims`\n"
            f"- **Audio / Transcripts:** `{audit.modality_distribution.get('audio', 0)} claims`\n"
            f"- **Visual Diagrams:** `{audit.modality_distribution.get('visual', 0)} claims`\n\n"
            f"### Triangulated Claims Topography\n\n"
            f"| Claim ID | Statement | Confidence | Modalities | Status |\n"
            f"| :--- | :--- | :--- | :--- | :--- |\n"
            f"{claims_rows}\n\n"
            f"### Cognitive Diagnostic Recommendations\n"
            f"- **Cross-Modal Grounding:** When claims span text, code, audio, and visual nodes, retention increases and conceptual errors drop by up to 50%.\n"
            f"- **Isolate Single-Source Biases:** Pay immediate attention to uncorroborated claims to avoid building complex mental models on unverified foundations.\n"
            f"- **Spatial Radar Equilibrium:** Strive for balanced coverage across all 4 quadrants of the synthesis radar.\n"
        )


def main():
    """Quick CLI runner."""
    print("MultimodalKnowledgeTriangulator Loaded.")


if __name__ == "__main__":
    main()
