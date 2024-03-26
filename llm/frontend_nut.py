import os
import requests
import dotenv
dotenv.load_dotenv()

def get_recipes(religion, allergies, diet):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params_breakfast = {
        "type": "breakfast",
        "apiKey": os.getenv("SPOONACULAR")
    }

    params_salad = {
        "type": "salad",
        "apiKey": os.getenv("SPOONACULAR")
    }
    params_dinner = {
        "type": "main course",
        "apiKey": os.getenv("SPOONACULAR")
    }

    params_dessert = {
        "type": "dessert",
        "apiKey": os.getenv("SPOONACULAR")
    }
    response_breakfast = requests.get(url, params=params_breakfast)
    response_lunch = requests.get(url, params=params_salad)
    response_dinner = requests.get(url, params=params_dinner)
    response_dessert = requests.get(url, params=params_dessert)
    if response_breakfast.status_code == 200:
        print("Breakfast Success: ", response_breakfast.status_code)
    else:
        print("Breakfast Error:", response_breakfast.status_code)
    if response_lunch.status_code == 200:
        print("Lunch Success: ", response_lunch.status_code)
    else:
        print("Lunch Error:", response_lunch.status_code)
    if response_dinner.status_code == 200:
        print("Breakfast Success: ", response_dinner.status_code)
    else:
        print("Breakfast Error:", response_dinner.status_code)
    if response_dessert.status_code == 200:
        print("Breakfast Success: ", response_dessert.status_code)
    else:
        print("Breakfast Error:", response_dessert.status_code)
    return [response_breakfast.json(), response_lunch.json(), response_dinner.json(), response_dessert.json()]

