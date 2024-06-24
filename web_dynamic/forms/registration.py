"""
This module will contain the class to manage our registration form
"""
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo
from model.engine import storage
from model.user_info import UserInfo


class RegistrationForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired(), Length(min=2, max=70)])
    emailAddress = StringField('Email Address', validators=[DataRequired(), Length(max=95), Email()])
    passWord = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=35)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=35), EqualTo('passWord')])
    submit = SubmitField('Register')

    def validate(self, extra_validators=None):
        if not super().validate():
            return False
        session = storage.session()
        if session.query(UserInfo).filter_by(emailAddress=self.emailAddress.data).first():
            self.emailAddress.errors.append("Email Exists")
            return False
        if session.query(UserInfo).filter_by(userName=self.userName.data).first():
            self.userName.errors.append(f"{self.userName.data} has been taken")
            return False

        return True
