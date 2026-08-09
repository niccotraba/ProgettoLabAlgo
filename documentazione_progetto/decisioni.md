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