from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import server.dbs_exec as dbe
from zkp.password_zkp import PasswordZKP
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Initialize ZKP
zkp = PasswordZKP()

# Helper Functions
def update_balance(account_id, amount, is_credit=True):
    """Update account balance in both databases"""
    try:
        # Get current balance
        query = f"SELECT balance FROM CUSTOMERS WHERE account_num={account_id}"
        result = dbe.executeQuery(query)
        if not result[0] or not result[1]:
            return False, "Account not found"
        
        current_balance = result[1][0][0]
        new_balance = current_balance + amount if is_credit else current_balance - amount
        
        if new_balance < 0:
            return False, "Insufficient balance"
            
        # Update balance
        query = f"""
            UPDATE CUSTOMERS 
            SET balance = {new_balance} 
            WHERE account_num = {account_id}
        """
        result = dbe.executeQuery(query)
        return result[0], new_balance
    except Exception as e:
        return False, str(e)

def record_transaction(from_acc, to_acc, amount, trans_type):
    """Record transaction in both databases"""
    try:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"""
            INSERT INTO TRANSACTIONS 
            (from_account, to_account, amount, type, date)
            VALUES ({from_acc}, {to_acc}, {amount}, '{trans_type}', '{date}')
        """
        return dbe.executeQuery(query)[0]
    except Exception as e:
        print(f"Transaction recording error: {e}")
        return False

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session['user_id'] != 0:
            flash('Admin access required')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = request.form.get('account_number')
        password = request.form.get('password')
        
        try:
            account_number = int(account_number)
            if account_number == 0:
                if dbe.isUserAdmin(account_number, password):
                    session['user_id'] = account_number
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid admin credentials')
            else:
                if dbe.authenticate(account_number, password):
                    session['user_id'] = account_number
                    return redirect(url_for('customer_dashboard'))
                else:
                    flash('Invalid credentials')
        except ValueError:
            flash('Invalid account number')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Admin Routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    try:
        total_accounts = len(dbe.executeQuery("SELECT * FROM CUSTOMERS")[1])
        total_transactions = len(dbe.executeQuery("SELECT * FROM TRANSACTIONS")[1])
    except:
        total_accounts = 0
        total_transactions = 0
    
    return render_template('admin/dashboard.html', 
                         total_accounts=total_accounts,
                         total_transactions=total_transactions)

@app.route('/admin/create_account', methods=['GET', 'POST'])
@admin_required
def create_account():
    if request.method == 'POST':
        try:
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            ssn = request.form.get('ssn')
            phone = request.form.get('phone')
            password = request.form.get('password')
            sms = request.form.get('sms', 'N')

            # Create customer
            query = f"""
                INSERT INTO CUSTOMERS 
                (first_name, last_name, ssn_num, phone_num, sms, balance)
                VALUES ('{first_name}', '{last_name}', '{ssn}', '{phone}', '{sms}', 0)
            """
            result = dbe.executeQuery(query)
            if not result[0]:
                raise Exception("Failed to create customer")

            # Get the new account number
            query = f"SELECT account_num FROM CUSTOMERS WHERE ssn_num='{ssn}'"
            result = dbe.executeQuery(query)
            if not result[0] or not result[1]:
                raise Exception("Failed to get account number")

            account_num = result[1][0][0]

            # Set up authentication
            if not dbe.setup_auth_for_new_account(account_num, password):
                raise Exception("Failed to set up authentication")

            flash('Account created successfully')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error creating account: {str(e)}')
    
    return render_template('admin/create_account.html')

@app.route('/admin/close_account', methods=['GET', 'POST'])
@admin_required
def close_account():
    if request.method == 'POST':
        try:
            account_number = int(request.form.get('account_number'))
            admin_password = request.form.get('admin_password')
            
            if dbe.isUserAdmin(0, admin_password):
                query = f"DELETE FROM CUSTOMERS WHERE account_num={account_number}"
                result = dbe.executeQuery(query)
                
                if result[0]:
                    flash('Account closed successfully')
                else:
                    flash('Failed to close account')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin password')
        except ValueError:
            flash('Invalid account number')
        except Exception as e:
            flash(f'Error closing account: {str(e)}')
    
    return render_template('admin/close_account.html')

@app.route('/admin/view_accounts')
@admin_required
def view_accounts():
    try:
        accounts = dbe.executeQuery("SELECT * FROM CUSTOMERS")[1]
    except:
        accounts = []
        flash('Error fetching accounts')
    return render_template('admin/view_accounts.html', accounts=accounts)

@app.route('/admin/view_transactions')
@admin_required
def view_transactions():
    try:
        transactions = dbe.executeQuery("SELECT * FROM TRANSACTIONS ORDER BY date DESC")[1]
    except:
        transactions = []
        flash('Error fetching transactions')
    return render_template('admin/view_transactions.html', transactions=transactions)

# Customer Routes
@app.route('/customer')
@login_required
def customer_dashboard():
    try:
        query = f"SELECT * FROM CUSTOMERS WHERE account_num={session['user_id']}"
        customer = dbe.executeQuery(query)[1][0]
    except:
        return redirect(url_for('logout'))
    return render_template('customer/dashboard.html', customer=customer)

@app.route('/customer/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            if amount <= 0:
                flash('Amount must be positive')
                return render_template('customer/deposit.html')

            success, result = update_balance(session['user_id'], amount, True)
            if not success:
                flash(f'Deposit failed: {result}')
                return render_template('customer/deposit.html')

            if record_transaction(session['user_id'], session['user_id'], amount, 'DEPOSIT'):
                flash('Deposit successful')
                return redirect(url_for('customer_dashboard'))
            else:
                flash('Failed to record transaction')
        except ValueError:
            flash('Invalid amount')
    return render_template('customer/deposit.html')

@app.route('/customer/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            if amount <= 0:
                flash('Amount must be positive')
                return render_template('customer/withdraw.html')

            success, result = update_balance(session['user_id'], amount, False)
            if not success:
                flash(f'Withdrawal failed: {result}')
                return render_template('customer/withdraw.html')

            if record_transaction(session['user_id'], session['user_id'], amount, 'WITHDRAWAL'):
                flash('Withdrawal successful')
                return redirect(url_for('customer_dashboard'))
            else:
                flash('Failed to record transaction')
        except ValueError:
            flash('Invalid amount')
    return render_template('customer/withdraw.html')

@app.route('/customer/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        try:
            recipient = int(request.form.get('recipient'))
            amount = float(request.form.get('amount'))
            
            if amount <= 0:
                flash('Amount must be positive')
                return render_template('customer/transfer.html')

            if not dbe.doesValueExist('account_num', recipient):
                flash('Recipient account not found')
                return render_template('customer/transfer.html')

            # Update sender's balance
            success, sender_result = update_balance(session['user_id'], amount, False)
            if not success:
                flash(f'Transfer failed: {sender_result}')
                return render_template('customer/transfer.html')

            # Update recipient's balance
            success, recipient_result = update_balance(recipient, amount, True)
            if not success:
                # Rollback sender's balance
                update_balance(session['user_id'], amount, True)
                flash('Transfer failed: Error updating recipient balance')
                return render_template('customer/transfer.html')

            if record_transaction(session['user_id'], recipient, amount, 'TRANSFER'):
                flash('Transfer successful')
                return redirect(url_for('customer_dashboard'))
            else:
                # Rollback both balances
                update_balance(session['user_id'], amount, True)
                update_balance(recipient, amount, False)
                flash('Failed to record transaction')
        except ValueError:
            flash('Invalid details')
    return render_template('customer/transfer.html')

@app.route('/customer/transactions')
@login_required
def transactions():
    try:
        query = f"""
            SELECT t.*, c.balance 
            FROM TRANSACTIONS t
            JOIN CUSTOMERS c ON c.account_num = {session['user_id']}
            WHERE t.from_account={session['user_id']} 
            OR t.to_account={session['user_id']}
            ORDER BY t.date DESC
        """
        result = dbe.executeQuery(query)
        transactions = result[1] if result[0] and result[1] else []
    except Exception as e:
        transactions = []
        flash(f'Error fetching transactions: {str(e)}')
    return render_template('customer/transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
