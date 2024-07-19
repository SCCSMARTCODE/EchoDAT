"""
This is the file that will contain the group routes
"""

from flask import Blueprint, redirect, url_for, render_template, flash, request, abort, jsonify
from flask_login import login_required, current_user
from model.project_info import ProjectInfo
from forms.create_project import CreateProjectForm
from forms.project_chat import ProjectChatForm
from forms.group_resources_upload import LyricsResourcesUpload, AudioResourcesUpload, FilesResourcesUpload
from function_module import *
from web_dynamic import app
from forms.create_group import CreateGroupForm
from werkzeug.utils import secure_filename
import os
from sqlalchemy import func
from sqlalchemy.orm import joinedload

blueP2 = Blueprint('group', __name__, url_prefix='/')


@blueP2.route('/groups')
@login_required
def user_group_management():
    try:
        with session_scoped() as session:
            current_user_avatar_name = get_user_avatar_name(current_user.get_id())
            groups = session.query(GroupRegistrationInfo).filter_by(userId=current_user.get_id()).all()
            return render_template('user_group_management.html', avatar_name=current_user_avatar_name, groups=groups)
    except Exception as e:
        app.logger.error(f"error reaching {user_group_management.__name__} with error message: {e}")
        return render_template('error_page.html', message='An error occurred. Please try again later.', title="Manage Group")


@blueP2.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    try:
        with session_scoped() as session:
            form = CreateGroupForm()
            current_user_avatar_name = get_user_avatar_name(current_user.get_id())

            if request.method == 'POST':
                try:
                    if form.validate_on_submit():
                        new_group = GroupInfo(
                            name=form.name.data,
                            description=form.description.data,
                            creatorId=current_user.get_id()
                        )
                        session.add(new_group)
                        session.commit()

                        new_group_registration = GroupRegistrationInfo(
                            userId=current_user.get_id(),
                            groupId=new_group.get_id()
                        )
                        session.add(new_group_registration)
                        session.commit()

                        flash(f'{new_group.name} Creation Successful', 'success')
                        return redirect(url_for('group.user_group_management'))

                except Exception as e:
                    app.logger.error(f"Error occurred during group creation: {e}")
                    flash('An error occurred while processing your request. Please try again later.', 'danger')
                    return redirect(url_for('group.user_group_management'))

            return render_template('create_group.html', avatar_name=current_user_avatar_name, form=form, title="Create Group")

    except Exception as e:
        app.logger.error(f"Error occurred in create_group route: {e}")
        flash('An error occurred. Please try again later.', 'danger')
        return render_template('error_page.html', message='An error occurred. Please try again later.', title="error")


@blueP2.route('/group_workspace/<group_id>', methods=['GET'])
@login_required
def group_workspace(group_id):
    try:
        with session_scoped() as session:
            current_user_avatar_name = get_user_avatar_name(current_user.get_id())
            group = session.query(GroupInfo).filter_by(_id=group_id).first()

            if not group:
                abort(404)

            if not session.query(GroupRegistrationInfo).filter_by(userId=current_user.get_id(), groupId=group_id).first():
                flash('Sorry, you are not an authorized member of this group', 'danger')
                return redirect(url_for('group.user_group_management'))

            projects = session.query(ProjectInfo).filter_by(groupId=group_id).all()

            return render_template('group_workspace.html',
                                   avatar_name=current_user_avatar_name,
                                   group=group,
                                   projects=projects,
                                   get_object_by_id=get_object_by_id,
                                   get_project_last_message_info=get_project_last_message_info,
                                   title="Group Workspace"
                                   )

    except Exception as e:
        app.logger.error(f"Error occurred in group_workspace route: {e}")
        flash('An error occurred. Please try again later.', 'danger')
        return render_template('error_page.html', message='An error occurred. Please try again later.', title="error")


@blueP2.route('/group_workspace/<group_id>/project/<project_id>', methods=['GET'])
@login_required
def project_page(project_id, group_id):
    try:
        with session_scoped() as session:
            current_user_avatar_name = get_user_avatar_name(current_user.get_id())
            projects = session.query(ProjectInfo).filter_by(groupId=group_id).all()
            project = session.query(ProjectInfo).filter_by(_id=project_id).first()

            if not project:
                abort(404, description="Project not found")

            group = session.query(GroupInfo).filter_by(_id=group_id).first()
            if not group:
                abort(404, description="Group not found")

            form = ProjectChatForm()

            return render_template('group_project_workspace.html',
                                   avatar_name=current_user_avatar_name,
                                   group=group,
                                   project=project,
                                   projects=projects,
                                   form=form,
                                   get_project_last_message_info=get_project_last_message_info,
                                   title="Project Page")
    except Exception as e:
        app.logger.error(f"Error occurred in project_page route: {e}")
        return render_template('error_page.html', message='An error occurred. Please try again later.')


@blueP2.route('/group_workspace/project/<project_id>/messages', methods=['GET'])
@login_required
def get_messages(project_id):
    try:
        with session_scoped() as session:
            messages = session.query(MessageInfo).options(joinedload(MessageInfo.creator)).filter_by(projectId=project_id).order_by(MessageInfo.created_at).all()
            app.logger.debug(f"Fetched messages: {messages}")
            message_list = []
            for message in messages:
                try:
                    message_list.append({
                        'creatorId': message.creatorId,
                        'creatorName': message.creator.userName,
                        'creatorAvatar': get_user_avatar_name(message.creatorId),
                        'message': message.message,
                        'created_at': message.created_at.isoformat()
                    })
                except AttributeError as ae:
                    app.logger.error(f"Attribute error with message object: {message} - {ae}")
        return jsonify(message_list)
    except Exception as e:
        app.logger.error(f"Error fetching messages for project {project_id}: {e}")
        return jsonify({"error": "An error occurred while fetching messages."}), 500


@blueP2.route('/group_workspace/project/<project_id>/messages', methods=['POST'])
@login_required
def send_message(project_id):
    try:
        with session_scoped() as session:
            form = ProjectChatForm()
            if form.validate_on_submit():
                project = session.query(ProjectInfo).filter_by(_id=project_id).first()
                if not project:
                    return jsonify({'success': False, 'error': 'Project not found'}), 404

                group = session.query(GroupInfo).filter_by(_id=project.group.get_id()).first()
                if not group:
                    return jsonify({'success': False, 'error': 'Group not found'}), 404

                new_message = MessageInfo(
                    creatorId=current_user.get_id(),
                    groupId=group.get_id(),
                    projectId=project.get_id(),
                    message=format_message(form.comment_field.data)
                )
                session.add(new_message)
                session.commit()
                return jsonify({'success': True}), 200

            return jsonify({'success': False, 'error': 'Form validation failed'}), 400
    except Exception as e:
        app.logger.error(f"Error adding new message: {e}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500


@blueP2.route('/group_workspace/create_project/<group_id>', methods=['GET', 'POST'])
@login_required
def create_project(group_id):
    try:
        with session_scoped() as session:
            current_user_avatar_name = get_user_avatar_name(current_user.get_id())
            group = session.query(GroupInfo).filter_by(_id=group_id).first()

            if not group:
                abort(404)

            projects = session.query(ProjectInfo).filter_by(groupId=group_id).all()
            form = CreateProjectForm()

            if request.method == 'POST' and form.validate_on_submit():
                try:
                    new_project = ProjectInfo(
                        name=form.name.data.strip(),
                        description=form.description.data.strip(),
                        creatorId=current_user.get_id(),
                        groupId=group_id
                    )
                    session.add(new_project)
                    group.totalProjectCount = group.totalProjectCount + 1
                    project_id = new_project.get_id()
                    session.commit()
                    return redirect(url_for('group.project_page', group_id=group_id, project_id=project_id))

                except Exception as e:
                    app.logger.error(f"Error occurred during project creation: {e}")
                    flash('An error occurred while processing your request. Please try again later.', 'danger')

            return render_template('group_create_project.html',
                                   avatar_name=current_user_avatar_name,
                                   group=group,
                                   form=form,
                                   projects=projects,
                                   get_user_avatar_name=get_user_avatar_name,
                                   get_project_last_message_info=get_project_last_message_info,
                                   title="Create Project"
                                   )

    except Exception as e:
        app.logger.error(f"Error occurred in create_project route: {e}")
        flash('An error occurred. Please try again later.', 'danger')

    return render_template('error_page.html', message='An error occurred. Please try again later.')


@blueP2.route('/search_member/<group_id>', methods=['GET', 'POST'])
@login_required
def search_member(group_id):
    try:
        with session_scoped() as session:
            group = session.query(GroupInfo).filter_by(_id=group_id).first()
            projects = session.query(ProjectInfo).filter_by(groupId=group_id).all()

            search_term = request.args.get('username', '')
            if search_term:
                pattern = f"%{search_term}%"
                users = session.query(UserInfo).filter(func.lower(UserInfo.userName).ilike(pattern.lower())).all()
                inactive_users = [user for user in users if not session.query(GroupRegistrationInfo).filter_by(userId=user.get_id(), groupId=group_id).first()]
                active_users = [user for user in users if session.query(GroupRegistrationInfo).filter_by(userId=user.get_id(), groupId=group_id).first()]
            else:
                active_users = inactive_users = []

            return render_template('group_add_member.html',
                                   group=group,
                                   projects=projects,
                                   results=inactive_users,
                                   active_users=active_users,
                                   get_user_avatar_name=get_user_avatar_name,
                                   get_project_last_message_info=get_project_last_message_info,
                                   title="Search Members")

    except Exception as e:
        app.logger.error(f"Error occurred in search_member route: {e}")
        flash('An error occurred. Please try again later.', 'danger')

    return render_template('error_page.html', message='An error occurred. Please try again later.')


@blueP2.route('/add_member/<group_id>', methods=['GET'])
@login_required
def add_member(group_id):
    try:
        with session_scoped() as session:
            member_id = request.args.get('member_id')

            if not session.query(UserInfo).filter_by(_id=member_id).first():
                abort(404)

            new_group_member = GroupRegistrationInfo(
                userId=member_id,
                groupId=group_id
            )
            session.add(new_group_member)

            group = session.query(GroupInfo).filter_by(_id=group_id).first()
            if group:
                group.amountOfMembers += 1
                session.commit()
                return redirect(url_for('group.group_workspace', group_id=group_id))

    except Exception as e:
        app.logger.error(f"Error occurred in add_member route: {e}")
        flash('An error occurred. Please try again later.', 'danger')

    return render_template('error_page.html', message='An error occurred. Please try again later.', title="Add Member")


@blueP2.route('/remove_member/<group_id>', methods=['GET'])
@login_required
def remove_member(group_id):
    try:
        with session_scoped() as session:
            member_id = request.args.get('member_id')

            if not session.query(UserInfo).filter_by(_id=member_id).first():
                abort(404)

            existing_group_member = session.query(GroupRegistrationInfo).filter_by(groupId=group_id, userId=member_id).first()

            if existing_group_member:
                session.delete(existing_group_member)

                group = session.query(GroupInfo).filter_by(_id=group_id).first()
                if group:
                    group.amountOfMembers -= 1
                    session.commit()

            return redirect(url_for('group.group_workspace', group_id=group_id))

    except Exception as e:
        app.logger.error(f"Error occurred in remove_member route: {e}")
        flash('An error occurred. Please try again later.', 'danger')

    return render_template('error_page.html', message='An error occurred. Please try again later.')


@blueP2.route('/project_resources/<group_id>', methods=['GET', 'POST'])
@login_required
def project_resources(group_id):
    try:
        with session_scoped() as session:
            project_id = request.args.get('project_id')
            audio_form = AudioResourcesUpload()
            lyrics_form = LyricsResourcesUpload()
            file_form = FilesResourcesUpload()

            if request.method == 'POST':
                form_tuple = None
                if audio_form.validate_on_submit():
                    form_tuple = ('AUDIO', audio_form)
                elif lyrics_form.validate_on_submit():
                    form_tuple = ('LYRICS', lyrics_form)
                elif file_form.validate_on_submit():
                    form_tuple = ('FILE', file_form)
                if form_tuple:
                    form_type, form = form_tuple
                    new_resources = ResourcesInfo(
                        title=form.title.data,
                        caption=form.description.data,
                        resourcesType=form_type,
                        creatorId=current_user.get_id(),
                        groupId=group_id,
                        projectId=project_id
                    )
                    file = None
                    if form_type == 'AUDIO':
                        file = form.audio_file.data
                    elif form_type == 'FILE':
                        file = form.random_file.data
                    elif form_type == 'LYRICS':
                        file = form.lyrics.data

                    saving_path = os.path.join(app.root_path, f'static/group_project_data/{group_id}/{project_id}/{form_type}')
                    os.makedirs(saving_path, exist_ok=True)

                    if form_type in ['AUDIO', 'FILE']:
                        file_ext = secure_filename(file.filename).split('.')[-1]
                        if file_ext:
                            file.save(os.path.join(saving_path, f'{new_resources.get_id()}.{file_ext}'))
                    else:
                        with open(os.path.join(saving_path, f'{new_resources.get_id()}.txt'), 'w') as f:
                            f.write(format_message(file))
                    session.add(new_resources)
                    session.commit()
                    return redirect(request.url)
                else:
                    flash('Failed to validate form. Please check your input and try again.', 'danger')

            group = session.query(GroupInfo).filter_by(_id=group_id).first()
            projects = session.query(ProjectInfo).filter_by(groupId=group_id).all()
            project = [proj for proj in projects if proj.get_id() == project_id]

            return render_template('group_project_resources.html',
                                   project=project[0],
                                   group=group,
                                   projects=projects,
                                   audio_form=audio_form,
                                   file_form=file_form,
                                   lyrics_form=lyrics_form,
                                   get_user_avatar_name=get_user_avatar_name,
                                   get_project_last_message_info=get_project_last_message_info,
                                   get_group_project_resources_name=get_group_project_resources_name,
                                   get_group_lyrics_resources=get_group_lyrics_resources,
                                   title="Project Resources"
                                   )

    except Exception as e:
        app.logger.error(f"Error occurred in project_resources route: {e}")
        flash('An error occurred. Please try again later.', 'danger')

    return render_template('error_page.html', message='An error occurred. Please try again later.')


@blueP2.route('/delete_resources/<group_id>/<project_id>/<resource_id>')
@login_required
def delete_resources(group_id, project_id, resource_id):
    try:
        with session_scoped() as session:
            filename = request.args.get('filename')
            resource_type = request.args.get('resource_type')
            resource_path = os.path.join(app.root_path, f'static/group_project_data/{group_id}/{project_id}/{resource_type}/{filename}')

            resource = session.query(ResourcesInfo).filter_by(_id=resource_id).first()
            if not resource:
                flash('Resource not found.', 'danger')
                return redirect(url_for('group.project_resources', group_id=group_id, project_id=project_id))

            session.delete(resource)
            session.commit()

            if os.path.exists(resource_path):
                os.remove(resource_path)
                flash('Resource deleted successfully.', 'success')
            else:
                flash('Resource file not found.', 'danger')

    except Exception as e:
        app.logger.error(f"Error occurred in delete_resources route: {e}")
        flash('An error occurred. Please try again later.', 'danger')

    return redirect(url_for('group.project_resources', group_id=group_id, project_id=project_id))
