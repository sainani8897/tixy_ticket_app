# controllers/ticket_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db # Assuming 'db' is your SQLAlchemy instance
from models.ticket import Ticket
from models.user import User # Assuming User model exists for current_user and relationships
from models.attachment import Attachment # NEW: Import Attachment model
from forms import TicketForm # Ensure TicketForm is imported
from utils.email_utils import send_email # For email notification
from datetime import datetime, date # Import datetime and date for timestamps/defaults
import os # For file system operations
from werkzeug.utils import secure_filename # For securing filenames
from uuid import uuid4 # For unique filenames

tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets') # Ensure your blueprint has a url_prefix

# --- Helper functions for file uploads ---
def allowed_file(filename):
    """Checks if a file's extension is in the ALLOWED_EXTENSIONS."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_attachment_file(file, ticket_id):
    """
    Saves the uploaded file to disk and creates a corresponding database record.
    Returns True on success, False on failure.
    """
    if file and file.filename != '' and allowed_file(file.filename):
        try:
            original_filename = file.filename
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            
            # Create a unique filename using UUID to prevent clashes
            unique_filename = f"{uuid4().hex}.{file_extension}"
            
            # Secure the original filename (e.g., remove problematic characters)
            secured_original_filename = secure_filename(original_filename)

            # Construct the full path where the file will be saved
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(save_path) # Save the actual file to disk

            # Create an Attachment record in the database
            attachment = Attachment(
                ticket_id=ticket_id,
                filename=secured_original_filename, # Store the user-friendly filename
                stored_filename=unique_filename, # Store the unique filename for disk lookup
                file_path=os.path.relpath(save_path, current_app.root_path), # Relative path from app root
                file_type=file.mimetype, # Get MIME type from the file object
                file_size=os.path.getsize(save_path), # Get actual size of the saved file
                uploaded_by_id=current_user.id,
                uploaded_at=datetime.utcnow()
            )
            db.session.add(attachment)
            db.session.commit() # Commit the attachment immediately
            flash(f'Attachment "{secured_original_filename}" uploaded successfully!', 'success')
            return True
        except Exception as e:
            # Clean up the file if DB commit fails after saving the file
            if os.path.exists(save_path):
                os.remove(save_path)
            db.session.rollback()
            current_app.logger.error(f"Error saving attachment for ticket {ticket_id}: {e}")
            flash(f'Failed to upload attachment: {e}', 'error')
            return False
    elif file and file.filename != '' and not allowed_file(file.filename):
        flash('Invalid file type. Allowed types are: ' + ', '.join(current_app.config['ALLOWED_EXTENSIONS']), 'warning')
        return False
    return False # No file provided or filename empty

# --- ADD TICKET Route ---
@tickets_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_ticket():
    form = TicketForm() # Instantiate the form with the attachment field
    
    if form.validate_on_submit():
        new_ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            reporter_id=current_user.id,
            submitter_email=current_user.email, # If you want to store reporter's email directly
            # Assign optional fields if they exist in your Ticket model and form
            # category=form.category.data, # if you have a category field
            # assigned_to_id=form.assigned_to.data.id if form.assigned_to.data else None, # if you have assigned_to
            due_date=form.due_date.data if form.due_date.data else None
        )
        db.session.add(new_ticket)
        db.session.commit() # Commit here to get the new_ticket.id

        # --- NEW: Handle Attachment Upload from Form ---
        if form.attachment.data: # Check if a file was provided via the form's FileField
            save_attachment_file(form.attachment.data, new_ticket.id)
        # --- END NEW Attachment Handling ---

        # Send email notification for new ticket (existing logic)
        if new_ticket.reporter and new_ticket.reporter.email:
            send_email(
                to_email=new_ticket.reporter.email,
                subject=f"New Ticket Created: #{new_ticket.id} - {new_ticket.title}",
                template='emails/new_ticket_notification.html',
                ticket=new_ticket
            )
            flash('Ticket created successfully and email notification sent!', 'success')
        else:
            flash('Ticket created successfully, but no email notification sent (reporter email not found).', 'warning')
        
        return redirect(url_for('tickets.index')) # Redirect to the tickets list

    # For GET requests or validation failures, render the form
    # Pass current_app.config to the template to display upload limits
    return render_template('tickets/add_ticket.html', form=form, config=current_app.config)


# --- VIEW TICKETS Index Route ---
@tickets_bp.route('/', methods=['GET'])
@login_required
def index():
    if current_user.role == 'user':
        tickets = Ticket.query.filter_by(reporter_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    else: # For admin, show all tickets
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('tickets/index.html', tickets=tickets)


# --- EDIT TICKET Route ---
@tickets_bp.route('/edit/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = TicketForm(obj=ticket) # Populate form fields with existing ticket data

    # Authorization Check: Only reporter or admin can edit
    if current_user.id != ticket.reporter_id and not (hasattr(current_user, 'role') and current_user.role == 'admin'):
        flash('You are not authorized to edit this ticket.', 'danger')
        return redirect(url_for('tickets.index'))

    # Store original values for comparison for email notification
    original_title = ticket.title
    original_description = ticket.description
    original_status = ticket.status
    original_priority = ticket.priority
    original_due_date = ticket.due_date # If you have a due_date field

    if form.validate_on_submit():
        # Update ticket details from form
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.status = form.status.data
        ticket.priority = form.priority.data
        ticket.updated_at = datetime.utcnow() # Update timestamp
        ticket.due_date = form.due_date.data if form.due_date.data else None

        db.session.commit()
        flash(f'Ticket #{ticket.id} updated successfully!', 'success')

        # --- NEW: Handle Attachment Upload from Form ---
        if form.attachment.data: # Check if a file was provided via the form's FileField
            save_attachment_file(form.attachment.data, ticket.id)
        # --- END NEW Attachment Handling ---

        # Prepare and Send Email Notification for Update (existing logic)
        changed_fields = []
        if original_title != ticket.title:
            changed_fields.append(f"Title changed from '{original_title}' to '{ticket.title}'")
        if original_description != ticket.description:
            # For description, you might just state "Description updated" due to length
            changed_fields.append(f"Description has been updated.")
        if original_status != ticket.status:
            changed_fields.append(f"Status changed from '{original_status}' to '{ticket.status}'")
        if original_priority != ticket.priority:
            changed_fields.append(f"Priority changed from '{original_priority}' to '{ticket.priority}'")
        if original_due_date != ticket.due_date:
            changed_fields.append(f"Due Date changed from '{original_due_date.strftime('%Y-%m-%d') if original_due_date else 'N/A'}' to '{ticket.due_date.strftime('%Y-%m-%d') if ticket.due_date else 'N/A'}'")


        recipients = [ticket.reporter.email,ticket.submitter_email] # Always notify the original reporter
        # Add other relevant parties if needed (e.g., assigned user, specific admin)
        # if ticket.assigned_to and ticket.assigned_to.email not in recipients:
        #     recipients.append(ticket.assigned_to.email)

        if recipients: # Only try to send if there's at least one recipient
            send_email(
                to_email=recipients,
                subject=f"Ticket Update: #{ticket.id} - {ticket.title}",
                template='emails/ticket_update_notification.html',
                ticket=ticket,
                updater=current_user,
                changed_fields=changed_fields
            )
            flash('Email notification sent successfully!', 'info')
        else:
            flash('No recipients found for email notification.', 'warning')
        
        return redirect(url_for('tickets.index')) # Redirect to tickets list after edit

    # For GET requests or validation failures:
    # Pre-populate the form (already done by form=TicketForm(obj=ticket))
    # Fetch existing attachments for display
    attachments = Attachment.query.filter_by(ticket_id=ticket.id).order_by(Attachment.uploaded_at.desc()).all()
    # Pass current_app.config to the template to display upload limits
    return render_template('tickets/edit_ticket.html', form=form, ticket=ticket, attachments=attachments, config=current_app.config)


# --- VIEW TICKET Route (displays ticket details and attachments) ---
@tickets_bp.route('/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    # Fetch all attachments related to this ticket
    attachments = Attachment.query.filter_by(ticket_id=ticket.id).order_by(Attachment.uploaded_at.desc()).all()
    
    # You might want to add authorization here too if only certain users can view tickets
    return render_template('tickets/view_ticket.html', ticket=ticket, attachments=attachments)


# --- Optional: Route to delete an attachment ---
# You would link to this from your templates (e.g., edit_ticket.html or view_ticket.html)
# with a small form and a delete button for each attachment.
@tickets_bp.route('/delete_attachment/<int:attachment_id>', methods=['POST'])
@login_required
def delete_attachment(attachment_id):
    attachment = Attachment.query.get_or_404(attachment_id)
    ticket_id = attachment.ticket_id # Get ticket_id before deleting attachment

    # Authorization: Only the uploader, the ticket reporter, or an admin can delete the attachment
    if current_user.id != attachment.uploaded_by_id and \
       current_user.id != attachment.ticket.reporter_id and \
       current_user.role != 'admin':
        flash('You are not authorized to delete this attachment.', 'danger')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))
    
    try:
        # Delete the file from the file system first
        full_file_path = os.path.join(current_app.root_path, attachment.file_path)
        if os.path.exists(full_file_path):
            os.remove(full_file_path)
        
        # Delete the attachment record from the database
        db.session.delete(attachment)
        db.session.commit()
        flash('Attachment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting attachment {attachment_id}: {e}")
        flash(f'Failed to delete attachment: {e}', 'error')
    
    # Redirect back to the ticket's view page
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))