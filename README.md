# DxSkills

> **Open-standard AI skills, prompts, and cognitive scaffolding that make agentic AI naturally dyslexia-friendly.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/sounny/dxskills/pulls)

---

## 💡 The Philosophy: Cognitive Leverage Over Deficit Patching

Most software treats dyslexia as a reading and spelling deficit to be patched with elementary tools: basic spellcheckers, text-to-speech, and simplified reading levels.

**DxSkills starts from the opposite premise.**

Decades of cognitive science (notably Dr. Brock and Fernette Eide's research in *The Dyslexic Advantage*) demonstrate that the dyslexic mind is naturally wired for:
* **High-dimensional spatial reasoning:** Visualizing 3D structures, geographic systems, and complex architectures.
* **Interconnected thinking:** Seeing macro patterns, cross-disciplinary relationships, and non-linear feedback loops.
* **Rapid parallel ideation:** Developing complete, multi-layered solutions at the speed of thought.

### The Bottleneck
The bottleneck is never the thinking; it is the **linear, sequential transcription**. Writing forces high-speed, multidimensional concepts through a single-file pipeline: one letter and one word at a time. Dense walls of uniform text cause severe visual fatigue, while mechanical spelling traps slow down creative and intellectual momentum.

**DxSkills provides the cognitive scaffolding.** It acts as an intelligent compiler between non-linear thinking and structured, polished output, allowing dyslexic thinkers to operate with AI at their full potential.

---

## 🧩 The Core Skills Suite

DxSkills is organized as a modular toolkit. You can use the entire suite together or activate individual skills as needed.

```
                    ┌─────────────────────────┐
                    │   Non-Linear Thinker    │
                    │ (Spatial / Rapid Ideas) │
                    └────────────┬────────────┘
                                 │
                   [ Raw Input / Brain Dump ]
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                            DxSkills                             │
├─────────────────┬─────────────────┬─────────────────────────────┤
│    dx-dump      │    dx-read      │          dx-write           │
│  Brain Dump to  │  Anti-Wall of   │     Authentic Voice &       │
│  Architecture   │      Text       │        Silent Polish        │
├─────────────────┼─────────────────┴─────────────────────────────┤
│  dx-interview   │                   dx-map                      │
│ Socratic Q&A to │             Spatial & Systems                 │
│  Draft Document │               Concept Mapper                  │
└─────────────────┴───────────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ High-Signal Deliverable │
                    │ (Polished & Structured) │
                    └─────────────────────────┘
```

### 1. `dx-dump` (Brain Dump to Architecture)
* **The Problem:** Thoughts arrive as a rapid flood of fragments, voice dictations, and half-formed bullet points.
* **The Fix:** Ingests raw, unstructured notes and automatically decomposes them into:
  1. A clear hierarchical outline.
  2. A visual system diagram or flowchart.
  3. Actionable next steps and deliverables.
* **Result:** You never need to write in linear order; drop your ideas as they fire.

### 2. `dx-read` (Anti-Wall-of-Text)
* **The Problem:** Dense, unbroken paragraphs in academic memos, long emails, and bureaucratic reports trigger cognitive fatigue and visual tracking loss.
* **The Fix:** Re-renders incoming text with high-signal visual anchors:
  * 2-sentence **Bottom Line Up Front (BLUF)**.
  * Side-by-side comparison tables and decision matrices.
  * Generous white space with bold thematic signposts.
* **Result:** You grasp the entire situation in five seconds without getting trapped in filler text.

### 3. `dx-write` (Voice Preservation & Silent Polish)
* **The Problem:** Typical AI grammar checkers sterilize your text into bland, robotic corporate filler, while standard spellcheckers constantly interrupt your flow.
* **The Fix:** Silently repairs phonetics, homophones, typos, and syntax in the background, while strictly preserving your authentic conversational warmth, directness, and cadence.
* **Result:** No generic corporate cheerleading, no robotic platitudes, and zero em dashes.

### 4. `dx-interview` (Socratic Drafter)
* **The Problem:** Starting a complex document, grant proposal, or article from a blank page is a massive friction point.
* **The Fix:** The AI takes the role of an interviewer. It asks 3 to 4 targeted, multiple-choice or forcing questions. You answer rapidly using speech-to-text or short phrases, and the AI drafts the linear prose from your spoken logic.
* **Result:** Blank-page anxiety is completely eliminated.

### 5. `dx-map` (Spatial Concept Mapper)
* **The Problem:** Dyslexic thinkers think in spatial relationships, but conventional writing tools are strictly linear.
* **The Fix:** Automatically generates Mermaid.js flowcharts, state charts, quadrant diagrams, and concept maps for any idea, process, or curriculum.
* **Result:** Instant visual alignment between how you imagine a system and how it is documented.

---

## 🚀 Quickstart: Using DxSkills Today

DxSkills is designed to work across all major AI platforms:

### Option A: ChatGPT / Claude Custom Instructions (Zero Install)
Grab the standalone **[D-Mode Prompt Card](./prompts/d-mode.md)** and paste it directly into your ChatGPT Custom Instructions, Claude Project, or Gemini Gem:

👉 **[View the Full D-Mode Prompt Card](./prompts/d-mode.md)**

```markdown
# Role & Cognitive Mode: D-Mode Active
You are acting as a dedicated cognitive scaffold for a non-linear, spatial thinker.
1. Zero-Friction Input: Accept raw notes, fragments, and typos without comment. Focus purely on underlying intent.
2. Anti-Wall-of-Text: Never output dense paragraphs. Use bold headers, bullet hierarchies, tables, and white space.
3. Silent Polish: Quietly correct spelling, homophones, and grammar without lecturing or calling out mistakes.
4. Voice Preservation: Keep writing direct, grounded, warm, and authentic. Eliminate robotic corporate filler and em dashes.
5. Systems-First: Explain workflows and processes with structured tables or Mermaid.js diagrams.
```

### Option B: Agentic AI (Antigravity / Claude Code)
Clone this repository directly into your agent skills directory:

```bash
git clone https://github.com/sounny/dxskills.git
```

Reference the modular `skills/` folders in your workflows or trigger them directly with `/dx`.

---

## 📂 Repository Roadmap

- [x] **v0.1:** Core architecture, README manifesto, and universal system prompt.
- [ ] **v0.2:** Standalone `SKILL.md` definitions for `dx-dump`, `dx-read`, and `dx-write`.
- [ ] **v0.3:** Interactive Socratic interview templates for academic and professional writing.
- [ ] **v0.4:** Mermaid.js visual template library for spatial concept mapping.
- [ ] **v0.5:** Ready-to-use Cursor rules (`.cursorrules`) and Claude Project presets.

---

## 🤝 Contributing

We welcome contributions from dyslexic builders, spatial scientists, educators, and AI researchers. Whether it is a new prompt pattern, an agentic skill specification, or a visual template, pull requests are welcome!

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/new-dx-skill`).
3. Commit your changes (`git commit -m 'Add dx-interview template'`).
4. Push to the branch (`git push origin feature/new-dx-skill`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE). It is completely free and open for personal, academic, and commercial use.

---

**Built with pride by spatial thinkers, for spatial thinkers.**
