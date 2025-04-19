import hashlib
import datetime
from typing import List, Optional


class User:
    def __init__(self, user_id: int, full_name: str, phone: str, password: str):
        self.user_id = user_id
        self.full_name = full_name
        self.phone = phone
        # Store hashed password
        self.password = self._hash_password(password)
        self.accounts: List[str] = []  # Store account numbers
        self.login_attempts = 0
        self.locked_until = None

    def _hash_password(self, password: str) -> str:
        """Create a SHA-256 hash of the password"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, password: str) -> bool:
        """Verify user password"""
        # Check if account is locked
        if self.is_locked():
            remaining_time = int(
                (self.locked_until - datetime.datetime.now()).total_seconds() / 60
            )
            print(f"Account is locked. Try again in {remaining_time} minutes.")
            return False

        # Compare hashed password
        if self._hash_password(password) == self.password:
            self.login_attempts = 0
            return True
        else:
            self.login_attempts += 1
            if self.login_attempts >= 3:
                self.locked_until = datetime.datetime.now() + datetime.timedelta(
                    minutes=30
                )
                print(f"Too many failed attempts. Account locked for 30 minutes.")
            return False

    def is_locked(self) -> bool:
        """Check if user account is locked"""
        if self.locked_until and datetime.datetime.now() < self.locked_until:
            return True
        elif self.locked_until:
            # Reset lock if time has passed
            self.locked_until = None
            self.login_attempts = 0
        return False

    def add_account(self, account_number: str) -> None:
        """Associate a bank account with this user"""
        if account_number not in self.accounts:
            self.accounts.append(account_number)

    def get_accounts(self) -> List[str]:
        """Return list of user's account numbers"""
        return self.accounts

    def to_dict(self) -> dict:
        """Convert user to dictionary for persistence"""
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "phone": self.phone,
            "password": self.password,
            "accounts": self.accounts,
            "login_attempts": self.login_attempts,
            "locked_until": (
                self.locked_until.isoformat() if self.locked_until else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create User object from dictionary"""
        user = cls(
            user_id=data["user_id"],
            full_name=data["full_name"],
            phone=data["phone"],
            password="",  # Temporary placeholder
        )
        # Directly set the hashed password
        user.password = data["password"]
        user.accounts = data["accounts"]
        user.login_attempts = data["login_attempts"]
        user.locked_until = (
            datetime.datetime.fromisoformat(data["locked_until"])
            if data["locked_until"]
            else None
        )
        return user