import threading
import time

import jsonpickle
import json
import meteo_pyowm
import utilities
from oggetti import Programma, Settore
import logging
from prettytable import PrettyTable

global meteo
meteo = ""
time_stop = threading.Event()


def __aggiorna_meteo__(latitudine, longitudine):
    global meteo
    try:
        meteo = meteo_pyowm.get_current_weather(latitudine, longitudine)
        return meteo
    except Exception as e:
        logging.error(e)
        return ""


def meteo_async(f_stop, latitudine, longitudine):
    # do something here ...
    __aggiorna_meteo__(latitudine, longitudine)
    # print(meteo_attuale)
    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(30, meteo_async, [f_stop, latitudine, longitudine]).start()


class Centralina(object):
    def __init__(self, nome, latitudine, longitudine, portata):
        self.nome = nome

        logging.basicConfig(filename=str("logs/" + self.nome + '.log'), level=logging.DEBUG,
                            format='%(asctime)s %(message)s')

        if utilities.check_coordinates(latitudine, longitudine) is not None:
            self.latitudine, self.longitudine = utilities.check_coordinates(latitudine, longitudine)
            self.check_meteo = True
            self.__attiva_meteo_automatico__()
        else:
            self.check_meteo = False
            self.latitudine = ""
            self.longitudine = ""
        self.lista_programmi = []
        self.portata_pompa = portata
        self.meteo_attuale = __aggiorna_meteo__(self.latitudine, self.longitudine)

    def __str__(self):
        if len(self.lista_programmi) > 0:
            return "INFO CENTRALINA: \n" \
                   + "Nome:\t\t" + self.nome + "\n" \
                   + "Programmi:\t" + str(len(self.lista_programmi)) + "\n" \
                   + "Coordinate GPS:\t" + self.latitudine + ", " + self.longitudine
        else:
            return str("INFO CENTRALINA: \n" + "Nome:\t\t" + self.nome + "\n")

    def __crea_programma__(self):
        try:
            hh = int(input("Inserisci l'ora di avvio (formato 0-24): "))
            mm = int(input("Inserisci il minuto di avvio (formato 0-59): "))
            programma = Programma(nome=input("Nome del programma: "), ora_inizio=hh, minuti_inizio=mm,
                                  portata_pompa=self.portata_pompa)
            programma.__crea_settore__()
            self.lista_programmi.append(programma)
            print("Programma creato con successo")
        except Exception as e:
            print("Errore, creazione annullata")

    def __mostra_programmi__(self):

        print(" --- Lista dei programmi --- ")
        x = PrettyTable()
        x.field_names = ["ID", "Nome", "N° settori", "Abilitato"]
        i = 0
        for programma in self.lista_programmi:
            x.add_row([i, programma.nome, len(programma.lista_settori), str(programma.status)])
            i += 1
        print(x)

    def __salva_configurazione__(self):
        try:
            centralina_freezed = jsonpickle.encode(self)
            with open('salvataggi/centralina.json', 'w') as outfile:
                json.dump(centralina_freezed, outfile)
            print("SALVATAGGIO COMPLETATO")
            logging.info("centralina scritta in memoria correttamente")
        except Exception as e:
            print("ERRORE NEL SALVATAGGIO")
            logging.error(e)

    def __carica_configurazione__(self):
        try:
            with open('salvataggi/centralina.json', 'r+') as f:
                frozen = json.load(f)
            centralina = jsonpickle.decode(frozen)
            self.nome = centralina.nome
            self.lista_programmi = centralina.lista_programmi
            self.check_meteo = centralina.check_meteo
            self.portata_pompa = centralina.portata_pompa
            self.longitudine = centralina.longitudine
            self.latitudine = centralina.latitudine
            print("CARICAMENTO COMPLETATO")
            logging.info("centralina caricata dalla memoria correttamente")
            return self
        except Exception as e:
            print("ERRORE NEL CARICAMENTO")
            logging.error(e)

    def __attiva_meteo_automatico__(self):
        # start calling f now and every 60 sec thereafter
        if utilities.check_coordinates(self.latitudine, self.longitudine) is not None:
            meteo_async(time_stop, self.latitudine, self.longitudine)
        else:
            print("Coordinate GPS non impostate.")

    def __disattiva_meteo_automatico__(self):
        # stop the thread when needed
        time_stop.set()

    def __set_coordinate__(self):
        lat = input("Latitudine: ")
        long = input("Longitudine: ")
        utilities.check_coordinates(lat, long)
        if utilities.check_coordinates(lat, long) is not None:
            self.latitudine, self.longitudine = utilities.check_coordinates(lat, long)
        else:
            print("Coordinate non valide")

    def __scan_programs__(self):
        for programma in self.lista_programmi:
            if utilities.check_orario_now(programma.ora_inizio, programma.ora_fine):
                # print("Inizio programma:\t" + programma.nome)
                programma.status = True
                programma.__start__()
            else:
                # print("Fine programma:\t " + programma.nome)
                programma.status = False
                programma.__stop__()

    def __avvia_programmi__(self):
        while 1:
            self.__scan_programs__()
            print("scan")
            time.sleep(1)

    def __add_settore_to_programma__(self):
        self.__mostra_programmi__()
        id = int(input("DIGITARE L'ID DEL PROGRAMMA: "))
        self.lista_programmi[id].__crea_settore__()
