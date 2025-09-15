#!/usr/bin/env python3
"""
Trigger Tracker - Streamlit Web Application
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from datetime import datetime, timedelta
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Trigger Tracker",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .emotion-bar {
        height: 20px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    .sidebar-content {
        background-color: #f8f9fc;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .entry-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .feeling-chip {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Data management
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "triggers.json")
REPORTS_DIR = "reports"

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

def read_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def save_entry(entry):
    data = read_json(DATA_FILE)
    data.append(entry)
    write_json(DATA_FILE, data)

# Initialize
ensure_dirs()

# Header
st.markdown('<div class="main-header">🌟 Trigger Tracker</div>', unsafe_allow_html=True)
st.markdown("*A safe space to understand your patterns and grow stronger*")

# Sidebar navigation
with st.sidebar:
    st.markdown("### Navigation")
    page = st.selectbox("Go to:", ["📝 New Entry", "📊 Dashboard", "📈 Analytics", "📋 History", "💾 Export"])

# Load data
data = read_json(DATA_FILE)

if page == "📝 New Entry":
    st.header("Log a New Trigger")
    
    with st.form("trigger_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            trigger = st.text_input("What was the trigger?", placeholder="Describe what happened...")
            
            col_before, col_after = st.columns(2)
            with col_before:
                before = st.text_area("What happened before?", placeholder="Context leading up to it...", height=100)
            with col_after:
                after = st.text_area("What happened after?", placeholder="Your response or what followed...", height=100)
        
        with col2:
            st.subheader("Rate Your Feelings")
            st.caption("0 = not at all, 10 = very intense")
            
            anxiety = st.slider("😰 Anxiety", 0, 10, 0)
            sadness = st.slider("😢 Sadness", 0, 10, 0)
            anger = st.slider("😠 Anger", 0, 10, 0)
            shame = st.slider("😔 Shame", 0, 10, 0)
            relief = st.slider("😌 Relief", 0, 10, 0)
            
            intensity = st.slider("⚡ Overall Intensity", 1, 10, 5)
        
        notes = st.text_area("Additional notes (optional)", placeholder="Any other thoughts or observations...")
        
        submitted = st.form_submit_button("Save Entry", type="primary")
        
        if submitted:
            if trigger.strip():
                entry = {
                    "id": int(datetime.utcnow().timestamp() * 1000),
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "trigger": trigger.strip(),
                    "before": before.strip(),
                    "after": after.strip(),
                    "feelings": {
                        "anxiety": anxiety,
                        "sadness": sadness,
                        "anger": anger,
                        "shame": shame,
                        "relief": relief,
                    },
                    "intensity": intensity,
                    "notes": notes.strip(),
                }
                
                save_entry(entry)
                st.success("✅ Entry saved successfully!")
                st.balloons()
            else:
                st.error("Please describe the trigger before saving.")

elif page == "📊 Dashboard":
    if not data:
        st.info("No entries yet. Start by logging your first trigger!")
    else:
        st.header("Your Trigger Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Entries", len(data))
        
        with col2:
            avg_intensity = sum(e.get("intensity", 0) for e in data) / len(data)
            st.metric("Avg Intensity", f"{avg_intensity:.1f}/10")
        
        with col3:
            recent_entries = [e for e in data if datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S") > datetime.now() - timedelta(days=7)]
            st.metric("This Week", len(recent_entries))
        
        with col4:
            triggers = [e["trigger"] for e in data]
            most_common = Counter(triggers).most_common(1)
            if most_common:
                st.metric("Top Trigger", most_common[0][0][:15] + ("..." if len(most_common[0][0]) > 15 else ""))
        
        # Recent activity
        st.subheader("Recent Activity")
        recent_data = sorted(data, key=lambda x: x["timestamp"], reverse=True)[:5]
        
        for entry in recent_data:
            with st.container():
                st.markdown(f"""
                <div class="entry-card">
                    <strong>{entry['trigger']}</strong><br>
                    <small>{entry['timestamp']} • Intensity: {entry['intensity']}/10</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Feelings overview
        st.subheader("Average Feelings Profile")
        
        if data:
            feelings_data = {}
            for feeling in ["anxiety", "sadness", "anger", "shame", "relief"]:
                avg_score = sum(e["feelings"].get(feeling, 0) for e in data) / len(data)
                feelings_data[feeling] = avg_score
            
            df_feelings = pd.DataFrame(list(feelings_data.items()), columns=["Feeling", "Average Score"])
            
            fig = px.bar(df_feelings, x="Feeling", y="Average Score", 
                        color="Average Score", 
                        color_continuous_scale="viridis",
                        title="Your Emotional Patterns")
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

elif page == "📈 Analytics":
    if not data:
        st.info("Add some entries to see your analytics!")
    else:
        st.header("Pattern Analysis")
        
        # Convert to DataFrame
        df_data = []
        for entry in data:
            row = {
                "timestamp": datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S"),
                "trigger": entry["trigger"],
                "intensity": entry["intensity"],
                **entry["feelings"]
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        df["date"] = df["timestamp"].dt.date
        df["hour"] = df["timestamp"].dt.hour
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Triggers over time
            daily_counts = df.groupby("date").size().reset_index(name="count")
            fig = px.line(daily_counts, x="date", y="count", 
                         title="Triggers Over Time",
                         markers=True)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Hourly patterns
            hourly_counts = df.groupby("hour").size().reset_index(name="count")
            fig = px.bar(hourly_counts, x="hour", y="count",
                        title="Triggers by Hour of Day")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Top triggers
        st.subheader("Most Common Triggers")
        trigger_counts = Counter(df["trigger"]).most_common(10)
        
        if trigger_counts:
            triggers_df = pd.DataFrame(trigger_counts, columns=["Trigger", "Count"])
            fig = px.bar(triggers_df, x="Count", y="Trigger", 
                        orientation="h", title="Top 10 Triggers")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        st.subheader("Emotional Correlations")
        feelings_df = df[["anxiety", "sadness", "anger", "shame", "relief", "intensity"]]
        corr = feelings_df.corr()
        
        fig = px.imshow(corr, text_auto=True, aspect="auto", 
                       title="How Your Feelings Relate to Each Other")
        st.plotly_chart(fig, use_container_width=True)

elif page == "📋 History":
    st.header("Entry History")
    
    if not data:
        st.info("No entries to display yet.")
    else:
        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input("🔍 Search entries", placeholder="Search triggers, notes, or context...")
        with col2:
            days_back = st.selectbox("Show entries from:", [7, 30, 90, 365, 9999], 
                                   format_func=lambda x: f"Last {x} days" if x < 9999 else "All time")
        
        # Filter data
        filtered_data = data
        
        # Date filter
        if days_back < 9999:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            filtered_data = [e for e in filtered_data if datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S") > cutoff_date]
        
        # Search filter
        if search_term:
            search_lower = search_term.lower()
            filtered_data = [e for e in filtered_data if 
                           search_lower in e.get("trigger", "").lower() or
                           search_lower in e.get("before", "").lower() or
                           search_lower in e.get("after", "").lower() or
                           search_lower in e.get("notes", "").lower()]
        
        st.caption(f"Showing {len(filtered_data)} of {len(data)} entries")
        
        # Display entries
        for entry in sorted(filtered_data, key=lambda x: x["timestamp"], reverse=True):
            with st.expander(f"{entry['timestamp']} - {entry['trigger'][:50]}{'...' if len(entry['trigger']) > 50 else ''}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**Trigger:**", entry["trigger"])
                    if entry.get("before"):
                        st.write("**Before:**", entry["before"])
                    if entry.get("after"):
                        st.write("**After:**", entry["after"])
                    if entry.get("notes"):
                        st.write("**Notes:**", entry["notes"])
                
                with col2:
                    st.write("**Intensity:**", f"{entry['intensity']}/10")
                    st.write("**Feelings:**")
                    for feeling, score in entry["feelings"].items():
                        if score > 0:
                            st.write(f"• {feeling.capitalize()}: {score}/10")

elif page == "💾 Export":
    st.header("Export Your Data")
    
    if not data:
        st.info("No data to export yet.")
    else:
        st.write(f"Export {len(data)} entries to analyze elsewhere or keep as backup.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV Export
            if st.button("📊 Download CSV", type="primary"):
                # Prepare CSV data
                csv_data = []
                for entry in data:
                    row = {
                        "id": entry.get("id"),
                        "timestamp": entry.get("timestamp"),
                        "trigger": entry.get("trigger"),
                        "before": entry.get("before"),
                        "after": entry.get("after"),
                        "intensity": entry.get("intensity"),
                        "notes": entry.get("notes", ""),
                        "anxiety": entry["feelings"].get("anxiety", 0),
                        "sadness": entry["feelings"].get("sadness", 0),
                        "anger": entry["feelings"].get("anger", 0),
                        "shame": entry["feelings"].get("shame", 0),
                        "relief": entry["feelings"].get("relief", 0),
                    }
                    csv_data.append(row)
                
                df = pd.DataFrame(csv_data)
                csv = df.to_csv(index=False)
                
                st.download_button(
                    label="💾 Download CSV File",
                    data=csv,
                    file_name=f"triggers_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            # JSON Export
            if st.button("📋 Download JSON", type="secondary"):
                json_str = json.dumps(data, indent=2, ensure_ascii=False)
                
                st.download_button(
                    label="💾 Download JSON File",
                    data=json_str,
                    file_name=f"triggers_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        # Data preview
        st.subheader("Data Preview")
        if data:
            preview_data = []
            for entry in data[-5:]:  # Show last 5 entries
                preview_data.append({
                    "Date": entry["timestamp"],
                    "Trigger": entry["trigger"][:50] + ("..." if len(entry["trigger"]) > 50 else ""),
                    "Intensity": f"{entry['intensity']}/10"
                })
            
            st.dataframe(pd.DataFrame(preview_data), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Remember: This tool is for personal insight. For professional support, consider speaking with a mental health professional.*")