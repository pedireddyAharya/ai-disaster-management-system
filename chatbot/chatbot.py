def get_bot_response(query, risk):
    query = query.lower()

    if "help" in query or "what to do" in query:
        if risk == "HIGH RISK":
            return "🚨 Immediate evacuation required. Move to nearest safe zone and follow alerts."
        elif risk == "MODERATE RISK":
            return "⚠️ Stay alert. Avoid risky areas and prepare essentials."
        else:
            return "✅ Everything is safe. Stay updated."

    elif "safe" in query:
        return "🟢 Safe zones are shown in the map above."

    elif "weather" in query:
        return "🌦 Weather data is updated in real-time above."

    elif "evacuate" in query:
        return "🚨 Follow the blue evacuation route shown on the map."

    else:
        return "🤖 Ask me about safety, evacuation, weather, or risk."