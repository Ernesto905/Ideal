from flask import Flask, render_template, url_for, request, redirect
from llm.openai_utils import get_completion
from openai import OpenAI
import dotenv

dotenv.load_dotenv()
client = OpenAI()

app = Flask(__name__)

# Frontend routes 
@app.route("/")
def home():
    return render_template('home/index.html')

@app.route("/builder")
def builder():
    return render_template('builder/index.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard/index.html')


# Backend routes (OPTIONAL: If decide to Auth, utilize Json web tokens 🤢🤮)
@app.route("/generate", methods=["GET", "POST"])
def generate():
    print("This should work")
    if request.method == "POST": 
        response = get_completion(request.form["user_input"])
        print(f"response is {response}")
        return redirect(url_for("generate", result=response))
    result = request.args.get("result")
    return render_template("index.html", result=result)


