from flask import Flask
from database_setup import createApp
from routes import *
import sys

global app

if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) == 1:
        app = createApp(False)
    else:
        app = createApp(True)
    app.register_blueprint(routes)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'not_secret_at_all'
    app.run(host='0.0.0.0', port=8080)
