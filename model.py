"""
Models for a fitness tracking app.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///trackitloseit", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

# TDEE table with id, weight, height, age, gender, activity_level, tdee_calories, user_id as columns
# One to many relationship setup with User
class TDEE(db.Model):
    """TDEE"""
    
    __tablename__ = "tdee"
    
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    activity_level = db.Column(db.String)
    tdee_calories = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    
    user = db.relationship("Users", back_populates="tdee")

# Users table with id, username, password, first_name, last_name, date_of_birth, email, and created at as columns
# One to Many Relationships setup with tdee, weight_notes, favorites 
class Users(db.Model):
    """Users"""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    
    tdee = db.relationship("TDEE", back_populates="user")
    weight_notes = db.relationship("WeightNotes", back_populates="user")
    favorites = db.relationship("Favorites", back_populates="user")

# WeightNotes Table with user_id (refers to User), workouts_done, weight_value, and date as columns
# One to many relationship between user and weight_notes
class WeightNotes(db.Model):
    """Weight Notes"""
    
    __tablename__ = "weight_notes"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    workouts_done = db.Column(db.Text)
    weight_value = db.Column(db.Float)
    date = db.Column(db.DateTime)
    
    user = db.relationship("Users", back_populates="weight_notes")

# recipes table with recipe_name,  calories, recipe_image_url, and recipe_source_url as columns 
# Two one to many relationships with recipe_ingredients and favorites
class Recipes(db.Model):
    """Recipes"""
    
    __tablename__ = "recipes"
    
    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_source_id = db.Column(db.Integer, unique=True)
    recipe_name = db.Column(db.String)
    calories = db.Column(db.Integer)
    recipe_image_url = db.Column(db.String)
    recipe_source_url = db.Column(db.String)
    
    recipe_ingredients = db.relationship("RecipeIngredients", back_populates="recipes")
    favorites = db.relationship("Favorites", back_populates="recipes")

# recipe_ingredients table with recipe_id, ingredient_name, ingredient_amount, and ingredient_unit as columns
# One to many relationship with Recipes
class RecipeIngredients(db.Model):
    """Recipe Ingredients"""
    
    __tablename__ = "recipe_ingredients"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_source_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), unique=True)
    ingredient_name = db.Column(db.String)
    ingredient_amount = db.Column(db.String)
    ingredient_unit = db.Column(db.String)
    
    recipe = db.relationship("Recipes", back_populates="recipe_ingredients")
    
# Favorites table with recipe_id, user_id
# two many to one relationship with Recipes and recipe_ingredients
class Favorites(db.Model):
    """Favorites"""
    
    __tablename__ = "favorites"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    
    user = db.relationship("Users", back_populates="favorites")
    recipe = db.relationship("Recipes", back_populates="favorites")


if __name__ == '__main__':
    from server import app
    import os
    
    os.system("dropdb trackitloseit --if-exists")
    os.system("createdb trackitloseit")

    connect_to_db(app)

    # Create the tables
    db.drop_all()
    db.create_all()