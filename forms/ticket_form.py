# forms/ticket_form.py
from datetime import date
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import  DateField, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length,Optional

class TicketForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=5, max=150)],
        render_kw={"placeholder": "Brief summary of the issue"}
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(min=10)],
        render_kw={"placeholder": "Detailed description of the problem"}
    )
    status = SelectField(
        'Status',
        choices=[
            ('Open', 'Open'),
            ('In Progress', 'In Progress'),
            ('Closed', 'Closed'),
            ('Reopened', 'Reopened')
        ],
        validators=[DataRequired()]
    )
    priority = SelectField(
        'Priority',
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
            ('Urgent', 'Urgent')
        ],
        validators=[DataRequired()]
    )
    due_date = DateField('Due Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[Optional()], default=date.today)
    
    # --- NEW: Attachment Field ---
    # FileAllowed validator dynamically fetches allowed extensions from app.config
    attachment = FileField('Attach File (Max 16MB, Allowed: .png, .jpg, .pdf, .doc, etc.)', validators=[
        FileAllowed({'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'}, 'Only images, PDFs, and documents are allowed!')
    ])
    # If you want to allow multiple files to be selected at once:
    # attachment = FileField('Attach Files', validators=[
    #     FileAllowed(lambda: current_app.config.get('ALLOWED_EXTENSIONS', set()), 'Only allowed file types are permitted!')
    # ], render_kw={"multiple": True}) # You'd then need to handle a list of files in the controller
    submit = SubmitField('Submit Ticket')