from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

app.secret_key="secret"

# Homepage_Query
@app.route('/homepage-query', methods=['GET'])
def api_homepage_query():
    fetchData_url = 'http://localhost:5003/fetch-data?query=SELECT * FROM accounts'
    try:
        response = requests.get(fetchData_url)
        homepage = response.json()
        
        return homepage, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Visits_Query
@app.route('/visit-query', methods=['GET'])
def api_visit_query():
    fetchData_url = 'http://localhost:5003/fetch-data?query=SELECT * FROM accounts WHERE appointment_datetime IS NOT NULL'
    try:
        response = requests.get(fetchData_url)
        visits = response.json()

        return visits, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Provider_Query
@app.route('/provider-query', methods=['GET'])
def api_provider_query():
    fetchData_url = 'http://localhost:5003/fetch-data?query=SELECT * FROM accounts'
    try:
        response = requests.get(fetchData_url)
        visits = response.json()

        return visits, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#Billing_Query
@app.route('/billing-query', methods=['GET'])
def api_billing_query():
    print("FETCHING BILLING QUERY")
    fetchData_url = 'http://localhost:5003/fetch-data?query=SELECT * FROM accounts'
    try:
        response = requests.get(fetchData_url)
        billing = response.json()
        print('query bill', billing)
        return billing, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(port=5005, debug=True)