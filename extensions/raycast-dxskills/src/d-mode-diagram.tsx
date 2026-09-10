import React from "react";
import { ActionPanel, Action, List, Icon } from "@raycast/api";

interface DiagramTemplate {
  id: string;
  title: string;
  subtitle: string;
  category: string;
  code: string;
}

const TEMPLATES: DiagramTemplate[] = [
  {
    id: "system-arch",
    title: "System Architecture",
    subtitle: "Client, API Gateway, Services, DB",
    category: "Engineering",
    code: `graph TD
    Client["Client / IDE / CLI"] --> Edge["Edge Cache"]
    Edge --> Gateway["Ingress API Gateway"]
    Gateway --> Service["Task Engine & Auth"]
    Service --> Workers["Background Worker Pool"]
    Service --> DB[("PostgreSQL Master")]
    Workers --> S3[("Object Storage")]
    Workers --> DB`
  },
  {
    id: "flywheel",
    title: "Strategy Flywheel",
    subtitle: "Closed-loop feedback and momentum",
    category: "Strategy",
    code: `graph TD
    A["Rapid Input: Zero Typing Friction"] --> B["High-Signal Synthesis: Visual Scaffolding"]
    B --> C["Accelerated Delivery: Polished Output"]
    C --> D["User Feedback & Real-World Validation"]
    D --> E["Expanded Knowledge & Trust"]
    E --> A`
  },
  {
    id: "curriculum",
    title: "Curriculum / Project Roadmap",
    subtitle: "3-Phase progressive disclosure",
    category: "Education",
    code: `graph LR
    subgraph P1 ["Phase 1: Foundations"]
        A1["Mental Models"] --> A2["Tooling & Setup"]
    end
    subgraph P2 ["Phase 2: Applied Workflows"]
        B1["Hands-On Labs"] --> B2["Integration Pipelines"]
    end
    subgraph P3 ["Phase 3: Synthesis"]
        C1["Autonomous Architecture"] --> C2["Peer Defense"]
    end
    A2 --> B1
    B2 --> C1`
  },
  {
    id: "decision-matrix",
    title: "Architectural Decision Tree",
    subtitle: "Branching choice pathways",
    category: "Architecture",
    code: `graph TD
    Q1["Problem: Architecture Design"] --> Q2{"High Concurrency?"}
    Q2 -- "Yes" --> Q3{"Complex Joins?"}
    Q2 -- "No" --> R1["Monolith (Fastest Delivery)"]
    Q3 -- "Yes" --> R2["Event-Driven Microservices"]
    Q3 -- "No" --> R3["Serverless Edge Functions"]`
  },
  {
    id: "state-machine",
    title: "State Machine",
    subtitle: "Lifecycle state transitions",
    category: "Engineering",
    code: `stateDiagram-v2
    [*] --> Draft
    Draft --> InReview: Submit
    InReview --> Approved: Accept
    InReview --> ChangesRequested: Feedback
    ChangesRequested --> Draft: Revise
    Approved --> Deployed: Release
    Deployed --> [*]`
  }
];

export default function Command() {
  return (
    <List searchBarPlaceholder="Search Mermaid architecture templates...">
      {TEMPLATES.map((tmpl) => (
        <List.Item
          key={tmpl.id}
          icon={Icon.Network}
          title={tmpl.title}
          subtitle={tmpl.subtitle}
          accessories={[{ text: tmpl.category }]}
          actions={
            <ActionPanel>
              <Action.CopyToClipboard
                title="Copy Mermaid Code"
                content={tmpl.code}
                icon={Icon.Clipboard}
              />
              <Action.Paste
                title="Paste to Frontmost App"
                content={tmpl.code}
                icon={Icon.Window}
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
