"""
Generazione di tabelle e grafici per i risultati del primo esercizio.

Il modulo legge i risultati aggregati prodotti dal benchmark full
e li trasforma in tabelle CSV più leggibili e grafici confrontabili
tra lista ordinata, ABR senza size e AVL aumentato.

Non esegue nuovi benchmark e non modifica i dati sperimentali originali.
"""

from __future__ import annotations

import csv

from pathlib import Path

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# COSTANTI / CONFIGURAZIONE
# ---------------------------------------------------------------------------


SCENARIOS = (
    "random_distinct",
    "increasing",
    "decreasing",
    "duplicate_heavy",
)

OPERATIONS = (
    "build",
    "search_present",
    "search_absent",
    "select",
    "rank",
    "delete",
)

STRUCTURES = (
    "ordered_list",
    "bst",
    "avl",
)

STRUCTURE_LABELS = {
    "ordered_list": "Lista ordinata",
    "bst": "ABR",
    "avl": "AVL",
}

SCENARIO_LABELS = {
    "random_distinct": "Casuale distinto",
    "increasing": "Crescente",
    "decreasing": "Decrescente",
    "duplicate_heavy": "Molti duplicati",
}

OPERATION_LABELS = {
    "build": "Costruzione",
    "search_present": "Ricerca presente",
    "search_absent": "Ricerca assente",
    "select": "Select",
    "rank": "Rank",
    "delete": "Delete",
}

# ---------------------------------------------------------------------------
# LETTURA E VALIDAZIONE DATI
# ---------------------------------------------------------------------------


def load_aggregated_results(
    path: Path,
) -> list[dict[str, str]]:
    """
    Legge il CSV aggregato prodotto dal benchmark full.

    Ogni riga viene restituita come dizionario le cui chiavi
    corrispondono ai nomi delle colonne del CSV.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"File dei risultati non trovato: {path}"
        )

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(
            csv.DictReader(file)
        )


def validate_aggregated_results(
    rows: list[dict[str, str]],
) -> None:
    """
    Verifica che il dataset full aggregato abbia la struttura attesa.

    Il benchmark completo deve contenere una riga per ogni
    combinazione di scenario, dimensione, struttura e operazione.
    """
    expected_rows = (
        len(SCENARIOS)
        * 5
        * len(STRUCTURES)
        * len(OPERATIONS)
    )

    if len(rows) != expected_rows:
        raise ValueError(
            f"Attese {expected_rows} righe aggregate, "
            f"trovate {len(rows)}"
        )

    for row in rows:
        if row["scenario"] not in SCENARIOS:
            raise ValueError(
                f"Scenario inatteso: {row['scenario']}"
            )

        if row["structure"] not in STRUCTURES:
            raise ValueError(
                f"Struttura inattesa: {row['structure']}"
            )

        if row["operation"] not in OPERATIONS:
            raise ValueError(
                f"Operazione inattesa: {row['operation']}"
            )

        if int(row["samples"]) != 30:
            raise ValueError(
                "Ogni gruppo full deve contenere 30 campioni"
            )

# ---------------------------------------------------------------------------
# GENERAZIONE TABELLE
# ---------------------------------------------------------------------------


def extract_series(
    rows: list[dict[str, str]],
    scenario: str,
    operation: str,
    structure: str,
) -> tuple[list[int], list[float]]:
    """
    Estrae le cinque mediane relative a una struttura.

    Per build viene utilizzato il tempo totale della costruzione.
    Per le altre operazioni viene utilizzato il tempo mediano
    normalizzato per singola chiamata.

    I tempi restituiti sono espressi in microsecondi.
    """
    if operation == "build":
        metric = "median_total_ns"
    else:
        metric = "median_per_operation_ns"

    selected = [
        row
        for row in rows
        if row["scenario"] == scenario
        and row["operation"] == operation
        and row["structure"] == structure
    ]

    selected.sort(
        key=lambda row: int(row["n"])
    )

    sizes = [
        int(row["n"])
        for row in selected
    ]

    times_us = [
        # I CSV registrano nanosecondi; la presentazione usa microsecondi.
        float(row[metric]) / 1_000
        for row in selected
    ]

    return sizes, times_us

def build_table_rows(
    rows: list[dict[str, str]],
    scenario: str,
    operation: str,
) -> list[dict[str, str]]:
    """
    Costruisce una tabella compatta per uno scenario e una operazione.

    La tabella finale ha una riga per ogni dimensione n e tre colonne
    principali dedicate alle tre strutture.

    Per build viene usato il tempo mediano totale.
    Per le altre operazioni viene usato il tempo mediano per chiamata.

    I tempi vengono espressi in microsecondi.
    """
    sizes_list, ordered_times = extract_series(
        rows,
        scenario=scenario,
        operation=operation,
        structure="ordered_list",
    )

    _, bst_times = extract_series(
        rows,
        scenario=scenario,
        operation=operation,
        structure="bst",
    )

    _, avl_times = extract_series(
        rows,
        scenario=scenario,
        operation=operation,
        structure="avl",
    )

    table_rows: list[dict[str, str]] = []

    for index, n in enumerate(sizes_list):
        table_rows.append(
            {
                "n": str(n),
                "lista_ordinata_us": f"{ordered_times[index]:.3f}",
                "abr_us": f"{bst_times[index]:.3f}",
                "avl_us": f"{avl_times[index]:.3f}",
            }
        )

    return table_rows

def write_table_csv(
    table_rows: list[dict[str, str]],
    path: Path,
) -> None:
    """
    Salva una tabella compatta in formato CSV.

    La cartella di destinazione viene creata automaticamente se non esiste.
    """
    if not table_rows:
        raise ValueError("La tabella da salvare è vuota")

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(table_rows[0].keys()),
        )

        writer.writeheader()

        for row in table_rows:
            writer.writerow(row)

# ---------------------------------------------------------------------------
# GENERAZIONE GRAFICI
# ---------------------------------------------------------------------------


def plot_comparison(
    rows: list[dict[str, str]],
    scenario: str,
    operation: str,
    output_path: Path,
) -> None:
    """
    Genera un grafico comparativo tra le tre strutture.

    Sull'asse X viene riportata la dimensione n.
    Sull'asse Y viene riportato il tempo mediano:
    - totale, per build;
    - per singola operazione, negli altri casi.

    Il grafico viene salvato come file PNG.
    """
    sizes, ordered_times = extract_series(
        rows,
        scenario=scenario,
        operation=operation,
        structure="ordered_list",
    )

    _, bst_times = extract_series(
        rows,
        scenario=scenario,
        operation=operation,
        structure="bst",
    )

    _, avl_times = extract_series(
        rows,
        scenario=scenario,
        operation=operation,
        structure="avl",
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(figsize=(8, 5))

    plt.plot(
        sizes,
        ordered_times,
        marker="o",
        label=STRUCTURE_LABELS["ordered_list"],
    )

    plt.plot(
        sizes,
        bst_times,
        marker="o",
        label=STRUCTURE_LABELS["bst"],
    )

    plt.plot(
        sizes,
        avl_times,
        marker="o",
        label=STRUCTURE_LABELS["avl"],
    )

    plt.xlabel("Dimensione n")

    if operation == "build":
        y_label = "Tempo mediano totale (µs)"
    else:
        y_label = "Tempo mediano per operazione (µs)"

    plt.ylabel(y_label)

    title = (
        f"{OPERATION_LABELS[operation]} — "
        f"{SCENARIO_LABELS[scenario]}"
    )
    plt.title(title)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path, dpi=200)
    plt.close()


# ---------------------------------------------------------------------------
# GENERAZIONE COMPLETA
# ---------------------------------------------------------------------------


def generate_all_tables_and_plots(
    rows: list[dict[str, str]],
    output_root: Path,
) -> tuple[int, int]:
    """
    Genera tutte le tabelle e tutti i grafici.

    Restituisce:
    - numero di tabelle generate;
    - numero di grafici generati.
    """
    tables_dir = output_root / "tabelle"
    plots_dir = output_root / "grafici"

    table_count = 0
    plot_count = 0

    for operation in OPERATIONS:
        for scenario in SCENARIOS:
            table_rows = build_table_rows(
                rows,
                scenario=scenario,
                operation=operation,
            )

            table_path = (
                tables_dir
                / f"{operation}_{scenario}.csv"
            )

            write_table_csv(
                table_rows,
                table_path,
            )
            table_count += 1

            plot_path = (
                plots_dir
                / f"{operation}_{scenario}.png"
            )

            plot_comparison(
                rows,
                scenario=scenario,
                operation=operation,
                output_path=plot_path,
            )
            plot_count += 1

    return table_count, plot_count

# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------


def main() -> None:
    """
    Punto di ingresso del modulo.

    Legge il dataset aggregato full, lo valida e genera
    tutte le tabelle e tutti i grafici utili alla relazione.
    """
    exercise_dir = Path(__file__).resolve().parents[1]

    aggregated_path = (
        exercise_dir
        / "risultati"
        / "dati_aggregati"
        / "benchmark_full_aggregato.csv"
    )

    rows = load_aggregated_results(
        aggregated_path
    )

    validate_aggregated_results(rows)

    output_root = (
        exercise_dir
        / "risultati"
    )

    table_count, plot_count = generate_all_tables_and_plots(
        rows,
        output_root,
    )

    print("Dataset aggregato validato correttamente.")
    print(f"Tabelle generate: {table_count}")
    print(f"Grafici generati: {plot_count}")
    print(f"Cartella risultati: {output_root}")


if __name__ == "__main__":
    main()
