# DxSkills Autonomous 24-Hour Development Backlog

> **Objective:** Systematically develop the DxSkills open-standard cognitive scaffolding suite, modular skills, tooling, platform configs, and web documentation over 24 hours (every 10 minutes).  
> **Repository:** `https://github.com/sounny/dxskills`  
> **Local Path:** `G:\My Drive\dxskills\`  
> **Hard Rule:** Strictly NO em dashes (Unicode U+2014) anywhere in code, markdown, comments, or prompts. Use hyphens, commas, colons, or parentheses.

---

## 🧭 Milestone Roadmap

### Phase 1: Platform Presets & Configs (Ready-to-Use Files)
- [x] **Task 1.1:** Create `prompts/cursorrules.md` (optimized `.cursorrules` file for Cursor IDE).
- [x] **Task 1.2:** Create `prompts/claude-project.md` (optimized system instructions for Claude Projects).
- [x] **Task 1.3:** Create `prompts/chatgpt-custom-instructions.md` (two-part setup for ChatGPT Custom Instructions).
- [x] **Task 1.4:** Create `prompts/gemini-gem.md` (custom instructions for Google Gemini Gems).

### Phase 2: Scientific & Cognitive Foundation
- [x] **Task 2.1:** Create `RESEARCH.md` (empirical backing from Eide & Eide, cognitive load theory, spatial reasoning vs. linear phonological loops, and working memory scaffolding).
- [x] **Task 2.2:** Create `CITATION.cff` (formal citation metadata for academic and institutional references).

### Phase 3: Modular Skill Expansion & Templates
- [x] **Task 3.1:** Build `skills/dx-map/templates/` containing 5 plug-and-play Mermaid templates:
  - `system_architecture.mmd`
  - `curriculum_map.mmd`
  - `strategy_flywheel.mmd`
  - `state_machine.mmd`
  - `decision_matrix.mmd`
- [x] **Task 3.2:** Build `skills/dx-interview/templates/` containing high-leverage question trees:
  - `grant_proposal_interview.md`
  - `technical_design_interview.md`
  - `course_syllabus_interview.md`
  - `executive_briefing_interview.md`
- [x] **Task 3.3:** Build `skills/dx-read/templates/` containing cognitive intake templates:
  - `academic_paper_distill.md`
  - `meeting_transcript_digest.md`
  - `policy_memo_reframe.md`
- [x] **Task 3.4:** Create `skills/dx-voice/SKILL.md` (Speech-to-Architecture skill integrating with local Whisper transcriber).

### Phase 4: CLI Tooling & Automation
- [x] **Task 4.1:** Build `scripts/dx_cli.py` (standalone Python CLI tool to compile brain dumps, run anti-wall-of-text transformations, and check updates locally).
- [x] **Task 4.2:** Build `scripts/bundle_skills.py` (packaging script to generate single-click zip archives and distribution bundles).

### Phase 5: Landing Page & Web Experience
- [x] **Task 5.1:** Enhance `index.html` with direct modal tabs or copy blocks for Cursor, Claude, ChatGPT, and Gemini presets.
- [x] **Task 5.2:** Add a visual diagram gallery showcase to `index.html` displaying live rendered Mermaid examples.
- [x] **Task 5.3:** Add downloadable `.zip` / JSON skill manifest links to the web navigation.

### Phase 6: Sync & Quality Assurance
- [x] **Task 6.1:** Verify zero em dashes across all files.
- [x] **Task 6.2:** Sync updates from `g:\My Drive\dxskills\` to `g:\My Drive\skills\dxskills` and `C:\Users\sounn\.gemini\config\skills\dxskills`.
- [x] **Task 6.3:** Commit and push all additions to GitHub repository (`origin/main`).

### Phase 7: Advanced Workflows & Testing Harness
- [x] **Task 7.1:** Build automated regression test suite `tests/test_skills.py` verifying YAML frontmatter, schema validity, and zero em dashes across all templates.
- [x] **Task 7.2:** Create Obsidian Vault Community Plugin integration guide and template cards (`prompts/obsidian-d-mode.md`).
- [x] **Task 7.3:** Create raycast/alfred quick-capture snippets for macOS/Windows clipboard compilation (`scripts/quick_capture.py` and `prompts/quick-capture.md`).
- [x] **Task 7.4:** Add interactive copy buttons for individual Mermaid templates in `index.html`.

### Phase 8: Open-Source Community & Governance
- [x] **Task 8.1:** Create `CONTRIBUTING.md` with guidelines for contributing new cognitive templates and prompts.
- [x] **Task 8.2:** Create `CODE_OF_CONDUCT.md` establishing a welcoming, neurodivergent-friendly standard.
- [x] **Task 8.3:** Create GitHub issue templates for bug reports and new skill proposals (`.github/ISSUE_TEMPLATE/`).
- [x] **Task 8.4:** Build an automated GitHub Action workflow (`.github/workflows/test.yml`) running `tests/test_skills.py` on push and pull requests.

### Phase 9: Specialized Cognitive Templates & Multi-Modal Extensions (Upcoming Cycles)
- [ ] **Task 9.1:** Create `skills/dx-dump/templates/startup_pitch_compile.md` (Raw brainstorm to 10-slide venture narrative).
- [ ] **Task 9.2:** Create `prompts/voice-card-calibration.md` (Personal tone and cadence calibration guide).
- [ ] **Task 9.3:** Add an interactive "Download Skills Bundle" modal and direct install script in `index.html`.
- [ ] **Task 9.4:** Add social share cards and OpenGraph preview optimization in `index.html`.

---

## 📝 Execution Log (Updated Every 10 Minutes)

| Cycle | Timestamp | Task Completed | Output Files | Git Commit |
| :--- | :--- | :--- | :--- | :--- |
| **Initial** | 2026-09-10 19:04 | Core Suite v0.1.0 Released | `SKILL.md`, `skills/*`, `scripts/*` | `8ffce8e` |
| **Cycle 1** | 2026-09-10 19:10 | Platform Presets & Research Basis | `prompts/*`, `RESEARCH.md`, `CITATION.cff` | `6ecc498` |
| **Cycle 2** | 2026-09-10 19:20 | Modular Templates, CLI & Diagram Showcase | `skills/*`, `scripts/*`, `index.html` | `772b22c` |
| **Cycle 3** | 2026-09-10 19:30 | Test Suite, Obsidian Scaffolding & Quick-Capture | `tests/*`, `scripts/quick_capture.py`, `prompts/*` | `b881a82` |
| **Cycle 4** | 2026-09-10 19:40 | Community Guidelines, CI/CD Actions & Issue Templates | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/*` | `pending` |
