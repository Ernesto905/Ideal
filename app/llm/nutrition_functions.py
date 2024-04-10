import openai

import os
import requests
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_recipes(
    diet, intolerances, minProtein, minCalories, maxCalories, minFat, maxFat, type: str
) -> str:
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "diet": diet,
        "intolerances": intolerances,
        "minProtein": minProtein,
        "minCalories": minCalories,
        "maxCalories": maxCalories,
        "minFat": minFat,
        "maxFat": maxFat,
        "type": type,
        "apiKey": os.getenv("SPOONACULAR"),
    }

    response = requests.get(url, params=params)
    recipe_info = ""
    if response.status_code == 200:
        response_data = response.json()
        recipe = response_data["results"][0]  # Selecting only the first recipe
        dish_title = recipe["title"]
        image_url = recipe["image"]
        calories = recipe["nutrition"]["nutrients"][0]["amount"]
        calories_unit = recipe["nutrition"]["nutrients"][0]["unit"]
        protein = recipe["nutrition"]["nutrients"][1]["amount"]
        protein_unit = recipe["nutrition"]["nutrients"][1]["unit"]
        fat = recipe["nutrition"]["nutrients"][2]["amount"]
        fat_unit = recipe["nutrition"]["nutrients"][2]["unit"]
        id = recipe["id"]

        # Construct the string format
        recipe_info = f"Dish 1: {dish_title}\nImage: {image_url}\nCalories: {calories}{calories_unit}\nProtein: {protein}{protein_unit}\nFat: {fat}{fat_unit}\n"
        # print(recipe_info)

    else:
        print("Error:", response.status_code)
    return recipe_info


def get_completion(messages, model="gpt-4", temperature=0, max_tokens=300, tools=None):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=tools,
    )
    return response.choices[0].message


def main(allergies, diet, religion, user_input):
    # Define the toolsif __name__ == "__main__" that we want to use
    # This is defined in JSON format for the OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_recipes",
                "description": "Get back a recipe recipes for a user based on their dietary restrictions and nutrition specification as input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "diet": {
                            "type": "string",
                            "description": "The diet they follow",
                        },
                        "intolerances": {
                            "type": "string",
                            "description": "What they avoid or what they're allergic to",
                        },
                        "minProtein": {
                            "type": "string",
                            "description": "The minimum protein amount in a meal they should consume to achiece their goals",
                        },
                        "minCalories": {
                            "type": "string",
                            "description": "The minimum amount of calories in a meal they should consume to achiece their goals",
                        },
                        "maxCalories": {
                            "type": "string",
                            "description": "The maximum amount of calories in a meal they should consume to achiece their goals",
                        },
                        "minFat": {
                            "type": "string",
                            "description": "The minimum amount of fat in a meal they should consume to achiece their goals",
                        },
                        "maxFat": {
                            "type": "string",
                            "description": "The maximum amount of fat in a meal they should consume to achiece their goals",
                        },
                        "type": {
                            "type": "string",
                            "description": "The type of meal, i.e. breakfast, lunch, dinner",
                        },
                    },
                    "required": [],
                },
            },
        }
    ]

    diet_string = f"I follow a {diet} diet." if diet else ""
    allergy_string = f"I am allergic to {allergies}." if allergies else ""
    religion_string = f"I am religious. My religion is {religion}" if religion else ""

    # Pre-load a message to begin the conversation
    msg = (
        f"{diet_string}. {allergy_string}"
        + user_input
        + ". What should I eat? Use only the tools available. If the tools aren't available then return a 'Im sorry i dont have access to the tools for that'. Your output should be in the form of a single recipe. It should be in markdown and you should ensure the image is on a different line than the rest of the recipe's information."
    )

    print(msg)
    messages = [{"role": "user", "content": msg}]

    response = get_completion(messages, tools=tools)

    tool_responses = []
    for tool_call in response.tool_calls:
        function_name = tool_call.function.name
        function_args = eval(tool_call.function.arguments)

        function_call = function_name + "("

        if "diet" in function_args:
            function_call += "'" + (function_args)["diet"] + "',"
        else:
            function_call += "'', "

        if "intolerances" in function_args:
            function_call += "'" + (function_args)["intolerances"] + "',"
        else:
            function_call += "'',"

        if "minProtein" in function_args:
            function_call += "'" + (function_args)["minProtein"] + "',"
        else:
            function_call += "'10',"

        if "minCalories" in function_args:
            function_call += "'" + (function_args)["minCalories"] + "',"
        else:
            function_call += "'200',"

        if "maxCalories" in function_args:
            function_call += "'" + (function_args)["maxCalories"] + "',"
        else:
            function_call += "'800',"

        if "minFat" in function_args:
            function_call += "'" + (function_args)["minFat"] + "',"
        else:
            function_call += "'1',"

        if "maxFat" in function_args:
            function_call += "'" + (function_args)["maxFat"] + "',"
        else:
            function_call += "'100',"

        if "type" in function_args:
            function_call += "'" + (function_args)["type"] + "'"
        else:
            function_call += "'" + "'"
        function_call += ")"
        print("Funtion call: ", function_call)

        tool_response = eval(function_call)
        tool_responses.append(
            {"function_name": function_name, "tool_response": tool_response}
        )

    # Adjust the messages array for next API call
    messages = [
        {"role": "user", "content": msg},
        response,
    ]

    for idx, tool_call in enumerate(response.tool_calls):
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_responses[idx]["function_name"],
                "content": tool_responses[idx]["tool_response"],
            }
        )

    response = get_completion(messages, tools=tools)

    # print(f"AI: {response.content}\n---")
    return response.content
