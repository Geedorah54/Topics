# PURPOSE: Communicate with MySQL database
from flask import session
import mysql.connector
import re, hashlib

# MySQL database credentials
host = 'localhost'
user = 'root'
password = 'group1@3980'
database = 'login'

# Function grab database credentials
def get_database_connection():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

# Function to write SQL for MySQL database
def fetch_data(query):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def execute_query(query, params=None):
    # Function to execute SQL queries
    # Implement using your database connection
    connection = get_database_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

# Return a dictionary from SQL query
def execute_queryD(query, params=None):
    connection = get_database_connection()
    cursor = connection.cursor(dictionary = True)
    if params:
        cursor.execute(query, params)
        account = cursor.fetchone()
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        return account
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()



