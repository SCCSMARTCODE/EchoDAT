from flask import session as flask_session, flash, redirect, url_for, render_template
from flask_login import current_user
from flask import Blueprint
from function_module import get_user_avatar_name

blueP3 = Blueprint('admin', __name__, url_prefix='/')


@blueP3.route("/Admin_Dashboard")
def admin_dashboard():
    current_user_avatar_name = 'default-avatar.jpeg'
    if not flask_session['IS_ADMIN']:
        flash('Your are not authorized to access this page', 'danger')
        return redirect(url_for('unauth.homepage'))
    return render_template('admin_dashboard.html',
                           avatar_name=current_user_avatar_name
                           )


@blueP3.route("/Admin_Notification")
def admin_notification():
    current_user_avatar_name = 'default-avatar.jpeg'
    if not flask_session['IS_ADMIN']:
        flash('Your are not authorized to access this page', 'danger')
        return redirect(url_for('unauth.homepage'))
    return render_template('admin_notification.html',
                           avatar_name=current_user_avatar_name
                           )


@blueP3.route("/Admin_Logout")
def admin_logout():
    if not flask_session['IS_ADMIN']:
        flash('Your are not authorized to access this page', 'danger')
        return redirect(url_for('unauth.homepage'))
    flask_session['IS_ADMIN'] = False
    return redirect(url_for('unauth.homepage'))
