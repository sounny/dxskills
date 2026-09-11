#!/usr/bin/env python3
"""
DxSkills Automated Regression & Integrity Test Suite
Verifies YAML frontmatter, file integrity, and zero em dash compliance.
"""

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestDxSkillsIntegrity(unittest.TestCase):

    def test_version_consistency(self):
        version_file = os.path.join(ROOT_DIR, "VERSION")
        self.assertTrue(os.path.isfile(version_file), "VERSION file must exist")
        with open(version_file, "r", encoding="utf-8") as f:
            version = f.read().strip()
        self.assertTrue(len(version) > 0, "VERSION must not be empty")

        skill_master = os.path.join(ROOT_DIR, "SKILL.md")
        with open(skill_master, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn(f"version: {version}", content, "Master SKILL.md version must match VERSION file")

    def test_modular_skills_exist(self):
        expected_skills = ["dx-dump", "dx-read", "dx-write", "dx-interview", "dx-map", "dx-voice"]
        for skill in expected_skills:
            skill_path = os.path.join(ROOT_DIR, "skills", skill, "SKILL.md")
            self.assertTrue(os.path.isfile(skill_path), f"SKILL.md must exist for {skill}")
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertTrue(content.startswith("---"), f"{skill} must start with YAML frontmatter")
            self.assertIn(f"name: {skill}", content, f"{skill} frontmatter must declare its name")

    def test_templates_exist(self):
        expected_templates = [
            os.path.join(ROOT_DIR, "skills", "dx-map", "templates", "system_architecture.mmd"),
            os.path.join(ROOT_DIR, "skills", "dx-map", "templates", "curriculum_map.mmd"),
            os.path.join(ROOT_DIR, "skills", "dx-map", "templates", "strategy_flywheel.mmd"),
            os.path.join(ROOT_DIR, "skills", "dx-map", "templates", "decision_matrix.mmd"),
            os.path.join(ROOT_DIR, "skills", "dx-map", "templates", "state_machine.mmd"),
            os.path.join(ROOT_DIR, "skills", "dx-interview", "templates", "grant_proposal_interview.md"),
            os.path.join(ROOT_DIR, "skills", "dx-interview", "templates", "technical_design_interview.md"),
            os.path.join(ROOT_DIR, "skills", "dx-interview", "templates", "course_syllabus_interview.md"),
            os.path.join(ROOT_DIR, "skills", "dx-interview", "templates", "executive_briefing_interview.md"),
            os.path.join(ROOT_DIR, "skills", "dx-read", "templates", "academic_paper_distill.md"),
            os.path.join(ROOT_DIR, "skills", "dx-read", "templates", "meeting_transcript_digest.md"),
            os.path.join(ROOT_DIR, "skills", "dx-read", "templates", "policy_memo_reframe.md"),
        ]
        for t in expected_templates:
            self.assertTrue(os.path.isfile(t), f"Template must exist: {t}")
            self.assertGreater(os.path.getsize(t), 50, f"Template file must have content: {t}")

    def test_zero_em_dashes(self):
        em_dash = "\u2014"
        violations = []
        for root, dirs, files in os.walk(ROOT_DIR):
            dirs[:] = [d for d in dirs if d not in {".git", "dist", "__pycache__", "node_modules", ".vscode", "out"}]
            for file in files:
                if file.endswith((".md", ".html", ".py", ".mmd", ".cff", ".json")):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for line_idx, line in enumerate(f, 1):
                            if em_dash in line:
                                rel_path = os.path.relpath(filepath, ROOT_DIR)
                                violations.append(f"{rel_path}:{line_idx}")

        self.assertEqual(len(violations), 0, f"Found {len(violations)} em dash violations: {violations}")

if __name__ == "__main__":
    unittest.main()
