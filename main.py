#!/usr/bin/env python3
"""
Trigger Tracker - CLI
Log detailed trigger entries and analyze patterns.

Run: python main.py
"""

import json
import os
import sys
from datetime import datetime
from utils.helpers import now_iso, read_json, write_json, prompt_int
from utils.stats import (
    average_emotion_scores,
    count_triggers,
    triggers_per_hour,
    triggers_per_day,
)
from utils.export import export_csv

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "triggers.json")
REPORTS_DIR = "reports"


def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)


def prompt_entry():
    print("\n--- New Trigger Entry ---")
    trigger = input("1) What was the trigger? ").strip()
    while not trigger:
        print("Trigger cannot be empty.")
        trigger = input("1) What was the trigger? ").strip()

    before = input("2) What happened immediately before the trigger? ").strip()
    after = input("3) What happened immediately after the trigger? ").strip()

    print("\n4) Rate these feelings from 0 (none) to 10 (very strong). Press Enter to accept 0.")
    anxiety = prompt_int("   Anxiety (0-10): ", 0, 10)
    sadness = prompt_int("   Sadness (0-10): ", 0, 10)
    anger = prompt_int("   Anger (0-10): ", 0, 10)
    shame = prompt_int("   Shame (0-10): ", 0, 10)
    relief = prompt_int("   Relief (0-10): ", 0, 10)

    intensity = prompt_int("\n5) Overall intensity (1-10): ", 1, 10)

    notes = input("\n6) Additional notes (optional): ").strip()

    entry = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "timestamp": now_iso(),
        "trigger": trigger,
        "before": before,
        "after": after,
        "feelings": {
            "anxiety": anxiety,
            "sadness": sadness,
            "anger": anger,
            "shame": shame,
            "relief": relief,
        },
        "intensity": intensity,
        "notes": notes,
    }

    print("\n--- Entry summary ---")
    print(f"Trigger : {entry['trigger']}")
    print(f"Before  : {entry['before']}")
    print(f"After   : {entry['after']}")
    print("Feelings:")
    for k, v in entry["feelings"].items():
        print(f"  - {k.capitalize():7}: {v}")
    print(f"Intensity: {entry['intensity']}")
    if entry["notes"]:
        print(f"Notes    : {entry['notes']}")
    else:
        print("Notes    : (none)")

    confirm = input("\nSave this entry? (Y/n) ").strip().lower()
    if confirm in ("", "y", "yes"):
        return entry
    print("Entry discarded.")
    return None


def add_entry(entry):
    data = read_json(DATA_FILE)
    data.append(entry)
    write_json(DATA_FILE, data)
    print("Entry saved.")


def show_recent(n=10):
    data = read_json(DATA_FILE)
    if not data:
        print("No entries found.")
        return
    print(f"\n--- Most recent {min(n, len(data))} entries ---")
    for e in sorted(data, key=lambda x: x["timestamp"], reverse=True)[:n]:
        ts = e["timestamp"]
        trig = e["trigger"]
        inten = e.get("intensity", "")
        print(f"{ts} | {trig} | intensity: {inten}")


def summary():
    data = read_json(DATA_FILE)
    if not data:
        print("No data available for summary.")
        return
    print("\n--- Summary ---")
    counts = count_triggers(data)
    print(f"Total entries: {len(data)}")
    print("\nTop triggers (by count):")
    for trig, cnt in counts.most_common(10):
        print(f"  {trig} — {cnt}")

    avg = average_emotion_scores(data)
    print("\nAverage feelings (0-10):")
    for k, v in avg.items():
        print(f"  {k.capitalize():7}: {v:.2f}")

    per_day = triggers_per_day(data)
    print("\nEntries per day (most recent 10):")
    for date, cnt in list(per_day.items())[-10:]:
        print(f"  {date}: {cnt}")


def generate_reports():
    data = read_json(DATA_FILE)
    if not data:
        print("No entries to export.")
        return
    csv_path = os.path.join(REPORTS_DIR, f"triggers_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    export_csv(data, csv_path)
    print(f"CSV exported: {csv_path}")


def interactive_menu():
    ensure_dirs()
    while True:
        print("\n=== Trigger Tracker Menu ===")
        print("1) Log new trigger")
        print("2) Show recent entries")
        print("3) Summary statistics")
        print("4) Export CSV report")
        print("5) Exit")
        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            entry = prompt_entry()
            if entry:
                add_entry(entry)
        elif choice == "2":
            show_recent(10)
        elif choice == "3":
            summary()
        elif choice == "4":
            generate_reports()
        elif choice == "5":
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Invalid selection. Enter a number from 1 to 5.")


if __name__ == "__main__":
    interactive_menu()
