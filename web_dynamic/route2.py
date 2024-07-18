"""
This is the file that will contain the authenticated and authentication routes
"""
import os.path

from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_required, logout_user, current_user
from forms.user_dash_basic_info import UserBasicInfoForm
from forms.change_password import ChangePwForm
from forms.update_email import UpdateEmailForm
from jwt.exceptions import DecodeError, ExpiredSignatureError
from function_module import *
from forms.audio_upload import UploadMusic
from werkzeug.utils import secure_filename
from route1 import bcrypt
from sqlalchemy.orm import joinedload
import json
from PIL import Image
import os

blueP1 = Blueprint('auth', __name__, url_prefix='/')

Session = storage.session()


@blueP1.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('unauth.homepage'))


@blueP1.route('/account_activation_notification/<email>')
def account_verification_notification_page(email):
    return render_template('email_confirmation.html', email=email, title="Activate Account")


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
    current_user_avatar_name = get_user_avatar_name(current_user.get_id())
    with session_scoped() as session:
        user_songs = session.query(AudioFileInfo).options(joinedload(AudioFileInfo.comments)).filter_by(
            creatorId=current_user.get_id()).order_by(AudioFileInfo.created_at).all()
        groups_id = get_user_groups_id(current_user.get_id())
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
                           get_group_info=get_group_info,
                           title="Dashboard"
                           )


@blueP1.route('/notification', methods=['GET'])
@login_required
def user_notification():
    current_user_avatar_name = get_user_avatar_name(current_user.get_id())
    data_path = os.path.join(app.root_path, 'static/local_storage/echodat_notification/data.json')
    with open(data_path, 'r') as f:
        datas = json.load(f)
    return render_template("user_notification.html",
                           avatar_name=current_user_avatar_name,
                           datas=reversed(datas),
                           list=list,
                           title="Notification"
                           )


@blueP1.route('/dashboard/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    current_user_avatar_name = get_user_avatar_name(current_user.get_id())
    infoForm = UserBasicInfoForm()
    pwResetForm = ChangePwForm()
    emailUpdateForm = UpdateEmailForm()

    if request.method == 'POST':
        if infoForm.validate_on_submit():
            form = infoForm
            try:
                with session_scoped() as session:
                    user = session.query(UserInfo).filter_by(_id=current_user.get_id()).first()
                    user.userName = form.userName.data
                    user.homeTown = form.homeTown.data
                    user.location = form.location.data
                    user.websiteUrl = form.websiteUrl.data
                    user.shortBiography = form.shortBiography.data
                    if form.avatar.data:
                        avatarExt = secure_filename(form.avatar.data.filename).split('.')[-1]
                        filename = f"{user.get_id()}.{avatarExt}"
                        user.pictureAvailability = True
                        saving_path = os.path.join(app.root_path, 'static/users_profile_avatar')
                        os.makedirs(saving_path, exist_ok=True)
                        avatar = form.avatar.data
                        file_path = os.path.join(saving_path, filename)

                        existing_avatar_name = next(iter([name for name in os.listdir(saving_path) if user.get_id() in name]))
                        if existing_avatar_name:
                            os.remove(os.path.join(saving_path, existing_avatar_name))
                        avatar.save(file_path)
                        with Image.open(file_path) as img:
                            img = img.resize((300, 300))
                            img.save(file_path)
            except Exception as e:
                app.logger.error(f'Error: {e}')

            flash('Details Updated', 'success')
        elif pwResetForm.validate_on_submit():
            form = pwResetForm
            with session_scoped() as session:
                user = session.query(UserInfo).filter_by(_id=current_user.get_id()).first()
                user.passWord = bcrypt.generate_password_hash(form.newPassword.data.strip())

                flash('PassWord Updated', 'success')

        elif emailUpdateForm.validate_on_submit():
            form = emailUpdateForm
            with session_scoped() as session:
                user = session.query(UserInfo).filter_by(_id=current_user.get_id()).first()
                user.emailAddress = form.newEmail.data.strip().lower()

                flash('Email Updated', 'success')
        return redirect(url_for('auth.edit_profile'))

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
                           emailUpdateForm=emailUpdateForm,
                           title="Edit Profile"
                           )


@blueP1.route('/profile')
@login_required
def user_profile():
    user_id = request.args.get('user_id')
    if not user_id:
        user_id = current_user.get_id()
    with session_scoped() as session:
        user = session.query(UserInfo).filter_by(_id=user_id).first()
        if not user:
            user = current_user
        uploaded_songs = session.query(AudioFileInfo).filter_by(creatorId=user.get_id()).order_by(AudioFileInfo.created_at).all()
        current_user_avatar_name = get_user_avatar_name(current_user.get_id())
        return render_template("profile.html", avatar_name=current_user_avatar_name,
                               user=user,
                               get_user_avatar_name=get_user_avatar_name,
                               total_group=len(get_user_groups_id(user_id)),
                               total_songs=len(uploaded_songs),
                               uploaded_songs=uploaded_songs,
                               title="Profile"
                               )


@blueP1.route('/upload', methods=['GET', 'POST'])
@login_required
def user_upload():
    current_user_avatar_name = get_user_avatar_name(current_user.get_id())
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
                    creatorId=current_user.get_id()
                )
                session.add(new_audio)
                if form.coverPicture:
                    coverPictureExt = secure_filename(form.coverPicture.data.filename).split('.')[-1]
                    filename = f"{new_audio.get_id()}.{coverPictureExt}"
                    new_audio.framePictureName = filename
                    saving_path = os.path.join(app.root_path, 'static/users_data/audios/avatar')
                    os.makedirs(saving_path, exist_ok=True)
                    avatar = form.coverPicture.data
                    file_path = os.path.join(saving_path, filename)
                    avatar.save(file_path)
                    with Image.open(file_path) as img:
                        img = img.resize((300, 300))
                        img.save(file_path)
                session.commit()
            saving_path = os.path.join(app.root_path, 'static/users_data/audios')
            os.makedirs(saving_path, exist_ok=True)

            file_data = form.file.data
            filename = secure_filename(file_data.filename)
            file_extension = filename.rsplit('.', 1)[-1].lower()

            file_name = f"{current_user.get_id()}_{new_audio.get_id()}.{file_extension}"
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
        user = session.query(UserInfo).filter_by(_id=current_user.get_id()).first()
        session.delete(user)
    logout_user()
    return redirect(url_for('unauth.homepage'))


@blueP1.route('/delete_audio_object')
@login_required
def delete_song_by_id():
    song_id = request.args.get('song_id')
    del_object_by_id(object_id=song_id, object_class='AudioFileInfo')
    flash('Successful Deletion', 'success')
    return redirect(url_for('auth.user_dashboard'))


@blueP1.route('/get_help')
@login_required
def get_help():
    current_user_avatar_name = get_user_avatar_name(current_user.get_id())
    return render_template('help.html',
                           avatar_name=current_user_avatar_name,
                           title="Help"
                           )
