from PyQt6 import uic
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from controller.coaches_controller import CoachesData
from controller.customer_controller import CustomerData
from controller.appointment_controller import AppointmentData
from controller.halle_controller import HalleData
from ui.coach_register_view import CoachesRegister
from ui.customer_register_view import CustomerRegister
from ui.appointment_view import AppointmentView
from PyQt6.QtCore import Qt, QDate
import os

class ProfileAdministration:
    def __init__(self, coachesData: CoachesData, customerData: CustomerData, appointmentData: AppointmentData, halleData: HalleData):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "profile_administration.ui")
        self.profile = uic.loadUi(ui_path)
        self.coachesData = coachesData
        self.customerData = customerData
        self.appointmentData = appointmentData
        self.halleData = halleData 
        self.last_search_text = ""
        self.last_profile_type = ""
        self.init_ui()
        self.profile.setFixedSize(600, 600)

    def init_ui(self):
        # Verwaltung Tabelle Name, Telefon und GebDatum
        self.profile.tableWidget.setColumnWidth(0, 170) 
        self.profile.tableWidget.setColumnWidth(1, 110)  
        self.profile.tableWidget.setColumnWidth(2, 100) 
        self.profile.tableWidget.setColumnWidth(3, 110) 

        self.profile.btnSearch.clicked.connect(self.search_data)
        self.profile.tableWidget.itemDoubleClicked.connect(self.on_row_double_clicked)

    def search_data(self):
        name = self.profile.fieldName.text().strip()
        phone = self.profile.fieldTelefon.text().strip()
        profile_type = self.profile.optionsComboBox.currentText()
        
        self.last_name = name
        self.last_phone = phone
        self.last_profile_type = profile_type

        if profile_type == "-- Bitte wählen":
            QMessageBox.warning(
                self.profile,
                "Hinweis",
                "Bitte wählen Sie eine Kategorie aus: Kunden, Trainer, Termine oder Halle"
            )
            return

        self.profile.tableWidget.setRowCount(0)

        if profile_type == "Halle": 
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.halle_delete = uic.loadUi(os.path.join(current_dir, "halle_delete.ui"))
            self.halle_delete.setFixedSize(618, 525)
            self.halle_delete.setParent(self.profile) 
            self.halle_delete.setWindowFlags(Qt.WindowType.Window)  
            
            halles = self.halleData.get_all_halles_for_delete()
            for halle in halles:
                self.halle_delete.comboBox.addItem(f"{halle[1]} - {halle[2]}", halle[0])
            
            self.halle_delete.btnDeleteCustomer.clicked.connect(self.on_delete_halle)
            self.halle_delete.show()
            return
    
        if not name and not phone:
            return

        if profile_type == "Kunden":
            results = self.customerData.search_customers(name, phone)
        elif profile_type == "Trainer":
            results = self.coachesData.search_coaches(name, phone)
        elif profile_type == "Termine":
            results = self.appointmentData.search_appointments(name, phone)
        else:
            return

        self.display_data(results, profile_type)
    def refresh_data(self):
        #Aktualisiert die Tabelle mit der letzten durchgeführten Suche
        if hasattr(self, 'last_name') and hasattr(self, 'last_phone'):
            self.profile.fieldName.setText(self.last_name)
            self.profile.fieldTelefon.setText(self.last_phone)
            self.search_data()
            
    def display_data(self, data, profile_type):
        self.profile.tableWidget.setRowCount(0)
        
        for row, item in enumerate(data):
            self.profile.tableWidget.insertRow(row)
            
            name_item = QTableWidgetItem(str(item[1]))  
            name_item.setData(Qt.ItemDataRole.UserRole, item[0])  # ID
            
            self.profile.tableWidget.setItem(row, 0, name_item)
            self.profile.tableWidget.setItem(row, 1, QTableWidgetItem(str(item[2] or "")))  
            self.profile.tableWidget.setItem(row, 2, QTableWidgetItem(str(item[3] or "")))  
            self.profile.tableWidget.setItem(row, 3, QTableWidgetItem(""))  
            
            if profile_type == "Termine" and len(item) > 4:
                appointment_date = QDate.fromString(item[4], "yyyy-MM-dd").toString("dd-MM-yyyy")
                self.profile.tableWidget.setItem(row, 3, QTableWidgetItem(appointment_date))

    def on_row_double_clicked(self, item):
        row = item.row()
        profile_type = self.profile.optionsComboBox.currentText()
        
        id_item = self.profile.tableWidget.item(row, 0)
        if not id_item:
            return
            
        profile_id = id_item.data(Qt.ItemDataRole.UserRole)
        
        if profile_type == "Trainer":
            self.trainer_edit = CoachesRegister(
                coachesData=self.coachesData, 
                coach_id=profile_id
            )
           
            self.trainer_edit.register_coach.finished.connect(self.refresh_data)
            self.trainer_edit.register_coach.show()
        elif profile_type == "Kunden":
            self.customer_edit = CustomerRegister(
                customerData=self.customerData,
                customer_id=profile_id
            )
           
            self.customer_edit.register.finished.connect(self.refresh_data)
            self.customer_edit.register.show()
        elif profile_type == "Termine":
            self.appointment_edit = AppointmentView(
                appointmentData=self.appointmentData,
                appointment_id=profile_id
            )
            self.appointment_edit.appointment.finished.connect(self.refresh_data)
            self.appointment_edit.appointment.show()

    
    def on_delete_halle(self):
        selected_index = self.halle_delete.comboBox.currentIndex()
        if selected_index < 0:
            return
            
        halle_id = self.halle_delete.comboBox.currentData()
        halle_name = self.halle_delete.comboBox.currentText()
       
        confirm = QMessageBox.question(
            self.halle_delete,
            'Bestätigen',
            f'Möchten Sie die Halle "{halle_name}" wirklich löschen?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            success = self.halleData.delete_halle(halle_id)
            
            if success:
                QMessageBox.information(
                    self.halle_delete,
                    "Erfolg",
                    "Halle wurde erfolgreich gelöscht"
                )
                self.halle_delete.close()
                self.refresh_data()
            else:
                QMessageBox.warning(
                    self.halle_delete,
                    "Fehler",
                    "Fehler beim Löschen der Halle"
                )
    def show(self):
        self.profile.show()