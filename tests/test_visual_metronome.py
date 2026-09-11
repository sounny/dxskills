"""Unit tests for Autonomous Cognitive Spatial Visual Pacing Rhythm & Bionic Fixation Metronome.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.visual_metronome import (
    LexicalAnchor,
    MetronomeTelemetry,
    PacingMode,
    VisualPacingMetronome,
)


def test_estimate_syllables():
    metronome = VisualPacingMetronome()
    assert metronome.estimate_syllables("cat") == 1
    assert metronome.estimate_syllables("buffer") == 2
    assert metronome.estimate_syllables("cognitive") >= 3
    assert metronome.estimate_syllables("architecture") >= 4
    assert metronome.estimate_syllables("") == 1


def test_calculate_ovp():
    assert VisualPacingMetronome.calculate_ovp("in") == 0
    assert VisualPacingMetronome.calculate_ovp("read") == 1
    assert VisualPacingMetronome.calculate_ovp("spatial") == 2
    assert VisualPacingMetronome.calculate_ovp("architecture") == 3


def test_format_bionic_anchor():
    assert VisualPacingMetronome.format_bionic_anchor("a") == "**a**"
    assert VisualPacingMetronome.format_bionic_anchor("dog") == "**d**og"
    assert VisualPacingMetronome.format_bionic_anchor("schema") == "**sc**hema"
    assert VisualPacingMetronome.format_bionic_anchor("pipeline") == "**pip**eline"
    assert VisualPacingMetronome.format_bionic_anchor("asynchronous") == "**asyn**chronous"
    # Punctuation retention
    assert VisualPacingMetronome.format_bionic_anchor('"graph",') == '"**gr**aph",'


def test_synthesize_empty():
    metronome = VisualPacingMetronome()
    telemetry = metronome.synthesize_pacing_timeline("")
    assert telemetry.total_words == 0
    assert telemetry.total_syllables == 0
    assert len(telemetry.anchors) == 0


def test_synthesize_pacing_modes(tmp_path: Path):
    sample = "Distributed asynchronous cognitive state machines coordinate deterministic visual memory topologies."

    # Adaptive mode
    m_adaptive = VisualPacingMetronome(base_wpm=200.0, mode=PacingMode.SYLLABLE_ADAPTIVE)
    t_adaptive = m_adaptive.synthesize_pacing_timeline(sample)
    assert t_adaptive.total_words == 10
    assert t_adaptive.total_syllables > 15
    assert t_adaptive.total_duration_sec > 1.0
    assert len(t_adaptive.anchors) == 10

    # Isochronic mode (equal intervals)
    m_iso = VisualPacingMetronome(base_wpm=200.0, mode=PacingMode.ISOCHRONIC)
    t_iso = m_iso.synthesize_pacing_timeline(sample)
    dwells = [a.dwell_ms for a in t_iso.anchors]
    assert all(d == 300.0 for d in dwells)

    # Morphological mode
    m_morph = VisualPacingMetronome(base_wpm=200.0, mode=PacingMode.MORPHOLOGICAL)
    t_morph = m_morph.synthesize_pacing_timeline(sample)
    assert t_morph.anchors[0].dwell_ms > 0

    # Accelerative mode
    m_accel = VisualPacingMetronome(base_wpm=200.0, mode=PacingMode.ACCELERATIVE)
    t_accel = m_accel.synthesize_pacing_timeline(sample)
    assert len(t_accel.anchors) == 10

    # Render ASCII
    ascii_out = m_adaptive.render_ascii_cadence(t_adaptive)
    assert "DxSkills Visual Pacing Rhythm" in ascii_out
    assert "Distributed" in ascii_out

    # Export Canvas
    canvas_path = tmp_path / "test_metronome.canvas"
    VisualPacingMetronome.export_canvas(t_adaptive, canvas_path)
    assert canvas_path.exists()
    canvas_data = json.loads(canvas_path.read_text(encoding="utf-8"))
    assert "nodes" in canvas_data
    assert len(canvas_data["nodes"]) >= 11

    # Export SVG
    svg_path = tmp_path / "test_metronome.svg"
    VisualPacingMetronome.export_svg_strip(t_adaptive, svg_path)
    assert svg_path.exists()
    svg_text = svg_path.read_text(encoding="utf-8")
    assert "<svg" in svg_text
    assert "DxSkills Visual Pacing Rhythm" in svg_text


def test_zero_em_dashes():
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "visual_metronome.py"
    test_path = Path(__file__).resolve()

    em_dash = chr(8212)
    assert em_dash not in script_path.read_text(encoding="utf-8")
    assert em_dash not in test_path.read_text(encoding="utf-8")
