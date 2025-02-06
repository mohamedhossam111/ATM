import unittest
from datetime import datetime
from customer import Customer, deposit_funds
from database_manager import DatabaseManager

class TestIntegration(unittest.TestCase):

    def setUp(self):
        # Set up the database manager
        self.db = DatabaseManager()
        self.db.initialize_atm_inventory()  # Make sure the db is initialized

        # Create a test user
        self.db.store_user("test_user", "1234", 12345678)

        # Fetch the user from the database
        self.user_data = self.db.authenticate_user("test_user", "1234")
        self.user = Customer(*self.user_data)

    def test_deposit_integration(self):
        initial_balance = self.user.balance
        deposit_funds(self.db, self.user)
        
        # Check if balance is updated correctly after deposit
        self.assertEqual(self.user.balance, initial_balance + 100.0)
        
        # Verify that the transaction was stored in the database
        transactions = self.db.get_transactions(self.user.user_id)
        self.assertGreater(len(transactions), 0)
        self.assertEqual(transactions[0][2], "Deposit")

if _name_ == '_main_':
    unittest.main()
