from __future__ import annotations

import random

from ..data import build_drones, build_stations
from ..problem import AssignmentProblem


def moving_drones_and_stations(
    num_drones: int = 6, num_stations: int = 5, area_size: int = 800, seed: int = 1337
) -> AssignmentProblem:
    random.seed(seed)
    stations_named = []
    for idx in range(num_stations):
        stations_named.append(
            (
                f"Istasyon {chr(65 + idx)}",
                (random.randint(0, area_size), random.randint(0, area_size)),
            )
        )
    drones_positions = tuple((random.randint(0, area_size), random.randint(0, area_size)) for _ in range(num_drones))
    stations = build_stations(stations_named)
    drones = build_drones(drones_positions)
    return AssignmentProblem(drones=drones, stations=stations)
