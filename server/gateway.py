#!/usr/bin/env python3
"""
DxSkills Self-Hosted Cognitive Gateway
Lightweight HTTP API providing speed-of-thought D-Mode compilation,
health monitoring, event logging, and latency telemetry for enterprise deployments.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import json
import time
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

TYPO_DICT = {
    "yestreday": "yesterday",
    "chekc": "check",
    "runing": "running",
    "refrence": "reference",
    "shure": "sure",
    "pct": "%",
    "wont": "won't",
    "reimbused": "reimbursed",
    "architechture": "architecture",
    "delievry": "delivery",
    "milstone": "milestone",
    "teh": "the",
    "taht": "that",
    "waht": "what",
    "wierd": "weird",
    "seperate": "separate"
}

STATS = {
    "requests_total": 0,
    "typos_fixed_total": 0,
    "total_latency_ms": 0.0,
    "start_time": time.time()
}

EVENT_LOG = []


def compile_d_mode(raw_input):
    clean = raw_input.strip()
    words = clean.split()
    corrected_words = []
    typos_fixed = 0
    for w in words:
        stripped = w.lower().strip(".,!?:;()")
        if stripped in TYPO_DICT:
            typos_fixed += 1
            w = w.lower().replace(stripped, TYPO_DICT[stripped])
        corrected_words.append(w)

    clean_text = " ".join(corrected_words).replace("\u2014", " - ")
    sentences = [s.strip() for s in clean_text.split(".") if s.strip()]
    if not sentences:
        sentences = [clean_text]

    bluf = sentences[0]
    if not bluf.endswith("."):
        bluf += "."
    bluf = bluf[0].upper() + bluf[1:]

    rows = []
    remaining = sentences[1:]
    if not remaining:
        rows.append(("Core Objective", "Active", bluf))
    else:
        for idx, s in enumerate(remaining, 1):
            s_low = s.lower()
            if any(k in s_low for k in ["deadline", "friday", "month", "sync", "wednesday", "call"]):
                item = "Timeline / Alignment"
                status = "Scheduled"
            elif any(k in s_low for k in ["package", "runway", "work", "proposal", "budget"]):
                item = "Deliverable Scope"
                status = "In Progress"
            else:
                item = f"Action Item {idx}"
                status = "Active"
            rows.append((item, status, s))

    # Construct clean markdown output
    md_lines = [
        "## BLUF (Bottom Line Up Front)",
        f"> **Takeaway:** {bluf}",
        "",
        "## Key Directives",
        "\n".join([f"- **Point:** {s}" for s in remaining]) if remaining else f"- {bluf}",
        "",
        "## Action Matrix",
        "| Focus / Deliverable | Status | Action Item |",
        "| :--- | :--- | :--- |"
    ]
    for r in rows:
        md_lines.append(f"| {r[0]} | {r[1]} | {r[2]} |")

    # Estimate cognitive load reduction metrics
    syllables_est = int(len(words) * 1.5)
    subvocal_sec = syllables_est * 0.18
    visual_scan_sec = (syllables_est * 0.45 * 0.18) / 3.2
    time_saved = max(1.0, subvocal_sec - visual_scan_sec)

    return {
        "bluf": bluf,
        "rows": rows,
        "typos_fixed": typos_fixed,
        "compiled": "\n".join(md_lines),
        "telemetry": {
            "raw_word_count": len(words),
            "subvocal_seconds": round(subvocal_sec, 1),
            "visual_scan_seconds": round(visual_scan_sec, 1),
            "cognitive_time_saved_sec": round(time_saved, 1),
            "extraneous_load_drop_pct": 74 if len(words) > 25 else 48
        }
    }


class GatewayHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, data):
        response_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path in ["/health", "/"]:
            uptime_sec = time.time() - STATS["start_time"]
            self._send_json(200, {
                "status": "healthy",
                "service": "dxskills-cognitive-gateway",
                "version": "0.1.0",
                "uptime_seconds": round(uptime_sec, 2),
                "em_dash_free": True
            })
        elif self.path in ["/metrics", "/stats"]:
            avg_latency = 0.0
            if STATS["requests_total"] > 0:
                avg_latency = STATS["total_latency_ms"] / STATS["requests_total"]
            self._send_json(200, {
                "requests_total": STATS["requests_total"],
                "typos_fixed_total": STATS["typos_fixed_total"],
                "avg_latency_ms": round(avg_latency, 3),
                "uptime_seconds": round(time.time() - STATS["start_time"], 1)
            })
        elif self.path == "/events":
            self._send_json(200, {
                "events": EVENT_LOG,
                "count": len(EVENT_LOG),
                "capacity": 50
            })
        else:
            self._send_json(200, {
                "message": "DxSkills Cognitive Scaffolding Gateway is running.",
                "endpoints": {
                    "health": "/health",
                    "metrics": "/metrics",
                    "events": "/events",
                    "compile": "POST /compile (payload: {\"text\": \"...\"})"
                }
            })

    def do_POST(self):
        if self.path == "/compile":
            start_t = time.time()
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len).decode("utf-8")

            try:
                data = json.loads(post_body)
                raw_text = data.get("text", "")
            except Exception:
                raw_text = post_body

            result = compile_d_mode(raw_text)
            elapsed_ms = (time.time() - start_t) * 1000.0

            STATS["requests_total"] += 1
            STATS["typos_fixed_total"] += result["typos_fixed"]
            STATS["total_latency_ms"] += elapsed_ms

            result["latency_ms"] = round(elapsed_ms, 3)

            # Record in rolling event log
            event = {
                "id": len(EVENT_LOG) + 1,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "latency_ms": round(elapsed_ms, 2),
                "words_count": len(raw_text.split()),
                "typos_fixed": result["typos_fixed"],
                "bluf": result["bluf"][:60]
            }
            EVENT_LOG.append(event)
            if len(EVENT_LOG) > 50:
                EVENT_LOG.pop(0)

            self._send_json(200, result)
        else:
            self._send_json(404, {"error": "Endpoint not found"})


def run_server(port=8080, host="0.0.0.0"):
    server_addr = (host, port)
    httpd = HTTPServer(server_addr, GatewayHandler)
    print(f"[DxSkills Gateway] Serving on http://{host}:{port}")
    print(f"[DxSkills Gateway] Health check: http://localhost:{port}/health")
    print(f"[DxSkills Gateway] Real-time events: http://localhost:{port}/events")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[DxSkills Gateway] Shutting down.")
        httpd.server_close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    run_server(port=port)
