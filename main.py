# main.py
import os
import json
from datetime import datetime

import pandas as pd
import streamlit as st

from utils import helpers, storage, stats, export_utils

# ---------------- Setup ---------------- #
st.set_page_config(page_title="Trigger Tracker", page_icon="🧠", layout="wide")
st.title("🧠 Trigger Tracker")
st.markdown("Log detailed trigger entries (what, before, after, feelings) and view patterns over time.")

DATA_DIR = "data"
JSON_FILE = os.path.join(DATA_DIR, "triggers.json")
CSV_FILE = os.path.join(DATA_DIR, "triggers.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# Initialize storage files if missing
storage.ensure_files(JSON_FILE, CSV_FILE)

# ---------------- Entry Form ---------------- #
with st.form("entry_form", clear_on_submit=True):
    st.header("Log a new trigger")
    what = st.text_input("What was the trigger? (brief)")
    before = st.text_area("What happened just *before* the trigger? (context)")
    after = st.text_area("What happened *after* the trigger? (reaction / response)")
    # Emotion inputs - numeric scales
    st.subheader("Rate emotions (1 = low, 10 = high)")
    col1, col2, col3 = st.columns(3)
    with col1:
        anxiety = st.slider("Anxiety", 1, 10, 5)
        sadness = st.slider("Sadness", 1, 10, 3)
    with col2:
        anger = st.slider("Anger", 1, 10, 2)
        shame = st.slider("Shame", 1, 10, 1)
    with col3:
        stress = st.slider("Stress", 1, 10, 6)
        other_label = st.text_input("Other emotion label (optional)")
        other_value = st.slider("Other emotion intensity", 1, 10, 1) if other_label else 0

    overall = st.slider("Overall intensity (1-10)", 1, 10, 5)
    notes = st.text_area("Other notes (optional)")

    submitted = st.form_submit_button("Save entry")
    if submitted:
        if not what.strip():
            st.error("Please describe the trigger (short description).")
        else:
            timestamp = helpers.format_timestamp()
            entry = {
                "Timestamp": timestamp,
                "What": what.strip(),
                "Before": before.strip(),
                "After": after.strip(),
                "Anxiety": int(anxiety),
                "Sadness": int(sadness),
                "Anger": int(anger),
                "Shame": int(shame),
                "Stress": int(stress),
                "OverallIntensity": int(overall),
                "Notes": notes.strip()
            }
            if other_label:
                entry[other_label] = int(other_value)
            storage.append_entry_json(JSON_FILE, entry)
            storage.append_entry_csv(CSV_FILE, entry)
            st.success("Entry saved.")

# ---------------- Load Data ---------------- #
df = storage.load_dataframe(JSON_FILE)

# ---------------- Display & Controls ---------------- #
st.sidebar.header("Quick actions")
if st.sidebar.button("Refresh data"):
    st.experimental_rerun()

st.sidebar.markdown("### Export")
csv_bytes = export_utils.df_to_csv_bytes(df)
json_bytes = export_utils.json_file_bytes(JSON_FILE)
st.sidebar.download_button("Download CSV", csv_bytes, file_name="triggers_export.csv", mime="text/csv")
st.sidebar.download_button("Download JSON", json_bytes, file_name="triggers_export.json", mime="application/json")

st.sidebar.markdown("---")
if st.sidebar.button("Clear all data (irreversible)"):
    storage.clear_data(JSON_FILE, CSV_FILE)
    st.success("All data cleared. Reloading...")
    st.experimental_rerun()

# ---------------- Data Table ---------------- #
st.header("Recent entries")
if df.empty:
    st.info("No entries yet. Use the form above to log a trigger.")
else:
    st.dataframe(df.sort_values("Timestamp", ascending=False).reset_index(drop=True))

# ---------------- Analytics ---------------- #
st.header("Analytics & Patterns")
if not df.empty:
    colA, colB = st.columns([2, 1])

    with colA:
        st.subheader("Daily entry counts")
        daily = stats.daily_trigger_count(df)
        st.line_chart(daily)

        st.subheader("Average overall intensity (by day)")
        avg_daily = df.copy()
        avg_daily["Date"] = pd.to_datetime(avg_daily["Timestamp"]).dt.date
        avg_by_day = avg_daily.groupby("Date")["OverallIntensity"].mean()
        st.line_chart(avg_by_day)

    with colB:
        st.subheader("Emotion summary (most recent 30)")
        recent = df.tail(30)
        emotion_cols = stats.get_emotion_columns(recent)
        if emotion_cols:
            emotion_summary = recent[emotion_cols].mean().round(2)
            st.table(emotion_summary)
        else:
            st.write("No emotion data found.")

    st.subheader("Top triggers")
    top = stats.top_triggers(df, top_n=8)
    st.table(top)

    st.subheader("Patterns: frequent triggers by hour or weekday")
    hour_patterns = stats.triggers_by_hour_pattern(df, threshold=2)
    weekday_patterns = stats.triggers_by_weekday_pattern(df, threshold=2)
    st.write("By hour (trigger @ hour -> count):", hour_patterns or "None above threshold")
    st.write("By weekday (trigger @ weekday -> count):", weekday_patterns or "None above threshold")

# ---------------- Single-entry inspector ---------------- #
st.header("Inspect an entry")
if not df.empty:
    idx = st.number_input("Enter row index (0 - newest)", min_value=0, max_value=len(df)-1, value=0)
    entry = df.sort_values("Timestamp", ascending=False).reset_index(drop=True).loc[idx]
    st.markdown(f"**Timestamp:** {entry['Timest]()
