import React, { useEffect, useState } from "react";
import {
  ActionPanel,
  Action,
  Detail,
  Clipboard,
  showToast,
  Toast,
  Icon
} from "@raycast/api";
import { compileDMode, CompiledOutput } from "./utils/compiler";

export default function Command() {
  const [compiled, setCompiled] = useState<CompiledOutput | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  async function loadAndCompile() {
    setIsLoading(true);
    try {
      const clipboardText = await Clipboard.readText();
      if (!clipboardText || !clipboardText.trim()) {
        await showToast({
          style: Toast.Style.Failure,
          title: "Clipboard Empty",
          message: "Copy some raw notes or thoughts first."
        });
        setIsLoading(false);
        return;
      }

      const result = compileDMode(clipboardText);
      setCompiled(result);
      await showToast({
        style: Toast.Style.Success,
        title: "D-Mode Compiled",
        message: `${result.typoCount} typos corrected silently.`
      });
    } catch (err) {
      await showToast({
        style: Toast.Style.Failure,
        title: "Compilation Error",
        message: String(err)
      });
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadAndCompile();
  }, []);

  if (isLoading) {
    return <Detail isLoading={true} markdown="# Ingesting Speed-of-Thought Dump..." />;
  }

  if (!compiled) {
    return (
      <Detail
        markdown="# No Content in Clipboard\n\nCopy some text to your clipboard and run this command again."
        actions={
          <ActionPanel>
            <Action title="Retry from Clipboard" icon={Icon.Redo} onAction={loadAndCompile} />
          </ActionPanel>
        }
      />
    );
  }

  const markdownContent = `# DxSkills: Compiled D-Mode Architecture

${compiled.fullMarkdown}

---
*Metrics: ${compiled.typoCount} typos silently polished • 0 em dashes • 100% local*
`;

  return (
    <Detail
      markdown={markdownContent}
      actions={
        <ActionPanel>
          <Action.CopyToClipboard
            title="Copy Full Architecture"
            content={compiled.fullMarkdown}
            icon={Icon.Clipboard}
          />
          <Action.Paste
            title="Paste to Frontmost App"
            content={compiled.fullMarkdown}
            icon={Icon.Window}
          />
          <Action.CopyToClipboard
            title="Copy BLUF Only"
            content={compiled.bluf}
            icon={Icon.Text}
          />
          <Action
            title="Re-Compile from Clipboard"
            icon={Icon.Redo}
            onAction={loadAndCompile}
          />
        </ActionPanel>
      }
    />
  );
}
