from flask import (Flask, render_template, request, flash, session, jsonify,
                   redirect, url_for)
import datetime
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud
import re
from crud import create_user
from spoonacularsearch import get_recipe_ingredients, find_recipes_by_calories, get_recipe_steps
from dateutil.relativedelta import relativedelta
from functools import wraps
import os


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def landing_page():
    """View landing page."""
    return render_template('landing_page.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/home/user/<int:user_id>')
@login_required
def homepage(user_id):
    """View personalized Home"""
    user = crud.get_user_by_id(user_id)
    if user:
        weight_notes = crud.get_user_weight_notes(user_id)
        favorite_recipes = crud.get_favorites_by_user(user_id)
        tdee_goal = crud.get_latest_tdee_goal(user_id)
        
        if tdee_goal is not None:
            tdee, goal = tdee_goal
        else:
            tdee, goal = None, None
        
    else:
        weight_notes = None
        favorite_recipes = None
        tdee = None
        goal = None

    return render_template('homepage.html', user=user, weight_notes=weight_notes, favorite_recipes=favorite_recipes, tdee=tdee, goal=goal)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = crud.get_user_by_username(username)

        if user:
            stored_password = user.password
            if password == stored_password:
                session['user_id'] = user.id
                flash('Login successful!')
                return redirect('/')
        
        flash('Invalid username or password. Please try again.')
        return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout the user"""
    session.pop('user_id', None)
    session.clear()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        email = request.form.get("email")
        created_at = datetime.datetime.now()

        if len(username) < 7:
            return jsonify({'message': 'Username must be at least 7 characters long!'})
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return jsonify({'message': 'Password must contain at least one special character!'})
        elif len(password) < 9:
            return jsonify({'message': 'Password must be at least 9 characters long!'})
        # Validate age (13 years or older)
        dob = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        age = relativedelta(datetime.date.today(), dob).years
        if age < 13:
            return jsonify({'message': 'You must be 13 years or older to register!'})
        elif crud.get_user_by_email(email):
            return jsonify({'message': 'User with this email already exists!'})
        elif crud.get_user_by_username(username):
            return jsonify({'message': 'User with this username already exists!'})
        else:
            user = crud.create_user(username, password, first_name, last_name, date_of_birth, email, created_at)
            db.session.add(user)
            db.session.commit()
            return jsonify({'redirect': '/login'})

    return render_template('register.html')

@app.route('/weight_notes', methods=['GET','POST'])
def weight_notes():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        workouts_done = request.form.get('workouts_done')
        weight_value = request.form.get('weight_value')
        date = request.form.get('date')

        weight_notes = crud.WeightNotes(user_id=user_id, workouts_done=workouts_done, weight_value=weight_value, date=date)

        db.session.add(weight_notes)
        db.session.commit()

        return redirect(url_for('weight_notes'))

    user_id = session.get('user_id')
    if user_id:
        user = crud.User.query.get(user_id)
        if user:
            weight_notes = user.weight_notes
        else:
            flash('User not found in the database.')
            return redirect(url_for('login'))
    else:
        flash('User ID not found in the session.')
        return redirect(url_for('login'))

    return render_template('weight_notes.html', weight_notes=weight_notes, user_id=user_id)

@app.route('/weight_and_date.json')
def get_weight_and_date_json():
    """Get the weight and date of the user as JSON"""

    user_id = session.get('user_id')

    if user_id:
        weight_and_date_rows = crud.get_user_weight_notes(user_id)
        weight_and_date = [{'date': str(row.date), 'weight': row.weight_value} for row in weight_and_date_rows]

        return jsonify({'data': weight_and_date})
    else:
        return jsonify({'error': 'User session not found'})

@app.route('/calculate_tdee', methods=['GET', 'POST'])
def calculate_tdee():
    tdee_calories = None
    tdee_goal = None

    if request.method == 'POST':
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        activity_level = float(request.form.get('activity_level'))
        goal = request.form.get('goal')

        tdee_calories = crud.calculate_tdee_calories(weight, height, age, gender, activity_level, goal)
        
        if tdee_calories is None:
            flash('Invalid calculation inputs. Please try again.')
            return redirect('/calculate_tdee')
        
        user_id = session.get('user_id')

        if goal == 'maintain':
            tdee_goal = "Maintain Weight"
        elif goal == 'lose':
            tdee_goal = "Lose Weight"
        elif goal == 'gain':
            tdee_goal = "Gain Weight"
        else:
            tdee_goal = None

        tdee = crud.create_tdee(weight, height, age, gender, activity_level, tdee_calories, goal, user_id)
        db.session.add(tdee)
        db.session.commit()

    return render_template('calculate_tdee.html', tdee_calories=tdee_calories, tdee_goal=tdee_goal)

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    """Route for users to enter their min, max, and number of recipes they would like displayed."""

    if request.method == 'POST':
        min_calories = request.form.get("min_calories")
        max_calories = request.form.get("max_calories")
        num_recipes = request.form.get("num_recipes")

        recipes = find_recipes_by_calories(min_calories, max_calories, num_recipes)

        return render_template('recipes.html', recipes=recipes)
    else:
        return render_template('recipe_request.html')

@app.route('/recipe/ingredients/<int:recipe_id>', methods=['GET'])
def view_recipe_ingredients(recipe_id):
    ingredients = get_recipe_ingredients(recipe_id)
    recipe_instructions = get_recipe_steps(recipe_id)
    recipe = crud.get_recipe_source_information(recipe_id)
    
    return render_template('recipe_ingredients.html', ingredients=ingredients, recipe=recipe, recipe_instructions=recipe_instructions)

@app.route('/recipe/<int:recipe_source_id>/favorite', methods=['POST'])
def add_recipe_to_favorites(recipe_source_id):
    user_id = session.get('user_id')  

    if user_id is None:
        flash('You must be logged in to add recipes to your favorites.', 'error')
        return redirect(url_for('login'))

    recipe = crud.get_recipe_source_information(recipe_source_id)

    if recipe is None:
        flash('Recipe not found.', 'error')
        return redirect(url_for('recipes')) 

    favorites = crud.get_favorites_by_user(user_id)
    for favorite in favorites:
        if favorite.recipe_id == recipe.recipe_id:
            flash('Recipe is already in favorites.', 'error')
            return redirect(url_for('recipes'))  

    new_favorite = crud.create_favorite(user_id, recipe.recipe_id)

    db.session.add(new_favorite)
    db.session.commit()

    flash('Recipe added to favorites.', 'success')
    return redirect(url_for('recipes'))

@app.route('/remove-favorite/<int:recipe_id>', methods=['POST'])
def remove_favorite(recipe_id):
    user_id = session.get('user_id')
    favorite = crud.delete_favorite(user_id, recipe_id)

    if favorite is not None:
        db.session.delete(favorite)
        db.session.commit()

    return redirect(url_for('homepage', user_id=user_id))

if __name__ == "__main__":
    connect_to_db(app)
    app.run("localhost", "5000", debug=True)

