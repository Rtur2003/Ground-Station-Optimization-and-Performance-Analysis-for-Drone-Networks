from __future__ import annotations

import random
import time
from typing import List, Tuple

from ..problem import AssignmentProblem, AssignmentResult


class Genetic:
    def __init__(
        self,
        population_size: int = 40,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.7,
        max_generations: int = 200,
    ) -> None:
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.max_generations = max_generations

    def solve(self, problem: AssignmentProblem) -> AssignmentResult:
        start = time.time()
        population = [self._random_individual(problem) for _ in range(self.population_size)]
        history: List[float] = []

        for _ in range(self.max_generations):
            fitnesses = [problem.evaluate(individual) for individual in population]
            best_idx = fitnesses.index(min(fitnesses))
            history.append(fitnesses[best_idx])

            next_population: List[List[Tuple[int, float]]] = [population[best_idx]]

            while len(next_population) < self.population_size:
                parent1 = self._select(population, fitnesses)
                parent2 = self._select(population, fitnesses)
                child1, child2 = self._crossover(parent1, parent2)
                child1 = self._mutate(child1, problem)
                child2 = self._mutate(child2, problem)
                next_population.extend([child1, child2])

            population = next_population[: self.population_size]

        fitnesses = [problem.evaluate(individual) for individual in population]
        best_idx = fitnesses.index(min(fitnesses))
        best_solution = population[best_idx]
        elapsed = time.time() - start
        assignments = [int(gene[0]) if gene[0] >= 0 else -1 for gene in best_solution]

        return AssignmentResult(
            assignments=assignments,
            fitness=fitnesses[best_idx],
            elapsed_seconds=elapsed,
            history={"best_fitness": history},
        )

    def _random_individual(self, problem: AssignmentProblem) -> List[Tuple[int, float]]:
        available = list(range(len(problem.stations)))
        random.shuffle(available)
        individual: List[Tuple[int, float]] = []
        for drone in problem.drones:
            station_idx = available.pop() if available else -1
            battery = random.uniform(0, drone.max_battery_level)
            individual.append((station_idx, battery))
        return individual

    def _select(self, population: List[List[Tuple[int, float]]], fitnesses: List[float]) -> List[Tuple[int, float]]:
        # roulette wheel selection (inverse fitness)
        inverted = [1 / (f + 1e-9) for f in fitnesses]
        total = sum(inverted)
        pick = random.uniform(0, total)
        current = 0.0
        for individual, weight in zip(population, inverted):
            current += weight
            if current >= pick:
                return [gene for gene in individual]
        return [gene for gene in population[-1]]

    def _crossover(
        self, parent1: List[Tuple[int, float]], parent2: List[Tuple[int, float]]
    ) -> Tuple[List[Tuple[int, float]], List[Tuple[int, float]]]:
        if random.random() > self.crossover_rate:
            return [gene for gene in parent1], [gene for gene in parent2]
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def _mutate(self, individual: List[Tuple[int, float]], problem: AssignmentProblem) -> List[Tuple[int, float]]:
        num_stations = len(problem.stations)
        for idx, (station_idx, battery) in enumerate(individual):
            if random.random() < self.mutation_rate:
                station_idx = random.randint(-1, num_stations - 1)
                battery = random.uniform(0, problem.drones[idx].max_battery_level)
                individual[idx] = (station_idx, battery)
        return individual
