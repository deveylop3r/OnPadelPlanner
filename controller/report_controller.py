from config.connection import Database
from datetime import datetime
import pandas as pd
from PyQt6.QtWidgets import QFileDialog

class ReportsData:
    def __init__(self, database):
        self.db = database
    
    def get_appointments(self, report_info):
        cursor = self.db.getConnection().cursor()
        
        query = """
            SELECT 
                a.id,
                c.name as customer_name,
                h.name as halle_name,
                tr.name as coach_name,
                a.date,
                a.start_time as time_start,
                a.price,
                a.payment_status
            FROM appointments a
            JOIN customers c ON a.customer_id = c.id
            JOIN halle h ON a.halle_id = h.id
            JOIN coaches tr ON a.coach_id = tr.id
            WHERE 1=1
        """
        params = []

        if report_info.customer_id:
            query += " AND a.customer_id = ?"
            params.append(report_info.customer_id)
        
        if report_info.halle_id:
            query += " AND a.halle_id = ?"
            params.append(report_info.halle_id)
        
        if report_info.start_date and report_info.end_date:
            query += " AND a.date BETWEEN ? AND ?"
            params.extend([report_info.start_date, report_info.end_date])
        cursor.execute(query, params)
        return cursor.fetchall()

    def export_to_excel(self, data):
        if not data:
            return False, "Keine Daten zum Exportieren gefunden"
        
        try:
        
            df = pd.DataFrame(data, columns=['ID', 'Name', 'Halle','Trainer', 'Datum', 'Uhrzeit','Preis', 'Bezahlt'])
            
            filename, _ = QFileDialog.getSaveFileName(
                None,
                "Excel speichern",
                f"reservierungen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)"
            )
            
            if filename: 
                df.to_excel(filename, index=False, engine='openpyxl')
                return True, filename
            return False, "Export abgebrochen"
        
        except Exception as e:
            return False, f"Fehler beim Exportieren: {str(e)}"