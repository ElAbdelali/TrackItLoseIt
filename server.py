from flask import (Flask, render_template, request, flash, session, jsonify,
                   redirect, url_for)
import datetime
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud, model
import re
from crud import create_user
from spoonacularsearch import get_recipe_ingredients, find_recipes_by_calories
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
app.secret_key = "trackitloseit"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""
    user_id = session.get('user_id')
    user = weight_notes = favorite_recipes = None
    
    if user_id:
        user = crud.get_user_by_id(user_id)
        weight_notes = crud.get_user_weight_notes(user_id)
        favorite_recipes = crud.get_favorites_by_user(user_id)

    return render_template('homepage.html', user=user, weight_notes=weight_notes, favorite_recipes=favorite_recipes)


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
        
        # Invalid username or password
        flash('Invalid username or password. Please try again.')
        return redirect('/login')

    # Handle GET request for displaying the login form
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout the user"""
    session.pop('user_id', None)
    session.clear()
    flash('You have been logged out.')
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
        # Retrieve form data
        user_id = request.form.get('user_id')
        workouts_done = request.form.get('workouts_done')
        weight_value = request.form.get('weight_value')
        date = request.form.get('date')

        # Create a new WeightNotes object
        weight_notes = crud.WeightNotes(user_id=user_id, workouts_done=workouts_done, weight_value=weight_value, date=date)

        # Add the weight notes to the database session and commit changes
        db.session.add(weight_notes)
        db.session.commit()

        # Redirect to the weight notes page
        return redirect(url_for('weight_notes'))

    # Fetch the user's weight notes from the database
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

        # Calculate TDEE calories
        tdee_calories = crud.calculate_tdee_calories(weight, height, age, gender, activity_level, goal)
        
        if tdee_calories is None:
            # Handle error case (e.g., invalid gender)
            flash('Invalid calculation inputs. Please try again.')
            return redirect('/calculate_tdee')
        
        user_id = session.get('user_id')

        # Set the TDEE goal based on the button clicked
        if goal == 'maintain':
            tdee_goal = "Maintain Weight"
        elif goal == 'lose':
            tdee_goal = "Lose Weight"
        elif goal == 'gain':
            tdee_goal = "Gain Weight"
        else:
            tdee_goal = None
        
        # Create TDEE record in the database
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
        # Handle GET requests for displaying the form or other actions
        return render_template('recipe_request.html')


@app.route('/recipe/ingredients/<int:recipe_id>', methods=['GET'])
def view_recipe_ingredients(recipe_id):
    ingredients = get_recipe_ingredients(recipe_id)
    
    recipe = crud.get_recipe_source_information(recipe_id)
    return render_template('recipe_ingredients.html', ingredients=ingredients, recipe=recipe)


@app.route('/recipe/<recipe_source_id>/favorite', methods=['POST'])
def add_to_favorites(recipe_source_id):
    """Add a recipe to user's favorites"""
    user_id = session.get('user_id')

    # check if the user is authenticated
    if user_id is None:
        # you can return an error message or redirect to login page
        return redirect(url_for('login'))

    # add the recipe to user's favorites
    crud.create_favorite(user_id, recipe_source_id)

    # redirect back to recipes page (or anywhere else you'd like)
    return redirect(url_for('recipes'))


def connect_to_db(flask_app, db_uri="postgresql:///trackitloseit", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    # # Create or recreate the tables
    # with flask_app.app_context():
    #     db.drop_all()
    #     db.create_all()

    print("Connected to the db!")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

