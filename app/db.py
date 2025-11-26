import sqlite3
import os
from models import Patient

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
        

#Defines a function to add a patient to the database
def add_patient(naam, geboorte_datum, telefoon, opmerkingen="/"):
    
    #Makes sure the database and tables exist
    initialize_db()
    
    #Insert the values into the table if patient doesn't exist yet
    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()
        
        
        #Does the patient exist?
        check_query = """
        SELECT id
        FROM patienten
        WHERE naam = ? AND geboorte_datum = ?
        """
        
        check_values = (naam, geboorte_datum)
        
        my_cursor.execute(check_query,check_values)
        
        existing_patient = my_cursor.fetchone()
        
        #If the patient already exists, the id of the existing one is returned
        if existing_patient is not None:
            print("Deze patient zit al in de database! Er wordt niks toegevoegd.")
            return existing_patient[0]
        
        # If the patient doesn't exist then a new entry is created and its id returned
        else:         
             query = """
             INSERT INTO patienten (naam, geboorte_datum, telefoon, opmerkingen)
             VALUES (?,?,?,?)
             """
        
             input_values = (naam, geboorte_datum, telefoon, opmerkingen)
        
             my_cursor.execute(query,input_values)
             db.commit()
        
             #With INTEGER PRIMARY KEY for id an integer id was automatically created by SQLite
             # Lastrowid returns the id
             return my_cursor.lastrowid



#Defines a function to get all patient entries from the database and return them as a list of patient objects
def get_all_patients():
    
    #Makes sure the database and tables exist
    initialize_db()
    
    #Select all patient entries, fetch them and return them as a list of patient objects
    
    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()
        query="""
        SELECT id, naam, geboorte_datum, telefoon, opmerkingen FROM patienten
        """
        
        my_cursor.execute(query)
        rows = my_cursor.fetchall()
        
        patients=[]
        for row in rows:
            id = row[0]
            naam = row[1]
            geboorte_datum = row[2]
            telefoon = row[3]
            opmerkingen = row[4]
            
            pt = Patient(id,naam, geboorte_datum,telefoon,opmerkingen)
            patients.append(pt)
        
        return patients
        
#Defines a function to add a task to the database
def add_task(patient_id, omschrijving, datum_aanmaak, deadline, prioriteit="normaal", status="lopende", voltooid_op="niet voltooid", opmerkingen_afhandeling="/"):
    
    #Makes sure the database and tables exist
    initialize_db()
    
    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()
        
        #Check if task doesnt exist yet
        check_query="""
        SELECT id
        FROM taken
        WHERE patient_id = ? AND datum_aanmaak = ? AND omschrijving = ? 
        """
        
        check_values = (patient_id, datum_aanmaak, omschrijving)
        my_cursor.execute(check_query,check_values)
        existing_task = my_cursor.fetchone()
        
        #If the task exists return its id
        if existing_task is not None:
            print('Deze taak werd reeds ingevoerd.')
            return existing_task[0]
        #If the task doesnt exist, created it and return its id
        else:
            query ="""
            INSERT INTO taken (patient_id, omschrijving, datum_aanmaak, deadline, prioriteit, status, voltooid_op, opmerkingen_afhandeling)
            VALUES (?,?,?,?,?,?,?,?)
            """
            input_values = (patient_id, omschrijving, datum_aanmaak,deadline,prioriteit,status,voltooid_op,opmerkingen_afhandeling)
            
            my_cursor.execute(query, input_values)
            
            db.commit()
            
            #With INTEGER PRIMARY KEY for id an integer id was automatically created by SQLite
            # Lastrowid returns the id
            return my_cursor.lastrowid
            

# Testing the code
if __name__ == "__main__":
    initialize_db()
    print(f"Het databasebestand {db_file} en tabellen zijn aangemaakt in map: {db_path} ")
    
    # Test: Add a patient
    add_patient("Patient Zero", "1950-01-01", "0123456789","Test Patient")
    
    #Test: Get and print all patient entries
    
    patients = get_all_patients()
    for p in patients:
        print(p)
    
    
    
    
    
    
    