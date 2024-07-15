"""
This module will contain the class to manage our group project creation form
"""
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from flask_login import current_user
from model.project_info import ProjectInfo
from web_dynamic.function_module import session_scoped


class CreateProjectForm(FlaskForm):
    name = StringField('Project Name:', validators=[DataRequired(), Length(max=95)])
    description = TextAreaField('Project Description:', validators=[DataRequired(), Length(max=5000)])
    groupId = StringField('Group Id', validators=[DataRequired()])
    create = SubmitField('Create Project')

    def validate(self, extra_validators=None):
        if not super(CreateProjectForm, self).validate():
            return False
        with session_scoped() as session:
            project = session.query(ProjectInfo).filter_by(groupId=self.groupId.data.strip(), name=self.name.data.strip()).first()
            if project:
                self.name.errors.append(f"{self.name.data} already Exist in the group")
                return False
        return True

