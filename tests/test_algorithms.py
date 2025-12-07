import unittest

from ground_station.algorithms import (
    AntColony,
    ArtificialBeeColony,
    DifferentialEvolution,
    Genetic,
    Grasshopper,
    GreyWolf,
    ParticleSwarm,
)
from ground_station.scenarios import static_scenario


class AlgorithmSmokeTests(unittest.TestCase):
    def setUp(self):
        self.problem = static_scenario()

    def _assert_solution(self, result):
        self.assertEqual(len(result.assignments), len(self.problem.drones))
        self.assertFalse(any(idx is None for idx in result.assignments))

    def test_pso(self):
        result = ParticleSwarm(num_particles=10, max_iterations=5).solve(self.problem)
        self._assert_solution(result)

    def test_gwo(self):
        result = GreyWolf(num_wolves=10, max_iterations=5).solve(self.problem)
        self._assert_solution(result)

    def test_ga(self):
        result = Genetic(population_size=10, max_generations=5).solve(self.problem)
        self._assert_solution(result)

    def test_aco(self):
        result = AntColony(num_ants=8, num_iterations=5).solve(self.problem)
        self._assert_solution(result)

    def test_abc(self):
        result = ArtificialBeeColony(num_employed_bees=6, num_onlooker_bees=6, max_iterations=5).solve(self.problem)
        self._assert_solution(result)

    def test_goa(self):
        result = Grasshopper(population_size=8, max_iterations=5).solve(self.problem)
        self._assert_solution(result)

    def test_dea(self):
        result = DifferentialEvolution(population_size=8, max_iterations=5).solve(self.problem)
        self._assert_solution(result)


if __name__ == "__main__":
    unittest.main()
