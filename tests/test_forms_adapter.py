#!/usr/bin/env python3
"""
Unit tests for SounnyForms AI multi-modal form adapter.
"""

import unittest
from scripts.forms_adapter import (
    clean_currency_and_number,
    adapt_dump_to_form,
    BUILTIN_SCHEMAS
)

class TestFormsAdapter(unittest.TestCase):

    def test_currency_normalization(self):
        self.assertEqual(clean_currency_and_number("$1.5m"), 1500000.0)
        self.assertEqual(clean_currency_and_number("250k"), 250000.0)
        self.assertEqual(clean_currency_and_number("50,000"), 50000.0)
        self.assertEqual(clean_currency_and_number("$1000"), 1000.0)

    def test_project_intake_mapping(self):
        dump = """
        Initiative: Distributed Spatial Index
        Goal: Sub-millisecond GeoAI inference on edge devices
        Budget: $500k
        PM: Anwar
        """
        result = adapt_dump_to_form(dump, "project_intake")
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["payload"]["project_name"], "Distributed Spatial Index")
        self.assertEqual(result["payload"]["budget"], 500000.0)
        self.assertEqual(len(result["missing_required"]), 0)

    def test_missing_required_fields(self):
        dump = "Budget: $10k"
        result = adapt_dump_to_form(dump, "project_intake")
        self.assertEqual(result["status"], "incomplete")
        self.assertIn("project_name", result["missing_required"])

    def test_grant_proposal_mapping(self):
        dump = """
        Title: TERRA Horizon Europe Climate EO
        Agency: European Research Council
        Amount: €1.8m
        Novelty: Multimodal satellite foundation model
        """
        result = adapt_dump_to_form(dump, "grant_proposal")
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["payload"]["grant_title"], "TERRA Horizon Europe Climate EO")
        self.assertEqual(result["payload"]["funding_program"], "European Research Council")
        self.assertEqual(result["payload"]["amount_requested"], 1800000.0)

if __name__ == "__main__":
    unittest.main()
