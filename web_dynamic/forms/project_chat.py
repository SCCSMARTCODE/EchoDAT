"""
This module will contain the class to manage our project chat form
"""
from wtforms import SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class ProjectChatForm(FlaskForm):
    comment_field = TextAreaField('Comment Message', validators=[DataRequired(), Length(max=9000)])
    submit = SubmitField('Send')
