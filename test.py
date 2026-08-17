import requests
import streamlit as st
API_KEY = st.secrets["OPENWEATHER_API_KEY"]
url = f"https://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={API_KEY}&units=metric"

try:
    print("Sending request...")

    res = requests.get(url)

    print("Status Code:", res.status_code)
    print("Response Text:", res.text)

except Exception as e:
    print("ERROR:", e)