import os

def setup_menus():
    menu_dir = os.path.join('server', 'menu')
    os.makedirs(menu_dir, exist_ok=True)
    
    menus = {
        'loginMenu.txt': '''@CLEAR
FINTECH FORTRESS    BANK,

FINTECH FORTRESS
-------------------------
Login Menu

a. Login to your account
b. Exit

Enter your choice: ''',

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
    
    for filename, content in menus.items():
        file_path = os.path.join(menu_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Created {filename}")

if __name__ == "__main__":
    setup_menus()
