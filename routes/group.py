from . import routes

@routes.route('/api/group')
def index():
    return "Hello World!"