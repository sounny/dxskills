#!/usr/bin/env python3
"""
Autonomous Cognitive Multi-Perspective Thesis Dialectic Matrix & Consensus Engine
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Decomposes complex multi-stakeholder debates, peer reviews, or product roadmaps
into a structured 2D Hegelian dialectic matrix (Thesis, Antithesis, Synthesis).
Resolves semantic divergence by identifying underlying conceptual alignment
beneath conflicting surface vocabulary.

Core Principles:
- De-escalate Wall-of-Text Conflict: Transforms verbal friction into clear spatial triads.
- False Divergence Detection: Distinguishes true trade-offs from vocabulary mismatches.
- High-Order Synthesis: Resolves opposing constraints without binary zero-sum trade-offs.
"""

import os
import re
import math
import json
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set


# Standard English stop words
STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}


# Known synonym clusters representing common conceptual alignments across technical fields
CONCEPT_CLUSTERS: List[Tuple[str, Set[str]]] = [
    ("Speed", {"speed", "velocity", "throughput", "latency", "fast", "rapid", "performance"}),
    ("Reliability", {"reliability", "stability", "robustness", "fault-tolerance", "resilience", "dependability"}),
    ("Security", {"security", "privacy", "safety", "protection", "compliance", "isolation", "hardening"}),
    ("Clarity", {"clarity", "simplicity", "minimalism", "usability", "readability", "ergonomics", "intuition"}),
    ("Scalability", {"scale", "growth", "distributed", "scalability", "concurrency", "volume", "capacity"}),
    ("Quality", {"quality", "thoroughness", "accuracy", "precision", "rigor", "correctness", "fidelity"}),
    ("Efficiency", {"cost", "budget", "efficiency", "frugality", "lean", "overhead", "resources"})
]


def tokenize(text: str) -> List[str]:
    """Tokenize raw text into clean lowercased tokens omitting stop words."""
    raw = re.findall(r'[a-zA-Z0-9_\-\u00C0-\u017F]+', text.lower())
    clean = []
    for tok in raw:
        tok_clean = tok.strip("-_")
        if len(tok_clean) > 2 and tok_clean not in STOP_WORDS and not tok_clean.isdigit():
            clean.append(tok_clean)
    return clean


@dataclass
class Perspective:
    """Represents a stakeholder viewpoint, reviewer critique, or philosophical stance."""
    name: str
    raw_text: str
    tokens: List[str] = field(default_factory=list)
    key_claims: List[str] = field(default_factory=list)
    core_values: List[str] = field(default_factory=list)


@dataclass
class DialecticTension:
    """Represents a direct conflict, trade-off, or perceived divergence between two perspectives."""
    perspective_a: str
    perspective_b: str
    topic: str
    claim_a: str
    claim_b: str
    is_false_divergence: bool  # True if they share underlying concept despite different wording
    shared_concept: Optional[str] = None
    polarity_weight: float = 0.5  # 0.0 (semantic match) to 1.0 (irreconcilable zero-sum)


@dataclass
class DialecticSynthesis:
    """Higher-order resolution integrating opposing claims into a workable compromise."""
    title: str
    description: str
    tension_resolved: str
    integrates_from_a: str
    integrates_from_b: str
    consensus_score: float  # 0 to 100


@dataclass
class DialecticMatrixResult:
    """Complete multi-perspective dialectic matrix and consensus analysis."""
    perspectives: List[Perspective]
    tensions: List[DialecticTension]
    syntheses: List[DialecticSynthesis]
    consensus_readiness_index: float  # 0 to 100%
    shared_vocabulary_pct: float
    total_false_divergences: int


class DialecticMatrixEngine:
    """Decomposes multi-agent perspectives into thesis-antithesis-synthesis triads."""

    def __init__(self):
        self.perspectives: List[Perspective] = []

    def add_perspective(self, name: str, text: str) -> Perspective:
        """Add a named stakeholder perspective and extract key claims."""
        tokens = tokenize(text)
        sentences = [s.strip() for s in re.split(r'[.!?\n]+', text) if len(s.strip()) > 15]

        # Extract top claims (first 3 substantial sentences)
        claims = sentences[:3] if sentences else [text[:80]]

        # Extract core values from top token frequencies
        counts = Counter(tokens)
        top_terms = [word for word, _ in counts.most_common(4)]

        p = Perspective(
            name=name,
            raw_text=text,
            tokens=tokens,
            key_claims=claims,
            core_values=top_terms
        )
        self.perspectives.append(p)
        return p

    def analyze_dialectic(self) -> DialecticMatrixResult:
        """Analyze tensions, detect false divergences, and synthesize resolutions."""
        if len(self.perspectives) < 2:
            return DialecticMatrixResult(
                perspectives=self.perspectives,
                tensions=[],
                syntheses=[],
                consensus_readiness_index=100.0,
                shared_vocabulary_pct=100.0,
                total_false_divergences=0
            )

        tensions: List[DialecticTension] = []
        syntheses: List[DialecticSynthesis] = []
        total_pairs = 0
        false_divergences = 0

        p1 = self.perspectives[0]
        p2 = self.perspectives[1]

        # Compute token overlap (shared vocabulary)
        set1 = set(p1.tokens)
        set2 = set(p2.tokens)
        union_set = set1 | set2
        shared_tokens = set1 & set2
        shared_vocab_pct = round((len(shared_tokens) / max(len(union_set), 1)) * 100, 1)

        # Pairwise claim analysis
        for idx_a, claim_a in enumerate(p1.key_claims):
            if idx_a < len(p2.key_claims):
                claim_b = p2.key_claims[idx_a]
            else:
                claim_b = p2.key_claims[-1]

            total_pairs += 1
            tokens_a = set(tokenize(claim_a))
            tokens_b = set(tokenize(claim_b))

            # Check if claims map to an underlying concept cluster (false divergence check)
            shared_cluster_concept = None
            for concept_name, cluster in CONCEPT_CLUSTERS:
                in_a = bool(tokens_a & cluster)
                in_b = bool(tokens_b & cluster)
                if in_a and in_b:
                    shared_cluster_concept = concept_name
                    break

            is_false = (shared_cluster_concept is not None) or (len(tokens_a & tokens_b) >= 2)
            if is_false:
                false_divergences += 1
                polarity = 0.25
                topic = shared_cluster_concept or "Shared Priority"
            else:
                polarity = 0.75
                topic = f"Constraint Trade-Off {total_pairs}"

            tension = DialecticTension(
                perspective_a=p1.name,
                perspective_b=p2.name,
                topic=topic,
                claim_a=claim_a,
                claim_b=claim_b,
                is_false_divergence=is_false,
                shared_concept=shared_cluster_concept,
                polarity_weight=polarity
            )
            tensions.append(tension)

            # Generate synthesis resolving tension
            if is_false:
                synth_title = f"Unified {topic} Architecture"
                synth_desc = (
                    f"Both {p1.name} and {p2.name} converge on {topic}. "
                    f"Align definitions and integrate {p1.name}'s execution strategy with {p2.name}'s standards."
                )
                c_score = 90.0
            else:
                synth_title = f"Layered {topic} Compromise"
                synth_desc = (
                    f"Decouple {p1.name}'s priority into the primary workflow while guaranteeing {p2.name}'s constraints "
                    f"through automated safety checks and modular stage-gates."
                )
                c_score = 75.0

            syntheses.append(DialecticSynthesis(
                title=synth_title,
                description=synth_desc,
                tension_resolved=topic,
                integrates_from_a=p1.core_values[0] if p1.core_values else "Core Claim",
                integrates_from_b=p2.core_values[0] if p2.core_values else "Counter Claim",
                consensus_score=c_score
            ))

        # Consensus Readiness Index (0 to 100%):
        # Higher if shared vocabulary is high and false divergences are high (meaning agreement exists beneath surface words)
        cri = round(min(100.0, max(20.0, (shared_vocab_pct * 0.4) + ((false_divergences / max(total_pairs, 1)) * 60.0))), 1)

        return DialecticMatrixResult(
            perspectives=self.perspectives,
            tensions=tensions,
            syntheses=syntheses,
            consensus_readiness_index=cri,
            shared_vocabulary_pct=shared_vocab_pct,
            total_false_divergences=false_divergences
        )

    def export_canvas(self, result: DialecticMatrixResult) -> Dict[str, Any]:
        """
        Generate Obsidian .canvas JSON graph representing the dialectic matrix.
        Columns:
        Col 0: Perspective A (Thesis)
        Col 1: Tension Anchor Nodes
        Col 2: Perspective B (Antithesis)
        Col 3: Higher-Order Synthesis
        """
        nodes = []
        edges = []

        if len(result.perspectives) < 2:
            return {"nodes": nodes, "edges": edges}

        p_a = result.perspectives[0]
        p_b = result.perspectives[1]

        # Top Header Nodes
        nodes.append({
            "id": "header_thesis",
            "type": "text",
            "text": f"### [THESIS]\n**Perspective:** `{p_a.name}`\nValues: {', '.join(p_a.core_values)}",
            "x": 0,
            "y": 0,
            "width": 300,
            "height": 140,
            "color": "2"  # Orange
        })
        nodes.append({
            "id": "header_antithesis",
            "type": "text",
            "text": f"### [ANTITHESIS]\n**Perspective:** `{p_b.name}`\nValues: {', '.join(p_b.core_values)}",
            "x": 400,
            "y": 0,
            "width": 300,
            "height": 140,
            "color": "1"  # Red
        })
        nodes.append({
            "id": "header_synthesis",
            "type": "text",
            "text": f"### [SYNTHESIS]\n**Consensus Readiness:** `{result.consensus_readiness_index}%`\nUnified Integrations",
            "x": 800,
            "y": 0,
            "width": 320,
            "height": 140,
            "color": "4"  # Green
        })

        # Tension and Synthesis Rows
        for idx, (tension, synth) in enumerate(zip(result.tensions, result.syntheses), 1):
            y_pos = idx * 220

            t_type = "False Divergence (Semantic Match)" if tension.is_false_divergence else "Structural Polarity"
            t_color = "5" if tension.is_false_divergence else "3"

            # Node A Claim
            nid_a = f"node_claim_a_{idx}"
            nodes.append({
                "id": nid_a,
                "type": "text",
                "text": f"**{p_a.name} Claim:**\n> {tension.claim_a}",
                "x": 0,
                "y": y_pos,
                "width": 300,
                "height": 180,
                "color": "2"
            })

            # Node B Claim
            nid_b = f"node_claim_b_{idx}"
            nodes.append({
                "id": nid_b,
                "type": "text",
                "text": f"**{p_b.name} Claim:**\n> {tension.claim_b}",
                "x": 400,
                "y": y_pos,
                "width": 300,
                "height": 180,
                "color": "1"
            })

            # Synthesis Node
            nid_s = f"node_synth_{idx}"
            nodes.append({
                "id": nid_s,
                "type": "text",
                "text": (
                    f"### {synth.title}\n"
                    f"**Topic:** {tension.topic} ({t_type})\n\n"
                    f"{synth.description}\n\n"
                    f"**Consensus:** {int(synth.consensus_score)}%"
                ),
                "x": 800,
                "y": y_pos,
                "width": 320,
                "height": 180,
                "color": "4"
            })

            # Connect A -> B (Tension Edge)
            edges.append({
                "id": f"edge_tension_{idx}",
                "fromNode": nid_a,
                "fromSide": "right",
                "toNode": nid_b,
                "toSide": "left",
                "color": t_color,
                "label": f"Tension: {tension.topic}"
            })

            # Connect B -> Synthesis Edge
            edges.append({
                "id": f"edge_synth_{idx}",
                "fromNode": nid_b,
                "fromSide": "right",
                "toNode": nid_s,
                "toSide": "left",
                "color": "4",
                "label": "Resolves into"
            })

        return {"nodes": nodes, "edges": edges}

    def export_svg(self, result: DialecticMatrixResult, width: int = 1000, height: int = 650) -> str:
        """Generate a vector SVG visual diagram of the dialectic consensus matrix."""
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            f'  <rect width="{width}" height="{height}" fill="#09090b" rx="16" />',
            f'  <!-- Header Banner -->',
            f'  <text x="30" y="40" fill="#ffffff" font-size="16" font-weight="700" font-family="sans-serif">Multi-Perspective Dialectic Consensus Matrix</text>',
            f'  <text x="30" y="60" fill="#a1a1aa" font-size="11" font-family="sans-serif">Consensus Readiness: {result.consensus_readiness_index}% | False Divergences: {result.total_false_divergences}</text>',
            f'  <!-- Tripartite Columns -->',
        ]

        if len(result.perspectives) >= 2:
            p_a = result.perspectives[0]
            p_b = result.perspectives[1]

            # Column 1: Thesis
            svg_lines.append(f'  <rect x="40" y="90" width="280" height="500" rx="12" fill="#18181b" stroke="#f97316" stroke-width="1.5" />')
            svg_lines.append(f'  <text x="60" y="125" fill="#f97316" font-size="14" font-weight="700" font-family="sans-serif">THESIS: {p_a.name}</text>')

            # Column 2: Antithesis
            svg_lines.append(f'  <rect x="360" y="90" width="280" height="500" rx="12" fill="#18181b" stroke="#ef4444" stroke-width="1.5" />')
            svg_lines.append(f'  <text x="380" y="125" fill="#ef4444" font-size="14" font-weight="700" font-family="sans-serif">ANTITHESIS: {p_b.name}</text>')

            # Column 3: Synthesis
            svg_lines.append(f'  <rect x="680" y="90" width="280" height="500" rx="12" fill="#18181b" stroke="#10b981" stroke-width="1.5" />')
            svg_lines.append(f'  <text x="700" y="125" fill="#10b981" font-size="14" font-weight="700" font-family="sans-serif">SYNTHESIS: Consensus</text>')

            # Rows of synthesis items
            for idx, synth in enumerate(result.syntheses[:2]):
                y_box = 160 + (idx * 210)

                # Thesis card
                safe_claim_a = result.tensions[idx].claim_a[:36].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                svg_lines.append(f'  <rect x="60" y="{y_box}" width="240" height="90" rx="8" fill="#27272a" />')
                svg_lines.append(f'  <text x="74" y="{y_box + 26}" fill="#f4f4f5" font-size="11" font-weight="600" font-family="sans-serif">{safe_claim_a}...</text>')

                # Antithesis card
                safe_claim_b = result.tensions[idx].claim_b[:36].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                svg_lines.append(f'  <rect x="380" y="{y_box}" width="240" height="90" rx="8" fill="#27272a" />')
                svg_lines.append(f'  <text x="394" y="{y_box + 26}" fill="#f4f4f5" font-size="11" font-weight="600" font-family="sans-serif">{safe_claim_b}...</text>')

                # Tension connection line
                svg_lines.append(f'  <line x1="300" y1="{y_box + 45}" x2="380" y2="{y_box + 45}" stroke="#eab308" stroke-width="2" stroke-dasharray="4 4" />')

                # Synthesis card
                safe_title = synth.title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                svg_lines.append(f'  <rect x="700" y="{y_box}" width="240" height="90" rx="8" fill="#064e3b" stroke="#10b981" stroke-width="1.5" />')
                svg_lines.append(f'  <text x="714" y="{y_box + 26}" fill="#34d399" font-size="12" font-weight="700" font-family="sans-serif">{safe_title}</text>')
                svg_lines.append(f'  <text x="714" y="{y_box + 46}" fill="#a7f3d0" font-size="10" font-family="sans-serif">Consensus: {int(synth.consensus_score)}%</text>')

                # Synthesis resolution line
                svg_lines.append(f'  <line x1="620" y1="{y_box + 45}" x2="700" y2="{y_box + 45}" stroke="#10b981" stroke-width="2" />')

        svg_lines.append('</svg>')
        return "\n".join(svg_lines)

    @classmethod
    def export_summary(cls, result: DialecticMatrixResult) -> str:
        """Generate markdown summary table of dialectic analysis."""
        lines = [
            f"# Multi-Perspective Dialectic Consensus Matrix",
            f"",
            f"**Consensus Readiness Index:** `{result.consensus_readiness_index}%`",
            f"**Shared Vocabulary Overlap:** `{result.shared_vocabulary_pct}%`",
            f"**False Divergences Detected:** `{result.total_false_divergences}`",
            f"",
            f"## Dialectic Tensions & Resolutions",
            f"",
            f"| Topic | Classification | Thesis vs Antithesis | Higher-Order Synthesis | Consensus |",
            f"| :--- | :--- | :--- | :--- | :--- |"
        ]

        for t, s in zip(result.tensions, result.syntheses):
            t_class = "False Divergence" if t.is_false_divergence else "Structural Polarity"
            lines.append(
                f"| **{t.topic}** | `{t_class}` | "
                f"`{t.claim_a[:35]}...` vs `{t.claim_b[:35]}...` | "
                f"**{s.title}** | **{int(s.consensus_score)}%** |"
            )

        return "\n".join(lines)


def main():
    """Quick CLI runner."""
    print("DialecticMatrixEngine Loaded.")


if __name__ == "__main__":
    main()
