class Technician:
    def _init_(self, username, pin):
        self.username = username
        self.pin = pin

def view_atm_inventory(db):
    atm_inventory = db.get_atm_inventory()
    print("ATM Inventory:")
    print(f"Bank Notes: {atm_inventory[0]}")
    print(f"Ink: {atm_inventory[1]}")
    print(f"Printer Paper: {atm_inventory[2]}")

def add_bank_note(db):
    amount = int(input("Enter the number of bank notes to add: "))
    db.update_bank_notes(amount)
    print("Bank notes added successfully!")

def update_paper(db):
    amount = int(input("Enter the amount of printer paper to add: "))
    db.update_printer_paper(amount)
    print("Printer paper inventory updated successfully!")

def update_ink(db):
    amount = int(input("Enter the amount of ink to add: "))
    db.update_ink(amount)
    print("Ink inventory updated successfully!")

def update_firmware():
    print("The firmware is updated.")

def update_os():
    print("The OS is updated.")
