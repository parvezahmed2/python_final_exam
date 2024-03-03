from abc import ABC, abstractmethod

class User(ABC):
    account_num_counter = 1  
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_num = User.account_num_counter
        User.account_num_counter += 1
        self.balance = 0
        self.loan = 0
        self.transaction_history = []

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.transaction_history.append(f'Deposit: +${amount}')
            print(f'After deposit, your current balance is ${self.balance}')
        else:
            print("INVALID DEPOSIT AMOUNT!")

    def withdraw(self, amount):
        if amount >= 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f'Withdrawal: -${amount}')
            print("SUCCESSFULLY WITHDRAWN!")
        else:
            print("WITHDRAWAL AMOUNT EXCEEDED")

    def check_available_balance(self):
        return f'{self.name}: Your available balance is ${self.balance}'

    def get_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.loan < 2 and amount > 0:
            self.balance += amount
            self.loan += 1
            self.transaction_history.append(f'Loan taken: +${amount}')
            print(f'You successfully took a loan of ${amount}. Your new balance is ${self.balance}')
        else:
            print('You cannot take a loan. Your current balance is ${self.balance}.')

class Savings(User):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Savings")

class Current(User):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Current")

class Admin:
    def __init__(self):
        self.users = []

    def create_account(self, name, email, address, account_type):
        if account_type.lower() == "savings":
            user = Savings(name, email, address)
        elif account_type.lower() == "current":
            user = Current(name, email, address)
        else:
            print("Invalid account type. Choose 'Savings' or 'Current'.")
            return

        self.users.append(user)
        return user

    def delete_account(self, user):
        if user in self.users:
            self.users.remove(user)
            print(f"Account of {user.name} has been deleted.")
        else:
            print("Account not found.")

    def view_user_accounts_list(self):
        for user in self.users:
            print(f"Account Number: {user.account_num}, Name: {user.name}, Account Type: {user.account_type}")

    def total_available_balance(self):
        total_balance = sum(user.balance for user in self.users)
        return f"Total Available Balance: ${total_balance}"

    def total_loan_amount(self):
        total_loan = sum(user.balance for user in self.users if user.loan > 0)
        return f"Total Loan Amount: ${total_loan}"

    def on_off_loan_feature(self, enable):
        for user in self.users:
            user.loan = 0 if enable else 2 

def user_login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    return next((user for user in admin.users if user.email == email), None)

admin = Admin()

while True:
    print("\n<-- BANKING SYSTEM -->")
    print("1. Register")
    print("2. Log In")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        account_type = input("Enter account type (Savings or Current): ")
        password = input("Create a password: ")
        user = admin.create_account(name, email, address, account_type)
        user.password = password
        print(f"Account created. Your account number is {user.account_num}.")

    elif choice == "2":
        logged_in_user = user_login()
        if logged_in_user:
            password = input("Enter your password: ")
            if hasattr(logged_in_user, 'password') and logged_in_user.password == password:
                print(f"Welcome, {logged_in_user.name}!")
                while True:
                    print("\n<-- USER MENU -->")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transaction History")
                    print("5. Take Loan")
                    print("6. Log Out")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        amount = float(input("Enter the amount to deposit: "))
                        logged_in_user.deposit(amount)
                    elif user_choice == "2":
                        amount = float(input("Enter the amount to withdraw: "))
                        logged_in_user.withdraw(amount)
                    elif user_choice == "3":
                        print(logged_in_user.check_available_balance())
                    elif user_choice == "4":
                        print(logged_in_user.get_transaction_history())
                    elif user_choice == "5":
                        amount = float(input("Enter the amount to loan: "))
                        logged_in_user.take_loan(amount)
                    elif user_choice == "6":
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Incorrect password.")
        else:
            print("User not found. Please register first.")

    elif choice == "3":
        break