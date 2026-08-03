# Specifica tecnica — Esercizio 1

## Stato

- Versione: 1.0
- Stato: congelata
- Data: 2026-08-03
- Oggetto: confronto tra implementazioni di statistiche d'ordine dinamiche

## Fonti

- `Esercizi LabAlgo.pdf`, pagina 1.
- `Slide_ASD.pdf`, pagine 248-296.
- In particolare:
  - ABR: pagine 248-266;
  - AVL: pagine 267-283;
  - statistiche d'ordine dinamiche: pagine 284-296.

## Obiettivo

Implementare e confrontare le statistiche d'ordine dinamiche mediante tre strutture dati:

1. lista ordinata collegata;
2. albero binario di ricerca non bilanciato senza attributo `size`;
3. albero AVL aumentato con attributo `size`.

Le tre implementazioni devono fornire operazioni equivalenti, in modo da poter essere verificate e confrontate mediante gli stessi test.

---

## Struttura 1 — Lista ordinata collegata

La struttura sarà una lista doppiamente collegata ordinata.

Ogni elemento sarà rappresentato da un nodo collegato mediante riferimenti ai nodi precedente e successivo.

La lista Python non sarà utilizzata come struttura di memorizzazione interna.

Proprietà richieste:

- ordinamento non decrescente delle chiavi;
- collegamenti coerenti tra nodo precedente e successivo;
- riferimento alla testa;
- riferimento alla coda;
- memorizzazione del numero di nodi;
- duplicati rappresentati mediante nodi distinti.

Una nuova chiave uguale sarà inserita dopo le occorrenze uguali già presenti.

---

## Struttura 2 — ABR senza `size`

La struttura sarà un albero binario di ricerca non bilanciato.

Ogni nodo conterrà almeno:

- chiave;
- riferimento al padre;
- riferimento al figlio sinistro;
- riferimento al figlio destro.

Non sarà presente l'attributo `size`.

Proprietà richiesta:

- le chiavi nel sottoalbero sinistro sono minori o uguali alla chiave del nodo;
- le chiavi nel sottoalbero destro sono maggiori o uguali alla chiave del nodo;
- la visita inorder restituisce una sequenza non decrescente.

Durante l'inserimento, una chiave uguale seguirà inizialmente il ramo destro.

L'albero non effettuerà rotazioni o altre operazioni di bilanciamento.

---

## Struttura 3 — AVL aumentato con `size`

La struttura sarà un albero AVL aumentato con il campo `size`.

Ogni nodo conterrà almeno:

- chiave;
- riferimento al padre;
- riferimento al figlio sinistro;
- riferimento al figlio destro;
- altezza;
- `size`.

Definizione:

`size(x)` è il numero di nodi presenti nel sottoalbero con radice `x`, incluso `x`.

Formula:

`x.size = x.left.size + x.right.size + 1`

Per un figlio assente o una sentinella:

`size = 0`

Proprietà richieste:

- proprietà dell'albero binario di ricerca;
- visita inorder non decrescente;
- differenza tra le altezze dei figli compresa tra -1 e 1;
- altezza corretta per ogni nodo;
- `size` corretto per ogni nodo;
- aggiornamento di altezza e `size` durante inserimenti, cancellazioni e rotazioni.

Durante l'inserimento, una chiave uguale seguirà inizialmente il ramo destro.

Le rotazioni possono modificare la posizione relativa dei nodi con chiavi uguali. La proprietà globale richiesta resta l'ordinamento non decrescente della visita inorder.

---

## Operazioni comuni

Le tre strutture devono fornire le seguenti operazioni logiche:

- `insert`
- `search`
- `delete`
- `select`
- `rank`

I nomi definitivi delle classi, dei tipi e dei metodi Python saranno stabiliti nel Task 1.

---

## Contratto di `insert`

Input:

- una chiave confrontabile con le chiavi già presenti.

Comportamento:

- crea sempre un nuovo nodo;
- sono ammesse chiavi duplicate;
- ogni duplicato è un nodo distinto;
- inserisce il nodo mantenendo gli invarianti della struttura.

Output:

- riferimento al nodo appena inserito.

`insert` non restituisce il rango.

Per conoscere il rango del nodo inserito si userà successivamente `rank(node)`.

---

## Contratto di `search`

Input:

- una chiave.

Comportamento:

- cerca una qualsiasi occorrenza della chiave.

Output:

- riferimento a un nodo corrispondente, se presente;
- `None`, se la chiave è assente.

Quando esistono duplicati, non viene garantito quale occorrenza sia restituita.

---

## Contratto di `delete`

Input:

- riferimento al nodo preciso da cancellare.

Comportamento:

- elimina soltanto il nodo indicato;
- aggiorna collegamenti, dimensione e metadati della struttura;
- mantiene tutti gli invarianti;
- rende il nodo scollegato dalla struttura.

Output:

- `True` se il nodo è stato eliminato;
- `False` se il nodo non appartiene alla struttura o è già stato eliminato.

La cancellazione per nodo evita ambiguità quando sono presenti chiavi duplicate.

---

## Contratto di `select`

Input:

- rango intero `i`.

Convenzione:

- il rango parte da 1;
- `select(1)` restituisce il nodo minimo;
- `select(n)` restituisce il nodo massimo.

Output:

- riferimento al nodo che occupa la posizione `i` nella visita inorder.

Errore:

- `IndexError` se `i < 1` oppure `i > n`.

---

## Contratto di `rank`

Input:

- riferimento a un nodo appartenente alla struttura.

Output:

- posizione del nodo nella visita inorder;
- il risultato è un intero compreso tra 1 e `n`.

Il rango è associato all'identità del nodo, non soltanto alla sua chiave.

Due nodi distinti con la stessa chiave possono avere ranghi differenti.

Errore:

- `ValueError` se il nodo non appartiene alla struttura o è già stato eliminato.

---

## Gestione dei duplicati

Decisioni:

- le chiavi duplicate sono ammesse;
- ogni duplicato è memorizzato come nodo distinto;
- due duplicati possono avere ranghi differenti;
- `rank` utilizza l'identità del nodo;
- `delete` riceve il nodo preciso;
- negli alberi, l'uguaglianza segue inizialmente il ramo destro;
- nella lista, un duplicato viene inserito dopo le occorrenze uguali già presenti.

Non sarà utilizzato un contatore di molteplicità all'interno di un singolo nodo.

---

## Comportamento nei casi limite

| Caso | Comportamento |
|---|---|
| `search` su struttura vuota | restituisce `None` |
| `select` su struttura vuota | genera `IndexError` |
| `select(0)` | genera `IndexError` |
| `select(n + 1)` | genera `IndexError` |
| `rank` su nodo estraneo | genera `ValueError` |
| `rank` su nodo eliminato | genera `ValueError` |
| `delete` su nodo estraneo | restituisce `False` |
| doppia cancellazione dello stesso nodo | la seconda restituisce `False` |
| inserimento di chiave duplicata | crea un nuovo nodo |
| ricerca di chiave duplicata | restituisce una qualsiasi occorrenza |
| cancellazione dell'ultimo nodo | lascia la struttura vuota e valida |

---

## Invarianti della lista ordinata

- la sequenza delle chiavi è non decrescente;
- `head.prev` è assente;
- `tail.next` è assente;
- per ogni nodo, i collegamenti `prev` e `next` sono coerenti;
- non sono presenti cicli;
- il numero di nodi raggiungibili coincide con la dimensione registrata.

---

## Invarianti dell'ABR

- nessun nodo possiede l'attributo `size`;
- ogni figlio contiene il riferimento corretto al padre;
- la radice non ha padre;
- non sono presenti cicli;
- la visita inorder è non decrescente;
- il numero dei nodi raggiungibili coincide con la dimensione registrata.

---

## Invarianti dell'AVL aumentato

- sono rispettati tutti gli invarianti dell'ABR;
- per ogni nodo il fattore di bilanciamento è compreso tra -1 e 1;
- l'altezza memorizzata coincide con quella calcolata;
- `size` coincide con il numero effettivo di nodi del sottoalbero;
- la radice non ha padre;
- eventuali sentinelle hanno altezza e `size` coerenti con la convenzione adottata.

---

## Stile implementativo

Regola generale:

1. seguire lo pseudocodice delle slide;
2. mantenere ricorsive le procedure presentate soltanto in forma ricorsiva;
3. mantenere iterative le procedure presentate in forma iterativa;
4. quando sono presentate entrambe le alternative, preferire quella più efficiente e sicura in Python;
5. motivare nella relazione ogni differenza rispetto allo pseudocodice.

Per l'ABR non bilanciato saranno preferite procedure iterative quando la ricorsione potrebbe raggiungere il limite di profondità di Python.

---

## Vincoli

- codice scritto da zero;
- nessuna implementazione esterna delle strutture dati;
- nessuna lista Python usata come memorizzazione interna della lista collegata;
- programmi `.py`, non notebook;
- tutte le strutture devono essere modificabili e spiegabili durante l'orale.

---

## Aspetti rinviati al Task 1

Non sono ancora fissati:

- nomi definitivi delle classi;
- nomi definitivi delle classi nodo;
- annotazioni di tipo Python;
- uso di `Protocol` o classe astratta;
- sistema concreto per verificare l'appartenenza di un nodo;
- eventuali sentinelle;
- visibilità pubblica o privata dei metodi ausiliari.

---

## Aspetti rinviati ai task sperimentali

Non sono ancora fissati:

- dimensioni degli input;
- numero di ripetizioni;
- seed;
- scenari completi;
- formato dei CSV;
- aggregazioni statistiche;
- grafici;
- tabelle;
- modalità rapida e completa.

---

## Criteri di accettazione della specifica

La specifica è considerata congelata quando:

- le tre strutture sono definite;
- le cinque operazioni comuni sono definite;
- input e output logici sono definiti;
- la gestione dei duplicati è definita;
- il rango parte da 1;
- casi limite ed errori sono definiti;
- gli invarianti principali sono definiti;
- gli aspetti non ancora decisi sono esplicitamente rinviati ai task successivi.
