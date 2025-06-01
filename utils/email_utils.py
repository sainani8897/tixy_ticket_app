# utils/email_utils.py
from flask_mail import Message
from models.config import Config
from flask import render_template, current_app # Import current_app and render_template
from app import mail # Import mail object

def send_email(to_email, subject, template, **kwargs):
    """
    Sends an email using Flask-Mail. Fetches SMTP settings from the database
    before each email attempt.
    
    Args:
        to_email (str or list): The recipient's email address(es).
        subject (str): The subject of the email.
        template (str): The name of the Jinja2 template file (e.g., 'emails/new_ticket_notification.html').
        **kwargs: Context variables to pass to the email template.
    """
    with current_app.app_context():
        config = Config.query.first()

        if not config or not all([config.smtp_host, config.smtp_port, config.smtp_username, config.smtp_password, config.smtp_sender_email]):
            print("ERROR: SMTP settings are incomplete. Email cannot be sent.")
            return False  # Prevent sending if settings are invalid

        # Apply config directly to current_app.config for Flask-Mail to pick up
        current_app.config['MAIL_SERVER'] = config.smtp_host
        current_app.config['MAIL_PORT'] = config.smtp_port
        current_app.config['MAIL_USE_TLS'] = config.smtp_use_tls
        current_app.config['MAIL_USERNAME'] = config.smtp_username
        current_app.config['MAIL_PASSWORD'] = config.smtp_password
        current_app.config['MAIL_DEFAULT_SENDER'] = config.smtp_sender_email

        # Re-initialize Flask-Mail with the current app's configuration
        # This ensures the mail object is aware of the latest config changes.
        mail.init_app(current_app) # Re-initialize Flask-Mail

        # Ensure recipients is a list
        recipients_list = [to_email] if isinstance(to_email, str) else to_email

        try:
            msg = Message(
                subject=subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=recipients_list # Now accepts a list
            )
            msg.html = render_template(template, **kwargs)
            mail.send(msg)
            print(f"Email successfully sent to {', '.join(recipients_list)} with subject '{subject}'")
            return True
        except Exception as e:
            print(f"ERROR: Failed to send email to {', '.join(recipients_list)}. Subject: '{subject}'. Error: {e}")
            return False