from app import db #Uses the db module from the app package
from datetime import datetime


#Shows the main menu on the screen
def toon_menu():
    print("\n===========================================") 
    print("\n      Takenmanager huisartsenpraktijk    ")
    print("\n===========================================\n") 


    print("1. Toon alle patiënten")
    print("2. Nieuwe patiënt toevoegen")
    print("3. Toon alle taken")
    print("4. Nieuwe taak toevoegen")
    print("5. Patiëntgegevens aanpassen")
#    print("6. Taak aanpassen")
    print("7. Exporteer alle openstaande taken naar csv")
    print("8. Vind uniek patiëntnummer obv patiëntnaam")
    print("0. Afsluiten\n")
    print("\nMaak een keuze")




# Function to display all the patients from the database and display them
def toon_alle_patienten():
    patienten = db.get_all_patients()
    if not patienten:
        print("\nEr staan nog geen patienten in de database!")
    else:
        print("\nOverzicht van alle patienten in de database:\n")
        for p in patienten:
            print(p)
            print("\n" + "-" * 36 +"\n")
            
#Funcion to add a new patient to the database
def toevoegen_nieuwe_patient():
    print("\nVul de gegevens van de patiënt in: ")
    
    #Making sure all the input is valid, if not start over
    naam = input("\nGeef de naam van de patiënt op: (familienaam voornaam) ")
    naam = naam.strip().title()
    if naam =="":
        print("Ongeldige naam opgegeven. Begin opnieuw.")
        return
    
    geboorte_datum = input("Geef de geboortedatum van de patiënt (YYYY-MM-DD): ")
    geboorte_datum = geboorte_datum.strip()
    if geboorte_datum =="":
        print("Ongeldige geboortedatum opgegeven. Begin opnieuw.")
        return
    else:
        try:
            datetime.strptime(geboorte_datum, "%Y-%m-%d")
        except ValueError:
            print("Ongeldige geboortedatum opgegeven. Begin opnieuw.")
            return
        
    telefoon = input("Geef het telefoonnummer van de patiënt op: ")
    telefoon = telefoon.strip()
    if telefoon =="":
        print("Ongeldig nummer opgegeven. Begin opnieuw.")
        return
    
    opmerkingen = input("Geef eventuele bijkomende info over de patiënt op: ")
    opmerkingen = opmerkingen.strip()
    if opmerkingen =="":
        opmerkingen ="/"
    
    patient_id = db.add_patient(naam, geboorte_datum, telefoon, opmerkingen)
    print(f"\nPatiënt werd toegevoegd (of bestond al) met id: {patient_id}\n")
    
#Function to show all tasks
def toon_alle_taken():
    alle_taken = db.get_all_tasks()
    if alle_taken:
        for t in alle_taken:
            print(t)
    else:
        print("\nEr zitten nog geen taken in de database")

#Function to add a new task to the database
def nieuwe_taak_toevoegen(): 
    print("\nVul de gegevens voor de taak in: ")
    
    #Making sure all the input is valid, if not start over or default
    patient_id = input("\nGeef het uniek nummer van de patiënt op: ")
    patient_id = patient_id.strip()
    if patient_id =="" or not patient_id.isnumeric():
        print("Ongeldig nummer opgegeven. Begin opnieuw.")
        return
    patient_id = int(patient_id)
    
    omschrijving = input("Geef een omschrijving van de taak: ")
    omschrijving = omschrijving.strip()
    if omschrijving =="":
        print("Ongeldige omschrijving opgegeven. Begin opnieuw.")
        return
    
    datum_aanmaak = datetime.today().strftime("%Y-%m-%d")
    
    deadline = input("Geef een deadline op in de vorm van YYYY-MM-DD:\n ")
    deadline = deadline.strip()
    try: 
        datetime.strptime(deadline,"%Y-%m-%d")
    except ValueError:
        print("Ongeldige deadline opgegeven. Begin opnieuw.")
        return
    
    prioriteit = input("Stel een prioriteit in: hoog, normaal, laag\n")
    prioriteit = prioriteit.strip().lower()
    if prioriteit not in ("hoog","laag","normaal"):
        prioriteit ="normaal"
        print("Ongeldige prioriteit opgegeven. De prioriteit wordt ingesteld op normaal!")
    
    status = "lopende"
    
    voltooid_op ="niet voltooid"
    
    opmerkingen_afhandeling = input("Geef eventuele bijkomende info op: ")
    opmerkingen_afhandeling = opmerkingen_afhandeling.strip()
    if opmerkingen_afhandeling =="":
        opmerkingen_afhandeling ="/"
    
    taak_id = db.add_task(patient_id, omschrijving, datum_aanmaak, deadline, prioriteit, status, voltooid_op,opmerkingen_afhandeling)
    print(f"\nTaak werd toegevoegd (of bestond al) met het unieke nummer: {taak_id}\n")

#Function to adjust patient data
def patient_aanpassen():
    
    print("\nU kan hier de patiëntgegevens aanpassen")
    
    patient_id = input("Geef het uniek patiëntnummer van de patiënt die u wil aanpassen: ")
    patient_id = patient_id.strip()
    if patient_id == "" or not patient_id.isnumeric():
        print("Ongeldig patiëntnummer.")
        return
    patient_id = int(patient_id)

    print("\nGeef niets op als u niets wil wijzigen.\n")
    nieuwe_naam = input("Nieuwe naam (familienaam voornaam): ")
    nieuwe_naam= nieuwe_naam.strip().title()
    if nieuwe_naam == "":
        nieuwe_naam = None

    nieuwe_geboorte_datum = input("Nieuwe geboortedatum (YYYY-MM-DD, leeg = geen wijziging): ")
    nieuwe_geboorte_datum = nieuwe_geboorte_datum.strip()
    if nieuwe_geboorte_datum == "":
        nieuwe_geboorte_datum = None
    else:
        try:
            datetime.strptime(nieuwe_geboorte_datum, "%Y-%m-%d")
        except ValueError:
            print("Ongeldige geboortedatum. Wijziging geboortedatum niet doorgevoerd.")
            nieuwe_geboorte_datum = None

    nieuwe_telefoon = input("Nieuw telefoonnummer (leeg = geen wijziging): ")
    nieuwe_telefoon = nieuwe_telefoon.strip()
    if nieuwe_telefoon == "":
        nieuwe_telefoon = None

    nieuwe_opmerkingen = input("Nieuwe opmerkingen (leeg = geen wijziging): ")
    nieuwe_opmerkingen=nieuwe_opmerkingen.strip()
    if nieuwe_opmerkingen == "":
        nieuwe_opmerkingen = None

    db.update_patient(
        id=patient_id,
        naam=nieuwe_naam,
        geboorte_datum=nieuwe_geboorte_datum,
        telefoon=nieuwe_telefoon,
        opmerkingen=nieuwe_opmerkingen,
    )

    print(f"\nPatiënt met nummer {patient_id} werd bijgewerkt.\n")
    
    
#Function to adjust task data
#def taak_aanpassen():
    
#Function to export all current tasks to csv-file
def openstaande_taken_naar_csv():
    print("\nWe gaan de openstaande taken exporteren als csv-bestand")
    export_path = input("Geef een path op waarnaar je het csv-bestand wil exporteren:\n")
    export_path = export_path.strip()
    if export_path =="":
        db.export_open_tasks_to_csv()
    else:
        db.export_open_tasks_to_csv(export_path)
    
    
#Function to get the patient_id based on his or her name
def vind_patientnummer_obv_naam():
    naam = input("Geef de naam van de patient (of een deel ervan) op (bij voorkeur familienaam voornaam): ")
    naam = naam.strip()
    if naam =="":
        print("Geef een geldige naam op")
        return
    
    patients_found = db.get_patients_by_name(naam)
    if not patients_found:
        print("Geen patiënten gevonden met deze naam")
    elif len(patients_found) ==1:
        pt = patients_found[0]
        print("Eén patiënt gevonden:")
        print(pt)
        print(f"Uniek patiëntnummer is: {pt.id}")
    else:
        print("Meerdere patiënten teruggevonden:")
        for pt in patients_found:
            print(pt)
            print(f"Uniek patiëntnummer is: {pt.id}")
            print("-"*35)
            
        
# Defines a main function to run the program
def main():
    print("========= Welkom in de takenbeheertool =========")
    
    # Make sure the database and its tables exists
    db.initialize_db()
    print(f"\n*** Database is geïnitialiseerd ***\n")
    
    
    #Create a loop to show the main menu
    while True:    
        toon_menu()
        
        keuze = input("\nGeef het getal hier in:  ")
        keuze = keuze.strip()
    
        #Depending on the input a different function/ action will be executed
        if keuze.isnumeric():
            if keuze == "1":
                toon_alle_patienten()
            elif keuze == "2":
                toevoegen_nieuwe_patient()
            elif keuze == "3":
                toon_alle_taken()
            elif keuze == "4":
                nieuwe_taak_toevoegen()
            elif keuze == "5":
                patient_aanpassen()
           # elif keuze == "6":
           #     taak_aanpassen()
            elif keuze == "7":
                openstaande_taken_naar_csv()
            elif keuze == "8":
                vind_patientnummer_obv_naam()
            elif keuze =="0":
                print("\nProgramma wordt afgesloten.")
                break
            else:
                print("\nGeef een geldig getal op!")
        else:
            print("\nOngeldige keuze ingegeven. Probeer opnieuw!")
    


if __name__ == "__main__":
    main()
    