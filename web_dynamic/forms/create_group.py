"""
This module will contain the class to manage our user group creation form
"""
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class CreateGroupForm(FlaskForm):
    name = StringField('Group Name:', validators=[DataRequired(), Length(max=95)])
    description = TextAreaField('Group Description:', validators=[DataRequired(), Length(max=5000)])
    create = SubmitField('Create Group')
