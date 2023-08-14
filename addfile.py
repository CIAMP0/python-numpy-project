import argparse
import csv
import os
import shutil

print("")  # creo spazio

# creo liste di appoggio
ImagesExtensions = ['.png', '.jpg', '.jpeg', '.gif']  # lista estensioni immagini
DocumentsExtensions = ['.doc', '.docx', '.odt', '.pages', '.txt']  # lista estensioni documenti
AudioExtensions = ['.mp3', '.acc', '.wav']  # lista estensioni audio
Ext_list = ImagesExtensions + DocumentsExtensions + AudioExtensions  # lista comprendente tutte le estensioni supportate
SubDir_list = []  # lista sottocartelle della cartella files
file_list = []  # lista file nella cartella files compatibili con lo spostamento in sottocartella

# divido i file della cartella files tra sottocartelle e file
# in modo da dare come lista di possibili scelte all'utente solo quelle valide
for x in os.listdir("files"):
    x_name, x_ext = os.path.splitext(x)  # ricavo nome ed estensione
    if os.path.isdir(os.path.join("files", x)):  # identifico sottocartelle
        SubDir_list += [x]  # aggiungo sottocartelle
    elif x_ext in Ext_list:  # identifico file compatibili
        file_list += [x]  # aggiungo file
    else:  # nel caso i file non siano ne sottocartelle ne file compatibili li ignoro
        continue


def add_file(file_name):
    global SubDir_list

    # creo file recap.csv se non esiste già
    if not os.path.isfile(os.path.join("files", "recap.csv")):  # verifico esistenza file
        with open(os.path.join("files", "recap.csv"), "w") as file:  # creo e apro il file in scrittura
            writer = csv.writer(file)
            writer.writerow(["name", "type", "size"])  # inserisco intestazione

    name, ext = os.path.splitext(file_name)  # ricavo nome ed estensione dei file che posso spostare
    size = os.path.getsize(os.path.join("files", file_name))  # trovo dimensione file

    # assegno nome sottocartella e gestico possibili files non riconosciuti
    if ext in ImagesExtensions:
        SubDirName = 'Images'
    elif ext in DocumentsExtensions:
        SubDirName = 'Docs'
    else:  # ext in AudioExtensions:
        SubDirName = 'Audio'

    # se non già presente aggiungo nome sotto-cartella alla lista e creo sotto-cartella
    if SubDirName not in SubDir_list:
        SubDir_list += [SubDirName]  # aggiungo il nome della cartella alla lista
        os.makedirs(os.path.join("files", SubDirName))  # creo sotto-cartella

    # sposto il file nella sottocartella
    shutil.move(os.path.join("files", file_name), os.path.join("files", SubDirName))

    # stampo info richieste
    print(f"name: {name}, type: {SubDirName}, size: {size}")

    # apro il file di recap e lo aggiorno
    with open(os.path.join("files", "recap.csv"), 'a') as recap:
        writer = csv.writer(recap)
        writer.writerow([name, SubDirName, size])


# definisco l'interfaccia a linea di comando
dscr = """ 
scegli un file presente nella cartella files,
questo verrà spostato nella sottocartella in base alla sua estensione.
Ricorda di scrivere anche l'estensione del file!
es: pomodoro.png 
"""

parser = argparse.ArgumentParser(description=dscr)  # creo il parser
parser.add_argument("file_name",
                    choices=file_list,
                    help="lista dei file da spostare nella sottocartella")  # aggiungo gli elementi
args = parser.parse_args()  # definisco gli elementi

# lancio funzione
add_file(args.file_name)
