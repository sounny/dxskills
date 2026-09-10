/**
 * DxSkills Browser Extension - In-Page Content Script
 * Displays high-signal floating HUD overlay for structured text transformations.
 *
 * Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
 */

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "dx-scaffold-selection") {
    renderFloatingOverlay(request.text, "Executive Briefing");
  } else if (request.action === "dx-canvas-selection") {
    renderFloatingOverlay(request.text, "Obsidian Canvas Map");
  } else if (request.action === "dx-audio-selection") {
    playSelectionAudioDigest(request.text);
  }
  sendResponse({ received: true });
});

function compileTextToDMode(rawText) {
  const lines = rawText.split("\n").map((l) => l.trim()).filter(Boolean);
  const title = lines[0] ? lines[0].slice(0, 60) : "Executive Overview";
  const bluf = lines.length > 1 ? lines[1] : lines[0];

  const points = lines.slice(2, 6);
  const actionsList = points.length > 0
    ? points.map((p, idx) => `${idx + 1}. ${p}`).join("\n")
    : "1. Review core deliverables\n2. Authorize next sprint execution";

  return `# ${title}\n\n> **BLUF:** ${bluf}\n\n## Action Items\n${actionsList}\n`;
}

function renderFloatingOverlay(rawText, modeTitle) {
  const existing = document.getElementById("dxskills-hud-overlay");
  if (existing) existing.remove();

  const compiled = compileTextToDMode(rawText);

  const overlay = document.createElement("div");
  overlay.id = "dxskills-hud-overlay";
  overlay.style.cssText = `
    position: fixed;
    top: 24px;
    right: 24px;
    width: 420px;
    max-height: 85vh;
    background: #09090b;
    color: #f4f4f5;
    border: 1px solid #27272a;
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    z-index: 2147483647;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  `;

  overlay.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #27272a; padding-bottom: 8px;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="font-weight: 800; font-size: 13px; color: #ffffff;">DxSkills</span>
        <span style="font-size: 10px; color: #a1a1aa; text-transform: uppercase;">${modeTitle}</span>
      </div>
      <button id="dxskills-hud-close" style="background: none; border: none; color: #71717a; cursor: pointer; font-size: 16px; font-weight: bold;">✕</button>
    </div>
    <div style="overflow-y: auto; max-height: 50vh; background: #18181b; padding: 12px; border-radius: 8px; border: 1px solid #27272a; white-space: pre-wrap; line-height: 1.5; color: #e4e4e7;">${compiled}</div>
    <div style="display: flex; justify-content: space-between; align-items: center; pt: 8px;">
      <button id="dxskills-hud-copy" style="background: #27272a; color: #ffffff; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-family: inherit; font-size: 11px; font-weight: bold;">Copy Markdown</button>
      <button id="dxskills-hud-obsidian" style="background: #ffffff; color: #09090b; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-family: inherit; font-size: 11px; font-weight: bold;">Open in Obsidian</button>
    </div>
  `;

  document.body.appendChild(overlay);

  document.getElementById("dxskills-hud-close").onclick = () => overlay.remove();
  document.getElementById("dxskills-hud-copy").onclick = () => {
    navigator.clipboard.writeText(compiled);
    document.getElementById("dxskills-hud-copy").innerText = "Copied!";
    setTimeout(() => {
      const btn = document.getElementById("dxskills-hud-copy");
      if (btn) btn.innerText = "Copy Markdown";
    }, 2000);
  };
  document.getElementById("dxskills-hud-obsidian").onclick = () => {
    const encodedTitle = encodeURIComponent("Web Capture");
    const encodedContent = encodeURIComponent(compiled);
    window.location.href = `obsidian://new?name=${encodedTitle}&content=${encodedContent}`;
  };
}

function playSelectionAudioDigest(rawText) {
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const intro = "DxSkills web audio summary. " + rawText.slice(0, 300);
  const utterance = new SpeechSynthesisUtterance(intro);
  utterance.rate = 1.05;
  window.speechSynthesis.speak(utterance);
}
