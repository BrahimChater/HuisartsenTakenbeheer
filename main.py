from app import db #Uses the db module from the app package


#Shows the main menu on the screen
def toon_menu():
    print("\n===========================================") 
    print("\n      Takenmanager huisartsenpraktijk    ")
    print("\n===========================================\n") 


    print("\n1. Toon alle patiënten")
#    print("2. Nieuwe patiënt toevoegen")
#    print("3. Toon alle taken")
#    print("4. Nieuwe taak toevoegen")
#    print("5. Patiëntgegevens aanpassen")
#    print("6. Taak aanpassen")
#    print("7. Exporteer alle openstaande taken naar csv")
#    print("0. Afsluiten\n")
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
            else:
                break
        else:
            print("\nOngeldige keuze ingegeven. Probeer opnieuw!")
    


if __name__ == "__main__":
    main()
    