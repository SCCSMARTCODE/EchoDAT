"""
This is the file that will contain the unauthenticated and authentication routes
"""

from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, session as flask_session
from forms.registration import RegistrationForm
from forms.login import LoginForm
from model.engine import storage
from model.user_info import UserInfo
from flask_bcrypt import Bcrypt
from web_dynamic import app
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from google.oauth2 import id_token
import requests
import secrets
import random
import string
import logging
import os
from pip._vendor import cachecontrol

login_manager = LoginManager()
login_manager.init_app(app)


session = storage.session()
blueP = Blueprint('unauth', __name__, url_prefix='/')
bcrypt = Bcrypt()
GOOGLE_CLIENT_ID = '507577884511-7g8q7a94q8ue0n6l5f0t85m33v0r4nrt.apps.googleusercontent.com'
client_secrets_file = os.path.join(os.path.dirname(__file__), 'static/.system_files/client_secret.json')
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
    return render_template('index.html')


@blueP.route('/about')
def about():
    return "Home page"


@blueP.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            encrypted_password = bcrypt.generate_password_hash(form.passWord.data)  # encrypt my password
            new_user = UserInfo(
                userName=form.userName.data,
                emailAddress=form.emailAddress.data,
                passWord=encrypted_password
            )
            session.add(new_user)
            session.commit()
            return redirect(url_for('unauth.login'))
    return render_template('registration.html', form=form)


@blueP.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = session.query(UserInfo).filter_by(emailAddress=form.emailAddress.data).first()
            if user:
                if not user.passWord:
                    flash(f"Please login {form.emailAddress.data} with google Authentication")
                    return redirect(url_for('unauth.login'))
                if not bcrypt.check_password_hash(user.passWord, form.passWord.data):
                    flash(f"{user.userName} you inputted an Invalid Password \nTry again or use `Forget Password`", 'danger')
                    return redirect(url_for('unauth.login'))
            else:
                flash(f"So Sorry {form.emailAddress.data} does not exists, Try Create an Account or recheck the Email Address", 'danger')
                return redirect(url_for('unauth.login'))
            login_user(user, remember=form.rememberMe.data)
            flash(f'{user.userName} logged in successfully', 'success')
            return redirect(url_for('unauth.homepage'))

    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return session.query(UserInfo).filter_by(_id=user_id).first()


@blueP.route('/contact')
def contact():
    return "Home page"


@blueP.route('/google_reg')
def sign_up_with_google():
    authorization_url, state = flow.authorization_url(access_type='offline', state=gen_state())
    flask_session['state'] = state
    print(f"State stored in session: {flask_session}")
    # return redirect(authorization_url)
    print(f"authorization_url: {authorization_url}")
    return redirect(url_for('unauth.verify_state', authorization_url=authorization_url))


@blueP.route('/verify_state/<path:authorization_url>')
def verify_state(authorization_url):
    print(f"State retrieved from session: {flask_session}")
    if 'state' not in flask_session:
        print("State not found in session!")
        abort(500)

    # Verify state and proceed to OAuth callback
    return redirect(authorization_url)


@blueP.route('/callback')
def google_callback():
    print(f"State retrieved from session: {flask_session}")
    if 'state' not in flask_session:
        print("State not found in session!")
        abort(500)

    print(flask_session['state'])
    if flask_session['state'] != request.args['state']:
        print(flask_session['state'])
        print("here")
        abort(500)  # State does not match!

    try:
        flow.fetch_token(authorization_response=request.url)
    except Exception as e:
        print(f"Error fetching token: {e}")
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    try:
        id_info = id_token.verify_oauth2_token(
            id_token=credentials.id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )
    except Exception as e:
        print(f"Error verifying ID token: {e}")
        abort(500)

    print(dict(id_info))

    user = session.query(UserInfo).filter_by(emailAddress=id_info['email']).first()

    if not user:
        user = UserInfo(
            userName=id_info.get('name'),
            emailAddress=id_info.get('email'),
            passWord=None  # Google account, no password is stored
        )
        session.add(user)
        session.commit()

    login_user(user)
    flash(f'{user.userName} logged in successfully', 'success')
    return redirect(url_for('unauth.homepage'))


def gen_state():
    generated_state = secrets.token_hex(16).upper()
    return generated_state


@blueP.route('redi')
def redi():
    print(f"State retrieved from session: {flask_session}")
    if 'state' not in flask_session:
        print("State not found in session!")
        abort(500)

    return redirect(url_for('unauth.registration'))


if __name__ == '__main__':
    print(gen_state())
