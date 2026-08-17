import requests
import streamlit as st
API_KEY = st.secrets["OPENWEATHER_API_KEY"]
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()

        print("DEBUG:", data)

        # ✅ FIX: handle both int and string
        if str(data.get("cod")) != "200":
            return None

        return {
    "temp": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "wind": data["wind"]["speed"],
    "weather": data["weather"][0]["main"],
    "lat": data["coord"]["lat"],     # ✅ ADD
    "lon": data["coord"]["lon"]      # ✅ ADD
}

    except Exception as e:
        print("ERROR:", e)
        return None