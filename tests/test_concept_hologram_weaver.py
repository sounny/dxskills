"""
Unit tests for Multimodal Concept Hologram & Interference Pattern Weaver Engine.
Verifies optical wave superposition, constructive interference peak detection,
holographic coherence scoring, SVG rendering, and diagnostic reporting.
Strictly zero em dash compliance.
"""

import pytest
import math
from scripts.concept_hologram_weaver import (
    WaveEmitter,
    InterferencePeak,
    HolographicTelemetry,
    ConceptHologramWeaver,
)


def test_wave_emitter_and_peak_creation():
    em = WaveEmitter(
        emitter_id="em-1",
        title="Visual Archetype",
        x=150.0,
        y=200.0,
        amplitude=1.5,
        wavelength_px=50.0,
        phase_rad=0.1,
        modality="SPATIAL",
        color="#38bdf8",
    )
    assert em.emitter_id == "em-1"
    d = em.to_dict()
    assert d["emitter_id"] == "em-1"
    assert d["modality"] == "SPATIAL"
    assert d["wavelength_px"] == 50.0

    pk = InterferencePeak(
        peak_id="pk-1",
        x=220.0,
        y=260.0,
        intensity=4.2,
        participating_emitters=["em-1", "em-2"],
        resonance_type="CONSTRUCTIVE",
    )
    pd = pk.to_dict()
    assert pd["peak_id"] == "pk-1"
    assert pd["resonance_type"] == "CONSTRUCTIVE"
    assert len(pd["participating_emitters"]) == 2


def test_compute_wave_field_empty():
    weaver = ConceptHologramWeaver()
    telemetry = weaver.compute_wave_field([])
    assert telemetry.total_emitters == 0
    assert len(telemetry.interference_peaks) == 0
    assert telemetry.global_coherence_index == 0.0
    assert telemetry.status_level == "DISPERSED"


def test_compute_wave_field_single_emitter():
    weaver = ConceptHologramWeaver(sample_grid_step=40.0)
    em = WaveEmitter("em-single", "Monad", 400.0, 300.0, amplitude=1.0, wavelength_px=60.0)
    telemetry = weaver.compute_wave_field([em])
    assert telemetry.total_emitters == 1
    assert telemetry.mean_field_intensity > 0.0
    # Single emitter has no multi-emitter constructive peak
    assert len(telemetry.interference_peaks) == 0


def test_compute_wave_field_constructive_interference():
    weaver = ConceptHologramWeaver(sample_grid_step=25.0)
    # Two identical in-phase emitters close together
    e1 = WaveEmitter("e1", "Concept 1", 380.0, 250.0, amplitude=1.0, wavelength_px=50.0, phase_rad=0.0)
    e2 = WaveEmitter("e2", "Concept 2", 420.0, 250.0, amplitude=1.0, wavelength_px=50.0, phase_rad=0.0)

    telemetry = weaver.compute_wave_field([e1, e2])
    assert telemetry.total_emitters == 2
    # Incoherent sum = 1^2 + 1^2 = 2.0
    # Maximum coherent constructive peak approaches (1+1)^2 = 4.0
    assert telemetry.peak_constructive_intensity > 2.0
    assert len(telemetry.interference_peaks) >= 1
    assert telemetry.interference_peaks[0].resonance_type in ["CONSTRUCTIVE", "HARMONIC"]


def test_demo_telemetry_generation():
    demo = ConceptHologramWeaver.create_demo_telemetry()
    assert demo.total_emitters == 3
    assert len(demo.interference_peaks) >= 1
    assert demo.peak_constructive_intensity > 0.0
    assert demo.global_coherence_index > 0.0
    assert demo.status_level in ["HIGH_COHERENCE", "RESONANT"]

    d = demo.to_dict()
    assert "global_coherence_index" in d
    assert "peak_constructive_intensity" in d


def test_markdown_report_formatting():
    weaver = ConceptHologramWeaver()
    demo = weaver.create_demo_telemetry()
    report = weaver.generate_markdown_report(demo)

    assert "# Multimodal Concept Hologram" in report
    assert "Karl Pribram Holonomic Brain Theory" in report
    assert "| Holographic Dimension |" in report
    assert "| Emitter ID |" in report
    assert chr(8212) not in report, "Em dash found in markdown report!"


def test_svg_rendering_integrity():
    weaver = ConceptHologramWeaver()
    demo = weaver.create_demo_telemetry()
    svg = weaver.generate_svg(demo, width=880, height=580)

    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg
    assert 'viewBox="0 0 880 580"' in svg
    assert 'MULTIMODAL CONCEPT HOLOGRAM WEAVER' in svg
    assert 'Holographic Field Telemetry' in svg
    assert 'Hologram Weaver Legend' in svg
    assert chr(8212) not in svg, "Em dash found in SVG output!"


def test_zero_em_dashes_enforcement():
    with open("scripts/concept_hologram_weaver.py", "r", encoding="utf-8") as f:
        src = f.read()
    assert chr(8212) not in src, "Em dash found in concept_hologram_weaver.py!"
