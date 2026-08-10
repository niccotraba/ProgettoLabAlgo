"""
Generazione degli input e dei target utilizzati negli esperimenti.

Il modulo produce sequenze di inserimento riproducibili per i diversi
scenari e prepara, prima delle misurazioni, chiavi e ranghi utilizzati
da search, select, rank e delete.
"""

from dataclasses import dataclass
from random import Random

from .configurazione import Scenario


@dataclass(frozen=True)
class QueryTargets:
    """Target preparati prima delle misurazioni."""

    present_keys: tuple[int, ...]
    absent_keys: tuple[int, ...]
    select_ranks: tuple[int, ...]
    rank_ranks: tuple[int, ...]
    delete_rank: int


_SCENARIO_CODES: dict[Scenario, int] = {
    "random_distinct": 1,
    "increasing": 2,
    "decreasing": 3,
    "duplicate_heavy": 4,
}


def derive_seed(
    base_seed: int,
    scenario: Scenario,
    n: int,
    run: int,
    salt: int = 0,
) -> int:
    """
    Costruisce un seed deterministico.

    Configurazioni differenti producono seed differenti.
    """
    scenario_code = _SCENARIO_CODES[scenario]

    return (
        (
            (
                (base_seed * 10 + scenario_code)
                * 100_000
                + n
            )
            * 1_000
            + run
        )
        * 10
        + salt
    )


def generate_input(
    scenario: Scenario,
    n: int,
    seed: int,
) -> list[int]:
    """Genera la sequenza di inserimento richiesta dallo scenario."""
    if n <= 0:
        raise ValueError("n deve essere positivo")

    rng = Random(seed)

    if scenario == "random_distinct":
        values = list(range(n))
        rng.shuffle(values)
        return values

    if scenario == "increasing":
        return list(range(n))

    if scenario == "decreasing":
        return list(range(n - 1, -1, -1))

    if scenario == "duplicate_heavy":
        max_key = max(1, n // 10)

        return [
            rng.randint(0, max_key)
            for _ in range(n)
        ]

    raise ValueError(f"Scenario non riconosciuto: {scenario}")


def prepare_query_targets(
    data: list[int],
    batch_size: int,
    seed: int,
) -> QueryTargets:
    """
    Prepara tutti i target prima dell'avvio dei timer.

    Le stesse posizioni e chiavi potranno quindi essere utilizzate
    sulle tre strutture.
    """
    if not data:
        raise ValueError("I dati non possono essere vuoti")

    if batch_size <= 0:
        raise ValueError("batch_size deve essere positivo")

    rng = Random(seed)

    ordered = sorted(data)
    n = len(ordered)

    present_keys = tuple(
        ordered[rng.randrange(n)]
        for _ in range(batch_size)
    )

    select_ranks = tuple(
        rng.randint(1, n)
        for _ in range(batch_size)
    )

    rank_ranks = tuple(
        rng.randint(1, n)
        for _ in range(batch_size)
    )

    minimum = ordered[0]
    maximum = ordered[-1]

    absent_keys: list[int] = []

    for index in range(batch_size):
        offset = index // 2 + 1

        if index % 2 == 0:
            absent_keys.append(minimum - offset)
        else:
            absent_keys.append(maximum + offset)

    return QueryTargets(
        present_keys=present_keys,
        absent_keys=tuple(absent_keys),
        select_ranks=select_ranks,
        rank_ranks=rank_ranks,
        delete_rank=(n + 1) // 2,
    )