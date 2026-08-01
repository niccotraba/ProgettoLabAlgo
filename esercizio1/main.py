from pathlib import Path
import csv

import matplotlib

# Permette di generare grafici anche senza interfaccia grafica.
# Sarà utile successivamente su PythonAnywhere.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "risultati" / "dati"
GRAPH_DIR = BASE_DIR / "risultati" / "grafici"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    dimensioni = [10, 20, 30, 40]
    valori = [100, 400, 900, 1600]

    csv_path = DATA_DIR / "verifica_ambiente.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["dimensione", "valore"])
        writer.writerows(zip(dimensioni, valori))

    graph_path = GRAPH_DIR / "verifica_ambiente.png"

    plt.figure()
    plt.plot(dimensioni, valori, marker="o")
    plt.xlabel("Dimensione")
    plt.ylabel("Valore")
    plt.title("Verifica ambiente di lavoro")
    plt.tight_layout()
    plt.savefig(graph_path, dpi=200)
    plt.close()

    print("Ambiente Python funzionante.")
    print(f"File CSV creato: {csv_path}")
    print(f"Grafico creato: {graph_path}")


if __name__ == "__main__":
    main()
