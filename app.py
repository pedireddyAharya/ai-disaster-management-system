import streamlit as st
import pandas as pd
import cv2
import random

from weather.weather import get_weather
from prediction.risk import predict_risk
from utils.precautions import get_precautions
from mapping.map import create_map
from detection.detect import detect_people

from streamlit_folium import st_folium
import plotly.graph_objects as go
import streamlit.components.v1 as components
import requests
def get_cached_map(lat, lon):
    return create_map(lat, lon)
def get_forecast_series(city):
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]

    # get coordinates
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo = requests.get(geo_url).json()

    if not geo:
        return None

    lat = geo[0]["lat"]
    lon = geo[0]["lon"]

    # forecast API
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    time = []
    temp_series = []
    humidity_series = []
    wind_series = []

    for i in range(7):
        item = data["list"][i]

        time.append(item["dt_txt"][-8:-3])  # time only
        temp_series.append(item["main"]["temp"])
        humidity_series.append(item["main"]["humidity"])
        wind_series.append(item["wind"]["speed"])

    return time, temp_series, humidity_series, wind_series
st.set_page_config(layout="wide")

# -------------------------------
# 🎨 FUTURISTIC UI
# -------------------------------

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #00e5ff;
    margin-bottom: 20px;
}

/* CARD */
.card {
    background: rgba(15, 23, 42, 0.9);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 0 25px rgba(0,229,255,0.2);
    margin-bottom: 20px;
}

/* METRIC BAR */
.metric-card {
    background: linear-gradient(145deg, #020617, #0f172a);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 20px rgba(0,229,255,0.2);
}

/* TEXT FIX */
p, span, div {
    color: #e2e8f0 !important;
}

/* INPUT */
input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
}

/* BUTTON */
button {
    background: linear-gradient(45deg, #22c55e, #00e5ff) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* RISK COLORS */
.safe { color: #22c55e; font-weight: bold; }
.moderate { color: #facc15; font-weight: bold; }
.high { color: #ef4444; font-weight: bold; }

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚨 AegisAI Disaster Management & Rescue System</div>', unsafe_allow_html=True)

# -------------------------------
# SESSION STATE
# -------------------------------
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

if "camera_on" not in st.session_state:
    st.session_state.camera_on = False

# -------------------------------
# INPUT
# -------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
with st.form("form"):
    col1, col2 = st.columns(2)

    with col1:
        city = st.text_input("📍 Enter City")

    submit = st.form_submit_button("🚀 Get Weather")
st.markdown('</div>', unsafe_allow_html=True)

if submit:
        st.session_state.weather_data = get_weather(city.strip())

data = st.session_state.weather_data
# -------------------------------
# WEATHER DISPLAY
# -------------------------------
if data:
    col1, col2, col3 = st.columns(3)

    col1.markdown(f'<div class="metric-card">🌡<br><h2>{data["temp"]}°C</h2>Temperature</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card">💧<br><h2>{data["humidity"]}%</h2>Humidity</div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card">🌬<br><h2>{data["wind"]} m/s</h2>Wind</div>', unsafe_allow_html=True)
    risk = predict_risk(data)

    color_class = "safe" if risk == "SAFE" else "moderate" if risk == "MODERATE" else "high"

    st.markdown(f"""
    <div class="card">
        ⚠️ Risk Level: <span class="{color_class}">{risk}</span>
    </div>
        """, unsafe_allow_html=True)

    st.write("### 🛟 Precautions")
    for p in get_precautions(risk):
        st.write("-", p)

    # -------------------------------
    # 📊 ADVANCED GRAPH
    # -------------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Weather Analytics")

    result = get_forecast_series(city)

    if result:
        time, temp_series, humidity_series, wind_series = result

    # smarter risk
    risk_series = []
    for i in range(len(temp_series)):
        score = 0

        if temp_series[i] > 40:
            score += 1
        if humidity_series[i] > 80:
            score += 1
        if wind_series[i] > 10:
            score += 1

        risk_series.append(score)

    colA, colB = st.columns(2)

    with colA:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=time, y=temp_series, name="Temp", line=dict(width=3)))
        fig1.add_trace(go.Scatter(x=time, y=humidity_series, name="Humidity", yaxis="y2"))

        fig1.update_layout(
            template="plotly_dark",
            title="Atmospheric Trend",
            yaxis=dict(title="Temp"),
            yaxis2=dict(overlaying='y', side='right', title="Humidity")
        )

        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=time, y=risk_series, name="Risk"))
        fig2.add_trace(go.Scatter(x=time, y=wind_series, name="Wind", yaxis="y2"))

        fig2.update_layout(
            template="plotly_dark",
            title="Threat & Wind",
            yaxis=dict(title="Risk"),
            yaxis2=dict(overlaying='y', side='right', title="Wind")
        )

        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # -------------------------------
    # 🗺 MAP
    # -------------------------------
    # ===============================
# FULL WIDTH MAP (OUTSIDE COLUMNS)
# ===============================
    st.markdown("### 🗺 Evacuation Map")

    st_folium(
    create_map(data["lat"], data["lon"]),
    height=500,
    use_container_width=True
)
else:
        st.info("Enter a city and click Get Weather")
# -------------------------------
# 🗺 SMART EVACUATION
# -------------------------------
if data:
    st.markdown("### 🚨 Evacuation Guidance")

    if data["wind"] > 10:
        st.error("🌪 Avoid open areas. Move indoors immediately.")

    elif data["humidity"] > 85:
        st.warning("🌊 Move to higher ground. Flood risk detected.")

    else:
        st.success("✅ No evacuation needed. Stay safe.")
# -------------------------------
# 🎥 CAMERA SECTION
# -------------------------------
st.subheader("🎥 Human Detection")

col1, col2 = st.columns(2)

if col1.button("▶️ Start Camera"):
    st.session_state.camera_on = True

if col2.button("⏹ Stop Camera"):
    st.session_state.camera_on = False

# -------------------------------
# 🚨 DASHBOARD WHEN CAMERA OFF
# -------------------------------
    # 📡 Alerts
    st.markdown("### 📡 Live Alerts")

    alerts = [
        "⚠️ Weather conditions may change",
        "📡 Monitoring environment...",
        "🌪 Wind fluctuations detected"
    ]

    for alert in alerts:
        st.warning(alert)

    # 🧠 AI Insights
    st.markdown("### 🧠 AI Insights")

    if data:
        if risk == "HIGH RISK":
            st.error("🚨 Evacuate immediately")
        elif risk == "MODERATE RISK":
            st.warning("⚠️ Stay alert")
        else:
            st.success("✅ Safe")

# -------------------------------
# CAMERA RUN
# -------------------------------
if st.session_state.camera_on:
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while st.session_state.camera_on:
        ret, frame = cap.read()
        if not ret:
            break

        count, img = detect_people(frame)

        cv2.putText(img, f"People: {count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        stframe.image(img, channels="BGR")

    cap.release()

# -------------------------------
# 🎯 MAIN LAYOUT (LIKE YOUR DESIGN)
# -------------------------------
st.set_page_config(layout="wide")
left, right = st.columns([2, 1],gap="large")

# -------------------------------
# LEFT SIDE → PANELS
# -------------------------------
with left:

    st.markdown("### 🌍 System Overview")

    # Panel 1
    st.markdown("""
    <div style="background:#020617;padding:20px;border-radius:15px;
    box-shadow:0 0 15px #00e5ff;color:white;margin-bottom:15px;">
    🌍 <b>System Status</b><br><br>
    🛰 Monitoring Environment<br>
    ⚡ Sensors Active<br>
    <span style="color:#22c55e;">✅ System Stable</span>
    </div>
    """, unsafe_allow_html=True)

    # Panel 2
    st.markdown("""
    <div style="background:#020617;padding:20px;border-radius:15px;
    box-shadow:0 0 15px #00e5ff;color:white;margin-bottom:15px;">
    ⚡ <b>Quick Safety Tips</b><br><br>
    🌊 Flood → Move to higher ground<br>
    🔥 Fire → Avoid smoke & exits<br>
    🌪 Storm → Stay indoors
    </div>
    """, unsafe_allow_html=True)

    # Panel 3 (Dynamic Data)
    if data:
        st.markdown(f"""
        <div style="background:#020617;padding:20px;border-radius:15px;
        box-shadow:0 0 15px #00e5ff;color:white;">
        📊 <b>Live Weather</b><br><br>
        🌡 Temp: {data['temp']}°C<br>
        💧 Humidity: {data['humidity']}%<br>
        🌬 Wind: {data['wind']} m/s
        </div>
        """, unsafe_allow_html=True)


# ================================
# 🤖 RIGHT SIDE CHATBOT (FINAL FIXED)
# ================================
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"]) # 🔒 don't hardcode real key in production

def ai_chat(msg):
    try:
        response = client.chat.completions.create(
           model="openai/gpt-oss-20b",,
            messages=[
                {
                    "role": "system",
                    "content": "You are AegisAI, a disaster management assistant. Give short, practical safety advice."
                },
                {
                    "role": "user",
                    "content": msg
                }
            ]
        )
        return response.choices[0].message.content
    except:
        return "⚠️ AI service unavailable"

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================================
# RIGHT COLUMN ONLY
# ================================
with right:

    # Header
    st.markdown("### 🤖 Disaster Assistant")

    # ======================
    # SCROLLABLE CHAT BOX
    # ======================
    st.markdown("""
    <style>
    .chat-scroll {
        height: 400px;
        overflow-y: auto;
        background: #020617;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 0 25px #00e5ff;
    }

    .msg-user {
        text-align: right;
        margin: 6px;
    }

    .msg-bot {
        text-align: left;
        margin: 6px;
        color: #22c55e;
    }
    </style>
    """, unsafe_allow_html=True)

    # Chat messages ONLY inside styled box
    chat_html = '<div class="chat-scroll">'

    if not st.session_state.chat_history:
        chat_html += '<div class="msg-bot">👋 Hello! Ask about disasters.</div>'

    for role, msg in st.session_state.chat_history:
        if role == "user":
            chat_html += f'<div class="msg-user">👤 {msg}</div>'
        else:
            chat_html += f'<div class="msg-bot">🤖 {msg}</div>'

    chat_html += '</div>'

    st.markdown(chat_html, unsafe_allow_html=True)

    # ======================
    # INPUT (OUTSIDE BOX ✅)
    # ======================
    user_input = st.text_input("", placeholder="Type message...", key="chat_input")

    if st.button("Send", use_container_width=True):
        if user_input.strip():
            st.session_state.chat_history.append(("user", user_input))

            reply = ai_chat(user_input)

            st.session_state.chat_history.append(("bot", reply))

            st.rerun()
# -------------------------------
# 🤖 AUTO DISASTER DETECTION
# -------------------------------
def detect_disaster(data):
    if data["wind"] > 12:
        return "🌪 Storm Risk"
    elif data["humidity"] > 85:
        return "🌊 Flood Risk"
    elif data["temp"] > 42:
        return "🔥 Heatwave Risk"
    else:
        return "✅ No Major Disaster"

if data:
    disaster_type = detect_disaster(data)
    st.markdown(f"### 🤖 Detected Disaster Type: {disaster_type}")
# -------------------------------
# 🧠 AI INSIGHTS
# -------------------------------
if data:
    st.markdown("### 🧠 AI Insights")

    insight = []

    if data["wind"] > 10:
        insight.append("🌪 High wind speed detected → Possible storm conditions")

    if data["humidity"] > 80:
        insight.append("💧 High humidity → Rain/Flood chances")

    if data["temp"] > 40:
        insight.append("🔥 Extreme temperature → Heatwave alert")

    if not insight:
        insight.append("✅ Weather conditions are stable")

    for i in insight:
        st.info(i)