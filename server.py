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
      
    return render_template('homepage.html')


@app.route('/recipe_request', methods=['GET', 'POST'])
def recipe_request():
    """Route for users to enter their min, max, and number of recipes they would like displayed."""
    
    return render_template('recipe_request.html')

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        min_calories = request.form.get("min_calories")
        max_calories = request.form.get("max_calories")
        num_recipes = request.form.get("num_recipes")

        recipes = find_recipes_by_calories(min_calories, max_calories, num_recipes)

        return render_template('recipes.html', recipes=recipes)
    else:
        # Handle GET requests for displaying the form or other actions
        return render_template('recipes.html', recipes=[])


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
            return '''
                <script>
                    alert("Username must be at least 7 characters long!");
                    window.location.href = "/register"; // Redirect to the registration page
                </script>'''
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return '''
                <script>
                    alert("Password must contain at least one special character!");
                    window.location.href = "/register"; // Redirect to the registration page
                </script>'''
        elif len(password) < 9:
            return '''
                <script>
                    alert("Password must be at least 9 characters long!");
                    window.location.href = "/register"; // Redirect to the registration page
                </script>'''
        # Validate age (13 years or older)
        dob = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        age = relativedelta(datetime.date.today(), dob).years
        if age < 13:
            return '''
                <script>
                    alert("You must be 13 years or older to register!");
                    window.location.href = "/register"; // Redirect to the registration page
                </script>'''

        elif crud.get_user_by_email(email):
            return '''
                <script>
                    alert("User with this email already exists!");
                    window.location.href = "/register"; // Redirect to the registration page
                </script>'''
        elif crud.get_user_by_username(username):
            return '''
                <script>
                    alert("User with this username already exists!");
                    window.location.href = "/register"; // Redirect to the registration page
                </script>'''
        else:
            user = crud.create_user(username, password, first_name, last_name, date_of_birth, email, created_at)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = crud.get_user_by_username(username)

        if user:
            stored_password = user.password
            if password == stored_password:
                # Login successful
                # Perform the desired actions, such as setting a session variable
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

@app.route('/calculate_tdee', methods=['GET', 'POST'])
def calculate_tdee():
    if request.method == 'POST':
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        activity_level = float(request.form.get('activity_level'))
        goal = request.form.get('goal')

        # Calculate TDEE calories
        tdee_calories = calculate_tdee_calories(weight, height, age, gender, activity_level, goal)
        
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
        
        return render_template('tdee_result.html', tdee_calories=tdee_calories, tdee_goal=tdee_goal)
    
    return render_template('calculate_tdee.html')


def calculate_tdee_calories(weight, height, age, gender, activity_level, goal):
    # Convert weight from pounds to kilograms
    weight_kg = weight * 0.45359237

    # Convert height from inches to centimeters
    height_cm = height * 2.54


    # Example calculation using Harris-Benedict equation
    if gender == 'male':
        bmr = 66 + (6.23 * weight_kg) + (12.7 * height_cm) - (6.8 * age)
    elif gender == 'female':
        bmr = 655 + (4.35 * weight_kg) + (4.7 * height_cm) - (4.7 * age)
    else:
        # Handle invalid gender case
        return None

    # Apply activity level to BMR
    if activity_level == 1.2:
        tdee = bmr * 1.2  # Sedentary (little to no exercise)
    elif activity_level == 1.375:
        tdee = bmr * 1.375  # Lightly Active (light exercise/sports 1-3 days/week)
    elif activity_level == 1.55:
        tdee = bmr * 1.55  # Moderately Active (moderate exercise/sports 3-5 days/week)
    elif activity_level == 1.725:
        tdee = bmr * 1.725  # Very Active (hard exercise/sports 6-7 days/week)
    elif activity_level == 1.9:
        tdee = bmr * 1.9  # Extra Active (very hard exercise/sports & physical job or 2x training)
    else:
        # Handle invalid activity level case
        return None

    # Adjust TDEE based on the user's goal
    if goal == 'maintain':
        tdee_calories = tdee  # Maintain Weight (no adjustment)
    elif goal == 'lose':
        tdee_calories = tdee - 500  # Lose Weight (reduce 500 calories from TDEE)
    elif goal == 'gain':
        tdee_calories = tdee + 500  # Gain Weight (add 500 calories to TDEE)
    else:
        # Handle invalid goal case
        return None

    return tdee_calories


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

