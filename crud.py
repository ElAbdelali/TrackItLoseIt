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

if __name__ == "__main__":
    from server import app

    connect_to_db(app)