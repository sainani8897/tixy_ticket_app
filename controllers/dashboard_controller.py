# controllers/dashboard_controller.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db # Needed for database queries
from models.ticket import Ticket # Needed to query tickets
from models.user import User # Needed to query users if displaying user stats

# Create a Blueprint for the dashboard
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required # Dashboard requires login
def overview():
    """
    Renders the dashboard page with summary statistics.
    """
    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status='Open').count()
    in_progress_tickets = Ticket.query.filter_by(status='In Progress').count()
    closed_tickets = Ticket.query.filter_by(status='Closed').count()

    # Tickets by Priority
    tickets_by_priority = {
        'Urgent': Ticket.query.filter_by(priority='Urgent').count(),
        'High': Ticket.query.filter_by(priority='High').count(),
        'Medium': Ticket.query.filter_by(priority='Medium').count(),
        'Low': Ticket.query.filter_by(priority='Low').count()
    }

    # Only show total users for 'admin' role
    total_users = None
    if current_user.role == 'admin':
        total_users = User.query.count()
    
    # You can add more complex queries here, e.g., tickets submitted by current_user,
    # tickets assigned to current_user, etc.

    context = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'closed_tickets': closed_tickets,
        'tickets_by_priority': tickets_by_priority,
        'total_users': total_users
    }

    return render_template('dashboard.html', **context)