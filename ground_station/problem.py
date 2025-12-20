from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

from .models import Drone, Station

AssignmentGene = Union[int, Tuple[int, float]]


@dataclass
class AssignmentResult:
    assignments: List[int]
    fitness: float
    elapsed_seconds: float
    history: Dict[str, List[float]] = field(default_factory=dict)


class AssignmentProblem:
    """
    Represents the drone-to-station assignment problem and provides a single fitness function
    used by all algorithms. A station index of -1 means unassigned.
    """

    def __init__(
        self,
        drones: Sequence[Drone],
        stations: Sequence[Station],
        unassigned_penalty: float = 100.0,
        require_unique_station: bool = True,
    ) -> None:
        if not drones:
            raise ValueError("At least one drone is required")
        if not stations:
            raise ValueError("At least one station is required")
        if unassigned_penalty < 0:
            raise ValueError("Unassigned penalty must be non-negative")
        
        self.drones = list(drones)
        self.stations = list(stations)
        self.unassigned_penalty = unassigned_penalty
        self.require_unique_station = require_unique_station

    def evaluate(self, solution: Sequence[AssignmentGene]) -> float:
        if solution is None:
            return math.inf

        assigned_stations = set()
        total = 0.0

        for idx, drone in enumerate(self.drones):
            gene = solution[idx]
            station_index, battery_level = self._parse_gene(gene, drone)

            if station_index is None:
                total += self.unassigned_penalty
                continue

            if self.require_unique_station and station_index in assigned_stations:
                total += self.unassigned_penalty
                continue

            assigned_stations.add(station_index)

            station = self.stations[station_index]
            distance = self._distance(drone.position, station.position)
            battery_fitness = 1 - (battery_level / drone.max_battery_level)
            total += (distance / max(drone.max_speed, 1e-9)) + battery_fitness

        return total

    def random_assignment(self, randomize_battery: bool = False) -> List[Tuple[int, float]]:
        """
        Build a random feasible assignment (unique stations when available).
        
        Args:
            randomize_battery: If True, assigns random battery levels; 
                             if False, uses max battery level (default).
        """
        available = list(range(len(self.stations)))
        random.shuffle(available)
        assignments: List[Tuple[int, float]] = []

        for drone in self.drones:
            station_idx = available.pop() if available else -1
            battery = random.uniform(0, drone.max_battery_level) if randomize_battery else drone.max_battery_level
            assignments.append((station_idx, battery))

        return assignments

    def _parse_gene(self, gene: AssignmentGene, drone: Drone) -> Tuple[Optional[int], float]:
        if isinstance(gene, tuple):
            station_idx, battery_level = gene
        else:
            station_idx, battery_level = gene, drone.max_battery_level

        if station_idx is None or station_idx < 0 or station_idx >= len(self.stations):
            return None, max(0.0, min(battery_level, drone.max_battery_level))

        station_idx = int(station_idx)
        battery_level = max(0.0, min(battery_level, drone.max_battery_level))
        return station_idx, battery_level

    @staticmethod
    def _distance(a: Iterable[float], b: Iterable[float]) -> float:
        ax, ay = a
        bx, by = b
        return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
