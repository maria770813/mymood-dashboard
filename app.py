import streamlit as st
import pandas as pd
import os
from datetime import date
from healing_message import get_healing_message
import random

st.set_page_config(
    page_title="Hyunkyung's Emotion Diary 💖",
    layout="wide"
)

# 💅 CSS styling
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #fff0f5;
            color: #4a3f3f;
            font-family: 'Nanum Gothic', sans-serif;
            font-size: 14.2px;
        }
        h1, h2, h3 {
            color: #8d6e63;
        }
        [data-testid="stSidebar"] {
            background-color: #ffe4f1 !important;
            font-size: 14px !important;
            color: #5a4552;
        }
        h4 {
            text-align: center;
            margin-top: 1rem;
        }
        .stButton>button {
            background-color: #f7b2b7;
            color: white;
            border-radius: 25px;
            border: none;
            padding: 0.5em 1.2em;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #f594a0;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Hyunkyung's Emotion Diary 💖")

# 📅 Emotion Score
today = date.today().isoformat()
score = st.slider("How would you rate your mood today?", 1, 10, 5)
st.write(f"🌈 Mood score for {today}: {score}")

# 📁 Load or create log file
log_file = "emotion_log.csv"
try:
    df_log = pd.read_csv(log_file)
    if "Date" not in df_log.columns:
        df_log.rename(columns={"날짜": "Date", "감정점수": "Score", "메모": "Memo"}, inplace=True)
except (FileNotFoundError, pd.errors.EmptyDataError, ValueError):
    df_log = pd.DataFrame(columns=["Date", "Score", "Memo"])

# 📝 Daily memo
memo = st.text_input(
    "📝 Write a short reflection for today",
    placeholder="e.g. I had a nice walk in the park!",
    key="memo_input_today"
)

if today not in df_log["Date"].values:
    new_row = pd.DataFrame([{
        "Date": today,
        "Score": score,
        "Memo": memo
    }])
    df_log = pd.concat([df_log, new_row], ignore_index=True)
    st.success("✨ Today's mood and memo have been saved!")
else:
    df_log.loc[df_log["Date"] == today, "Memo"] = memo
    st.info("✅ Mood already recorded for today. Memo has been updated.")

df_log.to_csv(log_file, index=False)

# 📊 Mood trend chart
st.subheader("📊 Mood Trend")
if not df_log.empty:
    st.line_chart(df_log.set_index("Date")["Score"])

# 😌 Mood classification
if len(df_log) >= 3:
    avg_score = df_log["Score"].mean()
    last_scores = df_log.tail(3)["Score"].tolist()
    trend = "up" if last_scores[-1] > last_scores[0] else "down"

    if avg_score <= 4:
        mood = "sad"
    elif trend == "down":
        mood = "down"
    elif trend == "up":
        mood = "happy"
    else:
        mood = "calm"
else:
    mood = "calm"
    st.info("⏳ Please record more days to see trends.")

# 🎨 Mood-based image & mascot
mood_assets = {
    "happy": {
        "img": "img/happy_day.jpg",
        "mascot": "🐥 It's a bright and joyful day!"
    },
    "down": {
        "img": "img/neutral_day.jpg",
        "mascot": "🐻 A calm and quiet moment."
    },
    "sad": {
        "img": "img/sad_day.jpg",
        "mascot": "🦥 Feeling a bit down? It's okay to rest."
    },
    "calm": {
        "img": "img/neutral_day.jpg",
        "mascot": "🐿️ A peaceful flow throughout the day."
    }
}
selected = mood_assets.get(mood, mood_assets["calm"])
st.image(selected["img"], use_column_width=True)
st.markdown(f"<h4 style='text-align: center;'>{selected['mascot']}</h4>", unsafe_allow_html=True)

# 💌 AI-generated message
message = get_healing_message(df_log)
st.subheader("💌 AI Suggested Message")
st.write(message)

# 🌸 Sidebar quotes
quotes_dict = {
    "sad": [
        "☁️ It's okay to feel down. You're doing your best.",
        "🥀 Tough days don't last. You're not alone.",
        "🫧 Be gentle with your heart today."
    ],
    "down": [
        "🌙 A gentle slowdown can be healing.",
        "🧘 Take a deep breath. You deserve peace.",
        "💤 You're doing great. Rest if you need."
    ],
    "happy": [
        "☀️ Shine bright today! Your smile is beautiful.",
        "🌼 Keep the joy alive in your heart.",
        "🎈 Celebrate the light within you."
    ],
    "calm": [
        "📖 Calm days are a gift to your soul.",
        "🫖 Stillness helps you hear your heart.",
        "🍃 You are enough, just as you are."
    ]
}

with st.sidebar:
    st.markdown("### 🌸 Daily Quote", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='font-size:14px; line-height:1.6; color:#5a4552;'>
            {random.choice(quotes_dict[mood])}
        </div>
    """, unsafe_allow_html=True)

# 📅 View diary by date
st.subheader("📅 View Past Entries")
selected_date = st.date_input("Select a date", value=date.today())
sel_str = str(selected_date)

if sel_str in df_log["Date"].values:
    row = df_log[df_log["Date"] == sel_str].iloc[0]
    st.markdown(f"""
    #### 📘 Entry for {sel_str}
    - Score: {row['Score']}
    - Memo: {row['Memo'] if row['Memo'] else '🕊️ No memo recorded'}
    """)
else:
    st.info("No entry found for the selected date.")
