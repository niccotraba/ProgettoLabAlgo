# Conclusioni sperimentali — Esercizio 1

## Costruzione

I risultati sperimentali mostrano che il costo di costruzione dipende
fortemente dall'ordine di inserimento per lista ordinata e ABR.

La lista ordinata risulta particolarmente penalizzata dagli input
crescenti, poiché ogni nuovo elemento viene inserito verso la coda e
richiede una scansione della struttura già costruita. Al contrario,
l'input decrescente rende gli inserimenti molto più economici perché i
nuovi elementi vengono inseriti vicino alla testa.

L'ABR non bilanciato mostra un forte peggioramento negli scenari crescente
e decrescente, nei quali l'albero degenera e raggiunge altezza pari a n.
Negli scenari casuali il comportamento risulta sensibilmente migliore.

L'AVL presenta invece un comportamento più stabile tra i diversi scenari,
coerentemente con il mantenimento di un'altezza logaritmica.

## Search

Le misure di search mostrano differenze tra chiavi presenti e assenti,
legate alla posizione del target e alla forma della struttura.

L'ABR risente in modo marcato degli input crescente e decrescente, mentre
l'AVL mantiene prestazioni più stabili grazie al bilanciamento.

Nella lista ordinata il costo dipende fortemente dalla posizione della
chiave e dalla possibilità di interrompere anticipatamente la scansione.

## Select

Select evidenzia chiaramente la differenza tra strutture non aumentate e
AVL aumentato.

Lista ordinata e ABR senza size mostrano una crescita significativa con n,
coerente con il costo lineare previsto.

L'AVL sfrutta invece l'attributo size dei sottoalberi e mantiene tempi
molto più contenuti, coerentemente con una complessità O(log n).

## Rank

Anche rank mostra in modo netto il vantaggio dell'aumento con size.

Lista ordinata e ABR senza size devono percorrere progressivamente
l'ordinamento per determinare il rango del nodo, mentre l'AVL può
calcolarlo risalendo lungo un solo cammino dell'albero.

La curva dell'AVL rimane molto vicina all'asse X rispetto alle altre
strutture, indicando tempi di esecuzione nettamente inferiori e coerenti
con il comportamento logaritmico previsto.

## Delete

La cancellazione viene misurata con il riferimento al nodo già noto,
quindi il tempo di ricerca non è incluso.

La lista ordinata può scollegare il nodo modificando un numero costante di
puntatori e mostra quindi costi molto ridotti.

L'AVL presenta un overhead maggiore perché, dopo la rimozione, deve
aggiornare height e size e può dover ripristinare il bilanciamento tramite
rotazioni.

Poiché viene eseguita una sola cancellazione per run e i tempi sono molto
ridotti, i risultati di delete vengono interpretati soprattutto in modo
qualitativo.

## Conclusioni generali

Gli esperimenti confermano le ipotesi teoriche principali.

La lista ordinata può risultare competitiva in specifici scenari,
soprattutto quando le modifiche avvengono in posizioni favorevoli, ma le
operazioni select e rank rimangono lineari.

L'ABR non bilanciato può offrire buone prestazioni su input favorevoli, ma
è fortemente sensibile all'ordine di inserimento e può degenerare fino ad
altezza lineare.

L'AVL aumentato introduce un costo aggiuntivo per mantenere bilanciamento,
height e size, ma offre prestazioni più stabili e soprattutto rende
select e rank efficienti, che rappresentano le operazioni caratteristiche
delle statistiche d'ordine dinamiche.