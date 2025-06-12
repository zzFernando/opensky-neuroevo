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

st.sidebar.header("Parâmetros")
num_storms = st.sidebar.slider("Número de tempestades", 0, 5, 2)
num_flights = st.sidebar.slider("Número de outros voos", 0, 5, 3)
n_waypoints = st.sidebar.slider("Waypoints", 3, 8, 5)
pop_size = st.sidebar.slider("Tamanho da população", 10, 100, 40, step=10)
generations = st.sidebar.slider("Gerações", 10, 100, 60, step=10)

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
    storms = generate_storms(num_storms, bounds, (50, 100))
    flights = generate_flights(num_flights, bounds, n_points=6)
    zones = storms + [(lat, lon, 10) for path in flights for (lat, lon) in path]
    best_route, best_per_gen, scores = evolutionary_route(
        start,
        end,
        bounds,
        n_waypoints=n_waypoints,
        pop_size=pop_size,
        generations=generations,
        zones=zones,
    )
    evals = [evaluate_route(r, zones) for r in best_per_gen]
    st.session_state.result = {
        "best_per_gen": best_per_gen,
        "storms": storms,
        "flights": flights,
        "zones": zones,
        "scores": scores,
        "evals": evals,
    }

if st.button("Executar Evolução"):
    run_evolution()

if "result" in st.session_state:
    res = st.session_state.result
    st.subheader("Evolução do fitness")
    st.line_chart(res["scores"])
    gen = st.slider(
        "Geração",
        1,
        len(res["best_per_gen"]),
        len(res["best_per_gen"]),
    )
    route = res["best_per_gen"][gen - 1]
    metrics = res["evals"][gen - 1]
    st.markdown(
        f"**Distância:** {metrics['distance']:.1f} km\n\n"
        f"**Angulo penalização:** {metrics['angle_penalty']:.2f}\n\n"
        f"**Zona penalização:** {metrics['zone_penalty']:.2f}"
    )
    m = create_route_map(route, airports, zones=res["storms"], flights=res["flights"])
    st_folium(m, width=1000, height=600)
    st.subheader("Métricas por geração")
    import pandas as pd
    df = pd.DataFrame(res["evals"]).assign(Geração=lambda d: d.index + 1)
    st.dataframe(df.set_index("Geração"))

