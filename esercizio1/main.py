"""
Punto di ingresso del programma sperimentale del primo esercizio.

Gestisce gli argomenti da riga di comando, seleziona la configurazione
quick, calibration o full e avvia l'esecuzione del benchmark.

Uso:
- nella root del progetto python -m esercizio1.main [--quick, --calibrate, --full]
"""

import argparse
from time import perf_counter

from esercizio1.esperimenti.benchmark import execute_benchmark
from esercizio1.esperimenti.configurazione import (
    CALIBRATION_CONFIG,
    FULL_CONFIG,
    QUICK_CONFIG,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark delle strutture per statistiche d'ordine."
        )
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--quick",
        action="store_true",
        help="Esegue la configurazione rapida.",
    )

    group.add_argument(
        "--calibrate",
        action="store_true",
        help="Esegue un run di calibrazione.",
    )

    group.add_argument(
        "--full",
        action="store_true",
        help="Esegue l'esperimento completo.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    if args.full:
        mode = "full"
        config = FULL_CONFIG

    elif args.calibrate:
        mode = "calibration"
        config = CALIBRATION_CONFIG

    else:
        mode = "quick"
        config = QUICK_CONFIG

    print(f"Modalità: {mode}")
    print(f"Dimensioni: {config.sizes}")
    print(f"Ripetizioni: {config.repetitions}")

    start = perf_counter()

    (
        raw_path,
        aggregate_path,
        environment_path,
        measurement_count,
    ) = execute_benchmark(
        config,
        mode,
    )

    elapsed = perf_counter() - start

    print()
    print(f"Misure prodotte: {measurement_count}")
    print(f"Tempo totale: {elapsed:.2f} s")
    print(f"Dati grezzi: {raw_path}")
    print(f"Dati aggregati: {aggregate_path}")
    print(f"Ambiente: {environment_path}")


if __name__ == "__main__":
    main()