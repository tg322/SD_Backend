# app.py
from flask import Blueprint, Flask
from flask_cors import CORS
from db_models import db  # Import only db, not all models globally if not needed


# Define the Blueprint
auth_bp = Blueprint('auth', __name__)

# Import route handlers
from user_access_endpoints import login_user

# Attach the route handler to the route
auth_bp.route('/login', methods=['POST'])(login_user)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/software_agile'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Good practice

    db.init_app(app)  # Initialize db with the app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  # Customize url_prefix as needed

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
