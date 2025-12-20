from __future__ import annotations

import random
import time
from typing import List, Tuple

from ..problem import AssignmentProblem, AssignmentResult


class ArtificialBeeColony:
    def __init__(
        self,
        num_employed_bees: int = 20,
        num_onlooker_bees: int = 20,
        max_iterations: int = 200,
        limit: int = 50,
    ) -> None:
        self.num_employed_bees = num_employed_bees
        self.num_onlooker_bees = num_onlooker_bees
        self.max_iterations = max_iterations
        self.limit = limit

    def solve(self, problem: AssignmentProblem) -> AssignmentResult:
        start = time.time()
        employed = [
            (self._random_solution(problem), float("inf"), 0) for _ in range(self.num_employed_bees)
        ]  # (solution, fitness, trials)

        best_solution = employed[0][0]
        best_fitness = problem.evaluate(best_solution)
        history: List[float] = [best_fitness]

        for _ in range(self.max_iterations):
            employed = [
                self._employed_step(problem, sol, trials) for sol, _, trials in employed
            ]

            for _ in range(self.num_onlooker_bees):
                index = self._select_onlooker(employed)
                sol, fit, trials = employed[index]
                new_sol = self._neighbor(problem, sol)
                new_fit = problem.evaluate(new_sol)
                if new_fit < fit:
                    employed[index] = (new_sol, new_fit, 0)
                else:
                    employed[index] = (sol, fit, trials + 1)

            employed = [
                self._scout_step(problem, sol, fit, trials) for sol, fit, trials in employed
            ]

            for sol, fit, _ in employed:
                if fit < best_fitness:
                    best_fitness = fit
                    best_solution = sol
            history.append(best_fitness)

        elapsed = time.time() - start
        assignments = [int(gene[0]) if gene[0] >= 0 else -1 for gene in best_solution]
        return AssignmentResult(
            assignments=assignments,
            fitness=best_fitness,
            elapsed_seconds=elapsed,
            history={"best_fitness": history},
        )

    def _random_solution(self, problem: AssignmentProblem) -> List[Tuple[int, float]]:
        available = list(range(len(problem.stations)))
        random.shuffle(available)
        solution: List[Tuple[int, float]] = []
        for drone in problem.drones:
            station_idx = available.pop() if available else -1
            battery = random.uniform(0, drone.max_battery_level)
            solution.append((station_idx, battery))
        return solution

    def _neighbor(self, problem: AssignmentProblem, solution: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
        neighbor: List[Tuple[int, float]] = []
        available = list(range(len(problem.stations)))
        random.shuffle(available)
        for idx, (station_idx, _) in enumerate(solution):
            if station_idx >= 0 and station_idx in available:
                available.remove(station_idx)
            new_station = available.pop() if available else -1
            neighbor.append((new_station, random.uniform(0, problem.drones[idx].max_battery_level)))
        return neighbor

    def _employed_step(
        self, problem: AssignmentProblem, solution: List[Tuple[int, float]], trials: int
    ) -> Tuple[List[Tuple[int, float]], float, int]:
        new_sol = self._neighbor(problem, solution)
        fit_old = problem.evaluate(solution)
        fit_new = problem.evaluate(new_sol)
        if fit_new < fit_old:
            return new_sol, fit_new, 0
        return solution, fit_old, trials + 1

    def _scout_step(
        self, problem: AssignmentProblem, solution: List[Tuple[int, float]], fitness: float, trials: int
    ) -> Tuple[List[Tuple[int, float]], float, int]:
        if trials > self.limit:
            new_sol = self._random_solution(problem)
            return new_sol, problem.evaluate(new_sol), 0
        return solution, fitness, trials

    def _select_onlooker(self, employed: List[Tuple[List[Tuple[int, float]], float, int]]) -> int:
        fitness_values = [1 / (fit + 1e-9) for _, fit, _ in employed]
        total = sum(fitness_values)
        pick = random.uniform(0, total)
        current = 0.0
        for idx, weight in enumerate(fitness_values):
            current += weight
            if current >= pick:
                return idx
        return len(employed) - 1
