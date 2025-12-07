from __future__ import annotations

import random
import time
from typing import List, Tuple

from ..problem import AssignmentProblem, AssignmentResult


class ParticleSwarm:
    def __init__(
        self,
        num_particles: int = 30,
        max_iterations: int = 200,
        inertia_weight: float = 0.8,
        cognitive_weight: float = 1.5,
        social_weight: float = 2.0,
    ) -> None:
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

    def solve(self, problem: AssignmentProblem) -> AssignmentResult:
        start = time.time()
        num_stations = len(problem.stations)
        num_drones = len(problem.drones)

        particles: List[List[Tuple[int, float]]] = [
            self._random_particle(problem) for _ in range(self.num_particles)
        ]
        best_global = particles[0]
        best_global_fitness = problem.evaluate(best_global)
        fitness_history: List[float] = [best_global_fitness]

        for _ in range(self.max_iterations):
            for particle in particles:
                fitness = problem.evaluate(particle)
                if fitness < best_global_fitness:
                    best_global = [gene for gene in particle]
                    best_global_fitness = fitness

                # update particle positions (only station indices)
                assigned = set()
                for idx in range(num_drones):
                    station_index, battery = particle[idx]
                    inertia = self.inertia_weight * station_index
                    cognitive = self.cognitive_weight * random.random() * (station_index - best_global[idx][0])
                    social = self.social_weight * random.random() * (best_global[idx][0] - station_index)
                    candidate = int(round(inertia + cognitive + social))
                    candidate = max(-1, min(candidate, num_stations - 1))

                    if candidate >= 0 and candidate in assigned and problem.require_unique_station:
                        available = [s for s in range(num_stations) if s not in assigned]
                        candidate = random.choice(available) if available else -1

                    particle[idx] = (candidate, battery)
                    if candidate >= 0:
                        assigned.add(candidate)

            fitness_history.append(best_global_fitness)

        elapsed = time.time() - start
        assignments = [int(gene[0]) if gene[0] >= 0 else -1 for gene in best_global]
        return AssignmentResult(
            assignments=assignments,
            fitness=best_global_fitness,
            elapsed_seconds=elapsed,
            history={"best_fitness": fitness_history},
        )

    def _random_particle(self, problem: AssignmentProblem) -> List[Tuple[int, float]]:
        available = list(range(len(problem.stations)))
        random.shuffle(available)
        particle: List[Tuple[int, float]] = []
        for drone in problem.drones:
            station_idx = available.pop() if available else -1
            battery = random.uniform(0, drone.max_battery_level)
            particle.append((station_idx, battery))
        return particle
