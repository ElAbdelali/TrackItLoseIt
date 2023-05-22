import requests
import json
import os

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

        recipe_output = {
            'recipe_source_id': recipe_id,
            'ingredients': ingredients
        }

        return recipe_output
    else:
        print(f"Request failed with status code: {recipe_source_res.status_code}")
        return {}
