from PyQt6 import uic
import os
from models.customer_model import Customer
from controller.customer_controller import CustomerData
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox


class CustomerRegister():
    def __init__(self, customerData: CustomerData, customer_id=None):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "register.ui")
        self.register = uic.loadUi(ui_path)
        self.customerData = customerData
        self.customer_id = customer_id
        self.register.setFixedSize(600, 600)
        self.register.customerBirthDate.setDate(QDate.currentDate())
        
        
        self.register.btnCustomerRegister.clicked.connect(self.on_save_clicked)
        self.register.btnDeleteCustomer.clicked.connect(self.on_delete_clicked)
        
        if customer_id:
            self.load_customer_data()
            self.register.setWindowTitle("Kunde bearbeiten")
            self.register.btnCustomerRegister.setText("Aktualisieren")
            self.register.btnDeleteCustomer.setVisible(True)
            self.register.txtCustomerTitle.setText("Kunde bearbeiten")
        else:
            self.register.btnDeleteCustomer.setVisible(False)

    #Kundendaten für die Bearbeitung laden
    def load_customer_data(self):
       
        customer = self.customerData.get_customer_by_id(self.customer_id)
        if customer:
            self.register.customerName.setText(customer[1])  
            self.register.customerCity.setText(customer[2])  
            self.register.customerEmail.setText(customer[3])  
            self.register.customerPhone.setText(customer[4])  
            
            try:
                birth_date = QDate.fromString(customer[5], "dd-MM-yyyy")
                self.register.customerBirthDate.setDate(birth_date)
            except:
                self.register.customerBirthDate.setDate(QDate.currentDate())
                
            self.register.customerAnotherInfo.setPlainText(customer[6])  

    def on_save_clicked(self):

        selected_date = self.register.customerBirthDate.date()
        current_date = QDate.currentDate()
        
        if selected_date > current_date:
            QMessageBox.warning(
                self.register,
                "Fehlende Daten",
                "Geburtsdatum kann nicht in der Zukunft liegen"
            )
            return False
        
        age = current_date.year() - selected_date.year() - (
            (current_date.month(), current_date.day()) < 
            (selected_date.month(), selected_date.day())
        )
    
        continue_register = True 
    
        if age < 18:
            confirm = QMessageBox.question(
                self.register,
                'Warnung',
                'Der Kunde ist minderjährig. Möchten Sie fortfahren?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            continue_register = (confirm == QMessageBox.StandardButton.Yes)
        
        if not continue_register:
            return False
            
        customer = Customer(
            name=self.register.customerName.text(),
            city=self.register.customerCity.text(),
            email=self.register.customerEmail.text(),
            phone=self.register.customerPhone.text(),
            birthdate=selected_date.toString("dd-MM-yyyy"),
            anotherInfo=self.register.customerAnotherInfo.toPlainText()
        )
        
        checkOk, missingFields = customer.validateFields()
        if not checkOk:
            error_message = "Bitte geben Sie folgende daten ein:\n* " + "\n* ".join(missingFields)
            QMessageBox.warning(
                self.register,
                "Fehlende Daten", error_message
            )
            return False
        
        if self.customer_id:
            success = self.customerData.update_customer(self.customer_id, customer)
            message = "Kunde wurde erfolgreich aktualisiert" if success else "Fehler bei der Aktualisierung"
        else:
            success = self.customerData.add_customer(customer)
            message = "Kunde wurde registriert" if success else "Fehler bei der Registrierung"
        
        QMessageBox.information(
            self.register,
            "Erfolg" if success else "Fehler", 
            message
        )
        
        if success:
            self.register.close()

    def on_delete_clicked(self):
        if not self.customer_id:
            return
            
        confirm = QMessageBox.question(
            self.register,
            'Bestätigen',
            'Möchten Sie diesen Kunden wirklich löschen?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            success = self.customerData.delete_customer(self.customer_id)
            
            if success:
                QMessageBox.information(
                    self.register,
                    "Erfolg", 
                    "Kunde wurde erfolgreich gelöscht"
                )
                self.register.close()
            else:
                QMessageBox.warning(
                    self.register,
                    "Fehler", 
                    "Fehler beim Löschen des Kundes"
                )