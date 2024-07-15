"""
This module will contain the class to manage our email verification form
"""
from wtforms import SubmitField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email


class EmailVerificationForm(FlaskForm):
    emailAddress = StringField('Email', validators=[DataRequired(), Length(max=95), Email()])
    verify = SubmitField('Verify')
