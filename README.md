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
git clone [https://github.com/sainani8897/tixy_ticket_app.git](https://github.com/sainani8897/tixy_ticket_app.git)
cd tixy_ticket_app # Navigate into your project directory