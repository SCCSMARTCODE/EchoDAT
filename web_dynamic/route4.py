from flask import session as flask_session, flash, redirect, url_for, render_template, request
from flask_login import current_user
from flask import Blueprint
from function_module import get_user_avatar_name, format_message
import os
from model.user_info import UserInfo
from model.group_info import GroupInfo
from model.audio_file_info import AudioFileInfo
from function_module import session_scoped
from web_dynamic import app
import json
from datetime import datetime

blueP3 = Blueprint('admin', __name__, url_prefix='/')


@blueP3.route("/Admin_Dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    current_user_avatar_name = 'default-avatar.jpeg'
    if not flask_session.get('IS_ADMIN'):
        flash('Your are not authorized to access this page', 'danger')
        return redirect(url_for('unauth.homepage'))
    with session_scoped() as session:
        status = {
            'users': session.query(UserInfo).count(),
            'groups': session.query(GroupInfo).count(),
            'songs': session.query(AudioFileInfo).count()
        }

    if request.method == 'POST':
        form = request.form
        adminNotification = [{
            str(datetime.utcnow()): {
                'receiver': 'USERS',
                'sender': 'ADMIN',
                'title': form.get('notification-title'),
                'message': format_message(form.get('notification-message'))
            }
        }]

        storage_path = os.path.join('static', 'local_storage', 'echodat_notification')
        os.makedirs(storage_path, exist_ok=True)  # Create the directory if it doesn't exist

        file_path = os.path.join(storage_path, 'data.json').replace('\\', '/')
        # print("\n\nThis is my file path", file_path, '\n\n')
        try:
            with open(file_path, 'x') as f:
                json.dump(adminNotification, f, indent=4)
        except FileExistsError:
            with open(file_path, 'r+') as f:
                json_data = json.load(f)
                json_data.append(next(iter(adminNotification)))
                f.seek(0)  # Move the file pointer to the beginning
                json.dump(json_data, f, indent=4)
                f.truncate()
        flash('Message Sent!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin_dashboard.html',
                           avatar_name=current_user_avatar_name,
                           status=status
                           )


@blueP3.route("/Admin_Notification")
def admin_notification():
    current_user_avatar_name = 'default-avatar.jpeg'
    if not flask_session.get('IS_ADMIN'):
        flash('Your are not authorized to access this page', 'danger')
        return redirect(url_for('unauth.homepage'))

    data_path = os.path.join(app.root_path, 'static/local_storage/echodat_contact/data.json')
    with open(data_path, 'r') as f:
        datas = json.load(f)
    return render_template('admin_notification.html',
                           avatar_name=current_user_avatar_name,
                           datas=datas,
                           list=list
                           )


@blueP3.route("/Admin_Logout")
def admin_logout():
    if not flask_session.get('IS_ADMIN'):
        flash('Your are not authorized to access this page', 'danger')
        return redirect(url_for('unauth.homepage'))
    flask_session['IS_ADMIN'] = False
    return redirect(url_for('unauth.homepage'))
