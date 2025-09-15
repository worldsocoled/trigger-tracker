"""
Utility helpers for Trigger Tracker.
"""

import json
import os
from datetime import datetime


def now_iso():
    """Return current UTC timestamp in ISO format (readable)."""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def read_json(path):
    """Read JSON list from file. Return empty list if file not found or invalid."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def write_json(path, data):
    """Write list to JSON file (pretty printed)."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def prompt_int(prompt_text, minimum=0, maximum=10, default=0):
    """Prompt user for integer between min and max. Blank accepts default."""
    while True:
        raw = input(prompt_text).strip()
        if raw == "":
            return default
        try:
            val = int(raw)
            if val < minimum or val > maximum:
                print(f"Enter a number between {minimum} and {maximum}.")
            else:
                return val
        except ValueError:
            print("Please enter a valid integer.")
