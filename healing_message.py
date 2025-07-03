def get_healing_message(df_log):
    if len(df_log) < 3:
        return "⏳ Not enough data yet. Try recording your mood for a few more days!"

    last_scores = df_log.tail(3)["Score"].tolist()
    trend = "up" if last_scores[-1] > last_scores[0] else "down"
    avg = df_log["Score"].mean()

    if avg <= 4:
        return "☁️ It's been a tough time lately. Your feelings are valid and important."
    elif trend == "down":
        return "🌙 Your emotional curve is slightly declining. It's okay to take a break."
    elif trend == "up":
        return "☀️ You're doing great! Your mood is steadily improving."
    else:
        return "📘 Your heart feels calm and steady. Wishing you continued peace today."
