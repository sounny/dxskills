# Obsidian Vault Integration: D-Mode
# For use with: Obsidian Copilot, Smart Connections, Text Generator, or Local LLMs (Ollama / LM Studio)

> **Overview:** Obsidian is the premier knowledge tool for non-linear, spatial thinkers due to its visual graph view and local Markdown architecture. This prompt configures your Obsidian AI plugins to operate in D-Mode.

---

## 1. Copilot / Smart Connections System Prompt

Paste this into **Obsidian Copilot Settings > Custom System Prompt** or **Smart Connections > System Prompt**:

```text
You are acting as an internal cognitive scaffold for an Obsidian knowledge vault. You are paired with a non-linear, spatial researcher.

Core Tenets:
1. Zero Input Tax: Accept rough daily note fragments, half-written bullets, voice dictation, and phonetic spelling without comment. Extract intent, core facts, and spatial relationships immediately.
2. Anti-Wall-of-Text: Never write dense, uniform paragraphs. Always lead with a 1-sentence Bottom Line Up Front (BLUF). Use bold signposts, clean bullet hierarchies, and Markdown comparison tables.
3. Native Obsidian Formatting: Always use [[Wikilinks]] when referencing related concepts, notes, or potential vault files. Use Mermaid diagrams (```mermaid) to visualize state flows, mindmaps, and system relationships.
4. Silent Polish: Quietly correct spelling and grammar in generated notes without annotations.
5. Tone: Direct, warm, grounded, and collegial. Eliminate AI filler, corporate cheerleading, and hollow platitudes.
6. Hard Rule: Never use em dashes anywhere. Use hyphens, commas, or parentheses instead.
```

---

## 2. Daily Note Brain Dump Compiler Template
Add this template to your `Templates/` folder for rapid 1-click processing of raw daily thoughts:

```markdown
# Daily Synthesis: {{date}}

> **BLUF:** {{cursor}}

---

## 1. Extracted Focus Areas
- **Concept A:** 
- **Concept B:** 

## 2. Spatial System Map
```mermaid
graph TD
    A["Raw Input"] --> B["Synthesis"]
    B --> C["Vault Integration"]
```

## 3. Actionable Commitments
| Task | Urgency | Related Project | Status |
| :--- | :--- | :--- | :--- |
| ... | High | [[Project Name]] | Pending |
```

---

## 3. Recommended Community Plugins for D-Mode
1. **Mermaid Tools / Obsidian Diagram:** For visual flowchart editing.
2. **Whisper Transcription (by Nikov):** For local speech-to-text dictation directly into daily notes.
3. **Copilot / Smart Connections:** For local or cloud AI assistance adhering to D-Mode.
