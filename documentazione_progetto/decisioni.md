# Registro delle decisioni

## Stato

- Versione: 1.0
- Data di congelamento: 2026-08-03

---

## D01 — Strutture del primo esercizio

- Decisione:
  1. lista ordinata collegata;
  2. ABR non bilanciato senza `size`;
  3. AVL aumentato con `size`.
- Fonte: traccia del progetto e slide sulle statistiche d'ordine.
- Stato: definitiva.

## D02 — Operazioni del primo esercizio

- Decisione:
  - `insert`;
  - `search`;
  - `delete`;
  - `select`;
  - `rank`.
- Motivazione:
  - `select` e `rank` sono le operazioni caratteristiche delle statistiche d'ordine;
  - inserimento e cancellazione rendono la struttura dinamica;
  - ricerca viene implementata per completezza e utilità operativa.
- Stato: definitiva.

## D03 — Indicizzazione del rango

- Decisione: rango indicizzato da 1.
- Conseguenza:
  - il minimo ha rango 1;
  - il massimo ha rango `n`.
- Stato: definitiva.

## D04 — Gestione dei duplicati

- Decisione:
  - duplicati ammessi;
  - ogni duplicato è un nodo distinto;
  - `rank` opera sull'identità del nodo;
  - negli alberi una chiave uguale segue inizialmente il ramo destro;
  - nella lista viene inserita dopo le occorrenze uguali.
- Stato: definitiva.

## D05 — Risultato di `insert`

- Decisione: restituisce il nodo appena creato.
- Non restituisce il rango.
- Il rango può essere ottenuto successivamente con `rank(node)`.
- Stato: definitiva.

## D06 — Risultato di `delete`

- Decisione:
  - riceve il nodo preciso;
  - restituisce un booleano;
  - `True` indica cancellazione eseguita;
  - `False` indica nodo non appartenente alla struttura.
- Stato: definitiva.

## D07 — Ricorsione e iterazione

- Decisione:
  - seguire lo stile dello pseudocodice del corso;
  - quando esistono più versioni, scegliere quella più efficiente e sicura;
  - motivare le scelte nella relazione.
- Stato: definitiva.

## D08 — Variante di quicksort

- Decisione:
  - quicksort standard;
  - ricorsivo;
  - in-place;
  - partizione di Lomuto;
  - ultimo elemento come pivot.
- Stato: definitiva.

## D09 — Input del secondo esercizio

- Decisione:
  - casuale con valori distinti;
  - ordinato;
  - inversamente ordinato;
  - casuale con molti duplicati.
- Stato: definitiva.

## D10 — Metriche del secondo esercizio

- Decisione:
  - tempo di esecuzione;
  - numero di confronti;
  - numero di scambi.
- Il tempo viene misurato sulla versione non strumentata.
- Confronti e scambi vengono misurati separatamente.
- Stato: definitiva.

## D11 — Parametri sperimentali

- Decisione:
  - dimensioni;
  - ripetizioni;
  - seed;
  - aggregazioni;
  - tabelle;
  - grafici
  saranno definiti nei task sperimentali.
- Stato: rinviata deliberatamente.

## D12 — Firme Python concrete

- Decisione:
  - il comportamento logico è congelato;
  - nomi delle classi, annotazioni di tipo, classi astratte e dettagli tecnici saranno definiti nel Task 1.
- Stato: rinviata deliberatamente.
