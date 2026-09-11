"""
Autonomous Cognitive Spatial Multimodal Phonological Loop Bridge & Grapheme Resonator
=====================================================================================
Theoretical Framework:
- Baddeley Working Memory Model: The phonological loop bottlenecks when decoding
  dense, irregular, multi-syllabic technical terminology.
- Grapheme-to-Phoneme Dissonance: Quantifies orthographic complexity, consonant clusters,
  and phonetic friction that induce sub-vocal stalling in dyslexic readers.
- Multi-Sensory Spatial Resonance: Decomposes complex terms into syllabic pacing
  blocks with visual stress anchors to bypass auditory loop exhaustion.
- Strictly NO em dashes (\u2014) anywhere in code, docstrings, or outputs.
"""

import re
import math
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class GraphemeToken:
    """An analyzed term evaluated for phonological loop friction."""
    term: str
    syllables: List[str]
    syllable_count: int
    friction_score: float  # 0.0 to 1.0
    dissonance_level: str  # low, moderate, high, critical
    phonetic_guide: str
    rhythm_pacing_ms: int

@dataclass
class PhonologicalBridgeTelemetry:
    """Telemetry measuring phonological strain and sub-vocalization pacing."""
    total_tokens: int
    high_friction_tokens: int
    mean_friction_score: float
    phonological_load_index: float
    recommended_pacing_wpm: float
    bottleneck_mitigation_score: float

@dataclass
class PhonologicalBridgeResult:
    """Result containing grapheme tokens, telemetry, SVG map, and audit report."""
    tokens: List[GraphemeToken]
    telemetry: PhonologicalBridgeTelemetry
    resonance_map_svg: str
    audit_report_md: str

    def to_dict(self) -> Dict[str, Any]:
        import dataclasses
        return {
            "tokens": [dataclasses.asdict(t) for t in self.tokens],
            "telemetry": dataclasses.asdict(self.telemetry)
        }

class PhonologicalLoopBridge:
    """
    Detects grapheme-to-phoneme dissonance across prose, decomposes multi-syllabic
    friction nodes into spatial syllables, and synthesizes rhythmic pacing anchors.
    """

    VOWELS = set("aeiouyAEIOUY")

    # Irregular consonant combinations and friction blends
    COMPLEX_CLUSTERS = [
        "str", "spl", "scr", "phth", "sch", "ght", "ngth", "rph",
        "tmn", "ps", "pn", "gn", "rrh", "thm", "xth", "ct", "pt"
    ]

    def __init__(self, high_friction_threshold: float = 0.55):
        self.high_friction_threshold = high_friction_threshold

    def decompose_syllables(self, word: str) -> List[str]:
        """Heuristic rule-based syllabification for English technical terms."""
        clean = re.sub(r'[^A-Za-z]', '', word)
        if len(clean) <= 3:
            return [clean] if clean else [word]

        # Simple vowel-consonant boundary split
        parts = []
        curr = ""
        vowel_seen = False

        for char in clean:
            curr += char
            is_v = char in self.VOWELS
            if is_v:
                vowel_seen = True
            elif vowel_seen and len(curr) >= 3:
                parts.append(curr)
                curr = ""
                vowel_seen = False

        if curr:
            if parts:
                parts[-1] += curr
            else:
                parts.append(curr)

        return parts if parts else [clean]

    def compute_friction_score(self, word: str) -> float:
        """Calculates phonetic friction based on syllabic count, cluster density, and length."""
        w_lower = word.lower()
        clean = re.sub(r'[^a-z]', '', w_lower)
        if not clean or len(clean) <= 2:
            return 0.10

        syllables = self.decompose_syllables(clean)
        s_count = len(syllables)

        # Base friction from syllable count (1: 0.1, 4+: 0.6)
        syllable_factor = min(1.0, s_count * 0.15)

        # Length factor normalized around 12 characters
        length_factor = min(1.0, len(clean) / 12.0)

        # Cluster friction
        cluster_bonus = 0.0
        for cluster in self.COMPLEX_CLUSTERS:
            if cluster in clean:
                cluster_bonus += 0.20

        raw_score = 0.40 * syllable_factor + 0.35 * length_factor + min(0.35, cluster_bonus)
        return round(min(1.0, max(0.05, raw_score)), 3)

    def evaluate_text(self, text: str) -> PhonologicalBridgeResult:
        """Evaluates prose for phonological friction and generates multi-sensory anchors."""
        raw_words = re.findall(r'\b[A-Za-z-]{3,}\b', text)
        if not raw_words:
            telemetry = PhonologicalBridgeTelemetry(
                total_tokens=0,
                high_friction_tokens=0,
                mean_friction_score=0.0,
                phonological_load_index=0.0,
                recommended_pacing_wpm=220.0,
                bottleneck_mitigation_score=1.0
            )
            return PhonologicalBridgeResult(
                tokens=[],
                telemetry=telemetry,
                resonance_map_svg="<svg width='800' height='450'></svg>",
                audit_report_md="# Phonological Bridge Report\n\nEmpty input text provided."
            )

        tokens: List[GraphemeToken] = []
        seen_words = set()
        friction_sum = 0.0

        for w in raw_words:
            w_lower = w.lower()
            if w_lower in seen_words:
                continue
            seen_words.add(w_lower)

            friction = self.compute_friction_score(w)
            friction_sum += friction

            syllables = self.decompose_syllables(w)
            s_count = len(syllables)

            if friction >= 0.70:
                dissonance = "critical"
            elif friction >= self.high_friction_threshold:
                dissonance = "high"
            elif friction >= 0.35:
                dissonance = "moderate"
            else:
                dissonance = "low"

            phonetic_guide = "·".join(s.upper() if idx == 0 else s.lower() for idx, s in enumerate(syllables))
            pacing_ms = int(120 + friction * 350)

            tokens.append(GraphemeToken(
                term=w,
                syllables=syllables,
                syllable_count=s_count,
                friction_score=friction,
                dissonance_level=dissonance,
                phonetic_guide=phonetic_guide,
                rhythm_pacing_ms=pacing_ms
            ))

        # Sort tokens by friction descending
        tokens.sort(key=lambda t: t.friction_score, reverse=True)

        total_cnt = len(tokens)
        high_friction_cnt = sum(1 for t in tokens if t.friction_score >= self.high_friction_threshold)
        mean_friction = round(friction_sum / max(1, total_cnt), 3)

        # Phonological load index (0 to 100)
        load_index = round(mean_friction * 100.0 * (1.0 + (high_friction_cnt / max(1, total_cnt))), 1)
        recommended_wpm = round(max(100.0, 240.0 - mean_friction * 120.0), 1)
        mitigation_score = round(min(1.0, 1.0 - (high_friction_cnt / max(1, total_cnt * 2))), 3)

        telemetry = PhonologicalBridgeTelemetry(
            total_tokens=total_cnt,
            high_friction_tokens=high_friction_cnt,
            mean_friction_score=mean_friction,
            phonological_load_index=load_index,
            recommended_pacing_wpm=recommended_wpm,
            bottleneck_mitigation_score=mitigation_score
        )

        svg = self.generate_svg(tokens, telemetry)
        md = self.generate_markdown_report(tokens, telemetry)

        return PhonologicalBridgeResult(
            tokens=tokens,
            telemetry=telemetry,
            resonance_map_svg=svg,
            audit_report_md=md
        )

    def generate_svg(
        self,
        tokens: List[GraphemeToken],
        telemetry: PhonologicalBridgeTelemetry,
        width: int = 800,
        height: int = 450
    ) -> str:
        """Renders a dark titanium SVG displaying syllabic decomposition and rhythm badges."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            '<defs>',
            '  <linearGradient id="titaniumPhonoBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#151922" />',
            '    <stop offset="100%" stop-color="#0a0d12" />',
            '  </linearGradient>',
            '</defs>',
            f'<rect width="{width}" height="{height}" rx="12" fill="url(#titaniumPhonoBg)" stroke="#30363d" stroke-width="1.5" />',
            '<!-- Header -->',
            '<text x="24" y="36" fill="#58a6ff" font-family="sans-serif" font-size="16" font-weight="bold">Multimodal Phonological Loop Bridge &amp; Grapheme Resonator</text>',
            f'<text x="{width - 24}" y="36" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="end">Pacing: {telemetry.recommended_pacing_wpm} WPM | Friction Load: {telemetry.phonological_load_index}</text>',
            f'<line x1="24" y1="48" x2="{width - 24}" y2="48" stroke="#30363d" stroke-width="1" />'
        ]

        # Display top 5 high-friction tokens
        y_pos = 75
        block_height = 55
        for t in tokens[:5]:
            border_color = "#f85149" if t.dissonance_level in ("critical", "high") else ("#d29922" if t.dissonance_level == "moderate" else "#58a6ff")
            badge_color = "#f85149" if t.dissonance_level == "critical" else ("#ffa657" if t.dissonance_level == "high" else "#7ee787")

            svg_parts.append(f'<g transform="translate(24, {y_pos})">')
            svg_parts.append(f'  <rect width="{width - 48}" height="{block_height}" rx="8" fill="#161b22" stroke="{border_color}" stroke-width="1.2" />')
            escaped_term = t.term.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg_parts.append(f'  <text x="16" y="24" fill="#f0f6fc" font-family="sans-serif" font-size="14" font-weight="bold">{escaped_term}</text>')
            escaped_guide = t.phonetic_guide.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg_parts.append(f'  <text x="16" y="44" fill="#8b949e" font-family="sans-serif" font-size="11">Syllables: <tspan fill="#58a6ff" font-weight="bold">{escaped_guide}</tspan></text>')

            # Friction meter bar
            bar_w = 140
            bar_fill = int(bar_w * t.friction_score)
            svg_parts.append(f'  <rect x="{width - 240}" y="18" width="{bar_w}" height="12" rx="4" fill="#21262d" />')
            svg_parts.append(f'  <rect x="{width - 240}" y="18" width="{bar_fill}" height="12" rx="4" fill="{badge_color}" />')
            svg_parts.append(f'  <text x="{width - 90}" y="28" fill="{badge_color}" font-family="sans-serif" font-size="11" font-weight="bold">Friction {t.friction_score:.2f}</text>')
            svg_parts.append(f'  <text x="{width - 90}" y="44" fill="#8b949e" font-family="sans-serif" font-size="10">Dwell: {t.rhythm_pacing_ms}ms</text>')
            svg_parts.append('</g>')

            y_pos += block_height + 12

        # Footer
        svg_parts.append(f'<line x1="24" y1="{height - 35}" x2="{width - 24}" y2="{height - 35}" stroke="#30363d" stroke-width="1" />')
        svg_parts.append(f'<text x="24" y="{height - 15}" fill="#8b949e" font-family="sans-serif" font-size="11">Total Evaluated Terms: {telemetry.total_tokens} | High Friction: {telemetry.high_friction_tokens} | Mean Friction: {telemetry.mean_friction_score:.2f}</text>')
        svg_parts.append(f'<text x="{width - 24}" y="{height - 15}" fill="#7ee787" font-family="sans-serif" font-size="11" text-anchor="end">Mitigation Efficiency: {telemetry.bottleneck_mitigation_score * 100:.1f}%</text>')
        svg_parts.append('</svg>')

        return "\n".join(svg_parts)

    def generate_markdown_report(
        self,
        tokens: List[GraphemeToken],
        telemetry: PhonologicalBridgeTelemetry
    ) -> str:
        """Generates an audit report with strictly zero em dashes."""
        lines = [
            "# Phonological Loop Bridge & Grapheme Resonator Report",
            "",
            "## Cognitive Phonological Metrics",
            f"- **Analyzed Vocabulary Tokens:** {telemetry.total_tokens}",
            f"- **High-Friction Terms:** {telemetry.high_friction_tokens}",
            f"- **Mean Phonetic Friction Score:** {telemetry.mean_friction_score:.3f}",
            f"- **Phonological Load Index:** {telemetry.phonological_load_index:.1f}",
            f"- **Recommended Pacing Velocity:** {telemetry.recommended_pacing_wpm:.1f} WPM",
            f"- **Sub-Vocal Mitigation Score:** {telemetry.bottleneck_mitigation_score * 100:.1f}%",
            "",
            "## Grapheme Friction Classification",
            "",
            "| Term | Syllables | Friction Score | Dissonance Level | Phonetic Guide | Pacing (ms) |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for t in tokens:
            lines.append(f"| **{t.term}** | {t.syllable_count} | {t.friction_score:.2f} | {t.dissonance_level.upper()} | `{t.phonetic_guide}` | {t.rhythm_pacing_ms} |")

        lines.extend([
            "",
            "## Theoretical Grounding",
            "- **Baddeley Working Memory Model:** Prevents phonological loop exhaustion by chunking complex terms into rhythmic syllables.",
            "- **Spatial Grapheme Anchoring:** Multi-sensory visual guides provide instantaneous recognition without silent sub-vocal stalling.",
            "- **Kinetic Pacing Calibration:** Adjusts reading velocity dynamically based on local linguistic friction coefficients.",
            ""
        ])

        return "\n".join(lines)
