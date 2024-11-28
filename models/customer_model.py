from datetime import datetime

class Customer():  
    def __init__(self,  name:str,
                        city:str,
                        email:str,
                        phone:str=None,
                        birthdate=None,
                        anotherInfo:str=None):
        self.name = name
        self.city = city
        self.email = email
        self.phone = phone
        self.birthdate = birthdate
        self.anotherInfo = anotherInfo

    def validateFields(self):
        missingFields = []
        
        if not self.name or self.name.strip() == "":
            missingFields.append("Name")
        if not self.city or self.city.strip() == "":
            missingFields.append("Stadt")
        if not self.phone or self.phone.strip() == "":
            missingFields.append("Telefon")
        if self.phone and not self.phone.replace('-','').isdigit():
            missingFields.append("Telefon (nur Zahlen und Bindestriche)")
        if self.email and '@' not in self.email:
            missingFields.append("E-Mail (ungültiges Format)")
        if not self.birthdate or self.birthdate.strip() == "":
            missingFields.append("Geburtsdatum (Pflichtfeld)")
        else:
            try:
                birth_date = datetime.strptime(self.birthdate, "%d-%m-%Y").date()
                today = datetime.now().date()
                if birth_date > today:
                    missingFields.append("Geburtsdatum (kann nicht in der Zukunft liegen)")
            except ValueError:
                missingFields.append("Geburtsdatum (ungültiges Format)")
            
        return len(missingFields) == 0, missingFields