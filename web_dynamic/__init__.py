from flask import Flask
from flask_session import Session

app = Flask('EchoDAT')
# app.config['SECRET_KEY'] = "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"


# Session configuration
# app.config['SESSION_TYPE'] = 'filesystem'  # Using filesystem for session storage
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_FILE_DIR'] = './flask_session/'
# app.config['SESSION_FILE_THRESHOLD'] = 100
#
# # Initialize session
# Session(app)
