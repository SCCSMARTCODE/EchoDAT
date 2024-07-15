"""
This is the file that will contain the authenticated and authentication routes
"""

from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_required, logout_user, current_user
from model.user_info import UserInfo
from model.audio_file_info import AudioFileInfo
from model.group_registration_info import GroupRegistrationInfo
from model.engine import storage
from forms.user_dash_basic_info import UserBasicInfoForm
from forms.change_password import ChangePwForm
from forms.update_email import UpdateEmailForm
from jwt.exceptions import DecodeError, ExpiredSignatureError
from function_module import *
from forms.audio_upload import UploadMusic
from werkzeug.utils import secure_filename
from route1 import bcrypt
from sqlalchemy.orm import joinedload

blueP1 = Blueprint('auth', __name__, url_prefix='/')

Session = storage.session()


@blueP1.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('unauth.homepage'))


@blueP1.route('/account_activation_notification/<email>')
def account_verification_notification_page(email):
    return render_template('email_confirmation.html', email=email)


@blueP1.route('/account_activation/<token>')
def account_verification_url(token):
    try:
        secret_token = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
    except ExpiredSignatureError:
        flash('Sorry, the token has expired.', "info")
        return redirect(url_for('unauth.homepage'))
    except DecodeError:
        flash('Sorry, the token is invalid.', "danger")
        return redirect(url_for('unauth.homepage'))

    user_id = secret_token.get('user_id')
    with session_scoped() as session:
        user = session.query(UserInfo).filter_by(_id=user_id).first()
        if user:
            if user.status:
                return redirect(url_for('unauth.login', email=user.emailAddress))
            user.status = True
            session.commit()
            flash('Account verification successful.', 'success')
        else:
            flash('This account does not exist. Please try registering a new account.', 'danger')
            return redirect(url_for('unauth.registration'))
        return redirect(url_for('unauth.login', email=user.emailAddress))


@blueP1.route('/dashboard', methods=['GET'])
@login_required
def user_dashboard():
    current_user_avatar_name = get_user_avatar_name(current_user._id)
    with session_scoped() as session:
        user_songs = session.query(AudioFileInfo).options(joinedload(AudioFileInfo.comments)).filter_by(
            creatorId=current_user._id).order_by(AudioFileInfo.created_at).all()
        groups_id = get_user_groups_id(current_user._id)
        response1 = {
            "user_songs": user_songs,
            "total_songs": len(user_songs),
            "user_groups_id": groups_id,
            "total_groups": len(groups_id),
            "object_len": len
        }
    return render_template("dashboard.html",
                           avatar_name=current_user_avatar_name,
                           get_object_by_id=get_object_by_id,
                           response1=response1,
                           get_group_info=get_group_info
                           )


@blueP1.route('/dashboard/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    current_user_avatar_name = get_user_avatar_name(current_user._id)
    infoForm = UserBasicInfoForm()
    pwResetForm = ChangePwForm()
    emailUpdateForm = UpdateEmailForm()

    if request.method == 'POST':
        form = None
        if infoForm.validate_on_submit():
            form = infoForm
            with session_scoped() as session:
                user = session.query(UserInfo).filter_by(_id=current_user._id).first()
                user.userName = form.userName.data
                user.homeTown = form.homeTown.data
                user.location = form.location.data
                user.websiteUrl = form.websiteUrl.data
                user.shortBiography = form.shortBiography.data

                flash('Details Updated', 'success')
        elif pwResetForm.validate_on_submit():
            form = pwResetForm
            with session_scoped() as session:
                user = session.query(UserInfo).filter_by(_id=current_user._id).first()
                user.passWord = bcrypt.generate_password_hash(form.newPassword.data.strip())

                flash('PassWord Updated', 'success')

        elif emailUpdateForm.validate_on_submit():
            form = emailUpdateForm
            with session_scoped() as session:
                user = session.query(UserInfo).filter_by(_id=current_user._id).first()
                user.emailAddress = form.newEmail.data.strip().lower()

                flash('Email Updated', 'success')

        return redirect(url_for('auth.user_dashboard'))

    infoForm.userName.data = current_user.userName
    infoForm.homeTown.data = current_user.homeTown
    infoForm.websiteUrl.data = current_user.websiteUrl
    infoForm.location.data = current_user.location
    infoForm.shortBiography.data = current_user.shortBiography
    emailUpdateForm.currentEmail.data = current_user.emailAddress

    return render_template("dashboard_edit_profile.html",
                           avatar_name=current_user_avatar_name,
                           infoForm=infoForm,
                           pwResetForm=pwResetForm,
                           emailUpdateForm=emailUpdateForm
                           )


@blueP1.route('/profile')
@login_required
def user_profile():
    user_id = request.args.get('user_id')
    if not user_id:
        user_id = current_user._id
    with session_scoped() as session:
        user = session.query(UserInfo).filter_by(_id=user_id).first()
        if not user:
            user = current_user
        uploaded_songs = session.query(AudioFileInfo).filter_by(creatorId=user._id).order_by(AudioFileInfo.created_at).all()
        current_user_avatar_name = get_user_avatar_name(current_user._id)
        return render_template("profile.html", avatar_name=current_user_avatar_name,
                               user=user,
                               get_user_avatar_name=get_user_avatar_name,
                               total_group=len(get_user_groups_id(user_id)),
                               total_songs=len(uploaded_songs),
                               uploaded_songs=uploaded_songs
                               )


@blueP1.route('/upload', methods=['GET', 'POST'])
@login_required
def user_upload():
    current_user_avatar_name = get_user_avatar_name(current_user._id)
    form = UploadMusic()

    if request.method == 'POST':
        if form.validate_on_submit():
            with session_scoped() as session:
                new_audio = AudioFileInfo(
                    title=form.title.data,
                    artist=form.artist.data,
                    featuring=form.featuring.data,
                    producersName=form.producers.data,
                    genre=form.genre.data,
                    mood=form.mood.data,
                    caption=form.caption.data,
                    release='PUBLIC' if form.release.data else 'PRIVATE',
                    creatorId=current_user._id
                )
                session.add(new_audio)
                session.commit()

            saving_path = os.path.join(app.root_path, 'static/users_data')
            os.makedirs(saving_path, exist_ok=True)

            file_data = form.file.data
            filename = secure_filename(file_data.filename)
            file_extension = filename.rsplit('.', 1)[-1].lower()

            file_name = f"{current_user._id}_{new_audio._id}.{file_extension}"
            file_data.save(os.path.join(saving_path, file_name))

            flash('Upload Successful', 'success')
            return redirect(url_for('auth.user_dashboard'))

    return render_template("upload.html", avatar_name=current_user_avatar_name, title='Upload', form=form)


@blueP1.route('/delete_user_account')
@login_required
def delete_user_account():
    """
    This route is still not perfect I have to delete user data to make it perfect


    check this out man
    :return:
    """
    with session_scoped() as session:
        user = session.query(UserInfo).filter_by(_id=current_user._id).first()
        session.delete(user)
    logout_user()
    return redirect(url_for('unauth.homepage'))


@blueP1.route('/delete_audio_object')
def delete_song_by_id():
    song_id = request.args.get('song_id')
    del_object_by_id(object_id=song_id, object_class='AudioFileInfo')
    return redirect(url_for('auth.user_dashboard'))


@blueP1.route('/get_help')
def get_help():
    current_user_avatar_name = get_user_avatar_name(current_user._id)
    return render_template('help.html',
                           avatar_name=current_user_avatar_name
                           )
