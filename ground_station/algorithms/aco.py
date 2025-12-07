from __future__ import annotations

import random
import time
from typing import List, Tuple

from ..problem import AssignmentProblem, AssignmentResult


class AntColony:
    def __init__(
        self,
        num_ants: int = 30,
        num_iterations: int = 200,
        evaporation_rate: float = 0.5,
        alpha: float = 1.0,
        beta: float = 2.0,
        initial_pheromone: float = 1.0,
        deposit_weight: float = 1.0,
    ) -> None:
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.initial_pheromone = initial_pheromone
        self.deposit_weight = deposit_weight

    def solve(self, problem: AssignmentProblem) -> AssignmentResult:
        start = time.time()
        pheromones = [self.initial_pheromone for _ in range(len(problem.stations))]
        best_solution: List[int] = [-1 for _ in problem.drones]
        best_fitness = float("inf")
        history: List[float] = []

        for _ in range(self.num_iterations):
            ants: List[Tuple[List[int], float]] = []
            for _ in range(self.num_ants):
                assignment = self._construct_solution(problem, pheromones)
                fitness = problem.evaluate([(s, problem.drones[i].max_battery_level) for i, s in enumerate(assignment)])
                ants.append((assignment, fitness))

                if fitness < best_fitness:
                    best_fitness = fitness
                    best_solution = assignment

            pheromones = [(1 - self.evaporation_rate) * p for p in pheromones]

            # deposit based on ant quality (lower fitness => higher deposit)
            for assignment, fitness in ants:
                deposit_amount = self.deposit_weight / (fitness + 1e-9)
                for station_idx in assignment:
                    if station_idx >= 0:
                        pheromones[station_idx] += deposit_amount

            history.append(best_fitness)

        elapsed = time.time() - start
        return AssignmentResult(
            assignments=best_solution,
            fitness=best_fitness,
            elapsed_seconds=elapsed,
            history={"best_fitness": history},
        )

    def _construct_solution(self, problem: AssignmentProblem, pheromones: List[float]) -> List[int]:
        available = list(range(len(problem.stations)))
        assignment: List[int] = []
        for drone in problem.drones:
            if not available:
                assignment.append(-1)
                continue

            weights = []
            for station_idx in available:
                pheromone_component = pheromones[station_idx] ** self.alpha
                distance = problem._distance(drone.position, problem.stations[station_idx].position)
                heuristic = (1 / (distance + 1e-9)) ** self.beta
                weights.append(pheromone_component * heuristic)

            selected = random.choices(available, weights=weights, k=1)[0]
            assignment.append(selected)
            available.remove(selected)

        return assignment
