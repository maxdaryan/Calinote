"""
bridge.py — Subprocess bridge between the Python GUI and the Rust backend.

Usage:
    from bridge import call_backend
    result = call_backend({"cmd": "list", "dir": "/path/to/notes"})
    # result = {"ok": True, "notes": [...]}
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# ── Locate the compiled Rust binary ───────────────────────────────────────────

def _find_binary() -> str:
    """Return the path to the compiled ghost binary."""
    base = Path(__file__).parent.parent  # project root
    candidates = [
        base / "backend" / "target" / "release" / "ghost",
        base / "backend" / "target" / "debug"   / "ghost",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    raise FileNotFoundError(
        "Ghost binary not found.\n"
        "Run:  cd backend && cargo build --release\n"
        f"Searched: {[str(c) for c in candidates]}"
    )

_BINARY: str | None = None

def _binary() -> str:
    global _BINARY
    if _BINARY is None:
        _BINARY = _find_binary()
    return _BINARY


# ── Core RPC call ─────────────────────────────────────────────────────────────

def call_backend(payload: dict) -> dict:
    """
    Send `payload` as JSON to the Rust binary via stdin.
    Returns the parsed JSON response dict.
    Raises RuntimeError on process failure.
    """
    try:
        binary = _binary()
    except FileNotFoundError as exc:
        return {"ok": False, "error": str(exc)}

    try:
        proc = subprocess.run(
            [binary],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=15,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Backend timed out (>15s)."}
    except Exception as exc:
        return {"ok": False, "error": f"Subprocess error: {exc}"}

    stdout = proc.stdout.strip()
    if not stdout:
        stderr = proc.stderr.strip()
        return {"ok": False, "error": f"Backend produced no output.\nstderr: {stderr}"}

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": f"Backend returned non-JSON:\n{stdout}"}


# ── Convenience wrappers ──────────────────────────────────────────────────────

def list_notes(notes_dir: str) -> dict:
    return call_backend({"cmd": "list", "dir": notes_dir})

def save_note(path: str, title: str, body: str, password: str) -> dict:
    return call_backend({"cmd": "save", "path": path, "title": title,
                         "body": body, "password": password})

def load_note(path: str, password: str) -> dict:
    return call_backend({"cmd": "load", "path": path, "password": password})

def delete_note(path: str) -> dict:
    return call_backend({"cmd": "delete", "path": path})
