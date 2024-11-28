import unittest
from unittest.mock import Mock
from controller.appointment_controller import AppointmentData

class TestAppointmentController(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.mock_cursor = Mock()
        self.mock_db.getConnection.return_value = self.mock_db
        self.mock_db.cursor.return_value = self.mock_cursor
        self.appointment_data = AppointmentData(self.mock_db)

    def test_calculate_price(self):
        
        self.mock_cursor.fetchone.return_value = (40, 45, 30, 35)  
        
        
        price_morning = self.appointment_data.calculate_price(1, "Einzel", 60, "10:00")
        self.assertEqual(price_morning, 40)
        
       
        price_afternoon = self.appointment_data.calculate_price(1, "Einzel", 60, "15:00")
        self.assertEqual(price_afternoon, 45)
        
      
        price_90min = self.appointment_data.calculate_price(1, "Einzel", 90, "10:00")
        self.assertEqual(price_90min, 40 * 1.5)

        
        self.mock_cursor.fetchone.return_value = None
        price_no_data = self.appointment_data.calculate_price(1, "Einzel", 60, "10:00")
        self.assertIsNone(price_no_data)

    def test_can_modify_appointment(self):
        future_date = "2025-01-01"
        can_modify, message = self.appointment_data.can_modify_appointment(future_date)
        self.assertTrue(can_modify)