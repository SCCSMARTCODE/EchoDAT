"""
This is the file that will contain the unauthenticated and authentication routes
"""

from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, session as flask_session
from forms.registration import RegistrationForm
from forms.login import LoginForm
from forms.comment import CommentForm
from forms.reset_password import PasswordResetForm
from forms.verify_email import EmailVerificationForm
# from model.engine import storage
# from model.user_info import UserInfo
# from model.audio_file_info import AudioFileInfo
from flask_bcrypt import Bcrypt
from web_dynamic import app
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from google.oauth2 import id_token
from function_module import *
import requests
import secrets
import random
import string
import logging
import os
from pip._vendor import cachecontrol
import imghdr
from PIL import Image
from sqlalchemy.orm import joinedload
import json

login_manager = LoginManager()
login_manager.init_app(app)


blueP = Blueprint('unauth', __name__, url_prefix='/')
bcrypt = Bcrypt()
GOOGLE_CLIENT_ID = '507577884511-7g8q7a94q8ue0n6l5f0t85m33v0r4nrt.apps.googleusercontent.com'
client_secrets_file = os.path.join(os.path.dirname(__file__), 'static/system_files/client_secret.json')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file.replace('/', '\\'),
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)


logging.basicConfig(level=logging.DEBUG)


@blueP.route('/')
@blueP.route('/home')
def homepage():
    if current_user.is_authenticated:
        current_user_avatar_name = get_user_avatar_name(current_user._id)
    else:
        current_user_avatar_name = 'default-avatar.jpeg'

    with session_scoped() as session:
        audios = {
            'trending_songs': ['Trending Songs', session.query(AudioFileInfo).order_by(desc(AudioFileInfo.likesCount)).all()],
            'recently_added': ['Recently Added', session.query(AudioFileInfo).order_by(AudioFileInfo.created_at.desc()).all()]
        }
        filter_ = request.args.get('filter')
        if filter_:
            audios = {filter_: audios.get(filter_)}

    return render_template('index.html',
                           avatar_name=current_user_avatar_name,
                           audios=audios
                           )


@blueP.route('/about')
def about():
    if current_user.is_authenticated:
        current_user_avatar_name = get_user_avatar_name(current_user._id)
    else:
        current_user_avatar_name = 'default-avatar.jpeg'
    return render_template('about_us.html',
                           avatar_name=current_user_avatar_name
                           )


@blueP.route('/contact', methods=['GET', 'POST'])
def contact():
    if current_user.is_authenticated:
        current_user_avatar_name = get_user_avatar_name(current_user._id)
    else:
        current_user_avatar_name = 'default-avatar.jpeg'

    if request.method == 'POST':
        form = request.form
        contactNotification = [{
            str(datetime.utcnow()): {
                'receiver': 'ADMIN',
                'sender': form.get('name'),
                'sender_email': form.get('email'),
                'message_subject': form.get('subject'),
                'message': format_message(form.get('message'))
            }
        }]

        storage_path = os.path.join('static', 'local_storage', 'echodat_contact')
        os.makedirs(storage_path, exist_ok=True)  # Create the directory if it doesn't exist

        file_path = os.path.join(storage_path, 'data.json').replace('\\', '/')
        try:
            with open(file_path, 'x') as f:
                json.dump(contactNotification, f, indent=4)
        except FileExistsError:
            with open(file_path, 'r+') as f:
                json_data = json.load(f)
                json_data.append(next(iter(contactNotification)))
                f.seek(0)
                json.dump(json_data, f, indent=4)
                f.truncate()
        flash('Message Sent!', 'success')
        return redirect(url_for('unauth.homepage'))
    return render_template('contact.html',
                           avatar_name=current_user_avatar_name
                           )


@blueP.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('unauth.homepage'))

    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            encrypted_password = bcrypt.generate_password_hash(form.passWord.data).decode('utf-8')  # encrypt the password
            with session_scoped() as session:
                new_user = UserInfo(
                    userName=form.userName.data.strip(),
                    emailAddress=form.emailAddress.data.strip(),
                    passWord=encrypted_password,
                    status=False
                )
                session.add(new_user)
                session.commit()

            send_user_account_activation_mail(new_user)

            return redirect(url_for('auth.account_verification_notification_page', email=new_user.emailAddress))
    return render_template('registration.html', form=form)


@blueP.route('/login/<email>', methods=['POST', 'GET'])
@blueP.route('/login', methods=['POST', 'GET'])
def login(email=""):
    if not request.args.get('SA'):
        if current_user.is_authenticated:
            return redirect(url_for('unauth.homepage'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            if form.emailAddress.data == app.config['ECHODAT_REG_ADMIN_MAIL_ACCOUNT']:
                flask_session['IS_ADMIN'] = True
                return redirect(url_for('admin.admin_dashboard'))
            with session_scoped() as session:
                user = session.query(UserInfo).filter_by(emailAddress=form.emailAddress.data.strip()).first()
                if user:
                    if not user.status:
                        flash(f'Sorry, this account has not been activated. An activation email has been sent to {user.emailAddress}.', 'warning')
                        send_user_account_activation_mail(user)
                        return redirect(url_for('unauth.login'))
                    if not user.passWord:
                        flash(f'Please log in with Google Authentication using {form.emailAddress.data}.', 'danger')
                        return redirect(url_for('unauth.login'))
                    if not bcrypt.check_password_hash(user.passWord, form.passWord.data):
                        flash(f'Invalid password for {user.userName}. Please try again or use the "Forgot Password" option.', 'danger')
                        return redirect(url_for('unauth.login'))
                else:
                    flash(f'Sorry, the email address {form.emailAddress.data} does not exist. Please create an account or double-check the email address.', 'danger')
                    return redirect(url_for('unauth.login'))
                login_user(user, remember=form.rememberMe.data)
                flash(f'{user.userName} logged in successfully.', 'success')
                return redirect(url_for('unauth.homepage'))
    if email:
        form.emailAddress.data = email
    return render_template('login.html', form=form)


@blueP.route('/view/audio', methods=['POST', 'GET'])
def view_public_audio():
    if current_user.is_authenticated:
        current_user_avatar_name = get_user_avatar_name(current_user._id)
    else:
        current_user_avatar_name = 'default-avatar.jpeg'

    audio_id = request.args.get('id')
    if not audio_id:
        abort(404)

    with session_scoped() as session:
        audio = session.query(AudioFileInfo).options(joinedload(AudioFileInfo.creator)).filter_by(_id=audio_id).first()
        if not audio:
            abort(404)

        form = CommentForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                new_comment = MessageInfo(
                    commentToId=audio_id,
                    creatorId=current_user._id,
                    message=form.comment.data
                )
                session.add(new_comment)
                session.commit()
                return redirect(request.url)

        messages = session.query(MessageInfo).filter_by(commentToId=audio_id).order_by(MessageInfo.created_at.desc()).all()

    return render_template('audio_view.html', len=len, form=form, messages=messages, avatar_name=current_user_avatar_name, audio=audio, get_user_avatar_name=get_user_avatar_name, get_audio_filename_by_id=get_audio_filename_by_id)


@blueP.route('/reset_password_check/email_verification', methods=['GET', 'POST'])
def reset_password_email_verification():
    """
    This leads to getting user email for password reset.
    """
    form = EmailVerificationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.emailAddress.data
            with session_scoped() as session:
                user = session.query(UserInfo).filter_by(emailAddress=email).first()
                if not user:
                    flash('Invalid Email Address', 'danger')
                    return redirect(url_for('unauth.login'))
                send_password_reset_mail(user)
                flash('A password reset email has been sent to your email address.', 'success')
                return redirect(url_for('unauth.login'))
    return render_template('password_reset_email_verification.html', form=form)


@blueP.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """This function helps reset the password"""
    with session_scoped() as session:
        try:
            secret_token = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            flash('Sorry, the token has expired.', "info")
            return redirect(url_for('unauth.homepage'))
        except jwt.DecodeError:
            flash('Sorry, the token is invalid.', "danger")
            return redirect(url_for('unauth.homepage'))

        form = PasswordResetForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                user_id = secret_token.get('user_id')
                user = session.query(UserInfo).filter_by(_id=user_id).first()
                if user:
                    user.passWord = bcrypt.generate_password_hash(form.newPassword.data)
                    session.commit()
                    flash('Password updated successfully.', 'info')
                    return redirect(url_for('unauth.login', email=user.emailAddress))
        return render_template('password_reset.html', title='Reset Password', form=form)


@blueP.route('/google_reg')
def sign_up_with_google():
    authorization_url, state = flow.authorization_url(access_type='offline', state=gen_state())
    flask_session['state'] = state
    return redirect(url_for('unauth.verify_state', authorization_url=authorization_url))


@blueP.route('/callback')
def google_callback():
    with session_scoped() as session:
        print(f"State retrieved from session: {flask_session}")
        # if 'state' not in flask_session:
        #     print("State not found in session!")
        #     abort(500)
        #
        # print(flask_session['state'])
        # if flask_session['state'] != request.args['state']:
        #     print(flask_session['state'])
        #     print("here")
        #     abort(500)  # State does not match!

        try:
            flow.fetch_token(authorization_response=request.url)
        except Exception as e:
            print(f"Error fetching token: {e}")
            abort(500)

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials.id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        user = session.query(UserInfo).filter_by(emailAddress=id_info['email']).first()

        if not user:
            user = UserInfo(
                userName=pick_random_google_userName(id_info.get('name')),
                emailAddress=id_info.get('email'),
                passWord=None  # Google account, no password is stored
            )
            picture_link = id_info.get('picture')
            if picture_link:
                picture = requests.get(picture_link, stream=True)
                print(picture.status_code)
                if picture.status_code == 200:
                    filename = f'{user._id}'
                    filepath = os.path.join(app.root_path, f'static/users_profile_avatar/{filename}').replace('\\', '/')
                    with open(filepath, 'wb') as f:
                        for chunk in picture.iter_content(1024):
                            f.write(chunk)
                    extension = imghdr.what(filepath)
                    if extension:
                        real_file_name = f'{filename}.{extension}'
                        real_file_path = os.path.join(app.root_path, f'static/users_profile_avatar/{real_file_name}').replace('\\', '/')
                        os.rename(filepath, real_file_path)
                        with Image.open(real_file_path) as img:
                            img = img.resize((300, 300))
                            img.save(real_file_path)

                        user.pictureAvailability = True
                        print(f"User here with pictureAvailability as {user.pictureAvailability}")
                    else:
                        print("Unable to determine the file extension.")
                        os.remove(filepath)
                else:
                    print(f"Failed to download image, status code: {picture.status_code}")

            session.add(user)
            session.commit()

        login_user(user)
        flash(f'{user.userName} logged in successfully', 'success')
        return redirect(url_for('unauth.homepage'))


@login_manager.user_loader
def load_user(user_id):
    with session_scoped() as session:
        return session.query(UserInfo).filter_by(_id=user_id).first()



@blueP.route('/verify_state/<path:authorization_url>')
def verify_state(authorization_url):
    if 'state' not in flask_session:
        abort(500)

    # Verify state and proceed to OAuth callback
    return redirect(authorization_url)
