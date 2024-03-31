from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from llm.openai_utils import (
    get_completion,
    display_recipes,
    test_backend_garv,
)
from llm.calculations import calculate_daily_recommendations
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SESSIONS_SECRET")


# Frontend routes
@app.route("/")
def home():
    return render_template("home/index.html")


@app.route("/builder", methods=["GET", "POST"])
def builder():

    if request.method == "POST":
        session["current_weight"] = request.form.get("current_weight")
        session["ideal_weight"] = request.form.get("ideal_weight")
        session["body_goal"] = request.form.get("body_goal")
        session["age"] = request.form.get("age")
        session["height"] = request.form.get("height")
        session["sex"] = request.form.get("sex")
        session["allergies"] = request.form.get("allergies")
        session["diet"] = request.form.get("diet")
        session["religion"] = request.form.get("religion")
        session["anything_else_diet"] = request.form.get("anything_else")
        session["physical_impediments"] = request.form.get("physical_impediments")
        calculate_daily_recommendations(session)
        return redirect("/dashboard")
    return render_template("builder/index.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    print("Current Weight:", session["current_weight"])
    print("Ideal Weight:", session["ideal_weight"])
    print("Body Composition:", session["body_goal"])
    print("Age:", session["age"])
    print("Sex:", session["sex"])

    print("Allergies:", session["allergies"])
    print("Diet:", session["diet"])
    print("Religion:", session["religion"])

    # print("Anything Else (Diet):", session["anything_else_diet"])

    print("Physical Impediments:", session["physical_impediments"])

    print("Daily calories", session["daily_calories"])
    print("Daily protein", session["daily_protein_grams"])
    print("Daily carbs", session["daily_carbs_grams"])
    print("Daily fats", session["daily_fats_grams"])
    # For when Api is yes! :)
    recipes_list = display_recipes(session)
    # print(f"recipes is: {recipes_list}")
    return render_template("dashboard/index.html", data=recipes_list)

    # For when no more api :(
    return render_template("dashboard/index.html")


# Backend routes


@app.route("/test_backend_garv", methods=["GET", "POST"])
def test_the_backend_garv():
    user_input = request.form["user_input"]
    result_garv = test_backend_garv(session, user_input)
    return result_garv


@app.route("/generate", methods=["GET", "POST"])
def generate():
    print("------------------------------------------------------This should work")
    if request.method == "POST":
        user_input = request.form["user_input"]
        result_garv = test_backend_garv(session, user_input)
        print("Garv's answer ==========================",result_garv)
        response = get_completion(user_input)  # Assuming this function returns a string
        print(f"response is {response}")
        # Return HTML snippet for HTMX to inject
        return f"<div id='chat-response' class='mb-3'>{response}</div>"
    return render_template("index.html")
