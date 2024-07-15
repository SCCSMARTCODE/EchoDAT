from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired
from web_dynamic.function_module import session_scoped
from model.user_info import UserInfo
from sqlalchemy import func


class UpdateEmailForm(FlaskForm):
    currentEmail = StringField("Current Email", validators=[Length(max=60), DataRequired()])
    newEmail = StringField("New Email", validators=[Length(max=60), DataRequired()])
    submit = SubmitField("Update Email")

    def validate(self, extra_validators=None):
        if not super(UpdateEmailForm, self).validate():
            return False
        with session_scoped() as session:
            user = session.query(UserInfo).filter_by(emailAddress=self.currentEmail.data.lower()).first()
            if user:
                if user._id != current_user._id:
                    self.currentEmail.errors.append(f"Invalid Request")
                    return False

            user = session.query(UserInfo).filter_by(emailAddress=self.newEmail.data.lower()).first()
            if user:
                if user._id != current_user._id:
                    self.newEmail.errors.append(f"Sorry {self.newEmail.data} is no more available")
                    return False
        return True

