from models.transaction import Transaction

t1 = Transaction(5000, 12000, "deposit", description="Opening deposit")
t2 = Transaction(2000, 10000, "withdrawal", description="ATM withdrawal")

print(t1)
print(t2)

data = t1.to_dict()
t3 = Transaction.from_dict(data)
print(t3)

from models.account import SavingsAccount, CurrentAccount

print("=== SAVINGS ACCOUNT ===")
s = SavingsAccount("Arjun", balance=5000)
s.deposit(3000, "Salary credit")
print(s.balance)                    # should print 8000.0

s.withdraw(2000, "Grocery")
print(s.balance)                    # should print 6000.0

try:
    s.withdraw(5500)                # should raise — drops below ₹1000 minimum
except ValueError as e:
    print(f"Caught: {e}")

interest = s.apply_interest()
print(f"Interest applied: ₹{interest:.2f}")  # 4% of 6000 = 240.0
print(s.balance)                    # should print 6240.0

s.get_statement()                   # should show all 4 transactions
print(s)                            # should show one clean summary line

print("\n=== CURRENT ACCOUNT ===")
c = CurrentAccount("Priya", balance=2000)
c.deposit(1000, "Opening top-up")
print(c.balance)                    # should print 3000.0

c.withdraw(8000, "Big purchase")    # should work — 3000 - 8000 = -5000, within overdraft
print(c.balance)                    # should print -5000.0

try:
    c.withdraw(6000)                # should raise — -5000 - 6000 = -11000, exceeds ₹10000 overdraft
except ValueError as e:
    print(f"Caught: {e}")

c.get_statement()                   # should show all 3 transactions
print(c)                            # clean summary line

print("\n=== FROM_DICT ROUND TRIP ===")
data = s.to_dict()
from models.account import BankAccount
s2 = SavingsAccount.from_dict(data)
print(s2)                           # should match s exactly
print(s2.balance)                   # should match s.balance


from models.customer import Customer
from models.account import SavingsAccount, CurrentAccount

c = Customer("Arjun", "arjun@gmail.com", "9999999999")

s = SavingsAccount("Arjun", balance=5000)
s.deposit(2000, "Salary")
c.add_account(s)

curr = CurrentAccount("Arjun", balance=3000)
c.add_account(curr)

print(c)
print(c.get_accounts())
print(c.get_account(s.account_number))

data = c.to_dict()
c2 = Customer.from_dict(data)
print(c2)
print(c2.get_account(s.account_number).balance)

from bank.bank import Bank

b = Bank("PyBank")

# create customers
c1 = b.create_customer("Arjun", "arjun@gmail.com", "9999999999")
c2 = b.create_customer("Priya", "priya@gmail.com", "8888888888")

# create accounts
acc1 = b.create_account(c1.customer_id, "savings", 5000)
acc2 = b.create_account(c2.customer_id, "current", 3000)

# deposit and withdraw
acc1.deposit(2000, "Salary")
acc2.deposit(1000, "Opening")

# transfer
b.transfer(acc1.account_number, acc2.account_number, 1000, "Rent payment")

# list all
b.list_all_accounts()

# find
print(b.find_customer(c1.customer_id))
print(b.find_account(acc1.account_number))

# delete account
b.delete_account(acc2.account_number)
b.list_all_accounts()

# to_dict round trip
data = b.to_dict()
b2 = Bank.from_dict(data)
print(b2)
print(b2.find_account(acc1.account_number).balance)

# error handling
try:
    b.find_account("ACC-00000")
except ValueError as e:
    print(f"Caught: {e}")

try:
    b.transfer(acc1.account_number, acc2.account_number, 500)
except ValueError as e:
    print(f"Caught: {e}")

from bank.bank import Bank
from utils.file_handler import save_data, load_data

b = Bank("PyBank")
c1 = b.create_customer("Arjun", "arjun@gmail.com", "9999999999")
acc1 = b.create_account(c1.customer_id, "savings", 5000)
acc1.deposit(2000, "Salary")

save_data(b)

b2 = load_data()
print(b2)
print(b2.find_account(acc1.account_number).balance)
b2.list_all_accounts()