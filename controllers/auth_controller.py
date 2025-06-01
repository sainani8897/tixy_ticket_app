# controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db # Import db object from the main app
from models.user import User # Import the User model
from flask_login import login_user, logout_user, login_required, current_user

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    GET: Displays the registration form.
    POST: Processes the registration form submission.
    """
    if current_user.is_authenticated:
        flash('You are already logged in!', 'info')
        return redirect(url_for('tickets.index'))

    if request.method == 'POST':
        email = request.form.get('email').lower().strip() # Store email as lowercase for consistency
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('auth.register'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('That email is already registered. Please login or use a different email.', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(email=email)
        new_user.set_password(password) # Hash the password

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration. Please try again.', 'error')
            # Log the full exception for debugging: app.logger.error(f"Registration error: {e}")
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    GET: Displays the login form.
    POST: Processes the login form submission.
    """
    if current_user.is_authenticated:
        flash('You are already logged in!', 'info')
        return redirect(url_for('tickets.index'))

    if request.method == 'POST':
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user) # Log the user in
            flash(f'Welcome back, {user.email}!', 'success')
            # Redirect to the page the user was trying to access, or to index
            next_page = request.args.get('next')
            return redirect(next_page or url_for('tickets.index'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required # Requires user to be logged in to access
def logout():
    """Logs out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))