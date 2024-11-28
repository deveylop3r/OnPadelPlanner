from config.connection import Database

class HalleZeitplanData:
    def __init__(self, database: Database):
        self.db = database.getConnection()   
    def validate_time_selections(self, selected_times):

        if not selected_times:
            return False, "Bitte wählen Sie mindestens eine Uhrzeit aus"
        return True, None
    
    def add_zeitplan(self, halle_id, day_id, selected_times):
        cursor = self.db.cursor()
        try:
            for i in range(1, 25):
                cursor.execute("""
                    INSERT INTO halle_zeitplan (halle_id, day_id, time_slot_id, is_available)
                    VALUES (?, ?, ?, 0)
                """, (halle_id, day_id, i))
            
         
            for time_slot_id in selected_times:
                cursor.execute("""
                    UPDATE halle_zeitplan 
                    SET is_available = 1
                    WHERE halle_id = ? AND day_id = ? AND time_slot_id = ?
                """, (halle_id, day_id, time_slot_id))
            
            self.db.commit()
            return True
            
        except Exception as e:
            print(f"Error adding zeitplan: {e}")
            self.db.rollback()
            return False

    def get_zeitplan(self, halle_id, day_id):
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT time_slot_id, is_available 
                FROM halle_zeitplan 
                WHERE halle_id = ? AND day_id = ?
                ORDER BY time_slot_id
            """, (halle_id, day_id))
            
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error getting zeitplan: {e}")
            return []

    def update_zeitplan(self, halle_id, day_id, selected_times):
        cursor = self.db.cursor()
        try:
          
            cursor.execute("""
                UPDATE halle_zeitplan 
                SET is_available = 0
                WHERE halle_id = ? AND day_id = ?
            """, (halle_id, day_id))
            
            for time_slot_id in selected_times:
                cursor.execute("""
                    UPDATE halle_zeitplan 
                    SET is_available = 1
                    WHERE halle_id = ? AND day_id = ? AND time_slot_id = ?
                """, (halle_id, day_id, time_slot_id))
            
            self.db.commit()
            return True
            
        except Exception as e:
            print(f"Error updating zeitplan: {e}")
            self.db.rollback()
            return False

    def get_available_times(self, halle_id, day_id):
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT t.time 
                FROM halle_zeitplan hz
                JOIN time_slots t ON hz.time_slot_id = t.id
                WHERE hz.halle_id = ? AND hz.day_id = ? AND hz.is_available = 1
                ORDER BY t.id
            """, (halle_id, day_id))
            
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error getting available times: {e}")
            return []