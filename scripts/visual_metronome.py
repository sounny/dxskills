"""Autonomous Cognitive Spatial Visual Pacing Rhythm & Bionic Fixation Metronome.

Theoretical Foundation:
- Rayner & Pollatsek Eye Movements & Fixation Duration Model:
  Foveal fixations expand from 200ms to 350-500ms on polysyllabic, low-frequency,
  or phonologically ambiguous tokens. Uncalibrated saccades cause lexical lookup
  stalls and regressive eye movements.
- Optimal Viewing Position (OVP):
  Lexical recognition speed is maximized when ocular fixation lands at or slightly
  to the left of the center of a word (characters 2-3).
- Syllable Duration Modulation:
  Computes phonological complexity per token to pace cognitive dwell times,
  synthesizing rhythmic cadence that stabilizes dyslexic reading flows.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import enum
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class PacingMode(str, enum.Enum):
    """Pacing rhythm modes for visual lexical guidance."""

    ISOCHRONIC = "isochronic"
    SYLLABLE_ADAPTIVE = "syllable_adaptive"
    MORPHOLOGICAL = "morphological"
    ACCELERATIVE = "accelerative"


@dataclass
class LexicalAnchor:
    """Individual word token with bionic fixation anchor and ocular pacing telemetry."""

    word: str
    clean_word: str
    syllable_count: int
    ovp_index: int
    formatted_token: str
    complexity_score: float
    dwell_ms: float
    timestamp_ms: float


@dataclass
class MetronomeTelemetry:
    """Telemetry report quantifying visual pacing rhythm and fixation cadence."""

    total_words: int
    total_syllables: int
    avg_dwell_ms: float
    total_duration_sec: float
    effective_wpm: float
    pacing_mode: str
    rhythm_regularity_score: float
    anchors: List[LexicalAnchor] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_words": self.total_words,
            "total_syllables": self.total_syllables,
            "avg_dwell_ms": round(self.avg_dwell_ms, 2),
            "total_duration_sec": round(self.total_duration_sec, 2),
            "effective_wpm": round(self.effective_wpm, 1),
            "pacing_mode": self.pacing_mode,
            "rhythm_regularity_score": round(self.rhythm_regularity_score, 3),
            "anchors": [asdict(a) for a in self.anchors],
        }


class VisualPacingMetronome:
    """Synthesizes bionic lexical fixation anchors and adaptive ocular pacing cadence."""

    def __init__(
        self,
        base_wpm: float = 200.0,
        mode: PacingMode = PacingMode.SYLLABLE_ADAPTIVE,
        min_dwell_ms: float = 120.0,
        max_dwell_ms: float = 480.0,
    ) -> None:
        self.base_wpm = max(60.0, min(base_wpm, 600.0))
        self.mode = mode
        self.min_dwell_ms = min_dwell_ms
        self.max_dwell_ms = max_dwell_ms

    @staticmethod
    def estimate_syllables(word: str) -> int:
        """Estimate syllable count in a clean English word."""
        token = word.lower().strip()
        token = re.sub(r"[^a-z]", "", token)
        if not token:
            return 1

        if len(token) <= 3:
            return 1

        # Count vowel sequences
        vowel_runs = len(re.findall(r"[aeiouy]+", token))

        # Subtract silent trailing e (except le)
        if token.endswith("e") and not token.endswith("le") and len(token) > 2:
            if not re.search(r"[aeiouy]{2}e$", token):
                vowel_runs = max(1, vowel_runs - 1)

        # Handle endings like -ed, -es
        if token.endswith("ed") and not token.endswith("ted") and not token.endswith("ded"):
            vowel_runs = max(1, vowel_runs - 1)

        return max(1, vowel_runs)

    @staticmethod
    def calculate_ovp(word: str) -> int:
        """Calculate the Optimal Viewing Position (OVP) index for lexical recognition.

        Empirically located at roughly 30-35 percent into the word token.
        For words with 1-3 chars: index 0
        For words with 4-6 chars: index 1
        For words with 7-9 chars: index 2
        For words with 10+ chars: index 3
        """
        clean = re.sub(r"[^a-zA-Z]", "", word)
        length = len(clean)
        if length <= 3:
            return 0
        if length <= 6:
            return 1
        if length <= 9:
            return 2
        return 3

    @classmethod
    def format_bionic_anchor(cls, word: str) -> str:
        """Synthesize bionic fixation anchor marking the Optimal Viewing Position."""
        match = re.match(r"^([^a-zA-Z]*)([a-zA-Z]+)([^a-zA-Z]*)$", word)
        if not match:
            return word

        leading_punct, core, trailing_punct = match.groups()
        length = len(core)
        if length <= 1:
            bold_len = 1
        elif length <= 3:
            bold_len = 1
        elif length <= 6:
            bold_len = 2
        elif length <= 9:
            bold_len = 3
        else:
            bold_len = 4

        return f"{leading_punct}**{core[:bold_len]}**{core[bold_len:]}{trailing_punct}"

    def compute_word_complexity(self, word: str, syllables: int) -> float:
        """Compute relative lexical complexity score between 0.0 and 1.0."""
        clean = re.sub(r"[^a-zA-Z]", "", word).lower()
        length = len(clean)
        if length == 0:
            return 0.0

        length_factor = min(1.0, length / 12.0)
        syllable_factor = min(1.0, syllables / 5.0)

        # Phonotactic friction proxy: rare consonant clusters
        rare_clusters = ["ph", "th", "ch", "str", "scr", "spl", "thr", "ght", "psy", "rhythm"]
        cluster_bonus = 0.2 if any(c in clean for c in rare_clusters) else 0.0

        complexity = (0.45 * syllable_factor) + (0.35 * length_factor) + cluster_bonus
        return max(0.05, min(1.0, complexity))

    def synthesize_pacing_timeline(self, text: str) -> MetronomeTelemetry:
        """Generate a complete rhythmic visual pacing timeline for prose."""
        raw_words = text.split()
        if not raw_words:
            return MetronomeTelemetry(
                total_words=0,
                total_syllables=0,
                avg_dwell_ms=0.0,
                total_duration_sec=0.0,
                effective_wpm=self.base_wpm,
                pacing_mode=self.mode.value,
                rhythm_regularity_score=1.0,
                anchors=[],
            )

        base_interval_ms = (60.0 / self.base_wpm) * 1000.0
        anchors: List[LexicalAnchor] = []
        cumulative_time_ms = 0.0
        total_syllables = 0
        dwell_times: List[float] = []

        total_word_count = len(raw_words)

        for idx, raw in enumerate(raw_words):
            clean = re.sub(r"[^a-zA-Z0-9]", "", raw)
            syllables = self.estimate_syllables(clean)
            total_syllables += syllables
            ovp = self.calculate_ovp(raw)
            formatted = self.format_bionic_anchor(raw)
            complexity = self.compute_word_complexity(raw, syllables)

            if self.mode == PacingMode.ISOCHRONIC:
                dwell = base_interval_ms
            elif self.mode == PacingMode.SYLLABLE_ADAPTIVE:
                # Modulate dwell by syllable count relative to average English (1.4 syllables)
                ratio = syllables / 1.4
                raw_dwell = base_interval_ms * (0.65 + 0.35 * ratio)
                dwell = max(self.min_dwell_ms, min(self.max_dwell_ms, raw_dwell))
            elif self.mode == PacingMode.MORPHOLOGICAL:
                # Heavily weight complex and multisyllabic terms
                dwell_mult = 0.7 + (complexity * 0.8)
                dwell = max(self.min_dwell_ms, min(self.max_dwell_ms, base_interval_ms * dwell_mult))
            elif self.mode == PacingMode.ACCELERATIVE:
                # Gradually ramp speed from 85 percent to 115 percent of base
                progress = idx / max(1, total_word_count - 1)
                speed_scale = 0.85 + (0.30 * progress)
                scaled_base = base_interval_ms / speed_scale
                ratio = syllables / 1.4
                dwell = max(self.min_dwell_ms, min(self.max_dwell_ms, scaled_base * (0.7 + 0.3 * ratio)))
            else:
                dwell = base_interval_ms

            dwell_times.append(dwell)
            anchors.append(
                LexicalAnchor(
                    word=raw,
                    clean_word=clean,
                    syllable_count=syllables,
                    ovp_index=ovp,
                    formatted_token=formatted,
                    complexity_score=round(complexity, 3),
                    dwell_ms=round(dwell, 1),
                    timestamp_ms=round(cumulative_time_ms, 1),
                )
            )
            cumulative_time_ms += dwell

        avg_dwell = sum(dwell_times) / len(dwell_times) if dwell_times else 0.0
        total_duration_sec = cumulative_time_ms / 1000.0
        effective_wpm = (total_word_count / total_duration_sec * 60.0) if total_duration_sec > 0 else self.base_wpm

        # Calculate rhythm regularity score (1.0 = steady isochronic, 0.0 = extreme variance)
        if len(dwell_times) > 1 and avg_dwell > 0:
            variance = sum((d - avg_dwell) ** 2 for d in dwell_times) / len(dwell_times)
            cv = math.sqrt(variance) / avg_dwell  # coefficient of variation
            regularity = max(0.1, min(1.0, 1.0 - (cv * 0.8)))
        else:
            regularity = 1.0

        return MetronomeTelemetry(
            total_words=total_word_count,
            total_syllables=total_syllables,
            avg_dwell_ms=avg_dwell,
            total_duration_sec=total_duration_sec,
            effective_wpm=effective_wpm,
            pacing_mode=self.mode.value,
            rhythm_regularity_score=regularity,
            anchors=anchors,
        )

    @staticmethod
    def render_ascii_cadence(telemetry: MetronomeTelemetry, max_words: int = 15) -> str:
        """Render a clean ASCII visual pacing chart safe for all terminals."""
        lines: List[str] = []
        lines.append("=== DxSkills Visual Pacing Rhythm & Fixation Metronome ===")
        lines.append(
            f"Mode: {telemetry.pacing_mode.upper()} | Words: {telemetry.total_words} | "
            f"Target WPM: {telemetry.effective_wpm:.1f} | Duration: {telemetry.total_duration_sec:.2f}s"
        )
        lines.append(f"Cadence Regularity: {telemetry.rhythm_regularity_score * 100:.1f}% | Avg Dwell: {telemetry.avg_dwell_ms:.1f}ms")
        lines.append("-" * 62)
        lines.append(f"{'Token':<18} {'Syll':<5} {'Dwell':<9} {'Timeline':<12} {'Fixation Bar'}")
        lines.append("-" * 62)

        slice_anchors = telemetry.anchors[:max_words]
        for anchor in slice_anchors:
            bar_len = int(round(anchor.dwell_ms / 20.0))
            bar_str = "=" * min(22, max(2, bar_len))
            sec_mark = f"{anchor.timestamp_ms / 1000.0:.2f}s"
            clean_display = anchor.clean_word[:16]
            lines.append(f"{clean_display:<18} {anchor.syllable_count:<5} {anchor.dwell_ms:>5.0f}ms   {sec_mark:<12} [{bar_str}]")

        if len(telemetry.anchors) > max_words:
            remaining = len(telemetry.anchors) - max_words
            lines.append(f"... ({remaining} additional paced lexical tokens queued)")

        lines.append("-" * 62)
        return "\n".join(lines)

    @staticmethod
    def export_canvas(telemetry: MetronomeTelemetry, filepath: str | Path) -> Path:
        """Export visual pacing metronome sequence to Obsidian Canvas (.canvas) JSON."""
        target = Path(filepath)
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []

        # Header node
        header_text = (
            f"## Visual Pacing Metronome Cadence\n\n"
            f"- **Mode:** {telemetry.pacing_mode}\n"
            f"- **Effective Velocity:** {telemetry.effective_wpm:.1f} WPM\n"
            f"- **Words:** {telemetry.total_words} | **Syllables:** {telemetry.total_syllables}\n"
            f"- **Duration:** {telemetry.total_duration_sec:.2f}s\n"
            f"- **Regularity:** {telemetry.rhythm_regularity_score * 100:.1f}%\n"
        )
        nodes.append({
            "id": "node-pacer-header",
            "x": 0,
            "y": 0,
            "width": 380,
            "height": 220,
            "type": "text",
            "text": header_text,
            "color": "6",
        })

        # Render paced token cards in a snake or linear rhythm band
        cols = 5
        card_w = 220
        card_h = 160
        spacing_x = 40
        spacing_y = 50
        start_x = 440
        start_y = 0

        for idx, a in enumerate(telemetry.anchors[:40]):
            r = idx // cols
            c = idx % cols
            nx = start_x + (c * (card_w + spacing_x))
            ny = start_y + (r * (card_h + spacing_y))

            card_content = (
                f"### {a.formatted_token}\n\n"
                f"- **Dwell:** {a.dwell_ms:.0f} ms\n"
                f"- **Syllables:** {a.syllable_count}\n"
                f"- **OVP Index:** {a.ovp_index}\n"
                f"- **Time:** {a.timestamp_ms / 1000.0:.2f}s\n"
            )

            card_id = f"token-{idx}"
            nodes.append({
                "id": card_id,
                "x": nx,
                "y": ny,
                "width": card_w,
                "height": card_h,
                "type": "text",
                "text": card_content,
                "color": "4" if a.complexity_score > 0.5 else "2",
            })

            if idx > 0:
                prev_id = f"token-{idx-1}"
                edges.append({
                    "id": f"edge-pacer-{idx-1}-{idx}",
                    "fromNode": prev_id,
                    "fromSide": "right" if (idx % cols != 0) else "bottom",
                    "toNode": card_id,
                    "toSide": "left" if (idx % cols != 0) else "top",
                    "label": f"{a.dwell_ms:.0f}ms",
                })

        canvas_data = {"nodes": nodes, "edges": edges}
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(canvas_data, indent=2), encoding="utf-8")
        return target

    @staticmethod
    def export_svg_strip(telemetry: MetronomeTelemetry, filepath: str | Path) -> Path:
        """Export standalone SVG visual strip showing paced lexical anchors."""
        target = Path(filepath)
        items = telemetry.anchors[:12]
        strip_width = 1000
        strip_height = 280

        svg_parts: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {strip_width} {strip_height}" width="100%" height="auto">',
            '  <defs>',
            '    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#090a0f"/>',
            '      <stop offset="100%" stop-color="#141824"/>',
            '    </linearGradient>',
            '    <linearGradient id="bar-grad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '      <stop offset="0%" stop-color="#3b82f6"/>',
            '      <stop offset="100%" stop-color="#10b981"/>',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{strip_width}" height="{strip_height}" rx="16" fill="url(#bg-grad)" stroke="#1e293b" stroke-width="2"/>',
            f'  <text x="32" y="42" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="16" font-weight="700">DxSkills Visual Pacing Rhythm &amp; Fixation Metronome</text>',
            f'  <text x="32" y="66" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12">Mode: {telemetry.pacing_mode.upper()} | Velocity: {telemetry.effective_wpm:.1f} WPM | Regularity: {telemetry.rhythm_regularity_score*100:.1f}%</text>',
        ]

        if items:
            box_width = 72
            gap = 8
            start_x = 32
            start_y = 100

            for i, anchor in enumerate(items):
                bx = start_x + (i * (box_width + gap))
                clean = anchor.clean_word[:8]
                dwell_height = int(max(10, min(80, (anchor.dwell_ms / 400.0) * 80)))
                bar_y = start_y + 100 - dwell_height

                svg_parts.append(
                    f'  <g transform="translate({bx}, {start_y})">'
                    f'    <rect x="0" y="0" width="{box_width}" height="130" rx="8" fill="#1e293b" fill-opacity="0.6" stroke="#334155" stroke-width="1"/>'
                    f'    <rect x="12" y="{bar_y - start_y}" width="{box_width - 24}" height="{dwell_height}" rx="4" fill="url(#bar-grad)"/>'
                    f'    <text x="{box_width//2}" y="40" fill="#ffffff" font-family="system-ui, sans-serif" font-size="13" font-weight="700" text-anchor="middle">{clean}</text>'
                    f'    <circle cx="{box_width//2}" cy="54" r="3" fill="#f59e0b"/>'
                    f'    <text x="{box_width//2}" y="120" fill="#94a3b8" font-family="monospace" font-size="10" text-anchor="middle">{anchor.dwell_ms:.0f}ms</text>'
                    f'  </g>'
                )

        svg_parts.append('</svg>')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(svg_parts), encoding="utf-8")
        return target
