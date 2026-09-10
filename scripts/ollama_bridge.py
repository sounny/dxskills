#!/usr/bin/env python3
"""
DxSkills Local LLM Bridge
Connects to local offline LLM runtimes (Ollama or LM Studio)
for zero-latency, private, on-device cognitive compilation.
"""

import os
import sys
import json
import argparse
import subprocess
import urllib.request
import urllib.error

DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_LMSTUDIO_HOST = "http://localhost:1234/v1"

def get_clipboard_text():
    if sys.platform == "win32":
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                capture_output=True,
                text=True,
                check=True
            )
            return res.stdout.strip()
        except Exception:
            return ""
    elif sys.platform == "darwin":
        try:
            res = subprocess.run(["pbpaste"], capture_output=True, text=True, check=True)
            return res.stdout.strip()
        except Exception:
            return ""
    return ""

def set_clipboard_text(text):
    if sys.platform == "win32":
        try:
            p = subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", "$input | Set-Clipboard"],
                stdin=subprocess.PIPE,
                text=True
            )
            p.communicate(input=text)
            return True
        except Exception:
            return False
    elif sys.platform == "darwin":
        try:
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE, text=True)
            p.communicate(input=text)
            return True
        except Exception:
            return False
    return False

def query_ollama(prompt, model="d-mode", host=DEFAULT_OLLAMA_HOST):
    url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            raw_response = body.get("response", "")
            # Enforce zero em dashes
            clean_response = raw_response.replace("\u2014", " - ")
            return clean_response
    except urllib.error.URLError as e:
        print(f"[DxSkills Ollama] Connection error to {url}: {e.reason}")
        print("\nTroubleshooting tips:")
        print("1. Ensure Ollama is running (`ollama serve`).")
        print("2. Create the D-Mode model: `ollama create d-mode -f models/Modelfile.llama3`")
        print("3. Or specify an installed model: `python scripts/ollama_bridge.py --model llama3.2`\n")
        return None

def query_lmstudio(prompt, model="default", host=DEFAULT_LMSTUDIO_HOST):
    url = f"{host.rstrip('/')}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are D-Mode, an open-standard cognitive scaffolding compiler. Lead with BLUF, use markdown tables, silently polish typos, and strictly never use em dashes."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            raw_response = body["choices"][0]["message"]["content"]
            clean_response = raw_response.replace("\u2014", " - ")
            return clean_response
    except urllib.error.URLError as e:
        print(f"[DxSkills LMStudio] Connection error to {url}: {e.reason}")
        print("\nTroubleshooting tips:")
        print("1. Ensure LM Studio Local Server is running (port 1234).")
        print("2. Load any local model into LM Studio.\n")
        return None

def main():
    parser = argparse.ArgumentParser(description="DxSkills Local LLM Cognitive Compiler")
    parser.add_argument("--provider", choices=["ollama", "lmstudio"], default="ollama", help="Local runtime provider")
    parser.add_argument("--model", type=str, default="d-mode", help="Model name (e.g., d-mode, llama3.2, mistral)")
    parser.add_argument("--host", type=str, default=None, help="Custom server host URL")
    parser.add_argument("--text", type=str, default=None, help="Raw input brain dump text")
    parser.add_argument("--file", type=str, default=None, help="Path to input text file")
    parser.add_argument("--clipboard", action="store_true", help="Read input from clipboard and write output back to clipboard")
    args = parser.parse_args()

    input_text = ""
    if args.text:
        input_text = args.text
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            input_text = f.read()
    elif args.clipboard:
        input_text = get_clipboard_text()
        if not input_text:
            print("[DxSkills] Clipboard is empty.")
            sys.exit(1)
    else:
        print("Enter raw notes (Ctrl+Z or Ctrl+D to submit):")
        input_text = sys.stdin.read()

    if not input_text.strip():
        print("[DxSkills] No input provided.")
        sys.exit(1)

    print(f"[DxSkills] Querying local {args.provider} (model: {args.model})...")

    if args.provider == "ollama":
        host = args.host or DEFAULT_OLLAMA_HOST
        result = query_ollama(input_text, model=args.model, host=host)
    else:
        host = args.host or DEFAULT_LMSTUDIO_HOST
        result = query_lmstudio(input_text, model=args.model, host=host)

    if result:
        print("\n--- Compiled D-Mode Output ---\n")
        print(result)
        if args.clipboard:
            set_clipboard_text(result)
            print("\n[DxSkills] Result copied to clipboard successfully.")

if __name__ == "__main__":
    main()
