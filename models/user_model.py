
class User():
    def __init__(self,role="",username="",password=""):
        self.role = role
        self._user = username
        self._password = password
        