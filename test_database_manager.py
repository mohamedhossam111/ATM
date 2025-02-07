import unittest
from database_manager import DatabaseManager
from unittest.mock import MagicMock

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        # Mock the actual database connection
        self.mock_db = MagicMock()
        self.db_manager = DatabaseManager()
        self.db_manager.connection = self.mock_db

    def test_store_user(self):
        self.db_manager.store_user("test_user", "1234", 12345678)
        self.mock_db.execute.assert_called_with(
            'INSERT INTO users (username, pin, account_number, balance) VALUES (?, ?, ?, ?)',
            ("test_user", "1234", 12345678, 0.0)
        )

    def test_get_balance(self):
        # Mock the database response
        self.mock_db.fetchone.return_value = (100.0,)
        balance = self.db_manager.get_balance(1)
        self.assertEqual(balance, 100.0)

    def test_update_balance(self):
        self.db_manager.update_balance(1, 150.0)
        self.mock_db.execute.assert_called_with(
            'UPDATE users SET balance=? WHERE id=?', (150.0, 1)
        )

