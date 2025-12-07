from __future__ import annotations

import random
from typing import Tuple

from ..data import build_drones, build_stations
from ..problem import AssignmentProblem


def moving_drones_static_stations(
    num_drones: int = 6, area_size: int = 800, seed: int = 42
) -> AssignmentProblem:
    random.seed(seed)
    station_positions: Tuple[Tuple[str, Tuple[float, float]], ...] = (
        ("Istasyon A", (200, 200)),
        ("Istasyon B", (500, 200)),
        ("Istasyon C", (200, 500)),
        ("Istasyon D", (500, 500)),
        ("Istasyon E", (350, 350)),
    )
    drones_positions = tuple((random.randint(0, area_size), random.randint(0, area_size)) for _ in range(num_drones))
    stations = build_stations(station_positions)
    drones = build_drones(drones_positions)
    return AssignmentProblem(drones=drones, stations=stations)
