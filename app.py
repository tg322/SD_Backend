# app.py
from flask import Blueprint, Flask
from flask_cors import CORS
from db_models import db  # Import only db, not all models globally if not needed

# Define the Blueprint
auth_bp = Blueprint('auth', __name__)

# Import route handlers
from user_access_endpoints import login_user, sign_up_user, test_get_auth_token

# Attach the route handlers to the blueprint testing
auth_bp.route('/login', methods=['POST'])(login_user)
auth_bp.route('/test', methods=['GET'])(test_get_auth_token)
auth_bp.route('/signup', methods=['POST'])(sign_up_user)

def create_app():
    app = Flask(__name__)
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/*": {
                "origins": [
                    "https://www.tg322.co.uk"  # Local Development Frontend
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/software_agile'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize db with the app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  # url_prefix

    return app

# Instantiate the app at the module level
app = create_app()

if __name__ == '__main__':
    app.run()