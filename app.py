import datetime

has_excepted = False
print("Calcolo tempo pompa v1.0")
choice = ""

while True:

    try:
        print("--------------------------------------------------------------")
        print("Inserire i dati relativi all'impianto")
        litri_minuto_pompa = int(input("Litri al minuto pompa: "))
        litri_minuto_irrigatore = int(input("Litri al minuto irrigatore: "))
        num_irrigatori_per_pianta = int(input("Numero irrigatori per pianta: "))
        num_piante = int(input("Numero di piante:"))
        litri_richiesti_per_pianta = int(input("Litri richiesti per pianta: "))

        litri_irrigatore_per_pianta = (litri_richiesti_per_pianta / num_irrigatori_per_pianta)
        litri_totali = num_piante * litri_irrigatore_per_pianta
        tempo_pompa = litri_totali / litri_minuto_pompa

        print("la pompa deve rimanere attiva per " + str(datetime.timedelta(minutes=tempo_pompa)) + " (hh:mm:ss)")

    except:
        choice = input("Input errato, premi INVIO per riprovare o digita Q per uscire.")

    if choice.lower() == "q":
        # break or return or..
        import sys

        sys.exit(0)
