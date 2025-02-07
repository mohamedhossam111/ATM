import unittest
from customer import Customer
from unittest.mock import MagicMock, patch

class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()
        self.customer = Customer(user_id=1, username="test_user", pin="1234", account_number=12345678, balance=100.0)

    @patch("customer.datetime")
    def test_deposit_funds(self, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "2025-02-06 12:00:00"

        self.customer.deposit_funds(self.mock_db, 100.0)  # Pass only the amount
        
        self.assertEqual(self.customer.balance, 200.0)
        self.mock_db.store_transaction.assert_called_once_with(
            self.customer.user_id, "Deposit", 100.0, 200.0, "2025-02-06 12:00:00"
        )

    @patch("customer.datetime")
    def test_withdraw_cash(self, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "2025-02-06 12:00:00"

        self.customer.withdraw_cash(self.mock_db, 50.0)  # Pass only the amount
        
        self.assertEqual(self.customer.balance, 50.0)
        self.mock_db.store_transaction.assert_called_once_with(
            self.customer.user_id, "Withdrawal", 50.0, 50.0, "2025-02-06 12:00:00"
        )

    def test_insufficient_balance_withdrawal(self):
        self.customer.balance = 50.0
        self.customer.withdraw_cash(self.mock_db, 100.0)  # Trying to withdraw more than balance

        self.assertEqual(self.customer.balance, 50.0)  # Balance should remain unchanged

if __name__ == "__main__":
    unittest.main()