from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import Length, DataRequired
from web_dynamic.function_module import session_scoped
from model.user_info import UserInfo
from web_dynamic.route1 import bcrypt


class ChangePwForm(FlaskForm):
    currentPassword = PasswordField("Current Password", validators=[Length(max=60), DataRequired()])
    newPassword = PasswordField("New Password", validators=[Length(min=8, max=60), DataRequired()])
    submit = SubmitField("Change Password")

    def validate(self, extra_validators=None):
        if not super(ChangePwForm, self).validate():
            return False
        with session_scoped() as session:
            user = session.query(UserInfo).filter_by(_id=current_user._id).first()
            if not user.passWord:
                return True
            if not bcrypt.check_password_hash(pw_hash=user.passWord, password=self.currentPassword.data):
                self.currentPassword.errors.append("Invalid password")
                return False
        return True

