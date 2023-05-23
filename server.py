from flask import (Flask, render_template, request, flash, session, jsonify,
                   redirect)
import datetime
from model import connect_to_db, db
from jinja2 import StrictUndefined

import crud, model
from crud import create_user
from spoonacularsearch import get_recipe_ingredients, find_recipes_by_calories

app = Flask(__name__)
app.secret_key = "dev"
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
            
        
        
    return render_template('register.html')
@app.route('/chart')
def chart():
    return render_template('weight_tracker.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)