"""Unit tests for Autonomous Cognitive Spatial Saliency Decoupler & Multi-Track Audio Pacer.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.audio_pacer import (
    AudioTrackType,
    CognitiveTaskProfile,
    SpatialAcousticNode,
    SpatialAudioPacer,
    SpatialSoundstageConfig,
)


def test_pacing_bpm_calculation():
    pacer = SpatialAudioPacer()

    # High complexity should produce slower, grounding pacing (theta/alpha)
    slow_bpm = pacer.calculate_pacing_bpm(complexity=0.9, cognitive_load=0.9)
    assert 54.0 <= slow_bpm <= 65.0
    band_slow = pacer.determine_entrainment_band(slow_bpm)
    assert "Theta" in band_slow or "Alpha" in band_slow

    # Low complexity should produce brisk, flow-state pacing (beta)
    fast_bpm = pacer.calculate_pacing_bpm(complexity=0.1, cognitive_load=0.1)
    assert 95.0 <= fast_bpm <= 110.0
    band_fast = pacer.determine_entrainment_band(fast_bpm)
    assert "Beta" in band_fast or "SMR" in band_fast


def test_saliency_decoupling_streams():
    pacer = SpatialAudioPacer()
    task = CognitiveTaskProfile(
        task_name="Architectural Refactoring",
        complexity_score=0.8,
        cognitive_load=0.7,
        stream_count=3,
    )

    raw_streams = [
        {
            "id": "code_compiler",
            "name": "Compiler Telemetry",
            "track_type": AudioTrackType.TELEMETRY_LOG,
            "description": "Streaming build warnings and test metrics",
        },
        {
            "id": "editor_focus",
            "name": "Codebase Synthesis",
            "track_type": AudioTrackType.PRIMARY_FOCUS,
            "description": "Active coding AST buffer",
        },
        {
            "id": "git_alerts",
            "name": "Branch CI Alert",
            "track_type": AudioTrackType.ALERT_URGENT,
            "description": "Urgent merge conflict notification",
        },
    ]

    config = pacer.decouple_saliency(task, raw_streams)
    assert len(config.nodes) == 3
    assert config.phonological_load_reduction_pct > 20.0
    assert 54.0 <= config.recommended_bpm <= 75.0

    # Verify primary focus node is centered
    focus_nodes = [n for n in config.nodes if n.track_type == AudioTrackType.PRIMARY_FOCUS]
    assert len(focus_nodes) == 1
    assert focus_nodes[0].azimuth_degrees == 0.0
    assert focus_nodes[0].pan == 0.0
    assert focus_nodes[0].cutoff_frequency_hz >= 10000.0

    # Verify urgent alert is biased right for quick attentional capture
    alert_nodes = [n for n in config.nodes if n.track_type == AudioTrackType.ALERT_URGENT]
    assert len(alert_nodes) == 1
    assert alert_nodes[0].pan > 0.0


def test_web_audio_manifest_generation():
    pacer = SpatialAudioPacer()
    task = CognitiveTaskProfile(task_name="Quick Debug Sprint", complexity_score=0.3, cognitive_load=0.2)
    raw_streams = [
        {"id": "s1", "name": "Primary Code", "track_type": AudioTrackType.PRIMARY_FOCUS},
        {"id": "s2", "name": "Log Stream", "track_type": AudioTrackType.TELEMETRY_LOG},
    ]
    config = pacer.decouple_saliency(task, raw_streams)
    manifest = pacer.generate_web_audio_manifest(config)

    assert manifest["version"] == "1.0.0"
    assert manifest["audioContext"]["masterGain"] == 0.85
    assert len(manifest["channels"]) == 2
    assert "panner" in manifest["channels"][0]
    assert "filter" in manifest["channels"][0]
    assert "gain" in manifest["channels"][0]
    assert "pacing" in manifest["channels"][0]


def test_obsidian_canvas_export(tmp_path):
    pacer = SpatialAudioPacer()
    task = CognitiveTaskProfile(task_name="Spatial Soundstage Exploration", complexity_score=0.5)
    raw_streams = [
        {"id": "focus", "name": "Center Hub", "track_type": AudioTrackType.PRIMARY_FOCUS},
        {"id": "ambience", "name": "Brown Noise Pacer", "track_type": AudioTrackType.BACKGROUND_AMBIENCE},
    ]
    config = pacer.decouple_saliency(task, raw_streams)

    out_file = tmp_path / "test_soundstage.canvas"
    canvas_data = pacer.export_canvas(config, str(out_file))

    assert out_file.exists()
    assert len(canvas_data["nodes"]) == 3  # listener + 2 audio nodes
    assert len(canvas_data["edges"]) == 2

    # Check listener node text
    listener = canvas_data["nodes"][0]
    assert listener["id"] == "listener_center"
    assert "Listener Center" in listener["text"]


def test_svg_soundstage_generation(tmp_path):
    pacer = SpatialAudioPacer()
    task = CognitiveTaskProfile(task_name="Audio Synthesis Test", complexity_score=0.6)
    raw_streams = [
        {"id": "st1", "name": "Focus Track", "track_type": AudioTrackType.PRIMARY_FOCUS},
        {"id": "st2", "name": "Rhythm Pulse", "track_type": AudioTrackType.RHYTHMIC_PACER},
    ]
    config = pacer.decouple_saliency(task, raw_streams)

    svg_file = tmp_path / "soundstage.svg"
    svg_content = pacer.export_svg_soundstage(config, str(svg_file))

    assert svg_file.exists()
    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert "Spatial Soundstage Radar" in svg_content
    assert "Cognitive Observer" in svg_content


def test_zero_em_dashes_enforcement():
    pacer = SpatialAudioPacer()
    task = CognitiveTaskProfile(task_name="Strict Typography Test", complexity_score=0.7)
    raw_streams = [
        {"id": "stream1", "name": "Core Pipeline", "track_type": AudioTrackType.PRIMARY_FOCUS},
        {"id": "stream2", "name": "Telemetry Node", "track_type": AudioTrackType.TELEMETRY_LOG},
    ]
    config = pacer.decouple_saliency(task, raw_streams)

    md_report = pacer.generate_markdown_report(config)
    svg_content = pacer.export_svg_soundstage(config)
    canvas_data = pacer.export_canvas(config)
    manifest = pacer.generate_web_audio_manifest(config)

    # Convert everything to text and assert zero em dashes
    full_text = md_report + svg_content + json.dumps(canvas_data) + json.dumps(manifest)
    assert chr(8212) not in full_text
    assert "\u2014" not in full_text
