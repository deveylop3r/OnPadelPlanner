from PyQt6 import uic
#from PyQt6 import QtGui
#from PyQt6.QtCore import QDate
import os
#from models.customer_model import Customer
#from models.coach_model import Coach
#from config.connection import Database
from ui.halle_register_view import HalleRegister
from ui.coach_register_view import CoachesRegister
from ui.customer_register_view import CustomerRegister
from ui.appointment_view import AppointmentView
from ui.report_view import ReportView
from ui.profile_administration_view import ProfileAdministration
from controller.customer_controller import CustomerData
from controller.coaches_controller import CoachesData
from controller.appointment_controller import AppointmentData
from controller.report_controller import ReportsData
from controller.halle_controller import HalleData
from controller.appointment_controller import AppointmentData


class MainWindow():
    def __init__(self, database=None):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "main.ui")
        self.main = uic.loadUi(ui_path)
        self.main.setFixedSize(690, 610) 

        self.db = database 
        self.customer_data = CustomerData(database=self.db)
        self.coaches_data = CoachesData(database=self.db)
        self.halle_data = HalleData(database=self.db) 
        self.appointment_data = AppointmentData(database=self.db)
        self.report_data = ReportsData(database=self.db)

        self.manual = None

        self.initGUI()
        self.main.show()
    def initGUI(self):
        self.main.btnCustomerRegister.triggered.connect(self.open_customer_register)
        self.main.btnAddCustomer.clicked.connect(self.open_customer_register)
        
        self.main.btnCoachAction.triggered.connect(self.open_coach_register)
        self.main.btnAddCoach.clicked.connect(self.open_coach_register)

        self.main.btnHalleAction.triggered.connect(self.open_halle_register)
        self.main.btnAddHalle.clicked.connect(self.open_halle_register)
        
        self.main.btnTerminAction.triggered.connect(self.open_appointment_booking)
        self.main.btnAddTermin.clicked.connect(self.open_appointment_booking)

        self.main.actionBerichte.triggered.connect(self.open_reports)
        self.main.btnReports.clicked.connect(self.open_reports)
        
        self.main.actionProfileBearbeiten.triggered.connect(self.open_profile_administration)
        self.main.btnEditProfile.clicked.connect(self.open_profile_administration)

        self.main.actionHandbuch.triggered.connect(self.open_user_manual)
        
    def open_customer_register(self):
        self.main.hide()  
        self.customer_register = CustomerRegister(customerData=self.customer_data, customer_id=None)
        self.customer_register.register.finished.connect(self.main.show) 
        self.customer_register.register.show()

    def open_coach_register(self):
        self.main.hide()
        self.trainer_register = CoachesRegister(coachesData=self.coaches_data,coach_id=None)
        self.trainer_register.register_coach.finished.connect(self.main.show)
        self.trainer_register.register_coach.show()

    def open_halle_register(self):
        self.main.hide()
        self.halle_window = HalleRegister(halleData=self.halle_data)
        self.halle_window.register.finished.connect(self.main.show) 
        self.halle_window.show()
    

    def open_appointment_booking(self):
        self.main.hide()
        self.appointment_view = AppointmentView(appointmentData=self.appointment_data)
        self.appointment_view.appointment.finished.connect(self.main.show)
        self.appointment_view.appointment.show()

    def open_reports(self):
        self.main.hide()
        self.report_view = ReportView(reportData=self.report_data)
        self.report_view.reports.finished.connect(self.main.show)
        self.report_view.reports.show()

    def open_profile_administration(self):
        self.main.hide()
        self.profile_admin = ProfileAdministration(
            coachesData=self.coaches_data,
            customerData=self.customer_data,
            appointmentData=self.appointment_data,
            halleData=self.halle_data
            
        )
        self.profile_admin.profile.finished.connect(self.main.show)
        self.profile_admin.show()

    def open_user_manual(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, "user_manual.ui")
        self.manual = uic.loadUi(ui_path)
        self.manual.setFixedSize(570, 594)
        self.manual.show()