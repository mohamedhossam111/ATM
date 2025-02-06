from datetime import datetime

class Customer:
    def _init_(self, user_id, username, pin, account_number, balance=0.0):
        self.user_id = user_id
        self.username = username
        self.pin = pin
        self.account_number = account_number
        self.balance = balance

def check_balance(db, user):
    balance = db.get_balance(user.user_id)
    print("Your current balance is:", balance)

def deposit_funds(db, user):
    try:
        amount = float(input("Enter the amount to deposit: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount entered. Please try again.")
        return
    
    user.balance += amount
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.store_transaction(user.user_id, "Deposit", amount, user.balance, timestamp)
    db.update_balance(user.user_id, user.balance)
    print("Deposit successful! New balance:", user.balance)

def withdraw_cash(db, user):
    try:
        amount_to_withdraw = float(input("Enter the amount to withdraw: "))
    except ValueError:
        print("Invalid amount entered. Please try again.")
        return

    if amount_to_withdraw <= user.balance:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user.balance -= amount_to_withdraw
        db.store_transaction(user.user_id, "Withdrawal", amount_to_withdraw, user.balance, timestamp)
        db.update_balance(user.user_id, user.balance)
        print("Withdrawal successful! New balance:", user.balance)
    else:
        print("Insufficient balance for withdrawal.")

def transaction_history(db, user):
    print("Transaction History:")
    transactions = db.get_transactions(user.user_id)
    for transaction in transactions:
        date, time, transaction_type, amount, new_balance = transaction[4:9]
        print(f"{date} {time} {transaction_type} {amount} {new_balance}")

def transfer_funds(db, user):
    receiver_username = input("Enter receiver's username: ")
    receiver = db.get_user_by_username(receiver_username)
    if receiver:
        try:
            amount = float(input("Enter the amount to transfer: "))
        except ValueError:
            print("Invalid amount entered. Please try again.")
            return
        
        if user.balance >= amount:
            user.balance -= amount
            receiver_balance = receiver[4]
            receiver_balance += amount
            db.update_balance(user.user_id, user.balance)
            db.update_balance(receiver[0], receiver_balance)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.store_transaction(user.user_id, f"Transfer to {receiver_username}", -amount, user.balance, timestamp)
            db.store_transaction(receiver[0], f"Transfer from {user.username}", amount, receiver_balance, timestamp)
            print("Transfer successful! New balance:", user.balance)
        else:
            print("Insufficient funds.")
    else:
        print("Receiver not found.")
