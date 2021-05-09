# Watermark
## Versione 1.2.4

Il programma applica un watermark nell’angolo in basso a destra alle immagini fornite. 
La dimensione dell’immagine del logo inserita è stabilita al 12% della larghezza di ogni foto.
Accanto al logo viene inserita la scritta su due livelli “Associazione Scout Laica Portici”.
La lunghezza della scritta è fissa ai 3/18-esimi della dimensione del logo.

# Istruzioni per l’uso:
1) copiare l’immagine del logo da inserire nella cartella “logo”
2) copiare le foto alle quali applicare il watermark nella cartella “pool”
3) doppio click sull’eseguibile “watermark”

Si aprirà una shell terminale che mostra i progressi fatti dal programma.
Il terminale chiederà se si desidera riscalare o meno le immagini. Inserire “y” oppure “n”. Il terminale chiederà inoltre di inserire la qualità di salvataggio delle foto su una scala da 75 a 95. Il parametro di default è 75.
Se l’immagine supera in una dimensione i 1024 pixel il programma esegue un riscalamento in modo da portare le dimensioni entro i 1024 pixel e aggiunge al nome la stringa “_r”.
Le foto processate vengono salvate, insieme alla loro directory, nella cartella “watermarked”.
Alle immagini processate viene aggiunta la stringa “_w” nel nome file.
Ogni operazione eseguita viene scritta nel file “log.txt” preceduta da data e orario di
inizio operazione.

## Accortenze

- TUTTE LE FOTO IN POOL VENGONO IRRIMEDIABILMENTE CANCELLATE DOPO ESSERE STATE PROCESSARE. ASSICURARSI DI COPIARE I FILE INSERITI PRIMA DI LANCIARE IL PROGRAMMA.