"""Verifica bilanciamento AVL, statistiche d'ordine e collegamenti dei nodi."""

import pytest

from esercizio1.strutture import (
    AVLNode,
    OrderStatisticAVL,
    OrderStatisticStructure,
)


def assert_valid_avl(tree: OrderStatisticAVL) -> None:
    """
    Verifica ricorsivamente gli invarianti dell'AVL.

    Questa funzione appartiene ai test, non all'implementazione.
    """

    inorder_keys: list[int] = []

    def visit(
        node: AVLNode | None,
        expected_parent: AVLNode | None,
    ) -> tuple[int, int]:
        if node is None:
            return 0, 0

        assert node.owner is tree
        assert node.parent is expected_parent

        left_height, left_size = visit(node.left, node)

        inorder_keys.append(node.key)

        right_height, right_size = visit(node.right, node)

        expected_height = max(left_height, right_height) + 1
        expected_size = left_size + right_size + 1

        assert node.height == expected_height
        assert node.size == expected_size

        assert abs(left_height - right_height) <= 1

        return expected_height, expected_size

    _, total_size = visit(tree.root, None)

    assert total_size == len(tree)
    assert inorder_keys == sorted(inorder_keys)

    if tree.root is None:
        assert len(tree) == 0
    else:
        assert tree.root.size == len(tree)


def test_avl_vuoto() -> None:
    """Verifica lo stato iniziale e il rifiuto di select su un AVL vuoto."""
    tree = OrderStatisticAVL()

    assert tree.root is None
    assert len(tree) == 0
    assert tree.search(10) is None

    with pytest.raises(IndexError):
        tree.select(1)


def test_nodo_iniziale() -> None:
    """Verifica altezza, dimensione e posizione della radice dopo il primo inserimento."""
    tree = OrderStatisticAVL()

    node = tree.insert(10)

    assert tree.root is node
    assert node.height == 1
    assert node.size == 1
    assert node.parent is None

    assert_valid_avl(tree)


def test_rotazione_left_left() -> None:
    """Verifica il riequilibrio del caso left-left tramite rotazione a destra."""
    tree = OrderStatisticAVL()

    tree.insert(30)
    tree.insert(20)
    tree.insert(10)

    assert tree.root is not None
    assert tree.root.key == 20
    assert tree.root.left is not None
    assert tree.root.left.key == 10
    assert tree.root.right is not None
    assert tree.root.right.key == 30

    assert_valid_avl(tree)


def test_rotazione_right_right() -> None:
    """Verifica il riequilibrio del caso right-right tramite rotazione a sinistra."""
    tree = OrderStatisticAVL()

    tree.insert(10)
    tree.insert(20)
    tree.insert(30)

    assert tree.root is not None
    assert tree.root.key == 20
    assert tree.root.left is not None
    assert tree.root.left.key == 10
    assert tree.root.right is not None
    assert tree.root.right.key == 30

    assert_valid_avl(tree)


def test_rotazione_left_right() -> None:
    """Verifica il riequilibrio del caso left-right e la radice risultante."""
    tree = OrderStatisticAVL()

    tree.insert(30)
    tree.insert(10)
    tree.insert(20)

    assert tree.root is not None
    assert tree.root.key == 20

    assert_valid_avl(tree)


def test_rotazione_right_left() -> None:
    """Verifica il riequilibrio del caso right-left e la radice risultante."""
    tree = OrderStatisticAVL()

    tree.insert(10)
    tree.insert(30)
    tree.insert(20)

    assert tree.root is not None
    assert tree.root.key == 20

    assert_valid_avl(tree)


def test_size_dei_sottoalberi() -> None:
    """Verifica che size rappresenti correttamente la cardinalità di ogni sottoalbero."""
    tree = OrderStatisticAVL()

    for key in (20, 10, 30, 5, 15, 25, 40):
        tree.insert(key)

    assert tree.root is not None

    assert tree.root.size == 7
    assert tree.root.left is not None
    assert tree.root.right is not None

    assert tree.root.left.size == 3
    assert tree.root.right.size == 3

    assert_valid_avl(tree)


def test_select() -> None:
    """Verifica che select restituisca i nodi nell'ordine inorder."""
    tree = OrderStatisticAVL()

    for key in (20, 10, 30, 5, 15, 25, 40):
        tree.insert(key)

    expected = [5, 10, 15, 20, 25, 30, 40]

    actual = [
        tree.select(index).key
        for index in range(1, len(tree) + 1)
    ]

    assert actual == expected


def test_select_rango_non_valido() -> None:
    """Verifica il rifiuto degli indici fuori dall'intervallo valido di select."""
    tree = OrderStatisticAVL()

    tree.insert(10)

    with pytest.raises(IndexError):
        tree.select(0)

    with pytest.raises(IndexError):
        tree.select(2)


def test_rank_select_coerenti() -> None:
    """Verifica la coerenza reciproca tra rank e select su tutte le posizioni."""
    tree = OrderStatisticAVL()

    for key in (20, 10, 30, 5, 15, 25, 40):
        tree.insert(key)

    for index in range(1, len(tree) + 1):
        node = tree.select(index)

        assert tree.rank(node) == index


def test_duplicati_sono_nodi_distinti() -> None:
    """Verifica identità e rango distinti per nodi AVL con la stessa chiave."""
    tree = OrderStatisticAVL()

    first = tree.insert(10)
    second = tree.insert(10)
    third = tree.insert(10)

    assert first is not second
    assert second is not third

    assert tree.rank(first) == 1
    assert tree.rank(second) == 2
    assert tree.rank(third) == 3

    assert_valid_avl(tree)


def test_search() -> None:
    """Verifica la ricerca di una chiave presente e di una chiave assente."""
    tree = OrderStatisticAVL()

    tree.insert(20)
    node = tree.insert(10)
    tree.insert(30)

    assert tree.search(10) is node
    assert tree.search(100) is None


def test_delete_foglia() -> None:
    """Verifica la rimozione di una foglia mantenendo invarianti e cardinalità AVL."""
    tree = OrderStatisticAVL()

    tree.insert(20)
    node = tree.insert(10)
    tree.insert(30)

    assert tree.delete(node) is True

    assert node.owner is None
    assert len(tree) == 2

    assert_valid_avl(tree)


def test_delete_nodo_con_un_figlio() -> None:
    """Verifica la rimozione di un nodo con un figlio e il mantenimento dei collegamenti."""
    tree = OrderStatisticAVL()

    node_20 = tree.insert(20)
    node_10 = tree.insert(10)
    tree.insert(30)
    node_5 = tree.insert(5)

    assert tree.delete(node_10) is True

    assert node_10.owner is None
    assert node_5.owner is tree
    assert node_20.owner is tree

    assert_valid_avl(tree)


def test_delete_nodo_con_due_figli() -> None:
    """Verifica la rimozione di un nodo con due figli e il successivo riequilibrio."""
    tree = OrderStatisticAVL()

    node_20 = tree.insert(20)

    for key in (10, 30, 5, 15, 25, 40):
        tree.insert(key)

    assert tree.delete(node_20) is True

    assert node_20.owner is None
    assert node_20.parent is None
    assert node_20.left is None
    assert node_20.right is None

    assert len(tree) == 6

    assert_valid_avl(tree)


def test_delete_radice() -> None:
    """Verifica la rimozione della radice in un albero non banale senza violare gli invarianti."""
    tree = OrderStatisticAVL()

    root = tree.insert(20)

    for key in (10, 30, 5, 15, 25, 40):
        tree.insert(key)

    assert tree.delete(root) is True

    assert root.owner is None

    assert_valid_avl(tree)


def test_doppia_cancellazione() -> None:
    """Verifica che una seconda cancellazione dello stesso nodo non abbia effetto."""
    tree = OrderStatisticAVL()

    node = tree.insert(10)

    assert tree.delete(node) is True
    assert tree.delete(node) is False

    assert_valid_avl(tree)


def test_delete_nodo_estraneo() -> None:
    """Verifica che un AVL non possa eliminare nodi appartenenti a un altro AVL."""
    first_tree = OrderStatisticAVL()
    second_tree = OrderStatisticAVL()

    node = first_tree.insert(10)

    assert second_tree.delete(node) is False

    assert_valid_avl(first_tree)
    assert_valid_avl(second_tree)


def test_rank_nodo_estraneo() -> None:
    """Verifica che rank rifiuti un nodo appartenente a un altro AVL."""
    first_tree = OrderStatisticAVL()
    second_tree = OrderStatisticAVL()

    node = first_tree.insert(10)

    with pytest.raises(ValueError):
        second_tree.rank(node)


def test_sequenza_crescente_resta_bilanciata() -> None:
    """Verifica che molti inserimenti crescenti non producano un albero degenerato."""
    tree = OrderStatisticAVL()

    for key in range(1, 100):
        tree.insert(key)

    assert_valid_avl(tree)

    assert tree.root is not None
    assert tree.root.height < 20


def test_cancellazioni_multiple_mantengono_avl() -> None:
    """Verifica il mantenimento degli invarianti dopo una sequenza articolata di cancellazioni."""
    tree = OrderStatisticAVL()

    nodes = {
        key: tree.insert(key)
        for key in range(1, 32)
    }

    assert_valid_avl(tree)

    deletion_order = (
        16,
        8,
        24,
        4,
        12,
        20,
        28,
        1,
        31,
        15,
        17,
    )

    for key in deletion_order:
        assert tree.delete(nodes[key]) is True
        assert_valid_avl(tree)


def test_protocollo_comune() -> None:
    """Verifica che l'AVL implementi il protocollo comune delle strutture ordinate."""
    tree = OrderStatisticAVL()

    assert isinstance(tree, OrderStatisticStructure)
