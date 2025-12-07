"""
Algorithm adapters exposing a consistent interface for assignment optimization.
Each algorithm implements `solve(problem: AssignmentProblem) -> AssignmentResult`.
"""

from .abc import ArtificialBeeColony
from .aco import AntColony
from .dea import DifferentialEvolution
from .ga import Genetic
from .goa import Grasshopper
from .gwo import GreyWolf
from .pso import ParticleSwarm

__all__ = [
    "AntColony",
    "ArtificialBeeColony",
    "DifferentialEvolution",
    "Genetic",
    "Grasshopper",
    "GreyWolf",
    "ParticleSwarm",
]
