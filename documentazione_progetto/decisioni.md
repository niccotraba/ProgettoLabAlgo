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

- Decisione: i parametri sperimentali sono definiti nel protocollo
  sperimentale del primo esercizio.
- Parametri principali:
  - dimensioni: `100, 300, 900, 2700, 5000`;
  - ripetizioni: `30`;
  - seed base: `2026`;
  - aggregazione tramite mediana, Q1, Q3 e IQR.
- Riferimento: D29.
- Stato: definitiva.

## D12 — Firme Python concrete

- Decisione: le firme Python concrete sono state definite tramite
  l'interfaccia comune descritta in D13.
- Stato: definitiva.


## D13 — Interfaccia comune Python

- Decisione: utilizzare `typing.Protocol`.
- Motivazione: lista ordinata, ABR e AVL possono soddisfare lo stesso contratto senza condividere una gerarchia di ereditarietà.
- Operazioni pubbliche comuni:
  - `__len__`
  - `insert`
  - `search`
  - `delete`
  - `select`
  - `rank`
- I nodi condividono logicamente:
  - `key`
  - `insertion_id`
  - `owner`
- `validate`, visite, rotazioni e altri metodi ausiliari non fanno parte dell'interfaccia pubblica comune.
- Stato: definitiva.


## D14 — Rappresentazione della lista ordinata

- Decisione:
  - lista doppiamente collegata;
  - non circolare;
  - senza sentinella;
  - riferimenti espliciti `head` e `tail`;
  - ogni nodo contiene `key`, `insertion_id`, `owner`, `prev` e `next`;
  - la lista mantiene `_size` come numero totale di nodi.
- La lista Python non viene utilizzata come struttura di memorizzazione interna.
- Motivazione:
  - aderire al vincolo della traccia che richiede strutture collegate tramite puntatori;
  - rendere la cancellazione di un nodo già noto eseguibile tramite aggiornamento locale dei puntatori.
- Stato: definitiva.

## D15 — Inserimento e duplicati nella lista ordinata

- Decisione:
  - `insert` mantiene sempre le chiavi in ordine non decrescente;
  - ogni inserimento crea un nodo distinto;
  - le chiavi duplicate sono ammesse;
  - una nuova occorrenza viene inserita dopo le occorrenze uguali già presenti.
- Conseguenza:
  - nodi con la stessa chiave possono avere ranghi differenti;
  - l'identità del nodo viene mantenuta tramite il riferimento all'oggetto e `insertion_id`.
- Stato: definitiva.

## D16 — Cancellazione nella lista ordinata

- Decisione:
  - `delete` riceve il riferimento al nodo preciso da eliminare;
  - non riceve direttamente una chiave;
  - il nodo viene scollegato aggiornando `prev`, `next`, `head` e `tail` quando necessario;
  - dopo la cancellazione `prev`, `next` e `owner` del nodo vengono impostati a `None`;
  - `delete` restituisce `False` se il nodo non appartiene alla lista o è già stato eliminato.
- Motivazione:
  - eliminare senza ambiguità una specifica occorrenza in presenza di chiavi duplicate;
  - mantenere coerenza con `rank(node)` e con l'interfaccia comune;
  - distinguere il costo della ricerca del nodo dal costo strutturale della sua rimozione.
- Complessità:
  - se il riferimento al nodo è già noto, `delete(node)` richiede `Theta(1)` perché modifica soltanto un numero costante di puntatori;
  - se l'operazione parte da una chiave, bisogna prima eseguire `search(key)`, che costa `O(n)`;
  - quindi `search(key) + delete(node)` ha costo complessivo `O(n)`.
- Nota:
  - questo chiarisce perché la cancellazione di una lista ordinata viene generalmente indicata come `O(n)` quando l'elemento deve prima essere individuato.
- Stato: definitiva.

## D17 — `select` e `rank` nella lista ordinata

- Decisione:
  - `select(i)` percorre la lista a partire da `head` fino alla posizione richiesta;
  - `rank(node)` percorre la lista da `head` fino a incontrare lo stesso oggetto nodo;
  - il confronto usato da `rank` è per identità (`is`) e non per uguaglianza della chiave;
  - i ranghi sono indicizzati da 1.
- Conseguenza:
  - `select` ha complessità `O(n)` nel caso peggiore;
  - `rank` ha complessità `O(n)` nel caso peggiore.
- Motivazione:
  - la lista non memorizza informazioni aggiuntive di rango;
  - nodi distinti con la stessa chiave devono poter avere ranghi diversi.
- Stato: definitiva.


## D18 — Rappresentazione dell'ABR senza `size`

- Decisione:
  - l'ABR è non bilanciato;
  - i figli assenti sono rappresentati con `None`;
  - non viene utilizzata una sentinella `NIL`;
  - ogni nodo contiene `key`, `insertion_id`, `owner`, `parent`, `left` e `right`;
  - i nodi non contengono l'attributo `size`.
- L'albero mantiene `_size` soltanto come numero totale di nodi, per supportare `len(tree)`.
- `_size` appartiene all'oggetto albero e non rappresenta la dimensione dei sottoalberi, quindi non costituisce l'attributo `size` escluso dalla traccia.
- Stato: definitiva.

## D19 — Inserimento e duplicati nell'ABR

- Decisione:
  - `insert` segue lo schema iterativo di `Tree-Insert`;
  - se la nuova chiave è strettamente minore si procede a sinistra;
  - in caso contrario si procede a destra;
  - quindi le chiavi duplicate seguono inizialmente il ramo destro;
  - ogni inserimento crea un nodo distinto.
- Motivazione: aderire allo pseudocodice base presentato nelle slide e mantenere una gestione dei duplicati coerente con la specifica del progetto.
- Stato: definitiva.

## D20 — Cancellazione per identità del nodo

- Decisione:
  - `delete` riceve il riferimento al nodo preciso da eliminare;
  - non riceve direttamente una chiave;
  - il nodo richiesto viene fisicamente rimosso dalla struttura;
  - dopo la cancellazione `owner`, `parent`, `left` e `right` del nodo rimosso vengono azzerati;
  - `delete` restituisce `False` per un nodo estraneo o già eliminato.
- Nel caso di nodo con due figli, il successore viene spostato strutturalmente nella posizione del nodo eliminato invece di copiare soltanto la sua chiave.
- Motivazione:
  - preservare l'identità dei nodi;
  - gestire correttamente le chiavi duplicate;
  - mantenere coerenti `rank(node)` e la semantica dell'interfaccia comune.
- Nota di complessità:
  - `delete(node)` misura la cancellazione quando il nodo è già noto;
  - la cancellazione a partire da una chiave corrisponde a `search(key)` seguito da `delete(node)`.
- Stato: definitiva.

## D21 — `select` e `rank` nell'ABR senza `size`

- Decisione:
  - `select` e `rank` non utilizzano informazioni sulla dimensione dei sottoalberi;
  - l'ordine dei nodi viene percorso tramite minimo e successore inorder;
  - `select(i)` parte dal minimo e avanza fino al rango `i`;
  - `rank(node)` parte dal minimo e avanza fino a incontrare lo stesso oggetto nodo;
  - il confronto in `rank` avviene per identità (`is`) e non per uguaglianza della chiave.
- Conseguenza:
  - `select` ha complessità `O(n)` nel caso peggiore;
  - `rank` ha complessità `O(n)` nel caso peggiore.
- Motivazione: mettere in evidenza il limite dell'ABR senza `size` rispetto all'AVL aumentato che sarà implementato nel Task 4.
- Stato: definitiva.

## D22 — Stile implementativo dell'ABR

- Decisione:
  - inserimento iterativo;
  - ricerca iterativa;
  - minimo iterativo;
  - successore iterativo;
  - nessuna procedura ricorsiva necessaria per le operazioni pubbliche dell'ABR.
- Motivazione:
  - coerenza con gli pseudocodici iterativi presentati nelle slide;
  - evitare problemi con il limite di ricorsione di Python nel caso di ABR degenerati.
- Stato: definitiva.

## D23 — Rappresentazione dell'AVL aumentato

- Decisione:
  - AVL implementato come ABR bilanciato;
  - figli assenti rappresentati mediante `None`;
  - `None` è semanticamente equivalente a `T.nil` delle slide;
  - per un figlio assente `height = 0` e `size = 0`;
  - ogni nodo reale appena creato possiede `height = 1` e `size = 1`;
  - ogni nodo contiene `key`, `insertion_id`, `owner`, `parent`, `left`, `right`, `height` e `size`.
- Stato: definitiva.

## D24 — Aggiornamento di `height` e `size`

- Decisione:
  - `height` e `size` vengono ricalcolati localmente tramite una funzione `_update`;
  - `_update` richiede tempo `O(1)`;
  - durante la risalita verso la radice vengono aggiornati entrambi i campi;
  - durante le rotazioni vengono aggiornati prima il nodo ruotato e poi la nuova radice del sottoalbero.
- Motivazione:
  - mantenere gli attributi aumentati senza attraversare nuovamente i sottoalberi;
  - preservare la complessità `O(log n)` delle operazioni AVL.
- Stato: definitiva.

## D25 — Rotazioni e riequilibrio AVL

- Decisione:
  - balance factor definito come `height(left) - height(right)`;
  - vengono gestiti i casi Left-Left, Left-Right, Right-Right e Right-Left;
  - il riequilibrio risale dal primo nodo modificato fino alla radice;
  - ogni rotazione aggiorna puntatori, `height` e `size`.
- Stato: definitiva.

## D26 — `select` e `rank` nell'AVL aumentato

- Decisione:
  - `select` utilizza `left.size + 1` per scegliere il ramo da visitare;
  - `rank` parte da `node.left.size + 1` e risale verso la radice;
  - quando la risalita proviene da un figlio destro vengono aggiunti `parent.left.size + 1`;
  - i ranghi sono indicizzati da 1;
  - l'identità del nodo distingue le occorrenze duplicate.
- Conseguenza:
  - `select` ha complessità `O(log n)`;
  - `rank` ha complessità `O(log n)`.
- Stato: definitiva.

## D27 — Cancellazione nell'AVL aumentato

- Decisione:
  - `delete` riceve il nodo preciso;
  - il nodo richiesto viene fisicamente rimosso;
  - con due figli il successore viene spostato strutturalmente al posto del nodo eliminato;
  - dopo la modifica si risale verso la radice aggiornando `height`, `size` e bilanciamento;
  - il nodo eliminato viene scollegato e impostato con `owner = None`.
- Nota sulla fonte:
  - le slide descrivono il principio di aggiornamento di `size` durante la cancellazione ma non forniscono uno pseudocodice completo della cancellazione AVL;
  - l'implementazione dettagliata adottata nel progetto è quindi una scelta implementativa coerente con gli invarianti AVL e con il mantenimento di `size`.
- Stato: definitiva.

## D28 — Strategia dei test comparati

- Decisione:
  - lista ordinata, ABR senza `size` e AVL aumentato vengono confrontati tramite la loro interfaccia pubblica comune;
  - la forma interna delle strutture non viene confrontata;
  - il contenuto ordinato viene rappresentato nei test tramite coppie `(key, insertion_id)`;
  - `insertion_id` permette di identificare la stessa inserzione logica nelle tre implementazioni e di distinguere correttamente le chiavi duplicate;
  - `select` e `rank` devono produrre risultati equivalenti sulla stessa occorrenza logica;
  - `search` viene confrontata soltanto in termini di presenza/assenza e chiave restituita, perché il contratto consente di restituire una qualsiasi occorrenza in presenza di duplicati;
  - le cancellazioni vengono applicate ai tre nodi corrispondenti alla stessa inserzione logica;
  - oltre a sequenze deterministiche viene utilizzata una sequenza pseudocasuale con seed fisso, in modo che eventuali errori siano riproducibili;
  - nei test può essere utilizzata una lista Python come oracle esterno, senza impiegarla nell'implementazione delle strutture richieste.
- Motivazione:
  - verificare l'equivalenza funzionale delle tre implementazioni indipendentemente dalla loro rappresentazione interna;
  - esercitare esplicitamente i casi con chiavi duplicate;
  - rendere riproducibili eventuali fallimenti.
- Stato: definitiva.

## D29 — Protocollo sperimentale del primo esercizio

- Decisione:
  - vengono confrontati quattro scenari di input:
    1. chiavi distinte pseudocasuali;
    2. chiavi distinte crescenti;
    3. chiavi distinte decrescenti;
    4. chiavi pseudocasuali con molti duplicati;
  - le dimensioni previste per l'esperimento completo sono
    `100, 300, 900, 2700, 5000`;
  - ogni configurazione viene ripetuta 30 volte;
  - prima delle misure definitive vengono eseguiti 3 warm-up non registrati;
  - i dati pseudocasuali vengono generati tramite seed deterministici
    derivati da un seed base `2026`;
  - nello stesso run le tre strutture ricevono esattamente lo stesso input;
  - l'ordine di esecuzione delle tre strutture viene ruotato tra i run.
- Misurazioni:
  - tempo di costruzione mediante `n` inserimenti;
  - `search` di chiavi presenti;
  - `search` di chiavi assenti;
  - `select`;
  - `rank`;
  - `delete(node)`;
  - altezza di ABR e AVL come metrica strutturale secondaria.
- Le operazioni non mutanti vengono misurate in batch di 20 chiamate e
  il tempo totale viene normalizzato per il numero di chiamate.
- `delete(node)` viene misurato con il nodo già individuato.
  La ricerca necessaria per cancellare a partire da una chiave non viene
  inclusa nel timer.
- Generazione dei dati, preparazione dei target, validazione, output,
  CSV e grafici vengono esclususi dalle regioni temporizzate.
- Timer: `time.perf_counter_ns()`.
- Aggregazione principale:
  - mediana;
  - Q1;
  - Q3;
  - IQR.
- Vengono conservati anche tutti i risultati grezzi.
- Sono previste una modalità `quick` per verifica e una modalità `full`
  per gli esperimenti definitivi.
- Stato: definitiva

  ## D30 — Architettura del benchmark

- Decisione:
  - la configurazione sperimentale è separata dal codice di misurazione;
  - i generatori producono input e target prima dell'avvio dei timer;
  - lo stesso input e gli stessi target logici vengono usati per tutte
    le strutture nello stesso run;
  - ogni misura grezza viene rappresentata da un record `Measurement`;
  - costruzione, query e cancellazione vengono temporizzate separatamente;
  - i nodi necessari a `rank` e `delete` vengono individuati fuori dal timer;
  - la cancellazione è l'ultima operazione misurata perché modifica la struttura;
  - l'altezza viene calcolata fuori dalle regioni temporizzate;
  - per l'ABR l'altezza viene calcolata iterativamente per gestire anche
    alberi degenerati;
  - risultati grezzi e aggregati vengono salvati separatamente;
  - vengono salvate anche le informazioni sull'ambiente di esecuzione;
  - sono disponibili modalità `quick`, `calibration` e `full`;
  - la modalità `calibration` è esclusivamente tecnica e i suoi risultati
    non vengono utilizzati nell'analisi finale.
- Stato: definitiva.

## D31 — Presentazione e interpretazione dei risultati

- Decisione:
  - i risultati sperimentali di riferimento sono quelli prodotti dalla
    modalità `full`;
  - vengono utilizzate principalmente le mediane delle 30 ripetizioni;
  - per ogni coppia scenario-operazione vengono generati:
    - un grafico comparativo tra lista ordinata, ABR e AVL;
    - una tabella compatta con i valori mediani;
  - i grafici utilizzano etichette in italiano;
  - i risultati temporali vengono visualizzati in microsecondi;
  - i grafici vengono generati tramite Matplotlib e salvati come file PNG;
  - vengono generati tutti i grafici possibili, ma nella relazione saranno
    inclusi soltanto quelli che mostrano andamenti significativi;
  - `build`, `select` e `rank` sono considerati i confronti principali;
  - i risultati di `delete(node)` vengono interpretati con maggiore cautela
    perché si misura una sola cancellazione per run e i tempi sono molto
    ridotti;
  - una curva graficamente vicina allo zero non viene interpretata come
    tempo nullo, ma come tempo molto inferiore rispetto alla scala del grafico.
- Stato: definitiva.