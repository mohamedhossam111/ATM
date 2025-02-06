from database_manager import DatabaseManager
from customer import Customer, deposit_funds, withdraw_cash, transaction_history, transfer_funds, check_balance
from technician import Technician, view_atm_inventory, add_bank_note, update_paper, update_ink, update_firmware, update_os
from random import randint

def main():
    atm_db = DatabaseManager()
    atm_db.initialize_atm_inventory()

    while True:
        print("Welcome to the ATM system!")
        print("1. Sign In")
        print("2. Sign Up")
        print("3. Technician Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            sign_in(atm_db)
        elif choice == "2":
            sign_up(atm_db)
        elif choice == "3":
            technician_login(atm_db)
        elif choice == "4":
            print("Exiting ATM system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def sign_in(db):
    username = input("Enter your username: ")
    pin = input("Enter your pin: ")

    user = db.authenticate_user(username, pin)
    if user:
        print("Sign in successful!")
        logged_in_user = Customer(*user)
        show_customer_menu(db, logged_in_user)
    else:
        print("Invalid username or pin. Please try again.")

def sign_up(db):
    username = input("Enter a new username: ")
    pin = input("Enter a pin: ")

    account_number = generate_account_number(db)
    db.store_user(username, pin, account_number)
    print("Sign up successful!")

def generate_account_number(db):
    while True:
        account_number = randint(10000000, 99999999)
        db.cursor.execute("SELECT id FROM users WHERE account_number=?", (account_number,))
        if not db.cursor.fetchone():
            return account_number

def technician_login(db):
    username = input("Enter technician username: ")
    pin = input("Enter technician pin: ")

    if username == "john" and pin == "8888":
        print("Technician login successful!")
        technician = Technician(username, pin)
        show_technician_menu(db, technician)
    else:
        print("Invalid technician username or pin. Please try again.")

def show_customer_menu(db, user):
    while True:
        print("\nLogged in as:", user.username)
        print("1. Deposit Funds")
        print("2. Withdraw Cash")
        print("3. Transaction History")
        print("4. Transfer Funds")
        print("5. Check Balance")
        print("6. Log Out")
        choice = input("Enter your choice: ")

        if choice == "1":
            deposit_funds(db, user)
        elif choice == "2":
            withdraw_cash(db, user)
        elif choice == "3":
            transaction_history(db, user)
        elif choice == "4":
            transfer_funds(db, user)
        elif choice == "5":
            check_balance(db, user)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def show_technician_menu(db, technician):
    while True:
        print("\nLogged in as Technician")
        print("1. View ATM Inventory")
        print("2. Add Bank Note")
        print("3. Update Paper Inventory")
        print("4. Update Ink Inventory")
        print("5. Update Firmware")
        print("6. Update Operating System")
        print("7. Log Out")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_atm_inventory(db)
        elif choice == "2":
            add_bank_note(db)
        elif choice == "3":
            update_paper(db)
        elif choice == "4":
            update_ink(db)
        elif choice == "5":
            update_firmware()
        elif choice == "6":
            update_os()
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

if _name_ == "_main_":
    main()
