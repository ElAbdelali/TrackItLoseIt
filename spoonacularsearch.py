import requests
import json

params = {
    'minCalories': '900',
    'maxCalories': '1900',
    'number': '1'
    
    
}
params2 = {
    'includeNutrition': 'false',
    'id': '642712'
}

res = requests.get('https://api.spoonacular.com/recipes/findByNutrients', params=params)

recipes = res.json()

num_results = len(recipes)
output = []

for i in range(num_results):
    title = recipes[i].get('title')
    calories = recipes[i].get('calories')
    img = recipes[i].get('image')
    id = recipes[i].get('id')
    recipeUrl = requests.get(f'https://api.spoonacular.com/recipes/{id}/information',params=params2)
    
    output.append({
        "title": title, 
        "calories": calories, 
        "image": img,
        "recipeId": id,
        "recipeSource": recipeUrl.json()['spoonacularSourceUrl']
        })
        
recipeIngredients = requests.get(f'https://api.spoonacular.com/recipes/{id}/information',params=params2).json()
extended_ingredients = recipeIngredients["extendedIngredients"]
ingredient_list =[]

for ing in (extended_ingredients):
    recipe_source_id = ing["id"]
    ingredient_name = ing["name"]
    ingredient_amount = ing["measures"]["us"]["amount"]
    ingredient_unit = ing["measures"]["us"]["unitLong"]
    
    output.append({
        "recipe_source_id": recipe_source_id,
        "ingredient_name": ingredient_name, 
        "ingredient_amount": ingredient_amount, 
        "ingredient_unit": ingredient_unit
        })

with open('data/recipedata.json', 'w') as f:
    json.dump(output, f, indent=4)