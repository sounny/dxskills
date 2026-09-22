#!/usr/bin/env python3
"""
Regression tests for the dx-plan skill CLI handler.
Verifies ordered checklist output, time-block table, silent polish, and zero em dashes.
"""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import scripts.dx_cli as dx_cli


class _Args:
    def __init__(self, input="", horizon="day"):
        self.input = input
        self.horizon = horizon


def _run_plan(text, horizon="day"):
    buf = io.StringIO()
    with redirect_stdout(buf):
        dx_cli.cmd_plan(_Args(input=text, horizon=horizon))
    return buf.getvalue()


class TestDxPlan(unittest.TestCase):

    SAMPLE = (
        "need to submit the grant by thursday. still havent finished the budget section. "
        "sarah has to review the methods. also need to email the letters of support ppl."
    )

    def test_outputs_bluf(self):
        out = _run_plan(self.SAMPLE)
        self.assertIn("Bottom Line Up Front", out)

    def test_outputs_start_here(self):
        out = _run_plan(self.SAMPLE)
        self.assertIn("Start Here", out)

    def test_ordered_checklist_is_numbered_with_checkboxes(self):
        out = _run_plan(self.SAMPLE)
        self.assertIn("1. [ ]", out)
        self.assertIn("4. [ ]", out)

    def test_time_block_table_renders(self):
        out = _run_plan(self.SAMPLE)
        self.assertIn("| Step | Focus Block | Energy | Done |", out)
        self.assertIn("| :--- | :--- | :--- | :--- |", out)

    def test_detects_deadline(self):
        out = _run_plan(self.SAMPLE)
        self.assertIn("Thursday", out)

    def test_silent_polish_fixes_typos(self):
        out = _run_plan(self.SAMPLE)
        self.assertIn("haven't", out)
        self.assertIn("people", out)
        self.assertNotIn("havent", out)
        self.assertNotIn(" ppl", out)

    def test_zero_em_dashes(self):
        out = _run_plan(self.SAMPLE)
        self.assertEqual(out.count("\u2014"), 0)

    def test_empty_input_produces_fallback(self):
        out = _run_plan("   ")
        self.assertIn("Define the goal", out)

    def test_horizon_is_reported(self):
        out = _run_plan(self.SAMPLE, horizon="project")
        self.assertIn("project", out)

    def test_focus_block_values_are_valid(self):
        out = _run_plan(self.SAMPLE)
        self.assertTrue(any(b in out for b in ["15 min", "25 min", "45 min"]))


if __name__ == "__main__":
    unittest.main()
