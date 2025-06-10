import random
from typing import List, Tuple


def generate_storms(n: int, bounds: dict, radius_range: Tuple[float, float]) -> List[Tuple[float, float, float]]:
    """Generate synthetic circular storm zones.

    Returns a list of (lat, lon, radius_km).
    """
    storms = []
    for _ in range(n):
        lat = random.uniform(bounds['lat_min'], bounds['lat_max'])
        lon = random.uniform(bounds['lon_min'], bounds['lon_max'])
        radius = random.uniform(*radius_range)
        storms.append((lat, lon, radius))
    return storms


def generate_flights(n: int, bounds: dict, n_points: int = 5) -> List[List[Tuple[float, float]]]:
    """Generate synthetic flight paths represented as lists of points."""
    flights = []
    for _ in range(n):
        start = (
            random.uniform(bounds['lat_min'], bounds['lat_max']),
            random.uniform(bounds['lon_min'], bounds['lon_max']),
        )
        end = (
            random.uniform(bounds['lat_min'], bounds['lat_max']),
            random.uniform(bounds['lon_min'], bounds['lon_max']),
        )
        path = [(
            start[0] + (end[0] - start[0]) * i / (n_points - 1) + random.uniform(-0.1, 0.1),
            start[1] + (end[1] - start[1]) * i / (n_points - 1) + random.uniform(-0.1, 0.1),
        ) for i in range(n_points)]
        flights.append(path)
    return flights
