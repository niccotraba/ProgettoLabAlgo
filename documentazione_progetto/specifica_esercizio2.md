# Specifica tecnica — Esercizio 2

## Stato

- Versione: 1.0
- Stato: congelata
- Data: 2026-08-03
- Oggetto: confronto tra selection sort e quicksort

## Fonti

- `Esercizi LabAlgo.pdf`, pagina 2.
- `Slide_ASD.pdf`, sezioni su selection sort e quicksort.
- Quicksort: pagine 164-178.

## Obiettivo

Implementare e confrontare:

1. selection sort;
2. quicksort.

Il lavoro sarà contenuto in un notebook Jupyter autosufficiente.

---

## Selection sort

Decisioni:

- implementazione iterativa;
- ordinamento in-place;
- nessun uso di funzioni Python di ordinamento nell'algoritmo;
- una versione non strumentata per i tempi;
- una versione strumentata per confronti e scambi.

---

## Quicksort

Decisioni:

- implementazione ricorsiva;
- ordinamento in-place;
- partizione di Lomuto;
- ultimo elemento del sottoarray come pivot;
- condizione di partizione coerente con lo pseudocodice del corso;
- nessuna variante randomizzata nella versione iniziale;
- una versione non strumentata per i tempi;
- una versione strumentata per confronti e scambi.

---

## Casi di input

Saranno considerate quattro categorie:

1. valori casuali distinti;
2. valori già ordinati;
3. valori ordinati in senso inverso;
4. valori casuali con molti duplicati.

Per ogni prova, entrambi gli algoritmi riceveranno copie dello stesso input iniziale.

---

## Metriche

### Tempi

Il tempo di esecuzione sarà misurato sulla versione non strumentata.

Non saranno inclusi nel timer:

- generazione dei dati;
- copia dell'array;
- verifica del risultato;
- stampa;
- produzione di grafici;
- salvataggio dei risultati.

### Confronti

Si conteranno i confronti tra valori dell'array.

### Scambi

Si conteranno gli scambi effettivi tra due posizioni distinte.

Tempi, confronti e scambi saranno analizzati separatamente.

---

## Generazione dei dati

- esecuzioni diverse devono generare dati diversi;
- ogni esecuzione deve mostrare il seed usato;
- lo stesso seed deve permettere di riprodurre una prova;
- i dati devono essere generati all'interno del notebook.

---

## Verifica di correttezza

Gli algoritmi saranno verificati su:

- array vuoto;
- array con un elemento;
- array con due elementi;
- array già ordinato;
- array inversamente ordinato;
- array con duplicati;
- array casuali.

`sorted` potrà essere usato esclusivamente come oracolo nei test, non come implementazione dell'ordinamento.

---

## Organizzazione del notebook

Il notebook deve alternare celle Markdown e celle di codice.

Struttura prevista:

1. titolo e obiettivo;
2. teoria essenziale;
3. configurazione;
4. implementazione di selection sort;
5. implementazione di quicksort;
6. test di correttezza;
7. generazione dei dati;
8. benchmark temporale;
9. misurazione di confronti e scambi;
10. grafici e tabelle;
11. analisi;
12. conclusioni.

---

## Aspetti rinviati ai task sperimentali

Non sono ancora fissati:

- dimensioni degli array;
- numero di ripetizioni;
- intervallo dei valori casuali;
- percentuale di duplicati;
- struttura finale delle tabelle;
- struttura finale dei grafici;
- eventuali limiti specifici per evitare `RecursionError`.

---

## Criteri di accettazione della specifica

La specifica è congelata quando:

- le varianti dei due algoritmi sono definite;
- la strategia del pivot è definita;
- i quattro tipi di input sono definiti;
- le tre metriche sono definite;
- la separazione tra benchmark temporale e strumentazione è definita;
- i requisiti del notebook sono definiti;
- i parametri ancora liberi sono esplicitamente rinviati.
