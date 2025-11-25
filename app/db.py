import sqlite3
import os


# Assigns the desired database folder, file and full path to a variable
db_path = "data"
db_file = "tasks.db"
db_full_path = os.path.join(db_path, db_file)


# Defines a function with which we can initialize the database
def initialize_db():
    # If the directory "data" doesn't exist it should first be created
    if not os.path.exists(db_path):
        os.makedirs(db_path, exist_ok=True)
    
    #Create a database if it doesn't exist yet and connect it. 
    #Then create a cursor object
    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()
    
        # Query to create a table "patienten" in the database
        query_pt = """
        CREATE TABLE IF NOT EXISTS patienten (
            id INTEGER PRIMARY KEY,
            naam TEXT NOT NULL,
            geboorte_datum TEXT NOT NULL,
            telefoon TEXT,
            opmerkingen TEXT
            )
        """
        
        # Create the table "patienten"
        my_cursor.execute(query_pt)
    
        # Query to create a table "taken" in the database
        query_taken = """
        CREATE TABLE IF NOT EXISTS taken (
            id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL,
            omschrijving TEXT NOT NULL,
            datum_aanmaak TEXT,
            prioriteit TEXT DEFAULT 'normaal',
            deadline TEXT,
            status TEXT NOT NULL DEFAULT 'lopende',
            voltooid_op TEXT,
            opmerkingen_afhandeling TEXT,
            FOREIGN KEY(patient_id)
            REFERENCES patienten(id)
            )
        """
        
        # Create the table "taken"
        my_cursor.execute(query_taken)
        # Commit the changes to the database     
        db.commit()
        

if __name__ == "__main__":
    initialize_db()
    print(f"Het databasebestand {db_file} en tabellen zijn aangemaakt in map: {db_path} ")