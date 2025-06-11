import os
import folium
import pandas as pd
from typing import List, Tuple


def create_route_map(
    route: List[Tuple[float, float]],
    airports_df: pd.DataFrame,
    zones: List[Tuple[float, float, float]] | None = None,
    flights: List[List[Tuple[float, float]]] | None = None,
) -> folium.Map:
    lats = [p[0] for p in route]
    lons = [p[1] for p in route]
    center = [sum(lats) / len(lats), sum(lons) / len(lons)]
    m = folium.Map(location=center, zoom_start=6)
    for _, row in airports_df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"],],
            popup=f"{row['IATA']} - {row['Nome']}",
            icon=folium.Icon(color="blue", icon="plane", prefix="fa"),
        ).add_to(m)
    if flights:
        for path in flights:
            folium.PolyLine(path, color="gray", weight=1, opacity=0.5).add_to(m)
    if zones:
        for lat, lon, rad in zones:
            folium.Circle(
                [lat, lon],
                radius=rad * 1000,
                color="orange",
                fill=True,
                fill_opacity=0.3,
            ).add_to(m)
    folium.PolyLine(route, color="red", weight=4, opacity=0.8).add_to(m)
    for i, (lat, lon) in enumerate(route):
        folium.CircleMarker(
            [lat, lon],
            radius=4,
            color="black",
            fill=True,
            fill_color="yellow",
            popup=f"WP{i}",
        ).add_to(m)
    return m

def plot_route_on_map(
    route: List[Tuple[float, float]],
    airports_df: pd.DataFrame,
    filename: str = "results/route_map.html",
    zones: List[Tuple[float, float, float]] | None = None,
    flights: List[List[Tuple[float, float]]] | None = None,
) -> None:
    m = create_route_map(route, airports_df, zones=zones, flights=flights)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    m.save(filename)
    print(f"Mapa salvo em {filename}")

def plot_evolution_on_map(
    routes_per_gen: List[List[Tuple[float, float]]],
    airports_df: pd.DataFrame,
    filename: str = "results/evolution_map.html",
    zones: List[Tuple[float, float, float]] | None = None,
    flights: List[List[Tuple[float, float]]] | None = None,
) -> None:
    m = create_evolution_map(routes_per_gen, airports_df, zones=zones, flights=flights)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    m.save(filename)
    print(f"Mapa da evolução salvo em {filename}")


def create_evolution_map(
    routes_per_gen: List[List[Tuple[float, float]]],
    airports_df: pd.DataFrame,
    zones: List[Tuple[float, float, float]] | None = None,
    flights: List[List[Tuple[float, float]]] | None = None,
) -> folium.Map:
    if not routes_per_gen:
        raise ValueError("Nenhuma rota para exibir.")
    lats = [p[0] for p in routes_per_gen[-1]]
    lons = [p[1] for p in routes_per_gen[-1]]
    center = [sum(lats) / len(lats), sum(lons) / len(lons)]
    m = folium.Map(location=center, zoom_start=6)
    for _, row in airports_df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['IATA']} - {row['Nome']}",
            icon=folium.Icon(color="blue", icon="plane", prefix="fa"),
        ).add_to(m)
    if flights:
        for path in flights:
            folium.PolyLine(path, color="gray", weight=1, opacity=0.5).add_to(m)
    if zones:
        for lat, lon, rad in zones:
            folium.Circle(
                [lat, lon],
                radius=rad * 1000,
                color="orange",
                fill=True,
                fill_opacity=0.3,
            ).add_to(m)
    n = len(routes_per_gen)
    for i, route in enumerate(routes_per_gen):
        color = f"#{int(255*(i/n)):02x}00{int(255*(1-i/n)):02x}"
        opacity = 0.3 + 0.7 * (i/(n-1) if n > 1 else 1)
        folium.PolyLine(route, color=color, weight=2 if i < n - 1 else 5, opacity=opacity).add_to(m)
    for i, (lat, lon) in enumerate(routes_per_gen[-1]):
        folium.CircleMarker(
            [lat, lon],
            radius=4,
            color="black",
            fill=True,
            fill_color="yellow",
            popup=f"WP{i}",
        ).add_to(m)
    return m
