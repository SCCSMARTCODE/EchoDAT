"""
This will be a module that handles group resources upload
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, InputRequired
from flask_wtf.file import FileRequired, FileField, FileSize, FileAllowed


class AudioResourcesUpload(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=70)])
    description = TextAreaField('Resource description', validators=[Optional(), Length(max=1500)])
    audio_file = FileField('Choose Audio', validators=[FileRequired(),
                                                       FileSize(max_size=16*1000*1000),
                                                       FileAllowed(['mp3', 'wav', 'aac', 'flac', 'ogg', 'wma', 'aiff', 'alac'], 'Audio files only!')
                                                       ])
    upload = SubmitField('Upload')


class LyricsResourcesUpload(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=70)])
    description = TextAreaField('Resource description', validators=[Optional(), Length(max=1500)])
    lyrics = TextAreaField('Input lyrics', validators=[DataRequired(), ])
    upload = SubmitField('Upload')


class FilesResourcesUpload(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=70)])
    description = TextAreaField('Resource description', validators=[Optional(), Length(max=1500)])
    random_file = FileField('Choose File', validators=[FileRequired(),
                                                       FileSize(max_size=20*1000*1000),
                                                       FileAllowed(['mp3', 'wav', 'aac', 'flac', 'ogg', 'wma', 'aiff', 'alac', 'pdf', 'txt', 'mp3', 'gif'], 'File type not supported!')
                                                       ])
    upload = SubmitField('Upload')
