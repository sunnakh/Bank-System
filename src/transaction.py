import uuid
import datetime
from typing import Optional


class Transaction:
    def __init__(
        self,
        transaction_type: str,
        amount: float,
        from_account: str,
        to_account: Optional[str] = None,
    ):
        self.transaction_id = str(uuid.uuid4())
        self.type = transaction_type  # 'deposit', 'withdraw', 'transfer'
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.timestamp = datetime.datetime.now()

    def to_dict(self) -> dict:
        """Convert transaction to dictionary for persistence"""
        return {
            "transaction_id": self.transaction_id,
            "type": self.type,
            "amount": self.amount,
            "from_account": self.from_account,
            "to_account": self.to_account,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Create Transaction object from dictionary"""
        transaction = cls(
            transaction_type=data["type"],
            amount=data["amount"],
            from_account=data["from_account"],
            to_account=data.get("to_account"),
        )
        transaction.transaction_id = data["transaction_id"]
        transaction.timestamp = datetime.datetime.fromisoformat(data["timestamp"])
        return transaction

    def __str__(self) -> str:
        if self.type == "deposit":
            return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] DEPOSIT: +${self.amount:.2f}"
        elif self.type == "withdraw":
            return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] WITHDRAW: -${self.amount:.2f}"
        else:  # transfer
            if self.to_account:
                return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] TRANSFER TO {self.to_account}: -${self.amount:.2f}"
            else:
                return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] TRANSFER FROM {self.from_account}: +${self.amount:.2f}"