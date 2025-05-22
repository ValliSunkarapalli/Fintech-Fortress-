# setup.py
import os
import sys

def verify_structure():
    # Required files and directories
    required_structure = {
        'files': [
            'common.py',
            'server/server_manager.py',
            'server/database_sync.py',
            'server/dbs_exec.py',
            'server/dbs_view.py',
            'server/menu/adminMenu.txt',
            'server/menu/loginMenu.txt',
            'server/menu/customerMenu.txt',
            'config/server_config.py'
        ],
        'dirs': [
            'server',
            'server/menu',
            'config'
        ]
    }

    # Check and create directories
    for dir_path in required_structure['dirs']:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")

    # Verify files
    missing_files = []
    for file_path in required_structure['files']:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("\nMissing files:")
        for file in missing_files:
            print(f"- {file}")
        return False

    # Create menu files if they don't exist
    menu_content = {
        'adminMenu.txt': '''@CLEAR
FINTECH FORTRESS BANK ADMIN MENU
-----------------------------
Options

a. Create a new account
b. Close an account
c. View all accounts
d. View all transactions
e. Log out

Enter your choice: ''',
        'loginMenu.txt': '''@CLEAR
FINTECH FORTRESS BANK,

FINTECH FORTRESS
-----------------
Login Menu

a. Login to your account
b. Exit

Enter your choice: ''',
        'customerMenu.txt': '''@CLEAR
FINTECH FORTRESS BANK CUSTOMER MENU
-------------------------------
Account number: {account_num}
Balance: {balance} Rs

Options

a. Refresh
b. Make a deposit
c. Make a withdrawal
d. Transfer money
e. See transaction history
f. Log out

Enter your choice: '''
    }

    for filename, content in menu_content.items():
        file_path = os.path.join('server', 'menu', filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Created menu file: {filename}")

    return True

if __name__ == "__main__":
    print("Verifying project structure...")
    if verify_structure():
        print("\nProject structure is correct.")
        print("\nYou can now run the servers:")
        print("1. Primary server:   python server/server_manager.py 0")
        print("2. Backup server:    python server/server_manager.py 1")
    else:
        print("\nPlease create the missing files before running the servers.")
