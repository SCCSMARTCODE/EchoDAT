"""
This is the module that starts up the application
"""
from flask import Flask
from route1 import blueP

app = Flask('__name__')
app.register_blueprint(blueP)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
