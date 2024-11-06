# app.py
from flask import Blueprint, Flask
from flask_cors import CORS
from db_models import db  # Import only db, not all models globally if not needed

# Define the Blueprint
auth_bp = Blueprint('auth', __name__)

# Import route handlers
from user_access_endpoints import login_user, sign_up_user

# Attach the route handlers to the blueprint
auth_bp.route('/login', methods=['POST'])(login_user)
auth_bp.route('/sign_up', methods=['POST'])(sign_up_user)

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/software_agile'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize db with the app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  # url_prefix

    return app

# Instantiate the app at the module level
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)