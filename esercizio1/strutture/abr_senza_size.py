from __future__ import annotations

from dataclasses import dataclass, field

# Nodo
@dataclass(eq=False, slots=True)
class BSTNode:
    """Nodo di un albero binario di ricerca senza attributo size"""

    key: int
    insertion_id: int
    owner: object | None = field(default=None, repr=False)

    # Attributi aggiunti
    parent: BSTNode | None = field(default=None, repr=False)
    left: BSTNode | None = field(default=None, repr=False)
    right: BSTNode | None = field(default=None, repr=False)


# Struttura
class BinarySearchTree:
    """Albero binario di ricerca non bilanciato e senza size nei nodi"""

    # Costruttore
    def __init__(self) -> None:
        self.root: BSTNode | None = None
        self._size = 0
        self._next_id = 0


    def __len__(self) -> int:
        """Restituisce il numero totale di nodi presenti nell'albero."""
        return self._size

    def insert(self, key: int) -> BSTNode:
        """
        Inserisce una nuova occorrenza di key.

        Le chiavi duplicate sono ammesse e seguono il ramo destro,
        come nello pseudocodice Tree-Insert delle slide.

        Restituisce il nodo appena creato.
        """
        new_node = BSTNode(
            key=key,
            insertion_id=self._next_id,
            owner=self,
        )
        self._next_id += 1

        parent: BSTNode | None = None
        current = self.root

        # Cerca la posizione in cui inserire il nuovo nodo
        while current is not None:
            parent = current

            if key < current.key:
                current = current.left
            else:
                current = current.right

        # Colleghiamo il nuovo nodo
        new_node.parent = parent

        # L'albero era vuoto
        if parent is None:
            self.root = new_node

        # Il nuovo nodo è figlio sinistro
        elif key < parent.key:
            parent.left = new_node

        # Il nuovo nodo è figlio destro
        else:
            parent.right = new_node

        self._size += 1
        return new_node

    def search(self, key: int) -> BSTNode | None:
        """
        Cerca una qualsiasi occorrenza della chiave.

        Implementazione iterativa dello pseudocodice
        Iterative-Tree-Search visto a lezione con costo O(h).
        """
        current = self.root

        while current is not None and key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right

        return current

    def delete(self, node: BSTNode) -> bool:
        """
        Elimina esattamente il nodo indicato.

        Restituisce False se il nodo non appartiene all'albero
        oppure è già stato eliminato.
        """
        if not isinstance(node, BSTNode):
            return False

        if node.owner is not self:
            return False

        # Caso 1: nessun figlio sinistro
        # Comprende sia una foglia sia un nodo con solo figlio destro
        if node.left is None:
            self._transplant(node, node.right)

        # Caso 2: nessun figlio destro
        # Il nodo possiede quindi soltanto il figlio sinistro
        elif node.right is None:
            self._transplant(node, node.left)

        # Caso 3: il nodo possiede due figli
        else:
            successor = self._minimum(node.right)

            # Se il successore non è il figlio destro immediato,
            # prima lo rimuoviamo dalla sua posizione originaria
            if successor.parent is not node:
                self._transplant(successor, successor.right)

                successor.right = node.right

                if successor.right is not None:
                    successor.right.parent = successor

            # Il successore prende il posto di node
            self._transplant(node, successor)

            successor.left = node.left

            if successor.left is not None:
                successor.left.parent = successor

        self._size -= 1

        # Il nodo cancellato viene scollegato completamente
        node.parent = None
        node.left = None
        node.right = None
        node.owner = None

        return True

    def select(self, index: int) -> BSTNode:
        """
        Restituisce il nodo di rango index.

        I ranghi partono da 1.

        Poiché l'ABR non possiede l'attributo size nei nodi,
        dobbiamo attraversare i nodi in ordine fino alla posizione
        richiesta a partire dal minimo.
        """
        if index < 1 or index > self._size:
            raise IndexError("Rango fuori dai limiti dell'albero")

        # Recuperiamo il minimo
        current = self._minimum(self.root)

        current_rank = 1

        while current_rank < index:
            successor = self._successor(current) # Avanziamo

            if successor is None:
                raise RuntimeError("Albero internamente incoerente")

            current = successor
            current_rank += 1

        return current

    def rank(self, node: BSTNode) -> int:
        """
        Restituisce il rango del nodo nella visita inorder.

        Il rango è associato all'identità del nodo, non soltanto
        alla sua chiave. SI parte quindi dal minimo.
        """
        if not isinstance(node, BSTNode):
            raise ValueError("Il nodo non appartiene all'albero")

        if node.owner is not self:
            raise ValueError("Il nodo non appartiene all'albero")

        if self.root is None:
            raise RuntimeError("Albero internamente incoerente")

        current = self._minimum(self.root)
        current_rank = 1

        while current is not node:
            successor = self._successor(current)

            if successor is None:
                raise RuntimeError("Albero internamente incoerente")

            current = successor
            current_rank += 1

        return current_rank

    def _minimum(self, node: BSTNode | None) -> BSTNode:
        """
        Restituisce il nodo con chiave minima nel sottoalbero indicato.

        Corrisponde al nodo più a sinistra.
        """
        if node is None:
            raise ValueError("Il sottoalbero è vuoto")

        current = node

        while current.left is not None:
            current = current.left

        return current

    def _successor(self, node: BSTNode) -> BSTNode | None:
        """
        Restituisce il nodo successivo nella visita inorder.

        Due casi:
        1. se current ha un sottoalbero destro, successor è il minimo di quel sottoalbero
        2. è necessario risalire al primo antenato per il quale current appare nel sottoalbeto sinistro

        Può avere la stessa chiave del nodo corrente in presenza
        di duplicati.
        """
        # Se esiste un sottoalbero destro, il successore
        # è il suo nodo più a sinistra
        if node.right is not None:
            return self._minimum(node.right)

        # Altrimenti risaliamo finché node non appartiene
        # a un ramo sinistro
        current = node
        parent = current.parent

        while parent is not None and current is parent.right:
            current = parent
            parent = parent.parent

        return parent

    def _transplant(
        self,
        old_subtree: BSTNode,
        new_subtree: BSTNode | None,
    ) -> None:
        """
        Sostituisce il sottoalbero con radice old_subtree
        con quello avente radice new_subtree.
        """
        if old_subtree.parent is None:
            self.root = new_subtree

        elif old_subtree is old_subtree.parent.left:
            old_subtree.parent.left = new_subtree

        else:
            old_subtree.parent.right = new_subtree

        if new_subtree is not None:
            new_subtree.parent = old_subtree.parent