# main.py

import logging
import argparse
import sys
from evolution import (
    load_airports,
    get_airport_by_iata,
    evolutionary_route,
    evaluate_route,
)
from visualizer import plot_route_on_map, plot_evolution_on_map
from synthetic_data import generate_storms, generate_flights

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Gerar rotas usando algoritmo genético")
    parser.add_argument("origem", nargs="?", default="POA", help="IATA da origem")
    parser.add_argument("destino", nargs="?", default="GIG", help="IATA do destino")
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Iniciar interface Streamlit em vez da execução via terminal",
    )
    args = parser.parse_args()

    if args.ui:
        from streamlit.web import cli as stcli

        sys.argv = ["streamlit", "run", "app.py"]
        stcli.main()
        return

    airports = load_airports()
    origem = args.origem.upper()
    destino = args.destino.upper()
    a1 = get_airport_by_iata(airports, origem)
    a2 = get_airport_by_iata(airports, destino)
    start = (a1['Latitude'], a1['Longitude'])
    end = (a2['Latitude'], a2['Longitude'])
    # Limites para geração de waypoints
    bounds = {
        'lat_min': min(a1['Latitude'], a2['Latitude']) - 2,
        'lat_max': max(a1['Latitude'], a2['Latitude']) + 2,
        'lon_min': min(a1['Longitude'], a2['Longitude']) - 2,
        'lon_max': max(a1['Longitude'], a2['Longitude']) + 2,
    }
    storms = generate_storms(2, bounds, (50, 100))
    flights = generate_flights(3, bounds, n_points=6)
    zones = storms + [(lat, lon, 10) for path in flights for (lat, lon) in path]
    # Executa algoritmo evolutivo
    best_route, best_per_gen, _ = evolutionary_route(
        start,
        end,
        bounds,
        n_waypoints=5,
        pop_size=40,
        generations=60,
        zones=zones,
    )
    metrics = evaluate_route(best_route, zones)
    print("Melhor rota encontrada:")
    for i, wp in enumerate(best_route):
        print(f"WP{i}: {wp}")
    print(
        f"Distância: {metrics['distance']:.1f} km\n"
        f"Penalização por ângulo: {metrics['angle_penalty']:.2f}\n"
        f"Penalização por zonas: {metrics['zone_penalty']:.2f}"
    )
    # Visualização
    plot_route_on_map(best_route, airports, zones=storms, flights=flights)
    plot_evolution_on_map(best_per_gen, airports, zones=storms, flights=flights)

if __name__ == "__main__":
    main()
