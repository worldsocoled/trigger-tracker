#  Trigger Tracker

A personal tool for understanding emotional triggers and building self-awareness. Track patterns, analyze your responses, and grow stronger over time.

## ✨ Features

- **📝 Easy Logging**: Record triggers with detailed context and emotional ratings
- **📊 Beautiful Dashboard**: Visual insights into your patterns and progress
- **📈 Advanced Analytics**: Spot trends over time and identify correlations
- **🔍 Smart Search**: Find and filter entries with powerful search tools
- **💾 Data Export**: Download your data as CSV or JSON for backup or analysis
- **🎨 Clean Interface**: Modern, supportive design that feels safe and welcoming

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone or download this project**
   ```bash
   mkdir trigger-tracker
   cd trigger-tracker
   ```

2. **Set up the project structure**
   ```bash
   mkdir utils data reports
   touch app.py main.py requirements.txt
   touch utils/__init__.py utils/helpers.py utils/stats.py utils/export.py
   ```

3. **Add the code files** (copy content from the project files)

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Launch the app**
   ```bash
   # For the beautiful web interface
   streamlit run app.py
   
   # Or for the command-line version
   python main.py
   ```

## 🎯 How to Use

### Web Interface (Recommended)
1. **Run** `streamlit run app.py`
2. **Navigate** using the sidebar menu
3. **Log entries** in the "New Entry" section
4. **View insights** in Dashboard and Analytics
5. **Search history** to find specific entries
6. **Export data** for backup or external analysis

### Command Line Interface
1. **Run** `python main.py`
2. **Follow prompts** to log new triggers
3. **View summaries** and recent entries
4. **Export reports** to CSV format

## 📊 What You Can Track

### Entry Details
- **Trigger**: What happened that caused the response
- **Before**: Context leading up to the trigger
- **After**: Your reaction or what followed
- **Notes**: Additional thoughts or observations

### Emotional Ratings (0-10 scale)
- 😰 **Anxiety**: Nervousness, worry, fear
- 😢 **Sadness**: Grief, disappointment, low mood
- 😠 **Anger**: Frustration, irritation, rage
- 😔 **Shame**: Guilt, embarrassment, self-criticism
- 😌 **Relief**: Comfort, release, positive resolution

### Analysis Features
- **Intensity Tracking**: Overall emotional intensity (1-10)
- **Pattern Recognition**: Identify your most common triggers
- **Time Analysis**: See when triggers happen most often
- **Emotional Correlations**: Understand how feelings relate
- **Progress Tracking**: Monitor changes over time

## 📁 Project Structure

```
trigger-tracker/
├── app.py                 # Streamlit web application
├── main.py               # Command-line interface
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── utils/
│   ├── __init__.py      # Package initialization
│   ├── helpers.py       # Utility functions
│   ├── stats.py         # Statistical analysis
│   └── export.py        # Data export functions
├── data/
│   └── triggers.json    # Your data storage (auto-created)
└── reports/
    └── (exports)        # CSV/JSON exports (auto-created)
```

## 🔧 Technical Details

### Dependencies
- **streamlit**: Modern web interface framework
- **pandas**: Data manipulation and analysis
- **matplotlib**: Basic plotting capabilities
- **seaborn**: Enhanced data visualization
- **plotly**: Interactive charts and graphs

### Data Storage
- **Format**: JSON for flexibility and human readability
- **Location**: `data/triggers.json`
- **Backup**: Automatic exports available in multiple formats
- **Privacy**: All data stays local on your machine

### Export Options
- **CSV**: Spreadsheet-compatible format for analysis
- **JSON**: Full data backup with all details preserved
- **Filtering**: Export specific date ranges or search results

## 🛡️ Privacy & Security

- **Local Storage**: All data stays on your computer
- **No Cloud**: No data sent to external servers
- **Your Control**: Easy export and backup options
- **Open Source**: Full transparency in how your data is handled

## 🎨 Interface Overview

### 📝 New Entry
Clean, guided form for logging triggers with:
- Context capture (before/after)
- Emotional rating sliders
- Intensity measurement
- Optional notes section

### 📊 Dashboard
At-a-glance overview featuring:
- Key metrics and trends
- Recent activity feed
- Emotional pattern visualization
- Quick insights into your data

### 📈 Analytics
Deep dive into your patterns:
- Triggers over time charts
- Hourly pattern analysis
- Most common triggers ranking
- Emotional correlation heatmaps

### 📋 History
Comprehensive entry management:
- Advanced search and filtering
- Expandable detailed view
- Date range selection
- Full-text search across all fields

### 💾 Export
Data portability options:
- One-click CSV downloads
- JSON backup creation
- Preview before export
- Timestamped file naming

## 🤝 Getting Help

### Troubleshooting
- **Installation issues**: Ensure Python 3.7+ and pip are installed
- **Dependencies**: Run `pip install -r requirements.txt` again
- **Port conflicts**: Streamlit typically uses port 8501
- **Data location**: Check the `data/` folder for your `triggers.json` file

### Support Resources
- Check that all files are created with correct content
- Ensure you're running commands from the project directory
- Verify file permissions allow reading/writing to data folder

## 📖 Tips for Effective Use

### Getting Started
1. **Start small**: Log a few entries to get comfortable
2. **Be honest**: Accurate entries lead to better insights
3. **Stay consistent**: Regular logging reveals patterns
4. **Review regularly**: Use analytics to understand trends

### Making Progress
- **Look for patterns**: What triggers appear most often?
- **Notice timing**: When do triggers typically occur?
- **Track intensity**: Are triggers becoming less intense over time?
- **Celebrate growth**: Acknowledge positive changes and insights

### Professional Support
This tool is designed for personal insight and self-awareness. For professional mental health support, consider speaking with a qualified therapist or counselor who can provide personalized guidance.

## 📄 License

This project is open source and available for personal use. Feel free to modify and adapt it to your needs.

---

*Remember: Understanding your patterns is the first step toward positive change. Be patient and compassionate with yourself as you grow.*
