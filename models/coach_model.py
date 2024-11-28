from datetime import datetime

class Coach(): 
    def __init__(self,  name:str,
                        phone:str,
                        address:str,
                        zipCode:str,
                        city:str,
                        birthdate:str=None,
                        email:str=None):
                      
        self.name = name
        self.phone = phone
        self.address = address
        self.zipCode = zipCode
        self.city = city
        self.email = email     
        self.birthdate = birthdate

    def validateFields(self):
        missingFields = []
        
        if not self.name or self.name.strip() == "":
            missingFields.append("Name")
        if not self.address or self.address.strip() == "":
            missingFields.append("Addresse")
        if not self.zipCode or self.zipCode.strip() == "":
            missingFields.append("PLZ")
        if not self.city or self.city.strip() == "":
            missingFields.append("Stadt")
        if not self.phone or self.phone.strip() == "":
            missingFields.append("Telefon")
        if self.phone and not self.phone.replace('-','').isdigit():
            missingFields.append("Telefon (nur Zahlen und Bindestriche)")
        if self.email and '@' not in self.email:
            missingFields.append("E-Mail (ungültiges Format)")
        if not self.birthdate:
            missingFields.append("Geburtsdatum")
        else:
            try:
                birth_date = datetime.strptime(self.birthdate, "%d-%m-%Y").date()
                today = datetime.now().date()
                if birth_date > today:
                    missingFields.append("Geburtsdatum (kann nicht in der Zukunft liegen)")
            except ValueError:
                missingFields.append("Geburtsdatum (ungültiges Format)")
            
        return len(missingFields) == 0, missingFields
        