from config.connection import Database
from models.coach_model import Coach


class CoachesData():
    def __init__(self, database: Database):
        self.db = database.getConnection()
        
    def add_coaches(self, info: Coach):
        try:
            cursor = self.db.cursor()
            cursor.execute("""INSERT INTO coaches (name, phone, address, zip_code, city, birthdate, email)
                            VALUES (?,?,?,?,?,?,?)""",(info.name, info.phone,info.address, info.zipCode, info.city, info.birthdate, info.email))
            self.db.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error adding Trainer: {e}")
            return False
        
    def search_coaches(self, name: str, phone: str):
        try:
            cursor = self.db.cursor()
            if name and phone:
                cursor.execute("""SELECT id, name, phone, birthdate 
                            FROM coaches 
                            WHERE name LIKE ? OR phone LIKE ?""", 
                            (f"%{name}%", f"%{phone}%"))
            elif name:
                cursor.execute("""SELECT id, name, phone, birthdate 
                            FROM coaches WHERE name LIKE ?""", 
                            (f"%{name}%",))
            elif phone:
                cursor.execute("""SELECT id, name, phone, birthdate 
                            FROM coaches WHERE phone LIKE ?""", 
                            (f"%{phone}%",))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching coaches: {e}")
            return []

        
    def get_coach_by_id(self, coach_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT * FROM coaches WHERE id = ?
            """, (coach_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting coach: {e}")
            return None

    def update_coach(self, coach_id, info: Coach):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                UPDATE coaches 
                SET name=?, phone=?, address=?, zip_code=?, 
                    city=?, birthdate=?, email=?
                WHERE id=?
            """, (info.name, info.phone, info.address, info.zipCode,
                info.city, info.birthdate, info.email, coach_id))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error updating coach: {e}")
            return False

    def delete_coach(self, coach_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM coaches WHERE id=?", (coach_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error deleting coach: {e}")
            return False