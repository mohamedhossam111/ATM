import sqlite3
import hashlib
from random import randint
from datetime import datetime

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager,cls).__new__(cls)
            cls._instance.connection = sqlite3.connect('atm.db')
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance.create_tables()
        return cls._instance
    
    def create_tables(self):
        # create tables if they don't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users ( 
                                id INTEGER PRIMARY KEY, 
                                username TEXT UNIQUE,
                                pin TEXT,
                                account_number INTEGER UNIQUE,
                                balance REAL DEFAULT 0)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                type TEXT,
                                amount REAL,
                                date TEXT,
                                time TEXT,
                                new_balance REAL,
                                timestamp TEXT,
                                FOREIGN KEY(user_id) REFERENCES users(id))''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS atm_inventory (
                               bank_notes INTEGER DEFAULT 4000,
                               ink INTEGER DEFAULT 25,
                               printer_paper INTEGER DEFAULT 20)''')
        self.connection.commit()

    def authenticate_user(self, username, pin):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND pin=?", (username, hashlib.sha256(pin.encode()).hexdigest()))
        return self.cursor.fetchone()
    
    def store_user(self, username, pin, account_number):
        self.cursor.execute("INSERT INTO users (username, pin, account_number) VALUES (?, ?, ?)", (username, hashlib.sha256(pin.encode()).hexdigest(), account_number))
        self.connection.commit()

    def store_transaction(self, user_id, transaction_type, amount, new_balance, timestamp):
        self.cursor.execute("INSERT INTO transactions (user_id, type, amount, new_balance, date, time, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (user_id, transaction_type, amount, new_balance, datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S:'), timestamp))
        self.connection.commit()

    def get_user_by_username(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()

    def get_atm_inventory(self):
        self.cursor.execute("SELECT * FROM atm_inventory")
        return self.cursor.fetchone()

    def update_bank_notes(self, amount):
        self.cursor.execute("UPDATE atm_inventory SET bank_notes=bank_notes+?", (amount,))
        self.connection.commit()

    def update_ink(self, amount):
        self.cursor.execute("UPDATE atm_inventory SET ink=ink+?", (amount,))
        self.connection.commit()

    def update_printer_paper(self, amount):
        self.cursor.execute("UPDATE atm_inventory SET printer_paper=printer_paper+?", (amount,))
        self.connection.commit()

    def initialize_atm_inventory(self):
        # SET initial amount for banknotes, printer paper, and ink
        self.cursor.execute("INSERT INTO atm_inventory DEFAULT VALUES")
        self.connection.commit()

    def update_balance(self, user_id, new_balance):
        self.cursor.execute("UPDATE users SET balance =? WHERE id=?", (new_balance, user_id))
        self.connection.commit()
    
    def get_balance(self, user_id):
        self.cursor.execute("SELECT balance FROM users WHERE id=?",(user_id,))
        return self.cursor.fetchone()[0]

    # database_manger.py
    def get_transactions(self, user_id):
        self.cursor.execute("SELECT * FROM transactions WHERE user_id=?", (user_id,))
        return self.cursor.fetchall()