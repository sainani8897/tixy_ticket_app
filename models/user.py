# models/user.py
from app import db # Import db object from the main app instance
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """
    Represents a user in the database for authentication purposes.
    Inherits UserMixin for Flask-Login integration.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False) # e.g., 'user', 'agent', 'admin'
    
     # NEW: Add the profile_image column
    profile_image = db.Column(db.String(120), nullable=True, default='default.png') # Stores filename, e.g., 'user_id.png'
    
    # Relationships (if you have them defined here)
    # reported_tickets = db.relationship('Ticket', foreign_keys='Ticket.reporter_id', backref='reporter', lazy=True)
    # assigned_tickets = db.relationship('Ticket', foreign_keys='Ticket.assigned_to_id', backref='assignee', lazy=True)

    def set_password(self, password):
        """Hashes the given password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'