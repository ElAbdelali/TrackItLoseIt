import requests
import json
import os
import crud
from model import db
from dotenv import load_dotenv

load_dotenv("secrets.sh")
api_key = os.environ.get("API_KEY")

def find_recipes_by_calories(minCals, maxCals, number_of_recipes):
    params = {
        'minCalories': str(minCals),
        'maxCalories': str(maxCals),
        'apiKey': api_key,
        'number': str(number_of_recipes)
    }

    res = requests.get('https://api.spoonacular.com/recipes/findByNutrients', params=params)

    if res.status_code == 200:
        recipes = res.json()
        output = []

        for recipe in recipes:
            recipe_source_id = recipe['id']
            recipe_source_url = f'https://api.spoonacular.com/recipes/{recipe_source_id}/information'

            recipe_output = {
                'recipe_name': recipe['title'],
                'calories': recipe['calories'],
                'recipe_image_url': recipe['image'],
                'recipe_source_id': recipe_source_id,
                'recipe_source_url': recipe_source_url
            }
            
            # Check if the recipe already exists in the database
            existing_recipe = crud.get_recipe_source_information(recipe_source_id)
            if existing_recipe is None:
                # Create a new recipe instance
                recipe_obj = crud.create_recipe(recipe_source_id, recipe_output['recipe_name'], recipe_output['calories'],
                                           recipe_output['recipe_image_url'], recipe_output['recipe_source_url'])
                
                # Add the recipe instance to the session
                db.session.add(recipe_obj)
                db.session.commit()  # Commit after each recipe is added to the session

            output.append(recipe_output)

        return output
    else:
        print(f"Request failed with status code: {res.status_code}")
        return []
def get_recipe_ingredients(recipe_id):
    params = {
        'apiKey': api_key,
    }  

    recipe_source_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    recipe_source_res = requests.get(recipe_source_url, params=params)

    if recipe_source_res.status_code == 200:
        recipe_data = recipe_source_res.json()
        ingredients = []

        for ing in recipe_data['extendedIngredients']:
            ingredient_output = {
                'ingredient_id': ing['id'],
                'ingredient_name': ing['name'],
                'ingredient_amount': ing['measures']['us']['amount'],
                'ingredient_unit': ing['measures']['us']['unitLong']
            }

            ingredients.append(ingredient_output)

        return ingredients
    else:
        print(f"Request failed with status code: {recipe_source_res.status_code}")
        return []
