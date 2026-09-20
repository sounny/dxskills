# DxSkills

> **Open-standard AI skills, prompts, and cognitive scaffolding that make agentic AI naturally dyslexia-friendly.**
>
> 🌐 **Interactive Web Platform & Playground:** [https://dxskills.sounny.com](https://dxskills.sounny.com)

[![Version](https://img.shields.io/badge/version-0.1.0-0ea5e9.svg)](./CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Website](https://img.shields.io/badge/Web-dxskills.sounny.com-10b981.svg)](https://dxskills.sounny.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-DxSkills-0077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/company/146509128/)
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

## 🎨 Before & After Transformation Gallery

To see concrete, real-world examples of how DxSkills transforms raw dictation, cluttered notes, and dense text into high-signal deliverables:

👉 **[Explore the Visual Transformation Gallery (EXAMPLES.md)](./EXAMPLES.md)**

The gallery showcases side-by-side comparisons for:
- `dx-dump`: Chaotic mobile voice dumps converted into Steve Jobs executive specs.
- `dx-write`: Phonetic speech-to-text dictation polished into warm, collegial prose.
- `dx-read`: 5-paragraph bureaucratic policies distilled into 3-column decision matrices.
- `dx-interview`: Step-by-step 4-phase interview dialogue compiled into a complete grant proposal.
- `dx-map`: Verbal architectural descriptions transformed into syntax-safe Mermaid topologies.
- `dx-voice`: Speech memos and audio transcripts compiled into structured Markdown (see [`skills/dx-voice/SKILL.md`](./skills/dx-voice/SKILL.md)).

---

## 🧩 The Core Skills Suite

DxSkills is organized as a modular toolkit with formal YAML schemas, machine-readable contracts, and drop-in prompt cards. You can use the entire suite together or activate individual skills as needed.

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
│                   DxSkills (six skills on disk)                 │
├─────────────────┬─────────────────┬─────────────────────────────┤
│    dx-dump      │    dx-read      │          dx-write           │
│  Brain Dump to  │  Anti-Wall of   │     Authentic Voice &       │
│  Architecture   │      Text       │        Silent Polish        │
├─────────────────┼─────────────────┼─────────────────────────────┤
│  dx-interview   │     dx-map      │         dx-voice            │
│ 4-Phase Gated   │ Spatial Systems │    Speech-to-Architecture   │
│ Socratic Drafter│ Concept Mapper  │     Audio Dictation         │
└─────────────────┴─────────────────┴─────────────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ High-Signal Deliverable │
                    │ (Polished & Structured) │
                    └─────────────────────────┘
```

### 1. [`dx-dump`](./skills/dx-dump/SKILL.md) ([Standalone Prompt](./prompts/dx-dump.md))
* **The Problem:** Thoughts arrive as a rapid flood of fragments, voice dictations, and half-formed bullet points.
* **The Fix:** Ingests raw, unstructured notes and automatically decomposes them into:
  1. A clear hierarchical outline.
  2. A visual system diagram or flowchart.
  3. Actionable next steps and deliverables.
* **Result:** You never need to write in linear order; drop your ideas as they fire.
* **Command:** `/dx dump` (also `/dx napkin`, `/dx spec`)

### 2. [`dx-read`](./skills/dx-read/SKILL.md) ([Standalone Prompt](./prompts/dx-read.md))
* **The Problem:** Dense, unbroken paragraphs in academic memos, long emails, and bureaucratic reports trigger cognitive fatigue and visual tracking loss.
* **The Fix:** Re-renders incoming text with high-signal visual anchors:
  * 2-sentence **Bottom Line Up Front (BLUF)**.
  * Side-by-side comparison tables and decision matrices.
  * Generous white space with bold thematic signposts.
* **Result:** Grasp the entire situation in five seconds without getting trapped in filler text.
* **Command:** `/dx read` (also `/dx finance`)

### 3. [`dx-write`](./skills/dx-write/SKILL.md) ([Standalone Prompt](./prompts/dx-write.md))
* **The Problem:** Typical AI grammar checkers sterilize your text into robotic corporate filler, while standard spellcheckers constantly interrupt your flow.
* **The Fix:** Silently repairs phonetics, homophones, typos, and syntax in the background, while strictly preserving your authentic conversational warmth, directness, and cadence. Includes embedded phoneme normalization for spatial jargon (e.g. choropleth, LiDAR, isochrone).
* **Result:** No generic corporate cheerleading, no robotic platitudes, natural paragraphs, and zero em dashes.
* **Command:** `/dx write`

### 4. [`dx-interview`](./skills/dx-interview/SKILL.md) ([Standalone Prompt](./prompts/dx-interview.md))
* **The Problem:** Starting a complex document, grant proposal, or article from a blank page is a massive friction point. Models often rush ahead by asking four questions at once.
* **The Fix:** A disciplined 4-phase sequential state machine (`[Phase 1/3 - Target Audience & Stakes]`, `[Phase 2/3 - Core Thesis & Bottleneck]`, `[Phase 3/3 - Tangible Proof & Metrics]`, `[Phase 4 - Synthesis]`). Enforces asking exactly one question at a time and waiting for your response before advancing.
* **Result:** Blank-page anxiety and conversational overwhelm are completely eliminated.
* **Command:** `/dx ask`

### 5. [`dx-map`](./skills/dx-map/SKILL.md) ([Standalone Prompt](./prompts/dx-map.md))
* **The Problem:** Dyslexic thinkers think in spatial relationships, but conventional writing tools are strictly linear, while LLMs frequently generate broken Mermaid syntax.
* **The Fix:** Generates syntax-safe Mermaid.js diagrams with strict syntactical guardrails (mandatory label quoting `id["Label"]`, max 8-12 nodes per diagram, maximum depth 3) paired with an accompanying Markdown component matrix.
* **Result:** Clean, guaranteed-to-render visual alignment between mental models and documentation.
* **Command:** `/dx map` (also `/dx storyboard`, `/dx taxonomy`)

### 6. [`dx-voice`](./skills/dx-voice/SKILL.md) ([Standalone Prompt](./prompts/dx-voice.md))
* **The Problem:** Keyboard transcription is the slowest path for many spatial thinkers. Voice is faster, but raw transcripts are full of filler, phonetic errors, and linear clutter.
* **The Fix:** Takes audio files or speech transcripts, strips disfluencies, silently normalizes domain jargon, and compiles the result into structured Markdown.
* **Result:** A voice memo becomes a plan, spec, or email without a typing bottleneck.
* **Command:** `/dx voice`

---

## 💻 Drop-in IDE Configurations

Calibrate your coding assistants into D-Mode with ready-to-use configuration files:

👉 **[View the IDE Configuration Suite (ide-configs/)](./ide-configs/)**

Supported editors:
* **Cursor IDE:** Drop `.cursorrules` into your project root.
* **Claude Code CLI:** Drop `CLAUDE.md` and `.clauderc` into your project root.
* **Windsurf IDE:** Drop `.windsurfrules` into your workspace root.

Run the automated installer:
```bash
python ide-configs/install_ide_configs.py
```

---

## 🚀 Quickstart (one screen)

All three paths are MIT-licensed and free. No account and no paywall.

### A. Paste the D-Mode prompt card (zero install)

Copy **[prompts/d-mode.md](./prompts/d-mode.md)** into ChatGPT Custom Instructions, a Claude Project, or a Gemini Gem.

```markdown
# Role & Cognitive Mode: D-Mode Active
You are acting as a dedicated cognitive scaffold for a non-linear, spatial thinker.
1. Zero-Friction Input: Accept raw notes, fragments, and typos without comment. Focus purely on underlying intent.
2. Anti-Wall-of-Text: Never output dense paragraphs. For prose and replies, use short 1-3 sentence paragraphs without forced bullets. For structure and data, use clear hierarchies and tables.
3. Silent Polish: Quietly correct spelling, homophones, and grammar without lecturing or calling out mistakes.
4. Voice Preservation: Keep writing direct, grounded, warm, and authentic. Never convert natural conversation into bullet outlines. Eliminate robotic corporate filler and em dashes.
5. Systems-First: Explain workflows and processes with structured tables or Mermaid.js diagrams.
```

### B. Clone into your agent skills directory

```bash
git clone https://github.com/sounny/dxskills.git skills/dxskills
```

Then tell your agent:
> Install the DxSkills cognitive scaffolding suite from https://github.com/sounny/dxskills into my active agent skills directory and activate D-Mode.

Later updates: `/dx update` in chat, or `python scripts/check_updates.py`.

### C. Offline zip

Use [`dist/dxskills-v0.1.0.zip`](./dist/dxskills-v0.1.0.zip) from this repo now. After tag `v0.1.0` is published, the same zip is also a GitHub Release asset.

Unzip, then point your agent at the extracted `skills/` folder.

---

## What's in public release 0.1.0

`VERSION` is **0.1.0**. That is the first public GitHub Release, not a future milestone.

Included now:
- Six skills on disk: `dx-dump`, `dx-read`, `dx-write`, `dx-interview`, `dx-map`, `dx-voice`
- D-Mode prompt cards in `prompts/`
- Interactive playground: [https://dxskills.sounny.com](https://dxskills.sounny.com)
- Before/after gallery: [EXAMPLES.md](./EXAMPLES.md)
- Offline bundle: `dist/dxskills-v0.1.0.zip` (see `dist/manifest.json`)
- IDE drop-in configs in `ide-configs/`
- MIT License, free for personal, academic, and commercial use. No paywall.

Earlier internal draft checkpoints (core prompts, skill cards, interview, maps, IDE configs, examples) are already folded into this 0.1.0 package. They are not separate public version numbers.

Release notes (copy-paste ready for the GitHub Release body): [CHANGELOG.md](./CHANGELOG.md).

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
