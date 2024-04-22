#PURPOSE: Map basic webpage data routes to addressbar pages

from flask import render_template, request, redirect, url_for, session, Flask
import requests

app = Flask(__name__)

app.secret_key="secret"

@app.route('/homepage', methods=['GET'])
def display_homepage():
    # Attempt to fetch data from the homepage-query service
    response = requests.get('http://localhost:5005/homepage-query')
    if response.status_code == 200:

        #Retrieves data from call, and global email for current user
        data = response.json()
        global_email = get_global_variable()
        email = global_email.get('value')

        # Filter rows where the email matches Config.userEmail
        rows = [row for row in data if row[3] == email]
        print("webpage rows", rows)

        # Prepare a default message in case of formatting failure
        default_html = '<p>Currently unable to display detailed table. Please try again later.</p>'

        try:
            # Send the filtered rows to another service to format them as HTML table
            format_response = requests.post('http://localhost:5006/homepage', json={'rows': rows}, timeout=5)
            
            if format_response.status_code == 200:
                # Use the formatted HTML table in your homepage template
                table_html = format_response.text
            else:
                # Log the error and use default HTML
                print("Error formatting tables:", format_response.status_code)
                table_html = default_html
        
        except requests.exceptions.RequestException as e:
            # Log the exception here
            print("Failed to connect to formatting service:", e)
            table_html = default_html

    else:
        # Handle errors from the initial data fetching service
        error_message = "Error fetching homepage data: " + str(response.status_code)
        return render_template('homepage.html', table_html=error_message)

    # Return the template with either formatted or default table HTML
    return render_template('homepage.html', table_html=table_html)

@app.route('/visits', methods=['GET'])
def display_visits():
    response = requests.get('http://localhost:5005/visit-query')

    #Retrieves data from call, and global email for current user
    data = response.json()
    global_email = get_global_variable()
    email = global_email.get('value')

    # Filters Query data for matching email from sign-in (stored in currentUser.py)
    rows = [row for row in data if row[3] == email]
    print("rows", rows)

    if not rows:
        # If rows is empty, return an HTML page or segment with "No bookings"
        return render_template('visits.html', table_html='<p>No bookings</p>')

    # Prepare a default message in case of formatting failure
    default_html = '<p>Currently unable to display booking details. Please try again later.</p>'
    
    try:
        # Attempt to send the filtered rows to another service to format them as HTML table
        format_response = requests.post('http://localhost:5006/visits_table', json={'rows': rows}, timeout=5)
        if format_response.status_code == 200:
            table_html = format_response.text
        else:
            # Log error and use default HTML
            print("Error formatting tables:", format_response.status_code)
            table_html = default_html
    except requests.exceptions.RequestException as e:
        # Log the exception and use default HTML
        print("Failed to connect to formatting service:", e)
        table_html = default_html

    # Return the template with either formatted or default table HTML
    return render_template('visits.html', table_html=table_html)

@app.route('/billing', methods=['GET'])
def display_billing():
    response = requests.get('http://localhost:5005/homepage-query')
    if response.status_code == 200:

        #Retrieves data from call, and global email for current user
        data = response.json()
        global_email = get_global_variable()
        email = global_email.get('value')

        # Filter rows where the email matches Config.userEmail
        rows = [row for row in data if row[3] == email]
        print(rows)
        balance = rows[0][6]


    if balance == 0:
        default_html = '<p>Currently unable to display billing details. Please try again later.</p>'
        return render_template('billing.html', table_html=default_html)
    else:
        default_html = f"<p>Amount Outstanding: ${balance}<p>"
        
    return render_template('billing.html', table_html=default_html)

#Basic routes
@app.route('/login')
def login():
    msg = ''
    return render_template('login.html', msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/provider')
def provider():
    # Attempt to fetch data from the homepage-query service
    response = requests.get('http://localhost:5005/homepage-query')
    if response.status_code == 200:

        #Retrieves data from call, and global email for current user
        data = response.json()
        global_email = get_global_variable()
        email = global_email.get('value')

        # Filter rows where the email matches Config.userEmail
        rows = [row for row in data if row[3]]
        print("webpage rows", rows)

        # Prepare a default message in case of formatting failure
        default_html = '<p>Currently unable to display detailed table. Please try again later.</p>'

        try:
            # Send the filtered rows to another service to format them as HTML table
            format_response = requests.post('http://localhost:5006/homepage', json={'rows': rows}, timeout=5)
            
            if format_response.status_code == 200:
                # Use the formatted HTML table in your homepage template
                table_html = format_response.text
            else:
                # Log the error and use default HTML
                print("Error formatting tables:", format_response.status_code)
                table_html = default_html
        
        except requests.exceptions.RequestException as e:
            # Log the exception here
            print("Failed to connect to formatting service:", e)
            table_html = default_html

    else:
        # Handle errors from the initial data fetching service
        error_message = "Error fetching homepage data: " + str(response.status_code)
        return render_template('provider.html', table_html=error_message)

    # Return the template with either formatted or default table HTML
    return render_template('provider.html', table_html=table_html)

# Local function to retrieve email from currentUser
def get_global_variable():
    url = 'http://localhost:5011/get'
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    app.run(port=5008, debug=True)