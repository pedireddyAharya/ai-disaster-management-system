import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
from shapely.geometry import LineString

# ================================
# 🚀 CREATE MAP (INSANE LEVEL)
# ================================
def create_map(lat, lon):

    dest_lat = lat + 0.05
    dest_lon = lon + 0.05

    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        scrollWheelZoom=False,
        tiles="CartoDB positron"
    )

    url = f"http://router.project-osrm.org/route/v1/driving/{lon},{lat};{dest_lon},{dest_lat}?overview=full&alternatives=true&geometries=geojson"
    res = requests.get(url)
    data = res.json()

    MAIN_BLUE = "#1E90FF"
    ALT_GRAY = "#6c757d"

    for i, route in enumerate(data["routes"]):

        coords = route["geometry"]["coordinates"]
        route_coords = [(c[1], c[0]) for c in coords]

        # Smooth route
        line = LineString(route_coords)
        route_coords = list(line.simplify(0.0001).coords)

        distance = route["distance"] / 1000
        duration = route["duration"] / 60

        # ====================
        # MAIN ROUTE
        # ====================
        if i == 0:

            # Glow
            folium.PolyLine(route_coords, color="white", weight=14).add_to(m)

            # Blue line
            folium.PolyLine(
                route_coords,
                color=MAIN_BLUE,
                weight=7,
                tooltip=f"{distance:.1f} km | {duration:.0f} min"
            ).add_to(m)

            # Stable traffic (no blinking)
            traffic_colors = ["#22c55e", "#facc15", "#ef4444"]

            for j in range(0, len(route_coords)-1, 15):
                segment = route_coords[j:j+15]

                traffic_color = traffic_colors[j % len(traffic_colors)]

                folium.PolyLine(
                    segment,
                    color=traffic_color,
                    weight=4,
                    opacity=0.8
                ).add_to(m)

            # Info card
            mid = route_coords[len(route_coords)//2]

            folium.Marker(
                mid,
                icon=folium.DivIcon(html=f"""
                <div style="
                    background:white;
                    padding:10px;
                    border-radius:15px;
                    font-size:13px;
                    box-shadow:0 6px 20px rgba(0,0,0,0.3);
                    text-align:center;
                    width:95px;
                ">
                    🚗<br>
                    <b>{distance:.1f} km</b><br>
                    ⏱ {duration:.0f} min
                </div>
                """)
            ).add_to(m)

        # ====================
        # ALT ROUTES
        # ====================
        else:
            folium.PolyLine(
                route_coords,
                color=ALT_GRAY,
                weight=5,
                opacity=0.6,
                dash_array="6,10"
            ).add_to(m)

    # ====================
    # MARKERS
    # ====================
    folium.Marker([lat, lon], tooltip="📍 You", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker([dest_lat, dest_lon], tooltip="🛟 Safe Zone", icon=folium.Icon(color="green")).add_to(m)

    return m


# ================================
# 🚀 CACHE (NO BLINKING)
# ================================
@st.cache_data(show_spinner=False)
def get_cached_map(lat, lon):
    return create_map(lat, lon)


# ================================
# 🚀 UI
# ================================
st.title("🚨 AegisAI Disaster Management System")

city = st.text_input("Enter City")

if st.button("Get Weather"):

    # Dummy coords (replace with your API)
    lat, lon = 17.3850, 78.4867  # Hyderabad

    st.session_state.map = get_cached_map(lat, lon)

# ================================
# 🚀 SHOW MAP
# ================================
if "map" in st.session_state:

    st.subheader("🗺 Evacuation Map")

    st_folium(
        st.session_state.map,
        height=450,
        width=700
    )