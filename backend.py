from database_setup import createApp
from routes import *
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        app = createApp(False)
    else:
        app = createApp(True)
    app.register_blueprint(routes)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'not_secret_at_all'
    app.run(host='0.0.0.0', port=8080)
