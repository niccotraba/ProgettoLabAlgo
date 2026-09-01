Trabalzini, Niccolò, 7114267
----------------------

Testo esercizio 1:
Confrontare varie implementazioni di statistiche d'ordine dinamiche:
1. lista ordinata;
2. ABR senza attributo size;
3. struttura come vista a lezione.
La lista è implementata mediante strutture collegate con puntatori e non mediante la lista Python.

----------------------
Esecuzione esercizio 1:

Aprire una console Bash e posizionarsi nella directory radice del progetto,
cioè nella cartella che contiene la directory "esercizio1".

Per eseguire una verifica rapida del programma:

python -m esercizio1.main --quick

La modalità quick utilizza una configurazione ridotta ed è adatta alla
verifica dell'esecuzione su PythonAnywhere.

Per eseguire il benchmark completo utilizzato per produrre i risultati
descritti nella relazione:

python -m esercizio1.main --full

Sono inoltre disponibili:

python -m esercizio1.main --calibrate

per una esecuzione tecnica di calibrazione.

Se non viene specificata alcuna opzione:

python -m esercizio1.main

viene utilizzata automaticamente la modalità quick.

----------------------
Output

Il benchmark crea automaticamente, se non presenti, le cartelle necessarie
all'interno di:

esercizio1/risultati/

e salva:

- dati grezzi in esercizio1/risultati/dati_grezzi/
- dati aggregati in esercizio1/risultati/dati_aggregati/
- informazioni sull'ambiente di esecuzione nella cartella dei risultati.

----------------------
Generazione di grafici e tabelle

Dopo aver eseguito il benchmark completo con --full, i grafici e le tabelle
possono essere generati con:

python -m esercizio1.esperimenti.presentazione_risultati

Il programma legge il dataset aggregato prodotto dalla modalità full e crea:

- esercizio1/risultati/grafici/
- esercizio1/risultati/tabelle/

Le cartelle di output vengono create automaticamente se non esistono.