class Appointment:
    def __init__(self, customer_id=None, halle_id=None, coach_id=None, 
                 date=None, time=None, duration=None, training_type=None, 
                 price=None, payment_status=None, another_info=None):
        self.customer_id = customer_id
        self.halle_id = halle_id
        self.coach_id = coach_id  
        self.date = date
        self.time = time
        self.duration = duration
        self.training_type = training_type
        self.price = price
        self.payment_status = payment_status
        self.another_info = another_info

    def validateFields(self):
        missing = []
        if not self.customer_id:
            missing.append("Kunde")
        if not self.halle_id:
            missing.append("Halle")
        if not self.coach_id:
            missing.append("Trainer")
        if not self.date:
            missing.append("Datum")
        if not self.time:
            missing.append("Zeit")
        if not self.duration:
            missing.append("Dauer")
        if not self.training_type or self.training_type == "--Bitte wählen":
            missing.append("Trainingstyp")
        if not self.payment_status or self.payment_status == "--Bitte wählen":
            missing.append("Zahlungsstatus")
            
        return len(missing) == 0, missing