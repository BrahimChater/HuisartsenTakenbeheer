# Python CLI Applicatie: TAKENBEHEER HUISARTSENPRAKTIJK

(FOR ENGLISH version: see README_en.md)

---

## ALGEMENE OMSCHRIJVING

Deze kleine tool dient om per patiënt openstaande taken (bijv. opmaken documenten, opvolging labo's, verwijzingen, te plegen telefoons, ...)  bij te houden en op te volgen in een huisartsenpraktijk.

---

## DOEL VAN DE APPLICATIE

- Registreren van nieuwe taken per patiënt
- Bijhouden van deadlines en prioriteit (hoog/ normaal /laag)
- Weergeven van een overzicht van alle taken
- Weergeven van enkel de openstaande (lopende) taken
- Exporteren van een overzicht van alle openstaande taken naar een CSV-bestand
- Aanpassen en afvinken van bestaande taken 
- Toevoegen van opmerkingen bij patiënten en bij taken
- Nieuwe patiënten toevoegen
- Updaten van patiëntinformatie

---

## FUNCTIONALITEITEN (OPTIES IN HET HOOFDMENU):

Bij het starten van de applicatie verschijnt een menu met volgende opties:

1. "Toon alle patiënten"  
   Toont alle patiënten in de database, met ID, naam, geboortedatum, telefoonnummer en opmerkingen.

2. "Nieuwe patiënt toevoegen"  
   Vraagt:
   - naam (familienaam voornaam)
   - geboortedatum ("YYYY-MM-DD")
   - telefoonnummer  
   - optionele opmerkingen (bijv. verzekerbaarheid of andere aandachtspunten) 

   De patiënt wordt opgeslagen in de tabel "patienten".  
   Als dezelfde combinatie van naam + geboortedatum al bestaat, wordt er geen nieuwe patiënt aangemaakt.

3. "Toon alle taken"  
   Toont alle taken uit de tabel "taken" (ongeacht status).
   De lijst wordt gesorteerd op deadline (vroegste datum eerst).
   Voor elke taak wordt eerst de patiënt getoond.
   Daarna volgen de taakgegevens:
   - taaknummer (ID)
   - patiënt-ID
   - omschrijving
   - datum aanmaak
   - deadline
   - prioriteit
   - status
   - voltooid op
   - opmerkingen/afhandeling

4. "Toon alle openstaande taken"
   Toont enkel de taken met status "lopende", gesorteerd op deadline (vroegste eerst).  
   Ook hier wordt per taak eerst de patiëntnaam met ID getoond, daarna de taakdetails.

5. "Nieuwe taak toevoegen"  
   Vraagt:
   - bestaand patiëntnummer ("patient_id")
   - omschrijving van de taak
   - deadline ("YYYY-MM-DD") van de taak
   - prioriteit (hoog / normaal / laag, standaard = normaal)
   - optionele opmerkingen vooral naar afhandeling toe en conclusies

   De datum van aanmaak wordt automatisch op vandaag gezet ("YYYY-MM-DD").  
   De status wordt standaard "lopende", en "voltooid_op" = "niet voltooid".  

   De code controleert:
   - of de patiënt met dit "id" bestaat; zo niet, wordt de taak niet toegevoegd;
   - of er niet al een taak met dezelfde "patient_id" + "datum_aanmaak" + "omschrijving" bestaat (dan wordt het bestaande taaknummer teruggegeven).

6. "Patiëntgegevens aanpassen"  
   Vraagt een bestaand patiëntnummer en laat dan toe (optioneel) te wijzigen:
   - naam
   - geboortedatum
   - telefoonnummer
   - opmerkingen  

   Velden die leeg worden gelaten, blijven ongewijzigd.

7. "Taak aanpassen"  
   Vraagt een bestaand taaknummer en laat dan toe (optioneel) te wijzigen:
   - omschrijving
   - deadline
   - prioriteit (hoog / normaal / laag)
   - status (lopende / afgewerkt)
   - opmerkingen/afhandeling  

   Wanneer de status wordt aangepast naar:
   - "afgewerkt" zal "voltooid_op" automatisch op de datum van vandaag worden gezet.
   - "lopende" zal "voltooid_op" op "niet voltooid" worden gezet.

8. "Exporteer alle openstaande taken naar CSV"  
   Vraagt optioneel een bestandsnaam (zonder extensie, eventueel inclusief map).  
   - Geen bestandsnaam opgegeven: export gebeurt naar de standaardlocatie: de map die ingesteld is in "settings.py"
   (of naar "export/open_taken.csv" indien settings.py niet gevonden werd).
   - Bestandsnaam opgegeven: 
   	- naam met map: export naar "<opgegeven_map/opgegeven_naam>.csv". Indien de map niet bestaat wordt ze aangemaakt.  
   	- naam zonder map: export "<opgegeven_naam>.csv" in de projectroot-folder waar je "python main.py" runt  

   De CSV bevat:
   - taaknummer
   - patiëntnaam
   - patiënt-ID
   - omschrijving
   - datum aanmaak
   - deadline
   - prioriteit
   - opmerkingen / afhandeling

9. "Zoek patiënt en diens uniek patiëntnummer obv de naam"  
   Vraagt (een deel van) de patiëntnaam.  
   Zoekt (case-insensitive) in de tabel "patienten" en:
   - toont "Geen patiënten gevonden" als er geen match is;
   - toont de patiëntgegevens en het unieke patiëntnummer als er precies één patiënt is;
   - toont een lijst met alle matches (met hun ID) als er meerdere patiënten zijn.

0. "Afsluiten"  
   Sluit het programma af.

---

## Projectstructuur (mappen en bestanden)

De belangrijkste bestanden en mappen:

- "main.py"  
  Hoofdscript van de applicatie. Toont het menu, leest gebruikersinvoer en roept functies uit de "app.db"-module aan.

- "app/" (package)
  - "__init__.py"  
    Maakt van "app" een Python package.
  - "db.py"  
    = Data access layer (DAL).  
    Bevat alle logica voor:
    - initialiseren van de SQLite-database,  
    - toevoegen / updaten van patiënten,  
    - toevoegen / updaten van taken,  
    - opvragen van patiënten en taken,  
    - ophalen van openstaande taken,  
    - export naar CSV.
  - "models.py"  
    Domain layer met eenvoudige klassen:
    - "Patient"  
    - "Taak"  
    Deze klassen worden gebruikt om database-rijen voor te stellen. Ze hebben een __str__ methode voor weergave van instanties in de terminal.

- "example_settings.py"  
  Voorbeeld van het instellingenbestand, toont hoe "settings.py" moet worden opgebouwd:  

```python
   # Example configuration for the tool Takenmanager Huisartsen

  # Folder where the SQLite database will be stored
  db_set_dir = "data"

  # SQLite database filename
  db_set_file = "task_manager.db"

  # Default folder for csv exports
  export_set_dir = "export"
```


### Belangrijke variabelen in "settings.py"

(NB Het bestand settings.py is te plaatsen in de folder waar main.py zich bevindt)

- "db_set_dir"  
  Map waar de database wordt opgeslagen (standaard "data").

- "db_set_file"  
  Bestandsnaam van de database (standaard "task_manager.db").

- "export_set_dir"  
  Standaardmap voor CSV-export (standaard "export").



Bij het initialiseren:

- Als "settings.py" bestaat, worden deze waarden uit "settings.py" gelezen.
- Als "settings.py" niet bestaat, worden de standaardwaarden gebruikt in "app/db.py":
  - "data" als datamap
  - "task_manager.db" als bestandsnaam voor de database
  - "export" als exportmap


De tabellen in de database zijn:

- "patienten"
- "taken"

Deze worden automatisch aangemaakt door "initialize_db()" in "app/db.py" als ze nog niet bestaan.

---

## INSTALLATIE EN GEBRUIK

Onderstaande stappen tonen hoe je de applicatie kan opzetten in een nieuwe omgeving.

1. Repository clonen


```bash
git clone https://github.com/BrahimChater/HuisartsenTakenbeheer.git
cd HuisartsenTakenbeheer
```

2. Virtuele omgeving aanmaken en activeren

*Windows* 
- PowerShell:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- Command Prompt (cmd):

```bash
python -m venv .venv
.\.venv\Scripts\activate.bat
```

*Unix(macOS /Linux)*

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Benodigde packages installeren

```
pip install -r requirements.txt
```
Deze tool maakt enkel gebruik van de Python standaard library. Er dienen dus geen extra PIP packages geïnstalleerd te worden.
cf. requirements.txt


4. Instellingenbestand aanmaken

Maak op basis van het voorbeeldbestand "example_settings.py" het lokale instellingenbestand:

*Windows (Powershell)/macOs/Linux*
```bash
cp example_settings.py settings.py
```
*Windows (Command Prompt)*
```bash
copy example_settings.py settings.py
```

Pas indien gewenst "db_set_dir", "db_set_file" of "export_set_dir" aan in "settings.py"
(bijvoorbeeld als de database of exports op een andere locatie moet komen te staan)


5. Database klaarzetten

5.1. Zorg dat de map uit "db_set_dir" bestaat (standaard "data/").
   Indien niet aanwezig, wordt deze automatisch aangemaakt bij het starten van de applicatie.
5.2 Plaats het meegeleverde voorbeeld-databasebestand in deze map, met exact dezelfde naam als "db_set_file" (standaard: "task_manager.db").

Met de standaardinstellingen moet de structuur er ongeveer zo uitzien:

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


*NB: De map `export/` wordt pas automatisch aangemaakt bij de eerste CSV-export. Tenzij door de gebruiker anders aangegeven.*


6. Applicatie starten

Activeer de virtuele omgeving en voer dan uit in de projectroot:

```bash
python main.py
```

Je krijgt nu het hoofdmenu in de terminal te zien en kan alle functies gebruiken.
Na elke actie wordt gevraagd om op Enter te drukken om terug te keren naar het hoofdmenu.
