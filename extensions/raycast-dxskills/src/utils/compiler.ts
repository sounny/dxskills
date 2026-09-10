export interface CompiledOutput {
  bluf: string;
  tableMarkdown: string;
  draft: string;
  fullMarkdown: string;
  typoCount: number;
}

const TYPO_DICT: Record<string, string> = {
  yestreday: "yesterday",
  chekc: "check",
  runing: "running",
  refrence: "reference",
  shure: "sure",
  pct: "%",
  wont: "won't",
  reimbused: "reimbursed",
  architechture: "architecture",
  delievry: "delivery",
  milstone: "milestone"
};

export function compileDMode(rawInput: string): CompiledOutput {
  const raw = rawInput.trim();
  if (!raw) {
    return {
      bluf: "No content provided.",
      tableMarkdown: "",
      draft: "",
      fullMarkdown: "",
      typoCount: 0
    };
  }

  let typoCount = 0;
  const words = raw.split(/\s+/);
  const correctedWords = words.map((w) => {
    const clean = w.toLowerCase().replace(/[.,!?:;()]/g, "");
    if (TYPO_DICT[clean]) {
      typoCount++;
      const fixed = TYPO_DICT[clean];
      return w.toLowerCase().replace(clean, fixed);
    }
    return w;
  });

  // Ensure zero em dashes
  const cleanText = correctedWords.join(" ").replace(/\u2014/g, " - ");

  // Extract sentences
  const sentences = cleanText
    .split(/(?<=[.?!])\s+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);

  const firstSentence = sentences.length > 0 ? sentences[0] : cleanText;
  let bluf = firstSentence;
  if (!bluf.endsWith(".")) bluf += ".";
  bluf = bluf.charAt(0).toUpperCase() + bluf.slice(1);

  // Build matrix rows
  const remaining = sentences.slice(1);
  const rows: Array<{ item: string; status: string; action: string }> = [];

  if (remaining.length === 0) {
    rows.push({
      item: "Core Objective",
      status: "Immediate Focus",
      action: bluf
    });
  } else {
    remaining.forEach((s, idx) => {
      let item = `Milestone ${idx + 1}`;
      let status = "Active";
      const sLow = s.toLowerCase();
      if (
        sLow.includes("deadline") ||
        sLow.includes("friday") ||
        sLow.includes("month") ||
        sLow.includes("sync")
      ) {
        item = "Timeline / Alignment";
        status = "Scheduled";
      } else if (
        sLow.includes("package") ||
        sLow.includes("runway") ||
        sLow.includes("work")
      ) {
        item = "Deliverable Scope";
        status = "In Progress";
      }
      rows.push({ item, status, action: s });
    });
  }

  // Markdown table
  let tableMarkdown = "| Deliverable | Timeline / Status | Action Item |\n";
  tableMarkdown += "| :--- | :--- | :--- |\n";
  rows.forEach((r) => {
    tableMarkdown += `| ${r.item} | ${r.status} | ${r.action} |\n`;
  });

  // Refined draft
  let draft = `Team,\n\n${bluf}\n\n`;
  if (rows.length > 0) {
    draft += "Key execution items:\n";
    rows.forEach((r) => {
      draft += `- **${r.item}:** ${r.action}\n`;
    });
  }
  draft += "\nPlease follow up if anything is blocked.\n";

  // Full unified markdown
  let fullMarkdown = `> **BLUF:** ${bluf}\n\n`;
  fullMarkdown += `${tableMarkdown}\n`;
  fullMarkdown += `### Refined Action Draft\n\n${draft}`;

  // Enforce zero em dashes one final time
  fullMarkdown = fullMarkdown.replace(/\u2014/g, " - ");

  return {
    bluf,
    tableMarkdown,
    draft,
    fullMarkdown,
    typoCount
  };
}
