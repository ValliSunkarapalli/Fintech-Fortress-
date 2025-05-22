import sqlite3
import time
import os

def print_database_contents(db_path, title):
    """Print the contents of a database"""
    print(f"\n{'-'*20} {title} {'-'*20}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Print Customers table
    print("\nCUSTOMERS TABLE:")
    cursor.execute("SELECT * FROM CUSTOMERS")
    customers = cursor.fetchall()
    if customers:
        print("Account_Num | First_Name | Last_Name | SSN | Phone | SMS | Balance")
        print("-" * 70)
        for customer in customers:
            print(f"{customer[0]:<11} | {customer[1]:<10} | {customer[2]:<9} | {customer[3]} | {customer[4]} | {customer[5]} | {customer[6]}")
    else:
        print("No customers found")
    
    # Print Transactions table
    print("\nTRANSACTIONS TABLE:")
    cursor.execute("SELECT * FROM TRANSACTIONS")
    transactions = cursor.fetchall()
    if transactions:
        print("Trans_ID | From_Acc | To_Acc | Amount | Type | Date")
        print("-" * 60)
        for trans in transactions:
            print(f"{trans[0]:<8} | {trans[1]:<8} | {trans[2]:<7} | {trans[3]:<6} | {trans[4]:<4} | {trans[5]}")
    else:
        print("No transactions found")
    
    conn.close()

def demonstrate_replication():
    """Demonstrate database replication"""
    db1_path = "server/database1.db"
    db2_path = "server/database2.db"
    
    while True:
        os.system('clear' if os.name != 'windows' else 'cls')
        print("\n=== Database Replication Demonstration ===")
        print("\n1. Show contents of both databases")
        print("2. Create new account (through Server 1)")
        print("3. Make a transaction (through Server 1)")
        print("4. Stop Server 1 (simulate failure)")
        print("5. Verify Backup Server (Server 2)")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            print_database_contents(db1_path, "Primary Database (Server 1)")
            print_database_contents(db2_path, "Backup Database (Server 2)")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            print("\nCreating new account through Server 1...")
            # Start Server 1 if not running
            print("Please run these commands in separate terminals:")
            print("1. python3 server/server_manager.py 0")
            print("2. python3 client/main.py")
            print("\nThen:")
            print("1. Login as admin (account: 0, password: admin)")
            print("2. Create a new account")
            input("\nPress Enter after completing these steps...")
            
        elif choice == '3':
            print("\nMaking a transaction through Server 1...")
            print("Please use the client to:")
            print("1. Login to an account")
            print("2. Make a deposit or transfer")
            input("\nPress Enter after completing these steps...")
            
        elif choice == '4':
            print("\nTo simulate Server 1 failure:")
            print("1. Stop Server 1 (Ctrl+C in Server 1's terminal)")
            print("2. Start Server 2: python3 server/server_manager.py 1")
            input("\nPress Enter after completing these steps...")
            
        elif choice == '5':
            print("\nVerifying backup server data...")
            print_database_contents(db2_path, "Backup Database (Server 2)")
            print("\nTry using the client now - it should automatically connect to Server 2")
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            print("\nExiting demonstration...")
            break
            
        else:
            print("\nInvalid choice! Press Enter to continue...")
            input()

if __name__ == "__main__":
    demonstrate_replication()
