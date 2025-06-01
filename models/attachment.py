# models/attachment.py
from datetime import datetime
from app import db # Assuming 'db' is your SQLAlchemy instance from app.py/app/__init__.py

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False) # Original filename provided by user
    stored_filename = db.Column(db.String(255), unique=True, nullable=False) # Unique filename on server
    file_path = db.Column(db.String(500), nullable=False) # Full relative path from app root
    file_type = db.Column(db.String(100), nullable=True) # MIME type (e.g., 'image/png')
    file_size = db.Column(db.BigInteger, nullable=True) # Size in bytes
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    ticket = db.relationship('Ticket', backref=db.backref('attachments', lazy=True, cascade="all, delete-orphan"))
    uploader = db.relationship('User', backref=db.backref('uploaded_attachments', lazy=True))

    def __repr__(self):
        return f"<Attachment {self.filename} for Ticket {self.ticket_id}>"