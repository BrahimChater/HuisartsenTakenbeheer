#Creates a class to represent a patient
class Patient:
    def __init__(self, id, naam, geboorte_datum, telefoon, opmerkingen="/"):
        self.id = id
        self.naam = naam
        self.geboorte_datum = geboorte_datum
        self.telefoon = telefoon
        self.opmerkingen = opmerkingen
        
    def __str__(self):
        return (
                f"({self.id}) {self.naam} (geb. {self.geboorte_datum}, tel. {self.telefoon})\n"
                f"(info: {self.opmerkingen})"
            )
                 
#Creates a class to represent a task
class Taak:
    def __init__(
            self, 
            id, 
            patient_id, 
            omschrijving, 
            datum_aanmaak, 
            deadline,
            prioriteit='normaal',
            status = 'lopende',
            voltooid_op="/",
            opmerkingen_afhandeling="/"
            ):
        self.id = id
        self.patient_id = patient_id
        self.omschrijving = omschrijving
        self.datum_aanmaak = datum_aanmaak
        self.prioriteit = prioriteit
        self.deadline = deadline
        self.status = status
        self.voltooid_op = voltooid_op
        self.opmerkingen_afhandeling = opmerkingen_afhandeling
        
        
    def __str__(self):
        return (
           f"Taak: {self.id}, (mbt patiënt {self.patient_id}) | Aangemaakt op: {self.datum_aanmaak}\n"
           f"Omschrijving: {self.omschrijving}\n"
           f"Deadline: {self.deadline} | prioriteit: {self.prioriteit} | status: {self.status}\n"
           f"Voltooid op: {self.voltooid_op}\n"
           f"Conclusie: {self.opmerkingen_afhandeling}\n"
        )
