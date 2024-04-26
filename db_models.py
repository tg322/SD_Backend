from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
    Generates the models for each table in the database.
    
    """

class ticket_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    PassHash = db.Column(db.String(250))
    Role = db.Column(db.Integer)

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_subject = db.Column(db.String(150))
    ticket_body = db.Column(db.String(3000))
    ticket_category = db.Column(db.Integer)
    ticket_from_id = db.Column(db.Integer)
    ticket_date_sent = db.Column(db.DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    ticket_status = db.Column(db.String(50), nullable=False, default='Open')

class encryption_key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encrypt_key = db.Column(db.String(250))

class roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50))