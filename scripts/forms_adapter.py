#!/usr/bin/env python3
"""
SounnyForms AI Multi-Modal Form Ingestion Adapter
Converts unstructured voice dictations and rapid brain dumps into validated,
schema-compliant form payloads without tedious manual field entry.
"""

import argparse
import json
import os
import re
import sys

BUILTIN_SCHEMAS = {
    "project_intake": {
        "title": "Project Intake Form",
        "fields": [
            {
                "name": "project_name",
                "type": "string",
                "required": True,
                "aliases": ["project", "initiative", "system", "name", "app"]
            },
            {
                "name": "objective",
                "type": "string",
                "required": True,
                "aliases": ["goal", "objective", "purpose", "target", "vision"]
            },
            {
                "name": "budget",
                "type": "number",
                "required": False,
                "aliases": ["budget", "funding", "cost", "investment", "capital"]
            },
            {
                "name": "lead",
                "type": "string",
                "required": False,
                "aliases": ["owner", "lead", "champion", "pm", "stakeholder"]
            },
            {
                "name": "deliverables",
                "type": "list",
                "required": False,
                "aliases": ["deliverables", "outputs", "milestones", "items", "features"]
            }
        ]
    },
    "grant_proposal": {
        "title": "Grant Proposal Intake",
        "fields": [
            {
                "name": "grant_title",
                "type": "string",
                "required": True,
                "aliases": ["title", "grant", "call", "proposal"]
            },
            {
                "name": "funding_program",
                "type": "string",
                "required": True,
                "aliases": ["program", "agency", "funder", "grant_agency", "nsf", "erc"]
            },
            {
                "name": "amount_requested",
                "type": "number",
                "required": False,
                "aliases": ["amount", "funding", "budget", "eur", "usd"]
            },
            {
                "name": "core_novelty",
                "type": "string",
                "required": True,
                "aliases": ["novelty", "innovation", "breakthrough", "contribution"]
            }
        ]
    }
}

def clean_currency_and_number(val_str):
    """Normalizes amounts like $1.5M, 250k, 50,000 into raw numeric float."""
    if not val_str:
        return None
    val_str = str(val_str).lower().replace(",", "").replace("$", "").replace("€", "").strip()
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([km])?", val_str)
    if match:
        num = float(match.group(1))
        unit = match.group(2)
        if unit == "k":
            num *= 1000
        elif unit == "m":
            num *= 1000000
        return num
    return None

def extract_field_value(text, field):
    """Heuristic regex and keyword extractor for a single schema field."""
    aliases = [field["name"]] + field.get("aliases", [])
    alias_pattern = r"(?:" + "|".join(re.escape(a) for a in aliases) + r")"
    
    # Check for direct key-value formats: "Key: Value" or "Key - Value"
    kv_pattern = re.compile(
        r"(?:^|\n)\s*(?:[-*]\s*)?(?:\*\*)?" + alias_pattern + r"(?:\*\*)?\s*[:\-=\s]\s*([^\n;]+)",
        re.IGNORECASE
    )
    match = kv_pattern.search(text)
    if match:
        raw_val = match.group(1).strip()
        return coerce_type(raw_val, field["type"])

    # If number, search near alias mentions
    if field["type"] == "number":
        num_pattern = re.compile(
            alias_pattern + r"[^0-9\n]{0,20}(\$?[0-9]+(?:\.[0-9]+)?\s*[km]?)",
            re.IGNORECASE
        )
        num_match = num_pattern.search(text)
        if num_match:
            return clean_currency_and_number(num_match.group(1))

    # If list, collect bullet items or comma sequences
    if field["type"] == "list":
        list_items = []
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                list_items.append(line[2:].strip())
        if list_items:
            return list_items

    return None

def coerce_type(val, target_type):
    """Converts raw extracted string to target schema type."""
    if val is None:
        return None
    if target_type == "number":
        return clean_currency_and_number(val)
    elif target_type == "list":
        if isinstance(val, list):
            return val
        items = [i.strip() for i in str(val).split(",") if i.strip()]
        return items if items else [str(val).strip()]
    elif target_type == "boolean":
        v = str(val).lower()
        return v in ["true", "yes", "1", "oui"]
    else:
        return str(val).strip()

def adapt_dump_to_form(raw_dump, schema):
    """Maps an unstructured dump into a validated schema payload."""
    if isinstance(schema, str):
        schema = BUILTIN_SCHEMAS.get(schema, {})
    
    payload = {}
    missing_required = []

    fields = schema.get("fields", [])
    for field in fields:
        fname = field["name"]
        val = extract_field_value(raw_dump, field)
        
        # Fallback for primary objective / BLUF if not explicitly matched
        if val is None and fname in ["objective", "goal", "purpose"]:
            lines = [l.strip() for l in raw_dump.split("\n") if l.strip()]
            if lines:
                val = lines[0]

        if val is not None:
            payload[fname] = val
        elif field.get("required", False):
            missing_required.append(fname)

    return {
        "status": "valid" if not missing_required else "incomplete",
        "schema_title": schema.get("title", "Form"),
        "payload": payload,
        "missing_required": missing_required
    }

def main():
    parser = argparse.ArgumentParser(description="SounnyForms Unstructured Dump Adapter")
    parser.add_argument("--schema", default="project_intake", help="Schema name or JSON path")
    parser.add_argument("--dump", help="Raw input text dump")
    parser.add_argument("--file", help="Path to text file containing raw dump")
    parser.add_argument("--output", help="Path to write JSON output")

    args = parser.parse_args()

    raw_text = args.dump or ""
    if args.file and os.path.isfile(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            raw_text = f.read()

    if not raw_text.strip():
        # Interactive demo default
        raw_text = "Project: Autonomous GeoAI Pipeline\nGoal: Real-time satellite SAR mapping for co-ops\nBudget: 250k\nOwner: Dr. Sounny\nDeliverables:\n- Data ingest node\n- Training cluster\n- Web viewer"

    schema = BUILTIN_SCHEMAS.get(args.schema)
    if not schema and os.path.isfile(args.schema):
        with open(args.schema, "r", encoding="utf-8") as f:
            schema = json.load(f)

    if not schema:
        schema = BUILTIN_SCHEMAS["project_intake"]

    result = adapt_dump_to_form(raw_text, schema)
    output_json = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Payload written to {args.output}")
    else:
        print(output_json)

if __name__ == "__main__":
    main()
