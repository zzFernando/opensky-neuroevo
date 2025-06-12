import numpy as np
import random
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from typing import List, Tuple

def load_airports(filepath="data/airports.csv"):
    return pd.read_csv(filepath)

def get_airport_by_iata(airports_df, iata):
    row = airports_df[airports_df['IATA'] == iata]
    if row.empty:
        raise ValueError(f"Aeroporto {iata} não encontrado.")
    return row.iloc[0]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def route_distance(route):
    dist = 0
    for i in range(len(route) - 1):
        dist += haversine(route[i][0], route[i][1], route[i+1][0], route[i+1][1])
    return dist

def angle_penalty(route):
    penalty = 0
    for i in range(1, len(route)-1):
        a = np.array(route[i-1])
        b = np.array(route[i])
        c = np.array(route[i+1])
        ba = a - b
        bc = c - b
        cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        if angle < np.deg2rad(60):  # penaliza curvas < 60 graus
            penalty += (np.deg2rad(60) - angle)
    return penalty


def zone_penalty(route: List[Tuple[float, float]], zones: List[Tuple[float, float, float]]) -> float:
    """Penalize routes that pass through restricted circular zones."""
    if not zones:
        return 0.0

    def point_segment_distance(p, a, b):
        # p, a, b are (lat, lon)
        pa = np.array([p[0] - a[0], p[1] - a[1]])
        ba = np.array([b[0] - a[0], b[1] - a[1]])
        h = np.clip(np.dot(pa, ba) / np.dot(ba, ba), 0.0, 1.0)
        d = pa - h * ba
        return np.linalg.norm(d)

    penalty = 0.0
    for lat_c, lon_c, rad in zones:
        center = (lat_c, lon_c)
        for i in range(len(route) - 1):
            a = route[i]
            b = route[i + 1]
            dist = point_segment_distance(center, a, b)
            if dist < rad / 111:  # approximate conversion km -> degrees
                penalty += (rad - dist * 111)
                break
    return penalty

def fitness(route: List[Tuple[float, float]], zones: List[Tuple[float, float, float]] = None) -> float:
    dist = route_distance(route)
    angle = angle_penalty(route)
    zone = zone_penalty(route, zones or [])
    return dist + 100 * angle + 1000 * zone


def evaluate_route(
    route: List[Tuple[float, float]],
    zones: List[Tuple[float, float, float]] | None = None,
) -> dict:
    """Return detailed fitness components for a route."""
    dist = route_distance(route)
    angle = angle_penalty(route)
    zone = zone_penalty(route, zones or [])
    return {
        "distance": dist,
        "angle_penalty": angle,
        "zone_penalty": zone,
        "fitness": dist + 100 * angle + 1000 * zone,
    }

def random_waypoint(bounds):
    lat = random.uniform(bounds['lat_min'], bounds['lat_max'])
    lon = random.uniform(bounds['lon_min'], bounds['lon_max'])
    return (lat, lon)

def create_individual(start, end, n_waypoints, bounds):
    waypoints = [random_waypoint(bounds) for _ in range(n_waypoints)]
    return [start] + waypoints + [end]

def mutate(ind, bounds, mutation_rate=0.2):
    for i in range(1, len(ind)-1):
        if random.random() < mutation_rate:
            ind[i] = random_waypoint(bounds)
    return ind

def crossover(parent1, parent2):
    n = len(parent1)
    cut = random.randint(1, n-2)
    child = parent1[:cut] + parent2[cut:]
    return child

def evolutionary_route(start, end, bounds, n_waypoints=5, pop_size=30, generations=50, zones: List[Tuple[float, float, float]] = None):
    """Evolve a route using a simple genetic algorithm.

    Returns the best route found, a list of the best route from each generation,
    and the corresponding fitness values for those routes.
    """
    pop = [create_individual(start, end, n_waypoints, bounds) for _ in range(pop_size)]
    best_per_gen: List[List[tuple]] = []
    best_scores: List[float] = []
    for gen in range(generations):
        scored = [(ind, fitness(ind, zones)) for ind in pop]
        scored.sort(key=lambda x: x[1])
        best = scored[0][0]
        best_per_gen.append(best)
        best_scores.append(scored[0][1])
        survivors = [ind for ind, _ in scored[:pop_size//2]]
        children = []
        while len(children) < pop_size:
            p1, p2 = random.sample(survivors, 2)
            child = crossover(p1, p2)
            child = mutate(child, bounds)
            children.append(child)
        pop = children
    scored = [(ind, fitness(ind, zones)) for ind in pop]
    scored.sort(key=lambda x: x[1])
    best = scored[0][0]
    best_per_gen[-1] = best
    best_scores[-1] = scored[0][1]
    return best, best_per_gen, best_scores
