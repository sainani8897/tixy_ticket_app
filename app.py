import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate # NEW: Import Migrate

# Initialize Flask app
app = Flask(__name__)

template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir) # <--- MODIFY THIS LINE

# --- Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_strong_and_unique_secret_key_here'

# Flask-Mail configuration (initial empty values, will be loaded from DB)
# Looking to send emails in production? Check out our Email API/SMTP product!
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '80941df966aa07'
app.config['MAIL_PASSWORD'] = '476d34f543d474'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Base URL for external links in emails (important for url_for(_external=True))
app.config['BASE_URL'] = os.environ.get('BASE_URL') or 'http://127.0.0.1:5000' # Change this for production!

# --- Attachment Upload Settings ---
# Define the upload folder relative to the app's root directory
# Files will be saved in your_app_root/static/uploads/
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
# Allowed file extensions (add/remove as needed)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'}
# Max file size in bytes (e.g., 16 MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 Megabytes

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Initialize Flask-Mail
mail = Mail(app)

# --- Import Models ---
from models.ticket import Ticket
from models.user import User
from models.config import Config
from models.attachment import Attachment

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Database Initialization ---
with app.app_context():
    db.create_all()
    if not Config.query.first():
        default_config = Config()
        db.session.add(default_config)
        db.session.commit()
    else: # Add this else block to load existing config immediately at startup
        config = Config.query.first()
        app.config['MAIL_SERVER'] = config.smtp_host
        app.config['MAIL_PORT'] = config.smtp_port
        app.config['MAIL_USE_TLS'] = config.smtp_use_tls
        app.config['MAIL_USERNAME'] = config.smtp_username
        app.config['MAIL_PASSWORD'] = config.smtp_password
        app.config['MAIL_DEFAULT_SENDER'] = config.smtp_sender_email
    
    print("\n--- Flask-Mail Configuration ---")
    print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"MAIL_PASSWORD (first 5 chars): {str(app.config.get('MAIL_PASSWORD'))[:5]}*****") # Don't print full password
    print(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
    print("--------------------------------\n")



# --- Register Blueprints ---
from controllers.ticket_controller import tickets_bp
from controllers.auth_controller import auth_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.settings_controller import settings_bp # NEW: Import settings blueprint

app.register_blueprint(tickets_bp, url_prefix='/tickets')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(settings_bp, url_prefix='/settings') # NEW: Register settings blueprint

# --- Redirect root to dashboard (requires login) ---
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard.overview'))

# --- Run the Flask Application ---
if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('templates/settings', exist_ok=True) # Ensure settings templates folder exists
    os.makedirs('models', exist_ok=True)
    os.makedirs('controllers', exist_ok=True)
    os.makedirs('utils', exist_ok=True)
    os.makedirs('templates/emails', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    

    app.run(debug=True)