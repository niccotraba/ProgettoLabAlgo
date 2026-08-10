"""
Strumenti di basso livello per le misurazioni sperimentali.

Il modulo definisce il formato di una misura grezza, temporizza
costruzioni e operazioni tramite perf_counter_ns e calcola alcune
metriche strutturali, come l'altezza di ABR e AVL.
"""

from dataclasses import dataclass
from time import perf_counter_ns
from typing import Any, Callable, Sequence

from esercizio1.strutture import (
    BinarySearchTree,
    OrderedLinkedList,
    OrderStatisticAVL,
)


Structure = OrderedLinkedList | BinarySearchTree | OrderStatisticAVL


@dataclass(frozen=True)
class Measurement:
    """Una singola misura grezza."""

    run: int
    data_seed: int
    target_seed: int
    scenario: str
    n: int
    structure: str
    operation: str
    target_type: str
    batch_size: int
    total_ns: int
    per_operation_ns: float
    height_after_build: int | None
    root_size_after_build: int | None


def measure_build(
    factory: Callable[[], Structure],
    data: list[int],
) -> tuple[Structure, int]:
    """
    Costruisce una struttura e misura soltanto gli inserimenti.
    """
    structure = factory()

    insert = structure.insert

    start = perf_counter_ns()

    for key in data:
        insert(key)

    elapsed = perf_counter_ns() - start

    return structure, elapsed


def measure_batch(
    operation: Callable[[Any], Any],
    targets: Sequence[Any],
) -> tuple[int, float]:
    """
    Misura un batch di chiamate alla stessa operazione.
    """
    if not targets:
        raise ValueError("Il batch non può essere vuoto")

    start = perf_counter_ns()

    for target in targets:
        operation(target)

    elapsed = perf_counter_ns() - start

    return elapsed, elapsed / len(targets)


def measure_single(
    operation: Callable[[Any], Any],
    target: Any,
) -> tuple[int, Any]:
    """Misura una singola chiamata e restituisce anche il risultato."""
    start = perf_counter_ns()

    result = operation(target)

    elapsed = perf_counter_ns() - start

    return elapsed, result


def structure_height(
    structure: Structure,
) -> int | None:
    """
    Restituisce l'altezza della struttura dopo la costruzione.

    La lista non possiede un'altezza.
    """
    if isinstance(structure, OrderedLinkedList):
        return None

    if isinstance(structure, OrderStatisticAVL):
        if structure.root is None:
            return 0

        return structure.root.height

    if isinstance(structure, BinarySearchTree):
        if structure.root is None:
            return 0

        maximum_height = 0

        stack = [
            (structure.root, 1),
        ]

        while stack:
            node, height = stack.pop()

            maximum_height = max(
                maximum_height,
                height,
            )

            if node.left is not None:
                stack.append(
                    (node.left, height + 1)
                )

            if node.right is not None:
                stack.append(
                    (node.right, height + 1)
                )

        return maximum_height

    raise TypeError("Struttura non riconosciuta")


def root_size(
    structure: Structure,
) -> int | None:
    """Restituisce root.size soltanto per l'AVL aumentato."""
    if not isinstance(structure, OrderStatisticAVL):
        return None

    if structure.root is None:
        return 0

    return structure.root.size