from config.connection import Database
from models.user_model import User

class UserData():
    def __init__(self, database=None):
        self.db = database if database else Database()

    def login(self, username: User):
        try:
            cursor = self.db.getConnection().cursor()
            res = cursor.execute("""
                            SELECT * FROM benutzer WHERE username = ? 
                            AND password = ?""", (username._user, username._password))
            row = res.fetchone() 
            if row:
                registeredUser = User(username=row[2], password=row[3])
                cursor.close()
                return registeredUser
            cursor.close()
            return None
        except Exception as e:
            print(f"Error en login: {e}")
            return None