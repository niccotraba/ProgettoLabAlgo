"""Verifica generatori deterministici, preparazione delle query e aggregazione dei benchmark."""

from esercizio1.esperimenti.benchmark import run_experiment
from esercizio1.esperimenti.configurazione import BenchmarkConfig
from esercizio1.esperimenti.generatori import (
    derive_seed,
    generate_input,
    prepare_query_targets,
)
from esercizio1.esperimenti.report import aggregate_measurements


def test_seed_riproducibile() -> None:
    """Verifica che lo stesso scenario e run producano lo stesso seed, distinti tra run diversi."""
    first = derive_seed(
        2026,
        "random_distinct",
        100,
        0,
    )

    second = derive_seed(
        2026,
        "random_distinct",
        100,
        0,
    )

    different_run = derive_seed(
        2026,
        "random_distinct",
        100,
        1,
    )

    assert first == second
    assert first != different_run


def test_generatore_random_distinct() -> None:
    """Verifica cardinalità, copertura dei valori e assenza di duplicati nello scenario casuale."""
    data = generate_input(
        "random_distinct",
        100,
        12345,
    )

    assert len(data) == 100
    assert sorted(data) == list(range(100))
    assert len(set(data)) == 100


def test_generatore_crescente() -> None:
    """Verifica che lo scenario crescente generi valori ordinati da zero a n meno uno."""
    data = generate_input(
        "increasing",
        5,
        12345,
    )

    assert data == [0, 1, 2, 3, 4]


def test_generatore_decrescente() -> None:
    """Verifica che lo scenario decrescente generi gli stessi valori in ordine inverso."""
    data = generate_input(
        "decreasing",
        5,
        12345,
    )

    assert data == [4, 3, 2, 1, 0]


def test_generatore_duplicati() -> None:
    """Verifica che lo scenario concentrato sui duplicati limiti i valori e ripeta alcune chiavi."""
    data = generate_input(
        "duplicate_heavy",
        100,
        12345,
    )

    assert len(data) == 100
    assert len(set(data)) < len(data)

    assert min(data) >= 0
    assert max(data) <= 10


def test_target_query_validi() -> None:
    """Verifica quantità e validità dei target per ricerca, select, rank e cancellazione."""
    data = [10, 20, 30, 40, 50]

    targets = prepare_query_targets(
        data,
        batch_size=10,
        seed=12345,
    )

    assert len(targets.present_keys) == 10
    assert len(targets.absent_keys) == 10
    assert len(targets.select_ranks) == 10
    assert len(targets.rank_ranks) == 10

    for key in targets.present_keys:
        assert key in data

    for key in targets.absent_keys:
        assert key not in data

    for rank in targets.select_ranks:
        assert 1 <= rank <= len(data)

    for rank in targets.rank_ranks:
        assert 1 <= rank <= len(data)

    assert 1 <= targets.delete_rank <= len(data)


def test_benchmark_minimo() -> None:
    """Verifica la pipeline minima del benchmark e il numero atteso di misurazioni prodotte."""
    config = BenchmarkConfig(
        sizes=(20,),
        repetitions=2,
        warmup_runs=0,
        query_batch_size=4,
        base_seed=2026,
        scenarios=("random_distinct",),
    )

    measurements = run_experiment(config)

    # Il conteggio atteso documenta la combinazione di run, strutture e operazioni
    # e intercetta omissioni nella pipeline sperimentale.
    # 2 run × 3 strutture × 6 misurazioni:
    # build, search_present, search_absent,
    # select, rank, delete
    assert len(measurements) == 36

    expected_operations = {
        "build",
        "search_present",
        "search_absent",
        "select",
        "rank",
        "delete",
    }

    assert {
        measurement.operation
        for measurement in measurements
    } == expected_operations

    for measurement in measurements:
        assert measurement.total_ns >= 0
        assert measurement.per_operation_ns >= 0


def test_aggregazione_benchmark() -> None:
    """Verifica che l'aggregazione produca un gruppo per struttura e operazione con statistiche coerenti."""
    config = BenchmarkConfig(
        sizes=(20,),
        repetitions=2,
        warmup_runs=0,
        query_batch_size=4,
        base_seed=2026,
        scenarios=("random_distinct",),
    )

    measurements = run_experiment(config)

    aggregates = aggregate_measurements(
        measurements
    )

    # 3 strutture × 6 operazioni
    assert len(aggregates) == 18

    for aggregate in aggregates:
        assert aggregate.samples == 2
        assert aggregate.q1_total_ns <= aggregate.q3_total_ns
        assert (
            aggregate.q1_per_operation_ns
            <= aggregate.q3_per_operation_ns
        )
