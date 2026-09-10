import * as vscode from "vscode";
import * as http from "http";
import * as https from "https";
import { URL } from "url";
import { quietNormalizeText } from "./quietFix";

const DIAGRAM_TEMPLATES: Record<string, string> = {
  "System Architecture Flowchart": `\`\`\`mermaid
flowchart TD
    subgraph Ingestion [1. Input Layer]
        A[Raw Brain Dump / Speech] --> B[D-Mode Compiler]
    end

    subgraph Processing [2. Transformation Layer]
        B --> C{Syntactic Filter}
        C -->|BLUF Extract| D[Executive Core]
        C -->|Action Items| E[Action Matrix]
        C -->|Entity Graph| F[Mermaid Diagram]
    end

    subgraph Output [3. Delivery Layer]
        D --> G[Structured Briefing]
        E --> G
        F --> G
    end

    style B fill:#111,stroke:#666,stroke-width:2px,color:#fff
    style G fill:#222,stroke:#888,stroke-width:2px,color:#fff
\`\`\``,

  "Strategy Flywheel Loop": `\`\`\`mermaid
graph TD
    A([1. Rapid Speech / Brain Dump]) --> B([2. Visual Spatial Synthesis])
    B --> C([3. High-Leverage Alignment])
    C --> D([4. Accelerated Execution])
    D --> A

    style A fill:#18181b,stroke:#a1a1aa,stroke-width:2px,color:#f4f4f5
    style B fill:#18181b,stroke:#a1a1aa,stroke-width:2px,color:#f4f4f5
    style C fill:#18181b,stroke:#a1a1aa,stroke-width:2px,color:#f4f4f5
    style D fill:#18181b,stroke:#a1a1aa,stroke-width:2px,color:#f4f4f5
\`\`\``,

  "State Machine Lifecycle": `\`\`\`mermaid
stateDiagram-v2
    [*] --> RawDraft : Capture Speed-of-Thought
    RawDraft --> SpatialScaffold : Compile D-Mode
    SpatialScaffold --> ReviewMatrix : Review Actions
    ReviewMatrix --> Published : Final Sign-off
    Published --> [*]
\`\`\``,

  "Decision Matrix": `\`\`\`mermaid
quadrantChart
    title Decision Prioritization Matrix
    x-axis Low Effort --> High Effort
    y-axis Low Leverage --> High High Leverage
    quadrant-1 Strategic Bets
    quadrant-2 Quick Wins
    quadrant-3 Deprioritize
    quadrant-4 Resource Drains
    "D-Mode Compiler": [0.25, 0.85]
    "Quiet Typo Fix": [0.18, 0.75]
    "Custom UI Themes": [0.70, 0.30]
    "Manual Formatting": [0.85, 0.15]
\`\`\``,

  "Concept Mindmap": `\`\`\`mermaid
mindmap
  root((DxSkills))
    Ingestion
      Whisper Voice
      Raw Brain Dump
      Obsidian Notes
    Cognitive Scaffolding
      BLUF
      Tables over Walls
      Mermaid Diagrams
    Deliverables
      Executive Briefs
      Architecture Specs
      Decision Trees
\`\`\``
};

function localDeterministicCompile(rawText: string): string {
  const lines = rawText
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.length > 0);

  if (lines.length === 0) {
    return rawText;
  }

  const bluf = lines[0];
  const items = lines.slice(1);

  const bulletList = items
    .map((item) => `- **Point:** ${item}`)
    .join("\n");

  return [
    "## BLUF (Bottom Line Up Front)",
    `> **Core Takeaway:** ${bluf}`,
    "",
    "## Key Takeaways",
    bulletList.length > 0 ? bulletList : "- Initial concept outlined above.",
    "",
    "## Action Items",
    "| Owner | Deliverable | Status | Target |",
    "| :--- | :--- | :--- | :--- |",
    `| Lead | Operationalize: ${bluf.slice(0, 40)}... | In Progress | Immediate |`,
    "| Team | Review structural dependencies | Pending | Next Sync |",
    "",
    "```mermaid",
    "flowchart LR",
    "    A[Input Idea] --> B[Structured Execution]",
    "    B --> C[Verified Milestone]",
    "    style A fill:#1a1a1a,stroke:#555,color:#eee",
    "    style B fill:#222,stroke:#777,color:#fff",
    "    style C fill:#1a1a1a,stroke:#555,color:#eee",
    "```"
  ].join("\n");
}

async function requestGatewayCompile(urlStr: string, text: string): Promise<string | null> {
  return new Promise((resolve) => {
    try {
      const u = new URL(urlStr);
      const postData = JSON.stringify({ text });
      const isHttps = u.protocol === "https:";
      const client = isHttps ? https : http;

      const req = client.request(
        {
          hostname: u.hostname,
          port: u.port || (isHttps ? 443 : 80),
          path: u.pathname,
          method: "POST",
          timeout: 2000,
          headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(postData)
          }
        },
        (res) => {
          let data = "";
          res.on("data", (chunk) => {
            data += chunk;
          });
          res.on("end", () => {
            if (res.statusCode === 200) {
              try {
                const parsed = JSON.parse(data);
                if (parsed.compiled) {
                  resolve(parsed.compiled);
                  return;
                }
              } catch {
                // fall through
              }
            }
            resolve(null);
          });
        }
      );

      req.on("error", () => resolve(null));
      req.on("timeout", () => {
        req.destroy();
        resolve(null);
      });

      req.write(postData);
      req.end();
    } catch {
      resolve(null);
    }
  });
}

export function activate(context: vscode.ExtensionContext) {
  // Status Bar Item
  const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  statusBar.text = "$(sparkle) DxSkills";
  statusBar.tooltip = "DxSkills: Speed-of-Thought Scaffolding (Click to compile selection)";
  statusBar.command = "dxskills.compileSelection";
  statusBar.show();
  context.subscriptions.push(statusBar);

  // Command: Compile Selection
  const compileCmd = vscode.commands.registerCommand("dxskills.compileSelection", async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showInformationMessage("DxSkills: Open an active editor with text to compile.");
      return;
    }

    const selection = editor.selection;
    const rawText = editor.document.getText(selection.isEmpty ? undefined : selection);

    if (!rawText.trim()) {
      vscode.window.showInformationMessage("DxSkills: Please select text to compile into D-Mode structure.");
      return;
    }

    statusBar.text = "$(sync~spin) DxSkills: Compiling...";

    const config = vscode.workspace.getConfiguration("dxskills");
    const gatewayUrl = config.get<string>("gatewayUrl", "http://localhost:8080/compile");

    let compiledText = await requestGatewayCompile(gatewayUrl, rawText);
    if (!compiledText) {
      compiledText = localDeterministicCompile(rawText);
    }

    await editor.edit((editBuilder) => {
      if (selection.isEmpty) {
        const fullRange = new vscode.Range(
          editor.document.positionAt(0),
          editor.document.positionAt(rawText.length)
        );
        editBuilder.replace(fullRange, compiledText!);
      } else {
        editBuilder.replace(selection, compiledText!);
      }
    });

    statusBar.text = "$(check) DxSkills: Structured";
    setTimeout(() => {
      statusBar.text = "$(sparkle) DxSkills";
    }, 4000);
  });

  // Command: Insert Diagram Template
  const insertDiagramCmd = vscode.commands.registerCommand("dxskills.insertDiagram", async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      return;
    }

    const choices = Object.keys(DIAGRAM_TEMPLATES);
    const pick = await vscode.window.showQuickPick(choices, {
      placeHolder: "Select a spatial architecture diagram to insert"
    });

    if (!pick) {
      return;
    }

    const snippet = DIAGRAM_TEMPLATES[pick];
    editor.insertSnippet(new vscode.SnippetString(snippet + "\n"));
  });

  // Command: Quiet Fix Inversions
  const quietFixCmd = vscode.commands.registerCommand("dxskills.quietFix", async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      return;
    }

    const selection = editor.selection;
    const targetRange = selection.isEmpty
      ? new vscode.Range(
          editor.document.positionAt(0),
          editor.document.positionAt(editor.document.getText().length)
        )
      : selection;

    const sourceText = editor.document.getText(targetRange);
    const { normalized, changesCount } = quietNormalizeText(sourceText);

    if (changesCount > 0) {
      await editor.edit((editBuilder) => {
        editBuilder.replace(targetRange, normalized);
      });
      statusBar.text = `$(check) DxSkills: Normalized ${changesCount} words`;
      setTimeout(() => {
        statusBar.text = "$(sparkle) DxSkills";
      }, 3500);
    } else {
      statusBar.text = "$(check) DxSkills: Clean text";
      setTimeout(() => {
        statusBar.text = "$(sparkle) DxSkills";
      }, 2500);
    }
  });

  // Optional Quiet Fix on Save
  vscode.workspace.onWillSaveTextDocument((event) => {
    const config = vscode.workspace.getConfiguration("dxskills");
    const enabled = config.get<boolean>("quietFixOnSave", false);
    if (!enabled) {
      return;
    }

    const doc = event.document;
    const text = doc.getText();
    const { normalized, changesCount } = quietNormalizeText(text);

    if (changesCount > 0) {
      const fullRange = new vscode.Range(
        doc.positionAt(0),
        doc.positionAt(text.length)
      );
      event.waitUntil(Promise.resolve([vscode.TextEdit.replace(fullRange, normalized)]));
    }
  });

  context.subscriptions.push(compileCmd, insertDiagramCmd, quietFixCmd);
}

export function deactivate() {}
