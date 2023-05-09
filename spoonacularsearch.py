import requests


params = {
    'minCalories': '600',
    'maxCalories': '1900',
    'apiKey': '1bc98f8a0b1b450bb695bc06f53a814d'
    
}
params2 = {
    'includeNutrition': 'false',
    'apiKey': '1bc98f8a0b1b450bb695bc06f53a814d'
}

res = requests.get('https://api.spoonacular.com/recipes/findByNutrients', params=params)

recipes = res.json()

num_results = len(recipes)

for i in range(num_results):
    title = recipes[i].get('title')
    calories = recipes[i].get('calories')
    img = recipes[i].get('image')
    id = recipes[i].get('id')
    recipeUrl = requests.get(f'https://api.spoonacular.com/recipes/{id}/information',params=params2)
    print(f'{title}:{calories} {img} {id} {recipeUrl.json()["spoonacularSourceUrl"]}')