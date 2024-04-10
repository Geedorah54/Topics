# PURPOSE: Run the program

from flask import Flask
from webpage_routes import routes_bp
from post_routes import post_routes_bp

app = Flask(__name__)
app.secret_key = 'your secret key'
app.register_blueprint(routes_bp)
app.register_blueprint(post_routes_bp)

if __name__ == '__main__':
    app.run(debug=False)
