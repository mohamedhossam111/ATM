import unittest
from customer import Customer
from unittest.mock import MagicMock

class TestCustomer(unittest.TestCase):

    def setUp(self):
        # Create a mock database object
        self.mock_db = MagicMock()
        
        # Create a test customer instance
        self.customer = Customer(user_id=1, username="test_user", pin="1234", account_number=12345678, balance=100.0)

    def test_deposit_funds(self):
        # Simulate the deposit
        self.customer.deposit_funds(self.mock_db, self.customer)
        
        # Verify that the balance is updated correctly
        self.assertEqual(self.customer.balance, 200.0)
        self.mock_db.store_transaction.assert_called_once_with(self.customer.user_id, "Deposit", 100.0, 200.0, "2025-02-06 12:00:00")

    def test_withdraw_cash(self):
        # Simulate withdrawal
        self.customer.withdraw_cash(self.mock_db, self.customer)
        
        # Verify that the balance is updated correctly
        self.assertEqual(self.customer.balance, 50.0)
        self.mock_db.store_transaction.assert_called_once_with(self.customer.user_id, "Withdrawal", 50.0, 50.0, "2025-02-06 12:00:00")

    def test_insufficient_balance_withdrawal(self):
        # Try to withdraw more than available balance
        self.customer.balance = 50.0
        self.customer.withdraw_cash(self.mock_db, self.customer)
        
        # Ensure that the withdrawal was not processed due to insufficient balance
        self.assertEqual(self.customer.balance, 50.0)

if __name__ == "_main_":
    unittest.main()