# Protocollo sperimentale — Esercizio 1

## 1. Obiettivo

L'esperimento confronta tre implementazioni di statistiche d'ordine dinamiche:

1. lista ordinata doppiamente collegata;
2. ABR non bilanciato senza attributo `size`;
3. AVL aumentato con `height` e `size`.

Il confronto ha lo scopo di valutare sperimentalmente vantaggi e svantaggi
delle tre strutture al variare:

- della dimensione dell'input;
- dell'ordine di inserimento;
- della presenza di chiavi duplicate;
- dell'operazione eseguita.

La correttezza delle implementazioni viene verificata separatamente tramite
la suite `pytest`. Il benchmark misura le prestazioni e non sostituisce i
test di correttezza.


## 2. Metrica principale

La metrica principale è il tempo di esecuzione.

Le misurazioni verranno effettuate con:

`time.perf_counter_ns()`

I tempi grezzi saranno memorizzati in nanosecondi.

Nelle tabelle e nei grafici potranno essere convertiti in microsecondi o
millisecondi quando ciò migliora la leggibilità.


## 3. Scenari di input

Per ogni dimensione vengono considerati quattro scenari.

### S1 — Chiavi distinte in ordine casuale

Vengono generate `n` chiavi distinte in ordine pseudocasuale.

Scopo:
- rappresentare un caso non costruito artificialmente per degenerare l'ABR;
- osservare il comportamento tipico delle tre strutture.

### S2 — Chiavi distinte in ordine crescente

Sequenza:

`0, 1, 2, ..., n - 1`

Scopo:
- produrre il caso degenerato destro dell'ABR;
- osservare l'effetto dell'ordine crescente sulla lista ordinata;
- verificare la capacità dell'AVL di mantenere altezza logaritmica.

### S3 — Chiavi distinte in ordine decrescente

Sequenza:

`n - 1, n - 2, ..., 0`

Scopo:
- produrre il caso degenerato sinistro dell'ABR;
- distinguere il comportamento della lista rispetto al caso crescente;
- verificare nuovamente l'indipendenza dell'AVL dall'ordine di inserimento.

### S4 — Chiavi pseudocasuali con molti duplicati

Vengono generate `n` chiavi nel range:

`[0, max(1, n // 10)]`

Scopo:
- produrre mediamente molte occorrenze per ciascuna chiave;
- verificare l'effetto dei duplicati sulle tre strutture;
- osservare in particolare l'effetto della convenzione di inserimento
  delle chiavi uguali nell'ABR.


## 4. Dimensioni

Per l'esperimento completo:

- 100
- 300
- 900
- 2700
- 5000

elementi.

Le dimensioni crescono abbastanza da permettere di osservare l'andamento
delle prestazioni senza rendere eccessivamente costosi i casi quadratici.


## 5. Ripetizioni

Per ogni combinazione:

`struttura × scenario × dimensione`

vengono effettuate:

`30 ripetizioni`

complete.

Prima delle misurazioni definitive vengono effettuati alcuni run di
riscaldamento non salvati nei risultati.

Numero iniziale previsto:

`3 warm-up run`

I warm-up servono esclusivamente a ridurre l'influenza dell'avvio del
programma e non vengono utilizzati nell'analisi statistica.


## 6. Riproducibilità dei dati casuali

Viene utilizzato un seed base fisso.

`BASE_SEED = 2026`

Per ogni scenario, dimensione e ripetizione viene ricavato un seed
deterministico differente.

All'interno dello stesso run, lista, ABR e AVL ricevono esattamente la
stessa sequenza di chiavi.

In questo modo:

- le tre strutture vengono confrontate sugli stessi dati;
- run diversi possono utilizzare dati casuali differenti;
- qualsiasi esperimento può essere riprodotto conoscendo il seed.


## 7. Operazioni misurate

### 7.1 Costruzione tramite inserimenti

La struttura viene creata vuota prima del timer.

Viene misurato il tempo necessario a eseguire gli `n` inserimenti della
sequenza di test.

Non vengono inclusi:

- generazione dei dati;
- creazione della sequenza Python;
- salvataggio dei risultati;
- validazione della struttura;
- stampa.

Il risultato rappresenta un workload di `n` operazioni `insert`.

Vengono registrati:

- tempo totale di costruzione;
- tempo medio per inserimento, ottenuto dividendo il tempo totale per `n`.


### 7.2 Search — chiave presente

Sulla struttura già costruita vengono preparate chiavi sicuramente presenti.

Le chiavi da cercare vengono selezionate utilizzando posizioni distribuite
nell'insieme ordinato.

La preparazione delle chiavi avviene prima del timer.

All'interno di ciascun run vengono effettuate più ricerche e viene
registrato il tempo medio per chiamata.


### 7.3 Search — chiave assente

Vengono preparate chiavi sicuramente non presenti.

Il workload contiene valori sia inferiori al minimo sia superiori al
massimo, per evitare di favorire sistematicamente una sola direzione
dell'albero.

La preparazione avviene fuori dal timer.


### 7.4 Select

Vengono preparati ranghi validi distribuiti uniformemente nell'intervallo:

`[1, n]`

I ranghi vengono generati prima della misura.

Viene misurato esclusivamente:

`structure.select(index)`


### 7.5 Rank

Prima della misura vengono individuati i nodi corrispondenti ai ranghi
preparati per `select`.

La ricerca dei nodi target non viene inclusa nel tempo.

Viene misurato esclusivamente:

`structure.rank(node)`


### 7.6 Delete

Viene scelto un nodo circa in posizione centrale nell'ordinamento.

Il nodo viene individuato prima dell'avvio del timer.

Viene misurato esclusivamente:

`structure.delete(node)`

La cancellazione viene eseguita come ultima operazione mutante del run.

La misura rappresenta quindi la cancellazione quando il riferimento al
nodo è già noto.

La cancellazione a partire da una chiave viene interpretata separatamente
come:

`search(key) + delete(node)`

e non viene mescolata alla misura di `delete(node)`.


## 8. Batch delle operazioni non mutanti

Le operazioni:

- `search`;
- `select`;
- `rank`;

sono molto rapide e una singola chiamata può essere influenzata
significativamente dal rumore della misura.

Per ogni run viene quindi eseguito un batch di:

`20 operazioni`

dello stesso tipo.

Si misura il tempo totale del batch e si calcola:

`tempo_batch / 20`

ottenendo il tempo medio per operazione di quel run.

Le operazioni mutanti, in particolare `delete`, non vengono ripetute sullo
stesso oggetto perché modificherebbero progressivamente la struttura.


## 9. Ordine di esecuzione delle strutture

Per evitare che una struttura venga sempre misurata per prima o per ultima,
l'ordine viene ruotato tra i run.

Esempio:

- run 0: Lista, ABR, AVL;
- run 1: ABR, AVL, Lista;
- run 2: AVL, Lista, ABR;
- run 3: Lista, ABR, AVL;
- ...

Questo riduce un possibile bias dovuto all'ordine temporale delle misure.


## 10. Parti escluse dalle misure

Non devono essere incluse nel timer:

- generazione dei dati;
- generazione dei seed;
- preparazione dei target;
- ricerca del nodo necessario a `rank` o `delete`;
- verifiche di correttezza;
- `pytest`;
- validatori degli invarianti;
- conversione dei risultati;
- scrittura dei CSV;
- generazione di grafici;
- stampa su terminale.

Il timer deve circondare soltanto l'operazione o il workload che si vuole
misurare.


## 11. Metriche strutturali secondarie

Oltre ai tempi vengono registrate, dove applicabili, alcune informazioni
utili a interpretare i risultati.

Per ABR:

- altezza dopo la costruzione.

Per AVL:

- altezza dopo la costruzione;
- `root.size`, utilizzabile come controllo del numero totale dei nodi.

L'altezza non viene utilizzata come metrica prestazionale principale ma
serve a spiegare eventuali differenze temporali tra ABR e AVL.


## 12. Aggregazione statistica

Tutti i risultati grezzi vengono conservati.

Per ogni combinazione di:

`struttura × scenario × dimensione × operazione`

si calcolano almeno:

- numero di campioni;
- mediana;
- primo quartile Q1;
- terzo quartile Q3;
- intervallo interquartile IQR = Q3 - Q1.

La mediana viene utilizzata come valore rappresentativo principale perché
è meno sensibile a misurazioni temporali anomale rispetto alla media.


## 13. Risultati grezzi

Il CSV dei risultati grezzi dovrà permettere di ricostruire ogni misura.

Campi previsti:

- run;
- seed;
- scenario;
- n;
- struttura;
- operazione;
- target o tipo di target;
- numero di operazioni nel batch;
- tempo totale in nanosecondi;
- tempo per operazione in nanosecondi;
- altezza della struttura, quando applicabile.


## 14. Risultati aggregati

Un secondo CSV conterrà almeno:

- scenario;
- n;
- struttura;
- operazione;
- numero di campioni;
- mediana;
- Q1;
- Q3;
- IQR.


## 15. Grafici

I grafici principali utilizzeranno:

- asse X: dimensione `n`;
- asse Y: tempo;
- una serie distinta per Lista, ABR e AVL.

Gli esperimenti relativi a scenari e operazioni differenti saranno
separati per evitare grafici eccessivamente affollati.

La selezione definitiva dei grafici da inserire nella relazione avverrà
dopo aver osservato i risultati.


## 16. Piattaforma

I risultati sperimentali definitivi devono essere raccolti sulla stessa
piattaforma.

Verranno registrati almeno:

- sistema operativo;
- versione di Python;
- processore;
- informazioni hardware disponibili;
- modalità di esecuzione del programma.

Durante gli esperimenti definitivi si eviteranno, per quanto possibile,
carichi di lavoro pesanti estranei al benchmark.


## 17. Modalità quick e full

Il programma di benchmark prevederà due configurazioni.

### Quick

Utilizzata per sviluppo e verifica:

- dimensioni: 100, 300;
- ripetizioni: 3;
- batch query ridotto.

### Full

Utilizzata per produrre i risultati della relazione:

- dimensioni: 100, 300, 900, 2700, 5000;
- ripetizioni: 30;
- 20 operazioni per batch non mutante.

La modalità quick non viene utilizzata per trarre conclusioni sperimentali.


## 18. PythonAnywhere

PythonAnywhere verrà utilizzato per verificare che il programma possa
essere eseguito correttamente da riga di comando.

A causa delle risorse limitate dell'account free potrà essere utilizzata
la modalità quick.

I risultati sperimentali di riferimento saranno ottenuti sulla piattaforma
locale documentata nella relazione.


## 19. Criterio di correttezza prima del benchmark

Prima dell'esecuzione degli esperimenti definitivi deve passare:

`python -m pytest`

I validatori e i test non vengono eseguiti all'interno delle regioni
temporizzate.

---
# Protocollo sperimentale esercizio 2

## Scenari
- scenari:
  1. valori distinti casuali;
  2. valori distinti ordinati in modo crescente;
  3. valori distinti ordinati in modo decrescente;
  4. valori casuali con circa il 35% di occorrenze duplicate;

## Generazione e seed
- Ogni esecuzione utilizza un **seed casuale registrato**. La funzione `generate_seed()` genera un nuovo valore di seed e, a partire da esso, inizializza un oggetto `Random` (`rng`) utilizzato successivamente per la generazione dei dati.
- il seed viene generato e registrato prima della generazione degli
  input sperimentali;

## Dimensioni e ripetizioni
- dimensioni: `50, 100, 200, 400, 800`;
- ripetizioni: `30` per ogni combinazione scenario-dimensione;
- per ogni ripetizione vengono generati nuovi dati;
- Selection Sort e Quick Sort ricevono copie dello stesso input
  iniziale nella stessa ripetizione;
- l'ordine di esecuzione di Selection Sort e Quick Sort viene
  alternato tra le ripetizioni;

## Benchmark temporale
- timer: `time.perf_counter_ns()`;
- la regione temporizzata comprende esclusivamente la chiamata
  all'algoritmo di ordinamento;
- i risultati temporali grezzi vengono conservati in nanosecondi
  e rappresentati in microsecondi;

## Confronti e scambi

## Aggregazione dei risultati
- aggregazione tramite mediana e IQR;
- la mediana è il valore temporale principale;

## Limite di ricorsione

## Ambiente di esecuzione
- il limite di ricorsione di Python non viene modificato;
- viene mantenuto un margine di sicurezza di `100` rispetto al
  limite di ricorsione rilevato nell'ambiente.