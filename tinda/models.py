# write all your SQL queries in this file.
from datetime import datetime
from tinda import conn, login_manager, app
from flask_login import UserMixin
from psycopg2 import sql
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_bcrypt import Bcrypt
from datetime import datetime
import os



@login_manager.user_loader
def load_user(email):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
    if cur.rowcount > 0:
        return Users(cur.fetchone())
    else:
        return None

def email_exists(email):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Users WHERE email = %s", (email,))
    exists = cur.fetchone()
    cur.close()
    return exists is not None

def insert_user(email, name, description, password, dateBirth, location):
    cur = conn.cursor()
    sql = """
    INSERT INTO Users(email, name, description, password, dateBirth, location)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql, (email, name, description, password, dateBirth, location))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def delete_user_by_email(email):
    cur = conn.cursor()
    # Execute DELETE statement to remove the row where the email matches
    cur.execute("DELETE FROM Users WHERE email = %s", (email,))
    # Commit the changes to the database to ensure the deletion is saved
    conn.commit()
    # Check how many rows were affected (optional)
    affected_rows = cur.rowcount
    cur.close()
    # Return True if any rows were deleted, else False
    return affected_rows > 0

def check_user(email,password):
    cur = conn.cursor()
    cur.execute("SELECT password FROM Users WHERE email = %s", (email,))
    result = cur.fetchone()
    cur.close()
    bcrypt = Bcrypt()

    if result is not None:
        stored_password_hash = result[0]  # Fetch the stored hash from the database
        return bcrypt.check_password_hash(stored_password_hash, password)
    else:
        return False  # Return False if no user is found

class Users(tuple, UserMixin):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.email = user_data[1]
        self.name = user_data[2]
        self.description = user_data[3]
        self.password = user_data[4]
        self.birth = user_data[5]
        self.location = user_data[6]

    def get_id(self):
       return (self.email)


def insert_picture(url, userid):
    cur = conn.cursor()
    sql = """
    INSERT INTO pictures(filename, userid)
    VALUES (%s, %s)
    """
    cur.execute(sql, (url, userid))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def select_pictures(userid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pictures WHERE userid = %s", (userid,))
    result = cur.fetchall()
    cur.close()
    print(result)
    return result

def delete_picture(filepath):
    # delete file
    
    UPLOAD_FOLDER = 'static/uploads'

    print(os.path.join(os.path.join(app.root_path, UPLOAD_FOLDER), filepath))
    if os.path.exists(os.path.join(os.path.join(app.root_path, UPLOAD_FOLDER), filepath)):
        os.remove(os.path.join(os.path.join(app.root_path, UPLOAD_FOLDER), filepath))

    # now delete in DB
    cur = conn.cursor()
    # Execute DELETE statement to remove the row where the email matches
    cur.execute("DELETE FROM pictures WHERE filename = %s", (filepath,))
    # Commit the changes to the database to ensure the deletion is saved
    conn.commit()
    # Check how many rows were affected (optional)
    affected_rows = cur.rowcount
    cur.close()
    # Return True if any rows were deleted, else False
    return affected_rows > 0


def select_swipe(userid):
    cur = conn.cursor()
    sql = """
    SELECT *
    FROM users u
    WHERE NOT EXISTS (
        SELECT 1
        FROM matches m
        WHERE m.matchee = u.userid AND m.matcher = %s ) AND
        NOT EXISTS (
        SELECT 1
        FROM matches m
        WHERE m.matcher = u.userid AND m.matchee = %s AND active = TRUE) AND
        NOT EXISTS (
        SELECT 1
        FROM matches m
        WHERE m.matcher = u.userid AND m.matchee = %s AND dislike = TRUE)
    AND u.userid != %s
    """
    cur.execute(sql, (userid,userid,userid,userid))
    user = Users(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user


def select_match(userid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pictures WHERE userid = %s", (userid,))
    result = cur.fetchall()
    cur.close()
    print(result)
    return result

def update_or_insert_match(userid, id):
    # Create a cursor object using the database connection
    cur = conn.cursor()
    

    # First, try to update if the specific match exists
    update_sql = """
    UPDATE matches
    SET active = TRUE
    WHERE matcher = %s AND matchee = %s;
    """
    cur.execute(update_sql, (id, userid))
    
    
    # Check if the update has affected any rows
    if cur.rowcount == 0:
        # No rows updated, meaning no such match exists
        # Perform the insert with reversed values
        insert_sql = """
        INSERT INTO matches (matchdate, active, dislike, matcher, matchee)
        VALUES (NOW(), FALSE, FALSE, %s, %s)
        """
        cur.execute(insert_sql, (userid, id))
    
    # Commit changes
    conn.commit()
    cur.close()

def dislike_match(userid, id):
    # Create a cursor object using the database connection
    cur = conn.cursor()
    

    # First, try to update if the specific match exists
    update_sql = """
    UPDATE matches
    SET dislike = TRUE
    WHERE matcher = %s AND matchee = %s;
    """
    cur.execute(update_sql, (userid, id))
    # Check if the update has affected any rows
    if cur.rowcount == 0:
        update_sql = """
        UPDATE matches
        SET dislike = TRUE
        WHERE matcher = %s AND matchee = %s;
        """
        cur.execute(update_sql, (id, userid))
        if cur.rowcount == 0:
            # No rows updated, meaning no such match exists
            # Perform the insert with reversed values
            insert_sql = """
            INSERT INTO matches (matchdate, active, dislike, matcher, matchee)
            VALUES (NOW(), FALSE, TRUE, %s, %s)
            """
            cur.execute(insert_sql, (userid, id))

    # Commit changes
    conn.commit()
    cur.close()

# OLD SHIT HERFRA

# class Customers(tuple, UserMixin):
#     def __init__(self, user_data):
#         self.CPR_number = user_data[0]
#         self.risktype = False
#         self.password = user_data[2]
#         self.name = user_data[3]
#         self.address = user_data[4]
#         self.role = "customer"

#     def get_id(self):
#        return (self.CPR_number)


# class Employees(tuple, UserMixin):
#     def __init__(self, employee_data):
#         self.id = employee_data[0]
#         self.name = employee_data[1]
#         self.password = employee_data[2]
#         self.role = "employee"
    
#     def get_id(self):
#        return (self.id)
    
# class CheckingAccount(tuple):
#     def __init__(self, user_data):
#         self.id = user_data[0]
#         self.create_date = user_data[1]
#         self.CPR_number = user_data[2]
#         self.amount = 0

# class InvestmentAccount(tuple):
#     def __init__(self, user_data):
#         self.id = user_data[0]
#         self.start_date = user_data[1]
#         self.maturity_date = user_data[2]
#         self.amount = 0

# class Transfers(tuple):
#     def __init__(self, user_data):
#         self.id = user_data[0]
#         self.amount = user_data[1]
#         self.transfer_date = user_data[2]

# def insert_Customers(name, CPR_number, password):
#     cur = conn.cursor()
#     sql = """
#     INSERT INTO Customers(name, CPR_number, password)
#     VALUES (%s, %s, %s)
#     """
#     cur.execute(sql, (name, CPR_number, password))
#     # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
#     conn.commit()
#     cur.close()

# def select_Customer(CPR_number):
#     cur = conn.cursor()
#     sql = """
#     SELECT * FROM Customers
#     WHERE CPR_number = %s
#     """
#     cur.execute(sql, (CPR_number,))
#     user = Customers(cur.fetchone()) if cur.rowcount > 0 else None;
#     cur.close()
#     return user

# #cus-1-3-2024
# def select_customer_direct(CPR_number):
#     #SELECT cpr_number, name, address FROM Customers
#     cur = conn.cursor()
#     sql = """
#     SELECT *
#      FROM Customers
#     WHERE CPR_number = %s
#     AND DIRECT IS TRUE
#     """
#     cur.execute(sql, (CPR_number,))
#     user = Customers(cur.fetchone()) if cur.rowcount > 0 else None;
#     cur.close()
#     return user

# def select_Employee(id):
#     cur = conn.cursor()
#     sql = """
#     SELECT * FROM Employees
#     WHERE id = %s
#     """
#     cur.execute(sql, (id,))
#     user = Employees(cur.fetchone()) if cur.rowcount > 0 else None;
#     cur.close()
#     return user


# def update_CheckingAccount(amount, CPR_number):
#     cur = conn.cursor()
#     sql = """
#     UPDATE CheckingAccount
#     SET amount = %s
#     WHERE CPR_number = %s
#     """
#     cur.execute(sql, (amount, CPR_number))
#     # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
#     conn.commit()
#     cur.close()

# def transfer_account(date, amount, from_account, to_account):
#     cur = conn.cursor()
#     sql = """
#     INSERT INTO Transfers(transfer_date, amount, from_account, to_account)
#     VALUES (%s, %s, %s, %s)
#     """
#     cur.execute(sql, (date, amount, from_account, to_account))
#     # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
#     conn.commit()
#     cur.close()

# #cus-1-3-2024
# def select_customers_direct():
#     cur = conn.cursor()
#     sql = """
#     SELECT
#       c.name customer
#     , cpr_number
#     , address
#     FROM customers c
# 	WHERE direct IS TRUE
#     ;
#     """
#     cur.execute(sql)
#     tuple_resultset = cur.fetchall()
#     cur.close()
#     return tuple_resultset

# def select_cus_accounts(cpr_number):
#     cur = conn.cursor()
#     sql = """
#     SELECT
#       e.name employee
#     , c.name customer
#     , cpr_number
#     , account_number
#     FROM manages m
#       NATURAL JOIN accounts
#       NATURAL JOIN customers c
#       LEFT OUTER JOIN employees e ON m.emp_cpr_number = e.id
# 	WHERE cpr_number = %s
#     ;
#     """
#     cur.execute(sql, (cpr_number,))
#     tuple_resultset = cur.fetchall()
#     cur.close()
#     return tuple_resultset


# def select_cus_investments(cpr_number):
#     cur = conn.cursor()
#     sql = """
#     SELECT i.account_number, a.cpr_number, a.created_date
#     FROM investmentaccounts i
#     JOIN accounts a ON i.account_number = a.account_number
#     WHERE a.cpr_number = %s
#     """
#     cur.execute(sql, (cpr_number,))
#     tuple_resultset = cur.fetchall()
#     cur.close()
#     return tuple_resultset

# def select_cus_investments_with_certificates(cpr_number):
#     # TODO-CUS employee id is parameter
#     cur = conn.cursor()
#     sql = """
#     SELECT i.account_number, a.cpr_number, a.created_date
#     , cd.cd_number, start_date, maturity_date, rate, amount
#     FROM investmentaccounts i
#     JOIN accounts a ON i.account_number = a.account_number
#     JOIN certificates_of_deposit cd ON i.account_number = cd.account_number
#     WHERE a.cpr_number = %s
#     ORDER BY 1
#     """
#     cur.execute(sql, (cpr_number,))
#     tuple_resultset = cur.fetchall()
#     cur.close()
#     return tuple_resultset

# def select_cus_investments_certificates_sum(cpr_number):
#     # TODO-CUS employee id is parameter - DONE
#     cur = conn.cursor()
#     sql = """
#     SELECT account_number, cpr_number, created_date, sum
#     FROM vw_cd_sum
#     WHERE cpr_number = %s
#     GROUP BY account_number, cpr_number, created_date, sum
#     ORDER BY account_number
#     """
#     cur.execute(sql, (cpr_number,))
#     tuple_resultset = cur.fetchall()
#     cur.close()
#     return tuple_resultset
