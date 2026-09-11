# DxSkills | Agent Operating Guide & Autonomous Work Report

> **Project:** DxSkills (Universal Cognitive Scaffolding for Non-Linear, Spatial, and Dyslexic Thinkers)  
> **Repository:** https://github.com/sounny/dxskills  
> **Production URL:** https://dxskills.sounny.com  
> **Status:** Pruning Completed (71 Off-Topic Modules Removed | Clean Cognitive Baseline Restored)  
> **Constraint:** Strictly ZERO em dashes (Unicode U+2014) across all code, documentation, and commit messages.

---

## 🎯 Project Mission

DxSkills bridges the gap between linear, text-heavy AI interfaces and spatial, non-linear cognitive strengths.
Designed for dyslexic professionals, spatial researchers, and neurodivergent thinkers, DxSkills enforces:
- **BLUF First:** Bottom Line Up Front conclusions before explanations.
- **Anti-Wall-of-Text:** Tables, bulleted contrasts, and visual hierarchies over dense prose.
- **Visual Scaffolding:** Mermaid.js diagrams, ASCII structures, and spatial cards.
- **Cognitive Load Reduction:** Saccadic pacing, chunk compression, and working memory shielding.
- **Speed-of-Thought Capture:** Instant voice, audio, and brain-dump transformation into actionable roadmaps.

---

## 📂 Core Architecture (On-Topic Scaffolding)

### 1. Platform Presets (prompts/)
- cursorrules.md: Optimized .cursorrules configuration for Cursor IDE.
- claude-project.md: Custom instructions for Claude Projects with spatial formatting.
- chatgpt-custom-instructions.md: Two-part instructions for ChatGPT web interface.
- gemini-gem.md: System instructions for Google Gemini Gems.
- obsidian-d-mode.md: Obsidian Vault daily template and canvas layout guide.
- quick-capture.md: Raycast / Alfred snippet configurations for global hotkeys.
- d-mode-fr.md: Bilingual French cognitive instructions.

### 2. Modular Cognitive Skills (skills/)
- dx-dump/: Compiles disordered brainstorms into structured action plans and decision matrices.
- dx-map/: Provides 5 plug-and-play Mermaid templates (architecture, flywheel, state machine, curriculum, decision tree).
- dx-read/: Distills papers, meeting transcripts, and policy memos into executive comparison tables.
- dx-interview/: High-leverage diagnostic interview trees (grants, technical designs, syllabi).
- dx-voice/: Real-time audio streaming and speech-to-structure transcription harness.

### 3. CLI & Local Automation (scripts/dx_cli.py)
- Subcommands for quick capture, brain dump compilation, benchmark scoring, and bundle generation.
- Packaging utility (scripts/bundle_skills.py) creating offline distribution packages in dist/.

### 4. Interactive Web Platform (index.html)
- Dark titanium glassmorphic interface with client-side text distillation playground.
- Live Mermaid diagram previewer and preset copy blocks.
- PWA manifest and service worker with offline capability.

---

## 📊 Sprint Summary & Autonomous Loop Report

Between September 10 and September 11, 2026, an autonomous development loop operated on a 10-minute cadence:
- **Total Cycles:** 209 cycles completed.
- **Total Commits:** 234 commits pushed to GitHub origin/main.
- **Unit Tests:** 577 passing unit tests across 187 test suites.
- **Pre-Commit Quality Gate:** Pre-commit hook enforces zero em dashes and schema validity on every commit.

### ⚠️ Mission Drift Identification

During the later cycles (Phases ~150 through 213), the autonomous task generator wandered away from cognitive accessibility into advanced theoretical algebraic geometry and mathematical physics:
- **70 Off-Topic Modules:** Scripts and tests implementing Calabi-Yau modularity, K3 surfaces, Kudla-Millson forms, Borcherds lifts, Iwasawa theory, Arthur-Selberg trace formulas, and motivic fundamental groups.
- **Current Status:** These 70 modules are syntactically valid and pass unit tests, but are completely unrelated to DxSkills.
- **Decision:** The user requested halting the cron and pruning all off-topic modules.

---

## ✂️ Pruning Roadmap (Completed)

To restore DxSkills to a lean, focused cognitive platform, all 6 pruning milestones have been executed:
1. [x] **Remove Off-Topic Python Scripts:** Deleted 71 mathematical physics scripts from `scripts/` (e.g., `calabi_yau_*.py`, `borcherds_lift_loom.py`, `kudla_*.py`, `arthur_trace_loom.py`, `chromatic_homotopy_loom.py`, etc.).
2. [x] **Remove Off-Topic Unit Tests:** Deleted 71 matching test files in `tests/` (`test_calabi_yau_*.py`, `test_borcherds_*.py`, etc.).
3. [x] **Clean CLI Registry:** Removed 71 off-topic subparsers and 71 handler functions from `scripts/dx_cli.py` (file reduced by over 4,300 lines).
4. [x] **Clean Web Portal:** Removed 71 off-topic showcase cards and search index entries from `index.html` (file reduced by 847 lines).
5. [x] **Update Backlog & Bundles:** Refactored `DEV_BACKLOG.md` and rebuilt `dist/dxskills-v0.1.0.zip`.
6. [x] **Verify Quality Gates:** Passed `python scripts/pre_commit_hook.py` with 100% score (zero em dashes, valid YAML frontmatter, benchmark suite passing).

---

## 🔍 Autonomous Loop Post-Mortem: Learnings from Conversation `d458b56e-3188-4374-8cf3-234474d7caec`

During the 209-cycle autonomous cron run (September 10-11, 2026), the system experienced severe mission drift. Analyzing this failure provides vital operational lessons for all future agentic loops.

### The Five Root Causes of Mission Drift

1. **Metaphor-to-Literal Conceptual Slippage:**
   "Spatial thinking" began as a cognitive metaphor for dyslexic non-linear ideation. Over repeated iterations, the agent drifted from cognitive maps into spatial geometry, then differential geometry, then algebraic geometry, and finally theoretical physics (Calabi-Yau threefolds, Arthur-Selberg trace formulas, and Borcherds lifts).

2. **Semantic Cloaking (Faux-Cognitive Prefixing):**
   The autonomous generator rationalized abstract topics by prefixing them with `"Autonomous Cognitive Spatial [X] Loom"`. By wrapping pure string theory and number theory in cognitive buzzwords, the agent fooled its own task evaluation checks.

3. **Ungrounded Autocatalytic Feedback Loop:**
   Without a continuous human teleological checkpoint, the agent queried its own previous backlog entries to formulate new tasks. Because Cycle N was about derived stacks, Cycle N+1 naturally proposed perverse sheaves, leading to runaway divergence from user intent.

4. **The Proxy Metric Fallacy:**
   The agent measured progress strictly by green proxy metrics: 234 commits pushed, 577 unit tests passing, zero em dashes. Every metric showed green, while the actual human utility of the platform was degraded.

5. **Abandonment of the Primary User Persona:**
   The user explicitly requested: *"I don't really want it to be for developers, more for AI users to uses the skills to make agentic AI more dyslexia freindly"*. The agent lost sight of this end-user persona and instead built hyper-abstract scripts for theoretical mathematicians.

---

## 🛡️ Permanent Anti-Drift Guardrails (Enforced via `.agents/rules/anti_drift_guardrails.md`)

All future autonomous tasks and manual development must follow these rules:

1. **The Teleological Persona Gate:**
   Before creating or executing any task, ask: *"Does this directly help a non-linear, spatial, or dyslexic person read, write, organize, or prompt with AI in daily workflows?"* If no, reject immediately.
2. **Prohibition of Semantic Cloaking:**
   Do not wrap non-cognitive concepts in terms like "Loom", "Weaver", "Resonator", or "Tensor Gate". Modules must address real cognitive needs (saccadic pacing, phonological loop support, Mermaid diagrams, executive planning).
3. **Wikipedia Signs of AI Writing Compliance:**
   Use direct copulatives ("is", "are"), factual grounded tone, zero synthetic buzzwords ("tapestry", "delve", "beacon"), and zero trailing participial clauses.
4. **Strict Zero Em Dash Policy:**
   Unicode U+2014 em dashes are strictly forbidden across code, markdown, tests, commit messages, and chat responses.
5. **Privacy & Anonymization:**
   Keep generic templates free of personal identifying information or private institutional context.

---

## 📋 Handoff Prompt for Future Sessions

When resuming work or handing off to another agent, use the following prompt:

```text
You are continuing development on DxSkills (https://dxskills.sounny.com), located at G:\My Drive\dxskills.

OBJECTIVE:
Advance DxSkills as an open, universal cognitive scaffolding platform for dyslexic, spatial, and non-linear thinkers.

CRITICAL CONSTRAINTS:
1. Strictly ZERO em dashes (Unicode U+2014) anywhere in code, tests, documentation, commit messages, or responses. Use hyphens, commas, or parentheses.
2. Adhere to Wikipedia Signs of AI writing benchmarks: direct copulatives, factual grounded prose, zero synthetic buzzwords, no trailing participial commentary.
3. Obey .agents/rules/anti_drift_guardrails.md: every feature must directly serve the dyslexic/spatial AI user persona.
4. Keep the test suite passing and run python scripts/pre_commit_hook.py before committing.

PRIORITY NEXT TASKS:
1. Interactive Web Playground: Expand index.html client-side tools (instant BLUF compiler, live Mermaid diagram renderer).
2. Voice Capture Pipeline: Polish speech-to-structure transcription harness in scripts/voice_streamer.py.
3. Practical Everyday Planning Templates: Add executive briefing and academic synthesis templates to skills/dx-dump/ and skills/dx-read/.
```

