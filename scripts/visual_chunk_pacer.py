"""Autonomous Cognitive Spatial Visual Chunk Pacer & Ocular Fixation Metronome.

Theoretical Foundation:
- Taft & Forster Dual-Route Morphemic Decomposition Model:
  Dyslexic lexical retrieval latency is substantially minimized when polysyllabic
  words are segmented at morphological seams (prefix, root, suffix), bypassing
  phonological assembly bottlenecks in the Visual Word Form Area (VWFA).
- Rayner & Frazier Syntactic Chunking & Cognitive Processing:
  The foveal and parafoveal field spans 2-4 lexical items per visual intake.
  Syntactic chunking organizes linear prose into semantic phrases (noun phrases,
  prepositional phrases, verb groups), stabilizing ocular saccades and eliminating
  within-clause regressive jitter.
- Sub-Lexical Fixation Pause Optimization:
  Calculates adaptive ocular pause intervals per phrase chunk based on accumulated
  morphemic complexity, token length, and clausal boundary punctuation.

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


class ChunkType(str, enum.Enum):
    """Grammatical or structural chunk category."""

    NOUN_PHRASE = "noun_phrase"
    VERB_GROUP = "verb_group"
    PREPOSITIONAL = "prepositional"
    CLAUSAL_TRANSITION = "clausal_transition"
    TECHNICAL_TERM = "technical_term"
    GENERAL = "general"


@dataclass
class MorphemeBreakdown:
    """Sub-lexical morphological decomposition of a complex token."""

    raw_token: str
    prefix: str = ""
    root: str = ""
    suffix: str = ""
    is_compound: bool = False
    segmented_form: str = ""
    morpheme_count: int = 1


@dataclass
class VisualChunk:
    """Syntactic phrase chunk with sub-lexical and ocular dwell telemetry."""

    chunk_id: int
    tokens: List[str]
    clean_text: str
    chunk_type: ChunkType
    total_syllables: int
    morpheme_breakdowns: List[MorphemeBreakdown]
    complexity_score: float
    pause_dwell_ms: float
    timestamp_ms: float
    formatted_display: str


@dataclass
class ChunkPacerTelemetry:
    """Telemetry report quantifying syntactic chunking and ocular pause pacing."""

    total_words: int
    total_chunks: int
    avg_tokens_per_chunk: float
    avg_chunk_dwell_ms: float
    total_duration_sec: float
    effective_wpm: float
    syntactic_cohesion_score: float
    chunks: List[VisualChunk] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_words": self.total_words,
            "total_chunks": self.total_chunks,
            "avg_tokens_per_chunk": round(self.avg_tokens_per_chunk, 2),
            "avg_chunk_dwell_ms": round(self.avg_chunk_dwell_ms, 2),
            "total_duration_sec": round(self.total_duration_sec, 2),
            "effective_wpm": round(self.effective_wpm, 1),
            "syntactic_cohesion_score": round(self.syntactic_cohesion_score, 3),
            "chunks": [asdict(c) for c in self.chunks],
        }


class MorphemeDecomposer:
    """Rule-based sub-lexical morphological decomposition engine."""

    COMMON_PREFIXES = [
        "anti", "auto", "co", "contra", "counter", "de", "dis", "extra", "hyper",
        "hypo", "infra", "inter", "intra", "macro", "micro", "mid", "mis", "multi",
        "non", "out", "over", "para", "post", "pre", "pro", "proto", "pseudo",
        "quasi", "re", "retro", "semi", "sub", "super", "tele", "trans", "ultra", "un"
    ]

    COMMON_SUFFIXES = [
        "ability", "able", "action", "al", "ance", "ancy", "ant", "ate", "ation",
        "ative", "centric", "ed", "en", "ence", "ent", "er", "es", "est", "ful",
        "graphy", "ible", "ic", "ical", "ing", "ion", "ious", "ise", "ish", "ism",
        "ist", "istic", "ity", "ive", "ize", "ization", "less", "logy", "ly",
        "ment", "ness", "oid", "ology", "or", "ous", "ship", "tion", "tive", "ward"
    ]

    @classmethod
    def decompose(cls, word: str) -> MorphemeBreakdown:
        """Decompose a word into prefix, root, and suffix boundaries."""
        clean = re.sub(r"[^a-zA-Z]", "", word).lower()
        if len(clean) <= 4:
            return MorphemeBreakdown(
                raw_token=word,
                root=clean,
                segmented_form=word,
                morpheme_count=1
            )

        found_prefix = ""
        remainder = clean

        # Check prefixes sorted by length descending
        for pre in sorted(cls.COMMON_PREFIXES, key=len, reverse=True):
            if remainder.startswith(pre) and len(remainder) - len(pre) >= 3:
                found_prefix = pre
                remainder = remainder[len(pre):]
                break

        found_suffix = ""
        # Check suffixes sorted by length descending
        for suf in sorted(cls.COMMON_SUFFIXES, key=len, reverse=True):
            if remainder.endswith(suf) and len(remainder) - len(suf) >= 3:
                found_suffix = suf
                remainder = remainder[:-len(suf)]
                break

        root = remainder
        morphemes = [m for m in [found_prefix, root, found_suffix] if m]
        morpheme_count = len(morphemes)

        # Build segmented display (e.g. "asyn*chron*ous" or "multi-agent")
        parts = []
        if found_prefix:
            parts.append(found_prefix)
        if root:
            parts.append(root)
        if found_suffix:
            parts.append(found_suffix)

        segmented = "-".join(parts) if len(parts) > 1 else word

        return MorphemeBreakdown(
            raw_token=word,
            prefix=found_prefix,
            root=root,
            suffix=found_suffix,
            is_compound=(morpheme_count >= 2),
            segmented_form=segmented,
            morpheme_count=morpheme_count
        )


class VisualChunkPacer:
    """Partitions text into syntactic chunks and calculates ocular pause cadences."""

    def __init__(
        self,
        base_wpm: float = 200.0,
        target_chunk_tokens: int = 3,
        min_pause_ms: float = 180.0,
        max_pause_ms: float = 650.0,
    ) -> None:
        self.base_wpm = max(60.0, min(base_wpm, 600.0))
        self.target_chunk_tokens = max(1, min(target_chunk_tokens, 6))
        self.min_pause_ms = min_pause_ms
        self.max_pause_ms = max_pause_ms

    @staticmethod
    def estimate_syllables(word: str) -> int:
        """Rule-based syllable estimator."""
        token = re.sub(r"[^a-z]", "", word.lower())
        if not token:
            return 1
        if len(token) <= 3:
            return 1
        runs = len(re.findall(r"[aeiouy]+", token))
        if token.endswith("e") and not token.endswith("le") and len(token) > 2:
            runs = max(1, runs - 1)
        return max(1, runs)

    def classify_chunk_type(self, tokens: List[str]) -> ChunkType:
        """Infer syntactic role of a phrase chunk."""
        joined = " ".join(tokens).lower()
        if any(p in tokens[0].lower() for p in ["in", "on", "at", "by", "for", "with", "across", "under", "over"]):
            return ChunkType.PREPOSITIONAL
        if any(v in joined for v in ["is", "are", "was", "were", "coordinate", "eliminates", "synthesize", "models", "execute"]):
            return ChunkType.VERB_GROUP
        if any(c in joined for c in ["however", "therefore", "furthermore", "whereas", "consequently", "because", "although"]):
            return ChunkType.CLAUSAL_TRANSITION
        if any(t in joined for t in ["architecture", "synchronization", "asynchronous", "deterministic", "consensus"]):
            return ChunkType.TECHNICAL_TERM
        return ChunkType.NOUN_PHRASE

    def segment_into_syntactic_chunks(self, text: str) -> List[List[str]]:
        """Partition raw prose into coherent phrase chunks (2-4 words)."""
        words = text.split()
        if not words:
            return []

        chunks: List[List[str]] = []
        current: List[str] = []

        prepositions_and_conjunctions = {
            "in", "on", "at", "to", "for", "with", "from", "by", "about", "as",
            "into", "like", "through", "after", "over", "between", "out", "against",
            "during", "without", "before", "under", "around", "among", "across",
            "and", "but", "or", "nor", "for", "yet", "so", "because", "although", "while"
        }

        for w in words:
            current.append(w)
            has_boundary_punct = any(p in w for p in [".", ",", ";", ":", "!", "?", "(", ")"])

            # Break on punctuation or when chunk reaches target size
            if has_boundary_punct:
                chunks.append(current)
                current = []
            elif len(current) >= self.target_chunk_tokens:
                chunks.append(current)
                current = []
            elif len(current) >= 2 and any(w.lower() in prepositions_and_conjunctions for w in [w]):
                # Natural clausal boundary
                chunks.append(current)
                current = []

        if current:
            if chunks and len(current) == 1:
                # Merge trailing single word into last chunk to avoid orphan token
                chunks[-1].extend(current)
            else:
                chunks.append(current)

        return chunks

    def compute_chunk_complexity(self, tokens: List[str], breakdowns: List[MorphemeBreakdown]) -> float:
        """Calculate overall cognitive intake complexity for the chunk."""
        token_count = len(tokens)
        if token_count == 0:
            return 0.0

        avg_morphemes = sum(b.morpheme_count for b in breakdowns) / token_count
        syllables = sum(self.estimate_syllables(t) for t in tokens)
        avg_syllables = syllables / token_count

        has_clause_break = any(any(p in t for p in [",", ";", ":", "."]) for t in tokens)
        clause_weight = 0.25 if has_clause_break else 0.0

        # Weighted combination
        raw_score = (0.4 * (avg_morphemes / 3.0)) + (0.4 * (avg_syllables / 3.5)) + clause_weight
        return max(0.1, min(1.0, raw_score))

    def pace_chunks(self, text: str) -> ChunkPacerTelemetry:
        """Synthesize syntactic chunks and compute sub-lexical pause durations."""
        raw_chunks = self.segment_into_syntactic_chunks(text)
        if not raw_chunks:
            return ChunkPacerTelemetry(
                total_words=0,
                total_chunks=0,
                avg_tokens_per_chunk=0.0,
                avg_chunk_dwell_ms=0.0,
                total_duration_sec=0.0,
                effective_wpm=self.base_wpm,
                syntactic_cohesion_score=1.0,
                chunks=[],
            )

        total_words = sum(len(c) for c in raw_chunks)
        ms_per_word = (60.0 / self.base_wpm) * 1000.0

        visual_chunks: List[VisualChunk] = []
        cumulative_time_ms = 0.0
        dwell_list: List[float] = []

        for idx, token_group in enumerate(raw_chunks):
            clean_text = " ".join(token_group)
            breakdowns = [MorphemeDecomposer.decompose(t) for t in token_group]
            chunk_type = self.classify_chunk_type(token_group)
            syllable_count = sum(self.estimate_syllables(t) for t in token_group)
            complexity = self.compute_chunk_complexity(token_group, breakdowns)

            # Base dwell proportional to word count
            base_chunk_dwell = ms_per_word * len(token_group)
            # Modulate by morphemic and syntactic complexity
            modulated_dwell = base_chunk_dwell * (0.75 + (complexity * 0.6))
            pause_dwell = max(self.min_pause_ms, min(self.max_pause_ms, modulated_dwell))
            dwell_list.append(pause_dwell)

            # Format display with visual brackets and morpheme guidance
            formatted_tokens = []
            for t, b in zip(token_group, breakdowns):
                if b.morpheme_count >= 2:
                    formatted_tokens.append(f"<{b.segmented_form}>")
                else:
                    formatted_tokens.append(t)
            formatted_display = f"[ {' '.join(formatted_tokens)} ]"

            visual_chunks.append(
                VisualChunk(
                    chunk_id=idx + 1,
                    tokens=token_group,
                    clean_text=clean_text,
                    chunk_type=chunk_type,
                    total_syllables=syllable_count,
                    morpheme_breakdowns=breakdowns,
                    complexity_score=round(complexity, 3),
                    pause_dwell_ms=round(pause_dwell, 1),
                    timestamp_ms=round(cumulative_time_ms, 1),
                    formatted_display=formatted_display,
                )
            )
            cumulative_time_ms += pause_dwell

        avg_tokens = total_words / len(visual_chunks) if visual_chunks else 0.0
        avg_dwell = sum(dwell_list) / len(dwell_list) if dwell_list else 0.0
        total_duration_sec = cumulative_time_ms / 1000.0
        effective_wpm = (total_words / total_duration_sec * 60.0) if total_duration_sec > 0 else self.base_wpm

        # Calculate syntactic cohesion score (evaluates variance around optimal 2.8 token size)
        variance = sum((len(c.tokens) - 2.8) ** 2 for c in visual_chunks) / len(visual_chunks)
        cohesion_score = max(0.2, min(1.0, 1.0 - (math.sqrt(variance) * 0.2)))

        return ChunkPacerTelemetry(
            total_words=total_words,
            total_chunks=len(visual_chunks),
            avg_tokens_per_chunk=avg_tokens,
            avg_chunk_dwell_ms=avg_dwell,
            total_duration_sec=total_duration_sec,
            effective_wpm=effective_wpm,
            syntactic_cohesion_score=cohesion_score,
            chunks=visual_chunks,
        )

    @staticmethod
    def render_ascii_cadence(telemetry: ChunkPacerTelemetry, max_chunks: int = 12) -> str:
        """Render a clean ASCII visual syntactic chunk pacer table."""
        lines: List[str] = []
        lines.append("=== DxSkills Visual Syntactic Chunk Pacer & Fixation Metronome ===")
        lines.append(
            f"Words: {telemetry.total_words} | Chunks: {telemetry.total_chunks} | "
            f"Avg Chunk Size: {telemetry.avg_tokens_per_chunk:.1f} tokens | Duration: {telemetry.total_duration_sec:.2f}s"
        )
        lines.append(
            f"Paced Velocity: {telemetry.effective_wpm:.1f} WPM | Avg Dwell: {telemetry.avg_chunk_dwell_ms:.0f}ms | "
            f"Cohesion: {telemetry.syntactic_cohesion_score*100:.1f}%"
        )
        lines.append("-" * 68)
        lines.append(f"{'Chunk':<5} {'Type':<14} {'Dwell':<9} {'Timeline':<10} {'Phrase Intake Block'}")
        lines.append("-" * 68)

        for chunk in telemetry.chunks[:max_chunks]:
            time_mark = f"{chunk.timestamp_ms / 1000.0:.2f}s"
            bar_len = int(round(chunk.pause_dwell_ms / 30.0))
            bar_str = "#" * min(18, max(2, bar_len))
            type_str = chunk.chunk_type.value[:13]
            clean_display = chunk.clean_text[:28]
            lines.append(f"#{chunk.chunk_id:<4} {type_str:<14} {chunk.pause_dwell_ms:>5.0f}ms   {time_mark:<10} [{clean_display}] {bar_str}")

        if len(telemetry.chunks) > max_chunks:
            diff = len(telemetry.chunks) - max_chunks
            lines.append(f"... ({diff} additional syntactic phrase chunks queued)")

        lines.append("-" * 68)
        return "\n".join(lines)

    @staticmethod
    def export_canvas(telemetry: ChunkPacerTelemetry, filepath: str | Path) -> Path:
        """Export syntactic chunk pacer graph to Obsidian Canvas (.canvas) JSON."""
        target = Path(filepath)
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []

        header_text = (
            f"## Visual Syntactic Chunk Pacing Cadence\n\n"
            f"- **Effective Velocity:** {telemetry.effective_wpm:.1f} WPM\n"
            f"- **Total Chunks:** {telemetry.total_chunks} ({telemetry.total_words} words)\n"
            f"- **Tokens per Chunk:** {telemetry.avg_tokens_per_chunk:.1f}\n"
            f"- **Avg Dwell:** {telemetry.avg_chunk_dwell_ms:.0f}ms\n"
            f"- **Syntactic Cohesion:** {telemetry.syntactic_cohesion_score*100:.1f}%\n"
        )
        nodes.append({
            "id": "node-chunk-header",
            "x": 0,
            "y": 0,
            "width": 380,
            "height": 220,
            "type": "text",
            "text": header_text,
            "color": "6",
        })

        cols = 4
        card_w = 260
        card_h = 180
        spacing_x = 50
        spacing_y = 60
        start_x = 450
        start_y = 0

        for idx, c in enumerate(telemetry.chunks[:32]):
            row = idx // cols
            col = idx % cols
            nx = start_x + (col * (card_w + spacing_x))
            ny = start_y + (row * (card_h + spacing_y))

            morphemes_str = ", ".join([b.segmented_form for b in c.morpheme_breakdowns if b.morpheme_count >= 2])
            morpheme_line = f"\n- **Morphemes:** {morphemes_str}" if morphemes_str else ""

            content = (
                f"### Chunk #{c.chunk_id}: {c.chunk_type.value}\n\n"
                f"**{c.formatted_display}**\n\n"
                f"- **Dwell:** {c.pause_dwell_ms:.0f}ms\n"
                f"- **Syllables:** {c.total_syllables}\n"
                f"- **Time:** {c.timestamp_ms / 1000.0:.2f}s"
                f"{morpheme_line}\n"
            )

            cid = f"chunk-{idx+1}"
            nodes.append({
                "id": cid,
                "x": nx,
                "y": ny,
                "width": card_w,
                "height": card_h,
                "type": "text",
                "text": content,
                "color": "3" if c.complexity_score > 0.4 else "1",
            })

            if idx > 0:
                prev_id = f"chunk-{idx}"
                edges.append({
                    "id": f"edge-chunk-{idx}-{idx+1}",
                    "fromNode": prev_id,
                    "fromSide": "right" if (idx % cols != 0) else "bottom",
                    "toNode": cid,
                    "toSide": "left" if (idx % cols != 0) else "top",
                    "label": f"{c.pause_dwell_ms:.0f}ms",
                })

        canvas_data = {"nodes": nodes, "edges": edges}
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(canvas_data, indent=2), encoding="utf-8")
        return target

    @staticmethod
    def export_svg_strip(telemetry: ChunkPacerTelemetry, filepath: str | Path) -> Path:
        """Export standalone SVG strip displaying visual syntactic intake chunks."""
        target = Path(filepath)
        items = telemetry.chunks[:10]
        width = 1050
        height = 300

        svg: List[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">',
            '  <defs>',
            '    <linearGradient id="c-bg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#0b0f19"/>',
            '      <stop offset="100%" stop-color="#1e1b4b"/>',
            '    </linearGradient>',
            '    <linearGradient id="bar-fill" x1="0%" y1="0%" x2="100%" y2="0%">',
            '      <stop offset="0%" stop-color="#6366f1"/>',
            '      <stop offset="100%" stop-color="#a855f7"/>',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" rx="16" fill="url(#c-bg)" stroke="#312e81" stroke-width="2"/>',
            f'  <text x="32" y="42" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="16" font-weight="700">DxSkills Syntactic Chunk Pacer &amp; Fixation Metronome</text>',
            f'  <text x="32" y="66" fill="#c7d2fe" font-family="system-ui, sans-serif" font-size="12">Paced Speed: {telemetry.effective_wpm:.1f} WPM | Avg Dwell: {telemetry.avg_chunk_dwell_ms:.0f}ms | Syntactic Cohesion: {telemetry.syntactic_cohesion_score*100:.1f}%</text>',
        ]

        if items:
            box_w = 92
            gap = 10
            sx = 32
            sy = 100

            for i, chunk in enumerate(items):
                bx = sx + (i * (box_w + gap))
                first_tok = chunk.tokens[0][:9]
                bar_h = int(max(12, min(75, (chunk.pause_dwell_ms / 600.0) * 75)))
                bar_y = sy + 100 - bar_h

                svg.append(
                    f'  <g transform="translate({bx}, {sy})">'
                    f'    <rect x="0" y="0" width="{box_w}" height="145" rx="8" fill="#1e1b4b" fill-opacity="0.7" stroke="#4338ca" stroke-width="1"/>'
                    f'    <rect x="14" y="{bar_y - sy}" width="{box_w - 28}" height="{bar_h}" rx="4" fill="url(#bar-fill)"/>'
                    f'    <text x="{box_w//2}" y="30" fill="#a5b4fc" font-family="monospace" font-size="10" text-anchor="middle">#{chunk.chunk_id}</text>'
                    f'    <text x="{box_w//2}" y="48" fill="#ffffff" font-family="system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="middle">{first_tok}</text>'
                    f'    <text x="{box_w//2}" y="132" fill="#e0e7ff" font-family="monospace" font-size="10" text-anchor="middle">{chunk.pause_dwell_ms:.0f}ms</text>'
                    f'  </g>'
                )

        svg.append('</svg>')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(svg), encoding="utf-8")
        return target
