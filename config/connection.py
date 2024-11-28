import sqlite3
import os

class Database():
   
    def __init__(self):
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(current_dir, "onpadelPlanner.db")
            self.conn = sqlite3.connect(db_path)
            self.createTableAdmin()
            self.createTableDays()
            self.creataTableTimeSlots()
            self.createTableCustomers()
            self.createTableCoaches()
            self.createTableHalle()
            self.createTableHalleDays()
            self.createTableHalleZeitplan()
            self.createTableAppointments()

            self.insertInitialData()
        except Exception as e:
            print(f"Error creating database: {e}")
            return None

    def createTableAdmin(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS "benutzer" (
                "id"	INTEGER,
                "role"  TEXT,
                "username"	TEXT NOT NULL,
                "password"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT),
                UNIQUE("username")
                )""")
        self.conn.commit()
        cursor.close()
        self.createAdmin()

    def createTableCustomers(self):
            try:
                cursor = self.conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS "customers" (
                    "id"	INTEGER,
                    "name"  TEXT,
                    "city"	TEXT,
                    "email"	TEXT,
                    "phone"	TEXT,
                    "birthdate"	TEXT,
                    "another_info"	TEXT,
                    "created"	TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')),
                    PRIMARY KEY("id" AUTOINCREMENT),
                    UNIQUE("name","phone","birthdate")
                    )""")
                self.conn.commit()
                cursor.close()
             #   print ("Customer table created successfully.")
            except Exception as e:
                print(f"Error creating customer table: {e}")

    def createTableCoaches(self):
            try:
                cursor = self.conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS "coaches" (
                    "id"	INTEGER,
                    "name"	TEXT NOT NULL UNIQUE,
                    "phone"	TEXT,
                    "address"	TEXT,
                    "zip_code"	TEXT,
                    "city"	TEXT,
                    "birthdate"	TEXT,
                    "email"	TEXT,
                    "created"	TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')),           
                    PRIMARY KEY("id" AUTOINCREMENT)
                    UNIQUE("name","phone","birthdate")
                    )""")
                self.conn.commit()
                cursor.close()
             #   print ("Trainer table created successfully.")
            except Exception as e:
                print(f"Error creating customer coaches: {e}")
    def createTableDays(self):
            try:
                cursor = self.conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS "days" (
                                    "id"	INTEGER,
                                    "name"	TEXT NOT NULL,
                                    PRIMARY KEY("id")
                                )""")
                    
                self.conn.commit()
                cursor.close()
            #    print ("Days table created successfully.")
            except Exception as e:
                print(f"Error creating table days: {e}")

    def createTableHalleZeitplan(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS "halle_zeitplan" (
                "id"	INTEGER,
                "halle_id"	INTEGER,
                "day_id"	INTEGER,
                "time_slot_id"	INTEGER,
                "is_available" INTEGER default 0,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("day_id") REFERENCES "days"("id"),
                FOREIGN KEY("halle_id") REFERENCES "halle"("id"),
                FOREIGN KEY("time_slot_id") REFERENCES "time_slots"("id")
                )""")
            self.conn.commit()
            cursor.close()
         #   print ("HalleZeitplan table created successfully.")
        except Exception as e:
            print(f"Error creating customer coaches: {e}")
               
    def creataTableTimeSlots(self):
            try:
                cursor = self.conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS "time_slots" (
                                    "id"	INTEGER,
                                    "time"	TEXT NOT NULL,
                                    PRIMARY KEY("id")
                                )""")
                    
                self.conn.commit()
                cursor.close()
            #    print ("Time_slots table created successfully.")
            except Exception as e:
                print(f"Error creating customer coaches: {e}")
    
    def createTableHalle(self):
            try:
                cursor = self.conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS "halle" (
                        "id"	INTEGER,
                        "name"	TEXT NOT NULL,
                        "address"	TEXT NOT NULL,
                        "zip_code"	TEXT NOT NULL,
                        "city"	TEXT NOT NULL,
                        "phone"	TEXT NOT NULL,
                        "contact_person"	TEXT,
                        "price_one_morning"	REAL,
                        "price_one_afternoon" REAL,
                        "price_group_morning" REAL,
                        "price_group_afternoon" REAL,
                        PRIMARY KEY("id" AUTOINCREMENT),
                        UNIQUE("name","city")
                    )""")
                self.conn.commit()
                cursor.close()
            #    print ("Halle table created successfully.")
            except Exception as e:
                print(f"Error creating customer coaches: {e}")
    
    def createTableHalleDays(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS "halle_days" (
                "halle_id"	INTEGER,
                "day_id"	INTEGER,
                PRIMARY KEY("halle_id","day_id"),
                FOREIGN KEY("day_id") REFERENCES "days"("id"),
                FOREIGN KEY("halle_id") REFERENCES "halle"("id")
                )""")
            self.conn.commit()
            cursor.close()
         #   print ("HalleDays table created successfully.")
        except Exception as e:
            print(f"Error creating HalleDays: {e}")

    def insertInitialData(self):
        cursor = self.conn.cursor()
        try:
            week_days = [
                (1, 'Montag'),
                (2, 'Dienstag'),
                (3, 'Mittwoch'),
                (4, 'Donnerstag'),
                (5, 'Freitag'),
                (6, 'Samstag')
            ]
            
            time_slots = [
                (1, '09:00'), (2, '09:30'),
                (3, '10:00'), (4, '10:30'),
                (5, '11:00'), (6, '11:30'),
                (7, '12:00'), (8, '12:30'),
                (9, '13:00'), (10, '13:30'),
                (11, '14:00'), (12, '14:30'),
                (13, '15:00'), (14, '15:30'),
                (15, '16:00'), (16, '16:30'),
                (17, '17:00'), (18, '17:30'),
                (19, '18:00'), (20, '18:30'),
                (21, '19:00'), (22, '19:30'),
                (23, '20:00'), (24, '21:00')
            ]

            for day_id, name in week_days:
                try:
                    cursor.execute("INSERT INTO days (id, name) VALUES (?, ?)", 
                                 (day_id, name))
                except sqlite3.IntegrityError:
                    pass

            for time_id, time in time_slots:
                try:
                    cursor.execute("INSERT INTO time_slots (id, time) VALUES (?, ?)", 
                                 (time_id, time))
                except sqlite3.IntegrityError:
                    pass

            self.conn.commit()
         #   print("Korrekt eingegebene Stammdaten")
            
        except Exception as e:
            print(f"Fehler beim Einfügen der Startdaten: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

    def createTableAppointments(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT exists "appointments" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                halle_id INTEGER,
                coach_id INTEGER,
                date TEXT,
                start_time TEXT,
                duration INTEGER,
                training_type TEXT,
                price REAL,
                payment_status TEXT,
                another_info TEXT,
                created	TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')),
                updated	TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now')),
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (halle_id) REFERENCES halle(id),
                FOREIGN KEY (coach_id) REFERENCES coaches(id)
            )""")
                
            self.conn.commit()
            cursor.close()
        #    print ("Appointment table created successfully.")
        except Exception as e:
            print(f"Error creating table Appointment: {e}")

    def createAdmin(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                        INSERT INTO benutzer (role,username, password) 
                        VALUES (?, ?, ?)
                    """, ("Administrator", "admin", "admin"))
            self.conn.commit()
        except Exception as e:
            print(f"Error add benutzer admin: {e}")
            return None
    
    def getConnection(self):
        return self.conn
