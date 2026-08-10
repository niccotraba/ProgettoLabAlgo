"""
Separo i parametri dal benchmark vero e proprio. Definisco con quali parametri vengono eseguiti gli esperimenti.

Definisco tre modalità:
- quick: sviluppo e controllo 
- calibration: per capire quanto costerebbe il benchmark full (non produce dati per la relazione)
- full: produzione dei dati definitivi


Configurazione degli esperimenti del primo esercizio.
"""

from dataclasses import dataclass
from typing import Literal


Scenario = Literal[
    "random_distinct",
    "increasing",
    "decreasing",
    "duplicate_heavy",
]


SCENARIOS: tuple[Scenario, ...] = (
    "random_distinct",
    "increasing",
    "decreasing",
    "duplicate_heavy",
)


@dataclass(frozen=True)
class BenchmarkConfig:
    """Configurazione di una campagna di benchmark."""

    sizes: tuple[int, ...]
    repetitions: int
    warmup_runs: int
    query_batch_size: int
    base_seed: int
    scenarios: tuple[Scenario, ...]


QUICK_CONFIG = BenchmarkConfig(
    sizes=(100, 300),
    repetitions=3,
    warmup_runs=1,
    query_batch_size=5,
    base_seed=2026,
    scenarios=SCENARIOS,
)


CALIBRATION_CONFIG = BenchmarkConfig(
    sizes=(100, 300, 900, 2700, 5000),
    repetitions=1,
    warmup_runs=0,
    query_batch_size=5,
    base_seed=2026,
    scenarios=SCENARIOS,
)


FULL_CONFIG = BenchmarkConfig(
    sizes=(100, 300, 900, 2700, 5000),
    repetitions=30,
    warmup_runs=3,
    query_batch_size=20,
    base_seed=2026,
    scenarios=SCENARIOS,
)