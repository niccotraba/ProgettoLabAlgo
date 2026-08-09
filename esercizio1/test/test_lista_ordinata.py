import pytest

from esercizio1.strutture import (
    OrderStatisticStructure,
    OrderedLinkedList,
)


def test_lista_vuota() -> None:
    linked_list = OrderedLinkedList()

    assert len(linked_list) == 0
    assert linked_list.head is None
    assert linked_list.tail is None
    assert linked_list.search(10) is None

    with pytest.raises(IndexError):
        linked_list.select(1)


def test_inserimento_mantiene_ordinamento() -> None:
    linked_list = OrderedLinkedList()

    linked_list.insert(20)
    linked_list.insert(5)
    linked_list.insert(30)
    linked_list.insert(10)

    assert len(linked_list) == 4

    assert linked_list.select(1).key == 5
    assert linked_list.select(2).key == 10
    assert linked_list.select(3).key == 20
    assert linked_list.select(4).key == 30


def test_collegamenti_prev_next() -> None:
    linked_list = OrderedLinkedList()

    linked_list.insert(20)
    linked_list.insert(10)
    linked_list.insert(30)

    first = linked_list.select(1)
    second = linked_list.select(2)
    third = linked_list.select(3)

    assert linked_list.head is first
    assert linked_list.tail is third

    assert first.prev is None
    assert first.next is second

    assert second.prev is first
    assert second.next is third

    assert third.prev is second
    assert third.next is None


def test_duplicati_sono_nodi_distinti() -> None:
    linked_list = OrderedLinkedList()

    first = linked_list.insert(10)
    second = linked_list.insert(10)
    third = linked_list.insert(10)

    assert first is not second
    assert second is not third

    assert first.key == second.key == third.key == 10

    assert linked_list.rank(first) == 1
    assert linked_list.rank(second) == 2
    assert linked_list.rank(third) == 3


def test_search() -> None:
    linked_list = OrderedLinkedList()

    linked_list.insert(5)
    node_10 = linked_list.insert(10)
    linked_list.insert(20)

    assert linked_list.search(10) is node_10
    assert linked_list.search(15) is None
    assert linked_list.search(100) is None


def test_select_e_rank_sono_coerenti() -> None:
    linked_list = OrderedLinkedList()

    for key in (30, 10, 40, 20):
        linked_list.insert(key)

    for index in range(1, len(linked_list) + 1):
        node = linked_list.select(index)

        assert linked_list.rank(node) == index


def test_select_rango_non_valido() -> None:
    linked_list = OrderedLinkedList()

    linked_list.insert(10)

    with pytest.raises(IndexError):
        linked_list.select(0)

    with pytest.raises(IndexError):
        linked_list.select(2)


def test_delete_nodo_interno() -> None:
    linked_list = OrderedLinkedList()

    first = linked_list.insert(10)
    middle = linked_list.insert(20)
    last = linked_list.insert(30)

    assert linked_list.delete(middle) is True

    assert len(linked_list) == 2

    assert first.next is last
    assert last.prev is first

    assert middle.prev is None
    assert middle.next is None
    assert middle.owner is None


def test_delete_testa() -> None:
    linked_list = OrderedLinkedList()

    first = linked_list.insert(10)
    second = linked_list.insert(20)

    assert linked_list.delete(first) is True

    assert linked_list.head is second
    assert second.prev is None
    assert len(linked_list) == 1


def test_delete_coda() -> None:
    linked_list = OrderedLinkedList()

    first = linked_list.insert(10)
    second = linked_list.insert(20)

    assert linked_list.delete(second) is True

    assert linked_list.tail is first
    assert first.next is None
    assert len(linked_list) == 1


def test_delete_unico_nodo() -> None:
    linked_list = OrderedLinkedList()

    node = linked_list.insert(10)

    assert linked_list.delete(node) is True

    assert len(linked_list) == 0
    assert linked_list.head is None
    assert linked_list.tail is None


def test_doppia_cancellazione() -> None:
    linked_list = OrderedLinkedList()

    node = linked_list.insert(10)

    assert linked_list.delete(node) is True
    assert linked_list.delete(node) is False


def test_nodo_di_altra_lista_non_puo_essere_eliminato() -> None:
    first_list = OrderedLinkedList()
    second_list = OrderedLinkedList()

    node = first_list.insert(10)

    assert second_list.delete(node) is False

    assert len(first_list) == 1
    assert len(second_list) == 0


def test_rank_nodo_di_altra_lista() -> None:
    first_list = OrderedLinkedList()
    second_list = OrderedLinkedList()

    node = first_list.insert(10)

    with pytest.raises(ValueError):
        second_list.rank(node)


def test_rispetta_protocollo_comune() -> None:
    linked_list = OrderedLinkedList()

    assert isinstance(linked_list, OrderStatisticStructure)

def test_sequenza_mista_lista() -> None:
    linked_list = OrderedLinkedList()

    node_20 = linked_list.insert(20)
    linked_list.insert(10)
    node_30 = linked_list.insert(30)

    assert linked_list.delete(node_20) is True

    node_15 = linked_list.insert(15)
    linked_list.insert(25)

    assert linked_list.select(1).key == 10
    assert linked_list.select(2) is node_15
    assert linked_list.select(4) is node_30

    assert linked_list.rank(node_15) == 2
