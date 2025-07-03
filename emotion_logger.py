import pandas as pd
import os
from datetime import date

LOG_FILE = "emotion_log.csv"

def load_log():
    try:
        df = pd.read_csv(LOG_FILE)
        if "날짜" not in df.columns:
            raise ValueError("날짜 열 없음")
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError, ValueError):
        return pd.DataFrame(columns=["날짜", "감정점수"])

def save_score(score: int):
    today = date.today().isoformat()
    df = load_log()

    if today not in df["날짜"].values:
        new_row = pd.DataFrame([{"날짜": today, "감정점수": score}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(LOG_FILE, index=False)
        return True
    return False

def get_log():
    return load_log()
