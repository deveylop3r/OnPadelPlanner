from config.connection import Database
from datetime import datetime

class AppointmentData:
    def __init__(self, database: Database):
        self.database = database
        self.db = database.getConnection()

    def get_available_times(self, halle_id, day_id, date_str):
    
        cursor = self.db.cursor()
        try:
            
            cursor.execute("""
                SELECT 1 FROM halle_days 
                WHERE halle_id = ? AND day_id = ?
            """, (halle_id, day_id))
            
            works_today = cursor.fetchone()
            
            if not works_today:
                return []

            cursor.execute("""
                SELECT DISTINCT ts.id, ts.time 
                FROM time_slots ts
                JOIN halle_zeitplan hz ON ts.id = hz.time_slot_id
                WHERE hz.halle_id = ? 
                AND hz.day_id = ? 
                AND hz.is_available = 1
                ORDER BY ts.time
            """, (halle_id, day_id))
            
            all_times = cursor.fetchall()
            
            if not all_times:
                return []

            formatted_date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

            cursor.execute("""
                SELECT start_time 
                FROM appointments 
                WHERE halle_id = ? 
                AND date = ?
            """, (halle_id, formatted_date))
            
            booked_times = {row[0] for row in cursor.fetchall()}
            
            available_times = [(time_id, time_str) for time_id, time_str in all_times 
                                if time_str not in booked_times]
            
            return available_times
                    
        finally:
            cursor.close()

    def save_appointment(self, appointment):
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                INSERT INTO appointments (
                    customer_id, halle_id, coach_id, date, 
                    start_time, duration, training_type, 
                    price, payment_status, another_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                appointment.customer_id,
                appointment.halle_id,
                appointment.coach_id,
                appointment.date,
                appointment.time,
                appointment.duration,
                appointment.training_type,
                appointment.price,
                appointment.payment_status,
                appointment.another_info
            ))
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def get_customers_by_name(self, name_pattern):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id, name, phone 
            FROM customers 
            WHERE name LIKE ?
        """, (f"%{name_pattern}%",))
        return cursor.fetchall()

    def get_available_halles(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, name FROM halle")
        return cursor.fetchall()

    def get_available_trainers(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, name FROM coaches")
        return cursor.fetchall()

    def get_customer_by_exact_name(self, name):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id, name, city, email, phone, birthdate, another_info
            FROM customers 
            WHERE name = ?
        """, (name,))
        return cursor.fetchone()
    
    def get_halle_prices(self, halle_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT price_one_morning, price_one_afternoon, 
                price_group_morning, price_group_afternoon
            FROM halle 
            WHERE id = ?
        """, (halle_id,))
        return cursor.fetchone()

    def calculate_price(self, halle_id, training_type, duration, time_str):
        try:
            prices = self.get_halle_prices(halle_id)
            if not prices:
                return None

            hour = int(time_str.split(':')[0])
            is_morning = hour < 14

            if training_type == "Einzel": 
                base_price = prices[0] if is_morning else prices[1]
            else: 
                base_price = prices[2] if is_morning else prices[3]

            duration_multiplier = {
                60: 1,
                90: 1.5,
                120: 2
            }
            
            return base_price * duration_multiplier[duration]
            
        except Exception as e:
            print(f"Error calculating price: {e}")
            return None
  
    def search_appointments(self, name, phone):
        cursor = self.db.cursor()
        try: 
            query = "SELECT id FROM customers WHERE 1=1 "
            params = []
            
            if name:
                query += " AND name LIKE ?"
                params.append(f"%{name}%")
            if phone:
                query += " AND phone LIKE ?"
                params.append(f"%{phone}%")
                
            cursor.execute(query, params)
            customer_ids = [row[0] for row in cursor.fetchall()]
            
            if not customer_ids:
                return []
                
            placeholders = ','.join('?' * len(customer_ids))
            cursor.execute(f"""
                SELECT 
                    a.id,
                    c.name,
                    c.phone,
                    c.birthdate,
                    a.date
                FROM appointments a
                JOIN customers c ON a.customer_id = c.id
                WHERE a.customer_id IN ({placeholders})
                ORDER BY a.date DESC
            """, customer_ids)
            
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_appointment_by_id(self, appointment_id):
        cursor = self.db.cursor()
        try:
            cursor.execute("""
            SELECT 
                a.id,c.name as customer_name, h.name as halle_name,co.name as coach_name,
                a.date,a.start_time,a.duration,a.training_type,a.price,a.payment_status,
                a.another_info,a.customer_id,a.halle_id,a.coach_id
            FROM appointments a
            JOIN customers c ON a.customer_id = c.id
            JOIN halle h ON a.halle_id = h.id
            LEFT JOIN coaches co ON a.coach_id = co.id
            WHERE a.id = ?
            """, (appointment_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def can_modify_appointment(self, date_str):
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.now().date()

            if appointment_date < today:
                return False, "Termine in der Vergangenheit können nicht geändert werden"
            return True, ""
        except Exception as e:
            return False, "Fehler bei der Datumsvalidierung"

    def update_appointment(self, appointment):

        can_modify, message = self.can_modify_appointment(appointment.date)
        if not can_modify:
            raise ValueError(message)
            
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                UPDATE appointments SET customer_id = ?, halle_id = ?, coach_id = ?, date = ?, start_time = ?,
                            duration = ?,training_type = ?,price = ?,payment_status = ?,another_info = ?,updated = strftime('%d-%m-%Y %H:%M:%S', 'now')
                        WHERE id = ?""", [
                        appointment.customer_id,appointment.halle_id,appointment.coach_id,appointment.date,
                        appointment.time,appointment.duration,appointment.training_type,appointment.price,
                        appointment.payment_status,appointment.another_info, appointment.id
            ])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def delete_appointment(self, appointment_id):
  
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            raise ValueError("Termin nicht gefunden")
            
        can_modify, message = self.can_modify_appointment(appointment[4])
        if not can_modify:
            raise ValueError(message)
        
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM appointments WHERE id = ?", [appointment_id])
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()