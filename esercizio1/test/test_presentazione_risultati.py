"""
Test della generazione dei risultati presentabili.

I test verificano il caricamento logico e l'estrazione delle serie,
senza verificare il contenuto grafico delle immagini.
"""

from esercizio1.esperimenti.presentazione_risultati import (
    extract_series,
    build_table_rows,
    validate_aggregated_results,
)


def test_extract_series_ordina_per_dimensione() -> None:
    """Verifica ordinamento per dimensione e conversione dei nanosecondi in microsecondi."""
    rows = [
        {
            "scenario": "increasing",
            "n": "300",
            "structure": "avl",
            "operation": "select",
            "median_per_operation_ns": "3000",
            "median_total_ns": "99999",
        },
        {
            "scenario": "increasing",
            "n": "100",
            "structure": "avl",
            "operation": "select",
            "median_per_operation_ns": "1000",
            "median_total_ns": "99999",
        },
    ]

    sizes, times = extract_series(
        rows,
        scenario="increasing",
        operation="select",
        structure="avl",
    )

    assert sizes == [100, 300]

    # 1000 ns = 1 microsecondo
    # 3000 ns = 3 microsecondi
    assert times == [1.0, 3.0]


def test_build_usa_tempo_totale() -> None:
    """Verifica che l'operazione build estragga il tempo totale, non quello per operazione."""
    rows = [
        {
            "scenario": "increasing",
            "n": "100",
            "structure": "bst",
            "operation": "build",
            "median_per_operation_ns": "100",
            "median_total_ns": "5000",
        }
    ]

    sizes, times = extract_series(
        rows,
        scenario="increasing",
        operation="build",
        structure="bst",
    )

    assert sizes == [100]
    assert times == [5.0]

def test_build_table_rows_costruisce_tabella_compatta() -> None:
    """Verifica la costruzione di una riga compatta con i tempi delle tre strutture."""
    rows = [
        {
            "scenario": "increasing",
            "n": "100",
            "structure": "ordered_list",
            "operation": "select",
            "samples": "30",
            "median_total_ns": "100000",
            "q1_total_ns": "0",
            "q3_total_ns": "0",
            "iqr_total_ns": "0",
            "median_per_operation_ns": "1000",
            "q1_per_operation_ns": "0",
            "q3_per_operation_ns": "0",
            "iqr_per_operation_ns": "0",
        },
        {
            "scenario": "increasing",
            "n": "100",
            "structure": "bst",
            "operation": "select",
            "samples": "30",
            "median_total_ns": "100000",
            "q1_total_ns": "0",
            "q3_total_ns": "0",
            "iqr_total_ns": "0",
            "median_per_operation_ns": "2000",
            "q1_per_operation_ns": "0",
            "q3_per_operation_ns": "0",
            "iqr_per_operation_ns": "0",
        },
        {
            "scenario": "increasing",
            "n": "100",
            "structure": "avl",
            "operation": "select",
            "samples": "30",
            "median_total_ns": "100000",
            "q1_total_ns": "0",
            "q3_total_ns": "0",
            "iqr_total_ns": "0",
            "median_per_operation_ns": "3000",
            "q1_per_operation_ns": "0",
            "q3_per_operation_ns": "0",
            "iqr_per_operation_ns": "0",
        },
    ]

    table_rows = build_table_rows(
        rows,
        scenario="increasing",
        operation="select",
    )

    assert table_rows == [
        {
            "n": "100",
            "lista_ordinata_us": "1.000",
            "abr_us": "2.000",
            "avl_us": "3.000",
        }
    ]


def test_validate_aggregated_results_rifiuta_samples_diversi_da_30() -> None:
    """Verifica che la validazione rifiuti risultati aggregati con un numero di campioni inatteso."""
    rows = []

    for scenario in (
        "random_distinct",
        "increasing",
        "decreasing",
        "duplicate_heavy",
    ):
        for n in ("100", "300", "900", "2700", "5000"):
            for structure in ("ordered_list", "bst", "avl"):
                for operation in (
                    "build",
                    "search_present",
                    "search_absent",
                    "select",
                    "rank",
                    "delete",
                ):
                    rows.append(
                        {
                            "scenario": scenario,
                            "n": n,
                            "structure": structure,
                            "operation": operation,
                            "samples": "30",
                            "median_total_ns": "1",
                            "q1_total_ns": "1",
                            "q3_total_ns": "1",
                            "iqr_total_ns": "0",
                            "median_per_operation_ns": "1",
                            "q1_per_operation_ns": "1",
                            "q3_per_operation_ns": "1",
                            "iqr_per_operation_ns": "0",
                        }
                    )

    rows[0]["samples"] = "29"

    try:
        validate_aggregated_results(rows)
        assert False, "Attesa ValueError"
    except ValueError:
        pass
