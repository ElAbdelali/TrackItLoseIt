import requests
import json

params = {
    'minCalories': '900',
    'maxCalories': '1900',
    'apiKey': 'dab35f4e82364810a9d2996cee3b687b',
    'number': '3'
}

params2 = {
    'includeNutrition': 'false',
    'apiKey': 'dab35f4e82364810a9d2996cee3b687b',
    'id': '642712'
}

res = requests.get('https://api.spoonacular.com/recipes/findByNutrients', params=params)
recipes = res.json()

num_results = len(recipes)
output = []

for i in range(num_results):
    recipe_name = recipes[i].get('title')
    calories = recipes[i].get('calories')
    recipe_image_url = recipes[i].get('image')
    recipe_source_id = recipes[i].get('id')
    recipe_source_url = requests.get(f'https://api.spoonacular.com/recipes/{recipe_source_id}/information', params=params2)
    recipe_data = recipe_source_url.json()

    recipe_output = {
        "recipe_name": recipe_name,
        "calories": calories,
        "recipe_image_url": recipe_image_url,
        "recipe_source_id": recipe_source_id,
        "recipe_source_url": recipe_data['spoonacularSourceUrl'],
        "ingredients": []
    }

    recipeIngredients = recipe_data["extendedIngredients"]
    for ing in recipeIngredients:
        recipe_source_id = recipes[i].get('id')
        ingredient_id = ing["id"]
        ingredient_name = ing["name"]
        ingredient_amount = ing["measures"]["us"]["amount"]
        ingredient_unit = ing["measures"]["us"]["unitLong"]

        ingredient_output = {
            "recipe_source_id": recipe_source_id,
            "ingredient_id": ingredient_id,
            "ingredient_name": ingredient_name,
            "ingredient_amount": ingredient_amount,
            "ingredient_unit": ingredient_unit
        }

        recipe_output["ingredients"].append(ingredient_output)

    output.append(recipe_output)

with open('data/recipedata.json', 'w') as f:
    json.dump(output, f, indent=4)
