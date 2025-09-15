import pandas as pd

def average_intensity(df):
    if df.empty:
        return 0
    return round(df["Intensity"].mean(), 2)

def triggers_by_mood(df):
    return df["Mood"].value_counts()

def daily_trigger_count(df):
    if df.empty:
        return pd.Series()
    df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
    return df.groupby('Date').size()