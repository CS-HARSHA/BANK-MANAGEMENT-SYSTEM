import uuid
from typing import List , Dict , Optional
from models.account import BankAccount , SavingsAccount , CurrentAccount

class Customer:

    def __inti__(self, name:str ,email:str ,phone:str ,customer_id:str):
        self.name= name
        self.email = email
        self.phone = phone
        self.customer_id = customer_id or f"CUST-{str(uuid.uuid4().int)[:5]}"
        self.accounts: List[BankAccount] = []

    def add_account(self, account: BankAccount):
        self.accounts.append(BankAccount)

    def get_accounts(self) -> List[BankAccount]:
        return self.accounts
    
    def get_account(self, account_number: str)-> Optional[BankAccount]:
        for acc in self.accounts:
            if acc.account_number == account_number:
                return acc
        return None
    
    def to_dict(self) -> Dict:
        """Serializes the customer and all their nested accounts."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "accounts": [acc.to_dict() for acc in self.accounts]
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Rebuilds the Customer object and properly instantiates their specific accounts."""
        # Rebuild the customer
        customer = cls(
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            customer_id=data.get("customer_id")
        )

        # Polymorphic reconstruction of accounts
        for acc_data in data.get("accounts", []):
            acc_type = acc_data.get("account_type", "Account")
            
            # Route the data to the correct factory method based on the account type
            if acc_type == "SavingsAccount":
                customer.add_account(SavingsAccount.from_dict(acc_data))
            elif acc_type == "CurrentAccount":
                customer.add_account(CurrentAccount.from_dict(acc_data))
            else:
                customer.add_account(BankAccount.from_dict(acc_data))
                
        return customer
    
    def __str__(self) -> str:
        """Clean, one-line summary of the customer."""
        return f"[{self.customer_id}] {self.name} | Phone: {self.phone} | Total Accounts: {len(self.accounts)}"
    