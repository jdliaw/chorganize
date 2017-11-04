from routes import *
from database_setup import app, db, User

app.register_blueprint(routes)


@routes.route('/')
def index():
    return "Hello World!"

