from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from models.user_model import User
from controller.user_controller import UserData
import os
from ui.main import MainWindow

class Login():
    def __init__(self, planner=None, database=None):
        self.planner = planner 
        self.db = database 
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "login.ui")
        self.login = uic.loadUi(ui_path)
        self.login.setFixedSize(700, 600) 
        self.initUI()
        self.login.lblMessage.setText("")
        self.login.show()

    def validateLogin(self):
        if len(self.login.txtUser.text()) < 2:
            self.login.lblMessage.setText("Bitte prüfen die Benutzer-Eingabe")
            self.login.txtUser.setFocus()
        elif len(self.login.txtPassword.text()) < 3:
            self.login.lblMessage.setText("Bitte geben Sie ein Passwort ein")
            self.login.txtPassword.setFocus()
        else:
            self.login.lblMessage.setText("")
            userFields = User(username=self.login.txtUser.text(), password=self.login.txtPassword.text())
            userData = UserData(database=self.db)
            if (userData.login(userFields)):
                self.login.lblMessage.setText("Login successful")
                main_window = MainWindow(database=self.db)
                if self.planner:
                    self.planner.set_main_window(main_window)
                self.login.hide()
            else:
                self.login.lblMessage.setText("Invalid username or password")
                self.login.txtUser.setFocus()

    def initUI(self):
        self.login.btnLogin.clicked.connect(self.validateLogin)
