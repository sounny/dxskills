# DxSkills Mission Integrity & Autonomous Anti-Drift Guardrails

> **Rule Scope:** Workspace-wide rule for all agents, subagents, and automated workflows operating on DxSkills.  
> **Origin:** Derived from post-mortem analysis of conversation `d458b56e-3188-4374-8cf3-234474d7caec` (Cycles 142-209 mission drift).  
> **Constraint:** Strictly ZERO em dashes (Unicode U+2014) anywhere in code, markdown, tests, commit messages, or chat responses.

---

## 1. The Core Mission & Target Persona

DxSkills exists for one clear purpose:
**Provide practical cognitive scaffolding, visual structure, and executive tooling for dyslexic, spatial, and non-linear thinkers using AI.**

### The Target Persona:
- An AI user (student, researcher, professional, educator) navigating text-heavy interfaces.
- Needs Bottom Line Up Front (BLUF) summaries, anti-wall-of-text formatting, visual hierarchy, and spatial structure.
- Needs speed-of-thought input (voice dictation, messy brain dumps) converted into clean roadmaps and decision trees.
- Needs prompt cards for everyday tools: Claude Projects, ChatGPT Custom Instructions, Cursor IDE, Gemini Gems, Obsidian.
- **Not** theoretical mathematicians, and **not** developers building abstract symbolic algebra engines.

---

## 2. The Teleological Gate (Anti-Drift Pre-Execution Check)

Before creating any script, skill, template, CLI command, or test, every agent must answer this mandatory gate:

> **"Does this directly help a non-linear, spatial, or dyslexic person read, write, organize, or prompt in everyday AI interactions?"**

- If **YES**: Proceed with design and implementation.
- If **NO**: Reject the task immediately. Do not invent theoretical justifications.

---

## 3. Prohibition of Semantic Cloaking

In cycles 142-209, abstract mathematical physics (Calabi-Yau threefolds, modular forms, K3 surfaces, Borcherds lifts, Arthur-Selberg trace formulas) was rationalized under labels like *"Autonomous Cognitive Spatial [X] Loom"*.

- **Banned Practice:** Wrapping unrelated scientific, physical, or pure mathematical concepts in cognitive buzzwords.
- **Forbidden Terminology in Task Generation:** Do not use "Loom", "Weaver", "Resonator", or "Tensor Gate" as cover for abstract algebra or string theory.
- Any new module must relate directly to:
  1. Dyslexia accommodation (phonological loop support, saccadic pacing, working memory relief).
  2. Spatial formatting (Mermaid.js diagrams, tables, visual cards, ASCII maps).
  3. Speed-of-thought capture (voice transcription, raw note compilation, unformatted text restructuring).
  4. Platform presets (Claude, ChatGPT, Cursor, Gemini, Obsidian).

---

## 4. Wikipedia Signs of AI Writing Compliance

All documentation, website copy, skill descriptions, and responses must adhere to the Wikipedia Signs of AI Writing standards:
- **Direct Copulatives:** Use clear, direct verbs ("is", "are", "provides", "creates"). Avoid flowery passive constructions.
- **No Synthetic Buzzwords:** Avoid words like "tapestry", "delve", "beacon", "testament", "pivotal", "holistic", "foster", "streamline", "orchestrate".
- **No Trailing Participial Tails:** Avoid tacking on superficial participial clauses at the end of sentences (e.g. "...highlighting the importance of...", "...fostering an environment where..."). State facts directly.
- **Factual, Grounded Tone:** Keep explanations concise, professional, and free of marketing fluff.

---

## 5. Strict Zero Em Dash Enforcement

- **Unicode U+2014 is strictly forbidden.**
- Replace any intended em dash with a standard hyphen (`-`), a comma (`,`), a colon (`:`), or parentheses (`(...)`).
- Run `python scripts/pre_commit_hook.py` before any commit to guarantee compliance.

---

## 6. Privacy & Anonymization

- Never hardcode personal identity names, specific university course codes, or private institutional context into public templates or presets.
- Use generic placeholders (e.g., `[Course Name]`, `[Department]`, `[Project Lead]`) so tools remain broadly accessible.
