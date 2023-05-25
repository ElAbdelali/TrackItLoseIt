from flask import (Flask, render_template, request, flash, session, jsonify,
                   redirect, url_for)
import datetime
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud, model
from crud import create_user
from spoonacularsearch import get_recipe_ingredients, find_recipes_by_calories

app = Flask(__name__)
app.secret_key = "trackitloseit"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""
    session_user = session.get('user')
    username = session.get('username')
    if session_user:
        user_id = session_user.id
        weights_and_dates = crud.get_user_weight_notes(user_id)
        if weights_and_dates:
            return render_template('homepage.html', username=session_user.username, weights_and_dates=weights_and_dates)
        else:
            return render_template('homepage.html', username=session_user.username)
    else:
        return render_template('homepage.html', username=username, weights_and_dates=None)






@app.route('/recipe_request', methods=['GET', 'POST'])
def recipe_request():
    """Route for users to enter their min, max, and number of recipes they would like displayed."""
    
    return render_template('recipe_request.html')

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        # Handle the form submission for POST requests
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
        
        
        if crud.get_user_by_email(email):
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

