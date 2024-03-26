from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from llm.openai_utils import (
    get_completion,
    display_recipes,
    test_backend,
    test_backend_garv,
)
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
        session["body_composition"] = request.form.get("body_composition")
        session["archetype"] = request.form.get("archetype")
        session["age"] = request.form.get("age")
        session["sex"] = request.form.get("sex")
        session["allergies"] = request.form.get("allergies")
        session["diet"] = request.form.get("diet")
        session["religion"] = request.form.get("religion")
        session["anything_else_diet"] = request.form.get("anything_else")
        session["physical_impediments"] = request.form.get("physical_impediments")
        return redirect("/dashboard")
    return render_template("builder/index.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    recipes_list = display_recipes(session)
    return render_template("dashboard/index.html", data=recipes_list)


# Backend routes (OPTIONAL: If decide to Auth, utilize Json web tokens 🤢🤮)
@app.route("/test_backend", methods=["GET"])
def test_the_backend():
    result = test_backend(session)
    return result


@app.route("/test_backend_garv", methods=["GET"])
def test_the_backend_garv():
    result_garv = test_backend_garv(session)
    return result_garv


"""Commented out just in case we need it in the future"""
# @app.route("/test_backend_ernesto", methods=["GET"])
# def test_the_backend_ernesto():
#     result_ernesto = test_backend_ernesto(session)
#     return jsonify(result_ernesto)


# @app.route("/generate", methods=["GET", "POST"])
# def generate():
#     print("This should work")
#     if request.method == "POST":
#         response = get_completion(request.form["user_input"])
#         print(f"response is {response}")
#         return redirect(url_for("generate", result=response))
#     result = request.args.get("result")
#     return render_template("index.html", result=result)
