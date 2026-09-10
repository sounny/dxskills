#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Spatial Working Memory Saccadic Pacing & Rhythm Metronome
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import wave
import tempfile
import unittest

from scripts.rhythm_pacer import (
    PacingCadence,
    RhythmTelemetryAudit,
    SaccadicRhythmPacer
)


class TestSaccadicRhythmPacer(unittest.TestCase):
    """Tests for cadence calculation, pacing timeline, metronome audio synthesis, and SVG export."""

    def setUp(self):
        self.pacer = SaccadicRhythmPacer()
        self.sample_text = (
            "Spatial cognition and visual memory offload phonological decoding stress. "
            "Rhythmic saccadic pacing stabilizes ocular fixation jumps across sentences."
        )

    def test_calculate_cadence(self):
        cadence = self.pacer.calculate_cadence(self.sample_text, target_wpm=160, words_per_fixation=2)
        self.assertEqual(cadence.wpm, 160)
        self.assertEqual(cadence.words_per_fixation, 2)
        self.assertEqual(cadence.fixation_interval_ms, 750)
        self.assertEqual(cadence.beats_per_minute, 80.0)
        self.assertGreaterEqual(cadence.total_words, 15)
        self.assertGreater(cadence.estimated_duration_sec, 4.0)

    def test_generate_pacing_timeline(self):
        timeline = self.pacer.generate_pacing_timeline(self.sample_text, target_wpm=160, words_per_fixation=2)
        self.assertGreaterEqual(len(timeline), 7)
        first = timeline[0]
        self.assertEqual(first["beat_idx"], 1)
        self.assertEqual(first["timestamp_ms"], 0)
        self.assertEqual(first["timestamp_sec"], 0.0)
        self.assertEqual(first["chunk"], "Spatial cognition")

        second = timeline[1]
        self.assertEqual(second["beat_idx"], 2)
        self.assertEqual(second["timestamp_ms"], 750)
        self.assertEqual(second["timestamp_sec"], 0.75)

    def test_audit_cadence_profiles(self):
        # Calm / Deep
        c_slow = self.pacer.calculate_cadence(self.sample_text, target_wpm=110)
        audit_slow = self.pacer.audit_cadence(c_slow)
        self.assertIn("Deep Absorption", audit_slow.cadence_profile)
        self.assertEqual(audit_slow.soundtrack_frequency_hz, 432.0)

        # Balanced
        c_med = self.pacer.calculate_cadence(self.sample_text, target_wpm=160)
        audit_med = self.pacer.audit_cadence(c_med)
        self.assertIn("Balanced Focus", audit_med.cadence_profile)
        self.assertEqual(audit_med.soundtrack_frequency_hz, 528.0)

        # Fast
        c_fast = self.pacer.calculate_cadence(self.sample_text, target_wpm=220)
        audit_fast = self.pacer.audit_cadence(c_fast)
        self.assertIn("Rapid Synthesis", audit_fast.cadence_profile)
        self.assertEqual(audit_fast.soundtrack_frequency_hz, 639.0)

    def test_write_audio_metronome(self):
        cadence = self.pacer.calculate_cadence(self.sample_text, target_wpm=180, words_per_fixation=2)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.pacer.write_audio_metronome(cadence, tmp_path, max_duration_sec=1.5)
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 5000)

            # Check WAV properties
            with wave.open(tmp_path, "rb") as w:
                self.assertEqual(w.getnchannels(), 2)
                self.assertEqual(w.getsampwidth(), 2)
                self.assertEqual(w.getframerate(), 44100)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_export_svg_and_summary(self):
        cadence = self.pacer.calculate_cadence(self.sample_text, target_wpm=160, words_per_fixation=2)
        audit = self.pacer.audit_cadence(cadence)
        timeline = self.pacer.generate_pacing_timeline(self.sample_text, target_wpm=160, words_per_fixation=2)

        svg = self.pacer.export_svg_pacer(timeline, cadence, audit)
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Saccadic Pacing &amp; Rhythm Metronome", svg)

        summary = SaccadicRhythmPacer.export_summary(cadence, audit, timeline)
        self.assertIn("# Saccadic Pacing & Rhythm Metronome Telemetry", summary)
        self.assertIn("Target Reading Cadence", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.rhythm_pacer as rp
        source = inspect.getsource(rp)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/rhythm_pacer.py")


if __name__ == "__main__":
    unittest.main()
