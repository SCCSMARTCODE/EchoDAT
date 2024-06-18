"""
This is the file that will contain the unauthenticated and authentication routes
"""

from flask import Blueprint, render_template


blueP = Blueprint('unauth', __name__, url_prefix='/')


@blueP.route('/')
@blueP.route('/home')
def homepage():
    return render_template('index.html')


@blueP.route('/about')
def about():
    return "Home page"


@blueP.route('/register')
def register():
    return "Home page"


@blueP.route('/login')
def login():
    return "Home page"


@blueP.route('/contact')
def contact():
    return "Home page"
