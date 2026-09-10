# Contributing to DxSkills

Thank you for your interest in contributing to DxSkills! We welcome contributions from spatial thinkers, dyslexic builders, educators, neurodiversity advocates, and software engineers.

---

## Core Contribution Philosophy

1. **Cognitive Scaffolding First:** We build tools that provide cognitive leverage rather than deficit-patching. Our skills empower high-speed non-linear ideation, spatial modeling, and authentic communication.
2. **Zero Shorthand Tax:** Contributions, issue reports, and discussions do not require formal polish or flawless spelling. Raw, direct ideas are always welcome.
3. **No Em Dashes (Hard Standard):** To prevent visual crowding and character-encoding glitches across legacy terminals and LLM wrappers, we strictly prohibit the Unicode em dash (U+2014) in all repository files. Use commas, hyphens, colons, or parentheses instead.

---

## How You Can Contribute

### 1. Proposing a New Modular Skill
If you have identified a recurring workflow where non-linear thinkers face friction:
1. Create a directory under `skills/your-skill-name/`.
2. Author a `SKILL.md` file adhering to our YAML frontmatter standard:
   ```yaml
   ---
   name: dx-your-skill
   description: 1-sentence summary of what cognitive bottleneck this skill resolves.
   command: /dx your-command
   version: 0.1.0
   ---
   ```
3. Define the operational heuristics, input tolerance rules, and standard output format.

### 2. Contributing Visual Mermaid Templates
Add useful, domain-specific visual diagrams to `skills/dx-map/templates/`:
- Use clean Mermaid syntax (`graph TD`, `graph LR`, `stateDiagram-v2`).
- Quote all node labels containing punctuation or parentheses.

### 3. Improving Prompt Presets
Help optimize the prompt presets in `prompts/` for emerging models (e.g., Claude 3.7 Sonnet, GPT-4.5, Gemini 2.5 Pro).

---

## Development & Testing Workflow

Before submitting a Pull Request, run the local regression test suite:

```bash
# Run unit tests and em-dash audit
python -m unittest tests/test_skills.py
```

All 4 test suites must pass:
1. Version consistency between `VERSION` and `SKILL.md`.
2. Existence and valid YAML frontmatter across all modular skills.
3. Existence and validity of all template files.
4. 100% compliance with the zero-em-dash rule across all repository files.

### Pull Request Process
1. Fork the repo and create your branch: `git checkout -b feature/my-new-skill`.
2. Commit your changes: `git commit -m "Add dx-research paper synthesis template"`.
3. Push to your fork: `git push origin feature/my-new-skill`.
4. Open a Pull Request on GitHub.
