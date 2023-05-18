from flask import (Flask, render_template, request, flash, session, jsonify,
                   redirect)
from datetime import datetime
from model import connect_to_db, db
from jinja2 import StrictUndefined

import crud, model
import spoonacularsearch

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""
    
    return render_template('index.html')

@app.route("/recipes")
def all_movies():
    """View all movies."""

    recipes = crud.get_recipes()

    return render_template("recipes.html", recipes=recipes)

# @app.route("TDEE")
# def tdee(method="POST")
    
# #example route recipe search by user input (minCalories, maxCalories, number of recipes wanted)
# @app.route('/recipe-search')
# def recipe_search():
#     # form rendered at this route
#     return render_template('recipe-search.html')

# @app.route('/get-recipes', methods=["GET"])
# def get_recipes():
#     min_cals = request.args.get('min_calories')
#     max_cals = request.args.get('max_calories')
#     num_of_recipes = request.args.get('num_of_recipes')

#     # Check in database for recipes meeting user's input min and max cals
#     # if recipes found, display recipes form database to user
#     # if no recipes found, then make the api request, and display api response to user

#     recipes = spoonacularsearch.find_recipe_by_calories(min_cals, max_cals, num_of_recipes)

# @app.route('/calculate_tdee', methods=['GET'])
# def calculate_tdee():
#     data = request.get_json()

#     # Retrieve the input values from the data
#     weight = float(data['weight'])
#     height = float(data['height'])
#     age = int(data['age'])
#     gender = data['gender']
#     activity_level = float(data['activity_level'])

#     # Perform TDEE calculation
#     if gender == 'male':
#         tdee = 10 * weight + 6.25 * height - 5 * age + 5
#     elif gender == 'female':
#         tdee = 10 * weight + 6.25 * height - 5 * age - 161
#     else:
#         return jsonify({'error': 'Invalid gender'})

#     tdee *= activity_level

#     # Save the TDEE data into the database
#     tdee_calories = tdee
#     created_at = datetime.utcnow()
#     user_id = 1  # Replace with the actual user ID

#     db_tdee = crud.create_tdee(weight, height, age, gender, activity_level, tdee_calories, user_id, created_at)
#     model.db.session.add(db_tdee)
#     model.db.session.commit()

#     # Return the calculated TDEE as a JSON response
#     return jsonify({'tdee': tdee})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)