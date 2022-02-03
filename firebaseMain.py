import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import key_handler
import os

def link_firestore():
    """ Create a link to the cloud firebase """

    private_key = key_handler.key.get_key()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = private_key

    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
    'projectId': 'fir-python-project-e63c6',
    })

    db = firestore.client()
    return db

def create_user(db):
    name = input("Enter Account Name: ")
    password = input("Create a Password: ")
    f_name = input("Enter First Name on Account: ")
    m_name = input("Enter Middle Name on Account: ") 
    l_name = input("Enter Last Name on Account: ") 
    age = int(input("Enter User's Age: "))
    acc_balance = float(input("Enter Account Starting Balance: "))

    doc = db.collection("users").document(name).get()
    if doc.exists:
        print("Account Name Already Exists!")
        return
    
    user_info = {"first_name" : f_name,
                "middle_name" : m_name,
                "last_name" : l_name,
                "age" : age,
                "account_balance" : acc_balance,
                "password" : password}
    db.collection("users").document(name).set(user_info)

    firestore_log(db, f"Created new account user {name}")

def display_accounts(db):
    users = db.collection("users")
    accounts = users.stream()
    
    for account in accounts:
        print(f"{account.id}")

def edit_account(db, acc_data, acc_name):
    selector = None
    acc_data = acc_data
    while selector != "0":
        print()
        print("0) Exit Editor")
        print("1) Change First Name")
        print("2) Change Middle Name")
        print("3) Change Last Name")
        print("4) Change Age")
        print("5) Make Deposit")
        print("6) Make Withdrawal")
        print("7) Change Password")
        print("66) Delete Account Completely")
        selector = input(">> ")
        print()
        if selector == "1":
            new_f_name = input("Enter New First Name: ")
            acc_data["first_name"] = new_f_name
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s first name was changed!")
        elif selector == "2":
            new_m_name = input("Enter New Middle Name: ")
            acc_data["middle_name"] = new_m_name
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s middle name was changed!")
        elif selector == "3":
            new_l_name = input("Enter New Last Name: ")
            acc_data["last_name"] = new_l_name
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s last name was changed!")
        elif selector == "4":
            new_age = input("Enter New Age: ")
            acc_data["age"] = new_age
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s age was changed!")
        elif selector == "5":
            deposit_amount = float(input("Enter Amount to Deposit: "))
            acc_data["account_balance"] += deposit_amount
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s account balance was increased!")
        elif selector == "6":
            withdrawal_amount = float(input("Enter Amount to Withdraw: "))
            if acc_data["account_balance"] >= withdrawal_amount:
                acc_data["account_balance"] -= withdrawal_amount
                db.collection("users").document(acc_name).set(acc_data)
                firestore_log(db, f"Account {acc_name}'s account balance was decreased!")
            else:
                print("Insufficient Funds in Balance to Make That Withdrawal!")
        elif selector == "7":
            new_password = input("Enter New Password: ")
            acc_data["password"] = new_password
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s password was changed!")
        elif selector == "66":
            confirm = input("Are you sure you want to delete this account? (Y/N): ") in ["Y", 'y']
            if confirm:
                db.collection("users").document(acc_name).delete()
                firestore_log(db, f"It's been a pleasure {acc_name}! (Account Deleted)")
                selector = "0"
                break
            else:
                print("Delete Canceled")

def access_account(db):
    navi = None
    while navi != "0":
        print()
        print("0) Return to Previous Screen")
        print("1) Display All Available Accounts")
        print("2) Begin Log In")
        navi = input(">> ")
        print()
        if navi == "1":
            display_accounts(db)
        elif navi == "2":
            acc_name = input("Enter account name: ")
            db_doc = db.collection("users").document(acc_name).get()
            if db_doc.exists:
                acc_data = db_doc.to_dict()
                acc_password = input("Enter account password: ")
                db_password = acc_data["password"]
                if db_password == acc_password:
                    logged = None
                    while logged != "0":
                        print()
                        print("0) Exit Account")
                        print("1) Display All Info")
                        print("2) Edit Account Info or Make Withdrawal/Deposit")
                        logged = input(">> ")
                        print()
                        if logged == "1":
                            print(f"Account info: {acc_data}")
                        elif logged == "2":
                            edit_account(db, acc_data, acc_name)
                            logged = "0"
                else:
                    print("Password Incorrect!")
            else:
                print("Account Name Doesn't Exist!")

def firestore_log(db, to_log):
    log_info = {"update" : to_log, 
                "time" : firestore.SERVER_TIMESTAMP}
    db.collection("log").add(log_info)


def balance_alert(results, changes, read_time):
    
    for change in changes:
        if change.type.name == "ADDED":
            print()
            print(f"The account balance for user {change.document.id} is below $100!")
            print("Be careful not to over withdraw!")
            print()
        elif change.type.name == "REMOVED":
            print()
            print(f"The account balance for user {change.document.id} is back above $100!")
            print("Spend wisely!")

def balance_notification(db):
    
    db.collection("users").where("account_balance", "<", 100).on_snapshot(balance_alert)



# Runs the entire program and loops menu
def main():
    # Establish link with firebase db and return the db
    db = link_firestore()
    # Initialize notification system to check account balances
    balance_notification(db)
    # Create menu navigation variable
    option = None
    # Added sleep so that notification system can send notice before menu runs 
    # Delete this and add better wait
    time.sleep(1)
    # Main terminal menu options: display all options first then let user input
    while option != "0":
        print()
        print("0) Exit Program")
        print("1) Create New User")
        print("2) Check All Users")
        print("3) Log Into Account")
        option = input(">> ")
        print()
        # if statement will enable user input to have an effect. Incorrect input will not break loop
        if option == "1":
            create_user(db)
        elif option =="2":
            display_accounts(db)
        elif option == "3":
            access_account(db)

    # Exited program statement
    print("Program exited...")
    print()
    print("Have a great day!")
    print()

if __name__ == '__main__':
    main()