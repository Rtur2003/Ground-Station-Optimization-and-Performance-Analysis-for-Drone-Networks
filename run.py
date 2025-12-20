import argparse
import random
from typing import Callable, Dict

from ground_station.algorithms import (
    AntColony,
    ArtificialBeeColony,
    DifferentialEvolution,
    Genetic,
    Grasshopper,
    GreyWolf,
    ParticleSwarm,
)
from ground_station.problem import AssignmentProblem
from ground_station.scenarios import (
    moving_drones_and_stations,
    moving_drones_static_stations,
    static_scenario,
)


ScenarioFactory = Callable[[], AssignmentProblem]


def get_scenarios() -> Dict[str, ScenarioFactory]:
    return {
        "static": static_scenario,
        "moving-drones": moving_drones_static_stations,
        "moving-all": moving_drones_and_stations,
    }


def build_algorithm(name: str, iterations: int):
    name = name.lower()
    if name == "pso":
        return ParticleSwarm(max_iterations=iterations)
    if name == "gwo":
        return GreyWolf(max_iterations=iterations)
    if name == "aco":
        return AntColony(num_iterations=iterations)
    if name == "ga":
        return Genetic(max_generations=iterations)
    if name == "abc":
        return ArtificialBeeColony(max_iterations=iterations)
    if name == "goa":
        return Grasshopper(max_iterations=iterations)
    if name == "dea":
        return DifferentialEvolution(max_iterations=iterations)
    raise ValueError(f"Unknown algorithm: {name}")


def main():
    parser = argparse.ArgumentParser(description="Drone -> ground station assignment simulation")
    parser.add_argument(
        "--scenario",
        choices=list(get_scenarios().keys()),
        default="static",
        help="Which scenario to run",
    )
    parser.add_argument(
        "--algo",
        choices=["pso", "gwo", "aco", "ga", "abc", "goa", "dea"],
        default="pso",
        help="Optimization algorithm",
    )
    parser.add_argument("--iterations", type=int, default=200, help="Iteration count")
    parser.add_argument("--seed", type=int, default=42, help="Randomness seed")
    args = parser.parse_args()

    if args.iterations <= 0:
        parser.error("Iterations must be positive")

    random.seed(args.seed)
    scenarios = get_scenarios()
    problem = scenarios[args.scenario]()
    algorithm = build_algorithm(args.algo, args.iterations)

    result = algorithm.solve(problem)

    print(f"Scenario: {args.scenario} | Algorithm: {args.algo}")
    print(f"Best fitness: {result.fitness:.4f} | Duration: {result.elapsed_seconds:.3f}s")
    print("\nAssignments:")
    for idx, station_idx in enumerate(result.assignments):
        drone = problem.drones[idx]
        if station_idx >= 0:
            station = problem.stations[station_idx]
            print(f"  - {drone.model} -> {station.name} ({station.x}, {station.y})")
        else:
            print(f"  - {drone.model} -> unassigned")


if __name__ == "__main__":
    main()
