# app.py
from flask import Blueprint, Flask
from flask_cors import CORS
from db_models import db  # Import only db, not all models globally if not needed

# Define the Blueprint
auth_bp = Blueprint('auth', __name__)
tickets_bp = Blueprint('tickets', __name__)
# Import route handlers
from user_access_endpoints import login_user, sign_up_user, test_get_auth_token, logout

# Attach the route handlers to the blueprintd
auth_bp.route('/login', methods=['POST'])(login_user)
auth_bp.route('/me', methods=['GET'])(test_get_auth_token)
auth_bp.route('/signup', methods=['POST'])(sign_up_user)
auth_bp.route('/logout', methods=['POST'])(logout)

from tickets import get_tickets, get_ticket_by_id, close_ticket, open_ticket, delete_ticket
tickets_bp.route('/gettickets', methods=['GET'])(get_tickets)
tickets_bp.route('/getticket', methods=['POST'])(get_ticket_by_id)
tickets_bp.route('/closeticket', methods=['POST'])(close_ticket)
tickets_bp.route('/openticket', methods=['POST'])(open_ticket)
tickets_bp.route('/deleteticket', methods=['POST'])(delete_ticket)

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={ "/*": {"origins": ["https://localhost:3000"]}})
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/software_agile'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize db with the app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  # url_prefix

    app.register_blueprint(tickets_bp, url_prefix='/api/tickets')  # url_prefix

    return app

# Instantiate the app at the module level
app = create_app()

if __name__ == '__main__':
    app.run(
        debug=True,
        ssl_context=('localhost.pem', 'localhost-key.pem'),
        host='localhost',
        port=5000)