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

### Phase 9: Specialized Cognitive Templates & Multi-Modal Extensions
- [x] **Task 9.1:** Create `skills/dx-dump/templates/startup_pitch_compile.md` (Raw brainstorm to 10-slide venture narrative).
- [x] **Task 9.2:** Create `prompts/voice-card-calibration.md` (Personal tone and cadence calibration guide).
- [x] **Task 9.3:** Add an interactive "Download Skills Bundle" modal and direct install script in `index.html`.
- [x] **Task 9.4:** Add social share cards and OpenGraph preview optimization in `index.html`.

### Phase 10: Multi-Model Evaluation & Benchmark Corpus
- [x] **Task 10.1:** Create synthetic benchmark dataset `tests/benchmark_corpus.json` containing diverse disordered brainstorm transcripts across engineering, academic, startup, and executive domains.
- [x] **Task 10.2:** Build evaluation script `scripts/eval_benchmarks.py` calculating BLUF adherence, table completeness, and zero-em-dash compliance across models.
- [x] **Task 10.3:** Add interactive live playground in `index.html` where users can test quick-capture transformation directly in their browser with instant client-side execution.

### Phase 11: Academic & Research Writing Scaffolding
- [x] **Task 11.1:** Create `skills/dx-dump/templates/peer_review_rebuttal.md` (distill emotional review feedback into structured point-by-point defense matrix).
- [x] **Task 11.2:** Create `skills/dx-dump/templates/journal_cover_letter.md` (high-signal editor pitch highlighting novelty and methodology).
- [x] **Task 11.3:** Create `skills/dx-read/templates/literature_matrix_extract.md` (multi-paper synthesis matrix comparing variables, methods, and results).

### Phase 12: Native Raycast Extension & Terminal Utilities
- [x] **Task 12.1:** Scaffold `extensions/raycast-dxskills/` manifest and quick-capture action command (`d-mode-compile`, `d-mode-diagram`).
- [x] **Task 12.2:** Build local clipboard listener daemon script (`scripts/clipboard_listener.py`) for automated speed-of-thought capture.

### Phase 13: Local LLM Integration (Ollama & LM Studio)
- [x] **Task 13.1:** Create `scripts/ollama_bridge.py` for direct offline local inference supporting both Ollama and LM Studio APIs.
- [x] **Task 13.2:** Add Modelfile configurations for local Mistral / Llama 3 D-Mode agents (`models/Modelfile.llama3`, `models/Modelfile.mistral`).

### Phase 14: Visual Concept Matrix & Mindmap Exporters
- [x] **Task 14.1:** Build ASCII table and flowchart generator for terminal-only / ssh environments (`scripts/ascii_scaffold.py`).
- [x] **Task 14.2:** Add interactive mindmap viewer shell in `index.html` featuring Mermaid 10+ syntax.

### Phase 15: Voice Ingestion Real-Time Streaming
- [x] **Task 15.1:** Integrate faster-whisper real-time streaming audio pipeline into `skills/dx-voice/scripts/voice_transcribe.py`.
- [x] **Task 15.2:** Add browser Web Audio speech-to-text input button in `index.html` playground.

### Phase 16: Internationalization & Multilingual Scaffolding
- [x] **Task 16.1:** Add French cognitive prompts (`prompts/d-mode-fr.md`) for francophone spatial researchers.
- [x] **Task 16.2:** Add bilingual language toggle and French prompt tab in `index.html`.

### Phase 17: Enterprise & Self-Hosted Deployment
- [x] **Task 17.1:** Create Dockerfile and `docker-compose.yml` for self-hosted D-Mode gateway with local Whisper and Ollama.
- [x] **Task 17.2:** Add health check endpoints, compilation API, and latency telemetry dashboard (`server/gateway.py`).

### Phase 18: VS Code Native Extension & Editor Scaffolding
- [x] **Task 18.1:** Scaffold `extensions/vscode-dxskills/` with status bar quick-capture command.
- [x] **Task 18.2:** Add automatic typo auto-fixer that operates quietly without red squiggly anxiety.

### Phase 19: Cognitive Load Analytics & Productivity Telemetry
- [x] **Task 19.1:** Add cognitive load reduction estimator calculating phonological working memory cycles saved per compiled deliverable (`scripts/cognitive_load_calc.py`).
- [x] **Task 19.2:** Add real-time telemetry badge in web interface (`index.html`).

### Phase 20: Automated PDF & Typography Exporter
- [x] **Task 20.1:** Create Typst and Pandoc executive briefing templates (`templates/executive_briefing.typ`).
- [x] **Task 20.2:** CLI command `dx_cli.py export --format pdf` for 1-click Swiss-style PDF export.

### Phase 21: Autonomous Webhook Receiver for Speed-of-Thought Voice Ingestion
- [x] **Task 21.1:** Build multi-channel webhook receiver (`server/webhook_receiver.py`) accepting audio recordings from Telegram, Slack, and WhatsApp.
- [x] **Task 21.2:** Auto-route received audio to Whisper transcription and D-Mode structured outputs.

### Phase 22: Team Collaboration Profiles & Architectural Review Matrix
- [x] **Task 22.1:** Create role-specific cognitive review lenses (`prompts/team-review-engineering.md`, `prompts/team-review-executive.md`).
- [x] **Task 22.2:** Add multi-perspective synthesis template for resolving architectural disagreements without wall-of-text debates (`skills/dx-read/templates/architectural_conflict_resolution.md`).

### Phase 23: Interactive Terminal TUI & Keyboard Scaffolding Navigation
- [x] **Task 23.1:** Create standalone terminal TUI (`scripts/dx_tui.py`) with split-pane live structuring and vim/arrow key navigation.
- [x] **Task 23.2:** Add fast keyboard shortcuts for 1-click diagram and table template injection.

### Phase 24: Real-Time Event Telemetry & Status API
- [x] **Task 24.1:** Build real-time event log and streaming stats endpoint in `server/gateway.py`.
- [x] **Task 24.2:** Add live telemetry stream and active server status monitor in web interface (`index.html`).

### Phase 25: Git Pre-Commit Hook & Automated Linter
- [x] **Task 25.1:** Create `scripts/pre_commit_hook.py` verifying zero em dashes, valid frontmatter, and compilation benchmarks before commit.
- [x] **Task 25.2:** Add fast installation script `scripts/install_git_hook.py` to auto-link hook into `.git/hooks/pre-commit`.

### Phase 26: Cognitive Load Reduction Matrix Visualizer on Web Portal
- [x] **Task 26.1:** Add interactive comparison matrix in `index.html` visualizing phonetic loop savings across all 10 benchmark corpus types.
- [x] **Task 26.2:** Add downloadable JSON telemetry reports directly from the benchmark matrix.

### Phase 27: Full-Text Search & Quick-Filter Command Palette
- [x] **Task 27.1:** Implement keyboard shortcut `/` or `Ctrl+K` search modal in `index.html` to instantly filter all 6 modular skills, 13 templates, and platform presets with zero latency.
- [x] **Task 27.2:** Add fuzzy tag filtering for domain-specific categories (executive, academic, engineering, voice, research).

### Phase 28: Offline Progressive Web Application & Desktop PWA Manifest
- [x] **Task 28.1:** Add `manifest.webmanifest`, service worker offline caching, and desktop PWA installation support.
- [x] **Task 28.2:** Add custom monochrome SVG icons for standalone desktop and mobile home screen launching.

### Phase 29: Accessibility Evaluation & High-Contrast OpenDyslexic Mode
- [x] **Task 29.1:** Add OpenDyslexic font toggle and enhanced letter-spacing mode in `index.html` for users with visual crowding symptoms.
- [x] **Task 29.2:** Add WCAG 2.1 AAA contrast audit and automated accessibility compliance test in `tests/test_accessibility.py`.

### Phase 30: SounnyForms & AI Agent Multi-Modal Form Ingestion Adapter (Next Cycles)
- [ ] **Task 30.1:** Add schema adapter for bidirectional sync with `SounnyForms` unstructured field parsing.
- [ ] **Task 30.2:** Create JSON schema mapper (`scripts/forms_adapter.py`) converting voice dumps into validated form payloads.

### Phase 31: Multi-Turn Socratic Clarification Tree UI Widget
- [ ] **Task 31.1:** Add interactive branching question widget in `index.html` simulating `dx-interview` clarifying dialogue.
- [ ] **Task 31.2:** Auto-compile answered branch nodes into a unified project specification block.

---

## 📝 Execution Log (Updated Every 10 Minutes)

| Cycle | Timestamp | Task Completed | Output Files | Git Commit |
| :--- | :--- | :--- | :--- | :--- |
| **Initial** | 2026-09-10 19:04 | Core Suite v0.1.0 Released | `SKILL.md`, `skills/*`, `scripts/*` | `8ffce8e` |
| **Cycle 1** | 2026-09-10 19:10 | Platform Presets & Research Basis | `prompts/*`, `RESEARCH.md`, `CITATION.cff` | `6ecc498` |
| **Cycle 2** | 2026-09-10 19:20 | Modular Templates, CLI & Diagram Showcase | `skills/*`, `scripts/*`, `index.html` | `772b22c` |
| **Cycle 3** | 2026-09-10 19:30 | Test Suite, Obsidian Scaffolding & Quick-Capture | `tests/*`, `scripts/quick_capture.py`, `prompts/*` | `b881a82` |
| **Cycle 4** | 2026-09-10 19:40 | Community Guidelines, CI/CD Actions & Issue Templates | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/*` | `e070e67` |
| **Cycle 5** | 2026-09-10 19:50 | Venture Pitch Scaffolding, Voice Calibration & Modal Bundle | `skills/dx-dump/*`, `prompts/*`, `index.html` | `6a96c7c` |
| **Cycle 6** | 2026-09-10 20:02 | Benchmark Evaluation Suite, 10-Corpus Test & Live Browser Playground | `tests/benchmark_corpus.json`, `scripts/eval_benchmarks.py`, `index.html` | `2baa1de` |
| **Cycle 7** | 2026-09-10 20:05 | Academic Scaffolding Suite: Peer Review, Cover Letter & Literature Matrix | `skills/dx-dump/*`, `skills/dx-read/*` | `a698472` |
| **Cycle 8** | 2026-09-10 20:12 | Native Raycast Extension & Background Clipboard Daemon | `extensions/raycast-dxskills/*`, `scripts/clipboard_listener.py` | `8b0bb23` |
| **Cycle 9** | 2026-09-10 20:22 | Local LLM Suite: Ollama Bridge, Llama 3 & Mistral Modelfiles | `models/*`, `scripts/ollama_bridge.py` | `d3d43ad` |
| **Cycle 10** | 2026-09-10 20:32 | Terminal ASCII Scaffolding & Live Web Concept Mindmap | `scripts/ascii_scaffold.py`, `index.html` | `be7d5c3` |
| **Cycle 11** | 2026-09-10 20:42 | Whisper Audio Pipeline & Browser Web Audio Dictation | `skills/dx-voice/*`, `index.html` | `9af66e7` |
| **Cycle 12** | 2026-09-10 20:52 | Multilingual Scaffolding: French D-Mode & Navbar Language Toggle | `prompts/d-mode-fr.md`, `index.html` | `450f965` |
| **Cycle 13** | 2026-09-10 21:02 | Self-Hosted Container Gateway & Docker Compose Stack | `server/gateway.py`, `Dockerfile`, `docker-compose.yml` | `79a2115` |
| **Cycle 14** | 2026-09-10 21:22 | VS Code Native Extension & Quiet Typo Stabilizer | `extensions/vscode-dxskills/*`, `index.html` | `423de01` |
| **Cycle 15** | 2026-09-10 21:32 | Cognitive Load Reduction Estimator & Live Telemetry Badges | `scripts/cognitive_load_calc.py`, `index.html` | `ebb0e48` |
| **Cycle 16** | 2026-09-10 21:42 | Typst & HTML Swiss Executive Briefing Exporter | `templates/executive_briefing.*`, `scripts/dx_cli.py` | `4db9dc7` |
| **Cycle 17** | 2026-09-10 21:52 | Multi-Channel Webhook Receiver & Docker Compose Service | `server/webhook_receiver.py`, `docker-compose.yml` | `533428f` |
| **Cycle 18** | 2026-09-10 22:02 | Team Review Lenses & Conflict Resolution Matrix | `prompts/team-review-*`, `skills/dx-read/templates/*` | `cad20e7` |
| **Cycle 19** | 2026-09-10 22:12 | Interactive Terminal TUI & CLI Subcommand Integration | `scripts/dx_tui.py`, `scripts/dx_cli.py` | `8e9c97a` |
| **Cycle 20** | 2026-09-10 22:22 | Real-Time Event Telemetry API & Live Web Gateway Monitor | `server/gateway.py`, `index.html` | `b0176ef` |
| **Cycle 21** | 2026-09-10 22:32 | Automated Pre-Commit Hook & Git Quality Gatekeeper | `scripts/pre_commit_hook.py`, `scripts/install_git_hook.py` | `3efa129` |
| **Cycle 22** | 2026-09-10 22:42 | Cognitive Load Reduction Matrix Visualizer & Telemetry JSON Exporter | `index.html`, `dist/*` | `93e2c75` |
| **Cycle 23** | 2026-09-10 22:52 | Full-Text Search & Quick-Filter Command Palette | `index.html`, `dist/*` | `fd6fa88` |
| **Cycle 24** | 2026-09-10 23:02 | Offline Progressive Web App (PWA) & Service Worker Cache | `manifest.webmanifest`, `sw.js`, `icons/*`, `index.html` | `3322d71` |
| **Cycle 25** | 2026-09-10 23:12 | OpenDyslexic Font Mode & WCAG 2.1 AAA Accessibility Suite | `index.html`, `tests/test_accessibility.py` | `95bb446` |












