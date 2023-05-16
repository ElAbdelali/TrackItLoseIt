from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
from jinja2 import StrictUndefined

import crud

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

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)