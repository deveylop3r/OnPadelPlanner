from datetime import datetime

class Report:
    def __init__(self, customer_id=None, halle_id=None, start_date=None, end_date=None):
        self.customer_id = customer_id
        self.halle_id = halle_id
        self.start_date = start_date
        self.end_date = end_date

    def validateFields(self):
        
        if not any([self.customer_id, self.halle_id, (self.start_date and self.end_date)]):
            return False, ["Mindestens ein Filter muss ausgewählt werden"]
        return True, []