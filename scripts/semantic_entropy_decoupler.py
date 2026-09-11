"""
Semantic Entropy Decoupler and Syntactic De-Noising Gate Engine
Autonomous cognitive spatial module calculating Shannon entropy, signal-to-noise ratio,
and syntactic noise attenuation across dense canvas notes. Isolates invariant semantic
core tokens from superficial decorative prose and hedging qualifiers to protect
working memory from lexical friction.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set, Optional, Any
import collections
import re
import math
import html


NOISE_STOPWORDS = {
    "it", "is", "a", "an", "the", "in", "on", "at", "by", "for", "with",
    "about", "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "to", "from", "up", "down", "in", "out",
    "over", "under", "again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
    "just", "don", "should", "now", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "would", "could", "might", "must", "shall"
}

HEDGING_PATTERNS = [
    r"\b(?:it appears that|it seems that|one might argue that|arguably)\b",
    r"\b(?:in order to|as a matter of fact|needless to say|it is worth noting that)\b",
    r"\b(?:with all due respect|generally speaking|to some extent|more or less)\b",
    r"\b(?:for all intents and purposes|at the end of the day|in the process of)\b",
]


@dataclass
class TextEntropyProfile:
    """Detailed entropy and SNR analysis of a text snippet or canvas node."""
    node_id: str
    title: str
    raw_text: str
    total_tokens: int
    unique_tokens: int
    shannon_entropy_bits: float
    syntactic_noise_ratio: float  # 0.0 to 1.0 (noise tokens / total)
    signal_to_noise_ratio_db: float  # SNR in dB
    core_semantic_tokens: List[str]
    attenuated_noise_tokens: List[str]
    de_noised_text: str


@dataclass
class ManifoldEntropyTelemetry:
    """Comprehensive telemetry report across a corpus of spatial nodes."""
    node_count: int
    mean_entropy_bits: float
    mean_snr_db: float
    mean_noise_ratio: float
    high_noise_nodes_count: int
    profiles: List[TextEntropyProfile] = field(default_factory=list)


class SemanticEntropyDecoupler:
    """
    Autonomous engine that computes information-theoretic entropy distributions
    and strips syntactic turbulence from conceptual nodes.
    """

    def __init__(self, snr_alert_threshold_db: float = 3.0):
        self.snr_alert_threshold_db = float(snr_alert_threshold_db)

    @staticmethod
    def calculate_shannon_entropy(tokens: List[str]) -> float:
        """Calculates Shannon entropy in bits for token frequency distribution."""
        if not tokens:
            return 0.0
        counts = collections.Counter(tokens)
        total = len(tokens)
        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0.0:
                entropy -= p * math.log2(p)
        return round(entropy, 3)

    def analyze_node(self, node_id: str, title: str, text: str) -> TextEntropyProfile:
        """Analyzes a single text node and produces a de-noised semantic representation."""
        cleaned_text = text.strip()
        if not cleaned_text:
            return TextEntropyProfile(
                node_id=node_id,
                title=title,
                raw_text="",
                total_tokens=0,
                unique_tokens=0,
                shannon_entropy_bits=0.0,
                syntactic_noise_ratio=0.0,
                signal_to_noise_ratio_db=0.0,
                core_semantic_tokens=[],
                attenuated_noise_tokens=[],
                de_noised_text="",
            )

        # Remove explicit hedging phrases
        de_hedged = cleaned_text
        for pat in HEDGING_PATTERNS:
            de_hedged = re.sub(pat, "", de_hedged, flags=re.IGNORECASE)
        de_hedged = re.sub(r"\s+", " ", de_hedged).strip()

        # Tokenize
        raw_tokens = [w.lower() for w in re.findall(r"[A-Za-z0-9_-]+", cleaned_text)]
        total_tokens = len(raw_tokens)
        unique_tokens = len(set(raw_tokens))
        entropy = self.calculate_shannon_entropy(raw_tokens)

        core_tokens: List[str] = []
        noise_tokens: List[str] = []

        for t in raw_tokens:
            if t in NOISE_STOPWORDS or len(t) <= 1:
                noise_tokens.append(t)
            else:
                core_tokens.append(t)

        core_count = len(core_tokens)
        noise_count = len(noise_tokens)

        noise_ratio = round(noise_count / max(1, total_tokens), 3)

        # Signal-to-noise ratio in decibels: 10 * log10(signal / noise)
        if noise_count == 0:
            snr_db = 20.0  # Cap clean text at 20 dB
        elif core_count == 0:
            snr_db = -10.0  # Cap pure noise at -10 dB
        else:
            snr_db = round(10.0 * math.log10(core_count / noise_count), 2)

        # De-noised concise summary
        unique_core = list(dict.fromkeys(core_tokens))
        de_noised = " ".join(unique_core[:12]).capitalize()
        if len(unique_core) > 12:
            de_noised += "..."

        return TextEntropyProfile(
            node_id=node_id,
            title=title,
            raw_text=cleaned_text,
            total_tokens=total_tokens,
            unique_tokens=unique_tokens,
            shannon_entropy_bits=entropy,
            syntactic_noise_ratio=noise_ratio,
            signal_to_noise_ratio_db=snr_db,
            core_semantic_tokens=unique_core,
            attenuated_noise_tokens=list(set(noise_tokens)),
            de_noised_text=de_noised,
        )

    def analyze_nodes(self, nodes: List[Dict[str, str]]) -> ManifoldEntropyTelemetry:
        """Analyzes a collection of nodes and generates aggregated manifold telemetry."""
        if not nodes:
            return ManifoldEntropyTelemetry(
                node_count=0,
                mean_entropy_bits=0.0,
                mean_snr_db=0.0,
                mean_noise_ratio=0.0,
                high_noise_nodes_count=0,
                profiles=[],
            )

        profiles: List[TextEntropyProfile] = []
        for n in nodes:
            nid = str(n.get("id", n.get("node_id", "node")))
            title = str(n.get("title", "Node"))
            text = str(n.get("text", n.get("content", "")))
            profiles.append(self.analyze_node(nid, title, text))

        node_count = len(profiles)
        mean_entropy = round(sum(p.shannon_entropy_bits for p in profiles) / node_count, 3)
        mean_snr = round(sum(p.signal_to_noise_ratio_db for p in profiles) / node_count, 2)
        mean_noise = round(sum(p.syntactic_noise_ratio for p in profiles) / node_count, 3)

        high_noise = len([p for p in profiles if p.signal_to_noise_ratio_db < self.snr_alert_threshold_db])

        return ManifoldEntropyTelemetry(
            node_count=node_count,
            mean_entropy_bits=mean_entropy,
            mean_snr_db=mean_snr,
            mean_noise_ratio=mean_noise,
            high_noise_nodes_count=high_noise,
            profiles=profiles,
        )

    def generate_markdown_report(self, telemetry: ManifoldEntropyTelemetry) -> str:
        """Generates structured markdown audit report with zero em dashes."""
        lines = [
            "# Semantic Entropy Decoupler and Syntactic De-Noising Report",
            "",
            "## 1. Information-Theoretic Manifold Overview",
            f"- **Analyzed Canvas Nodes:** {telemetry.node_count}",
            f"- **Mean Shannon Entropy:** {telemetry.mean_entropy_bits} bits/token",
            f"- **Mean Signal-to-Noise Ratio (SNR):** {telemetry.mean_snr_db} dB",
            f"- **Mean Syntactic Noise Ratio:** {int(telemetry.mean_noise_ratio * 100)}%",
            f"- **High-Noise Alerts (SNR < {self.snr_alert_threshold_db} dB):** {telemetry.high_noise_nodes_count} nodes",
            "",
            "## 2. Neuro-Cognitive Theoretical Grounding",
            "- **Shannon Information Entropy:** High token entropy with low semantic core indicates filler sprawl.",
            "- **Syntactic Friction Attenuation:** Stripping non-essential hedging lowers working memory cognitive drag.",
            "- **Invariant Semantic Crystallization:** Isolating substantive nouns, verbs, and constraints boosts retention.",
            "",
            "## 3. Node Entropy & Signal-to-Noise Catalog",
            "| Node ID | Title | Total Tokens | Entropy (bits) | Noise Ratio | SNR (dB) | De-Noised Semantic Core |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for p in telemetry.profiles:
            lines.append(
                f"| `{p.node_id}` | {p.title} | {p.total_tokens} | {p.shannon_entropy_bits} | {int(p.syntactic_noise_ratio * 100)}% | {p.signal_to_noise_ratio_db} dB | {p.de_noised_text} |"
            )

        lines.extend([
            "",
            "## 4. Operational Ergonomics Recommendations",
            "- Replace passive and hedging prose in nodes with SNR < 0 dB with active imperative verbs.",
            "- For nodes with high entropy (> 4.5 bits), decouple secondary clauses into child sub-nodes.",
            "- In high-pressure review modes, display the de-noised semantic core as primary card headers.",
        ])

        return "\n".join(lines)

    def generate_svg(
        self,
        telemetry: ManifoldEntropyTelemetry,
        width: int = 920,
        height: int = 560,
    ) -> str:
        """Generates publication-grade dark titanium entropy spectrum HUD SVG."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d18; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
            '<defs>',
            '  <linearGradient id="snrGrad" x1="0%" y1="100%" x2="0%" y2="0%">',
            '    <stop offset="0%" stop-color="#ef4444"/>',
            '    <stop offset="50%" stop-color="#eab308"/>',
            '    <stop offset="100%" stop-color="#22c55e"/>',
            '  </linearGradient>',
            '</defs>',
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#090d18"/>',
            '<!-- Background Grid -->',
        ]

        for gx in range(0, width, 50):
            svg_parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#1e293b" stroke-width="0.6" opacity="0.3"/>')
        for gy in range(0, height, 50):
            svg_parts.append(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#1e293b" stroke-width="0.6" opacity="0.3"/>')

        # Draw SNR Bar Chart
        bar_start_x = 60
        chart_w = width - 120
        chart_base_y = height - 100
        chart_top_y = 120
        chart_h = chart_base_y - chart_top_y

        n_profiles = len(telemetry.profiles)
        bar_w = min(80.0, max(24.0, (chart_w - (n_profiles * 15)) / max(1, n_profiles)))

        # Baseline 0 dB line
        zero_db_y = chart_base_y - (chart_h * 0.4)
        svg_parts.append(
            f'<line x1="{bar_start_x - 10}" y1="{zero_db_y}" x2="{width - 50}" y2="{zero_db_y}" stroke="#475569" stroke-width="1.2" stroke-dasharray="4,4"/>'
        )
        svg_parts.append(
            f'<text x="{bar_start_x - 14}" y="{zero_db_y + 4}" font-size="9" fill="#94a3b8" text-anchor="end">0 dB</text>'
        )

        for i, p in enumerate(telemetry.profiles):
            bx = bar_start_x + i * (bar_w + 24)
            # Map snr from -5 dB .. 15 dB to height
            clamped_snr = max(-5.0, min(15.0, p.signal_to_noise_ratio_db))
            bar_pct = (clamped_snr + 5.0) / 20.0
            bh = chart_h * bar_pct
            by = chart_base_y - bh

            fill_c = "#22c55e" if p.signal_to_noise_ratio_db >= 3.0 else ("#eab308" if p.signal_to_noise_ratio_db >= 0.0 else "#ef4444")

            svg_parts.append(
                f'<rect x="{bx}" y="{by}" width="{bar_w}" height="{bh}" rx="4" fill="{fill_c}" fill-opacity="0.85" stroke="{fill_c}" stroke-width="1.5"/>'
            )
            svg_parts.append(
                f'<text x="{bx + bar_w / 2}" y="{by - 8}" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">{p.signal_to_noise_ratio_db} dB</text>'
            )
            svg_parts.append(
                f'<text x="{bx + bar_w / 2}" y="{chart_base_y + 18}" font-size="9" font-weight="600" fill="#cbd5e1" text-anchor="middle">{html.escape(p.title[:10])}</text>'
            )
            svg_parts.append(
                f'<text x="{bx + bar_w / 2}" y="{chart_base_y + 30}" font-size="7.5" fill="#94a3b8" text-anchor="middle">H={p.shannon_entropy_bits}</text>'
            )

        # HUD Box
        svg_parts.append(
            f'<rect x="20" y="20" width="390" height="74" rx="8" fill="#0f172a" fill-opacity="0.9" stroke="#38bdf8" stroke-width="1.2"/>'
        )
        svg_parts.append(
            '<text x="32" y="38" font-size="11" font-weight="700" fill="#38bdf8">SEMANTIC ENTROPY DECOUPLER HUD</text>'
        )
        svg_parts.append(
            f'<text x="32" y="54" font-size="9" fill="#94a3b8">Nodes: {telemetry.node_count} | Mean Entropy: {telemetry.mean_entropy_bits} bits | Mean SNR: {telemetry.mean_snr_db} dB</text>'
        )
        svg_parts.append(
            f'<text x="32" y="70" font-size="9" fill="#94a3b8">Mean Noise: {int(telemetry.mean_noise_ratio * 100)}% | High-Noise Warnings: {telemetry.high_noise_nodes_count}</text>'
        )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def sample_noisy_nodes() -> List[Dict[str, str]]:
    """Generates demonstration text nodes with varying syntactic noise levels."""
    return [
        {
            "id": "node-1",
            "title": "Clean Core",
            "text": "Database pool balances transactional queries across replica clusters under strict latency SLA.",
        },
        {
            "id": "node-2",
            "title": "Hedging Sprawl",
            "text": "It seems that arguably in order to achieve consistency it might perhaps be useful to consider replication.",
        },
        {
            "id": "node-3",
            "title": "Dense Technical",
            "text": "Asymmetric cryptography validates digital signatures using elliptic curve discrete logarithms.",
        },
        {
            "id": "node-4",
            "title": "Procedural Filler",
            "text": "Needless to say for all intents and purposes we are in the process of ensuring that the cache is ready.",
        },
    ]
