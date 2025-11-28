import sqlite3
import os
from models import Patient, Taak

# Assigns the desired database folder, file and full path to a variable
db_path = "data"
db_file = "task_manager.db"

#Testdb
#db_path ="test/data"
#db_file = "test_tasks.db"

db_full_path = os.path.join(db_path, db_file)


# Defines a function with which we can initialize the database
def initialize_db():
    # If the directory "data" doesn't exist it should first be created
    if not os.path.exists(db_path):
        os.makedirs(db_path, exist_ok=True)

    # Create a database if it doesn't exist yet and connect it.
    # Then create a cursor object
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


# Defines a function to add a patient to the database
def add_patient(naam, geboorte_datum, telefoon, opmerkingen="/"):

    # Makes sure the database and tables exist
    initialize_db()

    # Insert the values into the table if patient doesn't exist yet
    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()

        # Does the patient exist?
        check_query = """
        SELECT id
        FROM patienten
        WHERE naam = ? AND geboorte_datum = ?
        """

        check_values = (naam, geboorte_datum)

        my_cursor.execute(check_query, check_values)

        existing_patient = my_cursor.fetchone()

        # If the patient already exists, the id of the existing one is returned
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

            my_cursor.execute(query, input_values)
            db.commit()

            # With INTEGER PRIMARY KEY for id an integer id was automatically created by SQLite
            # Lastrowid returns the id
            return my_cursor.lastrowid


# Defines a function to update a patient. Only the selected fields will be updated
def update_patient(id, naam=None, geboorte_datum=None, telefoon=None, opmerkingen=None):

    # Makes sure the database and tables exist
    initialize_db()

    # Update the table patienten for a given id
    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()

        # 1. Select the row from the database you want to update
        query_select = """
        SELECT naam, geboorte_datum, telefoon, opmerkingen
        FROM patienten
        WHERE id= ?
        """

        input_value = (id,)

        my_cursor.execute(query_select, input_value)

        selected_row = my_cursor.fetchone()

        if selected_row is None:
            print("Geen patient gevonden met dit id!")
            return None

        # 2. Fill in the new updated values
        current_naam = selected_row[0]
        current_geboorte_datum = selected_row[1]
        current_telefoon = selected_row[2]
        current_opmerkingen = selected_row[3]

        if naam is None:
            new_naam = current_naam
        else:
            new_naam = naam

        if geboorte_datum is None:
            new_geboorte_datum = current_geboorte_datum
        else:
            new_geboorte_datum = geboorte_datum

        if telefoon is None:
            new_telefoon = current_telefoon
        else:
            new_telefoon = telefoon

        if opmerkingen is None:
            new_opmerkingen = current_opmerkingen
        else:
            new_opmerkingen = opmerkingen

        # 3. Update the database entry
        query_update = """
        UPDATE patienten
        SET naam = ?,
            geboorte_datum = ?,
            telefoon =?,
            opmerkingen =?
        WHERE id = ?
        """

        update_values = (new_naam, new_geboorte_datum,
                         new_telefoon, new_opmerkingen, id)

        my_cursor.execute(query_update, update_values)

        db.commit()


# Defines a function to get all patient entries from the database and return them as a list of patient objects
def get_all_patients():

    # Makes sure the database and tables exist
    initialize_db()

    # Select all patient entries, fetch them and return them as a list of patient objects

    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()
        query = """
        SELECT id, naam, geboorte_datum, telefoon, opmerkingen FROM patienten
        """

        my_cursor.execute(query)
        rows = my_cursor.fetchall()

        patients = []
        for row in rows:
            id = row[0]
            naam = row[1]
            geboorte_datum = row[2]
            telefoon = row[3]
            opmerkingen = row[4]

            pt = Patient(id, naam, geboorte_datum, telefoon, opmerkingen)
            patients.append(pt)

        return patients


# Defines a function to add a task to the database
def add_task(patient_id, omschrijving, datum_aanmaak, deadline, prioriteit="normaal", status="lopende", voltooid_op="niet voltooid", opmerkingen_afhandeling="/"):

    # Makes sure the database and tables exist
    initialize_db()

    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()

        # Check if task doesnt exist yet
        check_query = """
        SELECT id
        FROM taken
        WHERE patient_id = ? AND datum_aanmaak = ? AND omschrijving = ?
        """

        check_values = (patient_id, datum_aanmaak, omschrijving)
        my_cursor.execute(check_query, check_values)
        existing_task = my_cursor.fetchone()

        # If the task exists return its id
        if existing_task is not None:
            print('Deze taak werd reeds ingevoerd.')
            return existing_task[0]
        # If the task doesnt exist, created it and return its id
        else:
            query = """
            INSERT INTO taken (patient_id, omschrijving, datum_aanmaak, deadline, prioriteit, status, voltooid_op, opmerkingen_afhandeling)
            VALUES (?,?,?,?,?,?,?,?)
            """
            input_values = (patient_id, omschrijving, datum_aanmaak, deadline,
                            prioriteit, status, voltooid_op, opmerkingen_afhandeling)

            my_cursor.execute(query, input_values)

            db.commit()

            # With INTEGER PRIMARY KEY for id an integer id was automatically created by SQLite
            # Lastrowid returns the id
            return my_cursor.lastrowid

# Defines a function to update a task


def update_task(id, patient_id, omschrijving, datum_aanmaak, deadline, prioriteit="normaal", status="lopende", voltooid_op="niet voltooid", opmerkingen_afhandeling="/"):

    # Makes sure the database and tables exist
    initialize_db()

    # Update the table taken for a given id
    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()

        query = """
        UPDATE taken
        SET patient_id = ?,
            omschrijving = ?,
            datum_aanmaak = ?,
            deadline = ?,
            prioriteit = ?,
            status = ?,
            voltooid_op = ?,
            opmerkingen_afhandeling = ?
        WHERE id = ?
        """

        input_values = (
            patient_id,
            omschrijving,
            datum_aanmaak,
            deadline,
            prioriteit,
            status,
            voltooid_op,
            opmerkingen_afhandeling,
            id,
        )

        my_cursor.execute(query, input_values)
        db.commit()


# Defines a function to get all tasks for a patient from the database and return them as a list of task objects
def get_all_tasks_for_patient(patient_id):

    # Makes sure the database and tables exist
    initialize_db()

    # Select all task entries for a patient, fetch them and return them as a list of task objects

    with sqlite3.connect(db_full_path) as db:
        my_cursor = db.cursor()
        query = """
        SELECT id, patient_id, omschrijving, datum_aanmaak,
        deadline, prioriteit, status, voltooid_op, opmerkingen_afhandeling
        FROM taken
        WHERE patient_id = ?
        """

        my_cursor.execute(query, (patient_id,))
        rows = my_cursor.fetchall()

        tasks = []
        for row in rows:
            id = row[0]
            patient_id = row[1]
            omschrijving = row[2]
            datum_aanmaak = row[3]
            deadline = row[4]
            prioriteit = row[5]
            status = row[6]
            voltooid_op = row[7]
            opmerkingen_afhandeling = row[8]

            taak = Taak(
                id,
                patient_id,
                omschrijving,
                datum_aanmaak,
                deadline,
                prioriteit,
                status,
                voltooid_op,
                opmerkingen_afhandeling,
            )
            tasks.append(taak)

        return tasks


# Testing the code
if __name__ == "__main__":
    
    initialize_db()
    print(
        f"Het databasebestand {db_file} en tabellen zijn aangemaakt in map: {db_path} ")

    # Test: Add a patient
    a = add_patient("Patient Zero", "1950-01-01", "0123456789", "mut in orde")
    b = add_patient("Patient One", "1970-10-01", "987654321", "ocmw patient")
    c = add_patient("Patient Two", "2010-12-01","22244442222555", "fedasil patient")

    # Test: Add a task for some patients
    d = add_task(
        patient_id=a,
        omschrijving="Verwijsbrief cardiologie maken",
        datum_aanmaak="2025-11-22",
        deadline="2025-11-30",
        prioriteit="hoog",
    )
    print(f"Taak {d} toegevoegd voor patiënt {a}\n")

    e = add_task(
        patient_id=b,
        omschrijving="Document FOD Handicap invullen",
        datum_aanmaak="2025-11-27",
        deadline="2025-12-15",
        prioriteit="normaal",
    )
    print(f"Taak {e} toegevoegd voor patiënt {b}\n")

    f = add_task(
        patient_id=c,
        omschrijving="Afspraak dermatologie maken",
        datum_aanmaak="2025-11-28",
        deadline="2025-12-30",
        prioriteit="laag",
    )
    print(f"Taak {f} toegevoegd voor patiënt {c}\n")

    # Test: Get and print all patient entries

    patients = get_all_patients()
    for p in patients:
        print(p)

    # Test: Get and print all tasks for this patient
    print("Alle taken voor patiënt a")
    tasks = get_all_tasks_for_patient(a)
    for t in tasks:
        print(t)

    print("Alle taken voor patiënt b")
    tasks = get_all_tasks_for_patient(b)
    for t in tasks:
        print(t)

    print("Alle taken voor patiënt c")
    tasks = get_all_tasks_for_patient(c)
    for t in tasks:
        print(t)

    # Test: update telefoon and opmerkingen for patient a and check change in patient entries
    print(f"Alle patienten met update van gegevens voor patiënt met id {a} (voor de velden telefoon, opmerkingen)")
    update_patient(id=a, telefoon="098666664321", opmerkingen="Geen geldige mutualiteit meer")
    patients = get_all_patients()
    for p in patients:
        print(p)

