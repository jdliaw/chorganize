from database_setup import app
from routes import *

app.register_blueprint(routes)

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'not_secret_at_all'
    app.run(host='0.0.0.0', port=8080)
