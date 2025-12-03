# Python CLI Application: TAKENBEHEER HUISARTSENPRAKTIJK

(FOR DUTCH version: see README.md)

---

## GENERAL DESCRIPTION

This small command-line tool is used to track and follow up outstanding tasks per patient in a GP (family doctor) practice (e.g. creating documents, following up lab results, referrals, phone calls to be made, …).

---

## PURPOSE OF THE APPLICATION

- Register new tasks per patient  
- Track deadlines and priority (high / normal / low)  
- Show an overview of all tasks  
- Show only open (ongoing) tasks  
- Export all open tasks to a CSV file  
- Edit and complete existing tasks  
- Add notes to patients and to tasks  
- Add new patients  
- Update patient information  

---

## FUNCTIONALITY (MAIN MENU OPTIONS)

When the application starts, the following menu is shown:

1. "Toon alle patiënten"  
   Shows all patients in the database, with:
   - ID  
   - Name  
   - Date of birth  
   - Phone number  
   - Notes  

2. "Nieuwe patiënt toevoegen"    
   Prompts for:
   - Name (last name + first name)  
   - Date of birth ("YYYY-MM-DD")  
   - Phone number  
   - Optional notes (e.g. insurance details or other points of attention)  

   The patient is stored in the "patienten" table.  
   If a patient with the same combination of "name" + "date of birth" already exists, no new patient is created.

3. "Toon alle taken"  
   Shows all tasks from the "taken" table (regardless of status).  
   The list is sorted by deadline (earliest date first).  
   For each task, the patient is shown first, then the task details:
   - Task ID  
   - Patient ID  
   - Description  
   - Created on  
   - Deadline  
   - Priority  
   - Status  
   - Completed on  
   - Notes / handling  

4. "Toon alle openstaande taken"
   Shows only tasks with status "lopende" (“ongoing”), sorted by deadline (earliest first).  
   For each task, the patient name with ID is shown first, then the task details.

5. "Nieuwe taak toevoegen"  
   Prompts for:
   - Existing patient number ("patient_id")  
   - Task description  
   - Deadline ("YYYY-MM-DD")  
   - Priority (high / normal / low, default = normal)  
   - Optional notes, mainly for follow-up and conclusions  

   The creation date is set automatically to today ("YYYY-MM-DD").  
   The default status is "lopende" (“ongoing”), and "voltooid_op" is set to "niet voltooid" (“not completed”).

   The code checks:
   - Whether a patient with this "id" exists; if not, the task is not added.  
   - Whether there is already a task with the same "patient_id" + "datum_aanmaak" + "omschrijving"; if so, the existing task ID is returned.

6. "Patiëntgegevens aanpassen"   
   Asks for an existing patient number and then allows (optionally) editing of:
   - Name  
   - Date of birth  
   - Phone number  
   - Notes  

   Fields left empty are left unchanged.

7. "Taak aanpassen"  
   Asks for an existing task number and then allows (optionally) editing of:
   - Description  
   - Deadline  
   - Priority (high / normal / low)  
   - Status (ongoing / completed)  
   - Notes / handling  

   When the status is changed:
   - To "afgewerkt" (“completed”): "voltooid_op" is automatically set to today’s date.  
   - To "lopende" (“ongoing”): "voltooid_op" is reset to "niet voltooid" (“not completed”).

8. "Exporteer alle openstaande taken naar CSV"  
   Optionally asks for a file name (without extension, optionally including a folder).  
   - No file name given: export goes to the default location from "settings.py"  
     (or to "export/open_taken.csv" if "settings.py" is not found).  
   - File name given:  
     - Name with folder: export to "<given_folder/given_name>.csv". The folder is created if it does not exist.  
     - Name without folder: export to "<given_name>.csv" in the project root folder where you run "python main.py".  

   The CSV contains:
   - Task ID  
   - Patient name  
   - Patient ID  
   - Description  
   - Created on  
   - Deadline  
   - Priority  
   - Notes / handling  

9. "Zoek patiënt en diens uniek patiëntnummer obv de naam"
   Prompts for (part of) the patient name.  
   Performs a case-insensitive search in the "patienten" table and:
   - Shows “No patients found” if there is no match;  
   - Shows the patient data and unique patient number if there is exactly one match;  
   - Shows a list of all matches (with their ID) if multiple patients are found.

0. "Afsluiten" 
   Exits the program.

---

## PROJECT STRUCTURE (FOLDERS AND FILES)

Main files and folders:

- "main.py"  
  Main script of the application. Shows the menu, reads user input and calls functions from the "app.db" module.

- "app/" (package)  
  - "__init__.py"  
    Marks "app" as a Python package.  
  - "db.py"  
    Data Access Layer (DAL). Contains logic for:
    - Initialising the SQLite database  
    - Adding / updating patients  
    - Adding / updating tasks  
    - Retrieving patients and tasks  
    - Retrieving open tasks  
    - Exporting to CSV  
  - "models.py"  
    Domain layer with simple classes:
    - "Patient"  
    - "Taak"  
    These classes represent database rows. They implement a "__str__" method so instances print nicely in the terminal.

- "example_settings.py"  
  Example configuration file, showing how to set up "settings.py":

  ```python
  # Example configuration for the tool GP Practice Task Manager

  # Folder where the SQLite database will be stored
  db_set_dir = "data"

  # SQLite database filename
  db_set_file = "task_manager.db"

  # Default folder for CSV exports
  export_set_dir = "export"
  ```

### Important variables in "settings.py"

Note: "settings.py" should be placed in the same folder as "main.py".

- "db_set_dir"  
  Folder where the database is stored (default: "data").

- "db_set_file"  
  Database file name (default: "task_manager.db").

- "export_set_dir"  
  Default folder for CSV exports (default: "export").

At initialisation:

- If "settings.py" exists, these values are read from "settings.py".  
- If "settings.py" does not exist, the defaults in "app/db.py" are used:
  - "data" as the data folder  
  - "task_manager.db" as the database file name  
  - "export" as the export folder  

The database contains two tables:

- "patienten"  
- "taken"  

They are automatically created by "initialize_db()" in "app/db.py" if they do not yet exist.

---

## INSTALLATION AND USAGE

The steps below show how to set up the application in a fresh environment.

1. Clone the repository

```bash
git clone https://github.com/BrahimChater/HuisartsenTakenbeheer.git
cd HuisartsenTakenbeheer
```

2. Create and activate a virtual environment

*Windows – PowerShell*

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*Windows – Command Prompt (cmd)*

```bash
python -m venv .venv
.\.venv\Scripts\activate.bat
```

*Unix (macOS / Linux)*

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install required packages

```bash
pip install -r requirements.txt
```

This tool only uses Python’s standard library. No extra third-party packages need to be installed  
(see "requirements.txt" for completeness).

4. Create the settings file

Based on the example file "example_settings.py", create the local settings file:

*Windows (PowerShell) / macOS / Linux*

```bash
cp example_settings.py settings.py
```

*Windows (Command Prompt)*

```bash
copy example_settings.py settings.py
```

If desired, adjust "db_set_dir", "db_set_file" or "export_set_dir" in "settings.py"  
(for example, if the database or export files should live elsewhere).

5. Prepare the database

5.1. Make sure the folder from "db_set_dir" exists (default: "data/").  
   If it does not exist, it will be created automatically when the application starts.  
5.2. Place the provided example database file in this folder, using exactly the same name as "db_set_file"  
   (default: "task_manager.db").

With the default settings, the structure should look something like this:

projectroot/
├─ main.py
├─ app/
│  ├─ __init__.py
│  ├─ db.py
│  └─ models.py
├─ example_settings.py
├─ settings.py
├─ requirements.txt
├─ data/
│  └─ task_manager.db
└─ export/


Note: the "export/" folder is created automatically on the first CSV export, unless the user specifies another location.

6. Start the application

Activate the virtual environment and run, from the project root:

```bash
python main.py
```

The main menu will be shown in the terminal and you can use all available functionality.  
After each action, you are prompted to press Enter to return to the main menu.
