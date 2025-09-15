import os
import pandas as pd
import streamlit as st
from utils import stats, helpers

if not os.path.exists("data"):
    os.makedirs("data")

csv_file = "data/triggers.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Timestamp", "Trigger", "Mood", "Intensity"])

st.set_page_config(page_title="Trigger Tracker", page_icon="🧠")
st.title("🧠 Trigger Tracker")
st.markdown("Log your triggers, moods, and intensity to spot patterns over time.")

with st.form("trigger_form"):
    trigger = st.text_input("Trigger description")
    mood = st.selectbox("Mood", ["Anxious", "Sad", "Angry", "Neutral", "Happy"])
    intensity = st.slider("Intensity (1-10)", 1, 10, 5)
    submitted = st.form_submit_button("Log Trigger")
    
    if submitted:
        timestamp = helpers.format_timestamp()
        intensity = helpers.validate_intensity(intensity)
        new_entry = pd.DataFrame([{
            "Timestamp": timestamp,
            "Trigger": trigger,
            "Mood": mood,
            "Intensity": intensity
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.success("Trigger logged!")

st.subheader("📊 Trigger History")
st.dataframe(df.tail(10))

st.subheader("📈 Analysis")
if not df.empty:
    st.metric("Average Intensity", stats.average_intensity(df))
    st.markdown("**Triggers by Mood:**")
    st.bar_chart(stats.triggers_by_mood(df))
    st.markdown("**Triggers per Day:**")
    st.line_chart(stats.daily_trigger_count(df))