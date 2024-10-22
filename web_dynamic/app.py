"""
This is the module that starts up the application
"""
from config_file import Config
from web_dynamic import app
app.config.from_object(Config)
from route1 import blueP
from route2 import blueP1
from route3 import blueP2
from route4 import blueP3


app.register_blueprint(blueP)
app.register_blueprint(blueP1)
app.register_blueprint(blueP2)
app.register_blueprint(blueP3)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


"""
Please work on login required for comment
"""
