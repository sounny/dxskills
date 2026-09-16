# DxSkills IDE Configuration Suite

This directory contains drop-in configuration files that calibrate AI coding agents into **D-Mode** (universal cognitive scaffolding for non-linear, spatial, and dyslexic thinkers).

---

## 📦 Supported Environments

| Environment | Config File | Purpose |
| :--- | :--- | :--- |
| **Cursor IDE** | `.cursorrules` | Project-level instructions for Cursor composer and chat. |
| **Claude Code CLI** | `CLAUDE.md`, `.clauderc` | Project memory and runtime flags for Anthropic's Claude Code CLI. |
| **Windsurf IDE** | `.windsurfrules` | Project rules for Codeium's Windsurf Cascade agent. |

---

## 🚀 Quick Installation

Run the automated installer script from your repository root:

```bash
# Install all IDE configs into current repository root
python ide-configs/install_ide_configs.py

# Install configs into a different project directory
python ide-configs/install_ide_configs.py --target /path/to/another/project

# Install only Cursor configuration
python ide-configs/install_ide_configs.py --ide cursor

# Use symlinks instead of file copies (supported on Linux/macOS and developer-mode Windows)
python ide-configs/install_ide_configs.py --mode symlink
```

---

## 🛠️ Manual Installation

If you prefer manual setup:
1. **Cursor:** Copy `ide-configs/.cursorrules` to your project root as `.cursorrules`.
2. **Claude Code:** Copy `ide-configs/CLAUDE.md` and `ide-configs/.clauderc` to your project root.
3. **Windsurf:** Copy `ide-configs/.windsurfrules` to your project root as `.windsurfrules`.
