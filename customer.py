from datetime import datetime
class customer:
    def __init__(self, user_id, username, pin, account_number, balance=0.0):
        self.user_id = user_id
        self.username = username
        self.pin = pin
        self.account_number = account_number
        self.balance = balance

def check_balance(db, user):
    balance = db.get_balance(user.user_id)
    print("Your current balance is :", balance)

def deposit_funds(db, user):
    amount = float(input("enter the amount to deposit:  "))
    user.balance += amount
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  #Get current time
    new_balance = user.balance # Calculate new balance
    db.store_transaction(user.user_id, "Deposit", amount, new_balance ,timestamp)
    db.update_balance(user.user_id, user.balance) # Update balance in the database
    print("deposit successful! New balance:", user.balance)

def withdraw_cash(db, user):
    amount_to_withdraw = float(input("Enter the amountto withdraw:  "))

    if amount_to_withdraw <= user.balance:
        # Sufficient balance for withdrawal
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S:') # Get current timestamp
        user.balance -= amount_to_withdraw
        new_balance = user.balance # Calculate new balance
        db.store_transaction(user.user_id, "Withdrawal" , amount_to_withdraw, new_balance, timestamp)
        db.update_balance(user.user_id, user.balance) # Update balance in the database
        print("Withdrawal successful! New balance:", user.balance)
    else:    
        print("Insufficient balance for withdrawal.")

def transaction_history(db, user):
    print("Transaction History:")
    
    print("{:<15} {:<15} {:<25} {:<15} {:<15}".format("Date", "Time", "Type", "Amount", "New balance"))
    transactions = db.get_transactions(user.user_id)
    for transaction in transactions:
        # Print(transaction)  # Print the transaction tuple for debugging
        if len(transaction) >= 7:
            _, _, transaction_type, amount, date, time, new_balance, _ = transaction[:8]
            new_balance = new_balance if new_balance is not None else "N/A"
            print("{:<15} {:<15} {:<25} {:<15} {:<15}".format(date, time, transaction_type, amount, new_balance))
        else:
            print("Invalid transaction format:", transaction)

def transfer_funds(db, user):
    receiver_username = input("Enter receiver's username: ")
    receiver = db.get_user_by_username(receiver_username)
    if receiver:
        amount = float(input("Enter the amount to transfer: "))
        if user.balance >= amount:
            user.balance -= amount
            receiver_balance = receiver[4]  # Assuming balance is at index 4 in the tuple
            receiver_balance += amount
            db.update_balance(user.user_id, user.balance)  # Update sender's balance
            db.update_balance(receiver[0], receiver_balance)  # Update receiver's balance
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp
            db.store_transaction(user.user_id, f"Transfer to {receiver_username}", -amount, user.balance, timestamp)
            db.store_transaction(receiver[0], f"Transfer from {user.username}", amount, receiver_balance, timestamp)
            print("Transfer successful! New balance:", user.balance)
        else:
            print("Insufficient funds.")
    else:
        print("Receiver not found.")