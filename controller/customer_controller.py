from config.connection import Database
from models.customer_model import Customer

class CustomerData():
    def __init__(self, database: Database):
        self.db = database.getConnection()
        
    def add_customer(self, info: Customer):
        try:
            cursor = self.db.cursor()
            cursor.execute("""INSERT INTO customers (name, city, email, phone, birthdate, another_info)
                           VALUES (?,?,?,?,?,?)""", 
                           (info.name, info.city, info.email, info.phone, info.birthdate, info.anotherInfo))
            self.db.commit()
            rows_affected = cursor.rowcount
            cursor.close()

            if rows_affected > 0:
                print("Customer added successfully")
                return True
               
            else:
                print("No customer was added")
                return False
        except Exception as e:
            print(f"Error adding customer: {e}")

    def search_customers(self, name: str, phone: str):
        try:
            cursor = self.db.cursor()
            if name and phone:
                cursor.execute("""SELECT id, name, phone, birthdate 
                            FROM customers 
                            WHERE name LIKE ? OR phone LIKE ?""", 
                            (f"%{name}%", f"%{phone}%"))
            elif name:
                cursor.execute("""SELECT id, name, phone, birthdate 
                            FROM customers WHERE name LIKE ?""", 
                            (f"%{name}%",))
            elif phone:
                cursor.execute("""SELECT id, name, phone, birthdate 
                            FROM customers WHERE phone LIKE ?""", 
                            (f"%{phone}%",))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching customers: {e}")
            return []
    def get_customer_by_id(self, id: int):
        try:
            cursor = self.db.cursor()
            cursor.execute("""SELECT id, name, city, email, phone, birthdate, another_info 
                           FROM customers WHERE id = ?""", (id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error getting customer: {e}")
            return None
            
    def update_customer(self, id: int, info: Customer):
        try:
            cursor = self.db.cursor()
            cursor.execute("""UPDATE customers 
                           SET name=?, city=?, email=?, phone=?, birthdate=?, another_info=?
                           WHERE id=?""", 
                           (info.name, info.city, info.email, info.phone, 
                            info.birthdate, info.anotherInfo, id))
            self.db.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating customer: {e}")
            return False
            
    def delete_customer(self, id: int):
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
            self.db.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False

   