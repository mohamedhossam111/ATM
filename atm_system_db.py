import sqlite3

class DatabaseManager:
    def __init__(self):  # Fixed the constructor
        self.connection = sqlite3.connect("atm.db")
        self.cursor = self.connection.cursor()

    def initialize_atm_inventory(self):
        # Create the tables if they do not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                pin TEXT,
                account_number INTEGER,
                balance REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                transaction_type TEXT,
                amount REAL,
                date TEXT,
                time TEXT,
                new_balance REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS atm_inventory (
                id INTEGER PRIMARY KEY,
                bank_notes INTEGER,
                ink INTEGER,
                printer_paper INTEGER
            )
        ''')
        self.connection.commit()

    def store_user(self, username, pin, account_number):
        self.cursor.execute('''
            INSERT INTO users (username, pin, account_number, balance)
            VALUES (?, ?, ?, ?)
        ''', (username, pin, account_number, 0.0))
        self.connection.commit()

    def authenticate_user(self, username, pin):
        self.cursor.execute('''
            SELECT id, username, pin, account_number, balance
            FROM users WHERE username=? AND pin=?
        ''', (username, pin))
        return self.cursor.fetchone()

    def get_balance(self, user_id):
        self.cursor.execute('''
            SELECT balance FROM users WHERE id=?
        ''', (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None  # Added a safety check

    def store_transaction(self, user_id, transaction_type, amount, new_balance, timestamp):
        date, time = timestamp.split()
        self.cursor.execute('''
            INSERT INTO transactions (user_id, transaction_type, amount, date, time, new_balance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, transaction_type, amount, date, time, new_balance))
        self.connection.commit()

    def update_balance(self, user_id, new_balance):
        self.cursor.execute('''
            UPDATE users SET balance=? WHERE id=?
        ''', (new_balance, user_id))
        self.connection.commit()

    def get_transactions(self, user_id):
        self.cursor.execute('''
            SELECT * FROM transactions WHERE user_id=?
        ''', (user_id,))
        return self.cursor.fetchall()

    def get_user_by_username(self, username):
        self.cursor.execute('''
            SELECT * FROM users WHERE username=?
        ''', (username,))
        return self.cursor.fetchone()

    def get_atm_inventory(self):
        self.cursor.execute('''
            SELECT bank_notes, ink, printer_paper FROM atm_inventory WHERE id=1
        ''')
        return self.cursor.fetchone()

    def update_bank_notes(self, amount):
        self.cursor.execute('''
            UPDATE atm_inventory SET bank_notes = bank_notes + ? WHERE id=1
        ''', (amount,))
        self.connection.commit()

    def update_printer_paper(self, amount):
        self.cursor.execute('''
            UPDATE atm_inventory SET printer_paper = printer_paper + ? WHERE id=1
        ''', (amount,))
        self.connection.commit()

    def update_ink(self, amount):
        self.cursor.execute('''
            UPDATE atm_inventory SET ink = ink + ? WHERE id=1
        ''', (amount,))
        self.connection.commit()