import json
import os
from typing import Dict, Optional

from user import User
from bank_account import BankAccount


class BankSystem:
    def __init__(self, data_file: str = "bank_data.json"):
        self.users: Dict[int, User] = {}
        self.accounts: Dict[str, BankAccount] = {}
        self.data_file = data_file
        self.next_user_id = 1
        self.next_account_number = 10000

        # Load data if file exists
        if os.path.exists(data_file):
            self.load_from_file()

    def register_user(
        self, full_name: str, phone: str, password: str
    ) -> Optional[User]:
        """Register a new user"""
        # Check if phone number already exists
        if self.find_user_by_phone(phone):
            print("Phone number already registered")
            return None

        # Create new user
        user_id = self.next_user_id
        self.next_user_id += 1

        user = User(user_id, full_name, phone, password)
        self.users[user_id] = user
        self.save_to_file()

        return user

    def login(self, phone: str, password: str) -> Optional[User]:
        """Authenticate user and return User object if successful"""
        user = self.find_user_by_phone(phone)
        if not user:
            print("User not found")
            return None

        if user.authenticate(password):
            return user
        else:
            # Authentication failed but handled in authenticate method
            return None

    def create_account(self, user: User, currency: str = "USD") -> BankAccount:
        """Create a new bank account for a user"""
        account_number = str(self.next_account_number)
        self.next_account_number += 1

        account = BankAccount(account_number, user.user_id, currency)
        self.accounts[account_number] = account
        user.add_account(account_number)

        self.save_to_file()
        return account

    def find_user_by_phone(self, phone: str) -> Optional[User]:
        """Find a user by phone number"""
        for user in self.users.values():
            if user.phone == phone:
                return user
        return None

    def get_account(self, account_number: str) -> Optional[BankAccount]:
        """Get account by account number"""
        return self.accounts.get(account_number)

    def save_to_file(self) -> None:
        """Save all data to JSON file"""
        data = {
            "next_user_id": self.next_user_id,
            "next_account_number": self.next_account_number,
            "users": {str(uid): user.to_dict() for uid, user in self.users.items()},
            "accounts": {
                acc_num: account.to_dict() for acc_num, account in self.accounts.items()
            },
        }

        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=2)

    def load_from_file(self) -> None:
        """Load data from JSON file"""
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)

            self.next_user_id = data["next_user_id"]
            self.next_account_number = data["next_account_number"]

            # Load users
            self.users = {}
            for uid, user_data in data["users"].items():
                self.users[int(uid)] = User.from_dict(user_data)

            # Load accounts
            self.accounts = {}
            for acc_num, acc_data in data["accounts"].items():
                self.accounts[acc_num] = BankAccount.from_dict(acc_data)

        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            print(f"Error loading data: {e}")
            # Initialize with empty data
            self.users = {}
            self.accounts = {}