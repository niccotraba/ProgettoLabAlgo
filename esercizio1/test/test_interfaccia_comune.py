"""Verifica a runtime i protocolli comuni per nodi e strutture di statistiche d'ordine."""

from dataclasses import dataclass

from esercizio1.strutture.interfaccia import (
    OrderStatisticNode,
    OrderStatisticStructure,
)


@dataclass
class DummyNode:
    """Nodo minimale usato per verificare il protocollo dei nodi."""

    key: int
    insertion_id: int
    owner: object | None = None


class DummyStructure:
    """Implementazione minimale del protocollo usata come doppio di test."""

    def __init__(self) -> None:
        self.nodes: list[DummyNode] = []
        self._next_id = 0

    def __len__(self) -> int:
        return len(self.nodes)

    def insert(self, key: int) -> DummyNode:
        node = DummyNode(
            key=key,
            insertion_id=self._next_id,
            owner=self,
        )
        self._next_id += 1
        self.nodes.append(node)
        return node

    def search(self, key: int) -> DummyNode | None:
        for node in self.nodes:
            if node.key == key:
                return node
        return None

    def delete(self, node: DummyNode) -> bool:
        if node.owner is not self:
            return False

        self.nodes.remove(node)
        node.owner = None
        return True

    def select(self, index: int) -> DummyNode:
        if index < 1 or index > len(self.nodes):
            raise IndexError("Rango non valido")

        ordered = sorted(self.nodes, key=lambda node: node.key)
        return ordered[index - 1]

    def rank(self, node: DummyNode) -> int:
        if node.owner is not self:
            raise ValueError("Nodo estraneo")

        ordered = sorted(self.nodes, key=lambda current: current.key)

        for index, current in enumerate(ordered, start=1):
            if current is node:
                return index

        raise ValueError("Nodo non trovato")


def test_node_protocol() -> None:
    """Verifica che un nodo minimale soddisfi il protocollo dei nodi ordinabili."""
    node = DummyNode(key=10, insertion_id=0)

    assert isinstance(node, OrderStatisticNode)


def test_structure_protocol() -> None:
    """Verifica che una struttura minimale soddisfi il protocollo comune richiesto."""
    structure = DummyStructure()

    assert isinstance(structure, OrderStatisticStructure)
