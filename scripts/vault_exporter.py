#!/usr/bin/env python3
"""
DxSkills Vault & Database Exporter (Obsidian & Notion)
Generates native Obsidian frontmatter/properties and structured Notion page payloads.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import re
import json
import urllib.parse
import urllib.request
from datetime import date

def format_obsidian_markdown(text, title=None, tags=None, doc_type="specification", vault=None):
    """
    Wraps markdown content with Obsidian-native YAML frontmatter and properties.
    Generates Obsidian URL scheme for 1-click vault creation.
    """
    today = date.today().isoformat()
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    # Extract title from first heading if not provided
    if not title:
        for line in lines:
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break
    if not title:
        title = "DxSkills Scaffolding Note"

    # Extract BLUF if present
    bluf = ""
    for line in lines:
        if line.startswith("> **Decision Requested:**") or line.startswith("> **BLUF:**") or line.startswith("> **Bottom Line Up Front:**"):
            bluf = line.replace("> ", "").strip()
            break

    tags_list = ["dxskills", "cognitive-scaffolding"]
    if tags:
        if isinstance(tags, list):
            tags_list.extend(tags)
        elif isinstance(tags, str):
            tags_list.extend([t.strip() for t in tags.split(",") if t.strip()])
    # Remove duplicate tags while preserving order
    clean_tags = list(dict.fromkeys(tags_list))

    frontmatter = [
        "---",
        f"title: \"{title}\"",
        f"type: {doc_type}",
        f"created: {today}",
        f"status: active",
        "tags:",
    ]
    for t in clean_tags:
        frontmatter.append(f"  - {t}")
    if bluf:
        escaped_bluf = bluf.replace('"', '\\"')
        frontmatter.append(f"bluf: \"{escaped_bluf}\"")
    frontmatter.append("---")
    frontmatter.append("")

    full_markdown = "\n".join(frontmatter) + text.strip() + "\n"

    # Construct obsidian:// URL
    encoded_title = urllib.parse.quote(title)
    encoded_content = urllib.parse.quote(full_markdown)
    vault_param = f"vault={urllib.parse.quote(vault)}&" if vault else ""
    obsidian_uri = f"obsidian://new?{vault_param}name={encoded_title}&content={encoded_content}"

    return {
        "title": title,
        "markdown": full_markdown,
        "obsidian_uri": obsidian_uri
    }

def format_notion_payload(text, title=None, database_id=None):
    """
    Transforms markdown specification into a structured Notion API page creation payload.
    Supports headings, callouts, tables, and numbered lists.
    """
    today = date.today().isoformat()
    lines = [line.strip() for line in text.strip().splitlines()]

    if not title:
        for line in lines:
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break
    if not title:
        title = "DxSkills Project Specification"

    # Detect BLUF
    bluf_text = ""
    for line in lines:
        if line.startswith("> "):
            clean_q = line.lstrip("> ").strip()
            if any(k in clean_q for k in ["BLUF", "Decision Requested", "Core Value", "Primary Learning"]):
                bluf_text = clean_q
                break

    # Build Notion Block Children
    children = []

    # Add Callout block for BLUF if found
    if bluf_text:
        children.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": bluf_text}}],
                "icon": {"emoji": "⚡"}
            }
        })

    # Add remaining blocks
    in_table = False
    table_rows = []

    for line in lines:
        if not line:
            continue
        if line.startswith("# "):
            continue # Title handled in page properties
        elif line.startswith("## "):
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line.lstrip("## ").strip()}}]
                }
            })
        elif line.startswith("### "):
            children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line.lstrip("### ").strip()}}]
                }
            })
        elif line.startswith("|") and line.endswith("|"):
            if ":---" in line or "---:" in line or "----" in line:
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            table_rows.append(cells)
            in_table = True
        elif line.startswith("- ") or line.startswith("* "):
            if in_table and table_rows:
                children.append(_create_notion_table_block(table_rows))
                table_rows = []
                in_table = False
            children.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line.lstrip("-* ").strip()}}]
                }
            })
        elif re.match(r"^\d+\.\s", line):
            if in_table and table_rows:
                children.append(_create_notion_table_block(table_rows))
                table_rows = []
                in_table = False
            content = re.sub(r"^\d+\.\s", "", line).strip()
            children.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                }
            })
        elif not in_table:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line.strip()}}]
                }
            })

    if in_table and table_rows:
        children.append(_create_notion_table_block(table_rows))

    payload = {
        "parent": {"database_id": database_id or "DATABASE_ID_PLACEHOLDER"},
        "properties": {
            "Name": {
                "title": [{"text": {"content": title}}]
            },
            "Type": {
                "select": {"name": "Cognitive Specification"}
            },
            "Status": {
                "select": {"name": "Active"}
            },
            "Created": {
                "date": {"start": today}
            }
        },
        "children": children
    }

    return payload

def _create_notion_table_block(rows):
    """Helper to convert Markdown table rows into Notion table block."""
    table_width = max(len(r) for r in rows) if rows else 2
    row_blocks = []
    for r in rows:
        cells = []
        for cell_text in r:
            cells.append([{"type": "text", "text": {"content": cell_text}}])
        # Pad cells if row is shorter
        while len(cells) < table_width:
            cells.append([{"type": "text", "text": {"content": ""}}])
        row_blocks.append({
            "type": "table_row",
            "table_row": {"cells": cells}
        })

    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": table_width,
            "has_column_header": True,
            "has_row_header": False,
            "children": row_blocks
        }
    }

def dispatch_notion_webhook(payload, webhook_url):
    """Dispatches page creation payload to an automated webhook or relay."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "DxSkills-Notion-Dispatcher/1.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.status, response.read().decode("utf-8")

if __name__ == "__main__":
    sample = "# Executive Briefing\n> **BLUF:** Ship on Friday.\n\n## Actions\n1. Review code\n2. Deploy cluster"
    obs = format_obsidian_markdown(sample, title="Cloud Cutover")
    print("Obsidian frontmatter title:", obs["title"])
    notion = format_notion_payload(sample, title="Cloud Cutover")
    print("Notion children blocks count:", len(notion["children"]))
