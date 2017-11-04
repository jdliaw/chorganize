
from sqlalchemy.orm.exc import NoResultFound
from database_setup import app, db, User
from routes import *
from flask import Flask, request


app.register_blueprint(routes)
"""
@app.route("/")
def hello():
    return "Hello World!"



@app.route('/')
@app.route('/catalog/')
def homepage():
    return jsonify(
        email = "shit"
    )
"""
"""
    categories = Category.query.order_by(Category.name)
    user_id = login_session.get('user_id')
    name = login_session.get('name')
    return render_template(
                          'latest_items.html',
                          user_id=user_id,
                          name=name,
                          categories=categories
                          )
"""

"""
# Create an anti-forgery state token
# Store it in the session for later validation.
@app.route('/login')
def show_login():
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        error = "Invalid state parameter."
        return error, 401

    auth_code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        credentials = credentials_from_clientsecrets_and_code(
            'client_secret.json',
            'openid profile',
            auth_code)
    except FlowExchangeError:
        error = "Failed to exchange authorization code for access token."
        return error, 401

    access_token = credentials.access_token
    payload = {'access_token': access_token}
    url_token_validation = "https://www.googleapis.com/oauth2/v3/tokeninfo"
    result = requests.get(url_token_validation, params=payload)
    result = result.json()

    if result.get('error'):
        return result.get('error'), 500

    # Verify that the access token is used for the intended user.
    user_id = credentials.id_token['sub']
    if result['sub'] != user_id:
        error = "Token's user ID doesn't match given user ID."
        return error, 401

    # Verify that the access token is valid for this app.
    if result['aud'] != CLIENT_ID:
        error = "Token's client ID does not match app's."
        return error, 401

    # Verify that the acess token does not expire.
    if int(result['expires_in']) < 1:
        error = "Token has already expired."
        return error, 401

    stored_credentials = login_session.get('access_token')
    stored_userid = login_session.get('user_id')
    if stored_credentials is not None and user_id == stored_userid:
        output = "<h1>You have already logged in.</h1>"
        return output

    url_userinfo = "https://www.googleapis.com/oauth2/v1/userinfo"
    payload = {'access_token': access_token, 'alt': 'json'}
    result = requests.get(url_userinfo, params=payload)
    result = result.json()

    # Store the user information including access token for later use
    login_session['access_token'] = access_token
    login_session['user_id'] = user_id
    login_session['name'] = result['name']
    login_session['picture'] = result['picture']

    # Add the user to the database if not being present before
    user_id, name = login_session['user_id'], login_session['name']
    try:
        user = User.query.filter_by(id=user_id).one()
    except NoResultFound:
        user = User(id=user_id, name=name)
        db.session.add(user)
        db.session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += login_session['name']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['name'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        error = "You haven't logged in yet."
        return render_template('prompt.html', prompt=error), 401

    url_revoke_token = "https://accounts.google.com/o/oauth2/revoke"
    payload = {'token': access_token}
    result = requests.get(url_revoke_token, params=payload)

    # Clear out the user information from the session
    del login_session['access_token']
    del login_session['user_id']
    del login_session['name']
    del login_session['picture']

    message = "You have successfully logged out."
    return render_template('prompt.html', prompt=message)


@app.route('/catalog/<string:category_name>/items/')
def items_of_category(category_name):
    categories = Category.query.order_by(Category.name)
    category = Category.query.filter_by(name=category_name).one()
    return render_template(
                          'items_of_category.html',
                          categories=categories,
                          category=category
                          )


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def show_item(category_name, item_name):
    item = Item.query.filter_by(name=item_name).one()
    return render_template('show_item.html', item=item)


@app.route('/catalog/add/', methods=['GET', 'POST'])
@login_required
def add_item():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        category_name = form.category.data
        try:
            item = Item.query.filter_by(name=name).one()
            flash("The item already exists.")
            return render_template(
                                  'add_or_edit_item.html',
                                  add=True,
                                  form=form
                                  )
        except NoResultFound:
            category = Category.query.\
                               filter_by(name=category_name).\
                               one()
            user = User.query.filter_by(id=login_session['user_id']).one()
            new_item = Item(name=name, description=description,
                            category=category, user=user)
            db.session.add(new_item)
            db.session.commit()
            flash("The new item was successfully added.")
            return redirect(url_for('homepage'))

    if request.method == "POST":
        if not (form.name.data and form.description.data):
            flash("You have to fill name and description about the item.")
        else:
            flash("Name is only allowed to have letters and spaces.")

    return render_template('add_or_edit_item.html', add=True, form=form)


@app.route('/catalog/<string:item_name>/edit/', methods=['GET', 'POST'])
@login_required
def edit_item(item_name):
    form = MyForm()
    item = Item.query.filter_by(name=item_name).one()
    user_id = login_session['user_id']
    if item.user_id != user_id:
        error = "You don't have the permission to do so."
        url = url_for(
                     'show_item',
                     category_name=item.category.name,
                     item_name=item.name
                     )
        return render_template('prompt.html', prompt=error, url=url), 401

    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.category_name = form.category.data
        db.session.add(item)
        db.session.commit()
        flash("The item was successfully edited.")
        return redirect(url_for('homepage'))

    if request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.category.data = item.category.name
    else:
        if not (form.name.data and form.description.data):
            flash("You have to fill name and description about the item.")
        else:
            flash("Name is only allowed to have letters and spaces.")

    return render_template('add_or_edit_item.html', item=item, form=form)


@app.route('/catalog/<string:item_name>/delete/', methods=['GET', 'POST'])
@login_required
def delete_item(item_name):
    item = Item.query.filter_by(name=item_name).one()
    user_id = login_session['user_id']
    if item.user_id != user_id:
        error = "You don't have the permission to do so."
        url = url_for(
                     'show_item',
                     category_name=item.category.name,
                     item_name=item.name
                     )
        return render_template('prompt.html', prompt=error, url=url), 401

    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash("The item was successfully deleted.")
        return redirect(url_for('homepage'))
    else:
        return render_template('delete.html', item=item)


@app.route('/catalog/<string:item_name>/json/')
def json_endpoint(item_name):
    item = Item.query.filter_by(name=item_name).one()
    return jsonify(Item=item.serialize)
"""
if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'not_secret_at_all'
    app.run(host='0.0.0.0', port=8080)
