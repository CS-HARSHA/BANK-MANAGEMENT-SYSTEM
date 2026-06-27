from bank.bank import Bank
from utils.file_handler import save_data , load_data

def main():
    bank = load_data() or Bank("PyBank")

    while True:
        print(f"\n--- {bank.name} Main Menu ---")
        print("1. Create customer")
        print("2. Create account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. View account statement")
        print("7. View customer details")
        print("8. List all accounts")
        print("9. Delete account")
        print("0. Exit")
        print("---------------------------")

        choice = input("\nSelect an option (0-9): ")

        try:
            if choice == '1':
                name = input("Enter customer name: ")
                email = input("Enter customer email: ")
                phone = input("Enter customer phone: ")
                
                customer = bank.create_customer(name, email, phone)
                save_data(bank)
                print(f"\n[SUCCESS] Customer created with ID: {customer.customer_id}")

            elif choice == '2':
                c_id = input("Enter Customer ID: ")
                acc_type = input("Account Type (savings/current): ")
                balance = float(input("Opening Balance: ₹"))
                
                account = bank.create_account(c_id, acc_type, balance)
                save_data(bank)
                print(f"\n[SUCCESS] Account created. Account Number: {account.account_number}")

            elif choice == '3':
                
                acc_num = input("Enter Account Number: ")
                amount = float(input("Enter amount to deposit: ₹"))
                desc = input("Description (optional): ")
                
                account = bank.find_account(acc_num)
                account.deposit(amount, desc or "Branch Deposit")
                save_data(bank)
                print(f"\n[SUCCESS] Deposited ₹{amount:.2f}. New Balance: ₹{account.balance:.2f}")

            elif choice == '4':
                acc_num = input("Enter Account Number: ")
                amount = float(input("Enter amount to withdraw: ₹"))
                desc = input("Description (optional): ")
                
                account = bank.find_account(acc_num)
                account.withdraw(amount, desc or "Branch Withdrawal")
                save_data(bank)
                print(f"\n[SUCCESS] Withdrew ₹{amount:.2f}. New Balance: ₹{account.balance:.2f}")

            elif choice == '5':
                from_acc = input("Enter From Account Number: ")
                to_acc = input("Enter To Account Number: ")
                amount = float(input("Enter amount to transfer: ₹"))
                desc = input("Description (optional): ")
                
                bank.transfer(from_acc, to_acc, amount, desc)
                save_data(bank)
                print(f"\n[SUCCESS] Transferred ₹{amount:.2f} from {from_acc} to {to_acc}.")

            elif choice == '6':
                acc_num = input("Enter Account Number: ")
                account = bank.find_account(acc_num)
                account.get_statement()

            elif choice == '7':
                c_id = input("Enter Customer ID: ")
                customer = bank.find_customer(c_id)
                print(f"\n--- Details for {customer.name} ---")
                print(f"ID: {customer.customer_id} | Phone: {customer.phone} | Email: {customer.email}")
                print("\nRegistered Accounts:")
                if not customer.accounts:
                    print("  No active accounts.")
                else:
                    for acc in customer.accounts:
                        print(f"  - {acc}")

            elif choice == '8':
                bank.list_all_accounts()

            elif choice == '9':
                acc_num = input("Enter Account Number to delete: ")
                confirm = input(f"Are you sure you want to delete {acc_num}? This action cannot be undone. (y/n): ")
                if confirm.lower() == 'y':
                    bank.delete_account(acc_num)
                    save_data(bank)
                    print(f"\n[SUCCESS] Account {acc_num} permanently deleted.")
                else:
                    print("\n[INFO] Deletion cancelled.")

            elif choice == '0':
                print("\n[SYSTEM] Saving final state to database...")
                save_data(bank)
                print("Session terminated. Goodbye.")
                break

            else:
                print("\n[ERROR] Invalid option. Please enter a number from 0 to 9.")

        except ValueError as e:
            print(f"\n[DENIED] {e}")
        except Exception as e:
            print(f"\n[FATAL ERROR] An unexpected system crash occurred: {e}")

if __name__ == "__main__":
    main()