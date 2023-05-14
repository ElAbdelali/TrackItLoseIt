import requests
import json

params = {
    'minCalories': '900',
    'maxCalories': '1900',
    'apiKey': 'dab35f4e82364810a9d2996cee3b687b',
    'number': '1'
    
    
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

for i in range(len(extended_ingredients)):
    ingredient_name = recipeIngredients[i]["name"]
    ingredient_amount = extended_ingredients[i]["measures"]["us"]["amount"]
    ingredient_unit = extended_ingredients[i]["measures"]["us"]["unitLong"]
    
    output.append({
        "ingredient_name": ingredient_name, 
        "ingredient_amount": ingredient_amount, 
        "ingredient_unit": ingredient_unit,
        })

with open('data/recipedata.json', 'w') as f:
    json.dump(output, f, indent=4)