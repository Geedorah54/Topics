# PURPOSE: Map POST data routes to addressbar pages

from flask import Blueprint, request, redirect, url_for
from post_query import AppointmentService, LoginVerify, RegisterUser
import MySQLdb
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
from extract_data import get_database_connection, execute_queryR

key = 'secret'

# links current page to app.py start file
post_routes_bp = Blueprint('post_routes', __name__)


@post_routes_bp.route('/book-visit', methods=['POST'])
def book_visit():
    email = request.form['email']
    datetime = request.form['datetime']
    if AppointmentService.book_appointment(email, datetime):
        return redirect(url_for('routes.display_visits'))
    else:
        return "Error booking appointment"

@post_routes_bp.route('/delete-appointment', methods=['POST'])
def delete_appointment():
    email = request.form['email']
    if AppointmentService.cancel_appointment(email):
        return redirect(url_for('routes.display_visits'))
    else:
        return "Error canceling appointment"

@post_routes_bp.route('/login-user', methods=['POST'])
def login_user():

    username = request.form['username']
    password = request.form['password']

    role = execute_queryR('SELECT role FROM accounts WHERE username = %s', [username])

    if LoginVerify.check_user(username, password):
        if (role[0][0] == 'p'):
            return redirect(url_for('routes.display_homepage'))
        elif (role[0][0] == 'd'):
            return redirect(url_for('routes.display_provider'))
    else:
        return redirect(url_for('routes.login'))
    
@post_routes_bp.route('/register-user', methods=['POST'])
def register_user():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))

        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form'
        else:
            hash = password + key
            hash = hashlib.sha1(hash.encode())
            #password = hash.hexdigest()
            password = password

            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            connection.commit()

    elif request.method == 'POST':
        msg = 'Completely fill out form'

    return redirect(url_for('routes.register'))