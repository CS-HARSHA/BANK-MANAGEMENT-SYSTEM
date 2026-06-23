import uuid
from datetime import datetime 

class Transaction:
    def __init__(self, amount:float, balance_after: float, transaction_type:str, transaction_id: str="", description: str="" , timestamp: str = None):
        self.amount = amount
        self.transaction_type = transaction_type
        self.transaction_id = transaction_id or str(uuid.uuid4())
        self.description = description
        self.timestamp = timestamp or datetime.now().isoformat()
        self.balance_after = balance_after

    def to_dict(self):
        return {
            "transaction_id" : self.transaction_id,
            "transaction_type": self.transaction_type,
            "amount" : self.amount,
            "description" : self.description,
            "timestamp": self.timestamp,
            "balance_after" : self.balance_after
        }
            
    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Transaction object from a dictionary (used when loading JSON)."""
        return cls(
            amount=data["amount"],
            transaction_type=data["transaction_type"],
            description=data.get("description", ""),
            transaction_id=data["transaction_id"],
            timestamp=data["timestamp"],
            balance_after=data["balance_after"]
        )
    
    def __str__(self):
        clean_time = datetime.fromisoformat(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        sign = "+" if self.transaction_type == "deposit" else "-"
        return f"[{clean_time}]  {self.transaction_type.upper():<12}  {sign}₹{self.amount:,.2f}  |  {self.description or 'No description'}"


