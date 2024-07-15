from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import Length, DataRequired, Optional
from web_dynamic.function_module import session_scoped
from model.user_info import UserInfo
from sqlalchemy import func


class UserBasicInfoForm(FlaskForm):
    userName = StringField("UserName", validators=[Length(max=70), DataRequired()])
    homeTown = StringField("HomeTown", validators=[Length(max=150), Optional()])
    location = StringField("Location", validators=[Length(max=500), Optional()])
    websiteUrl = StringField("Website Url", validators=[Length(max=350), Optional()])
    shortBiography = TextAreaField("Short Biography", validators=[Length(max=45000), Optional()])
    submit = SubmitField("Save")

    def validate(self, extra_validators=None):
        if not super(UserBasicInfoForm, self).validate():
            return False
        with session_scoped() as session:
            user = session.query(UserInfo).filter(func.lower(UserInfo.userName) == self.userName.data.lower()).first()
            if user:
                if user._id != current_user._id:
                    self.userName.errors.append(f"Sorry {self.userName.data} is no more available")
                    return False
        return True

