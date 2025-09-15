"""
Export helpers for Trigger Tracker.
Create CSV from JSON entries.
"""

import csv
from datetime import datetime


def export_csv(entries, path):
    """Write entries (list of dicts) to CSV file at path."""
    if not entries:
        raise ValueError("No entries to export.")

    # Flatten feelings into columns
    fieldnames = [
        "id",
        "timestamp",
        "trigger",
        "before",
        "after",
        "intensity",
        "notes",
        "feeling_anxiety",
        "feeling_sadness",
        "feeling_anger",
        "feeling_shame",
        "feeling_relief",
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in entries:
            feelings = e.get("feelings", {})
            row = {
                "id": e.get("id"),
                "timestamp": e.get("timestamp"),
                "trigger": e.get("trigger"),
                "before": e.get("before"),
                "after": e.get("after"),
                "intensity": e.get("intensity"),
                "notes": e.get("notes", ""),
                "feeling_anxiety": feelings.get("anxiety", 0),
                "feeling_sadness": feelings.get("sadness", 0),
                "feeling_anger": feelings.get("anger", 0),
                "feeling_shame": feelings.get("shame", 0),
                "feeling_relief": feelings.get("relief", 0),
            }
            writer.writerow(row)
