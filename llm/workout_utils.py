import openai
import os
import requests
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import json


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_workout(exercise_type, muscle_group, difficulty) -> str:
    url = "https://exercises-by-api-ninjas.p.rapidapi.com/v1/exercises"
    params = {
        "type": exercise_type,
        "muscle": muscle_group,
        "difficulty": difficulty,
    }
    headers = {}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return response.status_code


def set_up(
    age, gender, height, current_weight, target_weight, fitness_goal, impediments
):
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4",
    )
    prompt = """
             A {age} years old {gender} who currently weighs {current_weight} pounds, is {height} cm tall, and has the following impediments: {impediments},
             is trying to reach {target_weight} pounds and has the fitness goal: {fitness_goal}. Give a sample weekly workout plan.
             """
    prompt = PromptTemplate.from_template(prompt)
    chain = LLMChain(prompt=prompt, llm=llm, output_key="training_plan")

    prompt2 = """
              Take in a training plan: {training_plan}.
              For each day in the sample weekly workout plan, return the following in a list: type of exercise, muscle groups targeted, difficulty level.
              Make sure type of exercise is only one of the following: cardio, rest, strength. 
              Make sure the muscle groups targeted is in the following list: abdominals, adductors, biceps, calves, chest, forearms, glutes,
              hamstrings, lats, lower_back, middle_back, neck, quadriceps, traps, triceps.
              Make sure the diffculty level is one of the following: beginner, intermediate, expert.
              """
    prompt2 = PromptTemplate.from_template(prompt2)
    chain_two = LLMChain(llm=llm, prompt=prompt2, output_key="plan")

    prompt3 = """
              Take in a weekly workout plan: {plan}.
              Give it back in the format of a Python dictionary, where each day is a key. The value of each key is the information
              associated with it in the format of a python dictionary where exercise_type, muscle_group, and difficulty are the keys.
              Make sure to only include the dictionary in your response without including any other text.
              """
    prompt3 = PromptTemplate.from_template(prompt3)
    chain_three = LLMChain(llm=llm, prompt=prompt3)
    overall_chain = SequentialChain(
        chains=[chain, chain_two, chain_three],
        input_variables=[
            "age",
            "gender",
            "current_weight",
            "height",
            "impediments",
            "target_weight",
            "fitness_goal",
        ],
        verbose=True,
    )
    response = overall_chain(
        {
            "age": age,
            "gender": gender,
            "current_weight": current_weight,
            "height": height,
            "impediments": impediments,
            "target_weight": target_weight,
            "fitness_goal": fitness_goal,
        }
    )
    return response


def get_results(
    age, gender, height, current_weight, target_weight, fitness_goal, impediments
):
    text = json.loads(
        set_up(
            age,
            gender,
            height,
            current_weight,
            target_weight,
            fitness_goal,
            impediments,
        )["text"]
    )
    output = {}
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    for count, day in zip(weekdays, text.values()):
        if day["exercise_type"] == "cardio":
            exercises = get_workout("cardio", "", day["difficulty"])
            temp = {}
            output[count] = exercises
        elif day["exercise_type"] == "strength":
            temp = {}
            for group in day["muscle_group"]:
                exercises = get_workout("strength", group, day["difficulty"])
                temp[group] = exercises
            output[count] = temp
        else:
            output[count] = "Rest"
    return output


weekly_workout_plan = get_results(19, "male", "6", "140", "160", "trim fat", "none")
