from __future__ import annotations

import random
import time
from typing import List, Tuple

from ..problem import AssignmentProblem, AssignmentResult


class Grasshopper:
    def __init__(self, population_size: int = 30, max_iterations: int = 200) -> None:
        self.population_size = population_size
        self.max_iterations = max_iterations

    def solve(self, problem: AssignmentProblem) -> AssignmentResult:
        start = time.time()
        population: List[List[Tuple[int, float]]] = [problem.random_assignment(randomize_battery=True) for _ in range(self.population_size)]
        best_solution = population[0]
        best_fitness = problem.evaluate(best_solution)
        history: List[float] = [best_fitness]

        for _ in range(self.max_iterations):
            for idx, sol in enumerate(population):
                fitness = problem.evaluate(sol)
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_solution = [gene for gene in sol]

                # move grasshopper toward best
                assigned = set()
                for j, (station_idx, battery) in enumerate(sol):
                    perturb = random.uniform(-1, 1)
                    candidate = int(round((station_idx + best_solution[j][0]) / 2 + perturb))
                    candidate = max(-1, min(candidate, len(problem.stations) - 1))
                    if candidate >= 0 and candidate in assigned and problem.require_unique_station:
                        available = [s for s in range(len(problem.stations)) if s not in assigned]
                        candidate = random.choice(available) if available else -1
                    if candidate >= 0:
                        assigned.add(candidate)
                    sol[j] = (candidate, battery)

                population[idx] = sol

            history.append(best_fitness)

        elapsed = time.time() - start
        assignments = [int(gene[0]) if gene[0] >= 0 else -1 for gene in best_solution]
        return AssignmentResult(
            assignments=assignments,
            fitness=best_fitness,
            elapsed_seconds=elapsed,
            history={"best_fitness": history},
        )
