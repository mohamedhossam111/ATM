import sqlite3

class DatabaseManager:
    def _init_(self, db_name="atm_system.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.initialize_tables()

    def initialize_tables(self):
        # Create tables for users, technicians, and transaction history
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               username TEXT NOT NULL,
                               pin TEXT NOT NULL,
                               account_number INTEGER UNIQUE NOT NULL,
                               balance REAL DEFAULT 0)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               user_id INTEGER,
                               amount REAL,
                               transaction_type TEXT,
                               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                               FOREIGN KEY(user_id) REFERENCES users(id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS atm_inventory (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               paper_count INTEGER DEFAULT 0,
                               ink_level INTEGER DEFAULT 100,
                               firmware_version TEXT,
                               os_version TEXT)''')
        self.connection.commit()

    def store_user(self, username, pin, account_number):
        self.cursor.execute("INSERT INTO users (username, pin, account_number) VALUES (?, ?, ?)",
                            (username, pin, account_number))
        self.connection.commit()

    def authenticate_user(self, username, pin):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND pin=?", (username, pin))
        return self.cursor.fetchone()

    def get_user_by_account_number(self, account_number):
        self.cursor.execute("SELECT * FROM users WHERE account_number=?", (account_number,))
        return self.cursor.fetchone()

    def update_balance(self, user_id, amount):
        self.cursor.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, user_id))
        self.connection.commit()

    def store_transaction(self, user_id, amount, transaction_type):
        self.cursor.execute("INSERT INTO transactions (user_id, amount, transaction_type) VALUES (?, ?, ?)",
                            (user_id, amount, transaction_type))
        self.connection.commit()

    def initialize_atm_inventory(self):
        # Set initial inventory in ATM
        self.cursor.execute('''INSERT OR REPLACE INTO atm_inventory (id, paper_count, ink_level, firmware_version, os_version) 
                               VALUES (1, 1000, 100, 'v1.0', 'v1.0')''')
        self.connection.commit()

    def view_atm_inventory(self):
        self.cursor.execute("SELECT * FROM atm_inventory WHERE id=1")
        return self.cursor.fetchone()

    def add_bank_note(self, notes):
        self.cursor.execute("UPDATE atm_inventory SET paper_count = paper_count + ? WHERE id=1", (notes,))
        self.connection.commit()

    def update_paper(self, amount):
        self.cursor.execute("UPDATE atm_inventory SET paper_count = ? WHERE id=1", (amount,))
        self.connection.commit()

    def update_ink(self, ink_level):
        self.cursor.execute("UPDATE atm_inventory SET ink_level = ? WHERE id=1", (ink_level,))
        self.connection.commit()

    def update_firmware(self, version):
        self.cursor.execute("UPDATE atm_inventory SET firmware_version = ? WHERE id=1", (version,))
        self.connection.commit()

    def update_os(self, version):
        self.cursor.execute("UPDATE atm_inventory SET os_version = ? WHERE id=1", (version,))
        self.connection.commit()

    def close(self):
        self.connection.close()
