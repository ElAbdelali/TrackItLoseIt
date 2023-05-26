"""Crud Operations"""
from model import db, TDEE, User, WeightNotes, Recipes, RecipeIngredients, Favorite, connect_to_db
import requests


# Create a new TDEE entry
def create_tdee(weight, height, age, gender, activity_level, tdee_calories, goal, user_id):
    tdee = TDEE(weight=weight, height=height, age=age, gender=gender, activity_level=activity_level, tdee_calories=tdee_calories, goal=goal, user_id=user_id)

    return tdee

# Create a new user
def create_user(username, password, first_name, last_name, date_of_birth, email, created_at):
    user = User(username=username, password=password, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, email=email, created_at=created_at)

    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_username(username):
    """Return a user by username."""

    return User.query.filter(User.username == username).first()

def get_user_by_id(user_id):
    """Return a user by ID."""
    return User.query.get(user_id)

# Create a new weight note
def create_weight_note(user_id, workouts_done, weight_value, date):
    weight_note = WeightNotes(user_id=user_id, workouts_done=workouts_done, weight_value=weight_value, date=date)

    return weight_note

def get_user_weight_notes(user_id):
    weights_and_dates = db.session.query(WeightNotes.weight_value, WeightNotes.date).filter_by(user_id=user_id).all()
    return weights_and_dates

# Create a new recipe
def create_recipe(recipe_source_id, recipe_name, calories, recipe_image_url, recipe_source_url):
    recipe = Recipes(recipe_source_id=recipe_source_id, recipe_name=recipe_name, calories=calories, recipe_image_url=recipe_image_url, recipe_source_url=recipe_source_url)

    return recipe

# Create a new recipe ingredient
def create_recipe_ingredient(recipe_source_id, ingredient_id, ingredient_name, ingredient_amount, ingredient_unit):
    recipe_ingredient = RecipeIngredients(recipe_source_id=recipe_source_id, ingredient_id=ingredient_id, ingredient_name=ingredient_name, ingredient_amount=ingredient_amount, ingredient_unit=ingredient_unit)

    return recipe_ingredient

# Create a new favorite
def create_favorite(user, favorite):
    favorite = Favorite(user=user, favorite=favorite)

    return favorite

# create a crud operation to query calories by ensuring they are less than maxCalories input by user
# Recipes.query.filter_by..... where to column of calories < the entered user cals

if __name__ == "__main__":
    from server import app

    connect_to_db(app)