from config.connection import Database
from models.halle_model import Halle

class HalleData():
    def __init__(self, database: Database):
        self.database = database  
        self.db = database.getConnection()
    def add_halle(self, info: Halle):
        try:
            cursor = self.db.cursor()
            
            cursor.execute("""
                INSERT INTO halle (name, address, zip_code, city, phone, contact_person,
                                 price_one_morning, price_one_afternoon,
                                 price_group_morning, price_group_afternoon)
                VALUES (?,?,?,?,?,?,?,?,?,?)
                """, (
                    info.name, info.address, info.zipCode, info.city,
                    info.phone, info.contact,
                    info.price_one_morning, info.price_one_afternoon,
                    info.price_group_morning, info.price_group_afternoon
                ))
            
            halle_id = cursor.lastrowid
            
            for day_id in info.operating_days:
                cursor.execute("""
                    INSERT INTO halle_days (halle_id, day_id)
                    VALUES (?,?)
                    """, (halle_id, day_id))
            
            self.db.commit()
            return halle_id  
            
        except Exception as e:
            print(f"Error adding Halle: {e}")
            self.db.rollback()
            return False

    def validate_operating_days(self, selected_days):
      
        if not selected_days:
            return False, "Bitte wählen Sie mindestens einen Betriebstag aus"
        return True, None

    def get_halle(self, halle_id: int):
        try:
            cursor = self.db.cursor()
            
            cursor.execute("""
                SELECT * FROM halle WHERE id = ?
                """, (halle_id,))
            
            halle_data = cursor.fetchone()
            if not halle_data:
                return None
            
            cursor.execute("""
                SELECT day_id FROM halle_days WHERE halle_id = ?
                """, (halle_id,))
            
            operating_days = [row[0] for row in cursor.fetchall()]
            
            return Halle(
                name=halle_data[1],         
                address=halle_data[2],
                zipCode=halle_data[3],
                city=halle_data[4],
                phone=halle_data[5],
                contact=halle_data[6],
                operating_days=operating_days,
                price_one_morning=halle_data[7],
                price_one_afternoon=halle_data[8],
                price_group_morning=halle_data[9],
                price_group_afternoon=halle_data[10]
            )
            
        except Exception as e:
            print(f"Error getting Halle: {e}")
            return None

    def get_all_halles(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM halle")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting all Halles: {e}")
            return []
    
    def get_all_halles_for_delete(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT id, name, city, phone FROM halle")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting halles: {e}")
            return []
    
    def delete_halle(self, halle_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM halle_zeitplan WHERE halle_id=?", (halle_id,))
            cursor.execute("DELETE FROM halle_days WHERE halle_id=?", (halle_id,))
            cursor.execute("DELETE FROM halle WHERE id=?", (halle_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error deleting halle: {e}")
            self.db.rollback()
            return False