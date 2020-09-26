# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask, render_template  # From module flask import class Flask
from flask.globals import request

app = Flask(__name__)    # Construct an instance of Flask class for our webapp


# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'thisIsMySecretKey'

# Enter your database connection details below
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'customer_inventory'

app.config['MYSQL_HOST'] = '104.131.3.66'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Netcool@123'
app.config['MYSQL_DB'] = 'customer_inventory'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    """Say hello"""
#     return 'Hello, world!'
#     return render_template('j2_query.html')
#     return render_template('j2_derived.html')

# Output message if something goes wrong...
    msg = ''
    return render_template('Login.html', msg='')



@app.route('/login' , methods=['GET', 'POST'])   # URL '/' to be handled by main() route handler
def login():
    """Say hello"""
#     return 'Hello, world!'
#     return render_template('j2_query.html')
#     return render_template('j2_derived.html')

# Output message if something goes wrong...
    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer_inventory.inv_user where user_id = %s and pass = %s;', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['user_name']
            
            if account['user_type'] == 'admin':
                return redirect(url_for('admin'))
            elif account['user_type'] == 'bank':
                return redirect(url_for('bank'))
            elif account['user_type'] == 'company':
                return redirect(url_for('company'))
                
            
            
            
            # Redirect to home page
#             return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            
    
    return render_template('Login.html', msg=msg)

@app.route('/admin')
def admin():
    return render_template('Admin.html')
    

@app.route('/bankRegister')
def bankRegister():
    return render_template('Admin_Bank_Register.html')

@app.route('/bankDelete')
def bankDelete():
    return render_template('Admin_Bank_Delete.html')


@app.route('/companyRegister')
def companyRegister():
    return render_template('Admin_Company_Register.html')

@app.route('/companyDelete')
def companyDelete():
    return render_template('Admin_Company_Delete.html')

@app.route('/adminTransactions')
def adminTransactions():
    return render_template('Admin_Transactions.html')




#------------------ BANK

@app.route('/bank')
def bank():
    return render_template('Bank.html')

@app.route('/bankCompanySearch')
def bankCompanySearch():
    return render_template('Bank_Company_Search.html')

@app.route('/bankContactUs')
def bankContactUs():
    return render_template('bank_contact_us.html')

#------------------ BANK

@app.route('/company')
def company():
    return render_template('Company.html')





def showBankMainPage():
    return render_template('BankMain.html')
    
def showCompanyMainPage():
    return render_template('company.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
   # Redirect to login page
    return redirect(url_for('login'))






@app.route('/hello')
def hello():
    return 'Hello, world!'

@app.route('/hello/<username>')  # URL with a variable
def hello_username(username):    # The function shall take the URL variable as parameter
    return 'Hello, {}'.format(username)

@app.route('/hello/<int:userid>')  # Variable with type filter. Accept only int
def hello_userid(userid):          # The function shall take the URL variable as parameter
    return 'Hello, your ID is: {:d}'.format(userid)


@app.route('/process', methods=['POST'])
def process():
    # Retrieve the HTTP POST request parameter value from 'request.form' dictionary
    _username = request.form.get('username')  # get(attr) returns None if attr is not present
 
    # Validate and send response
    if _username:
        return render_template('j2_response.html', username=_username)
    else:
        return 'Please go back and enter your name...', 400  # 400 Bad Request



if __name__ == '__main__':  # Script executed directly?
    app.run(debug=True)  # Launch built-in web server and run this Flask webapp