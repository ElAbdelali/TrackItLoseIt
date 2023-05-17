from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
from jinja2 import StrictUndefined

import crud
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

@app.route("TDEE")
def tdee(method="POST")
    
#example route recipe search by user input (minCalories, maxCalories, number of recipes wanted)
@app.route('/recipe-search')
def recipe_search():
    # form rendered at this route
    return render_template('recipe-search.html')

@app.route('/get-recipes', methods=["GET"])
def get_recipes():
    min_cals = request.args.get('min_calories')
    max_cals = request.args.get('max_calories')
    num_of_recipes = request.args.get('num_of_recipes')

    # Check in database for recipes meeting user's input min and max cals
    # if recipes found, display recipes form database to user
    # if no recipes found, then make the api request, and display api response to user

    recipes = spoonacularsearch.find_recipe_by_calories(min_cals, max_cals, num_of_recipes)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)