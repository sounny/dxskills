#!/usr/bin/env python3
"""
DxSkills Self-Hosted Cognitive Gateway
Lightweight HTTP API providing speed-of-thought D-Mode compilation,
health monitoring, and latency telemetry for enterprise and local deployments.
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
    "milstone": "milestone"
}

STATS = {
    "requests_total": 0,
    "typos_fixed_total": 0,
    "total_latency_ms": 0.0,
    "start_time": time.time()
}

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
                item = f"Milestone {idx}"
                status = "Active"
            rows.append((item, status, s))

    table_lines = ["| Item | Status | Action / Detail |", "| :--- | :--- | :--- |"]
    for item, status, action in rows:
        table_lines.append(f"| {item} | {status} | {action} |")
    table_md = "\n".join(table_lines)

    draft_lines = [f"> **BLUF:** {bluf}", "", table_md, "", "### Refined Action Draft", "", "Team,", "", bluf, ""]
    for item, _, action in rows:
        draft_lines.append(f"- **{item}:** {action}")
    draft_lines.append("")
    draft_lines.append("Let me know if anything is blocked.")

    full_md = "\n".join(draft_lines).replace("\u2014", " - ")

    return {
        "bluf": bluf,
        "table": table_md,
        "full_markdown": full_md,
        "typos_fixed": typos_fixed
    }

class GatewayHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, data):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path in ["/health", "/healthz"]:
            uptime_sec = time.time() - STATS["start_time"]
            self._send_json(200, {
                "status": "healthy",
                "service": "dxskills-gateway",
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
        else:
            # Simple status splash
            self._send_json(200, {
                "message": "DxSkills Cognitive Scaffolding Gateway is running.",
                "endpoints": {
                    "health": "/health",
                    "metrics": "/metrics",
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
            self._send_json(200, result)
        else:
            self._send_json(404, {"error": "Endpoint not found"})

def run_server(port=8080, host="0.0.0.0"):
    server_addr = (host, port)
    httpd = HTTPServer(server_addr, GatewayHandler)
    print(f"[DxSkills Gateway] Serving on http://{host}:{port}")
    print(f"[DxSkills Gateway] Health check: http://localhost:{port}/health")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[DxSkills Gateway] Shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    run_server(port=port)
