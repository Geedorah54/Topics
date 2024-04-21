# PURPOSE: Handle POST Query requests
from flask import session, Flask, request, jsonify
import requests
import redis

app = Flask(__name__)

app.secret_key="secret"

# Checks when submitting an appointment
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    print('BOOKING_QUERY TRY')
     # Extract data from the incoming request
    email = request.json.get('email')
    datetime = request.json.get('datetime')

    # Define the payload for the POST request
    sql_command = f"UPDATE accounts SET appointment_datetime = '{datetime}' WHERE email = '{email}'"
    sql_command_encoded = requests.utils.quote(sql_command)

    # Make a POST request to the service that handles the database update
    url = f"http://localhost:5003/execute_query?query={sql_command_encoded}"
    response = requests.post(url)
    print('Response Code')
    print(response.status_code)
    
    # Check if the request was successful
    if response.status_code == 200:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": False}), response.status_code

@app.route('/cancel_appointment', methods=['POST'])
def cancel_appointment():
    email = request.json.get('email')
    print(email)

    # Define the payload for the POST request
    sql_command = f"UPDATE accounts SET appointment_datetime = NULL WHERE email = '{email}'"
    sql_command_encoded = requests.utils.quote(sql_command)

    # Checks when deleting an appointment
    try:
        url = f"http://localhost:5003/execute_query?query={sql_command_encoded}"
        response = requests.post(url)
        if response.status_code == 200:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": False}), response.status_code
    except Exception as e:
        print("Error canceling appointment:", e)
        return jsonify({"error": False}), 50
        
@app.route('/check_user', methods=['POST'])
def check_user():
    try:
        # Extract username and password from the request body
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        # Prepare the query
        query = {
            "query": "SELECT * FROM accounts WHERE username = %s AND password = %s",
            "params": [username, password]
        }
        print(query)
        
        # Make a POST request to the execute_query service
        response = requests.post("http://localhost:5003/execute_queryd", json=query)
        if response.status_code == 200:
            result = response.json()

            print('Assigning session', result['email'])
            set_global_variable(result['email'])

            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Incorrect username or password"}), 404
    except Exception as e:
        print(f"Incorrect username or passwordddd: {e}")
        return jsonify({"error": "An error occurred"}), 500
        
def set_global_variable(new_value):
    url = 'http://localhost:5011/set'
    response = requests.post(url, json={"value": new_value})
    print('setting', response.status_code)
    return response.json()

if __name__ == '__main__':
    app.run(port=5004, debug=True)