from . import routes

@routes.route('/api/group')
def group():
    return "Hello World!"