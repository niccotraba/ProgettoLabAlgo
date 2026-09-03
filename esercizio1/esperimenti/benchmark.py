"""
Orchestrazione del benchmark del primo esercizio.

Il modulo applica il protocollo sperimentale alle tre strutture,
coordinando generazione dei dati, costruzione, misurazione delle
operazioni, rotazione dell'ordine di esecuzione e raccolta dei risultati.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from esercizio1.strutture import (
    BinarySearchTree,
    OrderedLinkedList,
    OrderStatisticAVL,
)

from .configurazione import BenchmarkConfig
from .generatori import (
    QueryTargets,
    derive_seed,
    generate_input,
    prepare_query_targets,
)
from .misurazioni import (
    Measurement,
    Structure,
    measure_batch,
    measure_build,
    measure_single,
    root_size,
    structure_height,
)
from .report import (
    aggregate_measurements,
    write_aggregates_csv,
    write_environment_json,
    write_measurements_csv,
)


@dataclass(frozen=True)
class StructureSpec:
    """Nome e factory di una struttura da confrontare."""

    name: str
    factory: Callable[[], Structure]


STRUCTURES: tuple[StructureSpec, ...] = (
    StructureSpec(
        name="ordered_list",
        factory=OrderedLinkedList,
    ),
    StructureSpec(
        name="bst",
        factory=BinarySearchTree,
    ),
    StructureSpec(
        name="avl",
        factory=OrderStatisticAVL,
    ),
)


def _rotated_structures(
    run: int,
) -> tuple[StructureSpec, ...]:
    """Ruota l'ordine delle strutture in funzione del run."""
    # La rotazione distribuisce l'eventuale effetto dell'ordine di esecuzione
    # tra le strutture, evitando che la prima sia sempre nello stesso ruolo.
    offset = run % len(STRUCTURES)

    return (
        STRUCTURES[offset:]
        + STRUCTURES[:offset]
    )


def _make_measurement(
    *,
    run: int,
    data_seed: int,
    target_seed: int,
    scenario: str,
    n: int,
    structure_name: str,
    operation: str,
    target_type: str,
    batch_size: int,
    total_ns: int,
    per_operation_ns: float,
    height_after_build: int | None,
    root_size_after_build: int | None,
) -> Measurement:
    """Costruisce un record di misura."""
    return Measurement(
        run=run,
        data_seed=data_seed,
        target_seed=target_seed,
        scenario=scenario,
        n=n,
        structure=structure_name,
        operation=operation,
        target_type=target_type,
        batch_size=batch_size,
        total_ns=total_ns,
        per_operation_ns=per_operation_ns,
        height_after_build=height_after_build,
        root_size_after_build=root_size_after_build,
    )


def _measure_structure(
    *,
    spec: StructureSpec,
    data: list[int],
    targets: QueryTargets,
    run: int,
    data_seed: int,
    target_seed: int,
    scenario: str,
) -> list[Measurement]:
    """
    Esegue tutte le misurazioni previste su una struttura.

    La cancellazione viene eseguita per ultima perché modifica
    la struttura.
    """
    n = len(data)

    structure, build_ns = measure_build(
        spec.factory,
        data,
    )

    height = structure_height(structure)
    augmented_root_size = root_size(structure)

    measurements: list[Measurement] = []

    measurements.append(
        _make_measurement(
            run=run,
            data_seed=data_seed,
            target_seed=target_seed,
            scenario=scenario,
            n=n,
            structure_name=spec.name,
            operation="build",
            target_type="all_insertions",
            batch_size=n,
            total_ns=build_ns,
            per_operation_ns=build_ns / n,
            height_after_build=height,
            root_size_after_build=augmented_root_size,
        )
    )

    # Tutti i nodi necessari a rank e delete vengono individuati
    # PRIMA delle relative misurazioni: la preparazione non deve contribuire
    # ai tempi delle operazioni che si vogliono confrontare.
    rank_nodes = tuple(
        structure.select(rank)
        for rank in targets.rank_ranks
    )

    delete_node = structure.select(
        targets.delete_rank
    )

    search = structure.search

    total_ns, per_operation_ns = measure_batch(
        search,
        targets.present_keys,
    )

    measurements.append(
        _make_measurement(
            run=run,
            data_seed=data_seed,
            target_seed=target_seed,
            scenario=scenario,
            n=n,
            structure_name=spec.name,
            operation="search_present",
            target_type="present_key",
            batch_size=len(targets.present_keys),
            total_ns=total_ns,
            per_operation_ns=per_operation_ns,
            height_after_build=height,
            root_size_after_build=augmented_root_size,
        )
    )

    total_ns, per_operation_ns = measure_batch(
        search,
        targets.absent_keys,
    )

    measurements.append(
        _make_measurement(
            run=run,
            data_seed=data_seed,
            target_seed=target_seed,
            scenario=scenario,
            n=n,
            structure_name=spec.name,
            operation="search_absent",
            target_type="absent_key",
            batch_size=len(targets.absent_keys),
            total_ns=total_ns,
            per_operation_ns=per_operation_ns,
            height_after_build=height,
            root_size_after_build=augmented_root_size,
        )
    )

    select = structure.select

    total_ns, per_operation_ns = measure_batch(
        select,
        targets.select_ranks,
    )

    measurements.append(
        _make_measurement(
            run=run,
            data_seed=data_seed,
            target_seed=target_seed,
            scenario=scenario,
            n=n,
            structure_name=spec.name,
            operation="select",
            target_type="random_rank",
            batch_size=len(targets.select_ranks),
            total_ns=total_ns,
            per_operation_ns=per_operation_ns,
            height_after_build=height,
            root_size_after_build=augmented_root_size,
        )
    )

    rank = structure.rank

    total_ns, per_operation_ns = measure_batch(
        rank,
        rank_nodes,
    )

    measurements.append(
        _make_measurement(
            run=run,
            data_seed=data_seed,
            target_seed=target_seed,
            scenario=scenario,
            n=n,
            structure_name=spec.name,
            operation="rank",
            target_type="known_node",
            batch_size=len(rank_nodes),
            total_ns=total_ns,
            per_operation_ns=per_operation_ns,
            height_after_build=height,
            root_size_after_build=augmented_root_size,
        )
    )

    # Delete viene misurata singolarmente e per ultima: muta la struttura,
    # quindi non può essere accodata alle operazioni da confrontare.
    delete_ns, deleted = measure_single(
        structure.delete,
        delete_node,
    )

    if deleted is not True:
        raise RuntimeError(
            f"Delete fallita durante il benchmark di {spec.name}"
        )

    measurements.append(
        _make_measurement(
            run=run,
            data_seed=data_seed,
            target_seed=target_seed,
            scenario=scenario,
            n=n,
            structure_name=spec.name,
            operation="delete",
            target_type="middle_rank_known_node",
            batch_size=1,
            total_ns=delete_ns,
            per_operation_ns=float(delete_ns),
            height_after_build=height,
            root_size_after_build=augmented_root_size,
        )
    )

    return measurements


def _warm_up(
    config: BenchmarkConfig,
) -> None:
    """
    Esegue alcuni workload non registrati prima delle misure reali.
    """
    if config.warmup_runs <= 0:
        return

    n = min(config.sizes)

    for run in range(config.warmup_runs):
        data_seed = derive_seed(
            config.base_seed,
            "random_distinct",
            n,
            run,
            salt=8,
        )

        target_seed = derive_seed(
            config.base_seed,
            "random_distinct",
            n,
            run,
            salt=9,
        )

        data = generate_input(
            "random_distinct",
            n,
            data_seed,
        )

        targets = prepare_query_targets(
            data,
            config.query_batch_size,
            target_seed,
        )

        for spec in _rotated_structures(run):
            _measure_structure(
                spec=spec,
                data=data,
                targets=targets,
                run=-1,
                data_seed=data_seed,
                target_seed=target_seed,
                scenario="warmup",
            )


def run_experiment(
    config: BenchmarkConfig,
) -> list[Measurement]:
    """Esegue l'intera campagna sperimentale."""
    _warm_up(config)

    measurements: list[Measurement] = []

    for scenario in config.scenarios:
        for n in config.sizes:
            for run in range(config.repetitions):
                data_seed = derive_seed(
                    config.base_seed,
                    scenario,
                    n,
                    run,
                    salt=0,
                )

                target_seed = derive_seed(
                    config.base_seed,
                    scenario,
                    n,
                    run,
                    salt=1,
                )

                data = generate_input(
                    scenario,
                    n,
                    data_seed,
                )

                targets = prepare_query_targets(
                    data,
                    config.query_batch_size,
                    target_seed,
                )

                # Input e target identici per tutte le strutture isolano il
                # confronto dalle differenze nei dati o nelle query casuali.
                for spec in _rotated_structures(run):
                    measurements.extend(
                        _measure_structure(
                            spec=spec,
                            data=data,
                            targets=targets,
                            run=run,
                            data_seed=data_seed,
                            target_seed=target_seed,
                            scenario=scenario,
                        )
                    )

    return measurements


def execute_benchmark(
    config: BenchmarkConfig,
    mode: str,
) -> tuple[Path, Path, Path, int]:
    """
    Esegue il benchmark e salva risultati grezzi, aggregati e ambiente.
    """
    measurements = run_experiment(config)

    aggregates = aggregate_measurements(
        measurements
    )

    exercise_dir = Path(__file__).resolve().parents[1]

    raw_path = (
        exercise_dir
        / "risultati"
        / "dati_grezzi"
        / f"benchmark_{mode}.csv"
    )

    aggregate_path = (
        exercise_dir
        / "risultati"
        / "dati_aggregati"
        / f"benchmark_{mode}_aggregato.csv"
    )

    environment_path = (
        exercise_dir
        / "risultati"
        / "dati_grezzi"
        / f"ambiente_{mode}.json"
    )

    write_measurements_csv(
        measurements,
        raw_path,
    )

    write_aggregates_csv(
        aggregates,
        aggregate_path,
    )

    write_environment_json(
        environment_path,
        mode,
        config,
    )

    # I tre percorsi vengono restituiti a main.py, che li rende visibili
    # insieme al conteggio delle misure prodotte.
    return (
        raw_path,
        aggregate_path,
        environment_path,
        len(measurements),
    )
