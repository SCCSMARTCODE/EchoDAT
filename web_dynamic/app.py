"""
This is the module that starts up the application
"""
from flask import Flask

app = Flask('__name__')


@app.route('/')
@app.route('/home')
def home_page():
    return "Hello World!<br>Welcome to <b>EchoDAT</b>"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
