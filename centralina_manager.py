import os
import sys
import platform
from centralina import Centralina


def clean_screen():
    input("Premi INVIO per continuare...")
    if platform.system() == "Windows":
        os.system('cls')
    if platform.system() == "Linux":
        os.system('clear')


def main():
    scelta = input("Caricare i dati presenti in memoria (file centralina.json) [y/n]: ")
    if scelta.lower() == "y":
        test = Centralina("start", "", "", 0)
        centralina = test.__carica_configurazione__()
        print(type(centralina))

    else:
        nome = input("Nome della centralina: ")
        portata = int(input("Portata litri/minuto della pompa: "))
        gps = input("Si desidera impostare la posizione GPS per i controlli meteo? [y/n]:")
        if gps.lower() == "y":
            latitudine = input("Latitudine: ")
            longitudine = input("Longitudine: ")
            centralina = Centralina(nome, latitudine, longitudine, portata)
        else:
            centralina = Centralina(nome, "", "", portata)

    while True:
        clean_screen()
        # __aggiorna_meteo__(coordinate_amato)
        print("---MENU'---")
        print("1.\tCREA PROGRAMMA")
        print("2.\tMOSTRA PROGRAMMI CREATI")
        print("3.\tATTIVA TUTTI I PROGRAMMI")
        print("4.\tSTOPPA TUTTI I PROGRAMMI")
        print("5.\tSALVA CONFIGURAZIONE")
        print("6.\tCARICA CONFIGURAZIONE")
        print("7.\tIMPOSTA COORDINATE GPS")
        print("8.\tINFORMAZIONI")
        print("9.\tMETEO")
        print("99.\tESCI")
        try:
            scelta = int(input("Seleziona un'opzione: "))
        except:
            pass
        if scelta == 1:
            centralina.__crea_programma__()
        elif scelta == 2:
            centralina.__mostra_programmi__()
        elif scelta == 3:
            centralina.__avvia_programmi__()
        elif scelta == 4:
            # centralina.stoppa()
            print("blocco programmi")
        elif scelta == 5:
            centralina.__salva_configurazione__()
        elif scelta == 6:
            centralina.__carica_configurazione__()
        elif scelta == 7:
            centralina.__set_coordinate__()
        elif scelta == 8:
            print(centralina)
        elif scelta == 9:
            print(centralina.meteo_attuale)
        elif scelta == 99:
            sys.exit(0)


if __name__ == "__main__":
    main()
