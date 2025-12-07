from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Station:
    name: str
    x: float
    y: float

    @property
    def position(self) -> Tuple[float, float]:
        return self.x, self.y


@dataclass(frozen=True)
class Drone:
    model: str
    max_speed: float
    max_battery_level: float
    x: float
    y: float

    @property
    def position(self) -> Tuple[float, float]:
        return self.x, self.y
