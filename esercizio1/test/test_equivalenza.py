"""
Script che verifica l'equivalenza delle tre strutture.

Il test non è volto a verifificare il corretto funzionamento interno delle singole strutture,
ma, al contrario, di verificare che tutte e tre abbiano lo stesso contenuto logico dopo le stesse
operazioni, indipendentemente dalla struttura/forma interna.

- vengono utilizzate esclusivamente operazioni del contratto comune (test funzionale black-box)
- vengono usate sia key che insertion_id per la gestione dei duplicati
- insertion_id è utilizzato per verificare che le tre strutture siano sincronizzate sulla stessa inserzione logica
"""
from random import Random

from esercizio1.strutture import (
    AVLNode,
    BSTNode,
    BinarySearchTree,
    LinkedListNode,
    OrderedLinkedList,
    OrderStatisticAVL,
)


Structure = OrderedLinkedList | BinarySearchTree | OrderStatisticAVL

# Rappresenta la stessa inserzione logica sulle tre differenti strutture
NodeTriple = tuple[
    LinkedListNode,
    BSTNode,
    AVLNode,
]


def _create_structures() -> tuple[
    OrderedLinkedList,
    BinarySearchTree,
    OrderStatisticAVL,
]:
    """Crea le tre strutture vuote da confrontare."""
    return (
        OrderedLinkedList(),
        BinarySearchTree(),
        OrderStatisticAVL(),
    )


def _ordered_signature(
    structure: Structure,
) -> list[tuple[int, int]]:
    """
    Restituisce il contenuto logico della struttura in ordine.

    Ogni nodo viene rappresentato dalla coppia:
        (key, insertion_id)

    insertion_id permette di distinguere nodi diversi con la stessa chiave.
    """
    result: list[tuple[int, int]] = []

    for index in range(1, len(structure) + 1):
        node = structure.select(index)

        result.append(
            (node.key, node.insertion_id)
        )

    return result


def _insert_all(
    linked_list: OrderedLinkedList,
    bst: BinarySearchTree,
    avl: OrderStatisticAVL,
    key: int,
) -> NodeTriple:
    """
    Inserisce la stessa chiave nelle tre strutture.

    Restituisce i tre nodi che rappresentano la stessa
    inserzione logica.
    """
    list_node = linked_list.insert(key)
    bst_node = bst.insert(key)
    avl_node = avl.insert(key)

    # Poiché eseguiamo esattamente le stesse inserzioni nello stesso
    # ordine, gli insertion_id devono coincidere.
    assert (
        list_node.insertion_id
        == bst_node.insertion_id
        == avl_node.insertion_id
    )

    return list_node, bst_node, avl_node


def _delete_all(
    linked_list: OrderedLinkedList,
    bst: BinarySearchTree,
    avl: OrderStatisticAVL,
    nodes: NodeTriple,
) -> None:
    """Elimina la stessa occorrenza logica dalle tre strutture."""
    list_node, bst_node, avl_node = nodes

    assert linked_list.delete(list_node) is True
    assert bst.delete(bst_node) is True
    assert avl.delete(avl_node) is True


def _assert_equivalent(
    linked_list: OrderedLinkedList,
    bst: BinarySearchTree,
    avl: OrderStatisticAVL,
) -> None:
    """Verifica cardinalità, ordine, contenuto e identità dei duplicati nelle tre strutture."""
    assert len(linked_list) == len(bst) == len(avl)

    list_signature = _ordered_signature(linked_list)
    bst_signature = _ordered_signature(bst)
    avl_signature = _ordered_signature(avl)

    assert bst_signature == list_signature
    assert avl_signature == list_signature

    # Verifica anche la proprietà rank(select(i)) == i
    # nelle tre strutture.
    for index in range(1, len(linked_list) + 1):
        list_node = linked_list.select(index)
        bst_node = bst.select(index)
        avl_node = avl.select(index)

        assert linked_list.rank(list_node) == index
        assert bst.rank(bst_node) == index
        assert avl.rank(avl_node) == index


def test_sequenza_deterministica_equivalente() -> None:
    """Verifica l'equivalenza su una sequenza fissa che include duplicati e cancellazioni mirate."""
    linked_list, bst, avl = _create_structures()

    node_refs: dict[int, NodeTriple] = {}

    values = (
        20,
        10,
        30,
        10,
        25,
        5,
        30,
        15,
    )

    # Stesse inserzioni, stesso ordine.
    for key in values:
        nodes = _insert_all(
            linked_list,
            bst,
            avl,
            key,
        )

        logical_id = nodes[0].insertion_id
        node_refs[logical_id] = nodes

        _assert_equivalent(
            linked_list,
            bst,
            avl,
        )

    # Gli insertion_id corrispondono all'ordine di inserimento:
    #
    # id 0 -> 20
    # id 1 -> 10
    # id 2 -> 30
    # id 3 -> 10
    # id 4 -> 25
    # id 5 -> 5
    # id 6 -> 30
    # id 7 -> 15
    #
    # Quindi l'ordine atteso è:
    expected = [
        (5, 5),
        (10, 1),
        (10, 3),
        (15, 7),
        (20, 0),
        (25, 4),
        (30, 2),
        (30, 6),
    ]

    assert _ordered_signature(linked_list) == expected
    assert _ordered_signature(bst) == expected
    assert _ordered_signature(avl) == expected

    # Search può restituire una qualsiasi occorrenza quando
    # esistono duplicati. Non confrontiamo quindi insertion_id.
    for key in (5, 10, 20, 25, 30):
        for structure in (linked_list, bst, avl):
            node = structure.search(key)

            assert node is not None
            assert node.key == key

    # Chiavi assenti.
    for key in (-1, 12, 100):
        assert linked_list.search(key) is None
        assert bst.search(key) is None
        assert avl.search(key) is None

    # Verifica il rank delle stesse occorrenze logiche.
    for expected_rank, (_, logical_id) in enumerate(
        expected,
        start=1,
    ):
        list_node, bst_node, avl_node = node_refs[logical_id]

        assert linked_list.rank(list_node) == expected_rank
        assert bst.rank(bst_node) == expected_rank
        assert avl.rank(avl_node) == expected_rank

    # Eliminiamo precisamente il secondo 10, cioè insertion_id 3.
    _delete_all(
        linked_list,
        bst,
        avl,
        node_refs[3],
    )

    _assert_equivalent(
        linked_list,
        bst,
        avl,
    )

    assert _ordered_signature(linked_list) == [
        (5, 5),
        (10, 1),
        (15, 7),
        (20, 0),
        (25, 4),
        (30, 2),
        (30, 6),
    ]

    # Eliminiamo anche il nodo originariamente inserito con chiave 20.
    _delete_all(
        linked_list,
        bst,
        avl,
        node_refs[0],
    )

    _assert_equivalent(
        linked_list,
        bst,
        avl,
    )

    # Inseriamo ancora un duplicato dopo alcune cancellazioni.
    new_nodes = _insert_all(
        linked_list,
        bst,
        avl,
        10,
    )

    node_refs[new_nodes[0].insertion_id] = new_nodes

    _assert_equivalent(
        linked_list,
        bst,
        avl,
    )


def test_sequenza_pseudocasuale_equivalente() -> None:
    """
    Esegue una sequenza riproducibile di inserimenti e cancellazioni.

    Una lista Python viene usata soltanto come oracle del test,
    non come implementazione della struttura richiesta dall'esercizio.
    Il confronto con un oracle indipendente evita che il test passi se
    le tre strutture condividono lo stesso errore.
    """
    linked_list, bst, avl = _create_structures()

    # Il seed fisso rende riproducibile la sequenza e quindi facilita
    # l'analisi di eventuali divergenze tra le implementazioni.
    rng = Random(123456)

    active_nodes: dict[int, NodeTriple] = {}

    # Oracle:
    # (key, insertion_id) dei nodi attualmente presenti.
    expected: list[tuple[int, int]] = []

    for _ in range(200):

        # Se non ci sono nodi dobbiamo inserire.
        # Altrimenti inseriamo circa nel 65% dei casi.
        should_insert = (
            not active_nodes
            or rng.random() < 0.65
        )

        if should_insert:
            # Range piccolo intenzionalmente:
            # vogliamo generare parecchi duplicati.
            key = rng.randint(0, 20)

            nodes = _insert_all(
                linked_list,
                bst,
                avl,
                key,
            )

            logical_id = nodes[0].insertion_id

            active_nodes[logical_id] = nodes

            expected.append(
                (key, logical_id)
            )

            expected.sort()

        else:
            # Seleziona una specifica occorrenza logica da eliminare.
            logical_id = rng.choice(
                list(active_nodes)
            )

            nodes = active_nodes.pop(logical_id)

            _delete_all(
                linked_list,
                bst,
                avl,
                nodes,
            )

            expected = [
                item
                for item in expected
                if item[1] != logical_id
            ]

        # Dopo OGNI modifica le tre strutture devono avere
        # lo stesso contenuto ordinato.
        assert _ordered_signature(linked_list) == expected
        assert _ordered_signature(bst) == expected
        assert _ordered_signature(avl) == expected

        assert len(linked_list) == len(expected)
        assert len(bst) == len(expected)
        assert len(avl) == len(expected)

        # Test Search su una chiave casuale.
        searched_key = rng.randint(0, 20)

        expected_presence = any(
            key == searched_key
            for key, _ in expected
        )

        for structure in (linked_list, bst, avl):
            found = structure.search(searched_key)

            assert (found is not None) == expected_presence

            if found is not None:
                assert found.key == searched_key

        # Se la struttura non è vuota controlliamo anche
        # select e rank su una posizione casuale.
        if expected:
            index = rng.randint(
                1,
                len(expected),
            )

            expected_key, logical_id = expected[index - 1]

            list_selected = linked_list.select(index)
            bst_selected = bst.select(index)
            avl_selected = avl.select(index)

            assert (
                list_selected.key,
                list_selected.insertion_id,
            ) == (
                expected_key,
                logical_id,
            )

            assert (
                bst_selected.key,
                bst_selected.insertion_id,
            ) == (
                expected_key,
                logical_id,
            )

            assert (
                avl_selected.key,
                avl_selected.insertion_id,
            ) == (
                expected_key,
                logical_id,
            )

            list_node, bst_node, avl_node = active_nodes[logical_id]

            assert linked_list.rank(list_node) == index
            assert bst.rank(bst_node) == index
            assert avl.rank(avl_node) == index
