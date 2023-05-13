import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb trackitloseit")
os.system('createdb trackitloseit')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/recipedata.json') as f:
    recipe_data = json.loads(f.read())
    
recipe_data_in_db = []

for recipe in recipe_data:
    recipe_source_id, recipe_name, calories, recipe_image_url, recipe_source_url = (
        recipe["recipeId"],
        recipe["title"],
        recipe["calories"],
        recipe["image"],
        recipe["recipeSource"]
    )
    
    db_recipe = crud.create_recipe(recipe_source_id, recipe_name, calories, recipe_image_url, recipe_source_url)
    recipe_data_in_db.append(db_recipe)

# for ingredient in recipe_ingredient_data:
#     recipe_source_id, ingredient_name, ingredient_amount, ingredient_unit = (
        
#     )

model.db.session.add_all(recipe_data_in_db)
model.db.session.commit()