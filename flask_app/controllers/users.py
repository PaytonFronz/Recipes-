from sre_constants import SUCCESS
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import render_template, request, session, redirect, flash
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/users/registration', methods=['POST'])
def register_user():
    
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])

        data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
        }
    
        User.create_user(data)
        flash('you are registered!')

    return redirect('/')

@app.route('/users/login', methods = ['POST'])
def login_user():
    
    users = User.get_user_by_info(request.form)

    if len(users) != 1:
            flash('No valid user account found!')
            return redirect('/')
    
    user = users[0]
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password is incorrect!')
        return redirect('/')
    
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Login to view this page!')
        return redirect('/')

    recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', recipes = recipes)

@app.route('/users/logout')
def logout():
    session.clear()
    flash('You are now logged out!')

    return redirect('/')

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        flash('Please log in to view this page.')
        return redirect('/')
    return render_template('create.html')


@app.route('/recipes/create', methods =['POST'])
def create_recipe():

    if 'user_id' not in session:
        flash('Login to view this page!')
        return redirect('/')

    if Recipe.recipe_validation(request.form):
        data = {
            'name': request.form['name'],
            'under_30_mins': request.form['under_30_mins'],
            'instructions': request.form['instructions'],
            'description': request.form['description'],
            'date': request.form['date'],
            'user_id': session['user_id']
        }
        Recipe.create_recipe(data)
        return redirect('/dashboard')

    return redirect('/recipes/new')

@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):

    recipe = Recipe.get_recipe_by_id({'id':recipe_id})

    if 'user_id' not in session:
        flash('Login to view this page!')
        return redirect('/')

    
    return render_template('single_recipe.html', recipe = recipe)


@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):

    recipe = Recipe.get_recipe_by_id({'id': recipe_id})

    if recipe.user.id != session['user_id']:
        return redirect('/')

    return render_template('edit.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/edited', methods = ['POST'])
def edited_recipe(recipe_id):

    recipe = Recipe.get_recipe_by_id({'id':recipe_id})

    data = {
            'id': recipe_id,
            'name': request.form['name'],
            'under_30_mins': request.form['under_30_mins'],
            'instructions': request.form['instructions'],
            'description': request.form['description'],
            'date': request.form['date'],
        }
    
    Recipe.edit_recipe(data)

    return redirect(f'/recipes/{recipe.id}')

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    recipe = Recipe.get_recipe_by_id({'id':recipe_id})

    Recipe.delete_recipe({'id':recipe_id})
    return redirect('/')
