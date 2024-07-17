"""
This module will contain the class to manage our login form
"""
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from model.user_info import UserInfo
from web_dynamic import app


class LoginForm(FlaskForm):
    emailAddress = StringField('Email Address', validators=[DataRequired(), Length(max=95), Email()])
    passWord = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=35)])
    rememberMe = BooleanField('Remember Me', default=False)
    submit = SubmitField('Login')

    def validate(self, extra_validators=None):
        from model.engine import storage
        session = storage.session()
        if not super().validate():
            return False

        if self.emailAddress.data == app.config['ECHODAT_REG_ADMIN_MAIL_ACCOUNT'] and self.passWord.data == app.config['ECHODAT_REG_ADMIN_PASSWORD']:
            return True

        if not session.query(UserInfo).filter_by(emailAddress=self.emailAddress.data).first():
            self.emailAddress.errors.append("Invalid Gmail")
            return False
        return True
