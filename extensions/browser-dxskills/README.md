# DxSkills Browser Extension (Chrome, Brave, Edge & Firefox)

> **Manifest V3 Cognitive Scaffolding & Anti-Wall-of-Text Tool**  
> Turn dense web articles, messy slack transcripts, and disjointed brain dumps into structured D-Mode deliverables right inside your browser.

---

## ⚡ Key Features

1. **Right-Click Context Menu Actions:**
   - Highlight any dense text on any webpage.
   - Right-click and choose **"DxSkills: Restructure to D-Mode Brief"**.
   - Instant floating HUD overlay renders the high-signal executive structure.
2. **Obsidian Vault 1-Click Injection:**
   - Open restructured notes directly in your local Obsidian vault via `obsidian://new`.
3. **Instant Spoken Audio Digest:**
   - Listen to a 60-second synthesized audio overview before reading to anchor concepts spatially.
4. **Standalone Popup Scaffolder:**
   - Click the extension icon in your browser toolbar to compile quick dumps or scratchpad fragments on the fly.

---

## 🚀 Installation Guide

### Google Chrome / Brave / Edge
1. Clone or download this repository (`https://github.com/sounny/dxskills`).
2. Open your browser and navigate to `chrome://extensions` (or `edge://extensions` / `brave://extensions`).
3. Toggle on **Developer mode** in the top-right corner.
4. Click **Load unpacked**.
5. Select the folder: `extensions/browser-dxskills/`.
6. The DxSkills icon will now appear in your browser extension toolbar!

### Mozilla Firefox
1. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`.
2. Click **Load Temporary Add-on...**.
3. Select `extensions/browser-dxskills/manifest.json`.
4. The extension will be loaded and active across your tabs.

---

## 🛡️ Privacy & Local Computation

- **100% Client-Side:** Text structuring, speech synthesis, and clipboard operations occur strictly in your local browser sandbox.
- **Zero Third-Party Telemetry:** No external server calls, tracking pixels, or third-party cookies.
- **Zero Em Dash Standard:** Enforces strict hyphens, commas, or parentheses formatting.
