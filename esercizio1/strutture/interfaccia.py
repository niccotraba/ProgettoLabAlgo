from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable


@runtime_checkable
class OrderStatisticNode(Protocol):
    """Contratto minimo comune per i nodi delle strutture"""

    key: int
    insertion_id: int # Distingue nodi diversi con la stessa chiave
    owner: object | None # Controlla al'ownership del nodo

# Usiamo il protocollo per salvare il tipo concreto del nodo
NodeT = TypeVar("NodeT", bound=OrderStatisticNode)


@runtime_checkable
class OrderStatisticStructure(Protocol):
    """Interfaccia comune delle strutture per statistiche d'ordine"""

    def __len__(self) -> int:
        """Restituisce il numero di nodi presenti nella struttura"""
        ...

    def insert(self, key: int) ->NodeT:
        """Inserisce una nuova occorrenza di key e restituisce il nuovo nodo"""
        ...

    def search(self, key: int) -> NodeT | None:
        """Restituisce una qualsiasi occorrenze di key, oppure None"""
        ...

    def delete(self, node: NodeT) -> bool:
        """Elimina il nodo indicato e restituisce True se l'operazione riesce"""
        ...

    def select(self, index: int) -> NodeT:
        """
        Restituisce il nodo di rango index.
        I ranghi sono indicizzati da 1.
        Genera IndexError se index non appartiene a [1, n]
        """
        ...

    def rank(self, node: NodeT) -> int:
        """
        Restituisce il rango del nodo, indicizzato da 1.
        Genera ValueError se il nodo non appartiene alla struttura.
        """
        ...