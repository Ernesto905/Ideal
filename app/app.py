from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
)
from llm.openai_utils import (
    complete_workout,
    get_completion,
    test_backend_garv,
)
from llm.calculations import calculate_daily_recommendations, count_nutrients
from llm.recipe_utils import (
    display_recipes_grid,
    get_recipe_details,
    get_recipe_nutrients,
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
    return render_template("dashboard/index.html")

    # For when no more api :(
    # return render_template("dashboard/index.html")


@app.route("/get_nutrients", methods=["GET"])
def get_nutrients():
    return render_template("dashboard/nutrients_left.html")


# Backend routes
@app.route("/generate-workout", methods=["GET"])
def generate_workout():
    workout_list = complete_workout(session)
    return render_template("dashboard/workout.html", workout=workout_list)


@app.route("/generate-recipes", methods=["GET"])
def generate_recipes():
    recipes_list = display_recipes_grid(session)
    return render_template("dashboard/recipes.html", data=recipes_list)


@app.route("/test_backend_garv", methods=["GET", "POST"])
def test_the_backend_garv():
    user_input = request.form["user_input"]
    result_garv = test_backend_garv(session, user_input)
    return result_garv


@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        user_input = request.form["user_input"]
        # result_garv = test_backend_garv(session, user_input)
        response = get_completion(user_input)
        return f"<div id='chat-response' class='mb-3'>{response}</div>"
    return render_template("index.html")


@app.route("/recipes", methods=["GET"])
def recipes():
    if request.method == "GET":
        recipe_id = request.args.get("recipe_id")
        if recipe_id:
            session["recipe_data"] = get_recipe_details(recipe_id)
            return render_template("dashboard/recipe_details.html")
    return "Error", 404


@app.route("/update_nutrients", methods=["POST"])
def update_nutrients():
    recipe_id = request.args.get("recipe_id")
    recipe = get_recipe_nutrients(recipe_id)
    if recipe:
        count_nutrients(recipe, session)
        return render_template("dashboard/nutrients_left.html")
    return "Error", 404


if __name__ == "__main__":
    app.run(host="0.0.0.9")
