"""Unit tests for Autonomous Cognitive Spatial Visual Chunk Pacer & Ocular Fixation Metronome.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.visual_chunk_pacer import (
    ChunkPacerTelemetry,
    ChunkType,
    MorphemeBreakdown,
    MorphemeDecomposer,
    VisualChunk,
    VisualChunkPacer,
)


def test_morpheme_decomposer():
    # Prefix and suffix detection
    decomp1 = MorphemeDecomposer.decompose("multidimensional")
    assert decomp1.prefix == "multi"
    assert decomp1.is_compound is True
    assert "multi" in decomp1.segmented_form

    decomp2 = MorphemeDecomposer.decompose("synchronization")
    assert "ation" in decomp2.suffix or decomp2.is_compound is True

    # Short word
    decomp3 = MorphemeDecomposer.decompose("the")
    assert decomp3.morpheme_count == 1
    assert decomp3.is_compound is False


def test_segment_into_syntactic_chunks():
    pacer = VisualChunkPacer(target_chunk_tokens=3)
    text = "Distributed state machines coordinate consensus across geographic boundaries, ensuring consistency."
    chunks = pacer.segment_into_syntactic_chunks(text)

    assert len(chunks) >= 3
    # Check that punctuation causes a chunk break
    assert any(any("," in t for t in c) for c in chunks)


def test_pace_chunks_empty():
    pacer = VisualChunkPacer()
    telemetry = pacer.pace_chunks("")
    assert telemetry.total_words == 0
    assert telemetry.total_chunks == 0
    assert len(telemetry.chunks) == 0


def test_pace_chunks_telemetry(tmp_path: Path):
    pacer = VisualChunkPacer(base_wpm=200.0, target_chunk_tokens=3)
    text = (
        "Distributed asynchronous state machines coordinate deterministic state across multiple regions. "
        "Consensus protocols eliminate split-brain synchronization anomalies during network partitions."
    )
    telemetry = pacer.pace_chunks(text)

    assert telemetry.total_words > 15
    assert telemetry.total_chunks >= 5
    assert telemetry.avg_tokens_per_chunk >= 1.5
    assert telemetry.avg_chunk_dwell_ms > 100.0
    assert telemetry.total_duration_sec > 1.0
    assert 0.2 <= telemetry.syntactic_cohesion_score <= 1.0

    # Verify visual formatting
    assert "[" in telemetry.chunks[0].formatted_display
    assert "]" in telemetry.chunks[0].formatted_display

    # Render ASCII
    ascii_table = pacer.render_ascii_cadence(telemetry)
    assert "DxSkills Visual Syntactic Chunk Pacer" in ascii_table
    assert "#1" in ascii_table

    # Export Canvas
    canvas_file = tmp_path / "test_chunks.canvas"
    pacer.export_canvas(telemetry, canvas_file)
    assert canvas_file.exists()
    cdata = json.loads(canvas_file.read_text(encoding="utf-8"))
    assert "nodes" in cdata
    assert len(cdata["nodes"]) >= telemetry.total_chunks + 1

    # Export SVG
    svg_file = tmp_path / "test_chunks.svg"
    pacer.export_svg_strip(telemetry, svg_file)
    assert svg_file.exists()
    svg_content = svg_file.read_text(encoding="utf-8")
    assert "<svg" in svg_content
    assert "DxSkills Syntactic Chunk Pacer" in svg_content


def test_zero_em_dashes():
    script_file = Path(__file__).resolve().parent.parent / "scripts" / "visual_chunk_pacer.py"
    test_file = Path(__file__).resolve()

    em_dash = chr(8212)
    assert em_dash not in script_file.read_text(encoding="utf-8")
    assert em_dash not in test_file.read_text(encoding="utf-8")
