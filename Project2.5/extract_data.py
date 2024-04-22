# PURPOSE: Communicate with MySQL database
from flask import session, Flask, request, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key="secret"

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

# Exposed function for fetching data
@app.route('/fetch-data', methods=['GET'])
def api_fetch_data():
    query = request.args.get('query')  # Example: /fetch-data?query=SELECT * FROM accounts
    try:
        result = fetch_data(query) # Calls local function to handle process
        return result, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Closed Function for /fetch-data API
def fetch_data(query):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


# Exposed function for fetching data
@app.route('/execute_query', methods=['POST'])
def api_execute_query():
    print('EXECUTING')
    query = request.args.get('query')  # Example: /fetch-data?query=SELECT * FROM my_table
    if not query:
        return jsonify({"error": "No query provided"}), 400
    try:
        result = execute_query(query) # Calls local function to handle process
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

def execute_queryR(query, params=None):
    connection = get_database_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

@app.route('/execute_queryd', methods=['POST'])
def execute_queryd():
    # Extract data from request
    request_data = request.json
    query = request_data['query']
    print(query)
    params = request_data.get('params', None)

    # Database connection and query execution
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    account = {}
    if params:
        cursor.execute(query, params)
        account = cursor.fetchone()
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    # Returning the result as JSON
    if account:
        return jsonify(account), 200
    else:
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    app.run(port=5003, debug=True)