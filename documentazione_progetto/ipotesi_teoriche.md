# Ipotesi teoriche — Esercizio 1

## 1. Obiettivo

Le ipotesi vengono formulate sulla base delle complessità teoriche delle
tre strutture prima dell'interpretazione dei risultati sperimentali.

Le strutture confrontate sono:

1. lista ordinata doppiamente collegata;
2. ABR non bilanciato senza `size`;
3. AVL aumentato con `size`.

Le misure sperimentali considerate sono:

- costruzione tramite `n` inserimenti;
- search di chiavi presenti;
- search di chiavi assenti;
- select;
- rank;
- delete con riferimento al nodo già noto.


## 2. Complessità delle singole operazioni

| Operazione | Lista ordinata | ABR senza size | AVL + size |
|---|---:|---:|---:|
| insert | O(n) | O(h) | O(log n) |
| search | O(n) | O(h) | O(log n) |
| delete(node) | Theta(1) | O(h) | O(log n) |
| select | O(n) | O(n) | O(log n) |
| rank | O(n) | O(n) | O(log n) |

Per l'ABR `h` indica l'altezza dell'albero e dipende fortemente
dall'ordine di inserimento.


## 3. Ipotesi sulla costruzione

La misura `build` rappresenta il tempo totale necessario a eseguire
`n` inserimenti.

### 3.1 Lista ordinata

#### Input crescente

Ogni nuovo elemento viene inserito verso la coda e richiede una scansione
della lista già presente.

Tempo totale atteso:

`Theta(n^2)`.

#### Input decrescente

Ogni nuovo elemento è minore della testa corrente e viene quindi inserito
in testa dopo un controllo locale.

Tempo totale atteso:

`Theta(n)`.

#### Input casuale distinto

La posizione di inserimento è variabile ma mediamente richiede la visita
di una frazione lineare degli elementi già presenti.

Tempo totale atteso:

`Theta(n^2)` in media.

#### Input con molti duplicati

La lista deve comunque individuare la corretta posizione ordinata e i
duplicati vengono inseriti dopo quelli già presenti.

Si prevede un comportamento complessivamente vicino al caso quadratico.


## 4. Ipotesi sull'ABR senza size

### Input crescente e decrescente

L'albero degenera in una catena.

Altezza:

`Theta(n)`.

Le singole operazioni dipendenti dall'altezza diventano quindi lineari.

La costruzione mediante `n` inserimenti ha tempo totale:

`Theta(n^2)`.

### Input casuale distinto

Un ABR costruito da un ordine casuale non dovrebbe degenerare
sistematicamente.

Si prevede:

- altezza attesa dell'ordine di `log n`;
- search e insert mediamente dell'ordine di `log n`;
- costruzione complessiva dell'ordine di `n log n`.

### Input con molti duplicati

La regola adottata invia inizialmente le chiavi uguali a destra.

La forma risultante dipende dalla distribuzione effettiva delle chiavi.
Si prevede un'altezza mediamente maggiore rispetto al caso casuale con
chiavi distinte, ma non viene fissata un'ipotesi asintotica più forte.

Questo scenario viene quindi considerato input-sensitive.


## 5. Ipotesi sull'AVL aumentato

L'AVL mantiene altezza `O(log n)` indipendentemente dall'ordine di
inserimento.

Si prevede quindi:

- build: `O(n log n)`;
- search: `O(log n)`;
- select: `O(log n)`;
- rank: `O(log n)`;
- delete: `O(log n)`.

L'attributo `size` permette a select e rank di evitare una scansione
lineare dell'ordinamento.


## 6. Ipotesi su search

### Lista ordinata

Per una chiave presente scelta in modo distribuito nell'insieme ordinato,
il numero medio di nodi visitati cresce linearmente con `n`.

Per le chiavi assenti il benchmark alterna valori inferiori al minimo e
superiori al massimo:

- sotto il minimo: terminazione quasi immediata;
- sopra il massimo: scansione completa.

Il batch complessivo mantiene quindi un comportamento atteso lineare.

### ABR

- crescente/decrescente: `Theta(n)` nel workload medio del benchmark;
- casuale distinto: comportamento atteso vicino a `O(log n)`;
- molti duplicati: comportamento dipendente dall'altezza effettivamente
  prodotta.

### AVL

Comportamento atteso `O(log n)` in tutti gli scenari.


## 7. Ipotesi su select e rank

### Lista ordinata

Entrambe le operazioni richiedono una scansione a partire dalla testa.

Comportamento atteso:

`Theta(n)` per target distribuiti nell'intervallo dei ranghi.

### ABR senza size

La struttura non dispone dell'informazione sulla dimensione dei
sottoalberi.

Select e rank percorrono quindi l'ordinamento tramite minimo e successori.

Comportamento atteso:

`O(n)` e, con ranghi distribuiti, andamento empirico approssimativamente
lineare.

### AVL aumentato

L'attributo `size` consente di scendere o risalire lungo un solo cammino
dell'albero.

Comportamento atteso:

`O(log n)`.


## 8. Ipotesi su delete

Il benchmark misura `delete(node)` con il riferimento al nodo già noto.

### Lista

Lo scollegamento modifica un numero costante di puntatori.

Tempo atteso:

`Theta(1)`.

### ABR

Il limite superiore dipende dall'altezza:

`O(h)`.

Tuttavia il costo effettivo dipende anche dalla configurazione locale del
nodo cancellato. Un nodo con zero o un figlio può essere eliminato con
pochi aggiornamenti anche in un albero molto alto.

Non ci si aspetta quindi che il singolo benchmark di delete segua
perfettamente la curva dell'altezza.

### AVL

Il limite teorico è `O(log n)` per il ripristino degli invarianti.

Anche in questo caso una singola cancellazione può avere un costo molto
piccolo e il timer misura una sola operazione per run.

I risultati di delete saranno quindi considerati evidenza secondaria e
interpretati con maggiore cautela.


## 9. Ipotesi strutturali sull'altezza

### ABR

- increasing: altezza `n`;
- decreasing: altezza `n`;
- random_distinct: altezza molto inferiore a `n`, attesa dell'ordine
  logaritmico;
- duplicate_heavy: altezza input-sensitive e presumibilmente superiore
  al caso casuale distinto.

### AVL

L'altezza deve rimanere dell'ordine di `log n` in tutti gli scenari.

L'altezza costituisce una metrica esplicativa: permette di collegare
la forma della struttura ai tempi osservati.


## 10. Criterio di confronto con i dati

La mediana delle 30 ripetizioni viene utilizzata come misura principale.

Per le curve temporali verranno confrontati:

- andamento al crescere di `n`;
- fattore di crescita fra dimensione minima e massima;
- normalizzazione rispetto al modello teorico;
- altezza di ABR e AVL.

Non verrà richiesto che i tempi sperimentali seguano esattamente una
funzione matematica ideale: costi costanti, interprete Python, cache,
scheduler e granularità del timer possono influire sui valori misurati.