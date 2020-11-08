# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask, render_template  # From module flask import class Flask
from flask.globals import request
import pandas as pd
from functools import wraps
import json
from datetime import datetime
from Crypto.Cipher import AES
import base64

app = Flask(__name__)  # Construct an instance of Flask class for our webapp

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'thisIsMySecretKey'

HASH_SALT = "Fr33L@nC!NG";

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


@app.route('/')  # URL '/' to be handled by main() route handler
def main():
    """Say hello"""
#     return 'Hello, world!'
#     return render_template('j2_query.html')
#     return render_template('j2_derived.html')

# Output message if something goes wrong...
    msg = ''
    return render_template('Login.html', msg='')


@app.route('/login' , methods=['GET', 'POST'])  # URL '/' to be handled by main() route handler
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
            elif account['user_type'] == 'SuperAdmin':
                return redirect(url_for('superAdmin'))
            
            # Redirect to home page
#             return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('Login.html', msg=msg)


def login_required(function_to_protect):

    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        isLogin = session.get('loggedin')
        if isLogin:
            # Success!
            return function_to_protect(*args, **kwargs)
        else:
            flash("Please log in")
            return redirect(url_for('login'))

    return wrapper


@app.route('/admin')
def admin():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    
    statesQuery = '''
        Select count(*) as num , "total transactions" as element from inv_inventory
        union
        Select count(*) as num, "total companies" as element from inv_company
        union
        select count(*) as num, "total bank" as element from inv_bank;
        '''    
    cursor.execute(statesQuery)
    states = cursor.fetchall()
    return render_template('Admin.html', states = states)    

@app.route('/bankRegister', methods=['GET', 'POST'])
def bankRegister():
    msg = ""
    if request.method == 'POST':
        bankName = request.form['bankName']
        shortCode = request.form['shortCode']
        registrationDate = request.form['registrationDate']
        registrationEnd = request.form['registrationEnd']
        membershipCategory = request.form['membershipCategory']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = '''
            insert into inv_bank values (Null, '%s' , '%s', '%s', '%s', '%s')
            ''' % (bankName, shortCode, registrationDate, registrationEnd, membershipCategory)
            
        print(query)
        cursor.execute(query)
        mysql.connection.commit()
        msg = "Bank Added Successfully"
        return render_template('Admin_Bank_Register.html', msg = msg)
    
    return render_template('Admin_Bank_Register.html', msg = msg)


@app.route('/bankDelete' , methods=['GET'])
@login_required
def bankDelete():
    banks = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        return render_template('Admin_Bank_Delete.html', banks = banks)
    
    cursor.execute('SELECT * FROM customer_inventory.inv_bank')
    banks = cursor.fetchall()
    return render_template('Admin_Bank_Delete.html', banks = banks)


@app.route('/bankDelete/<int:id>' , methods=['GET'])
@login_required
def bankDeleteWithId(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = '''
        delete from inv_bank where id = %s
        ''' % (id)
            
    print(query)
    cursor.execute(query)
    mysql.connection.commit()
    
    return redirect(url_for('bankDelete'))


@app.route('/companyRegister' , methods=['GET', 'POST'])
def companyRegister():
    msg = ""
    if request.method == 'POST':
        
        company_name = request.form['company_name']
        company_establishdate = request.form['company_establishdate']
        company_type = request.form['company_type']
        company_websiteurl = request.form['company_websiteurl']
        company_employeecount = request.form['company_employeecount']
        company_annualsale = request.form['company_annualsale']
        company_picturepath = request.form['company_picturepath']
        company_registerationdate = request.form['company_registerationdate']
        company_registerationenddate = request.form['company_registerationenddate']
        company_membershipcategory = request.form['company_membershipcategory']
        company_address = request.form['company_address']
        company_phone = request.form['company_phone']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = '''
            INSERT INTO `customer_inventory`.`inv_company` 
            (`company_name`, `company_establishdate`, `company_type`, `company_websiteurl`, `company_employeecount`, `company_annualsale`, `company_picturepath`, `company_registerationdate`, `company_registerationenddate`, `company_membershipcategory`, `login_id`, `company_address`, `company_phone`) 
            VALUES 
            ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
            ''' %(str(company_name), str(company_establishdate), str(company_type), str(company_websiteurl), str(company_employeecount), str(company_annualsale), str(company_picturepath), str(company_registerationdate), str(company_registerationenddate), str(company_membershipcategory), str(0), str(company_address), str(company_phone))
            
        print(query)
        cursor.execute(query)
        mysql.connection.commit()
        msg = "Company Added Successfully"
        return render_template('Admin_Company_Register.html', msg = msg)
    
    return render_template('Admin_Company_Register.html', msg = msg)
    
    

@app.route('/companyDelete')
def companyDelete():
    companies = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        return render_template('Admin_Company_Delete.html', companies = companies)
    
    cursor.execute('SELECT * FROM customer_inventory.inv_company')
    companies = cursor.fetchall()
    return render_template('Admin_Company_Delete.html', companies = companies)
   
@app.route('/companyDelete/<int:id>' , methods=['GET'])
@login_required
def companyDeleteWithId(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = '''
        delete from inv_company where company_id = %s
        ''' % (id)
            
    print(query)
    cursor.execute(query)
    mysql.connection.commit()
    
    return redirect(url_for('companyDelete'))


@app.route('/userRegister')
def userRegister():
    companies = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        return render_template('Admin_Company_Delete.html', companies = companies)
    
    cursor.execute('SELECT * FROM customer_inventory.inv_company')
    companies = cursor.fetchall()
    return render_template('Admin_Company_Delete.html', companies = companies)

@app.route('/superAdmin', methods=['GET', 'POST'])
def superAdmin():
    msg = "";
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM customer_inventory.inv_company')
    companies = cursor.fetchall()
    
    cursor.execute('SELECT * FROM customer_inventory.inv_bank')
    banks = cursor.fetchall()
    
    if request.method == 'POST':
        
        userName = request.form['userName']
        userId = request.form['userId']
        Password = request.form['Password']
        userType = request.form['userType']
        
        if userType == 'company':
            type_id = request.form['company_type_id']
        elif userType == 'bank':
            type_id = request.form['bank_type_id']
        
        if userType != 'admin' and type_id == str(0):
            msg = "Please Select Company/Bank"
            return render_template('SuperAdmin_User_Register.html', companies=companies, banks=banks, msg=msg)
        
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = '''
            insert into inv_user values (Null, '%s' , '%s', '%s', '%s', '%s', '%s')
            ''' % (userName, userId, Password, userType, type_id, 3)
            
        print(query)
        cursor.execute(query)
        mysql.connection.commit()
        msg = "User Added Successfully"
       
        
        return render_template('SuperAdmin_User_Register.html', companies=companies, banks=banks, msg = msg)
    
    
    
    return render_template('SuperAdmin_User_Register.html', companies=companies, banks=banks, msg=msg)


@app.route('/deleteUser')
def deleteUser(): 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM customer_inventory.inv_user')
    users = cursor.fetchall()  
    
    for user in users:
        if user['user_type'] == 'bank':
            cursor.execute('select * from inv_bank where id =  %s;', (str(user['type_id'])))
            bank = cursor.fetchone()
            if bank:
                user['type_name'] = bank['name']
            else:
                user['type_name'] = 'Unknown Bank'
        if user['user_type'] == 'company':
            cursor.execute('select * from inv_company where company_id =  %s;', (str(user['type_id'])))
            compay = cursor.fetchone()
            if compay:
                user['type_name'] = compay['company_name']
            else:
                user['type_name'] = 'unknown Company'
        if user['user_type'] == 'admin':
            user['type_name'] = 'admin'
        if user['user_type'] == 'SuperAdmin':
            user['id'] = 'admin'
    
    return render_template('SuperAdmin_User_Delete.html', users = users)

@app.route('/deleteUser/<int:id>' , methods=['GET'])
@login_required
def userDeleteWithId(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = '''
        delete from inv_user where id = %s
        ''' % (id)
            
    print(query)
    cursor.execute(query)
    mysql.connection.commit()
    
    return redirect(url_for('deleteUser'))

@app.route('/userManagementDelete')
def userManagement():
    companies = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        return render_template('Admin_Company_Delete.html', companies = companies)
    
    cursor.execute('SELECT * FROM customer_inventory.inv_company')
    companies = cursor.fetchall()
    return render_template('Admin_Company_Delete.html', companies = companies)
   
@app.route('/userManagementDelete/<int:id>' , methods=['GET'])
@login_required
def userManagementDeleteWithId(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = '''
        delete from inv_company where company_id = %s
        ''' % (id)
            
    print(query)
    cursor.execute(query)
    mysql.connection.commit()
    
    return redirect(url_for('companyDelete'))



@app.route('/adminTransactions', methods=['GET', 'POST'])
def adminTransactions():
    companyDetails = []
    companyTransactions = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    if request.method == 'POST':
        
#         bankId = 0;
#         userId = session.get('id')
#         cursor.execute('SELECT * FROM customer_inventory.inv_user where id = %s;', (userId,))
#         account = cursor.fetchone()
#         if account:
#             bankId = account['type_id']
#         else:
#             flash("Please log in")
#             return redirect(url_for('login'))
         
        companyName = request.form['companyName']
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        
        companyDetails = "SELECT * FROM customer_inventory.inv_company where company_name = '"+companyName+"';"
        cursor.execute(companyDetails)
        companyDetails = cursor.fetchone()
        
        companyTransactions = "SELECT * FROM customer_inventory.inv_inventory where company_id = " + str(companyDetails['company_id']) + " and inventory_datetime between  '"+ str(from_date)+"' AND '"+str(to_date)+"'"
        cursor.execute(companyTransactions)
        companyTransactions = cursor.fetchall()
        
#         query = '''
#              insert into customer_inventory.inv_banksearch values (NULL, %s, '%s', '%s', '%s', "%s")
#             ''' % (bankId, from_date, to_date, datetime.now(), companyDetails['company_id'])    
#         print(query)
#         cursor.execute(query)
#         mysql.connection.commit()
      
      
    allCompanies = "SELECT * FROM customer_inventory.inv_company;"
    cursor.execute(allCompanies)
    allCompanies = cursor.fetchall()
            
    return render_template('Admin_Transactions.html', allCompanies = allCompanies,  companyDetails = companyDetails,  companyTransactions = companyTransactions)


#------------------ BANK


@app.route('/bank')
@login_required
def bank():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    
    bankId = 0;
    userId = session.get('id')
    cursor.execute('SELECT * FROM customer_inventory.inv_user where id = %s;', (userId,))
    account = cursor.fetchone()
    if account:
        bankId = account['type_id']
    else:
        flash("Please log in")
        return redirect(url_for('login'))
    
    statesQuery = '''
        Select 'totalCompany' as element, count(*) as val from inv_company
        union 
        Select 'today_transactions' as element, count(*) as val from inv_inventory where inventory_datetime between  CURRENT_DATE() AND CURRENT_DATE() + INTERVAL 1 DAY 
        union 
        Select 'last_7_days_transactions' as element, count(*) as val from inv_inventory where inventory_datetime between  DATE(NOW()) - INTERVAL 7 DAY AND DATE(NOW()) 
        union
        Select 'this_month' as element, count(*) as val from inv_inventory where (inventory_datetime between  DATE_FORMAT(NOW() ,'%Y-%m-01') AND LAST_DAY(NOW()) )

        '''    
    cursor.execute(statesQuery)
    states = cursor.fetchall()
    
    graphQuery = '''
        select 
            count(*) as count,
            DATE_FORMAT(inventory_datetime,'%H:00') as time
        from 
            inv_inventory 
        where
            inventory_datetime between  CURRENT_DATE() AND CURRENT_DATE() + INTERVAL 1 DAY
        group by 
            DATE_FORMAT(inventory_datetime,'%H:00')
        order by     
            DATE_FORMAT(inventory_datetime,'%H:00')
        '''

    cursor.execute(graphQuery)
    todayTransactionsGraphCursor = cursor.fetchall()
    chartData = []
    barChatLables = []
    transaction = None
    for i in range(24):
        if len(todayTransactionsGraphCursor) > i:
            transaction = todayTransactionsGraphCursor[i]
        keyTime = "0" + str(i) + ":00" if i <= 9 else str(i) +":00"
        barChatLables.append(keyTime)
        if transaction and transaction['time'] == keyTime:
            chartData.append(transaction['count'])
        else:
            chartData.append(0)
        
    
    top5TransactinsCompanyQuery = '''
        select 
            count(*) as num, 
            comp.company_name
        from 
            inv_inventory  inv, inv_company comp
        where 
            inv.company_id = comp.company_id
        group by 
            inv.company_id
        order by 
            count(*)
        LIMIT 5
        '''
    
    cursor.execute(top5TransactinsCompanyQuery)
    top5TransactinsCompany = cursor.fetchall()
    
    top5SearchQuery = '''
         SELECT search.date , company.company_name 
         FROM inv_banksearch search, inv_company company 
         where 
         search.company = company.company_id
         and 
         bankid = %s
         order by date desc LIMIT 5;
        '''% (bankId)
    
    cursor.execute(top5SearchQuery)
    top5Search = cursor.fetchall()
    
#     barChatLables = ["0", "1", "2", "3", "4", "5","6", "7", "8", "9", "10", "11","12", "13", "14", "15", "16", "17","18", "19", "20", "21", "22", "23"]
#     chartData =  [4215, 5312, 6251, 7841, 9821, 14984,4215, 5312, 6251, 7841, 9821, 14984,4215, 5312, 6251, 7841, 9821, 14984,4215, 5312, 6251, 7841, 9821, 14984]
    
    return render_template('Bank.html',states = states, barChatLables = json.dumps(barChatLables), chartData = json.dumps(chartData), top5TransactinsCompany = top5TransactinsCompany, top5Search = top5Search )


@app.route('/bankCompanySearch', methods=['GET', 'POST'])
@login_required
def bankCompanySearch():
    companyDetails = []
    allCompanies = []
    companyTransactions = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    if request.method == 'POST':
        
        bankId = 0;
        userId = session.get('id')
        cursor.execute('SELECT * FROM customer_inventory.inv_user where id = %s;', (userId,))
        account = cursor.fetchone()
        if account:
            bankId = account['type_id']
        else:
            flash("Please log in")
            return redirect(url_for('login'))
         
        companyName = request.form['companyName']
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        
        companyDetails = "SELECT * FROM customer_inventory.inv_company where company_name = '"+companyName+"';"
        cursor.execute(companyDetails)
        companyDetails = cursor.fetchone()
        
        companyTransactions = "SELECT * FROM customer_inventory.inv_inventory where company_id = " + str(companyDetails['company_id']) + " and inventory_datetime between  '"+ str(from_date)+"' AND '"+str(to_date)+"'"
        cursor.execute(companyTransactions)
        companyTransactions = cursor.fetchall()
        
        query = '''
             insert into customer_inventory.inv_banksearch values (NULL, %s, '%s', '%s', '%s', "%s")
            ''' % (bankId, from_date, to_date, datetime.now(), companyDetails['company_id'])    
        print(query)
        cursor.execute(query)
        mysql.connection.commit()
      
      
    allCompanies = "SELECT * FROM customer_inventory.inv_company;"
    cursor.execute(allCompanies)
    allCompanies = cursor.fetchall()
            
    return render_template('Bank_Company_Search.html', allCompanies = allCompanies,  companyDetails = companyDetails,  companyTransactions = companyTransactions)


@app.route('/bankContactUs')
def bankContactUs():
    return render_template('bank_contact_us.html')


#------------------ Company
@app.route('/company')
@login_required
def company():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    companyId = 0;
    userId = session.get('id')
    cursor.execute('SELECT * FROM customer_inventory.inv_user where id = %s;', (userId,))
    account = cursor.fetchone()
    if account:
        companyId = account['type_id']
    else:
        flash("Please log in")
        return redirect(url_for('login'))  
    
#     
#     transactionQuery = '''
#                         Select 'total' as element, count(*) as val from inv_inventory
#                         union 
#                         Select 'week' as element, count(*) as val from inv_inventory where inventory_datetime > DATE(NOW()) - INTERVAL 7 DAY
#                         union 
#                         Select 'this_month' as element, count(*) as val from inv_inventory where (inventory_datetime between  DATE_FORMAT(NOW() ,'%Y-%m-01') AND LAST_DAY(NOW()) )
#                         ''' 
    
    
    transactionQuery = '''
                        Select 'total' as element, count(*) as val from inv_inventory where company_id = %s
                        union 
                        Select 'week' as element, count(*) as val from inv_inventory where company_id = %s and inventory_datetime > DATE(NOW()) - INTERVAL 7 DAY
                        union 
                        Select 'this_month' as element, count(*) as val from inv_inventory where company_id = %s and (inventory_datetime between  DATE_FORMAT(NOW() ,'%Y-%m-01') AND LAST_DAY(NOW()) )

                        '''.replace("%s", str(companyId))
    
    cursor.execute(transactionQuery)
    transactionsSummary = cursor.fetchall()
    
    cursor.execute('SELECT * FROM customer_inventory.inv_company where company_id = %s;', (companyId,))
    company = cursor.fetchone()
   
    
    return render_template('Company.html', transactionsSummary = transactionsSummary, company = company)


@app.route('/uploadFile', methods=['GET', 'POST'])
@login_required
def uploadFile():
    msg = ""
    if request.method == 'POST':
#         return jsonify({"result": request.get_array(field_name='file')})
        print(request.files['file'])
        f = request.files['file']
#         data_xls = pd.read_excel(f)
        data_xls = pd.read_excel(f, sheet_name='Sheet1', usecols=['productname', 'mode', 'quantity', 'datetime', 'amount'])
#         print(data_xls.columns.ravel())
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        companyId = 0;
        userId = session.get('id')
        cursor.execute('SELECT * FROM customer_inventory.inv_user where id = %s;', (userId,))
        account = cursor.fetchone()
        if account:
            companyId = account['type_id']
        else:
            flash("Please log in")
            return redirect(url_for('login'))   
        
        for row in  range(data_xls.shape[0]):    
#             INSERT INTO customer_inventory.inv_inventory VALUES           (null, 4, 'abc', 'x', 5, Timestamp('2020-10-09 00:00:00'), 10)        
#             query = 'INSERT INTO customer_inventory.inv_inventory VALUES (NULL, %s,\'%s\',\'%s\', %s, Timestamp(\'%s\'), %s,NULL )' % (companyId, data_xls.iat[row, 0], data_xls.iat[row, 1], data_xls.iat[row, 2], data_xls.iat[row, 3], data_xls.iat[row, 4])
            query = '''
            INSERT INTO customer_inventory.inv_inventory 
            (inventory_id, company_id, inventory_productname, inventory_mode, inventory_quantity,inventory_datetime, inventory_amount) VALUES 
            (NULL, %s,\'%s\',\'%s\', %s, Timestamp(\'%s\'), %s)
            ''' % (companyId, data_xls.iat[row, 0], data_xls.iat[row, 1], data_xls.iat[row, 2], data_xls.iat[row, 3], data_xls.iat[row, 4])
            
            print(query)
            cursor.execute(query)
        mysql.connection.commit()
        msg = "File Uploaded Successfully. You can confirm this upload in transaction view."
#             for col in range(data_xls.shape[1]):
#                 print(data_xls.iat[row, col])
        
        render_template('Company_uploadFile.html', msg = msg)
    return render_template('Company_uploadFile.html', msg = msg)


@app.route('/uploadFileApi', methods=['POST'])
def uploadFileApi():
    msg = ""
    if request.method == 'POST' and 'payload' in request.form and request.headers.get("companyUser") and request.headers.get("companyPass"):
#         return jsonify({"result": request.get_array(field_name='file')})

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        companyUser = request.headers.get("companyUser");
        companyPass = request.headers.get("companyPass");
        cursor.execute('SELECT * FROM customer_inventory.inv_user where user_id = %s and pass = %s;', (companyUser, companyPass))
        # Fetch one record and return result
        CompamyAccount = cursor.fetchone()
        
        if CompamyAccount == None or CompamyAccount['user_type'] != 'company':
            return "<h1>Error in adding Transactions</h1><p>Please Contact Administrator</p>"
        
        payloads = json.loads(request.form['payload'])
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        for payload in  payloads["payload"]:    
#             INSERT INTO customer_inventory.inv_inventory VALUES           (null, 4, 'abc', 'x', 5, Timestamp('2020-10-09 00:00:00'), 10)        
#             query = 'INSERT INTO customer_inventory.inv_inventory VALUES (NULL, %s,\'%s\',\'%s\', %s, Timestamp(\'%s\'), %s,NULL )' % (companyId, data_xls.iat[row, 0], data_xls.iat[row, 1], data_xls.iat[row, 2], data_xls.iat[row, 3], data_xls.iat[row, 4])
            query = '''
            INSERT INTO customer_inventory.inv_inventory 
            (inventory_id, company_id, inventory_productname, inventory_mode, inventory_quantity,inventory_datetime, inventory_amount) VALUES 
            (NULL, %s,\'%s\',\'%s\', %s, Timestamp(\'%s\'), %s)
            ''' % (CompamyAccount['type_id'], payload["productname"], payload["mode"], payload["quantity"], payload["datetime"], payload["amount"])
            
            print(query)
            cursor.execute(query)
        mysql.connection.commit()
        msg = "File Uploaded Successfully. You can confirm this upload in transaction view."
#             for col in range(data_xls.shape[1]):
#                 print(data_xls.iat[row, col])
        
        return "<h1>Transactions added Successfully</h1><p>Please login to Portal and verify</p>"
    return "<h1>Error in adding Transactions</h1><p>Please Contact Administrator</p>"
    

@app.route('/transactions')
def transactions():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    companyId = 0;
    userId = session.get('id')
    cursor.execute('SELECT * FROM customer_inventory.inv_user where id = %s;', (userId,))
    account = cursor.fetchone()
    if account:
        companyId = account['type_id']
    else:
        flash("Please log in")
        return redirect(url_for('login'))   
    
    cursor.execute('SELECT * FROM customer_inventory.inv_inventory where company_id = %s;', (companyId,))
    allTransactions = cursor.fetchall()
    
    return render_template('Company_transactions.html', transactions = allTransactions)


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
def hello_username(username):  # The function shall take the URL variable as parameter
    return 'Hello, {}'.format(username)


@app.route('/hello/<int:userid>')  # Variable with type filter. Accept only int
def hello_userid(userid):  # The function shall take the URL variable as parameter
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
