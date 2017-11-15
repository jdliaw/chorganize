from flask import Flask
from database_setup import createApp
from routes import *

#app = Flask(__name__)
"""
def initApp(testing):
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_sqlite.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    print("blah this excecutes")
    return app"""
    
#app.register_blueprint(routes)

if __name__ == '__main__':
    app = createApp(True)
    app.register_blueprint(routes)
    #app.app_context().push()
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'not_secret_at_all'
    app.run(host='0.0.0.0', port=8080)
