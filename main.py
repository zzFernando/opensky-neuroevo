# main.py

import logging
from evolution import load_airports, get_airport_by_iata, evolutionary_route
from visualizer import plot_route_on_map, plot_evolution_on_map

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Carrega aeroportos
    airports = load_airports()
    print("Aeroportos disponíveis:")
    print(airports[['IATA', 'Nome']])
    # Seleção de origem e destino
    origem = input("Digite o IATA do aeroporto de origem (ex: POA): ").strip().upper()
    destino = input("Digite o IATA do aeroporto de destino (ex: CGH): ").strip().upper()
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
    # Executa algoritmo evolutivo
    best_route, best_per_gen = evolutionary_route(start, end, bounds, n_waypoints=5, pop_size=40, generations=60)
    print("Melhor rota encontrada:")
    for i, wp in enumerate(best_route):
        print(f"WP{i}: {wp}")
    # Visualização
    plot_route_on_map(best_route, airports)
    plot_evolution_on_map(best_per_gen, airports)

if __name__ == "__main__":
    main()
