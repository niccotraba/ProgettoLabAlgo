import pytest

from esercizio1.strutture import (
    BinarySearchTree,
    OrderStatisticStructure,
)


def test_albero_vuoto() -> None:
    tree = BinarySearchTree()

    assert len(tree) == 0
    assert tree.root is None
    assert tree.search(10) is None

    with pytest.raises(IndexError):
        tree.select(1)


def test_inserimento_costruisce_abr_corretto() -> None:
    tree = BinarySearchTree()

    root = tree.insert(20)
    left = tree.insert(10)
    right = tree.insert(30)

    assert tree.root is root

    assert root.left is left
    assert root.right is right

    assert left.parent is root
    assert right.parent is root

    assert len(tree) == 3


def test_nodo_non_possiede_size() -> None:
    tree = BinarySearchTree()

    node = tree.insert(10)

    assert not hasattr(node, "size")


def test_inserimento_duplicati_a_destra() -> None:
    tree = BinarySearchTree()

    first = tree.insert(10)
    second = tree.insert(10)
    third = tree.insert(10)

    assert first.right is second
    assert second.right is third

    assert first is not second
    assert second is not third


def test_search() -> None:
    tree = BinarySearchTree()

    tree.insert(20)
    node_10 = tree.insert(10)
    tree.insert(30)

    assert tree.search(10) is node_10
    assert tree.search(100) is None


def test_select_restituisce_ordine_inorder() -> None:
    tree = BinarySearchTree()

    for key in (20, 10, 30, 5, 15, 25, 40):
        tree.insert(key)

    expected = [5, 10, 15, 20, 25, 30, 40]

    actual = [
        tree.select(index).key
        for index in range(1, len(tree) + 1)
    ]

    assert actual == expected


def test_select_rango_non_valido() -> None:
    tree = BinarySearchTree()

    tree.insert(10)

    with pytest.raises(IndexError):
        tree.select(0)

    with pytest.raises(IndexError):
        tree.select(2)


def test_rank_e_select_sono_coerenti() -> None:
    tree = BinarySearchTree()

    for key in (20, 10, 30, 5, 15, 25, 40):
        tree.insert(key)

    for index in range(1, len(tree) + 1):
        node = tree.select(index)

        assert tree.rank(node) == index


def test_rank_distingue_i_duplicati() -> None:
    tree = BinarySearchTree()

    first = tree.insert(10)
    second = tree.insert(10)
    third = tree.insert(10)

    assert tree.rank(first) == 1
    assert tree.rank(second) == 2
    assert tree.rank(third) == 3


def test_rank_nodo_estraneo() -> None:
    first_tree = BinarySearchTree()
    second_tree = BinarySearchTree()

    node = first_tree.insert(10)

    with pytest.raises(ValueError):
        second_tree.rank(node)


def test_delete_foglia() -> None:
    tree = BinarySearchTree()

    root = tree.insert(20)
    leaf = tree.insert(10)

    assert tree.delete(leaf) is True

    assert root.left is None
    assert leaf.owner is None
    assert len(tree) == 1


def test_delete_nodo_con_un_figlio() -> None:
    tree = BinarySearchTree()

    root = tree.insert(20)
    node = tree.insert(10)
    child = tree.insert(15)

    assert tree.delete(node) is True

    assert root.left is child
    assert child.parent is root

    assert node.owner is None
    assert len(tree) == 2


def test_delete_nodo_con_due_figli() -> None:
    tree = BinarySearchTree()

    node_20 = tree.insert(20)
    node_10 = tree.insert(10)
    tree.insert(30)
    node_25 = tree.insert(25)
    node_40 = tree.insert(40)

    assert tree.delete(node_20) is True

    # Il nodo richiesto è stato fisicamente eliminato.
    assert node_20.owner is None
    assert node_20.parent is None
    assert node_20.left is None
    assert node_20.right is None

    # Il successore 25 prende il posto della vecchia radice.
    assert tree.root is node_25
    assert node_25.left is node_10
    assert node_25.right is not None
    assert node_25.right.key == 30

    assert node_10.parent is node_25
    assert node_40.parent is node_25.right

    assert len(tree) == 4


def test_delete_radice_con_un_figlio() -> None:
    tree = BinarySearchTree()

    root = tree.insert(20)
    child = tree.insert(10)

    assert tree.delete(root) is True

    assert tree.root is child
    assert child.parent is None
    assert root.owner is None


def test_delete_unico_nodo() -> None:
    tree = BinarySearchTree()

    node = tree.insert(10)

    assert tree.delete(node) is True

    assert tree.root is None
    assert len(tree) == 0


def test_doppia_cancellazione() -> None:
    tree = BinarySearchTree()

    node = tree.insert(10)

    assert tree.delete(node) is True
    assert tree.delete(node) is False


def test_delete_nodo_di_altro_albero() -> None:
    first_tree = BinarySearchTree()
    second_tree = BinarySearchTree()

    node = first_tree.insert(10)

    assert second_tree.delete(node) is False

    assert len(first_tree) == 1
    assert len(second_tree) == 0


def test_delete_duplicato_preciso() -> None:
    tree = BinarySearchTree()

    first = tree.insert(10)
    second = tree.insert(10)
    third = tree.insert(10)

    assert tree.delete(second) is True

    assert first.owner is tree
    assert second.owner is None
    assert third.owner is tree

    assert len(tree) == 2

    assert tree.select(1) is first
    assert tree.select(2) is third


def test_inserimento_crescente_degenera_albero() -> None:
    tree = BinarySearchTree()

    nodes = [tree.insert(key) for key in range(1, 6)]

    assert tree.root is nodes[0]

    assert nodes[0].right is nodes[1]
    assert nodes[1].right is nodes[2]
    assert nodes[2].right is nodes[3]
    assert nodes[3].right is nodes[4]


def test_rispetta_protocollo_comune() -> None:
    tree = BinarySearchTree()

    assert isinstance(tree, OrderStatisticStructure)