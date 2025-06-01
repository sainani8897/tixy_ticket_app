# Tixy - Simple Ticketing Application

![Tixy Logo](https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/static/images/tixy_logo.svg) 
## 📝 Description

Tixy is a lightweight and intuitive ticketing application designed to help teams and individuals manage and track issues, support requests, and tasks efficiently. It provides a clean interface for creating, updating, and viewing tickets, complete with attachment support for better context.

## ✨ Features

* **User Authentication:** Secure login and registration for users.
* **Role-Based Access:** Differentiate between `user` (reporter) and `admin` roles.
* **Ticket Management:**
    * Create new tickets with title, description, status, priority, and due date.
    * Edit existing tickets to update their details.
    * View detailed information for each ticket.
    * List all tickets (admin) or tickets reported by the user (regular user).
* **Attachments & Screenshots:**
    * Attach files and screenshots directly to tickets during creation or editing.
    * View and download existing attachments.
    * Delete attachments (with appropriate authorization).
* **Email Notifications:** Send automated email notifications for new ticket creation and updates.
* **Responsive UI:** Built with Tailwind CSS for a modern and adaptable user experience.
* **Database Migrations:** Utilizes Flask-Migrate for robust database schema management.

## 🛠️ Technologies Used

* **Backend:** Python, Flask
* **Database:** SQLAlchemy (ORM), SQLite (default development database)
* **Database Migrations:** Flask-Migrate (Alembic)
* **Forms:** Flask-WTF, WTForms
* **Email:** Flask-Mail
* **File Uploads:** `werkzeug.utils` for secure filenames, built-in `uuid` for unique naming
* **Frontend:** HTML, CSS (Tailwind CSS), JavaScript (jQuery for DataTables)
* **Version Control:** Git

## 🚀 Setup & Installation

Follow these steps to get Tixy up and running on your local machine.

### Prerequisites

* Python 3.8+
* Git
* A code editor (e.g., VS Code)

### 1. Clone the Repository

First, clone the Tixy repository to your local machine:

```bash
git clone https://github.com/sainani8897/tixy_ticket_app.git
cd tixy_ticket_app # Navigate into your project directory
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
#source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the root directory of your project (same level as main.py) and add your OpenAI and Eleven Labs API keys:

```bash
YOUR_KEYS="your_api_key_here"
```

### 5. Run the Application 

```bash
flask run --debug
```
> **Note:** The `--debug` flag is useful during development as it automatically restarts the server on code changes.

### 6. Access the Frontend
- Open your web browser and navigate to: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Usage

1. **Register**: Navigate to `/auth/register` to create a new user account.
2. **Login**: Use your registered credentials to log in.
3. **Create Tickets**: Go to `/tickets/add` to create new tickets.
4. **View & Edit**: Explore `/tickets` to see all tickets (or your reported tickets) and click on individual tickets to view details or edit them.


## Project Structure

```
.
my_ticketing_app/
├── app.py
│ 
│
├── controllers/                 # Contains blueprint definitions and route logic (views).
│   ├── __init__.py              # Makes 'controllers' a Python package.
│   ├── auth_controller.py       # Handles user authentication routes (login, register, logout).
│   ├── ticket_controller.py     # Manages ticket-related routes (add, edit, view, delete, attachments).
│   ├── dashboard_controller.py  # Handles dashboard or main overview routes.
│   └── (admin_controller.py)    # Optional: For admin-specific routes if separated.
│
├── models/                      # Defines your SQLAlchemy database models.
│   ├── __init__.py              # Makes 'models' a Python package.
│   ├── user.py                  # User model for authentication.
│   ├── ticket.py                # Ticket model for issues/requests.
│   └── attachment.py            # Model for file attachments linked to tickets.
│
├── static/                      # Static assets served directly by the web server (CSS, JS, images).
│   ├── css/
│   │   └── style.css            # Your custom CSS (if any, beyond Tailwind's utility classes).
│   ├── js/
│   │   └── main.js              # Your custom JavaScript files (if any).
│   ├── uploads/                 # **Crucial: This is where uploaded attachments are stored.**
│   │   └── .gitkeep             # (Optional) Empty file to ensure Git tracks an empty folder.
│   └── images/                  # For logos, favicons, or other static images.
│       └── tixy_logo.svg        # Your new Tixy SVG logo.
│
├── templates/                   # HTML templates rendered by Flask.
│   ├── base.html                # Base template for consistent layout across pages.
│   ├── auth/                    # Templates for authentication.
│   │   ├── login.html
│   │   └── register.html
│   ├── tickets/                 # Templates for ticket management.
│   │   ├── index.html           # List of all tickets.
│   │   ├── add_ticket.html      # Form for adding new tickets.
│   │   ├── edit_ticket.html     # Form for editing tickets.
│   │   └── view_ticket.html     # Detailed view of a single ticket.
│   ├── dashboard/
│   │   └── overview.html        # Dashboard overview page.
│   └── emails/                  # Templates for email notifications.
│       ├── new_ticket_notification.html
│       └── ticket_update_notification.html
│
├── utils/                       # Shared utility functions (e.g., email, helpers).
│   ├── __init__.py              # Makes 'utils' a Python package.
│   └── email_utils.py           # Functions for sending emails (Flask-Mail integration).
│
│
├── .env                         # **Environment variables for local development (NOT committed to Git).**
│                                # E.g., SECRET_KEY, DATABASE_URL, MAIL_USERNAME, MAIL_PASSWORD.
├── .flaskenv                    # Optional: Special environment variables for Flask CLI (e.g., FLASK_APP).
├── .gitignore                   # **Tells Git which files/folders to ignore** (e.g., venv, .env, __pycache__, /static/uploads/).
```

## Contributing

Feel free to fork the repository, open issues, or submit pull requests.

## License

This project is open-source and available under the MIT License.
