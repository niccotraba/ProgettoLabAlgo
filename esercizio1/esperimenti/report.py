"""
Aggregazione e salvataggio dei risultati sperimentali.

Il modulo calcola le statistiche riassuntive delle misure grezze
e salva risultati, dati aggregati e informazioni sull'ambiente
di esecuzione in file CSV e JSON.
"""

from __future__ import annotations

import csv
import json
import platform
import sys

from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median, quantiles

from .configurazione import BenchmarkConfig
from .misurazioni import Measurement


@dataclass(frozen=True)
class AggregateMeasurement:
    """Risultato aggregato di un gruppo di misure."""

    scenario: str
    n: int
    structure: str
    operation: str
    samples: int

    median_total_ns: float
    q1_total_ns: float
    q3_total_ns: float
    iqr_total_ns: float

    median_per_operation_ns: float
    q1_per_operation_ns: float
    q3_per_operation_ns: float
    iqr_per_operation_ns: float


def _quartiles(
    values: list[float],
) -> tuple[float, float, float, float]:
    """Restituisce mediana, Q1, Q3 e IQR."""
    if not values:
        raise ValueError("Nessun valore da aggregare")

    med = float(median(values))

    if len(values) == 1:
        return med, med, med, 0.0

    q1, _, q3 = quantiles(
        values,
        n=4,
        method="inclusive",
    )

    return med, q1, q3, q3 - q1


def aggregate_measurements(
    measurements: list[Measurement],
) -> list[AggregateMeasurement]:
    """Aggrega le misure per scenario, n, struttura e operazione."""
    groups: dict[
        tuple[str, int, str, str],
        list[Measurement],
    ] = defaultdict(list)

    for measurement in measurements:
        key = (
            measurement.scenario,
            measurement.n,
            measurement.structure,
            measurement.operation,
        )

        groups[key].append(measurement)

    result: list[AggregateMeasurement] = []

    for key, group in sorted(groups.items()):
        scenario, n, structure, operation = key

        total_values = [
            float(item.total_ns)
            for item in group
        ]

        per_operation_values = [
            item.per_operation_ns
            for item in group
        ]

        (
            median_total,
            q1_total,
            q3_total,
            iqr_total,
        ) = _quartiles(total_values)

        (
            median_per_operation,
            q1_per_operation,
            q3_per_operation,
            iqr_per_operation,
        ) = _quartiles(per_operation_values)

        result.append(
            AggregateMeasurement(
                scenario=scenario,
                n=n,
                structure=structure,
                operation=operation,
                samples=len(group),
                median_total_ns=median_total,
                q1_total_ns=q1_total,
                q3_total_ns=q3_total,
                iqr_total_ns=iqr_total,
                median_per_operation_ns=median_per_operation,
                q1_per_operation_ns=q1_per_operation,
                q3_per_operation_ns=q3_per_operation,
                iqr_per_operation_ns=iqr_per_operation,
            )
        )

    return result


def write_measurements_csv(
    measurements: list[Measurement],
    path: Path,
) -> None:
    """Scrive le misure grezze."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not measurements:
        raise ValueError("Nessuna misura da salvare")

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(
                asdict(measurements[0]).keys()
            ),
        )

        writer.writeheader()

        for measurement in measurements:
            writer.writerow(
                asdict(measurement)
            )


def write_aggregates_csv(
    aggregates: list[AggregateMeasurement],
    path: Path,
) -> None:
    """Scrive le misure aggregate."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not aggregates:
        raise ValueError("Nessun risultato aggregato da salvare")

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(
                asdict(aggregates[0]).keys()
            ),
        )

        writer.writeheader()

        for aggregate in aggregates:
            writer.writerow(
                asdict(aggregate)
            )


def write_environment_json(
    path: Path,
    mode: str,
    config: BenchmarkConfig,
) -> None:
    """Salva le informazioni principali sull'ambiente di esecuzione."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    environment = {
        "mode": mode,
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "config": asdict(config),
    }

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            environment,
            file,
            indent=2,
            ensure_ascii=False,
        )