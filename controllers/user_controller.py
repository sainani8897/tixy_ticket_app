# controllers/user_controller.py
import os
import uuid
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from forms.profile_form import ProfileEditForm
from models.user import User # Import the User model
from app import db # Assuming 'db' is your SQLAlchemy instance

user_bp = Blueprint('user', __name__)

# Helper function to save profile picture
def save_profile_picture(form_picture):
    random_hex = uuid.uuid4().hex # Generate a unique hex string
    _, f_ext = os.path.splitext(form_picture.filename) # Get file extension
    picture_fn = random_hex + f_ext # Create unique filename
    picture_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], picture_fn)

    # Resize image if necessary (optional, but good practice for profile pictures)
    # from PIL import Image
    # output_size = (125, 125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)

    form_picture.save(picture_path) # Save the picture

    return picture_fn # Return the unique filename

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileEditForm(original_email=current_user.email) # Pass original email for validation
    
    if form.validate_on_submit():
        if form.profile_picture.data:
            # Delete old profile picture if it's not the default one
            if current_user.profile_image != 'default.png':
                old_picture_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], current_user.profile_image)
                if os.path.exists(old_picture_path):
                    try:
                        os.remove(old_picture_path)
                        current_app.logger.info(f"Deleted old profile picture: {old_picture_path}")
                    except OSError as e:
                        current_app.logger.error(f"Error deleting old profile picture {old_picture_path}: {e}")

            picture_file = save_profile_picture(form.profile_picture.data)
            current_user.profile_image = picture_file
        
        current_user.email = form.email.data
        # If you added password fields to the form, update here:
        # if form.password.data:
        #     current_user.set_password(form.password.data)

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        # If you had other fields, pre-populate them here

    profile_image_url = url_for('static', filename='uploads/' + current_user.profile_image)
    return render_template('profile/profile.html', title='Profile', form=form, profile_image_url=profile_image_url)