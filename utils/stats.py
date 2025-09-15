"""
Statistics helpers for Trigger Tracker.
"""

from collections import Counter, OrderedDict
import pandas as pd
from datetime import datetime


def average_emotion_scores(entries):
    """Compute average scores for each recorded feeling."""
    if not entries:
        return {"anxiety": 0, "sadness": 0, "anger": 0, "shame": 0, "relief": 0}
    sums = {"anxiety": 0.0, "sadness": 0.0, "anger": 0.0, "shame": 0.0, "relief": 0.0}
    count = 0
    for e in entries:
        f = e.get("feelings") or {}
        for k in sums:
            sums[k] += float(f.get(k, 0))
        count += 1
    return {k: (sums[k] / count) for k in sums}


def count_triggers(entries):
    """Return Counter of triggers (exact-match)."""
    triggers = [e.get("trigger", "").strip() for e in entries if e.get("trigger")]
    return Counter(triggers)


def triggers_per_hour(entries):
    """Return OrderedDict(hour -> count)."""
    hours = Counter()
    for e in entries:
        ts = e.get("timestamp")
        if not ts:
            continue
        try:
            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            hours[dt.hour] += 1
        except Exception:
            continue
    return OrderedDict(sorted(hours.items()))


def triggers_per_day(entries):
    """Return OrderedDict(date -> count)."""
    days = Counter()
    for e in entries:
        ts = e.get("timestamp")
        if not ts:
            continue
        try:
            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            days[dt.date().isoformat()] += 1
        except Exception:
            continue
    # return ordered by date
    ordered = OrderedDict(sorted(days.items()))
    return ordered
