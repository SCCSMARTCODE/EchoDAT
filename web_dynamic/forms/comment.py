"""
This module will contain the class to manage our comment form
"""
from wtforms import SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment Message', validators=[DataRequired(), Length(max=9000)])
    submit = SubmitField('Comment')
