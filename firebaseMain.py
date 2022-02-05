# Import firebase libraries to access the cloud
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# import time for quick fix in main
import time
# Importing secret key
import key_handler
# Importing os to access environ
import os

# Create link to firestore and return database
def link_firestore():
    """ Create a link to the cloud firebase """

    # Unique private key to access firebase. Please download new private key if exported from github
    private_key = key_handler.key.get_key()
    # Set environment to the private key so Python can access the cloud
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = private_key

    # Use the application default credentials (and don't forget to set the projectID to your firebase project id)
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
    'projectId': 'fir-python-project-e63c6',
    })

    # Create link and store as "db" to return to main()
    db = firestore.client()
    return db

def create_user(db):
    """ This function will allow the user to create a new account in the firebase """

    # Prompt user for the new account's basic information including an account name and password
    name = input("Enter Account Name: ")
    password = input("Create a Password: ")
    f_name = input("Enter First Name on Account: ")
    m_name = input("Enter Middle Name on Account: ") 
    l_name = input("Enter Last Name on Account: ") 
    age = int(input("Enter User's Age: "))
    acc_balance = float(input("Enter Account Starting Balance: "))

    # Check to see if this account exists already. If it does, prompt the user for a different account name
    doc = db.collection("users").document(name).get()
    if doc.exists:
        print("Account Name Already Exists!")
        return
    
    # Compact the user's inputed data into a single dictionary
    user_info = {"first_name" : f_name,
                "middle_name" : m_name,
                "last_name" : l_name,
                "age" : age,
                "account_balance" : acc_balance,
                "password" : password}
    # Now throw that data into the collection "users" and into the new document (account) they just made
    db.collection("users").document(name).set(user_info)

    # Prompt the firestore log to create a log of the new account being made
    firestore_log(db, f"Created new account user {name}")

def display_accounts(db):
    """ This funtion will access the collection and display the names of all the accounts available
        Without disclosing any private information like passwords """

    # Save all collection into users
    users = db.collection("users")
    # Using the stream() function will allow all of the items into of the collection to be retrieved one at a time
    # This would ideally save space compared to get() which would withdraw all account at once
    accounts = users.stream()
    
    # Loop through the accounts being streamed in and print their names.
    # ***Change this to be a map instead because "for" loops are evil
    for account in accounts:
        print(f"{account.id}")

def edit_account(db, acc_data, acc_name):
    """ This function will allow the user to make changes to an existing account they've already acquired access to
        then apply those changes to the firebase """

    # Selector will allow menu navigation
    selector = None
    # passing in acc_data from the access_account() to allow the user to change data in their document
    acc_data = acc_data

    # This loop will allow the user to continue to make changes until they finish or until the account is deleted
    while selector != "0":
        # List options
        print()
        print("0) Exit Editor")
        print("1) Change First Name")
        print("2) Change Middle Name")
        print("3) Change Last Name")
        print("4) Change Age")
        print("5) Make Deposit")
        print("6) Make Withdrawal")
        print("7) Change Password")
        print("66) Delete Account Completely") # Execute order 66 to delete account
        selector = input(">> ")
        print()
        # if statement to allow user input to do something. This will also not crash if invalid input is entered
        if selector == "1":
            new_f_name = input("Enter New First Name: ")                        # Prompt for new name
            acc_data["first_name"] = new_f_name                                 # Make change in local variable
            db.collection("users").document(acc_name).set(acc_data)             # Commit change to firebase using .set()
            firestore_log(db, f"Account {acc_name}'s first name was changed!")  # Note change in log
        elif selector == "2":
            new_m_name = input("Enter New Middle Name: ")                       # Same as above but with middle name
            acc_data["middle_name"] = new_m_name
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s middle name was changed!")
        elif selector == "3":
            new_l_name = input("Enter New Last Name: ")                         # Same as above but with last name
            acc_data["last_name"] = new_l_name
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s last name was changed!")
        elif selector == "4":
            new_age = input("Enter New Age: ")                                  # Prompt user for new age
            acc_data["age"] = new_age                                           # Make age change in local variable
            db.collection("users").document(acc_name).set(acc_data)             # Apply change to firebase
            firestore_log(db, f"Account {acc_name}'s age was changed!")         # Log change
        elif selector == "5":
            deposit_amount = float(input("Enter Amount to Deposit: "))                      # Prompt for amount of money to add to account
            acc_data["account_balance"] += deposit_amount                                   # Add to existing amount
            db.collection("users").document(acc_name).set(acc_data)                         # Make change to firebase
            firestore_log(db, f"Account {acc_name}'s account balance was increased!")       # Log change
        elif selector == "6":
            withdrawal_amount = float(input("Enter Amount to Withdraw: "))                  # Prompt for amount of money to withdraw
            if acc_data["account_balance"] >= withdrawal_amount:                            # Create if statement to prevent user from going negative
                acc_data["account_balance"] -= withdrawal_amount                            # Subtract withdrawal amount
                db.collection("users").document(acc_name).set(acc_data)                     # Apply change to firebase
                firestore_log(db, f"Account {acc_name}'s account balance was decreased!")   # Log change
            else:
                print("Insufficient Funds in Balance to Make That Withdrawal!")             # Warn user they don't have enough money
        elif selector == "7":
            new_password = input("Enter New Password: ")                                    # Same as name changing code found above
            acc_data["password"] = new_password
            db.collection("users").document(acc_name).set(acc_data)
            firestore_log(db, f"Account {acc_name}'s password was changed!")
        elif selector == "66":
            confirm = input("Are you sure you want to delete this account? (Y/N): ") in ["Y", 'y'] # Prompt user for confirmation (save as boolean)
            if confirm: 
                db.collection("users").document(acc_name).delete()                                  # Use .delete() to remove document from firebase
                firestore_log(db, f"It's been a pleasure {acc_name}! (Account Deleted)")            # Log change
                selector = "0"                                                                      # Exit the user from this while loop because account was deleted
                break
            else:
                print("Delete Canceled")                                                            # Inform user that deletion command was averted 

def access_account(db):
    """ This function will allow the user to access their account through password/username verification. 
        This can alternatively be done on the firebase side, but for this example we'll include it in the code """

    # Create menu navigator
    navi = None
    # While they are choosing an account to log into, loop
    while navi != "0":
        # List options
        print()
        print("0) Return to Previous Screen")
        print("1) Display All Available Accounts")
        print("2) Begin Log In")
        navi = input(">> ")
        print()
        # if statement to allow functionality to user input. Will not crash to invalid input
        if navi == "1":
            # Display all available account names w/o showing private information by using the display_account() function
            display_accounts(db)
        elif navi == "2":
            # Prompt user for the account name they want to access
            acc_name = input("Enter account name: ")
            # Behind the scenes, withdraw that account's password for check
            db_doc = db.collection("users").document(acc_name).get()
            # Verify that account does exist
            if db_doc.exists:
                acc_data = db_doc.to_dict()                         # Convert above retrieved information into readable format
                acc_password = input("Enter account password: ")    # Prompt user for password
                db_password = acc_data["password"]                  # Compare password to actual password
                if db_password == acc_password:                     # If valid, enter logged menu
                    logged = None                                   # Create second navigation variable
                    while logged != "0":
                        # List logged in options
                        print()
                        print("0) Exit Account")
                        print("1) Display All Info")
                        print("2) Edit Account Info or Make Withdrawal/Deposit")
                        logged = input(">> ")
                        print()
                        # if statement to allow functionality. Also will not crash from incorrect input
                        if logged == "1":
                            # Display all account information in dictionary format to user
                            print(f"Account info: {acc_data}")
                        elif logged == "2":
                            # Move user to the edit_account() function and menu
                            edit_account(db, acc_data, acc_name)
                            # Changed logged to "0" so they exit their account when they return
                            # This will prevent them from reaccessing their account if it's deleted
                            logged = "0"
                else:
                    print("Password Incorrect!") # Wrong password warning
            else:
                print("Account Name Doesn't Exist!") # Account doesn't exist warning

def firestore_log(db, to_log):
    """ This function will apply the log report to the firebase """

    # Store log information into a single dictionary including the message and timestamp
    log_info = {"update" : to_log, 
                "time" : firestore.SERVER_TIMESTAMP}
    # Ship information to separate collection named "log" for record keeping
    db.collection("log").add(log_info)


def balance_alert(results, changes, read_time):
    """ This function will create an alert to react to the balance_notification's on_snapshot.
        This will warn the user if an account's balance is too low. """

    # Firebase will feed all changes into here which we can sort through
    for change in changes:
        # If a blip is "heard" with the name "ADDED," then we know someone's balance is low
        if change.type.name == "ADDED": 
            # Print notification to screen
            print()
            print(f"The account balance for user {change.document.id} is below $100!")
            print("Be careful not to over withdraw!")
            print()
        # If blip is "heard" with the name "REMOVED," then a problem was resolved
        elif change.type.name == "REMOVED":
            # Print resolved notification to screen
            print()
            print(f"The account balance for user {change.document.id} is back above $100!")
            print("Spend wisely!")
            print()

def balance_notification(db):
    """ This function will create an on_snapshot listener to monitor the program """

    # If a user's account balance falls below $100, this will alert them to be careful spending
    db.collection("users").where("account_balance", "<", 100).on_snapshot(balance_alert)


def main():
    """ This function runs the entire program and loops menu """

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

# Runs program in VSCode when called
if __name__ == '__main__':
    main()