from PyQt6 import uic
import os
from models.coach_model import Coach
from controller.coaches_controller import CoachesData
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox


class CoachesRegister():
    def __init__(self, coachesData: CoachesData, coach_id=None):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "trainer_register.ui")
        self.register_coach = uic.loadUi(ui_path)
        self.coachesData = coachesData
        self.coach_id = coach_id
        self.register_coach.setFixedSize(600, 600) 
        self.register_coach.coachBirthDate.setDate(QDate.currentDate())
        
        self.register_coach.btnCoachRegister.clicked.connect(self.on_save_clicked)
        self.register_coach.btnDeleteCoach.clicked.connect(self.on_delete_clicked)
        
        if coach_id:
            self.load_coach_data()
            self.register_coach.setWindowTitle("Trainer Bearbeiten")
            self.register_coach.btnCoachRegister.setText("Aktualisieren")
            self.register_coach.btnDeleteCoach.setVisible(True)
            self.register_coach.txtCoachTitle.setText("Trainer Bearbeiten")
           

    def load_coach_data(self):
        coach = self.coachesData.get_coach_by_id(self.coach_id)
        if coach:
            self.register_coach.coachName.setText(coach[1]) 
            self.register_coach.coachPhone.setText(coach[2])  
            self.register_coach.coachAddress.setText(coach[3]) 
            self.register_coach.coachZipCode.setText(coach[4])  
            self.register_coach.coachCity.setText(coach[5])  
            self.register_coach.coachEmail.setText(coach[7])  
            
            try:
                birth_date = QDate.fromString(coach[6], "dd-MM-yyyy")
                self.register_coach.coachBirthDate.setDate(birth_date)
            except:
                self.register_coach.coachBirthDate.setDate(QDate.currentDate())

    
    def on_save_clicked(self):
        selected_date = self.register_coach.coachBirthDate.date()
        current_date = QDate.currentDate()
        
        if selected_date > current_date:
            QMessageBox.warning(
                self.register_coach,
                "Fehlende Daten",
                "Geburtsdatum kann nicht in der Zukunft liegen"
            )
            return False
            
        coach = Coach(
            name=self.register_coach.coachName.text(),
            phone=self.register_coach.coachPhone.text(),
            address=self.register_coach.coachAddress.text(),
            zipCode=self.register_coach.coachZipCode.text(),
            city=self.register_coach.coachCity.text(),
            email=self.register_coach.coachEmail.text(),
            birthdate=selected_date.toString("dd-MM-yyyy")
        )
        
        checkOk, missingFields = coach.validateFields()
        if not checkOk:
            error_message = "Bitte geben Sie folgende Daten ein:\n* " + "\n* ".join(missingFields)
            QMessageBox.warning(
                self.register_coach,
                "Fehlende Daten", 
                error_message
            )
            return False
        
        if self.coach_id:
            success = self.coachesData.update_coach(self.coach_id, coach)
            message = "Trainer wurde aktualisiert" if success else "Fehler bei der Aktualisierung"
        else:
            success = self.coachesData.add_coaches(coach)
            message = "Trainer wurde registriert" if success else "Fehler bei der Registrierung"
        
        QMessageBox.information(
            self.register_coach,
            "Erfolg" if success else "Fehler", 
            message
        )
        
        if success:
            self.register_coach.close()

    def on_delete_clicked(self):
        if not self.coach_id:
            return
            
        confirm = QMessageBox.question(
            self.register_coach,
            'Bestätigen',
            'Möchten Sie diesen Trainer wirklich löschen?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        if confirm == QMessageBox.StandardButton.Yes:
            success = self.coachesData.delete_coach(self.coach_id)
            
            if success:
                QMessageBox.information(
                    self.register_coach,
                    "Erfolg", 
                    "Trainer wurde erfolgreich gelöscht"
                )
                self.register_coach.close()
            else:
                QMessageBox.warning(
                    self.register_coach,
                    "Fehler", 
                    "Fehler beim Löschen des Trainers"
                )
        
        