# Ground Station Optimization for Drone Networks

Assign drones to ground stations with swarm / evolutionary heuristics and compare their performance across different mobility scenarios.

## What's inside

- Algorithms: PSO, Grey Wolf, Ant Colony, Genetic, Artificial Bee Colony, Grasshopper, Differential Evolution
- Scenarios:
  - `static`: fixed drone and station positions
  - `moving-drones`: random drone positions, fixed stations
  - `moving-all`: random drones and stations
- Clean Python package under `ground_station/` with shared models and a single fitness function
- CLI runner (`run.py`) and smoke tests under `tests/`

## Project layout

```
ground_station/
  algorithms/           # algorithm adapters with a common solve() interface
  scenarios/            # ready-to-run scenario factories
  data.py               # drone catalog and helpers to build drones/stations
  models.py             # Drone, Station dataclasses
  problem.py            # AssignmentProblem + fitness definition
run.py                  # CLI to run any scenario + algorithm combo
tests/                  # unittest smoke tests
dron_atamasi/           # legacy GUI scripts (kept for reference)
```

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate  # or source .venv/bin/activate on Unix
pip install -r requirements.txt  # optional, no strict deps by default

# Run a scenario
python run.py --scenario static --algo pso --iterations 200
python run.py --scenario moving-all --algo ga --iterations 300
```

## Testing

```bash
python -m unittest discover -s tests -v
```

## Notes

- `ground_station` code is the maintained path; legacy `dron_atamasi/*.py` remains for historical reference.
- Fitness function enforces unique station assignment by default; adjust in `AssignmentProblem` if you need a different policy.
