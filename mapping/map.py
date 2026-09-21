import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
from shapely.geometry import LineString


# ================================
# 🚀 CREATE MAP
# ================================
def create_map(lat, lon):

    dest_lat = lat + 0.05
    dest_lon = lon + 0.05

    # ================================
    # MAP
    # ================================
    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        scrollWheelZoom=False,
        tiles="OpenStreetMap"
    )

    # ================================
    # OSRM ROUTE
    # ================================
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{lon},{lat};{dest_lon},{dest_lat}"
        f"?overview=full&alternatives=true&geometries=geojson"
    )

    res = requests.get(url, timeout=15)
    data = res.json()

    # Check whether routes are available
    if "routes" not in data or not data["routes"]:
        st.warning("⚠️ Unable to find an evacuation route.")
        return m

    MAIN_BLUE = "#1E90FF"
    ALT_GRAY = "#6c757d"

    # ================================
    # ROUTES
    # ================================
    for i, route in enumerate(data["routes"]):

        coords = route["geometry"]["coordinates"]

        route_coords = [
            (c[1], c[0])
            for c in coords
        ]

        # ================================
        # SMOOTH ROUTE
        # ================================
        line = LineString(route_coords)

        route_coords = list(
            line.simplify(0.0001).coords
        )

        distance = route["distance"] / 1000
        duration = route["duration"] / 60

        # ================================
        # MAIN ROUTE
        # ================================
        if i == 0:

            # Route glow
            folium.PolyLine(
                route_coords,
                color="white",
                weight=14,
                opacity=0.8
            ).add_to(m)

            # Main blue route
            folium.PolyLine(
                route_coords,
                color=MAIN_BLUE,
                weight=7,
                tooltip=f"{distance:.1f} km | {duration:.0f} min"
            ).add_to(m)

            # ================================
            # TRAFFIC VISUALIZATION
            # ================================
            traffic_colors = [
                "#22c55e",
                "#facc15",
                "#ef4444"
            ]

            for j in range(
                0,
                len(route_coords) - 1,
                15
            ):

                segment = route_coords[j:j + 15]

                if len(segment) < 2:
                    continue

                traffic_color = traffic_colors[
                    (j // 15) % len(traffic_colors)
                ]

                folium.PolyLine(
                    segment,
                    color=traffic_color,
                    weight=4,
                    opacity=0.8
                ).add_to(m)

            # ================================
            # ROUTE INFO CARD
            # ================================
            mid = route_coords[
                len(route_coords) // 2
            ]

            folium.Marker(
                mid,
                icon=folium.DivIcon(
                    html=f"""
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
                    """
                )
            ).add_to(m)

        # ================================
        # ALTERNATIVE ROUTES
        # ================================
        else:

            folium.PolyLine(
                route_coords,
                color=ALT_GRAY,
                weight=5,
                opacity=0.6,
                dash_array="6,10"
            ).add_to(m)

    # ================================
    # USER MARKER
    # ================================
    folium.Marker(
        [lat, lon],
        tooltip="📍 You",
        icon=folium.Icon(
            color="blue"
        )
    ).add_to(m)

    # ================================
    # SAFE ZONE MARKER
    # ================================
    folium.Marker(
        [dest_lat, dest_lon],
        tooltip="🛟 Safe Zone",
        popup="🛟 Emergency Safe Zone",
        icon=folium.Icon(
            color="green"
        )
    ).add_to(m)

    return m


# ================================
# 🚀 CACHE
# ================================
@st.cache_data(show_spinner=False)
def get_cached_map(lat, lon):

    return create_map(lat, lon)


# ================================
# 🚀 UI
# ================================
st.title("🚨 AegisAI Disaster Management System")

city = st.text_input(
    "Enter City"
)


if st.button("Get Weather"):

    # Dummy coordinates for testing
    # Hyderabad
    lat, lon = 17.3850, 78.4867

    st.session_state.map = get_cached_map(
        lat,
        lon
    )


# ================================
# 🚀 SHOW MAP
# ================================
if "map" in st.session_state:

    st.subheader(
        "🗺 Evacuation Map"
    )

    st_folium(
        st.session_state.map,
        height=450,
        width=700
    )
