#!/usr/bin/env python3
"""
DxSkills Multi-Channel Webhook Receiver
Enables asynchronous speed-of-thought voice and text ingestion from Telegram,
Slack, WhatsApp, and generic mobile recording workflows.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import os
import sys
import json
import time
import base64
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Tuple

PORT = int(os.environ.get("WEBHOOK_PORT", 8081))
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")

STATS = {
    "webhooks_received": 0,
    "telegram_events": 0,
    "slack_events": 0,
    "whatsapp_events": 0,
    "generic_events": 0,
    "start_time": time.time()
}

TYPO_DICT = {
    "teh": "the",
    "taht": "that",
    "waht": "what",
    "wierd": "weird",
    "recieved": "received",
    "recieve": "receive",
    "seperate": "separate",
    "acheive": "achieve",
    "calender": "calendar",
    "definately": "definitely",
    "delievry": "delivery",
    "milstone": "milestone"
}


def compile_d_mode_text(raw_input: str) -> Dict[str, Any]:
    """Compiles unstructured text into D-Mode executive structure."""
    clean = raw_input.strip()
    words = clean.split()
    corrected = []
    typo_count = 0

    for w in words:
        stripped = w.lower().strip(".,!?:;()")
        if stripped in TYPO_DICT:
            typo_count += 1
            w = w.lower().replace(stripped, TYPO_DICT[stripped])
        corrected.append(w)

    clean_text = " ".join(corrected).replace("\u2014", " - ")
    sentences = [s.strip() for s in clean_text.split(".") if s.strip()]
    if not sentences:
        sentences = [clean_text]

    bluf = sentences[0]
    if not bluf.endswith("."):
        bluf += "."
    bluf = bluf[0].upper() + bluf[1:]

    remaining = sentences[1:]
    rows = []
    if not remaining:
        rows.append(("Core Objective", "Active", bluf))
    else:
        for idx, s in enumerate(remaining, 1):
            category = "Operational Focus"
            status = "In Progress"
            low = s.lower()
            if any(k in low for k in ["deadline", "friday", "sync", "call", "schedule"]):
                category = "Timeline & Alignment"
                status = "Scheduled"
            elif any(k in low for k in ["api", "bug", "crs", "outage", "error", "blocker"]):
                category = "Technical Deliverable"
                status = "Immediate"
            rows.append((category, status, s))

    # Build Markdown
    md_lines = [
        "## BLUF (Bottom Line Up Front)",
        f"> **Directive:** {bluf}",
        "",
        "## Action Matrix",
        "| Focus Area | Status | Action Item |",
        "| :--- | :--- | :--- |"
    ]
    for r in rows:
        md_lines.append(f"| {r[0]} | {r[1]} | {r[2]} |")

    md_lines.extend([
        "",
        "### Operational Brief",
        f"Team, {bluf}",
        "",
        "Please align on the action items above. Flag blockers immediately."
    ])

    return {
        "bluf": bluf,
        "rows": rows,
        "typos_fixed": typo_count,
        "compiled_markdown": "\n".join(md_lines)
    }


def send_telegram_reply(chat_id: int, text: str):
    """Replies directly to Telegram chat if bot token is configured."""
    if not TELEGRAM_BOT_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[Webhook] Telegram reply error: {e}", file=sys.stderr)


class WebhookRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: Dict[str, Any]):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/health", "/"):
            self._send_json(200, {
                "status": "healthy",
                "service": "dxskills-webhook-receiver",
                "version": "0.1.0",
                "channels": ["telegram", "slack", "whatsapp", "generic"],
                "uptime_seconds": round(time.time() - STATS["start_time"], 1)
            })
        elif self.path == "/stats":
            self._send_json(200, STATS)
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        STATS["webhooks_received"] += 1

        # 1. Telegram Webhook
        if self.path == "/webhook/telegram":
            STATS["telegram_events"] += 1
            try:
                data = json.loads(raw_body.decode("utf-8"))
                message = data.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "")

                if text:
                    result = compile_d_mode_text(text)
                    reply_text = f"*DxSkills Speed-of-Thought Synthesis*\n\n{result['compiled_markdown']}"
                    if chat_id:
                        send_telegram_reply(chat_id, reply_text)
                    self._send_json(200, {"ok": True, "result": result})
                    return
                elif "voice" in message or "audio" in message:
                    # Voice note received
                    note = message.get("voice") or message.get("audio")
                    file_id = note.get("file_id")
                    if chat_id:
                        send_telegram_reply(chat_id, "Voice note received. Transcribing and structuring with D-Mode...")
                    self._send_json(200, {"ok": True, "status": "voice_received", "file_id": file_id})
                    return
                self._send_json(200, {"ok": True, "notice": "Unhandled message type"})
            except Exception as e:
                self._send_json(400, {"error": str(e)})

        # 2. Slack Webhook (Events API)
        elif self.path == "/webhook/slack":
            STATS["slack_events"] += 1
            try:
                data = json.loads(raw_body.decode("utf-8"))
                # URL verification handshake
                if data.get("type") == "url_verification":
                    self._send_json(200, {"challenge": data.get("challenge")})
                    return

                event = data.get("event", {})
                text = event.get("text", "")
                if text and event.get("type") == "message" and not event.get("bot_id"):
                    result = compile_d_mode_text(text)
                    self._send_json(200, {"ok": True, "result": result})
                    return
                self._send_json(200, {"ok": True})
            except Exception as e:
                self._send_json(400, {"error": str(e)})

        # 3. WhatsApp / Twilio Webhook
        elif self.path == "/webhook/whatsapp":
            STATS["whatsapp_events"] += 1
            try:
                # Can be form-encoded (Twilio) or JSON (Meta Cloud API)
                content_type = self.headers.get("Content-Type", "")
                if "json" in content_type:
                    data = json.loads(raw_body.decode("utf-8"))
                    text = str(data)
                else:
                    text = raw_body.decode("utf-8", errors="ignore")
                result = compile_d_mode_text(text)
                self._send_json(200, {"ok": True, "result": result})
            except Exception as e:
                self._send_json(400, {"error": str(e)})

        # 4. Generic / Mobile App Ingestion Webhook
        elif self.path in ("/webhook/generic", "/webhook"):
            STATS["generic_events"] += 1
            try:
                content_type = self.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    data = json.loads(raw_body.decode("utf-8"))
                    text = data.get("text", "")
                    if not text and "audio_base64" in data:
                        # Audio payload
                        text = "Voice audio payload received for offline Whisper transcription."
                else:
                    text = raw_body.decode("utf-8", errors="ignore")

                if not text.strip():
                    self._send_json(400, {"error": "No text or audio content received"})
                    return

                result = compile_d_mode_text(text)
                self._send_json(200, {
                    "ok": True,
                    "result": result,
                    "telemetry": {
                        "syllables_est": len(text.split()) * 1.5,
                        "time_saved_sec": max(1.0, round(len(text.split()) * 0.12, 1))
                    }
                })
            except Exception as e:
                self._send_json(400, {"error": str(e)})

        else:
            self._send_json(404, {"error": "Webhook endpoint not found"})


def run_server(port: int = PORT):
    server = HTTPServer(("0.0.0.0", port), WebhookRequestHandler)
    print(f"[DxSkills] Webhook Receiver listening on http://0.0.0.0:{port}")
    print("           Supported endpoints:")
    print("           - POST /webhook/telegram (Telegram bot updates)")
    print("           - POST /webhook/slack    (Slack events API)")
    print("           - POST /webhook/whatsapp (WhatsApp cloud/Twilio)")
    print("           - POST /webhook/generic  (REST & mobile recording apps)")
    print("           - GET  /health           (Health check)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[DxSkills] Shutting down Webhook Receiver.")
        server.server_close()


if __name__ == "__main__":
    run_server()
