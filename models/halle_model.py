class Halle(): 
    def __init__(self,  name:str,
                        address:str,
                        zipCode:str,
                        city:str,
                        phone:str,
                        contact:str=None,
                        operating_days: list = None,
                        price_one_morning:str=None,
                        price_one_afternoon:str=None,
                        price_group_morning:str=None,
                        price_group_afternoon:str=None):
                      
        self.name = name
        self.address = address
        self.zipCode = zipCode
        self.city = city
        self.phone = phone
        self.contact = contact
        self.operating_days = operating_days or []
        self.price_one_morning = price_one_morning
        self.price_one_afternoon = price_one_afternoon
        self.price_group_morning = price_group_morning
        self.price_group_afternoon = price_group_afternoon

    def validateFields(self):
        missingFields = []
        
        if not self.name or self.name.strip() == "":
            missingFields.append("Name")
        if not self.address or self.address.strip() == "":
            missingFields.append("Adresse")
        if not self.zipCode or self.zipCode.strip() == "":
            missingFields.append("Postleitzahl")
        if not self.city or self.city.strip() == "":
            missingFields.append("Stadt")
        if not self.phone or self.phone.strip() == "":
            missingFields.append("Telefonnummer")
        if not self.contact or self.contact.strip() == "":
            missingFields.append("Kontaktperson")
        if not self.price_one_morning or self.price_one_morning.strip() == "":
            missingFields.append("Preis für einzel Vormittag")
        if not self.price_one_afternoon or self.price_one_afternoon.strip() == "":
            missingFields.append("Preis für einzel Nachmittag")
        if not self.price_group_morning or self.price_group_morning.strip() == "":
            missingFields.append("Preis für Gruppen Vormittag")
        if not self.price_group_afternoon or self.price_group_afternoon.strip() == "":
            missingFields.append("Preis für Gruppen Nachmittag")
        
        return len(missingFields) == 0, missingFields