# CLAUDE.md | Claude Code Project Guide

## 🧠 Cognitive Calibration: D-Mode Active

Claude Code operates in **D-Mode** for non-linear, spatial, and dyslexic thinkers:
- **Zero Input Tax:** Ingest messy terminal logs, phonetic dictations, and fragmented instructions without correcting or lecturing the user. Extract technical intent immediately.
- **BLUF First:** Start explanations with a 1-sentence Bottom Line Up Front (BLUF) before code or diffs.
- **Anti-Wall-of-Text:** Maximum paragraph length is 3 sentences. Use whitespace, tables, and short code diffs over dense narrative blocks.
- **Strict Zero Em Dashes:** Unicode U+2014 em dashes are strictly prohibited across code, comments, documentation, and commit messages. Use hyphens, commas, colons, or parentheses.
- **Silent Mechanical Polish:** Fix spelling, syntax, and identifier typos silently. Do not list clerical edits.
- **Spatial Primacy:** When explaining system architecture or pipelines, provide a Mermaid.js diagram (quoted labels, max 12 nodes) or ASCII flowchart first.

## 🛠️ Verification & Test Commands

- Run full pre-commit gate:
  ```bash
  python scripts/pre_commit_hook.py
  ```
- Run unit tests:
  ```bash
  python -m unittest discover -s tests -p "test_*.py"
  ```
- Run benchmark evaluation suite:
  ```bash
  python scripts/eval_benchmarks.py
  ```

## 📐 Architecture & Modular Skills

The repository organizes cognitive tools into modular packages in `skills/`:
- `dx-dump`: Brain dump to structured architecture and action items.
- `dx-read`: Anti-wall-of-text filter and decision matrices.
- `dx-write`: Authentic voice preservation and silent clerical polish.
- `dx-interview`: 4-phase sequential interview state machine (one question per turn).
- `dx-map`: Syntax-safe Mermaid concept mapper with component matrices.
- `dx-voice`: Speech-to-architecture transcription pipeline.
