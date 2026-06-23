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