/**
 * DxSkills Browser Extension - Background Service Worker
 * Registers right-click context menu actions and routes highlighted text to content overlay.
 *
 * Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
 */

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "dx-scaffold-selection",
    title: "DxSkills: Restructure to D-Mode Brief",
    contexts: ["selection"]
  });

  chrome.contextMenus.create({
    id: "dx-canvas-selection",
    title: "DxSkills: Map to Obsidian Canvas",
    contexts: ["selection"]
  });

  chrome.contextMenus.create({
    id: "dx-audio-selection",
    title: "DxSkills: Audio Digest of Selection",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (!info.selectionText || !tab || !tab.id) return;

  const payload = {
    action: info.menuItemId,
    text: info.selectionText,
    url: tab.url,
    title: tab.title
  };

  // Cache in local extension storage
  chrome.storage.local.set({ activeScaffold: payload });

  // Forward to active tab content script
  chrome.tabs.sendMessage(tab.id, payload).catch((err) => {
    // Content script might not be injected yet, fallback to storage
    console.log("[DxSkills Extension] Content script message buffered:", err.message);
  });
});
