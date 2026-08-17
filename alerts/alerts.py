import streamlit as st

def show_alert(risk):
    if risk == "HIGH RISK":
        st.error("🚨 HIGH RISK ALERT! Immediate action required!")
    elif risk == "MODERATE RISK":
        st.warning("⚠️ Moderate Risk. Stay cautious.")
    else:
        st.success("✅ Safe Conditions")