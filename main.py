from app import db #Uses the db module from the app package


#Shows the main menu on the screen
def toon_menu():
    print("\n===========================================") 
    print("\n      Takenmanager huisartsenpraktijk    ")
    print("\n===========================================\n") 


    print("1. Toon alle patiënten")
    print("2. Nieuwe patiënt toevoegen")
    print("3. Toon alle taken")
#    print("4. Nieuwe taak toevoegen")
#    print("5. Patiëntgegevens aanpassen")
#    print("6. Taak aanpassen")
#    print("7. Exporteer alle openstaande taken naar csv")
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
def add_new_patient():
    print("\nVul de gegevens van de patiënt in: ")
    
    naam = input("\nGeef de naam van de patiënt op: ")
    naam = naam.strip().title()
    if naam =="":
        print("Ongeldige naam opgegeven. Begin opnieuw.")
        return
    
    geboorte_datum = input("Geef de geboortedatum van de patiënt (YYYY-MM-DD): ")
    geboorte_datum = geboorte_datum.strip()
    if geboorte_datum =="":
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
    
        #Depening on the input a different function/ action will be executed
        if keuze.isnumeric():
            if keuze == "1":
                toon_alle_patienten()
            elif keuze == "2":
                add_new_patient()
            elif keuze == "3":
                toon_alle_taken()
            elif keuze =="0":
                print("\nProgramma wordt afgesloten.")
                break
            else:
                print("\nGeef een geldig getal op!")
        else:
            print("\nOngeldige keuze ingegeven. Probeer opnieuw!")
    


if __name__ == "__main__":
    main()
    