"""
Pre-defined scenarios used for benchmarking algorithms.
Each scenario returns an `AssignmentProblem` populated with drones and stations.
"""

from .static_drones_static_stations import static_scenario
from .moving_drones_static_stations import moving_drones_static_stations
from .moving_all import moving_drones_and_stations

__all__ = [
    "static_scenario",
    "moving_drones_static_stations",
    "moving_drones_and_stations",
]
