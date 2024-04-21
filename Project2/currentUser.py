from flask import Flask, jsonify, request
import redis

app = Flask(__name__)

global_variable = None

@app.route('/set', methods=['POST'])
def set_variable():
    global global_variable
    data = request.get_json()
    print(data)
    global_variable = data.get('value')
    print('set', global_variable)
    return jsonify({"message": "Variable updated successfully", "value": global_variable}), 200

@app.route('/get', methods=['GET'])
def get_variable():
    global global_variable
    print('get', global_variable)
    if global_variable is not None:
        return jsonify({"value": global_variable}), 200
    else:
        return jsonify({"error": "Variable not set"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5011)