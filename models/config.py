# models/config.py
from app import db # Import db object from the main app instance

class Config(db.Model):
    """
    Stores global application configurations, such as SMTP settings.
    Designed to have only one row.
    """
    id = db.Column(db.Integer, primary_key=True, default=1) # Default to 1 to ensure single row

    # SMTP Configuration
    smtp_host = db.Column(db.String(100), default='smtp.example.com')
    smtp_port = db.Column(db.Integer, default=587)
    smtp_use_tls = db.Column(db.Boolean, default=True)
    smtp_username = db.Column(db.String(100), nullable=True)
    smtp_password = db.Column(db.String(100), nullable=True) # Store password directly for simplicity here
    smtp_sender_email = db.Column(db.String(100), default='no-reply@yourdomain.com')

    def __repr__(self):
        return f'<Config ID: {self.id}>'