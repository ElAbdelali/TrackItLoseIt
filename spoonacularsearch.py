import requests
import json

params = {
    'minCalories': '900',
    'maxCalories': '1900',
    'apiKey': '4ff5446f172e4657adb4966662984339'
    
    
}
params2 = {
    'includeNutrition': 'false',
    'apiKey': '4ff5446f172e4657adb4966662984339'
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
    
with open('data/recipedata.json', 'w') as f:
    json.dump(output, f, indent=4)