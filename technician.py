class Technician:
    def __init__(self, username, pin):
        self.username = username
        self.pin = pin

def view_atm_inventory(db):
    # Function to view the ATM inventory
    # Retrieve ATM inventory from the database         
    atm_inventory = db.get_atm_inventory()
    print("ATM Inventory:")
    print(f"Bank Notes: {atm_inventory[0]}")
    print(f"Ink: {atm_inventory[1]}")
    print(f"Printer Paper: {atm_inventory[2]}")
       
def add_bank_note(db):
    # Function to add bank notes to the ATM
    amount = int(input("Enter the number of bank notes to add: "))
    db.update_bank_notes(amount)
    print("Bank notes added successful!")     
    
def update_paper(db):
    # Function to update paper inventory
    amount = int(input("Enter the amount of printer paper to add: "))
    db.update_printer_paper(amount)
    print("Printer paper inventory updated successful!")

def update_ink(db):
    # Function to update ink inventory
    amount = int(input("Enter the amount of ink to add: "))
    db.update_ink(amount)
    print("Ink inventory updated successfully!")

def update_firmware():
    # Function to update firmware
    print("The firmware is updated.")

def update_os():
        # Function to update operating system
        print("The os is updated.")
