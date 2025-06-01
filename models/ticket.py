# models/ticket.py
from app import db # Import the db object from your main app instance
from datetime import datetime

class Ticket(db.Model):
    """
    Represents a single support ticket in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    submitter_email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), default='Open', nullable=False) # e.g., 'Open', 'In Progress', 'Closed'
    priority = db.Column(db.String(50), default='Medium', nullable=False) # e.g., 'Low', 'Medium', 'High', 'Urgent'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) # <--- THIS LINE!
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    assigned_to = db.Column(db.String(120), nullable=True) # Who the ticket is assigned to
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    reporter = db.relationship('User', backref='tickets', lazy=True)  # Relationship to User model
    #comments = db.relationship('Comment', backref='ticket', lazy=True)  # Relationship to Comment model
    
    # NEW: Add the due_date column
    due_date = db.Column(db.Date, nullable=True) # Use db.Date for date-only values, nullable=True if it's optional

    def __repr__(self):
        return f"Ticket('{self.id}', '{self.title}', '{self.status}', '{self.priority}')"