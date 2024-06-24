"""
This is the module that starts up the application
"""
from config_file import Config
from route1 import blueP
from web_dynamic import app

app.register_blueprint(blueP)
app.config.from_object(Config)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
