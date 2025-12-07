from __future__ import annotations

import random
import time
from typing import List, Tuple

from ..problem import AssignmentProblem, AssignmentResult


class GreyWolf:
    def __init__(self, num_wolves: int = 20, max_iterations: int = 200) -> None:
        self.num_wolves = num_wolves
        self.max_iterations = max_iterations

    def solve(self, problem: AssignmentProblem) -> AssignmentResult:
        start = time.time()
        wolves: List[List[Tuple[int, float]]] = [self._random_wolf(problem) for _ in range(self.num_wolves)]

        best_fitness = float("inf")
        best_wolf: List[Tuple[int, float]] = wolves[0]
        history: List[float] = []

        for t in range(self.max_iterations):
            fitnesses = [problem.evaluate(wolf) for wolf in wolves]
            alpha, beta, delta = self._select_top(wolves, fitnesses)

            # track best
            if fitnesses[fitnesses.index(min(fitnesses))] < best_fitness:
                best_fitness = min(fitnesses)
                best_wolf = [gene for gene in wolves[fitnesses.index(best_fitness)]]

            a = 2 - 2 * (t / self.max_iterations)
            updated = []
            for wolf in wolves:
                assigned = set()
                new_wolf: List[Tuple[int, float]] = []
                for idx, (station_idx, battery) in enumerate(wolf):
                    r1, r2 = random.random(), random.random()
                    A1 = 2 * a * r1 - a
                    C1 = 2 * r2

                    candidate = int(round(abs(alpha[idx][0] - A1 * abs(C1 * alpha[idx][0] - station_idx))))
                    candidate = max(-1, min(candidate, len(problem.stations) - 1))

                    if candidate >= 0 and candidate in assigned and problem.require_unique_station:
                        available = [s for s in range(len(problem.stations)) if s not in assigned]
                        candidate = random.choice(available) if available else -1

                    if candidate >= 0:
                        assigned.add(candidate)
                    new_wolf.append((candidate, battery))
                updated.append(new_wolf)

            wolves = updated
            history.append(best_fitness)

        elapsed = time.time() - start
        assignments = [int(gene[0]) if gene[0] >= 0 else -1 for gene in best_wolf]
        return AssignmentResult(
            assignments=assignments,
            fitness=best_fitness,
            elapsed_seconds=elapsed,
            history={"best_fitness": history},
        )

    def _random_wolf(self, problem: AssignmentProblem) -> List[Tuple[int, float]]:
        available = list(range(len(problem.stations)))
        random.shuffle(available)
        wolf: List[Tuple[int, float]] = []
        for drone in problem.drones:
            station_idx = available.pop() if available else -1
            battery = random.uniform(0, drone.max_battery_level)
            wolf.append((station_idx, battery))
        return wolf

    def _select_top(self, wolves: List[List[Tuple[int, float]]], fitnesses: List[float]):
        sorted_indices = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i])
        return wolves[sorted_indices[0]], wolves[sorted_indices[1]], wolves[sorted_indices[2]]
