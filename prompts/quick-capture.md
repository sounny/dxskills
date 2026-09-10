# Quick-Capture Setup: 1-Hotkey Thought Compilation

> **Objective:** Bind a single keyboard shortcut (e.g., `Cmd+Shift+D` or `Ctrl+Alt+D`) that takes whatever messy text or speech transcript is on your clipboard, runs it through D-Mode compilation, and puts clean Markdown back onto your clipboard.

---

## Method 1: Windows (PowerShell / AutoHotkey / PowerToys Run)

### Option A: Direct Shortcut (PowerShell)
Create a desktop shortcut or bind a key via PowerToys:
- **Target:** `powershell.exe -WindowStyle Hidden -File "g:\My Drive\dxskills\scripts\quick_capture.py"`

### Option B: AutoHotkey v2
Add this line to your `AutoHotkey.ahk` script:

```autohotkey
^!d:: ; Ctrl + Alt + D
{
    Run("python `"g:\My Drive\dxskills\scripts\quick_capture.py`"",, "Hide")
    ToolTip("D-Mode Compiled to Clipboard!")
    SetTimer () => ToolTip(), -1500
}
```

---

## Method 2: macOS (Raycast Script Command / Alfred Workflow)

### Raycast Script Command
Save as `~/.config/raycast/scripts/dx-capture.sh`:

```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title D-Mode Clipboard Compiler
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🧠
# @raycast.packageName DxSkills

python3 "$HOME/dxskills/scripts/quick_capture.py"
```

---

## How It Works in Practice
1. You dictate a fast voice memo or paste a messy raw bullet list into any text box.
2. Select all and press `Ctrl+C` (or `Cmd+C`).
3. Press your hotkey (`Ctrl+Alt+D` or `Cmd+Shift+D`).
4. Press `Ctrl+V` (or `Cmd+V`): your text is replaced with a clean BLUF, visual signposts, and a structured table.
