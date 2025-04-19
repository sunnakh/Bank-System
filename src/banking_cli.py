from bank_system import BankSystem


class BankingCLI:
    def __init__(self):
        self.bank_system = BankSystem()
        self.current_user = None

    def display_menu(self):
        """Display the main menu"""
        print("\n==== Banking System ====")
        if self.current_user:
            print(f"Logged in as: {self.current_user.full_name}")
            print("1. View Accounts")
            print("2. Create New Account")
            print("3. Deposit")
            print("4. Withdraw")
            print("5. Transfer Money")
            print("6. Account Statement")
            print("7. Logout")
        else:
            print("1. Register")
            print("2. Login")
            print("3. Exit")

    def run(self):
        """Main program loop"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")

            if self.current_user:
                self.handle_authenticated_menu(choice)
            else:
                if choice == "1":
                    self.register()
                elif choice == "2":
                    self.login()
                elif choice == "3":
                    print("Thank you for using our banking system!")
                    break
                else:
                    print("Invalid choice. Please try again.")

    def handle_authenticated_menu(self, choice):
        """Handle menu options for authenticated users"""
        if choice == "1":
            self.view_accounts()
        elif choice == "2":
            self.create_account()
        elif choice == "3":
            self.deposit()
        elif choice == "4":
            self.withdraw()
        elif choice == "5":
            self.transfer()
        elif choice == "6":
            self.view_statement()
        elif choice == "7":
            print(f"Goodbye, {self.current_user.full_name}!")
            self.current_user = None
        else:
            print("Invalid choice. Please try again.")

    def register(self):
        """Register a new user"""
        print("\n--- Register New User ---")
        full_name = input("Enter your full name: ")
        phone = input("Enter your phone number: ")
        password = input("Create password: ")

        user = self.bank_system.register_user(full_name, phone, password)
        if user:
            print(f"Registration successful! User ID: {user.user_id}")
            self.current_user = user

    def login(self):
        """Log in a user"""
        print("\n--- User Login ---")
        phone = input("Phone number: ")
        password = input("Password: ")

        user = self.bank_system.login(phone, password)
        if user:
            print(f"Welcome back, {user.full_name}!")
            self.current_user = user

    def view_accounts(self):
        """Display user's accounts"""
        print("\n--- Your Accounts ---")
        account_numbers = self.current_user.get_accounts()

        if not account_numbers:
            print("You don't have any accounts yet.")
            return

        for acc_num in account_numbers:
            account = self.bank_system.get_account(acc_num)
            if account:
                print(
                    f"Account: {acc_num} | Balance: {account.currency} {account.balance:.2f}"
                )

    def create_account(self):
        """Create a new bank account"""
        print("\n--- Create New Account ---")
        currencies = ["USD", "EUR", "GBP"]

        print("Available currencies:")
        for i, curr in enumerate(currencies, 1):
            print(f"{i}. {curr}")

        choice = input("Select currency (1-3): ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(currencies):
                currency = currencies[idx]
                account = self.bank_system.create_account(self.current_user, currency)
                print(
                    f"Account created successfully! Account number: {account.account_number}"
                )
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

    def select_account(self, message="Select an account: "):
        """Helper to select from user's accounts"""
        account_numbers = self.current_user.get_accounts()

        if not account_numbers:
            print("You don't have any accounts.")
            return None

        print("\nYour accounts:")
        for i, acc_num in enumerate(account_numbers, 1):
            account = self.bank_system.get_account(acc_num)
            print(
                f"{i}. Account {acc_num} - Balance: {account.currency} {account.balance:.2f}"
            )

        choice = input(message)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(account_numbers):
                return self.bank_system.get_account(account_numbers[idx])
            else:
                print("Invalid selection.")
                return None
        except ValueError:
            print("Please enter a number.")
            return None

    def deposit(self):
        """Deposit money into an account"""
        print("\n--- Deposit Money ---")
        account = self.select_account("Select account for deposit: ")
        if not account:
            return

        try:
            amount = float(input(f"Enter amount to deposit ({account.currency}): "))
            if account.deposit(amount):
                print(
                    f"Deposit successful! New balance: {account.currency} {account.balance:.2f}"
                )
                self.bank_system.save_to_file()
        except ValueError:
            print("Please enter a valid amount.")

    def withdraw(self):
        """Withdraw money from an account"""
        print("\n--- Withdraw Money ---")
        account = self.select_account("Select account for withdrawal: ")
        if not account:
            return

        try:
            amount = float(input(f"Enter amount to withdraw ({account.currency}): "))
            if account.withdraw(amount):
                print(
                    f"Withdrawal successful! New balance: {account.currency} {account.balance:.2f}"
                )
                self.bank_system.save_to_file()
        except ValueError:
            print("Please enter a valid amount.")

    def transfer(self):
        """Transfer money between accounts"""
        print("\n--- Transfer Money ---")
        from_account = self.select_account("Select source account: ")
        if not from_account:
            return

        to_account_number = input("Enter destination account number: ")
        to_account = self.bank_system.get_account(to_account_number)

        if not to_account:
            print("Destination account not found.")
            return

        if from_account.account_number == to_account.account_number:
            print("Cannot transfer to the same account.")
            return

        try:
            amount = float(
                input(f"Enter amount to transfer ({from_account.currency}): ")
            )
            if from_account.transfer(to_account, amount):
                print(f"Transfer successful!")
                print(
                    f"Source account balance: {from_account.currency} {from_account.balance:.2f}"
                )
                self.bank_system.save_to_file()
        except ValueError:
            print("Please enter a valid amount.")

    def view_statement(self):
        """View transaction history for an account"""
        print("\n--- Account Statement ---")
        account = self.select_account("Select account to view statement: ")
        if not account:
            return

        print(f"\nStatement for Account {account.account_number}")
        print(f"Current Balance: {account.currency} {account.balance:.2f}")
        print("=" * 50)

        statements = account.get_statement()
        for stmt in statements:
            print(stmt)