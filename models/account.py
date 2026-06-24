import uuid
from models.transaction import Transaction
from typing import List , Dict

class BankAccount:

    def __init__(self, owner: str, account_number: str = None, balance: float = 0.0):
        self.owner = owner
        self.account_number = account_number or f"ACC-{str(uuid.uuid4().int)[:5]}"
        self._balance = balance  # Protected variable
        self.transactions: List[Transaction] = []
    
    @property
    def balance(self) -> float:
        """Getter for balance. Prevents direct modification from outside."""
        return self._balance
    
    def deposit(self, amount: float, description: str = "") -> Transaction:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        
        self._balance += amount
        transaction = Transaction(amount=amount,balance_after=self._balance, transaction_type="Deposit", description=description)
        self.transactions.append(transaction)
        return transaction

        # # Creating the transaction (assuming your Transaction class accepts these kwargs)
        # transaction = Transaction(
        #     amount=amount, 
        #     transaction_type="Deposit", 
        #     description=description
        # )
        # self.transactions.append(transaction)
        # return transaction
    
    def withdraw(self , amount: float, description: str = "") -> Transaction:
        if amount <= 0:
            raise ValueError("Withdrawl amount must be greater than zero")
        if amount > self._balance:
            raise ValueError(f"Insufficient balance, Current balance is ₹{self._balance:.2f}. ")
        
        self._balance -= amount
        transaction = Transaction(amount=amount, balance_after=self._balance, transaction_type="Withdrawal", description=description)
        self.transactions.append(transaction)
        return transaction
    
    def get_statement(self):
        print("-" * 30)
        print(f"Statement for {self.account_number} owned by {self.owner}")
        print(f"The current balance is ₹{self._balance:.2f}")
        print("-" * 30)

        for t in self.transactions:
            print(t)

        print("-" * 30)

    def to_dict(self) -> Dict:
        return {
            "account_type": self.__class__.__name__,
            "account_number": self.account_number,
            "owner": self.owner,
            "balance": self._balance,
            "transactions": [t.to_dict() for t in self.transactions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        account = cls(owner=data["owner"], account_number=data["account_number"], balance=data["balance"])
        if "transactions" in data:
            account.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
        return account

    def __str__(self) -> str:
        acc_type = self.__class__.__name__.replace("Account", "") or "General"
        return f"[{self.account_number}] {self.owner} | {acc_type} | Balance: ₹{self._balance:.2f}"
    
    
class SavingsAccount(BankAccount):
    def __init__(self, owner:str , account_number: str = None , balance: float = 0.0, minimum_balance: float = 1000.0, interest_rate: float = 4.0):
        super().__init__(owner, account_number ,balance)
        self.minimum_balance = minimum_balance
        self.interest_rate = interest_rate

    def withdraw(self, amount: float, description: str = "") -> Transaction:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if (self._balance - amount) < self.minimum_balance:
            raise ValueError(f"Withdrawal denied. Minimum balance of ₹{self.minimum_balance:.2f} must be maintained.")
        
        self._balance -= amount
        transaction = Transaction(amount=amount,balance_after=self._balance, transaction_type="Withdrawal", description=description)
        self.transactions.append(transaction)
        return transaction
    
    def apply_interest(self) -> float:
        interest_amount = (self._balance * self.interest_rate) / 100
        self.deposit(interest_amount, "Interest applied")
        return interest_amount
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data["minimum_balance"] = self.minimum_balance
        data["interest_rate"] = self.interest_rate
        return data
    
    @classmethod
    def from_dict(cls, data: Dict):
        account = cls(
         owner=data["owner"],
         account_number=data["account_number"],
         balance=data["balance"],
         minimum_balance=data.get("minimum_balance", 1000.0),
         interest_rate=data.get("interest_rate", 4.0)
        )
        if "transactions" in data:
          account.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
        return account


class CurrentAccount(BankAccount):
    def __init__(self, owner: str, account_number: str = None, balance: float = 0.0, overdraft_limit: float = 10000.0):
        super().__init__(owner, account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float, description: str = "") -> Transaction:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if (self._balance - amount) < -self.overdraft_limit:
            raise ValueError(f"Withdrawal denied. Exceeds overdraft limit of ₹{self.overdraft_limit:.2f}.")
        
        self._balance -= amount
        transaction = Transaction(amount=amount,balance_after=self._balance, transaction_type="Withdrawal", description=description)
        self.transactions.append(transaction)
        return transaction

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data["overdraft_limit"] = self.overdraft_limit
        return data

    @classmethod
    def from_dict(cls, data: Dict):
       account = cls(
         owner=data["owner"],
         account_number=data["account_number"],
         balance=data["balance"],
         overdraft_limit=data.get("overdraft_limit", 10000.0)
        )
       if "transactions" in data:
         account.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
       return account

