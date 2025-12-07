from __future__ import annotations

from typing import Tuple

from ..data import build_drones, build_stations
from ..problem import AssignmentProblem


def static_scenario() -> AssignmentProblem:
    station_positions: Tuple[Tuple[str, Tuple[float, float]], ...] = (
        ("Istasyon A", (200, 200)),
        ("Istasyon B", (500, 200)),
        ("Istasyon C", (200, 500)),
        ("Istasyon D", (500, 500)),
        ("Istasyon E", (350, 350)),
    )

    drone_positions = (
        (100, 100),
        (250, 250),
        (350, 500),
        (450, 300),
        (350, 450),
        (150, 350),
    )

    stations = build_stations(station_positions)
    drones = build_drones(drone_positions)
    return AssignmentProblem(drones=drones, stations=stations)
