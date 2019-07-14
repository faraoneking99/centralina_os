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
    try:
        test = Centralina("start", "", "", 0)
        centralina = test.__carica_configurazione__()
    except Exception as e:
        print("Errore nel caricamento di centralina.json")
        sys.exit(99)
    centralina.__avvia_programmi__()


if __name__ == "__main__":
    main()
