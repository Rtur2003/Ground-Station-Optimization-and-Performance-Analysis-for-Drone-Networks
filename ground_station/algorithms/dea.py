from __future__ import annotations

import random
import time
from typing import List, Tuple

from ..problem import AssignmentProblem, AssignmentResult


class DifferentialEvolution:
    def __init__(
        self,
        population_size: int = 30,
        max_iterations: int = 200,
        scaling_factor: float = 0.8,
        crossover_rate: float = 0.7,
    ) -> None:
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.scaling_factor = scaling_factor
        self.crossover_rate = crossover_rate

    def solve(self, problem: AssignmentProblem) -> AssignmentResult:
        start = time.time()
        population = [self._random_vector(problem) for _ in range(self.population_size)]
        best = population[0]
        best_fitness = problem.evaluate(best)
        history: List[float] = [best_fitness]

        for _ in range(self.max_iterations):
            for i in range(self.population_size):
                trial = self._mutate_and_crossover(problem, population, i)
                trial_fitness = problem.evaluate(trial)
                current_fitness = problem.evaluate(population[i])
                if trial_fitness < current_fitness:
                    population[i] = trial
                if trial_fitness < best_fitness:
                    best = trial
                    best_fitness = trial_fitness
            history.append(best_fitness)

        elapsed = time.time() - start
        assignments = [int(gene[0]) if gene[0] >= 0 else -1 for gene in best]
        return AssignmentResult(
            assignments=assignments,
            fitness=best_fitness,
            elapsed_seconds=elapsed,
            history={"best_fitness": history},
        )

    def _random_vector(self, problem: AssignmentProblem) -> List[Tuple[int, float]]:
        available = list(range(len(problem.stations)))
        random.shuffle(available)
        vector: List[Tuple[int, float]] = []
        for drone in problem.drones:
            station_idx = available.pop() if available else -1
            battery = random.uniform(0, drone.max_battery_level)
            vector.append((station_idx, battery))
        return vector

    def _mutate_and_crossover(
        self, problem: AssignmentProblem, population: List[List[Tuple[int, float]]], idx: int
    ) -> List[Tuple[int, float]]:
        indices = list(range(len(population)))
        indices.remove(idx)
        a, b, c = random.sample(indices, 3)
        donor: List[Tuple[int, float]] = []
        for j in range(len(population[idx])):
            xa, xb, xc = population[a][j][0], population[b][j][0], population[c][j][0]
            new_station = xa + self.scaling_factor * (xb - xc)
            new_station = max(-1, min(int(round(new_station)), len(problem.stations) - 1))
            new_battery = population[a][j][1] + self.scaling_factor * (population[b][j][1] - population[c][j][1])
            new_battery = max(0.0, min(new_battery, problem.drones[j].max_battery_level))
            donor.append((new_station, new_battery))

        trial: List[Tuple[int, float]] = []
        for j, gene in enumerate(population[idx]):
            if random.random() < self.crossover_rate or j == random.randint(0, len(population[idx]) - 1):
                trial.append(donor[j])
            else:
                trial.append(gene)

        # enforce uniqueness if requested
        if problem.require_unique_station:
            seen = set()
            for j, (station_idx, battery) in enumerate(trial):
                if station_idx >= 0 and station_idx in seen:
                    available = [s for s in range(len(problem.stations)) if s not in seen]
                    station_idx = random.choice(available) if available else -1
                    trial[j] = (station_idx, battery)
                if station_idx >= 0:
                    seen.add(station_idx)

        return trial
