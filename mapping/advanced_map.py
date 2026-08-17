import folium
import requests

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjJlZWIzY2U2MzMwNjRhMGQ4NjQwNjJiY2NhMjIwMmQwIiwiaCI6Im11cm11cjY0In0="

def get_route(start, end):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [start[1], start[0]],
            [end[1], end[0]]
        ]
    }

    res = requests.post(url, json=body, headers=headers)
    data = res.json()

    coords = data["features"][0]["geometry"]["coordinates"]
    return [(c[1], c[0]) for c in coords]


def create_advanced_map(lat, lon, risk):
    # ✅ FIXED TILE (NO ERROR)
    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        tiles="CartoDB positron"
    )

    # Risk color
    color = "green"
    if risk == "HIGH RISK":
        color = "red"
    elif risk == "MODERATE RISK":
        color = "orange"

    # Risk zone
    folium.Circle(
        location=[lat, lon],
        radius=500,
        color=color,
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

    # Safe zone
    safe_lat = lat + 0.02
    safe_lon = lon + 0.02

    folium.Marker(
        [safe_lat, safe_lon],
        popup="Safe Zone",
        icon=folium.Icon(color="green")
    ).add_to(m)

    # Route
    try:
        route = get_route((lat, lon), (safe_lat, safe_lon))

        folium.PolyLine(route, color="blue", weight=5).add_to(m)

    except:
        folium.PolyLine(
            [[lat, lon], [safe_lat, safe_lon]],
            color="blue"
        ).add_to(m)

    return m