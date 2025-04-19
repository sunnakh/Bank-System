from typing import List
from transaction import Transaction


class BankAccount:
    def __init__(self, account_number: str, user_id: int, currency: str = "USD"):
        self.account_number = account_number
        self.user_id = user_id
        self.balance = 0.0
        self.currency = currency
        self.transactions: List[Transaction] = []

    def deposit(self, amount: float) -> bool:
        """Add funds to account"""
        if amount <= 0:
            print("Amount must be positive")
            return False

        self.balance += amount
        transaction = Transaction("deposit", amount, self.account_number)
        self.transactions.append(transaction)
        return True

    def withdraw(self, amount: float) -> bool:
        """Remove funds from account"""
        if amount <= 0:
            print("Amount must be positive")
            return False

        if amount > self.balance:
            print("Insufficient funds")
            return False

        self.balance -= amount
        transaction = Transaction("withdraw", amount, self.account_number)
        self.transactions.append(transaction)
        return True

    def transfer(self, to_account: "BankAccount", amount: float) -> bool:
        """Transfer funds to another account"""
        if amount <= 0:
            print("Amount must be positive")
            return False

        if amount > self.balance:
            print("Insufficient funds for transfer")
            return False

        # Create withdraw transaction for this account
        self.balance -= amount
        out_transaction = Transaction(
            "transfer", amount, self.account_number, to_account.account_number
        )
        self.transactions.append(out_transaction)

        # Create deposit transaction for recipient account
        to_account.balance += amount
        in_transaction = Transaction(
            "transfer", amount, self.account_number, to_account.account_number
        )
        to_account.transactions.append(in_transaction)

        return True

    def get_statement(self) -> List[str]:
        """Return formatted transaction history"""
        if not self.transactions:
            return ["No transactions found"]

        # Sort transactions by timestamp
        sorted_transactions = sorted(self.transactions, key=lambda t: t.timestamp)
        return [str(transaction) for transaction in sorted_transactions]

    def to_dict(self) -> dict:
        """Convert account to dictionary for persistence"""
        return {
            "account_number": self.account_number,
            "user_id": self.user_id,
            "balance": self.balance,
            "currency": self.currency,
            "transactions": [t.to_dict() for t in self.transactions],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BankAccount":
        """Create BankAccount object from dictionary"""
        account = cls(
            account_number=data["account_number"],
            user_id=data["user_id"],
            currency=data["currency"],
        )
        account.balance = data["balance"]
        account.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
        return account