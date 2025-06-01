# forms/ticket_form.py
from datetime import date
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # Make sure FileAllowed is imported here
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Optional, Email, ValidationError
from models.user import User # Import User model to check for existing email

class ProfileEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Optional: If you want to allow changing password directly on this form, add PasswordField
    # password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    # confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password', message='Passwords must match')])
    
    profile_picture = FileField('Update Profile Picture', validators=[
         FileAllowed({'png', 'jpg', 'jpeg'}, 'Only images')
    ])
    submit = SubmitField('Update Profile')

    # Custom validation for email to prevent changing to an already existing email (excluding current user's email)
    def __init__(self, original_email, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                raise ValidationError('That email is already taken. Please choose a different one.')