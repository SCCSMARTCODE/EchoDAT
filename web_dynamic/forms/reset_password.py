"""
This module will contain the class to manage our reset password form
"""
from wtforms import PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo


class PasswordResetForm(FlaskForm):
    newPassword = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=35)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=35), EqualTo('newPassword')])
    reset = SubmitField('Reset')
