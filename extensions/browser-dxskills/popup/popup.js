/**
 * DxSkills Browser Extension - Popup Controller
 * Manages instant in-browser compilation, Obsidian URI routing, and speech synthesis.
 *
 * Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
 */

document.addEventListener("DOMContentLoaded", () => {
  const inputElem = document.getElementById("popup-input");
  const outputElem = document.getElementById("popup-output");
  const compileBtn = document.getElementById("compile-btn");
  const audioBtn = document.getElementById("audio-btn");
  const copyBtn = document.getElementById("copy-btn");
  const obsidianBtn = document.getElementById("obsidian-btn");

  // Load buffered selection if present
  if (chrome.storage && chrome.storage.local) {
    chrome.storage.local.get("activeScaffold", (data) => {
      if (data && data.activeScaffold && data.activeScaffold.text) {
        inputElem.value = data.activeScaffold.text;
        compile();
      }
    });
  }

  function compile() {
    const raw = inputElem.value.trim();
    if (!raw) {
      outputElem.innerText = "Please paste some notes or an article excerpt above.";
      return;
    }

    const lines = raw.split("\n").map((l) => l.trim()).filter(Boolean);
    const title = lines[0] ? lines[0].slice(0, 50) : "Quick Synthesis";
    const bluf = lines.length > 1 ? lines[1] : lines[0];
    const items = lines.slice(2, 6);

    const actionList = items.length > 0
      ? items.map((it, idx) => `${idx + 1}. ${it}`).join("\n")
      : "1. Triage priorities\n2. Authorize next sprint execution";

    const result = `# ${title}\n\n> **BLUF:** ${bluf}\n\n## Action Items\n${actionList}\n`;
    outputElem.innerText = result;
  }

  compileBtn.onclick = compile;

  copyBtn.onclick = () => {
    const text = outputElem.innerText;
    navigator.clipboard.writeText(text).then(() => {
      copyBtn.innerText = "Copied!";
      setTimeout(() => {
        copyBtn.innerText = "Copy Markdown";
      }, 2000);
    });
  };

  obsidianBtn.onclick = () => {
    const text = outputElem.innerText;
    const lines = text.split("\n").filter(Boolean);
    const title = lines[0] ? lines[0].replace(/^#+\s*/, "") : "Web Synthesis";
    const uri = `obsidian://new?name=${encodeURIComponent(title)}&content=${encodeURIComponent(text)}`;
    window.open(uri, "_blank");
  };

  audioBtn.onclick = () => {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const text = outputElem.innerText;
    const utterance = new SpeechSynthesisUtterance("DxSkills overview. " + text.slice(0, 300));
    utterance.rate = 1.05;
    window.speechSynthesis.speak(utterance);
  };
});
