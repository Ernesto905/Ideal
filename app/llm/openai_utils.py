from flask import jsonify
from openai import OpenAI
import dotenv
import json
from llm import recipe_utils, nutrition_functions
from llm.workout_utils import workout_system_msg, workout_user_msg

dotenv.load_dotenv()
client = OpenAI()


def get_completion(form_input):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. You are concise and to the point.",
            },
            {"role": "user", "content": form_input},
        ],
    )

    return completion.choices[0].message


def initialize_nutrition_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "get_recipes",
                "description": "Get a list of recommended ingredients to make dishes out of, and give examples. The diet should be one of [vegetarian, lacto-vegetarian, ovo-vegetarian, vegan, pescetarian, paleo, primal]. The intolerances should be one of ["
                ", dairy, egg, gluten, grain, peanut, seafood, sesame, shellfish, soy, sulfite, wheat]. If intolerances are not specified in the prompt, just use "
                ". The minCalories shoulbe be >= 50, maxCalories should be <= 800, maxProtein should be <= 100, minFat >= 1, maxFat <= 100. Make sure you specify values for protein, calories, and fat that you think is best suited for them to achieve their goals. Type should be one of [breakfast, main course, dessert]",
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
                    "required": [
                        "diet, intolerances, minProtein, minCalories, maxCalories, minFat, maxFat",
                        "type",
                    ],
                },
            },
        }
    ]


def complete_nutrition(session):

    # Pre-load a message to begin the conversation
    msg = f"""
    I follow a {session['diet']} diet, my allergies are {session['allergies']}, and my religion is {session['religion']}. 
    Recite to me what my diet, allergies, and religion are.
    """
    messages = [{"role": "user", "content": msg}]

    # To be implemented with tools
    # tools = initialize_tools()
    # response = get_completion(messages, tools=tools)
    response = get_completion(messages)

    return response


def complete_workout(session, typeOfWorkout):
    user_message = workout_user_msg(session, typeOfWorkout)

    system_message = workout_system_msg()
    valid_json = False
    while not valid_json:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            messages=[system_message, user_message],
            temperature=0.5,
        )
        valid_json = is_json(response.choices[0].message.content)
    print("---------------------------------------------------------------")
    print(
        "THE RESPONSE FOR THE ",
        typeOfWorkout,
        "EXERCISE IS: ",
        response.choices[0].message.content,
    )
    print("---------------------------------------------------------------")
    return json.loads(response.choices[0].message.content)


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


def test_backend_garv(session, user_input):
    # Access session values
    current_weight = session.get("current_weight")
    ideal_weight = session.get("ideal_weight")

    archetype = session.get("body_goal")
    age = session.get("age")
    sex = session.get("sex")
    allergies = session.get("allergies")
    diet = session.get("diet")
    religion = session.get("religion")
    anything_else_diet = session.get("anything_else_diet")
    physical_impediments = session.get("physical_impediments")

    session_values = nutrition_functions.main(
        current_weight, ideal_weight, archetype, age, sex, allergies, diet, user_input
    )
    print(f"The return from main is: {session_values}")

    return session_values
