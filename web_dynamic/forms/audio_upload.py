"""
This module will contain the class to manage our music upload form
"""
from wtforms import StringField, SelectField, SubmitField, BooleanField, TextAreaField
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Optional
from model.user_info import UserInfo


# class Producer(Form):
#     name = StringField('Producer Name', validators=[Optional()])


class UploadMusic(FlaskForm):

    genres_list = [
        "Alternative", "Disco", "Drum and Bass", "Dubstep", "Electronic", "Folk", "Funk", "Garage", "Ambient", "Blues", "Classical", "Country", "Dance", "Latin Jazz", "Lounge", "Madchester", "Mariachi", "Math Rock", "Medieval", "Merengue",
        "Grime", "Hardcore", "Hip Hop", "House", "Indie", "Jazz", "Latin", "Metal", "New Age", "Opera", "Pop", "Psychedelic", "Punk", "R&B", "Rap", "Reggae", "Merseybeat", "Minimal", "Motown", "Neoclassical", "New Wave", "Nortec", "Nu Metal", "Nu-Disco", "Polka",
        "Rock", "Ska", "Soul", "Techno", "Trance", "Trap", "World Music", "Afrobeat", "Bluegrass", "Boogie Woogie", "Bossa Nova", "Calypso", "Celtic", "Chillwave", "Chiptune", "Christian", "Cumbia", "Dancehall", "Dark Wave", "Disco Polo", "Doo Wop",
        "Downtempo", "Dream Pop", "Drone", "Dub", "Electro Swing", "Emo", "Exotica", "Flamenco", "Folk Rock", "Gospel", "Grunge", "Hard Rock", "Hardcore Punk", "Heavy Metal", "Hi-NRG",
        "House Music", "IDM (Intelligent Dance Music)", "Industrial", "Italo Disco", "J-Pop", "K-Pop", "Krautrock",
        "Post Punk", "Post Rock", "Progressive Rock", "Psytrance", "Ragga", "Ragtime", "Rock and Roll", "Salsa", "Samba", "Shoegaze", "Soca", "Soft Rock", "Synthwave", "Tango", "Trip Hop", "Tropical House", "Vaporwave", "Zydeco"
    ]

    moods = [
        "Happy", "Sad", "Energetic", "Relaxed", "Romantic", "Melancholic", "Angry", "Hopeful", "Peaceful", "Excited", "Nostalgic", "Uplifting", "Calm", "Reflective", "Gloomy", "Passionate", "Motivational", "Chill", "Mysterious", "Aggressive",
        "Joyful", "Somber", "Confident", "Euphoric", "Tense", "Dreamy", "Playful", "Triumphant", "Bittersweet", "Dark", "Cheerful", "Spiritual", "Serene", "Inspiring", "Tender", "Grateful", "Yearning", "Bold", "Optimistic"
    ]

    file = FileField('Upload Audio File', validators=[
        FileRequired(),
        FileAllowed(['mp3', 'wav', 'aac', 'flac', 'ogg', 'wma', 'aiff', 'alac'], 'Audio files only!')
    ])

    artist = StringField('Artist', validators=[DataRequired(), Length(max=100)])
    title = StringField('Song Title', validators=[DataRequired(), Length(max=100)])
    featuring = StringField('Featuring (Separate names using commas)', validators=[DataRequired(), Length(max=100)])
    producers = StringField("Producers' Name (Separate names using commas)", validators=[Optional()])
    genre = SelectField(u'Genre', choices=sorted(genres_list), validators=[DataRequired()])
    mood = SelectField(u'Mood', choices=sorted(moods), validators=[DataRequired()])
    caption = TextAreaField("Caption", validators=[Optional(), Length(max=900)])
    release = BooleanField("Release to Public", validators=[Optional()])
    coverPicture = FileField('Cover Picture', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], "Image Extension not Allowed choose of 'jpeg', 'jpg', 'png'")
    ])
    upload = SubmitField('Upload')
