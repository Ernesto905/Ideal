import openai

import os
import requests
import dotenv
dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_recipes(diet, intolerances, minProtein, minCalories, maxCalories, minFat, maxFat, type : str) -> str:
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
        "apiKey": os.getenv("SPOONACULAR")
    }

    response = requests.get(url, params=params)
    recipe_info=""
    if response.status_code == 200:
        response_data = response.json()
        for i, recipe in enumerate(response_data["results"], 1):
          dish_title = recipe["title"]
          image_url = recipe["image"]
          calories = recipe["nutrition"]["nutrients"][0]["amount"]
          calories_unit = recipe["nutrition"]["nutrients"][0]["unit"]
          protein = recipe["nutrition"]["nutrients"][1]["amount"]
          protein_unit = recipe["nutrition"]["nutrients"][1]["unit"]
          fat = recipe["nutrition"]["nutrients"][2]["amount"]
          fat_unit = recipe["nutrition"]["nutrients"][2]["unit"]

          # Construct the string format
          recipe_info += f"Dish {i}: {dish_title}\nImage: {image_url}\nCalories: {calories}{calories_unit}\nProtein: {protein}{protein_unit}\nFat: {fat}{fat_unit}\n"
        print(recipe_info)
    else:
        print("Error:", response.status_code)
    return recipe_info


def get_completion(messages, model="gpt-4", temperature=0, max_tokens=300, tools=None):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=tools
    )
    return response.choices[0].message

def main(current_weight, ideal_weight, body_composition, archetype, age, sex, allergies, diet):
    # Define the toolsif __name__ == "__main__" that we want to use
    # This is defined in JSON format for the OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_recipes",
                "description": "Get a list of recommended ingredients to make dishes out of, and give examples. The diet should be one of [vegetarian, lacto-vegetarian, ovo-vegetarian, vegan, pescetarian, paleo, primal]. The intolerances should be one of ["", dairy, egg, gluten, grain, peanut, seafood, sesame, shellfish, soy, sulfite, wheat]. If intolerances are not specified in the prompt, just use "". The minCalories shoulbe be >= 50, maxCalories should be <= 800, maxProtein should be <= 100, minFat >= 1, maxFat <= 100. Make sure you specify values for protein, calories, and fat that you think is best suited for them to achieve their goals. Type should be one of [breakfast, main course, dessert]",
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
                            "description": "The type of meal, i.e. breakfast, lunch, dinner"
                        },
                    },
                    "required": ["diet, intolerances, minProtein, minCalories, maxCalories, minFat, maxFat", "type"],
                },
            },
        }
    ]

    # Pre-load a message to begin the conversation
    msg = f"I am {age} years old, {sex}, {body_composition} and follow a {diet} diet, I want to become {archetype}. My current weight is {current_weight} and I want to become {ideal_weight}. I am allergic to {allergies}. What should I eat for dessert?"
    messages = [
        {
            "role": "user",
            "content": msg
        }
    ]
    # print(f"User: {msg}\n---")


    response = get_completion(messages, tools=tools)

    # Now, we need to parse the response - the response will contain a TOOL CALL, rather than a completion.
    # The TOOL CALL tells us the function (and appropriate arguments) that the LLM wants to call.
    # This works because OpenAI's API LLMs have been fine-tuned to understand and call functions - other LLMs, such as Llama, do not have this capability.

    # Uncomment the following line to see the response object
    # print(response)

    tool_responses = []
    for tool_call in response.tool_calls:
        function_name = tool_call.function.name
        function_args = eval(tool_call.function.arguments)

        function_call = function_name + "(\'" + (function_args)["diet"] + "\',"

        if "intolerances" in function_args:
            function_call += "\'" + (function_args)["intolerances"] + "\',"
        else:
            function_call += "\'\',"

        function_call += "\'" + (function_args)["minProtein"] + "\',"
        function_call += "\'" + (function_args)["minCalories"] + "\',"
        function_call += "\'" + (function_args)["maxCalories"] + "\',"
        function_call += "\'" + (function_args)["minFat"] + "\',"
        function_call += "\'" + (function_args)["maxFat"] + "\', " + "\'dessert\')"

        tool_response = eval(function_call)
        # print(f"Function returns: {tool_response}\n---")
        tool_responses.append({"function_name": function_name, "tool_response": tool_response})

    # Adjust the messages array for next API call
    messages = [
        {
            "role": "user",
            "content": msg
        },
        response,
    ]

    for idx, tool_call in enumerate(response.tool_calls):
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_responses[idx]['function_name'],
                "content": tool_responses[idx]['tool_response'],
            }
        )


    response = get_completion(messages, tools=tools)

    print(f"AI: {response.content}\n---")
    return response.content
