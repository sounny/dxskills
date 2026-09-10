#!/usr/bin/env python3
"""
Unit tests for Autonomous Cognitive Non-Linear Narrative Branching Simulator & Plot Mesh
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)
"""

import os
import json
import unittest

from scripts.narrative_brancher import (
    NarrativeBeat,
    PlotBranch,
    NarrativeAudit,
    NarrativeBranchingSimulator
)


class TestNarrativeBranchingSimulator(unittest.TestCase):
    """Tests for narrative beat addition, markdown parsing, causality tracking, and canvas export."""

    def setUp(self):
        self.sim = NarrativeBranchingSimulator()

    def test_add_beat_and_branch(self):
        b1 = self.sim.add_beat("Discovery of Anomaly", character="Vance", tension_level=40.0, act="Act 1")
        b2 = self.sim.add_beat("Hull Breach Warning", character="Vance", tension_level=85.0, act="Act 2")
        self.assertEqual(b1.character, "Vance")
        self.assertEqual(b2.tension_level, 85.0)

        br = self.sim.add_branch(b1.id, b2.id, condition="Sensor fails", consequence="Pressure drops")
        self.assertEqual(br.source_id, b1.id)
        self.assertEqual(br.target_id, b2.id)
        self.assertTrue(br.is_canonical)

    def test_parse_markdown_storyline(self):
        markdown_text = """
### Beat: The Mysterious Signal
- Character: Communications Officer
- Tension: 35
- Act: Act 1
- Description: Deep-space encrypted transmission intercepted.
- Leads To: Decryption Attempt | Condition: If quantum cipher holds

### Beat: Decryption Attempt
- Character: AI Specialist
- Tension: 60
- Act: Act 2
- Description: AI unravels anomalous code signature.
- Leads To: System Lockdown | Condition: If malware triggers
- Leads To: Safe Contact | Condition: If protocol verified

### Beat: System Lockdown
- Character: Security Lead
- Tension: 90
- Act: Act 3
- Description: Ship thrusters and shields locked down.
- Terminal: true

### Beat: Safe Contact
- Character: Diplomat
- Tension: 50
- Act: Act 3
- Description: Peaceful handshake established with extraterrestrial beacon.
- Terminal: true
"""
        self.sim.parse_markdown_storyline(markdown_text)
        self.assertEqual(len(self.sim.beats), 4)
        self.assertEqual(len(self.sim.branches), 3)

        audit = self.sim.audit_narrative()
        self.assertEqual(audit.total_beats, 4)
        self.assertEqual(audit.total_branches, 3)
        self.assertEqual(audit.dangling_threads_count, 0)
        self.assertGreater(audit.narrative_agency_score, 30.0)

    def test_dangling_threads_and_bottlenecks(self):
        # Beat without terminal status and no outgoing branches
        b1 = self.sim.add_beat("Fork Choice", is_terminal=False)
        b2 = self.sim.add_beat("Unresolved Branch", is_terminal=False)
        self.sim.add_branch(b1.id, b2.id)

        audit = self.sim.audit_narrative()
        self.assertEqual(audit.dangling_threads_count, 1)

        # Bottleneck test: converge 3 branches onto single beat
        b3 = self.sim.add_beat("Branch B")
        b4 = self.sim.add_beat("Branch C")
        target = self.sim.add_beat("Convergent Chokepoint", is_terminal=True)

        self.sim.add_branch(b2.id, target.id)
        self.sim.add_branch(b3.id, target.id)
        self.sim.add_branch(b4.id, target.id)

        audit2 = self.sim.audit_narrative()
        self.assertGreaterEqual(audit2.pacing_bottlenecks_count, 1)

    def test_export_canvas(self):
        b1 = self.sim.add_beat("Opening Incident", act="Act 1", tension_level=30.0)
        b2 = self.sim.add_beat("Climax Confrontation", act="Act 3", tension_level=95.0, is_terminal=True)
        self.sim.add_branch(b1.id, b2.id, condition="Evidence revealed")

        canvas_data = self.sim.export_canvas()
        self.assertIn("nodes", canvas_data)
        self.assertIn("edges", canvas_data)
        self.assertEqual(len(canvas_data["nodes"]), 2)
        self.assertEqual(len(canvas_data["edges"]), 1)

        # Check edge structure
        edge = canvas_data["edges"][0]
        self.assertEqual(edge["fromNode"], b1.id)
        self.assertEqual(edge["toNode"], b2.id)
        self.assertIn("Evidence revealed", edge["label"])

    def test_export_svg_and_summary(self):
        b1 = self.sim.add_beat("Act One Start", character="Hero", tension_level=20.0)
        b2 = self.sim.add_beat("Midpoint Shift", character="Rival", tension_level=70.0)
        b3 = self.sim.add_beat("Resolution", character="Hero", tension_level=40.0, is_terminal=True)
        self.sim.add_branch(b1.id, b2.id)
        self.sim.add_branch(b2.id, b3.id)

        svg = self.sim.export_svg()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("Non-Linear Narrative Branching Simulator", svg)

        audit = self.sim.audit_narrative()
        summary = NarrativeBranchingSimulator.export_summary(audit, list(self.sim.beats.values()))
        self.assertIn("# Non-Linear Narrative Branching Simulator", summary)
        self.assertIn("Narrative Agency Score", summary)

    def test_zero_em_dashes(self):
        import inspect
        import scripts.narrative_brancher as nb
        source = inspect.getsource(nb)
        self.assertNotIn(chr(8212), source, "Illegal em dash found in scripts/narrative_brancher.py")


if __name__ == "__main__":
    unittest.main()
