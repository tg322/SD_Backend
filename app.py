# app.py
from flask import Flask
from flask_cors import CORS
from db_models import *
  # Importing db and models

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/software_agile'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # It's a good practice to disable this

    db.init_app(app)  # Initialize db with the app

    # Optionally, import and register your blueprints here

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)