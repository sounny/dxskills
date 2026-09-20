# Changelog

Copy the `0.1.0` section below into the GitHub Release body when tagging `v0.1.0`. Later versions should be added above this section only when they ship.

Tagger checklist (do not paste this block into the Release):
- Tag name: `v0.1.0`
- Attach `dist/dxskills-v0.1.0.zip` as a Release asset
- Treat older internal draft checkpoints as history only, not public version numbers

---

## 0.1.0

**First public release of DxSkills.** Open-standard, MIT-licensed cognitive scaffolding that makes agentic AI naturally dyslexia-friendly. No account and no paywall.

Site: https://dxskills.sounny.com
Repo: https://github.com/sounny/dxskills
Gallery: https://github.com/sounny/dxskills/blob/main/EXAMPLES.md
License: [MIT](https://github.com/sounny/dxskills/blob/main/LICENSE)

### What ships

Six skills on disk (`skills/`):

| Skill | Command | What it does |
| :--- | :--- | :--- |
| `dx-dump` | `/dx dump` | Compiles raw notes and voice dumps into outlines, diagrams, and next steps. |
| `dx-read` | `/dx read` | Distills dense text into BLUF, tables, and decision matrices. |
| `dx-write` | `/dx write` | Silently polishes phonetic dictation while keeping authentic voice. |
| `dx-interview` | `/dx ask` | One-question-at-a-time drafting for grants, specs, and syllabi. |
| `dx-map` | `/dx map` | Syntax-safe Mermaid maps and spatial component matrices. |
| `dx-voice` | `/dx voice` | Speech-to-architecture from audio files or transcripts. |

Also included:
- D-Mode prompt cards in `prompts/` (ChatGPT, Claude, Gemini, Cursor, Obsidian)
- Interactive playground at https://dxskills.sounny.com
- Before/after gallery in `EXAMPLES.md`
- Offline bundle `dist/dxskills-v0.1.0.zip` (manifest: `dist/manifest.json`)
- IDE drop-in configs in `ide-configs/`

`VERSION` is `0.1.0`. That number is this public release, not a future milestone.

### Install (pick one)

**A. Paste D-Mode (zero install)**
Copy [`prompts/d-mode.md`](https://github.com/sounny/dxskills/blob/main/prompts/d-mode.md) into ChatGPT Custom Instructions, a Claude Project, or a Gemini Gem.

**B. Clone into your agent skills directory**
```bash
git clone https://github.com/sounny/dxskills.git skills/dxskills
```
Then tell your agent: "Install the DxSkills cognitive scaffolding suite from https://github.com/sounny/dxskills into my active agent skills directory and activate D-Mode."

**C. Offline zip**
Download `dxskills-v0.1.0.zip` from this Release (or from `dist/` on `main`). Unzip and point your agent at the extracted `skills/` folder.
