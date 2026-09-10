#!/usr/bin/env python3
"""
Unit Tests for DxSkills Autonomous Desktop Menubar Companion & Local Daemon
Verifies floating HUD compiler, typo normalizer, Obsidian URI generation,
and headless daemon iteration loop.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys
import unittest

# Ensure repository root is in sys.path
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_DIR not in sys.path:
    sys.path.insert(0, REPO_DIR)

import scripts.desktop_companion as dc

class TestDesktopCompanion(unittest.TestCase):

    def setUp(self):
        self.companion = dc.DesktopCompanion(headless=True)
        self.sample_messy = "dx: teh plan for yestreday was to fix runing architechture. first setup monitoring. second verify backups. third deploy to prod."

    def test_initialization_headless(self):
        self.assertTrue(self.companion.headless)
        self.assertFalse(self.companion.running)
        self.assertIsNone(self.companion.launch_floating_hud())

    def test_compile_text_with_typo_correction(self):
        res = self.companion.compile_text(self.sample_messy)
        self.assertIn("The plan for yesterday", res["markdown"])
        self.assertIn("architecture", res["markdown"])
        self.assertGreaterEqual(res["typos_fixed"], 2)

    def test_compile_text_bluf_and_structure(self):
        res = self.companion.compile_text(self.sample_messy)
        self.assertEqual(res["title"], "Desktop Scaffolding Note")
        self.assertTrue(res["bluf"].startswith("The plan"))
        self.assertTrue(len(res["pillars"]) > 0)
        self.assertTrue(len(res["actions"]) > 0)
        self.assertIn("> **BLUF:**", res["markdown"])
        self.assertIn("## Core Architecture", res["markdown"])
        self.assertIn("## Action Vectors", res["markdown"])

    def test_obsidian_uri_generated(self):
        res = self.companion.compile_text(self.sample_messy)
        self.assertTrue(res["obsidian_uri"].startswith("obsidian://new?"))
        self.assertIn("Desktop%20Scaffolding%20Note", res["obsidian_uri"])

    def test_zero_em_dash_enforcement(self):
        bad_input = f"dx: first milestone {chr(8212)} very critical. second milestone ok."
        res = self.companion.compile_text(bad_input)
        self.assertTrue(res["zero_em_dash_clean"])
        self.assertNotIn(chr(8212), res["markdown"])

    def test_daemon_loop_bounded_iteration(self):
        # Mock get_system_clipboard so subprocess powershell is not spawned in unit tests
        orig_get = dc.get_system_clipboard
        try:
            dc.get_system_clipboard = lambda: ""
            self.companion.run_daemon_loop(poll_interval=0.001, max_iterations=1)
            self.assertFalse(self.companion.running)
        finally:
            dc.get_system_clipboard = orig_get

if __name__ == "__main__":
    unittest.main()
