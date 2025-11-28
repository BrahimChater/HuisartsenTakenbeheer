from app import db #Uses the db module from the app package


#Shows the main menu on the screen
def toon_menu():
    print("\n====================================") 
    print("\n     Takenmanager huisartsenpraktijk    ")
    print("\n====================================") 


#    print("1. Toon alle patiënten")
#    print("2. Nieuwe patiënt toevoegen")
#    print("3. Toon alle taken")
#    print("4. Nieuwe taak toevoegen")
#    print("5. Patiëntgegevens aanpassen")
#    print("6. Taak aanpassen")
#    print("7. Exporteer alle openstaande taken naar csv")
#    print("0. Afsluiten")





# Defines a main function to run the program
def main():
    print("========= Welkom in de takenbeheertool =========")
    
    # Make sure the database and its tables exists
    db.initialize_db()
    print(f"\n*** Database is geïnitialiseerd ***\n")




if __name__ == "__main__":
    main()
    