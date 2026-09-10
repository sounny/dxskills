#!/usr/bin/env python3
import os
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, 'index.html')

class TestSocraticInterviewWidget(unittest.TestCase):

    def setUp(self):
        self.true(os.path.isfile(INDEX_PATH), 'index.html must exist')
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            self.html = f.read()

    def true(self, cond, msg):
        self.true = self.true(cond, msg) if hasattr(self, '_true') else self.assertTrue(cond, msg)

    def test_simulator_interview_tab_and_view(self):
        self.assertIn('id="sim-tab-interview"', self.html)
        self.assertIn('id="sim-view-interview"', self.html)
        self.assertIn("switchSimulatorView('interview')", self.html)

    def test_interview_dom_elements(self):
        required = [
            'id="interview-step-indicator"',
            'id="interview-progress-bar"',
            'id="interview-breadcrumbs"',
            'id="interview-step-phase"',
            'id="interview-question-title"',
            'id="interview-options-container"',
            'id="interview-custom-input"',
            'id="interview-prev-btn"',
            'id="interview-next-btn"',
            'id="interview-compiled-output"',
            'copyInterviewSpec()',
            'sendInterviewToPlayground()',
            'downloadInterviewSpec()',
            'resetInterviewTree()',
        ]
        for elem in required:
            self.assertIn(elem, self.html, f"Element {elem} missing")

    def test_domain_tracks_exist(self):
        for track in ['executive', 'technical', 'pitch', 'syllabus']:
            self.assertIn(f'id="tree-track-{track}"', self.html)
            self.assertIn(f"switchInterviewTrack('{track}')", self.html)

    def test_socratic_trees_data_structure(self):
        self.assertIn('const socraticInterviewTrees =', self.html)
        self.assertIn('initSocraticInterview()', self.html)

    def test_zero_em_dashes(self):
        em_dash = '\u2014'
        self.assertNotIn(em_dash, self.html, 'index.html must contain zero em dashes')

if __name__ == '__main__':
    unittest.main()
