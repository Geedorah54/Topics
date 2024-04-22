# PURPOSE: Map POST data routes to addressbar pages

from flask import Blueprint, request, redirect, url_for, Flask
import requests
import re, hashlib
from extract_data import get_database_connection, execute_queryR

# links current page to app.py start file
app = Flask(__name__)
app.secret_key="secret"

@app.route('/book-visit', methods=['POST'])
def book_visit():
    # Extract email and datetime from the form data
    email = request.form['email']
    datetime = request.form['datetime']
    
    # Prepare the data for the POST request
    appointment_data = {"email": email, "datetime": datetime}

    # Make a POST request to the book_appointment service
    response = requests.post("http://127.0.0.1:5004/book_appointment", json=appointment_data)

    # Check the response status code to determine the outcome
    if response.ok:
        # Redirect to the display visits page if the booking was successful
        return redirect('http://127.0.0.1:5008/visits')
    else:
        # Return an error message if booking failed
        return "Error booking appointment: routes", 400

@app.route('/delete-appointment', methods=['POST'])
def delete_appointment():
    # Extract email from the form data
    email = request.form['email']
    
    # Prepare the data for the POST request
    cancel_data = {"email": email}
    
    # Make a POST request to the cancel_appointment service
    response = requests.post("http://127.0.0.1:5004/cancel_appointment", json=cancel_data)
    
    # Check the response status code to determine the outcome
    if response.ok:
        # Redirect to the display visits page if the cancellation was successful
        return redirect('http://127.0.0.1:5008/visits')
    else:
        # Return an error message if cancellation failed
        return "Error canceling appointment", 400

@app.route('/login-user', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    user_data = {
        "username": username,
        "password": password
    }

    role = execute_queryR('SELECT role FROM accounts WHERE username = %s', [username])
    print(role[0][0])
    
    response = requests.post("http://127.0.0.1:5004/check_user", json=user_data)
    if response.status_code == 200 and role[0][0] == 'p':
        return redirect('http://127.0.0.1:5008/homepage')
    elif response.status_code ==200 and role[0][0] == 'd':
        return redirect('http://127.0.0.1:5008/provider')
    else:
        # Redirect to the login page if wrong
        return redirect('http://127.0.0.1:5008/login')
    
@app.route('/register-user', methods=['POST'])
def register_user():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'age' in request.form:

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']


        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))

        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not firstname or not lastname or not age:
            msg = 'Please fill out the form'
        else:
            hash = password + 'secret'
            hash = hashlib.sha1(hash.encode())
            #password = hash.hexdigest()
            password = password

            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s, %s, %s, NULL)', (username, password, email, firstname, lastname, age))
            connection.commit()

    elif request.method == 'POST':
        msg = 'Completely fill out form'

    return redirect('http://127.0.0.1:5008/login')

if __name__ == '__main__':
    app.run(port=5009, debug=True)