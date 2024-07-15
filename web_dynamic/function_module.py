"""
This is the file that contains EchoDAT running app Functions
"""
from web_dynamic import app
from email.message import EmailMessage
from model.engine import storage
from model.user_info import UserInfo
from model.message_info import MessageInfo
from model.resources_info import ResourcesInfo
from model.group_info import GroupInfo
from model.group_registration_info import GroupRegistrationInfo
from model.audio_file_info import AudioFileInfo
import ssl
import smtplib
from static.system_files.default_email_structures import account_activation, reset_password
import secrets
import os
import jwt
from datetime import datetime, timedelta
import random
from sqlalchemy import desc
import re
from contextlib import contextmanager
from flask_login import current_user

Session = storage.session()

classes_strings = {
    'UserInfo': UserInfo,
    'MessageInfo': MessageInfo,
    'ResourcesInfo': ResourcesInfo,
    'GroupInfo': GroupInfo,
    'AudioFileInfo': AudioFileInfo
}


def send_user_account_activation_mail(user):
    """
    This function helps in sending account activation mail to newly registered users
    :param user:
    :return: None
    """
    email_receiver = user.emailAddress
    email_subject = "Activate Your EchoDAT Account Now"
    email_body = account_activation.generate_email(user.userName, get_user_email_activation_link(user._id))
    send_email(email_receiver, email_subject, email_body)


def send_password_reset_mail(user):
    """
    This function helps in sending password reset mail to users
    :param user:
    :return: None
    """
    email_receiver = user.emailAddress
    email_subject = "Reset you Password with EchoDAT"
    email_body = reset_password.generate_email(user.userName, get_user_password_reset_link(user._id))
    send_email(email_receiver, email_subject, email_body)


def send_email(
        email_receiver,
        email_subject,
        email_body
        ):
    """
    This function serves as the engine that sends EchoDAT email provided the necessary info
    :param email_receiver:
    :param email_subject:
    :param email_body:
    :return:
    """

    email_sender = app.config.get('ECHODAT_GMAIL_ACCOUNT')
    email_password = app.config.get('ECHODAT_GMAIL_PASSWORD')

    email_message = EmailMessage()

    email_message['From'] = email_sender
    email_message['To'] = email_receiver
    email_message['subject'] = email_subject
    email_message.set_content(email_body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(user=email_sender, password=email_password)
        smtp.send_message(email_message)


def get_user_email_activation_link(user_id):
    token = jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=2)}, app.config.get('SECRET_KEY'), algorithm='HS256')

    url = 'http://127.0.0.1:5000/account_activation/' + token
    return url


def get_user_password_reset_link(user_id):
    token = jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(hours=2)}, app.config.get('SECRET_KEY'), algorithm='HS256')

    url = 'http://127.0.0.1:5000/reset_password/' + token
    return url


def gen_state():
    """
    This function help in getting random state value for our
    app session cookie
    :return: generated_state
    """
    generated_state = secrets.token_hex(16).upper()
    return generated_state


@app.template_filter('get_user_avatar_name')
def get_user_avatar_name(user_id):
    """
    This function returns the current user avatar name
    :param user_id
    :return: current_user_avatar_name
    """
    avatar_folder_path = os.path.join(app.root_path, 'static', 'users_profile_avatar')
    files = os.listdir(avatar_folder_path)
    current_user_avatar_name = [name for name in files if user_id in name]
    if current_user_avatar_name:
        current_user_avatar_name = current_user_avatar_name[0]
    else:
        current_user_avatar_name = 'default-avatar.jpeg'
    return current_user_avatar_name


@app.template_filter('get_audio_filename_by_id')
def get_audio_filename_by_id(audio_id):
    """
    This function returns the audio file name using audio id
    :param audio_id
    :return: current_user_avatar_name
    """
    users_audio_folder_path = os.path.join(app.root_path, 'static', 'users_data')
    files = os.listdir(users_audio_folder_path)
    audio_file_name = [name for name in files if audio_id in name]
    if audio_file_name:
        audio_file_name = audio_file_name[0]
    else:
        audio_file_name = 'default-audio.mp3'
    return audio_file_name


def pick_random_google_userName(name):
    with session_scoped() as session:
        name_prefix = random.choice(name.split(' '))
        name = name_prefix + str(secrets.token_hex(2)).lower()
        while session.query(UserInfo).filter_by(userName=name).first():
            name = name_prefix + str(secrets.token_hex(2)).lower()
        return name


def format_message(message=""):
    message = message.replace('<', '&lt').replace('>', '&gt').replace('\n', '<br>')
    if '**' in message:
        message_list = message.split('**', 2)
        if len(message_list) == 3:
            message = ''.join([message_list[0], '<strong>', message_list[1], '</strong>', message_list[2]])

    url_structure = re.compile(r'(^(https?://|www\.|mailto:|ftp://|ssh://|\w+://))|(\.(com|tech)$)')
    chunk_message = message.split()
    prefix_outputs = list(map(re.search, [url_structure]*len(chunk_message), chunk_message))
    message_list = [f'<a href="{token}" target="_blank" class="message_link">{token}</a>' if prefix_outputs[index] else token for index, token in enumerate(chunk_message)]
    message = " ".join(message_list)
    return message


@app.template_filter('is_new_user_message')
def is_new_user_message(message):
    with session_scoped() as session:
        consecutive_message = session.query(MessageInfo).filter_by(projectId=message.projectId).where(MessageInfo.created_at <= message.created_at).order_by(desc(MessageInfo.created_at)).limit(2).all()
        if len(consecutive_message) != 2:
            return True
        if consecutive_message[0].creatorId == consecutive_message[1].creatorId:
            return False
        return True


def get_project_last_message_info(project_id):
    with session_scoped() as session:
        last_message = session.query(MessageInfo).filter_by(projectId=project_id).order_by(desc(MessageInfo.created_at)).first()
        if last_message:
            messanger = session.query(UserInfo).filter_by(_id=last_message.creatorId).first()
            return last_message, messanger
        return None


def get_group_project_resources_name(group_id, project_id, resources_type):
    with session_scoped() as session:
        files_directory_path = os.path.join(app.root_path, 'static/group_project_data', f'{group_id}/{project_id}/{resources_type}')
        os.makedirs(files_directory_path, exist_ok=True)
        file_names = os.listdir(files_directory_path)
        file_objects = session.query(ResourcesInfo).filter_by(groupId=group_id, projectId=project_id, resourcesType=resources_type).order_by(ResourcesInfo.created_at).all()

    output = []
    for file_object in file_objects:
        filename = [filename for filename in file_names if file_object._id in filename][0]
        output.append([filename, file_object])
        file_names.remove(filename)

    return output


def get_group_lyrics_resources(group_id, project_id, filename):
    lyrics_directory_path = os.path.join(app.root_path, f'static/group_project_data/{group_id}/{project_id}/Lyrics')

    with open(os.path.join(lyrics_directory_path, filename), 'r') as f:
        lyrics = f.read()

    return lyrics


def get_object_by_id(object_id, object_class):
    with session_scoped() as session:
        _object = session.query(classes_strings.get(object_class)).filter_by(_id=object_id).first()
        return _object


def del_object_by_id(object_id, object_class):
    with session_scoped() as session:
        _object = session.query(classes_strings.get(object_class)).filter_by(_id=object_id).first()
        if _object:
            session.delete(_object)
            return True
    return False


def get_group_info(group_id):
    group = get_object_by_id(group_id, 'GroupInfo')
    if group:
        with session_scoped() as session:
            info = {
                'members': len(session.query(GroupRegistrationInfo).filter_by(userId=current_user._id, groupId=group_id).all()),
                'audios': len(session.query(ResourcesInfo).filter_by(creatorId=current_user._id, resourcesType='AUDIO').all()),
                'lyrics': len(session.query(ResourcesInfo).filter_by(creatorId=current_user._id, resourcesType='LYRICS').all()),
                'files': len(session.query(ResourcesInfo).filter_by(creatorId=current_user._id, resourcesType='FILE').all())
            }
            return info
    return None


def get_user_groups_id(user_id):
    with session_scoped() as session:
        user_groups_relationships = session.query(GroupRegistrationInfo).filter_by(userId=current_user._id).order_by(
                GroupRegistrationInfo.created_at).all()
        group_ids = [user_groups_relationship.groupId for user_groups_relationship in user_groups_relationships]
        return group_ids



@contextmanager
def session_scoped():
    try:
        yield Session
        try:
            Session.commit()
        except Exception as e:
            app.logger.error(f"Error message: {e}")
    except Exception as e:
        app.logger.error(f"Error working with session with error message: {e}")
        try:
            Session.rollback()
            raise
        except Exception as e:
            app.logger.error(f"Could not session.rollback(): {e}")
            raise
    finally:
        try:
            Session.close()
        except Exception as e:
            app.logger.error(f"Error message: {e}")
