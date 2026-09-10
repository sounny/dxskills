# DxSkills VS Code Extension

> **Speed-of-thought cognitive scaffolding, anti-wall-of-text compiler, and quiet typo normalizer for Visual Studio Code.**

---

## ⚡ What It Does

1. **Compile Selection (`ctrl+alt+d` / `cmd+alt+d`):** Takes disordered notes, transcripts, or brainstorm dumps and transforms them instantly into structured executive summaries (BLUF), key takeaways, and action matrices.
2. **Insert Diagram:** Injects production-ready Mermaid architecture, flywheel, state machine, or mindmap diagrams directly into your Markdown files.
3. **Quiet Typo Normalizer (`ctrl+alt+f` / `cmd+alt+f`):** Quietly normalizes common letter inversions (such as `teh` -> `the`, `recieve` -> `receive`, `seperate` -> `separate`) without triggering anxious red squiggly underlines.
4. **Local Gateway Support:** Connects automatically to your local `dxskills-gateway` (running via Docker or Python on port 8080) if available, with instantaneous deterministic fallback when offline.

---

## 🚀 Keybindings & Commands

| Command | Keybinding | Action |
| :--- | :--- | :--- |
| `DxSkills: Compile Selection` | `ctrl+alt+d` (Windows/Linux) / `cmd+alt+d` (macOS) | Structures highlighted text into D-Mode format |
| `DxSkills: Insert Architecture / Mindmap Diagram` | Command Palette (`Ctrl+Shift+P`) | Inserts Mermaid architecture diagrams |
| `DxSkills: Quietly Normalize Inversions and Typos` | `ctrl+alt+f` (Windows/Linux) / `cmd+alt+f` (macOS) | Stabilizes text without red squiggles |

---

## 🛠️ Configuration Settings

- `dxskills.gatewayUrl`: URL of the self-hosted DxSkills Gateway (default: `http://localhost:8080/compile`).
- `dxskills.quietFixOnSave`: When set to `true`, quietly fixes letter inversions every time you save a document.

---

## 📦 Building and Packaging

To package into a `.vsix` extension:

```bash
cd extensions/vscode-dxskills
npm install
npm run compile
npx @vscode/vsce package
```

Then install in VS Code via:
`code --install-extension dxskills-vscode-0.1.0.vsix`
