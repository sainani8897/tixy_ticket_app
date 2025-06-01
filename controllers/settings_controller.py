# controllers/settings_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db, app, mail # Import app and mail for dynamic configuration
from models.config import Config
import functools # <--- ADD THIS IMPORT

settings_bp = Blueprint('settings', __name__)

# Helper function to check if the current user is an admin
def admin_required(f):
    """
    Decorator to restrict access to admin users only.
    """
    @functools.wraps(f) # <--- ADD THIS LINE!
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied. You do not have administrative privileges.', 'error')
            return redirect(url_for('dashboard.overview')) # Redirect to dashboard
        return f(*args, **kwargs)
    return decorated_function

@settings_bp.route('/smtp', methods=['GET', 'POST'])
@admin_required # Only admin users can access this route
def smtp_settings():
    """
    Manages SMTP server configuration.
    GET: Displays the current SMTP settings form.
    POST: Updates the SMTP settings.
    """
    config = Config.query.first()
    if not config: # Should not happen if app.py initializes it
        config = Config()
        db.session.add(config)
        db.session.commit()

    if request.method == 'POST':
        config.smtp_host = request.form.get('smtp_host', '').strip()
        config.smtp_port = int(request.form.get('smtp_port', 587))
        config.smtp_use_tls = 'smtp_use_tls' in request.form
        config.smtp_username = request.form.get('smtp_username', '').strip()
        config.smtp_password = request.form.get('smtp_password', '').strip()
        config.smtp_sender_email = request.form.get('smtp_sender_email', '').strip()

        try:
            db.session.commit()

            # Dynamically update Flask-Mail configuration
            app.config['MAIL_SERVER'] = config.smtp_host
            app.config['MAIL_PORT'] = config.smtp_port
            app.config['MAIL_USE_TLS'] = config.smtp_use_tls
            app.config['MAIL_USERNAME'] = config.smtp_username
            app.config['MAIL_PASSWORD'] = config.smtp_password
            app.config['MAIL_DEFAULT_SENDER'] = config.smtp_sender_email

            print("\n--- Flask-Mail Configuration AFTER UPDATE ---")
            print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
            print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
            print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
            print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
            print(f"MAIL_PASSWORD (first 5 chars): {str(app.config.get('MAIL_PASSWORD'))[:5]}*****")
            print(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
            print("-------------------------------------------\n")

            flash('SMTP settings updated successfully!', 'success')
            return redirect(url_for('settings.smtp_settings'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving SMTP settings: {e}', 'error')

    return render_template('settings/smtp_settings.html', config=config)