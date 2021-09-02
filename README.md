# Playlist Converter

![logo](https://routenote.com/blog/wp-content/uploads/2017/12/if_spotify_then_deezer.png)

## Descrizione

Questo programma ha il compito di trasferire tutte le tracce presenti in una playlist, dalla piattaforma Spotify alla piattaforma Deezer. Per poter interagire con i due servizi musicali ho dovuto utilizzare gli API, anche noti come Web-Services, forniti dai 2 servizi musicali.

## Struttura del progetto

Il progetto e' suddiviso in diverse cartelle quali:
* **data** : cartella che contiene il file config.ini (file che contiene i dati necessari a interfacciarsi con i diversi API)
* **libs** : cartella che contiene le librerie da me realizzata al fine di semplificare l'esecuzione di alcuni comandi

## File del progetto

* **Deez.py** : classe principale per la gestione dell'API di deezer. Questa classe contiene diversei metodi che verranno approfonditi nella sezione Deezer.

* **Spotify.py** : classe principale per la gestione dell'API di deezer. Questa classe contiene diversi metodi che verranno approfonditi nella sezione Deezer.

* **PlaylistConverter.py** : classe che si occupa di creare l'interazione tra Spotify e Deezer al fine di permettere il trasferimentod delle playlist da una piattaforma all'altra.

* **Track.py** : classe che contiene tutte le proprieta' riguardanti una trccia. 

## Deez.py

Questa classe contiene i seguenti metodi:


# Note

Per migliorare l'aspetto grafico ho aggiunto una funzione nel file __init__.py della classe progress scaricata da internet
che mi permettesse di aggiornare il messaggio a lato sinstro della progress bar in modo da poterci inserire la traccia corrente che stava trasferendo.

Questo progetto è stata la tesi per la maturità 2019/2020

La funzione e' questa:
```
def edit_message(self, message):
    self.message = message
```
