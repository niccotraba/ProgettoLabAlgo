from __future__ import annotations

from dataclasses import dataclass, field

# Nodo
@dataclass(eq=False, slots=True)
class LinkedListNode:
    """Nodo della lista ordinata doppiamente collegata."""

    key: int # chiave
    insertion_id: int
    owner: object | None = field(default=None, repr=False)

    # Puntatore logici
    prev: LinkedListNode | None = field(default=None, repr=False)
    next: LinkedListNode | None = field(default=None, repr=False)


class OrderedLinkedList:
    """Lista ordinata doppiamente collegata."""

    # Costruttore
    def __init__(self) -> None:
        self.head: LinkedListNode | None = None
        self.tail: LinkedListNode | None = None
        self._size = 0
        self._next_id = 0

    def __len__(self) -> int:
        """Restituisce il numero di nodi presenti nella lista."""
        return self._size

    def insert(self, key: int) -> LinkedListNode:
        """
        Inserisce una nuova occorrenza di key mantenendo la lista ordinata.

        Le chiavi duplicate sono ammesse e una nuova occorrenza viene
        inserita dopo le occorrenze uguali già presenti.

        Restituisce il nodo appena creato.
        """
        # Creazione nuovo nodo
        new_node = LinkedListNode(
            key=key,
            insertion_id=self._next_id,
            owner=self,
        )
        self._next_id += 1

        # Caso 1: lista vuota -> il nuvo nodo è sia head che tail della lista
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self._size = 1
            return new_node

        # Cerchiamo il primo nodo con chiave strettamente maggiore
        # I duplicati vengono inseriti dopo i duplicati già presenti
        current = self.head
        while current is not None and current.key <= key:
            current = current.next

        # Caso 2: inserimento in testa
        if current is self.head:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        # Caso 3: inserimento in coda
        elif current is None:
            assert self.tail is not None
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        # Caso 4: inserimento fra due nodi
        else:
            previous = current.prev
            assert previous is not None
            new_node.prev = previous
            new_node.next = current
            previous.next = new_node
            current.prev = new_node

        self._size += 1
        return new_node

    def search(self, key: int) -> LinkedListNode | None:
        """
        Cerca una qualsiasi occorrenza della chiave.

        Poiché la lista è ordinata, la ricerca termina appena viene
        incontrata una chiave maggiore di quella cercata.
        """
        current = self.head

        while current is not None and current.key < key:
            current = current.next

        if current is not None and current.key == key:
            return current

        return None

    def delete(self, node: LinkedListNode) -> bool:
        """
        Elimina dalla lista il nodo indicato.

        Restituisce False se il nodo non appartiene alla lista oppure
        se è già stato eliminato.
        """
        if not isinstance(node, LinkedListNode):
            return False

        if node.owner is not self:
            return False

        # Il nodo non ha predecessore: è la testa
        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next

        # Il nodo non ha successore: è la coda
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        self._size -= 1

        # Il nodo viene esplicitamente scollegato
        node.prev = None
        node.next = None
        node.owner = None

        return True

    def select(self, index: int) -> LinkedListNode:
        """
        Restituisce il nodo di rango index.

        I ranghi partono da 1:
        - select(1) restituisce il minimo;
        - select(len(self)) restituisce il massimo.
        """
        if index < 1 or index > self._size:
            raise IndexError("Rango fuori dai limiti della lista")

        current = self.head
        current_rank = 1

        while current_rank < index:
            assert current is not None

            current = current.next
            current_rank += 1

        assert current is not None
        return current

    def rank(self, node: LinkedListNode) -> int:
        """
        Restituisce il rango del nodo nella lista ordinata.

        Il confronto avviene per identità del nodo, non per chiave,
        perché chiavi duplicate possono avere ranghi differenti.
        """
        if not isinstance(node, LinkedListNode):
            raise ValueError("Il nodo non appartiene alla lista")

        if node.owner is not self:
            raise ValueError("Il nodo non appartiene alla lista")

        current = self.head
        current_rank = 1

        while current is not None:
            if current is node: # Il confronto è ffatto sul nodo e non sulla key per gestire i duplicati
                return current_rank

            current = current.next
            current_rank += 1

        # Se owner è self ma il nodo non è raggiungibile, la struttura
        # si trova in uno stato incoerente
        raise RuntimeError("Lista internamente incoerente")