from __future__ import annotations

from dataclasses import dataclass, field

# Nodo
@dataclass(eq=False, slots=True)
class AVLNode:
    """
    Nodo di un AVL aumentato con height e size.

    Distinzione: 
    - heght serve al bilancialmento dell'albero
    - size serve alle statistiche d'ordine
    """

    key: int
    insertion_id: int
    owner: object | None = field(default=None, repr=False)

    # Attributi aggiuntivi
    parent: AVLNode | None = field(default=None, repr=False)
    left: AVLNode | None = field(default=None, repr=False)
    right: AVLNode | None = field(default=None, repr=False)
    height: int = 1 # Una foglia appena insertia ha altezza 1
    size: int = 1 # Il sottoalbero formato soltanto dal nodo contiene un nodo


# Struttura
class OrderStatisticAVL:
    """Albero AVL aumentato per statistiche d'ordine dinamiche."""

    def __init__(self) -> None:
        self.root: AVLNode | None = None
        self._size = 0
        self._next_id = 0

    def __len__(self) -> int:
        """Restituisce il numero totale di nodi presenti nell'albero."""
        return self._size

    def insert(self, key: int) -> AVLNode:
        """
        Inserisce una nuova occorrenza di key e riequilibra l'AVL.

        Le chiavi uguali seguono inizialmente il ramo destro.
        Restituisce il nodo appena creato.
        """
        new_node = AVLNode(
            key=key,
            insertion_id=self._next_id,
            owner=self,
        )
        self._next_id += 1

        parent: AVLNode | None = None
        current = self.root

        # Inserimento normale da ABR
        while current is not None:
            parent = current

            if key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1

        # Solo gli antenati del nuovo nodo possono avere
        # height, size o bilanciamento da aggiornare
        self._rebalance_from(parent)

        return new_node

    def search(self, key: int) -> AVLNode | None:
        """Cerca una qualsiasi occorrenza della chiave."""
        current = self.root

        while current is not None and current.key != key:
            if key < current.key:
                current = current.left
            else:
                current = current.right

        return current

    def delete(self, node: AVLNode) -> bool:
        """
        Elimina esattamente il nodo indicato e ripristina l'AVL.

        Restituisce False se il nodo non appartiene all'albero
        oppure è già stato cancellato.
        """
        if not isinstance(node, AVLNode):
            return False

        if node.owner is not self:
            return False

        rebalance_start: AVLNode | None

        # Caso 1: nessun figlio sinistro
        if node.left is None:
            rebalance_start = node.parent
            self._replace_subtree(node, node.right)

        # Caso 2: nessun figlio destro
        elif node.right is None:
            rebalance_start = node.parent
            self._replace_subtree(node, node.left)

        # Caso 3: due figli
        else:
            successor = self._minimum(node.right)

            # Il successore è direttamente il figlio destro
            if successor.parent is node:
                self._replace_subtree(node, successor)

                successor.left = node.left
                successor.left.parent = successor

                rebalance_start = successor

            # Il successore si trova più in basso
            else:
                successor_old_parent = successor.parent

                assert successor_old_parent is not None

                # Rimuove il successore dalla posizione originaria
                self._replace_subtree(successor, successor.right)

                # Il vecchio sottoalbero destro di node diventa
                # sottoalbero destro del successore
                successor.right = node.right
                successor.right.parent = successor

                # Il successore prende il posto di node
                self._replace_subtree(node, successor)

                successor.left = node.left
                successor.left.parent = successor

                # Da qui parte il primo percorso modificato
                # Risalendo arriveremo anche al successore
                rebalance_start = successor_old_parent

        self._size -= 1

        # Il nodo richiesto viene fisicamente scollegato
        node.parent = None
        node.left = None
        node.right = None
        node.owner = None

        # Aggiorna size, height e bilanciamento fino alla radice
        self._rebalance_from(rebalance_start)

        return True

    def select(self, index: int) -> AVLNode:
        """
        Restituisce il nodo di rango index.

        I ranghi sono indicizzati da 1.
        Utilizza size per scegliere a ogni passo il sottoalbero corretto.
        """
        if index < 1 or index > self._size:
            raise IndexError("Rango fuori dai limiti dell'albero")

        current = self.root
        target_rank = index

        while current is not None:
            left_size = self._subtree_size(current.left)
            current_rank = left_size + 1

            if target_rank == current_rank:
                return current

            if target_rank < current_rank:
                current = current.left
            else:
                target_rank -= current_rank
                current = current.right

        raise RuntimeError("AVL internamente incoerente")

    def rank(self, node: AVLNode) -> int:
        """
        Restituisce il rango del nodo nell'ordine inorder.

        Il calcolo segue OS-Rank delle slide.
        """
        if not isinstance(node, AVLNode):
            raise ValueError("Il nodo non appartiene all'albero")

        if node.owner is not self:
            raise ValueError("Il nodo non appartiene all'albero")

        rank_value = self._subtree_size(node.left) + 1
        current = node

        while current is not self.root:
            parent = current.parent

            if parent is None:
                raise RuntimeError("AVL internamente incoerente")

            if current is parent.right:
                rank_value += self._subtree_size(parent.left) + 1

            current = parent

        return rank_value

    @staticmethod
    def _height(node: AVLNode | None) -> int:
        """
        Altezza di un sottoalbero.

        None rappresenta la foglia vuota T.nil visto a lezione.
        """
        if node is None:
            return 0

        return node.height

    @staticmethod
    def _subtree_size(node: AVLNode | None) -> int:
        """
        Numero di nodi del sottoalbero.

        None rappresenta T.nil e quindi possiede size 0.
        """
        if node is None:
            return 0

        return node.size

    def _update(self, node: AVLNode) -> None:
        """Ricalcola height e size di un nodo in O(1), poiché i 4 valori letti sono memorizzati nel nodo."""
        node.height = (
            max(
                self._height(node.left),
                self._height(node.right),
            )
            + 1
        )

        node.size = (
            self._subtree_size(node.left)
            + self._subtree_size(node.right)
            + 1
        )

    def _balance_factor(self, node: AVLNode) -> int:
        """Restituisce BF(node) = height(left) - height(right)."""
        return (
            self._height(node.left)
            - self._height(node.right)
        )

    def _left_rotate(self, node: AVLNode) -> AVLNode:
        """
        Esegue una rotazione a sinistra su node.

        Restituisce la nuova radice del sottoalbero ruotato.
        """
        new_root = node.right

        if new_root is None:
            raise ValueError(
                "Rotazione sinistra impossibile senza figlio destro"
            )

        transferred_subtree = new_root.left

        # Il sottoalbero centrale passa a destra di node
        node.right = transferred_subtree

        if transferred_subtree is not None:
            transferred_subtree.parent = node

        # new_root prende la vecchia posizione di node
        new_root.parent = node.parent

        if node.parent is None:
            self.root = new_root
        elif node is node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root

        # node diventa figlio sinistro di new_root
        new_root.left = node
        node.parent = new_root

        # Prima node, poi new_root:
        # new_root dipende dai nuovi valori di node
        self._update(node)
        self._update(new_root)

        return new_root

    def _right_rotate(self, node: AVLNode) -> AVLNode:
        """
        Esegue una rotazione a destra su node.

        Restituisce la nuova radice del sottoalbero ruotato.
        """
        new_root = node.left

        if new_root is None:
            raise ValueError(
                "Rotazione destra impossibile senza figlio sinistro"
            )

        transferred_subtree = new_root.right

        node.left = transferred_subtree

        if transferred_subtree is not None:
            transferred_subtree.parent = node

        new_root.parent = node.parent

        if node.parent is None:
            self.root = new_root
        elif node is node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root

        new_root.right = node
        node.parent = new_root

        self._update(node)
        self._update(new_root)

        return new_root

    def _rebalance_from(self, node: AVLNode | None) -> None:
        """
        Risale da node alla radice.

        A ogni livello:
        - aggiorna height;
        - aggiorna size;
        - controlla il balance factor;
        - effettua eventuali rotazioni.
        """
        current = node

        while current is not None:
            self._update(current)

            balance = self._balance_factor(current)

            # Sottoalbero sinistro troppo alto
            if balance > 1:
                left_child = current.left

                if left_child is None:
                    raise RuntimeError("AVL internamente incoerente")

                # Caso Left-Right.
                if self._balance_factor(left_child) < 0:
                    self._left_rotate(left_child)

                # Caso Left-Left, oppure seconda rotazione del Left-Right
                new_root = self._right_rotate(current)

                current = new_root.parent

            # Sottoalbero destro troppo alto
            elif balance < -1:
                right_child = current.right

                if right_child is None:
                    raise RuntimeError("AVL internamente incoerente")

                # Caso Right-Left
                if self._balance_factor(right_child) > 0:
                    self._right_rotate(right_child)

                # Caso Right-Right, oppure seconda rotazione del Right-Left
                new_root = self._left_rotate(current)

                current = new_root.parent

            else:
                current = current.parent

    def _minimum(self, node: AVLNode) -> AVLNode:
        """Restituisce il nodo minimo del sottoalbero."""
        current = node

        while current.left is not None:
            current = current.left

        return current

    def _replace_subtree(
        self,
        old_subtree: AVLNode,
        new_subtree: AVLNode | None,
    ) -> None:
        """Sostituisce old_subtree con new_subtree."""
        if old_subtree.parent is None:
            self.root = new_subtree

        elif old_subtree is old_subtree.parent.left:
            old_subtree.parent.left = new_subtree

        else:
            old_subtree.parent.right = new_subtree

        if new_subtree is not None:
            new_subtree.parent = old_subtree.parent