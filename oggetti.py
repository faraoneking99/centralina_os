import datetime
import time


class Pianta():
    def __init__(self, nome, litri_richiesti):
        self.nome = nome
        self.litri_richiesti = litri_richiesti

    def __get_litri_pianta__(self):
        return self.litri_richiesti


class Settore():
    def __init__(self, nome, numero_piante, irrigatori_per_pianta):
        self.nome = nome
        self.numero_piante = numero_piante
        self.irrigatori_per_pianta = int(irrigatori_per_pianta)

    def __get_litri_necessari__(self):
        return self.piante.litri_richiesti * self.numero_piante

    def __aggiungi_coltivazione__(self):
        tipo_pianta = input("tipo di pianta: ")
        litri_pianta = int(input("litri per pianta: "))
        pianta = Pianta(tipo_pianta, litri_pianta)
        self.piante = pianta
        self.litri_pianta_su_irrigatore = litri_pianta / self.irrigatori_per_pianta


class Programma():
    def __init__(self, nome, ora_inizio, minuti_inizio, portata_pompa):
        self.nome = nome
        self.lista_settori = []
        self.ora_inizio = ora_inizio
        self.minuti_inizio = minuti_inizio
        self.lista_vavole = []
        self.portata_pompa = portata_pompa
        self.status = True

    def __activate__(self):
        self.status = True

    def __deactivate__(self):
        self.status = False

    def __show_settori__(self):
        print("--- SETTORI ESISTENTI ---")
        for settore in self.lista_settori:
            print(settore.nome + "\t" + settore.numero_piante + "L/pianta")
        print("-----------")

    def __crea_settore__(self):
        print("---- Aggiunta Settore ----")
        settore = Settore(nome=input("Nome settore: "), irrigatori_per_pianta=input("Numero irrigatori per pianta: "),
                          numero_piante=input("Numero di piante:"))
        add_settore = input("Aggiungere una coltivazione? [y/n]")
        if add_settore == "y":
            settore.__aggiungi_coltivazione__()
            self.lista_settori.append(settore)
        elif add_settore == "n":
            print("Settore aggiunto senza coltivazione")
            self.lista_settori.append(settore)
        else:
            print("input non valido")

    def __start__(self):
        # inizia irrigazione
        print("inizio ciclo irrigazione")

        for settore in self.lista_settori:
            litri_totali = settore.numero_piante * settore.litri_pianta_su_irrigatore
            tempo_pompa = litri_totali / self.portata_pompa
            print("irrigo settore: " + settore.nome)
            # apri valvole del settore
            tempo_secondi = tempo_pompa * 60
            time.sleep(tempo_secondi)
            print("fine irrigazione settore: " + settore.nome)
    def __stop__(self):
        for settore in self.lista_settori:
            print("chiudo settore: " + settore.nome)

    def __start_forzato__(self):
        # start forzato irrigazione
        print("start forzato")

    def __stop_forzato__(self):
        # stop forzato
        print("stop forzato ciclo")
