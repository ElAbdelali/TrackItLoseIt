"""
Models for a fitness tracking app.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import server
db = SQLAlchemy()


def connect_to_db(flask_app, db_uri="postgresql:///trackitloseit", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class Users(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.DateTime,  nullable=False)
    email = db.Column(db.String(50),  nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    weights = db.relationship("Weight", back_populates="user")
    notes = db.relationship("Note", back_populates="user")
    recipes = db.relationship("Recipe", back_populates="user")
    workouts = db.relationship("Workouts", back_populates="user")
    tdee = db.relationship("TDEE", back_populates="user")

    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'

class TDEE(db.Model):
    """TDEE """
    
    __tablename__ = "tdee"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    activity_level = db.Column(db.String(50), nullable=False)
    tdee_value = db.Column(db.Integer,  nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    last_updated = db.Column(db.DateTime, default=datetime.now())
    
    user = db.relationship("Users", back_populates="tdee")
    
class Weight(db.Model):
    """A weight measurement."""

    __tablename__ = "weights"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weight_value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user = db.relationship("Users", back_populates="weights")

    def __repr__(self):
        return f'<Weight id={self.id} weight_value={self.weight_value}>'
    

class Note(db.Model):
    """A user note."""

    __tablename__ = "notes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user = db.relationship("Users", back_populates="notes")

    def __repr__(self):
        return f'<Note id={self.id} note_text={self.note_text}>'
    

class Recipe(db.Model):
    """A user recipe."""

    __tablename__ = "recipes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_name = db.Column(db.String(50), nullable=False)
    calories_per_serving = db.Column(db.Integer, nullable=False)
    recipe_image_url = db.Column(db.String(200), nullable=False)
    recipe_source_url = db.Column(db.String(200), nullable=False)

    user = db.relationship("Users", back_populates="recipes")
    ingredients = db.relationship("RecipeIngredient", back_populates="recipe")

    def __repr__(self):
        return f'<Recipe id={self.id} recipe_name={self.recipe_name}>'
    

class RecipeIngredient(db.Model):
    """An ingredient in a user recipe."""

    __tablename__ = "recipe_ingredients"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_name = db.Column(db.String(50), nullable=False)
    ingredient_amount = db.Column(db.String(50), nullable=False)
    ingredient_unit = db.Column(db.String(50), nullable=False)
    
    
    recipe = db.relationship("Recipe", back_populates='ingredients')

    
class Workouts(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_name = db.Column(db.String(40), nullable=False)
    body_group = db.Column(db.String(40), nullable=False)

    user = db.relationship("Users", back_populates="workouts")

    def __repr__(self):
        return f"<Workout(id={self.id}, workout_name='{self.workout_name}', body_group='{self.body_group}')>"

if __name__ == '__main__':
    from server import app
    import os
    
    os.system("dropdb trackitloseit --if-exists")
    os.system("createdb trackitloseit")

    connect_to_db(app)

    # Create the tables
    db.drop_all()
    db.create_all()