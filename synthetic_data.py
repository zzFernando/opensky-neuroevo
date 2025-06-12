import random
from typing import List, Tuple


def generate_storms(
    n: int,
    start: Tuple[float, float],
    end: Tuple[float, float],
    radius_range: Tuple[float, float],
    deviation: float = 1.0,
) -> List[Tuple[float, float, float]]:
    """Generate storm zones roughly along the direct path from start to end."""

    storms = []
    for _ in range(n):
        t = random.random()
        lat = start[0] + (end[0] - start[0]) * t
        lon = start[1] + (end[1] - start[1]) * t
        lat += random.uniform(-deviation, deviation)
        lon += random.uniform(-deviation, deviation)
        radius = random.uniform(*radius_range)
        storms.append((lat, lon, radius))
    return storms


def generate_flights(
    n: int,
    start: Tuple[float, float],
    end: Tuple[float, float],
    n_points: int = 5,
    deviation: float = 1.0,
) -> List[List[Tuple[float, float]]]:
    """Generate flight paths that cross the direct route from start to end."""

    flights = []
    dx = end[1] - start[1]
    dy = end[0] - start[0]
    norm = (dx ** 2 + dy ** 2) ** 0.5 or 1.0
    perp = (-dy / norm, dx / norm)

    for _ in range(n):
        t = random.random()
        base_lat = start[0] + (end[0] - start[0]) * t
        base_lon = start[1] + (end[1] - start[1]) * t
        offset = random.uniform(-deviation, deviation)
        start_pt = (
            base_lat + perp[0] * offset,
            base_lon + perp[1] * offset,
        )
        end_pt = (
            base_lat - perp[0] * offset,
            base_lon - perp[1] * offset,
        )
        path = [(
            start_pt[0] + (end_pt[0] - start_pt[0]) * i / (n_points - 1) + random.uniform(-0.1, 0.1),
            start_pt[1] + (end_pt[1] - start_pt[1]) * i / (n_points - 1) + random.uniform(-0.1, 0.1),
        ) for i in range(n_points)]
        flights.append(path)
    return flights
