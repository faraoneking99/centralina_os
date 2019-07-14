import datetime
import sys
import threading
from time import sleep
from utilities import check_orario_now
import jsonpickle

import meteo_pyowm
from oggetti import Programma

global meteo_attuale

lista_programmi = []

coordinate_amato = (38.369992, 15.954787)

print("------ CENTRALINA FARAONE V1.0 ------")


def __carica_configurazione__():
    with open('salvataggi/centralina.json', 'r+') as f:
        frozen = f.read()
    global lista_programmi
    lista_programmi = jsonpickle.decode(frozen)


load_previous = input("Caricare i dati se presenti in memoria?: [y/n]")
if load_previous != "n":
    __carica_configurazione__()

global portata_pompa
portata_pompa = input("Portata della pompa: ")


def __aggiorna_meteo__(coordinate):
    global meteo_attuale

    amato_latitudine, amato_longitudine = coordinate
    meteo_attuale = meteo_pyowm.get_current_weather(amato_latitudine, amato_longitudine)


def meteo_async(f_stop):
    global meteo_attuale

    # do something here ...
    __aggiorna_meteo__(coordinate_amato)
    # print(meteo_attuale)
    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(30, meteo_async, [f_stop]).start()


time_stop = threading.Event()
# start calling f now and every 60 sec thereafter
meteo_async(time_stop)


# stop the thread when needed
# f_stop.set()


def __crea_programma__():
    try:
        hh = int(input("Inserisci l'ora di avvio (formato 0-24): "))
        mm = int(input("Inserisci il minuto di avvio (formato 0-59): "))
        programma = Programma(nome=input("Nome del programma: "), ora_inizio=hh, minuti_inizio=mm,
                              portata_pompa=portata_pompa)
        programma.__crea_settore__()
        lista_programmi.append(programma)
        print("Programma creato con successo")
    except Exception as e:
        print("Errore, creazione annullata")


def __mostra_programmi__():
    print(" --- Lista dei programmi --- ")
    i = 0
    for programma in lista_programmi:
        print(str(i) + ". \t" + programma.nome + "\t ATTIVO: " + str(programma.status))
        i += 1


def __scan_programs__():
    for programma in lista_programmi:
        if check_orario_now(programma.ora_inizio, programma.ora_fine):
            # print("Inizio programma:\t" + programma.nome)
            programma.status = True
            programma.__start__()
        else:
            # print("Fine programma:\t " + programma.nome)
            programma.status = False
            programma.__stop__()


def check_time(f_stop):
    # do something here ...
    # print(str(meteo_attuale.get_rain()))
    if str(meteo_attuale.get_rain()) == "{}":
        __scan_programs__()
    if not f_stop.is_set():
        # call check_time() again in 29 seconds
        threading.Timer(10, check_time, [f_stop]).start()


time_stop = threading.Event()
# start calling f now and every 60 sec thereafter
check_time(time_stop)

# stop the thread when needed
# f_stop.set()


"""
FINE DEL NON TOCCARE
"""


def __salva_configurazione__():
    centralina_freezed = jsonpickle.encode(lista_programmi)
    import json
    with open('salvataggi/centralina.json', 'w') as f:
        json.dump(centralina_freezed, f)


while True:
    # __aggiorna_meteo__(coordinate_amato)
    print("---MENU'---")
    print("1.\tCREA PROGRAMMA")
    print("2.\tMOSTRA SETTORI")
    print("3.\tSTOPPA/RIATTIVA TUTTI I PROGRAMMI")
    print("4.\tSALVA CONFIGURAZIONE")
    print("99.\tSPEGNI")
    scelta = int(input("Seleziona un'opzione: "))
    if scelta == 1:
        __crea_programma__()
    elif scelta == 2:
        __mostra_programmi__()
    elif scelta == 4:
        __salva_configurazione__()
    elif scelta == 99:
        sys.exit(0)
