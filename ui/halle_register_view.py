from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from models.halle_model import Halle
from controller.halle_controller import HalleData
from controller.halleZeitplan_controller import HalleZeitplanData
import os

class HalleRegister():
    def __init__(self, halleData: HalleData):
        """
        Initialisiert das Registrierungsfenster
        """
        self.halleData = halleData
        self.zeitplan_data = HalleZeitplanData(halleData.database)
        self.current_halle_id = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.register = uic.loadUi(os.path.join(current_dir, "halle_register.ui"))
        self.zeitplan = uic.loadUi(os.path.join(current_dir, "halle_zeitplan.ui"))
        self.register.setFixedSize(660, 600)
        self.zeitplan.setFixedSize(631, 490)
        
        self.register.btnHalleSave.clicked.connect(self.on_register_clicked)
        self.zeitplan.btnZeitPlan.clicked.connect(self.on_zeitplan_save)
       
        # Tage Buttons initialisieren 
        self.day_buttons = [
            self.register.btnMontag,
            self.register.btnDienstag,
            self.register.btnMittwoch,
            self.register.btnDonnerstag,
            self.register.btnFreitag,
            self.register.btnSamstag
        ]
        self.day_names = ['Montag', 'Dienstag', 'Mittwoch', 
                         'Donnerstag', 'Freitag', 'Samstag']
        
        self.current_day_index = 0
        self.selected_days = []

    def show(self):
        self.register.show()

    def get_selected_days(self):
        """
        Holt die ausgewählten Tage von den UI-Buttons
        """
        selected = []
        for i, btn in enumerate(self.day_buttons, start=1):
            if btn.isChecked():
                selected.append(i)
        return selected

    def update_zeitplan_title(self):
        """
        Aktualisiert den Titel des Zeitplanfensters
        """
        current_day = self.day_names[self.selected_days[self.current_day_index]-1]
        self.zeitplan.txtHalletext.setText(f"Bitte wählen Sie die Uhrzeit für {current_day}:")

    def clear_time_selections(self):

        for i in range(1, 25):
            button = getattr(self.zeitplan, f"pushButton_{i}", None)
            if button:
                button.setChecked(False)
    
    def get_selected_times(self):
        """
        Holt die ausgewählten Zeiten von den UI-Buttons
        """
        selected = []
        for i in range(1, 25):
            button = getattr(self.zeitplan, f"pushButton_{i}", None)
            if button and button.isChecked():
                selected.append(i)
        return selected

    def on_register_clicked(self):

        halle = Halle(
            name=self.register.halleName.text(),
            address=self.register.halleAddress.text(),
            zipCode=self.register.halleZipCode.text(),
            city=self.register.halleCity.text(),
            phone=self.register.hallePhone.text(),
            contact=self.register.contactPersonHalle.text(),
            operating_days=self.get_selected_days(),
            price_one_morning=self.register.priceOneMorning.text(),
            price_one_afternoon=self.register.priceOneEvening.text(),
            price_group_morning=self.register.priceGroupMorning.text(),
            price_group_afternoon=self.register.priceGroupEvening.text()
        )

        # Validierung 
        checkOk, missingFields = halle.validateFields()
        if not checkOk:
            QMessageBox.warning(
                self.register,
                "Fehlende Daten",
                "Bitte geben Sie folgende Daten ein:\n* " + "\n* ".join(missingFields)
            )
            return
        
        days_ok, days_error = self.halleData.validate_operating_days(self.get_selected_days())
        if not days_ok:
            QMessageBox.warning(self.register, "Fehlende Daten", days_error)
            return

        self.current_halle_id = self.halleData.add_halle(halle)
        if self.current_halle_id:
            QMessageBox.information(
                self.register,
                "Erfolg",
                "Halle gespeichert, bitte geben Sie die Zeitangaben im nächsten Fenster an."
            )
            self.selected_days = self.get_selected_days()
            self.current_day_index = 0
            self.update_zeitplan_title()
            self.zeitplan.show()
            self.register.hide()
        else:
            QMessageBox.critical(
                self.register,
                "Fehler",
                "Fehler beim Speichern der Daten"
            )

    def on_zeitplan_save(self):
        """
        Handler für den Zeitplan-Speichern-Button
        """
        selected_times = self.get_selected_times()
        current_day = self.selected_days[self.current_day_index]
        
        success = self.zeitplan_data.add_zeitplan(
            halle_id=self.current_halle_id,
            day_id=current_day,
            selected_times=selected_times
        )
        
        if not success:
            QMessageBox.warning(
                self.zeitplan,
                "Fehler",
                "Fehler beim Speichern der Zeitangaben"
            )
            return
        
        self.clear_time_selections()
        self.current_day_index += 1
        
        if self.current_day_index < len(self.selected_days):
            self.update_zeitplan_title()
        else:
            self.zeitplan.close()
            QMessageBox.information(
                self.register,
                "Erfolg",
                "Zeitplan wurde erfolgreich gespeichert"
            )
            self.register.show()
            self.clear_form()
    def clear_form(self):

        self.register.halleName.setText("")
        self.register.halleAddress.setText("")
        self.register.halleZipCode.setText("")
        self.register.halleCity.setText("")
        self.register.hallePhone.setText("")
        self.register.contactPersonHalle.setText("")
        self.register.priceOneMorning.setText("")
        self.register.priceOneEvening.setText("")
        self.register.priceGroupMorning.setText("")
        self.register.priceGroupEvening.setText("")
        
        for button in self.day_buttons:
            button.setChecked(False)
        
        self.current_day_index = 0
        self.selected_days = []
        
        self.clear_time_selections()
        
        self.register.halleName.setFocus()