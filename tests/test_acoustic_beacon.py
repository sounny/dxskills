#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Spatial Audio Landmark & Acoustic Beacon Anchoring
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import wave
import json
import tempfile
import unittest

from scripts.acoustic_beacon import (
    SoundstageBeacon,
    ListenerPosition,
    AcousticBeaconEngine,
    ANCHOR_FREQUENCIES
)


class TestAcousticBeaconEngine(unittest.TestCase):
    """Tests for acoustic beacon extraction, binaural stereo panning, and WAV synthesis."""

    def setUp(self):
        self.engine = AcousticBeaconEngine()
        self.sample_canvas = {
            "nodes": [
                {"id": "node_hub1", "type": "text", "text": "Problem Statement Root", "x": 100, "y": 200, "width": 260, "height": 160},
                {"id": "node_hub2", "type": "text", "text": "Architecture Core", "x": 600, "y": 200, "width": 260, "height": 160},
                {"id": "node_hub3", "type": "text", "text": "Synthesis Terminal", "x": 350, "y": 600, "width": 260, "height": 160}
            ],
            "edges": [
                {"id": "e1", "fromNode": "node_hub1", "toNode": "node_hub2"},
                {"id": "e2", "fromNode": "node_hub2", "toNode": "node_hub3"}
            ]
        }

    def test_extract_beacons_from_canvas(self):
        beacons = self.engine.extract_beacons_from_canvas(self.sample_canvas, max_beacons=3)
        self.assertEqual(len(beacons), 3)

        # Node with highest degree should be first (node_hub2 has degree 2)
        top_beacon = beacons[0]
        self.assertEqual(top_beacon.node_id, "node_hub2")
        self.assertEqual(top_beacon.frequency, ANCHOR_FREQUENCIES[0][0])
        self.assertIn("Architecture", top_beacon.title)

    def test_calculate_binaural_gains(self):
        beacon_left = SoundstageBeacon(
            beacon_id="b1",
            node_id="n1",
            title="Left Beacon",
            x=100.0,
            y=300.0,
            frequency=432.0,
            tone_label="Grounding"
        )
        beacon_right = SoundstageBeacon(
            beacon_id="b2",
            node_id="n2",
            title="Right Beacon",
            x=500.0,
            y=300.0,
            frequency=528.0,
            tone_label="Core"
        )
        listener = ListenerPosition(x=300.0, y=300.0)

        # Left beacon: dx = -200, should have left_gain > right_gain
        lg_l, rg_l = self.engine.calculate_binaural_gains(beacon_left, listener)
        self.assertGreater(lg_l, rg_l)

        # Right beacon: dx = +200, should have right_gain > left_gain
        lg_r, rg_r = self.engine.calculate_binaural_gains(beacon_right, listener)
        self.assertGreater(rg_r, lg_r)

    def test_synthesize_wav_bytes(self):
        self.engine.extract_beacons_from_canvas(self.sample_canvas)
        duration = 0.5  # half second
        pcm_bytes = self.engine.synthesize_wav(duration_sec=duration)

        # 44100 samples/sec * 0.5 sec * 2 channels * 2 bytes/sample = 88200 bytes
        expected_len = int(duration * 44100) * 4
        self.assertEqual(len(pcm_bytes), expected_len)

    def test_write_wav_file(self):
        self.engine.extract_beacons_from_canvas(self.sample_canvas)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.engine.write_wav_file(tmp_path, duration_sec=0.25)
            self.assertTrue(os.path.exists(tmp_path))

            with wave.open(tmp_path, "rb") as wf:
                self.assertEqual(wf.getnchannels(), 2)
                self.assertEqual(wf.getsampwidth(), 2)
                self.assertEqual(wf.getframerate(), 44100)
                frames = wf.getnframes()
                self.assertEqual(frames, int(0.25 * 44100))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_export_soundstage_svg_and_summary(self):
        beacons = self.engine.extract_beacons_from_canvas(self.sample_canvas)
        svg = self.engine.export_soundstage_svg()

        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("3D Acoustic Landmark &amp; Soundstage Map", svg)
        self.assertIn("Listener (You)", svg)

        summary = AcousticBeaconEngine.export_summary(beacons)
        self.assertIn("# Spatial Audio Landmark & Acoustic Beacon Anchoring", summary)
        self.assertIn("432.0 Hz", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.acoustic_beacon as ab
        source = inspect.getsource(ab)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/acoustic_beacon.py")


if __name__ == "__main__":
    unittest.main()
