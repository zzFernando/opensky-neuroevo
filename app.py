import streamlit as st
from streamlit_folium import st_folium

from evolution import load_airports, get_airport_by_iata, evolutionary_route, evaluate_route
from synthetic_data import generate_storms, generate_flights
from visualizer import create_route_map

st.set_page_config(page_title="Route Evolution", layout="wide")
st.title("✈️ Route Evolution Explorer")

# Load airport data
airports = load_airports()

origem = st.selectbox("Origem", airports["IATA"])
destino = st.selectbox(
    "Destino",
    airports["IATA"],
    index=1 if len(airports) > 1 else 0,
)

def run_evolution():
    a1 = get_airport_by_iata(airports, origem)
    a2 = get_airport_by_iata(airports, destino)
    start = (a1["Latitude"], a1["Longitude"])
    end = (a2["Latitude"], a2["Longitude"])
    bounds = {
        "lat_min": min(a1["Latitude"], a2["Latitude"]) - 2,
        "lat_max": max(a1["Latitude"], a2["Latitude"]) + 2,
        "lon_min": min(a1["Longitude"], a2["Longitude"]) - 2,
        "lon_max": max(a1["Longitude"], a2["Longitude"]) + 2,
    }
    storms = generate_storms(2, bounds, (50, 100))
    flights = generate_flights(3, bounds, n_points=6)
    zones = storms + [(lat, lon, 10) for path in flights for (lat, lon) in path]
    best_route, best_per_gen = evolutionary_route(
        start,
        end,
        bounds,
        n_waypoints=5,
        pop_size=40,
        generations=60,
        zones=zones,
    )
    st.session_state.result = {
        "best_per_gen": best_per_gen,
        "storms": storms,
        "flights": flights,
        "zones": zones,
    }

if st.button("Executar Evolução"):
    run_evolution()

if "result" in st.session_state:
    res = st.session_state.result
    gen = st.slider("Geração", 1, len(res["best_per_gen"]), len(res["best_per_gen"]))
    route = res["best_per_gen"][gen - 1]
    metrics = evaluate_route(route, res["zones"])
    st.markdown(
        f"**Distância:** {metrics['distance']:.1f} km\n\n"
        f"**Angulo penalização:** {metrics['angle_penalty']:.2f}\n\n"
        f"**Zona penalização:** {metrics['zone_penalty']:.2f}"
    )
    m = create_route_map(route, airports, zones=res["storms"], flights=res["flights"])
    st_folium(m, width=700, height=500)

