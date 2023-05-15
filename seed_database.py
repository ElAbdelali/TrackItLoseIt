import os
import json

import crud
import model
import server
import random
from datetime import datetime

os.system("dropdb trackitloseit")
os.system('createdb trackitloseit')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/recipedata.json') as f:
    recipe_data = json.loads(f.read())
    
with open('data/users.json') as f:
    user_data = json.loads(f.read())

with open("data/tdee.json") as f:
    tdee_data = json.loads(f.read())

recipe_data_in_db = []
users_in_db = []
tdee_in_db = []
for user in user_data:
    username = user["username"]
    password = user["password"]
    first_name = user["first_name"]
    last_name = user["last_name"]
    date_of_birth = user["date_of_birth"]
    email = user["email"]
    created_at = datetime.utcnow()

         
    db_user = crud.create_user(username, password, first_name, last_name, date_of_birth, email, created_at=created_at)
    users_in_db.append(db_user)
    
model.db.session.add_all(users_in_db)
model.db.session.commit()
    
for data in tdee_data:
    weight = data["weight"]
    height = data["height"]
    age = data["age"]
    gender = data["gender"]
    activity_level = data["activity_level"]
    tdee_calories = data["tdee_calories"]
    user_id = random.choice(users_in_db).id
    

    db_tdee = crud.create_tdee(weight, height, age, gender, activity_level, tdee_calories, user_id)
    tdee_in_db.append(db_tdee)

model.db.session.add_all(tdee_in_db)
model.db.session.commit()
     
for recipe in recipe_data:
    recipe_source_id = recipe["recipe_source_id"]
    recipe_name = recipe["recipe_name"]
    calories = recipe["calories"]
    recipe_image_url = recipe["recipe_image_url"]
    recipe_source_url = recipe["recipe_source_url"]

    db_recipe = crud.create_recipe(recipe_source_id, recipe_name, calories, recipe_image_url, recipe_source_url)
    recipe_data_in_db.append(db_recipe)

for recipe in recipe_data:
    recipe_source_id = recipe["recipe_source_id"]
    ingredients = recipe["ingredients"]

    for ingredient in ingredients:
        ingredient_id = ingredient["ingredient_id"]
        ingredient_name = ingredient["ingredient_name"]
        ingredient_amount = ingredient["ingredient_amount"]
        ingredient_unit = ingredient["ingredient_unit"]

        db_ingredient = crud.create_recipe_ingredient(recipe_source_id, ingredient_id, ingredient_name, ingredient_amount, ingredient_unit)
        recipe_data_in_db.append(db_ingredient)
        
objects_to_add = recipe_data_in_db + users_in_db + tdee_in_db
model.db.session.add_all(objects_to_add)
model.db.session.commit()
