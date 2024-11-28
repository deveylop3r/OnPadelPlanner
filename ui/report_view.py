from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from models.report_model import Report
from datetime import datetime
from config.connection import Database
import os

class ReportView:
    def __init__(self, reportData):
        self.report_data = reportData
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "reports.ui")
        self.reports = uic.loadUi(ui_path)
        self.current_appointments = []
        self.reports.setFixedSize(800, 500)
        self.init_ui()
        
    def init_ui(self):

        self.reports.tableWidget.setColumnWidth(0, 10)   # ID
        self.reports.tableWidget.setColumnWidth(1, 150)  # Name
        self.reports.tableWidget.setColumnWidth(2, 110)  # Halle
        self.reports.tableWidget.setColumnWidth(3, 100)  # Trainer
        self.reports.tableWidget.setColumnWidth(4, 88)  # Datum
        self.reports.tableWidget.setColumnWidth(5, 65)  # Uhrzeit
        self.reports.tableWidget.setColumnWidth(6, 40)   # Preis
        self.reports.tableWidget.setColumnWidth(7, 165)  # Zahlungstatus 

        today = datetime.now()
        self.reports.dateEditVon.setDate(today)
        self.reports.dateEditBis.setDate(today)
        
        self.load_combos()
        
        self.reports.btnHalleSave.clicked.connect(self.search_data)
        self.reports.btnExportExcel.clicked.connect(self.export_excel)
        
    def load_combos(self):
     
        cursor = self.report_data.db.getConnection().cursor()
        cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = cursor.fetchall()
        self.reports.comboBoxTrainer_2.addItem("--Bitte wählen", None)
        for customer in customers:
            self.reports.comboBoxTrainer_2.addItem(customer[1], customer[0])
            
        
        cursor.execute("SELECT id, name FROM halle ORDER BY name")
        halls = cursor.fetchall()
        self.reports.comboBoxHalle.addItem("--Bitte wählen", None)
        for hall in halls:
            self.reports.comboBoxHalle.addItem(hall[1], hall[0])
            
    def search_data(self):
       
        customer_id = self.reports.comboBoxTrainer_2.currentData()
        halle_id = self.reports.comboBoxHalle.currentData()
        start_date = self.reports.dateEditVon.date().toString("yyyy-MM-dd")
        end_date = self.reports.dateEditBis.date().toString("yyyy-MM-dd")
   
        report = Report(
            customer_id=customer_id,
            halle_id=halle_id,
            start_date=start_date,
            end_date=end_date
        )
        
        is_valid, missing = report.validateFields()
        if not is_valid:
            QMessageBox.warning(
                self.reports,
                "Fehlende Daten",
                "Bitte füllen Sie die folgenden Felder aus:\n* " + "\n* ".join(missing)
            )
            return
            

        self.current_appointments = self.report_data.get_appointments(report)
        
      
        self.display_data(self.current_appointments)

    def format_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d.%m.%Y")
        except:
            return date_str
    
    def format_price(self, price):
        try:
            return "{:.2f}".format(float(price))
        except:
            return str(price)  
    
    def display_data(self, appointments):

        if not appointments:
            QMessageBox.information(
                self.reports,
                "Keine Ergebnisse",
                "Keine Ergebnisse gefunden. Bitte wählen Sie ein anderes Datum oder wählen Sie einen anderen Kunden oder eine andere Halle."
            )
            return
        # Tabelle leeren
        self.reports.tableWidget.setRowCount(0)
        
        # Tabelle befüllen
        for row, appointment in enumerate(appointments):
            self.reports.tableWidget.insertRow(row)
            for col, value in enumerate(appointment):
                formatted_value = value
                if col == 3:  # Datum
                    formatted_value = self.format_date(str(value))
                elif col == 4:  # Preise
                    formatted_value = self.format_price(value)
                    
                self.reports.tableWidget.setItem(row, col, 
                    QTableWidgetItem(str(formatted_value)))
    
    def export_excel(self):
        if not self.current_appointments:
            QMessageBox.information(
                self.reports,
                "Hinweis", 
                "Keine Daten zum Exportieren verfügbar. Bitte führen Sie zuerst eine Suche durch."
                )
            return
            
        success, result = self.report_data.export_to_excel(self.current_appointments)
        
        if success:
            QMessageBox.information(
                self.reports,
                "Erfolg", 
                f"Daten wurden erfolgreich exportiert nach: {result}"
            )
            #self.reports.close()
        else:
            QMessageBox.warning(
                self.reports,
                "Fehler", 
                f"Fehler beim Exportieren: {result}"
            )