from openai import OpenAI
import os
import json
import requests
import dotenv


dotenv.load_dotenv()
client = OpenAI()


def display_recipes_grid(session):

    url = "https://api.spoonacular.com/recipes/complexSearch"
    params_breakfast = {
        "type": "breakfast",
        "intolerances": session["allergies"],
        "diet": session["diet"],
        "apiKey": os.getenv("SPOONACULAR"),
    }
    params_salad = {
        "type": "salad",
        "intolerances": session["allergies"],
        "diet": session["diet"],
        "apiKey": os.getenv("SPOONACULAR"),
    }
    params_dinner = {
        "type": "main course",
        "intolerances": session["allergies"],
        "diet": session["diet"],
        "apiKey": os.getenv("SPOONACULAR"),
    }
    params_dessert = {
        "type": "dessert",
        "intolerances": session["allergies"],
        "diet": session["diet"],
        "apiKey": os.getenv("SPOONACULAR"),
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
        print("Dinner Success: ", response_dinner.status_code)
    else:
        print("Dinner Error:", response_dinner.status_code)
    if response_dessert.status_code == 200:
        print("Dessert Success: ", response_dessert.status_code)
    else:
        print("Dessert Error:", response_dessert.status_code)

    recipes = {
        "breakfast": response_breakfast.json(),
        "lunch": response_lunch.json(),
        "dinner": response_dinner.json(),
        "dessert": response_dessert.json(),
    }

    # Account for religion. This will be slow, but it's async
    if session["religion"]:
        print("religion detected")
        print("Recipe before: ", recipes)
        recipes = touch_of_god(recipes, session["religion"])

    return recipes


def get_recipe_details(id):
    url = f"https://api.spoonacular.com/recipes/{id}/information"
    params_id = {"apiKey": os.getenv("SPOONACULAR")}
    response = requests.get(url, params=params_id)
    if response.status_code == 200:
        print("Recipe Success: ", response.status_code)
        return response.json()
    else:
        print("ERROR getting recipe:", response.status_code)
        return {"Error": "No response available"}


def get_recipe_nutrients(id):
    url = f"https://api.spoonacular.com/recipes/{id}/nutritionWidget.json"
    params = {"apiKey": os.getenv("SPOONACULAR")}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Nutrients obtained successfully: ", response.status_code)
        return response.json()
    else:
        print("ERROR getting Nutrients:", response.status_code)
        return {"Error": "No response available"}


# Openai utils that must be in this file
def touch_of_god(recipes, religion):
    user_msg = f"""
    my religion is {religion}. 
    Please exclude only the recipes from below which are against my religion, do not change anything else:
    ---
    {recipes}
    """

    user_message = {"role": "user", "content": user_msg}

    system_msg = """
    You will take in a JSON formatted list of recipes and output the same json list after excluding a user inputted religion. It is very important that you return only the allowed foods. Do not remove anything that would be allowed. Return the JSON In the same format as it was inputted. 
    """
    system_message = {"role": "system", "content": system_msg}

    valid_json = False
    while not valid_json:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[system_message, user_message],
            temperature=0.5,
        )
        print("Inside json, so far we have a response of", response)
        valid_json = is_json(response.choices[0].message.content)
    print("------------------------------------")
    print("Recipe after: ", response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True
