from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.login import Login
from config.connection import Database
import sys

class Planner():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = None
        self.db = Database() 
        self.login = Login(planner=self, database=self.db)
        self.app.exec()  
    
    def set_main_window(self, window):
        self.main_window = window
                                
        if self.main_window:
            self.main_window.main.logoutIcon.clicked.connect(self.logout)
    
    def logout(self):
        """Abmeldungen verwalten - Beenden Sie die Verbindung zur Datenbank, 
        schließen Sie alle offenen Fenster und beenden Sie die Anwendung."""

        if not self.main_window:
            return
            
        reply = QMessageBox.question(
            self.main_window.main,
            'Bestätigen',
            'Möchten Sie OnPadel-Planner beenden?',
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Ok
        )

        if reply == QMessageBox.StandardButton.Ok:
            try:
                if self.db:
                    self.db.getConnection().close()
            except:
                pass
            
            try:
                self.main_window.register.close()
            except:
                pass
            try:
                self.main_window.register_coach.close()
            except:
                pass
            try:
                self.main_window.appointment_view.appointment.close()
            except:
                pass
                
            self.main_window.main.close()
            self.main_window = None
            
            self.app.quit()
