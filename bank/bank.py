from typing import Dict , Tuple
from models.customer import Customer
from models.account import BankAccount , SavingsAccount , CurrentAccount

class Bank:

    def __init__(self, name:str):
        self.name = name
        self.customers : Dict[str, Customer] = {}
        self.accounts : Dict[str, BankAccount] = {}
        
    def create_customer(self, name:str , email:str , phone:str) -> Customer :
        customer = Customer(name=name, email=email, phone=phone)
        self.customers[customer.customer_id] = customer
        return customer
    
    def create_account(self, customer_id:str ,account_type: str, opening_balance: float) -> BankAccount:
        customer = self.find_customer(customer_id) 

        if account_type.lower() == "savings":
            account = SavingsAccount(owner=customer.name, balance=opening_balance)
        elif account_type.lower() == "current":
            account = CurrentAccount(owner=customer.name, balance=opening_balance)
        else:
            raise ValueError("Invalid account type. Must be 'savings' or 'current'.")
        
        # Add to the bank's central registry
        self.accounts[account.account_number] = account
        # Link it to the specific customer
        customer.add_account(account)
        return account
    
    def find_account(self, account_number: str) -> BankAccount:
        if account_number not in self.accounts:
            raise ValueError(f"Account {account_number} not found.")
        return self.accounts[account_number]

    # find_customer
    def find_customer(self, customer_id: str) -> Customer:
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found.")
        return self.customers[customer_id]
    
    #  transfer
    def transfer(self, from_number: str, to_number: str, amount: float, description: str = "") -> Tuple:
        from_account = self.find_account(from_number)
        to_account   = self.find_account(to_number)

        # Format clean descriptions for both sides of the transfer
        w_desc = description or f"Transfer to {to_number}"
        d_desc = description or f"Transfer from {from_number}"
        
        # The withdraw method natively handles limits and insufficient funds checks
        w_transaction = from_account.withdraw(amount, description=w_desc)
        d_transaction = to_account.deposit(amount, description=d_desc)
        
        return (w_transaction, d_transaction)
    
    def delete_account(self, account_number: str) -> bool:
        account = self.find_account(account_number)
        
        # 1. Remove from the central bank registry
        del self.accounts[account_number]
        
        # 2. Clean up the dangling reference in the Customer object to prevent memory leaks
        for customer in self.customers.values():
            if account in customer.accounts:
                customer.accounts.remove(account)
                break
                
        return True
    
    #  list_all_accounts
    def list_all_accounts(self):
        print("-" * 30)
        print(f"All Active Accounts for {self.name}")
        print("-" * 30)
        if not self.accounts:
            print("No accounts found.")
        else:
            for acc in self.accounts.values():
                print(acc)
        print("-" * 30)

    def to_dict(self) -> Dict:
        """
        Notice we only serialize the customers. 
        Because the Customer object natively holds the Account objects, 
        saving self.accounts separately would create duplicated, out-of-sync JSON data.
        """
        return {
            "name": self.name,
            "customers": {cid: customer.to_dict() for cid, customer in self.customers.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict):
        bank = cls(name=data["name"])
        
        if "customers" in data:
            for cid, c_data in data["customers"].items():
                # Rebuild the customer (which auto-rebuilds their nested accounts)
                customer = Customer.from_dict(c_data)
                bank.customers[cid] = customer
                
                # Repopulate the bank's central self.accounts dictionary for O(1) lookups
                for account in customer.accounts:
                    bank.accounts[account.account_number] = account
                    
        return bank
    
    #  __str__
    def __str__(self) -> str:
        return f"{self.name} | Total Customers: {len(self.customers)} | Total Accounts: {len(self.accounts)}"