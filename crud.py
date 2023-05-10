"""Crud Operations"""
from model import Users, TDEE, Weight, Note, Recipe, RecipeIngredient, Workouts

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    
