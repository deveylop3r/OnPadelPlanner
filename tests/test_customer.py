import unittest
from models.customer_model import Customer

class TestCustomerModel(unittest.TestCase):
    def test_valid_customer(self):
        customer = Customer(
            name="Max Mustermann",
            city="Berlin",
            email="max@example.com",
            phone="123-456-789",
            birthdate="01-01-1990"
        )
        is_valid, missing = customer.validateFields()
        self.assertTrue(is_valid)
        self.assertEqual(len(missing), 0)

    def test_invalid_phone_format(self):
        customer = Customer(
            name="Max",
            city="Berlin",
            email="max@example.com",
            phone="abc123",
            birthdate="01-01-1990"
        )
        is_valid, missing = customer.validateFields()
        self.assertFalse(is_valid)
        self.assertIn("Telefon (nur Zahlen und Bindestriche)", missing)

    def test_invalid_email_format(self):
        customer = Customer(
            name="Max",
            city="Berlin",
            email="invalid-email",
            phone="123-456",
            birthdate="01-01-1990"
        )
        is_valid, missing = customer.validateFields()
        self.assertFalse(is_valid)
        self.assertIn("E-Mail (ungültiges Format)", missing)