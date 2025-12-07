from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

from .models import Drone, Station

# Default drone catalogue pulled from legacy scripts.
DRONE_CATALOG = [
    {
        "name": "DJI Mavic Air 2",
        "max_speed": 68,
        "battery_capacity_mAh": 3500,
        "battery_voltage_V": 11.55,
    },
    {
        "name": "Parrot Anafi",
        "max_speed": 55,
        "battery_capacity_mAh": 6800,
        "battery_voltage_V": 11.55,
    },
    {
        "name": "Skydio 2",
        "max_speed": 55,
        "battery_capacity_mAh": 4280,
        "battery_voltage_V": 13.05,
    },
    {
        "name": "DJI Phantom 4 Pro",
        "max_speed": 72,
        "battery_capacity_mAh": 5870,
        "battery_voltage_V": 15.2,
    },
    {
        "name": "Autel Robotics EVO 2",
        "max_speed": 72,
        "battery_capacity_mAh": 7100,
        "battery_voltage_V": 11.55,
    },
    {
        "name": "Yuunec Typhoon H Pro",
        "max_speed": 70,
        "battery_capacity_mAh": 5400,
        "battery_voltage_V": 14.8,
    },
]


def build_drones(positions: Sequence[Tuple[float, float]]) -> List[Drone]:
    drones: List[Drone] = []
    for idx, (x, y) in enumerate(positions):
        model = DRONE_CATALOG[idx % len(DRONE_CATALOG)]
        battery_wh = (model["battery_capacity_mAh"] * model["battery_voltage_V"]) / 1000
        drones.append(
            Drone(
                model=model["name"],
                max_speed=model["max_speed"],
                max_battery_level=battery_wh,
                x=x,
                y=y,
            )
        )
    return drones


def build_stations(named_positions: Iterable[Tuple[str, Tuple[float, float]]]) -> List[Station]:
    return [Station(name=name, x=pos[0], y=pos[1]) for name, pos in named_positions]
