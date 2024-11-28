from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QCompleter
from PyQt6.QtCore import Qt, QDate
from PyQt6 import QtCore
from models.appointment_model import Appointment
from controller.appointment_controller import AppointmentData
import os

class AppointmentView:
    def __init__(self, appointmentData: AppointmentData, appointment_id=None):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "appointment.ui")
        self.appointment = uic.loadUi(ui_path)
        self.appointmentData = appointmentData
        self.selected_customer = None
        self.appointment_id = appointment_id
        self.appointment.setFixedSize(600, 600)
        
        self.init_ui()
        self.load_initial_data()

        if self.appointment_id:
            self.setup_edit_mode()
            self.load_appointment()
            self.appointment.btnTerminBuchen.setText("Aktualisieren")
            self.appointment.btnClearFieldsAppointment.setText("Termin löschen")

    def init_ui(self):
        """Benutzeroberfläche initialisieren und Events verbinden"""
        self.appointment.dateEdit.setMinimumDate(QDate.currentDate())
        self.appointment.terminName.textChanged.connect(self.on_customer_search)
        self.appointment.comboBoxHalle.currentIndexChanged.connect(self.on_halle_changed)
        self.appointment.dateEdit.dateChanged.connect(self.update_available_times)
        self.appointment.comboBoxTrainingTyp.currentIndexChanged.connect(self.update_price)
        self.appointment.btnTerminBuchen.clicked.connect(self.save_appointment)
        self.appointment.comboBoxDauer.currentIndexChanged.connect(self.update_price)
        self.appointment.btnClearFieldsAppointment.clicked.connect(self.clear_form)
        
        if not self.appointment_id:
            self.setup_customer_field()
            self.appointment.terminName.textChanged.connect(self.on_customer_search)
        

        self.appointment.terminPhone.setReadOnly(True)
        self.appointment.terminePreis.setReadOnly(True)

    def load_initial_data(self):
        """Bereits registrierte Daten in CombosBox laden"""
        self.load_halles()
        self.load_trainers()

    def setup_customer_field(self):
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.activated.connect(self.on_customer_selected)
        self.appointment.terminName.setCompleter(self.completer)

           # Conectar el evento de pérdida de foco
        self.appointment.terminName.editingFinished.connect(self.validate_customer_selection)

    def validate_customer_selection(self):
        current_text = self.appointment.terminName.text().strip()
        if current_text:
            customer = self.appointmentData.get_customer_by_exact_name(current_text)
            if customer:
                self.selected_customer = customer
                self.appointment.terminPhone.setText(customer[4] if customer[4] else '')
            else:
                self.selected_customer = None
                if current_text != "":
                    self.appointment.terminName.clear()
                    self.appointment.terminPhone.clear()

    def on_customer_search(self, text):
        if len(text) >= 2:
            customers = self.appointmentData.get_customers_by_name(text)
            customer_names = [customer[1] for customer in customers]
            model = QtCore.QStringListModel(customer_names)
            self.completer.setModel(model)

    def on_customer_selected(self, name): 
        customer = self.appointmentData.get_customer_by_exact_name(name)
        if customer:
            self.selected_customer = customer
            self.appointment.terminPhone.setText(customer[4] if customer[4] else '')

    def load_halles(self):
      
        halles = self.appointmentData.get_available_halles()
        self.appointment.comboBoxHalle.clear()
        self.appointment.comboBoxHalle.addItem("--Bitte wählen", None)
        for halle_id, name in halles:
            self.appointment.comboBoxHalle.addItem(name, halle_id)

    def load_trainers(self):
  
        trainers = self.appointmentData.get_available_trainers()
        self.appointment.comboBoxTrainer.clear()
        self.appointment.comboBoxTrainer.addItem("--Bitte wählen", None)
        for trainer_id, name in trainers:
            self.appointment.comboBoxTrainer.addItem(name, trainer_id)

    def update_available_times(self):
        #Aktualisieren der verfügbaren Zeitpläne nach Datum und Halle
        halle_id = self.appointment.comboBoxHalle.currentData()
        selected_date = self.appointment.dateEdit.date()
        
        if not halle_id:
            return

        day_id = selected_date.dayOfWeek()
        if day_id == 7: 
            self.appointment.comboBoxZeit.clear()
            QMessageBox.warning(
                self.appointment,
                "Hinweis",
                "Sonntags sind keine Termine verfügbar"
            )
            return
        
        available_times = self.appointmentData.get_available_times(
            halle_id, 
            day_id,
            selected_date.toString("dd-MM-yyyy")
        )
        
        self.appointment.comboBoxZeit.clear()
        self.appointment.comboBoxZeit.addItem("--Bitte wählen", None)
        for time_id, time_str in available_times:
            self.appointment.comboBoxZeit.addItem(time_str, time_id)

    def update_price(self):
        # Preis wird entsprechend der Auswahl aktualisiert
        halle_id = self.appointment.comboBoxHalle.currentData()
        training_type = self.appointment.comboBoxTrainingTyp.currentText() 
        time_str = self.appointment.comboBoxZeit.currentText()
        duration = self.appointment.comboBoxDauer.currentText()

        if not all([halle_id, training_type, time_str, duration]) or \
        time_str == "--Bitte wählen" or \
        training_type == "--Bitte wählen":  # Agregada esta validación
            self.appointment.terminePreis.clear()
            return

        price = self.appointmentData.calculate_price(
            halle_id, 
            training_type, 
            int(duration),
            time_str
        )
        
        if price is not None:
            self.appointment.terminePreis.setText(f"{price:.2f}")
        else:
            self.appointment.terminePreis.clear()

    def save_appointment(self):
        if self.appointment_id:
            selected_date = self.appointment.dateEdit.date()
            current_date = QDate.currentDate()
            if selected_date < current_date:
                QMessageBox.warning(
                    self.appointment,
                    "Fehler",
                    "Termine in der Vergangenheit können nicht bearbeitet werden"
                )
                return
        if not self.selected_customer:
            QMessageBox.warning(
                self.appointment,
                "Fehler",
                "Bitte wählen Sie einen Kunden aus"
            )
            return
        price_text = self.appointment.terminePreis.text().strip()
        if not price_text:
            QMessageBox.warning(
                self.appointment,
                "Fehler",
                "Bitte wählen Sie Trainingstyp, Dauer und Zeit aus"
            )
            return
    
        new_appointment = Appointment(
            customer_id=self.selected_customer[0],
            halle_id=self.appointment.comboBoxHalle.currentData(),
            coach_id=self.appointment.comboBoxTrainer.currentData(),
            date=self.appointment.dateEdit.date().toString("yyyy-MM-dd"),
            time=self.appointment.comboBoxZeit.currentText(),
            duration=int(self.appointment.comboBoxDauer.currentText()),
            training_type=self.appointment.comboBoxTrainingTyp.currentText(),
            payment_status=self.appointment.comboBoxPaymentStatus.currentText(),
            price=float(price_text),
            another_info=self.appointment.customerAnotherInfo.toPlainText()
        )

        if self.appointment_id:
            new_appointment.id = self.appointment_id

        valid, missing_fields = new_appointment.validateFields()
        if not valid:
            QMessageBox.warning(
                self.appointment,
                "Fehlende Daten",
                "Bitte füllen Sie die folgenden Felder aus:\n* " + "\n* ".join(missing_fields)
            )
            return

        try:
            if self.appointment_id:
                self.appointmentData.update_appointment(new_appointment)
                message = "Termin wurde aktualisiert"
                QMessageBox.information(self.appointment, "Erfolg", message)
                self.appointment.close() 
            else:
                self.appointmentData.save_appointment(new_appointment)
                message = "Termin wurde gespeichert"    
                QMessageBox.information(self.appointment, "Erfolg", message)
                self.clear_form()
            
        except Exception as e:
            QMessageBox.critical(self.appointment, "Fehler", str(e))

    def refresh_data(self):
        """Actualizar todos los datos después de cambios"""
        
        current_halle = self.appointment.comboBoxHalle.currentData()
        current_trainer = self.appointment.comboBoxTrainer.currentData()
        
        self.load_halles()
        self.load_trainers()
        self.load_initial_data()
        
        if current_halle:
            index = self.appointment.comboBoxHalle.findData(current_halle)
            if index >= 0:
                self.appointment.comboBoxHalle.setCurrentIndex(index)
                
        if current_trainer:
            index = self.appointment.comboBoxTrainer.findData(current_trainer)
            if index >= 0:
                self.appointment.comboBoxTrainer.setCurrentIndex(index)

    def on_halle_changed(self):

        self.update_available_times()
        self.update_price()

    def clear_form(self):
        if self.appointment_id:
            reply = QMessageBox.question(
                self.appointment,
                'Bestätigung',
                'Möchten Sie diesen Termin löschen?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                try:
                    self.appointmentData.delete_appointment(self.appointment_id)
                    QMessageBox.information(self.appointment, "Erfolg", "Termin wurde gelöscht")
                    self.appointment.close()
                except Exception as e:
                    QMessageBox.critical(self.appointment, "Fehler", str(e))
        else:
           
            self.appointment.terminName.clear()
            self.appointment.terminPhone.clear()
            self.appointment.customerAnotherInfo.clear()
            self.appointment.terminePreis.clear()
            
            self.appointment.comboBoxHalle.setCurrentIndex(0)
            self.appointment.comboBoxTrainer.setCurrentIndex(0)
            self.appointment.comboBoxTrainingTyp.setCurrentIndex(0)
            self.appointment.comboBoxDauer.setCurrentIndex(0)
            self.appointment.comboBoxZeit.setCurrentIndex(0)
            self.appointment.comboBoxPaymentStatus.setCurrentIndex(0)
            
            self.appointment.dateEdit.setDate(QDate.currentDate())
            
            self.selected_customer = None
            
            self.load_initial_data()

    def load_appointment(self):
        try:
            appointment_data = self.appointmentData.get_appointment_by_id(self.appointment_id)
            if not appointment_data:
                return
                
            customer_name = appointment_data[1]  
            appointment_date = QDate.fromString(appointment_data[4], "yyyy-MM-dd").toString("dd.MM.yyyy")
            appointment_time = appointment_data[5] 
            
            info_text = f"{customer_name} - Datum: {appointment_date} um {appointment_time} Uhr"
            self.appointment.terminName.setText(info_text)
            
            halle_index = self.appointment.comboBoxHalle.findText(appointment_data[2])  
            if halle_index >= 0:
                self.appointment.comboBoxHalle.setCurrentIndex(halle_index)
                
            trainer_index = self.appointment.comboBoxTrainer.findText(appointment_data[3]) 
            if trainer_index >= 0:
                self.appointment.comboBoxTrainer.setCurrentIndex(trainer_index)
                
            self.appointment.comboBoxTrainingTyp.setCurrentText(appointment_data[7]) 
            self.appointment.comboBoxDauer.setCurrentText(str(appointment_data[6]))   
            self.appointment.comboBoxPaymentStatus.setCurrentText(appointment_data[9]) 
            
            
            self.appointment.dateEdit.setDate(QDate.fromString(appointment_data[4], "yyyy-MM-dd"))
            self.appointment.comboBoxZeit.setCurrentText(appointment_data[5])  # start_time
            
            self.appointment.terminePreis.setText(str(appointment_data[8]))
            self.appointment.customerAnotherInfo.setPlainText(appointment_data[10])

            customer = self.appointmentData.get_customer_by_exact_name(appointment_data[1])
            if customer:
                self.selected_customer = customer
                
        except Exception as e:
            QMessageBox.critical(self.appointment, "Fehler", f"Fehler beim Laden: {str(e)}")
                
    def setup_edit_mode(self):
        #Konfiguration des Edit-modus
       
        self.appointment.setWindowTitle("Training bearbeiten")
        self.appointment.txtTitleAppointment.setText("Training Bearbeiten")
        self.appointment.txtKundeName.setText("Daten der Reservierung")
        self.appointment.txtTime.setText("Neue Uhrzeit")
        
        self.appointment.terminName.setReadOnly(True)
      #  self.appointment.terminName.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        self.appointment.terminName.setMinimumWidth(400)
        
        self.appointment.terminName.textChanged.disconnect()
        self.appointment.terminName.setCompleter(None)
        self.appointment.txtPhone.hide()
        self.appointment.terminPhone.hide()
        
        self.appointment.dateEdit.setMinimumDate(QDate.currentDate())